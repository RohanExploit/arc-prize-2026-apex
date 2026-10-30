import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from pathlib import Path

scratch = Path('e:/projects/arc-agi-3/scratch')
for d in sorted(scratch.glob('sota_*')):
    print(f"\n==================== {d.name} ====================")
    meta_p = d / 'kernel-metadata.json'
    if meta_p.exists():
        meta = json.loads(meta_p.read_text(encoding='utf-8'))
        print("Title:", meta.get('title'))
        print("Datasets:", meta.get('dataset_sources'))
        print("Models:", meta.get('model_sources'))
    for nb_p in d.glob('*.ipynb'):
        nb = json.loads(nb_p.read_text(encoding='utf-8'))
        cells = nb.get('cells', [])
        print(f"Notebook: {nb_p.name} ({len(cells)} cells)")
        for idx, c in enumerate(cells[:8]):
            src = "".join(c.get('source', []))
            first_lines = "\n    ".join(src.splitlines()[:5])
            print(f"  Cell {idx} [{c.get('cell_type')} len={len(src)}]: {first_lines[:220]}")
