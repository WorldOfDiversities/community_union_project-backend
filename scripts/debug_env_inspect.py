from pathlib import Path
import unicodedata

env = Path(__file__).resolve().parents[1] / '.env'
print('Reading', env)
text = env.read_text(encoding='utf-8')
lines = text.splitlines()
start = 30
end = 40
for i in range(start, end):
    if i < len(lines):
        line = lines[i]
        print(f"{i+1}: {repr(line)}")
    else:
        print(f"{i+1}: <no line>")

print('\n--- Codepoints for lines that mention "service" or "key" ---')
for i, line in enumerate(lines, start=1):
    if 'service' in line.lower() or 'key' in line.lower():
        print('\nLine', i, repr(line))
        for c in line:
            print(hex(ord(c)), unicodedata.name(c, ''))
        break
