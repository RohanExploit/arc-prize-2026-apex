import json
from pathlib import Path

p = Path("scratch/foysal/lb-9-arc3-duck-v12-with-qwen-3-8-27b.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))
print(f"Total cells: {len(nb['cells'])}")
for idx, cell in enumerate(nb['cells'][:10]):
    src = "".join(cell.get("source", []))
    lines = src.split("\n")
    first_line = lines[0] if lines else ""
    print(f"Cell {idx} ({cell['cell_type']}): {first_line[:80]} ({len(lines)} lines)")
