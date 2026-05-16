from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / '.env'
print('Checking .env at', env_path)
if not env_path.exists():
    print('not found')
    raise SystemExit(1)

with env_path.open(encoding='utf-8') as f:
    lines = list(f)
    for i, line in enumerate(lines[:200], start=1):
        print(i, repr(line))
    print('\n--- Scanning for keywords ---')
    for i, line in enumerate(lines, start=1):
        low = line.lower()
        if 'service key' in low or 'service_key' in low or 'supabase_service_role_key' in low:
            print('Found keyword on line', i, '->', repr(line))
            if ':' in line:
                print('Value:', line.split(':', 1)[1].strip())
            elif '=' in line:
                print('Value:', line.split('=', 1)[1].strip())
            break
    else:
        print('No service key line found during scan')
