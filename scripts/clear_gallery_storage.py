import os
from urllib.parse import urlparse


def load_env(path):
    data = {}
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                data[k.strip()] = v.strip()
    return data


def main():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    env_path = os.path.abspath(env_path)
    if not os.path.exists(env_path):
        print('.env not found at', env_path)
        return 1

    env = load_env(env_path)
    access_key = env.get('AWS_ACCESS_KEY_ID')
    secret_key = env.get('AWS_SECRET_ACCESS_KEY')
    bucket = env.get('AWS_STORAGE_BUCKET_NAME')
    endpoint = env.get('AWS_S3_ENDPOINT_URL')
    region = env.get('AWS_S3_REGION_NAME') or None

    if not (access_key and secret_key and bucket and endpoint):
        print('Missing storage credentials in .env')
        return 2

    # Normalize endpoint to root host (boto3 expects endpoint like https://<host>)
    parsed = urlparse(endpoint)
    endpoint_root = f"{parsed.scheme}://{parsed.netloc}"

    print('Using endpoint:', endpoint_root)
    print('Bucket:', bucket)

    try:
        import boto3
        from botocore.client import Config
    except Exception as e:
        print('boto3 not installed:', e)
        return 3

    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_root,
        config=Config(signature_version='s3v4'),
        region_name=region,
    )

    prefix = 'Gallery/'
    print('Deleting objects with prefix:', prefix)

    deleted = 0
    continuation_token = None
    while True:
        if continuation_token:
            resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

        contents = resp.get('Contents') or []
        if not contents:
            break

        # collect keys
        keys = [{'Key': obj['Key']} for obj in contents]
        # delete in a single batch
        resp_del = s3.delete_objects(Bucket=bucket, Delete={'Objects': keys})
        del_count = len(resp_del.get('Deleted', []))
        deleted += del_count
        print(f"Deleted {del_count} objects in this batch")

        if resp.get('IsTruncated'):
            continuation_token = resp.get('NextContinuationToken')
        else:
            break

    print('Total deleted:', deleted)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
