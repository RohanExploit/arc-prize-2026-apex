import sys
import json

sys.stdout.reconfigure(encoding="utf-8")

with open("notebooks/arc3-apex-sglang-v2/arc3-apex-sglang-v2.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Total cells in apex v2: {len(nb.get('cells', []))}")
for i, cell in enumerate(nb.get("cells", [])):
    src = "".join(cell.get("source", []))
    for k in ["M85", "PRIORITY", "taaf", "SCHEMA", "fast_commit", "dead", "probe", "token"]:
        if k.lower() in src.lower():
            first_line = src.strip().splitlines()[0] if src.strip() else ""
            print(f"Cell {i} [{cell.get('cell_type')}]: {first_line[:100]}")
            break
