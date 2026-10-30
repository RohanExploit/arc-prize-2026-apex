import json
import re
from pathlib import Path

p = Path("scratch/mbmmurad/arc-agi-3-lb-0-86-3rd-place-candidate-milestone.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))
full_text = ""
for cell in nb['cells']:
    full_text += "".join(cell.get("source", [])) + "\n"

matches = re.findall(r"/kaggle/input/[^\s\'\"\;\)\:]+", full_text)
print("=== KAGGLE INPUT PATHS IN MBMMURAD ===")
for m in sorted(set(matches)):
    print(m)
