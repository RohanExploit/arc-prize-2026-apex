import json
from pathlib import Path

p = Path("scratch/foysal/lb-9-arc3-duck-v12-with-qwen-3-8-27b.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))

for idx in [3, 8]:
    src = "".join(nb['cells'][idx].get("source", []))
    print(f"=== CELL {idx} ===")
    print(src[:1200])
    print("\n" + "="*40 + "\n")
