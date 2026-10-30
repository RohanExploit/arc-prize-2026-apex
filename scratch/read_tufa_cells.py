import json
from pathlib import Path

p = Path("scratch/duck_fork/arc3-duck-flash-nvfp4-fork.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))
for idx in [0, 1, 7, 9, 13, 15]:
    cell = nb['cells'][idx]
    src = "".join(cell.get("source", []))
    print(f"=== CELL {idx} ===")
    print(src[:1000])
    print("\n" + "="*40 + "\n")
