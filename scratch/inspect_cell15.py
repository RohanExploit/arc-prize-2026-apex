import json
from pathlib import Path

p = Path("scratch/duck_fork/arc3-duck-flash-nvfp4-fork.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))
cell15 = "".join(nb['cells'][15].get("source", []))
lines = cell15.split("\n")
print(f"Total lines in Cell 15: {len(lines)}")
for idx, l in enumerate(lines[100:160], start=100):
    print(f"{idx}: {l}")
