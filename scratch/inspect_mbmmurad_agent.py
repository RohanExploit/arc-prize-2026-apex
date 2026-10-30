import json
import re
from pathlib import Path

p = Path("scratch/mbmmurad/arc-agi-3-lb-0-86-3rd-place-candidate-milestone.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))
cell3 = "".join(nb['cells'][3].get("source", []))

lines = cell3.split("\n")
print(f"Total lines in Cell 3: {len(lines)}")
classes = [line for line in lines if line.strip().startswith("class ")]
print("=== CLASSES FOUND ===")
for c in classes:
    print(c)

print("\n=== TOP 50 LINES ===")
for l in lines[:50]:
    print(l)
