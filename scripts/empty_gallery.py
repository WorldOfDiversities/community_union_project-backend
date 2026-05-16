import os
import sys
from pathlib import Path
import re
import json
import urllib.parse
import requests

try:
    import boto3
    from botocore.config import Config
except ImportError:
    print('boto3 not installed, please install (pip install boto3)')
    sys.exit(1)

# Load .env-like file
env_path = Path(__file__).resolve().parents[1] / '.env'
if not env_path.exists():
    print('Could not find .env at', env_path)
    sys.exit(1)

conf = {}
with env_path.open() as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k, v = line.split('=', 1)
            conf[k.strip()] = v.strip()

AWS_KEY = conf.get('AWS_ACCESS_KEY_ID')
AWS_SECRET = conf.get('AWS_SECRET_ACCESS_KEY')
BUCKET = conf.get('AWS_STORAGE_BUCKET_NAME')
ENDPOINT = conf.get('AWS_S3_ENDPOINT_URL')
REGION = conf.get('AWS_S3_REGION_NAME') or None

if not (AWS_KEY and AWS_SECRET and BUCKET and ENDPOINT):
    print('Missing required storage credentials in .env')
    sys.exit(1)

# Supabase endpoint provided may include a path like /storage/v1/s3; boto3 expects base endpoint
endpoint_base = ENDPOINT

print('Using endpoint:', endpoint_base)
print('Bucket:', BUCKET)

# Attempt to extract a Supabase service role key from .env (supports 'service key:' fallback)
service_key = None
# More tolerant extraction: support lines like
# "service key: <token>", "service_key=<token>", "SUPABASE_SERVICE_ROLE_KEY=<token>",
# and variants with leading whitespace. Also accept an "anon public key" fallback if present.
import re
# Try several tolerant strategies to find the service role key in .env
token_re = re.compile(r"[A-Za-z0-9_\-\.=]{20,}")
with env_path.open(encoding='utf-8') as f:
    lines = f.readlines()

    # Strategy 1: case-insensitive key label on a single line (robust to weird whitespace)
    label_re = re.compile(r"(?i)(?:service\W*key|supabase_service_role_key|supabase_service_role|anon\W*public\W*key)")
    for line in lines:
        if label_re.search(line):
            t = token_re.search(line)
            if t:
                candidate = t.group(0).strip().strip('"\'')
                if len(candidate) > 20:
                    service_key = candidate
                    break

    # Strategy 2: look for 'service key' and then take the next long token anywhere in the file
    if not service_key:
        text = ''.join(lines)
        m = re.search(r"(?i)(?:service\W*key|supabase_service_role_key|anon\W*public\W*key)\W*[:=\-\s,]*([A-Za-z0-9_\-\.=]{20,})", text)
        if m:
            service_key = m.group(1).strip().strip('"\'')

    # Strategy 3: fallback to parsed conf dict entries
    if not service_key:
        for k in ('SUPABASE_SERVICE_ROLE_KEY', 'SERVICE_ROLE_KEY', 'SERVICE_KEY', 'ANON_PUBLIC_KEY'):
            if k in conf:
                service_key = conf[k].strip().strip('"\'')
                break

if service_key:
    print('Using Supabase service role key for REST API operations')
    # Build supabase base URL from the endpoint host (replace .storage.supabase.co -> .supabase.co)
    parsed = urllib.parse.urlparse(ENDPOINT)
    project_host = parsed.netloc.replace('.storage.supabase.co', '.supabase.co')
    base_url = f"{parsed.scheme}://{project_host}"
    headers = {'Authorization': f'Bearer {service_key}', 'apikey': service_key}

    prefixes = ['Gallery/', 'gallery/']
    total_deleted = 0
    for prefix in prefixes:
        print('\nListing objects with prefix:', prefix)
        list_url = f"{base_url}/storage/v1/object/list/{BUCKET}"
        payload = {'prefix': prefix}
        resp = requests.post(list_url, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            print('Failed to list objects:', resp.status_code, resp.text)
            continue
        objs = resp.json() or []
        if not objs:
            print('No objects found for prefix', prefix)
            continue
        print(f'Found {len(objs)} objects; deleting...')
        for obj in objs:
            name = obj.get('name') or obj.get('Key') or obj.get('key')
            if not name:
                continue
            del_url = f"{base_url}/storage/v1/object/{BUCKET}/{urllib.parse.quote(name, safe='')}"
            dresp = requests.delete(del_url, headers=headers, timeout=30)
            if dresp.status_code in (200, 204):
                total_deleted += 1
                print('Deleted', name)
            else:
                print('Failed to delete', name, dresp.status_code, dresp.text)

    print('\nTotal deleted objects:', total_deleted)
    print('Done.')
else:
    print('Service role key not found in .env; cannot use REST API. Exiting.')
    sys.exit(1)
