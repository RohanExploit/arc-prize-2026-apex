import json
from pathlib import Path

p = Path("scratch/mbmmurad/arc-agi-3-lb-0-86-3rd-place-candidate-milestone.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))

for idx in [1, 2, 4, 5]:
    src = "".join(nb['cells'][idx].get("source", []))
    print(f"=== CELL {idx} ===")
    print(src[:800])
    print("\n" + "="*40 + "\n")
