import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
from pathlib import Path

scratch = Path('e:/projects/arc-agi-3/scratch')

def dump_nb(folder, nb_name, max_cell_len=8000):
    p = scratch / folder / nb_name
    nb = json.loads(p.read_text(encoding='utf-8'))
    print(f"\n################################################################")
    print(f"### {folder} / {nb_name}")
    print(f"################################################################")
    for idx, c in enumerate(nb['cells']):
        src = "".join(c.get('source', []))
        if len(src) > 100000:
            print(f"\n--- Cell {idx} [{c.get('cell_type')}] (HUGE: {len(src)} chars, first 600 chars) ---")
            print(src[:600])
        else:
            print(f"\n--- Cell {idx} [{c.get('cell_type')}] ({len(src)} chars) ---")
            print(src[:max_cell_len])

dump_nb('sota_cosmorin_why-1-is-1-arc-agi-3-gap-analysis', 'why-1-is-1-arc-agi-3-gap-analysis.ipynb', 10000)
dump_nb('sota_vickyfym_arc-agi-3-lalalia-dprime-m85tuned', 'arc-agi-3-lalalia-dprime-m85tuned.ipynb', 6000)
dump_nb('sota_habanwer_arcaid3-lexicon-dprime-dfranzen-m2', 'arcaid3-lexicon-dprime-dfranzen-m2.ipynb', 6000)
dump_nb('sota_kirilltym_arc3-persistent-python-verified-planning', 'arc3-persistent-python-verified-planning.ipynb', 6000)
