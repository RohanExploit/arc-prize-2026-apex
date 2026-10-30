import sys
import json

sys.stdout.reconfigure(encoding="utf-8")

with open("notebooks/arc3-apex-sglang-v2/arc3-apex-sglang-v2.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell_idx in [3, 17, 21]:
    cell = nb["cells"][cell_idx]
    src = "".join(cell.get("source", []))
    print(f"\n=================== CELL {cell_idx} ===================")
    print(src[:1200])
