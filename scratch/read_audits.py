import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

def inspect_notebook(path):
    p = Path(path)
    if not p.exists():
        print(f"File not found: {path}")
        return
    with open(p, "r", encoding="utf-8") as f:
        nb = json.load(f)
    print(f"\n=======================================================")
    print(f"INSPECTING: {p.name} ({len(nb.get('cells', []))} cells)")
    print(f"=======================================================")
    for i, cell in enumerate(nb.get("cells", [])):
        src = "".join(cell.get("source", []))
        cell_type = cell.get("cell_type", "")
        print(f"\n--- [{cell_type.upper()} Cell {i}] ---")
        print(src.strip())
        outputs = cell.get("outputs", [])
        for out in outputs:
            text = "".join(out.get("text", []))
            if text:
                print(f"\n   [Output]:\n{text.strip()[:1000]}")

if __name__ == "__main__":
    inspect_notebook("scratch/sota_cosmorin_why-1-is-1-arc-agi-3-gap-analysis/why-1-is-1-arc-agi-3-gap-analysis.ipynb")
