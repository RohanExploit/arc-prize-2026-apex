import re

with open(r'E:\projects\arc-agi-3\scripts\dispatch_00utc.py', 'r', encoding='utf-8') as f:
    text = f.read()

tracks_v4 = '''TRACKS = [
    {
        "name": "Track 1 (Apex v4 Master): SGLang v4 (Deterministic 115% Physics Solvers + Hybrid SGLang Server)",
        "kernel": "rohanexploit/arc3-apex-sglang-v4-top-10-hybrid-master",
        "version": 1,
        "file": "submission.parquet",
        "message": "Autonomous Top-10 Push: SGLang v4 Master Hybrid (Target >= 46.82%)",
    },
    {
        "name": "Track 2 (Apex v3 Master): SGLang v3 (Spatial Masking + Token Governor + mem 0.88)",
        "kernel": "rohanexploit/arc3-apex-sglang-v3",
        "version": 1,
        "file": "submission.parquet",
        "message": "Autonomous Top-10 Push: SGLang v3 Master Apex (Target >= 46.82%)",
    },
]'''

text = re.sub(r'TRACKS = \[.*?\]\n', tracks_v4 + '\n', text, flags=re.DOTALL)

with open(r'E:\projects\arc-agi-3\scripts\dispatch_00utc.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('TRACKS updated cleanly!')
