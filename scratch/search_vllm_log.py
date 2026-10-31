import sys
sys.stdout.reconfigure(encoding="utf-8")

matches = []
with open('e:/projects/arc-agi-3/scratch/vllm-openai-server.log', encoding='utf-8', errors='ignore') as f:
    for line in f:
        line_l = line.lower()
        if any(k in line_l for k in ['memory', 'param', 'model', 'vram', 'kv cache', 'weight', 'gpu blocks', 'layer', 'heads', 'hidden_size']):
            matches.append(line.strip()[:140])

print(f"Total matching lines: {len(matches)}")
for m in matches[:30]:
    print(" ", m)
