import json
from pathlib import Path

def get_cells(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    return nb.get('cells', [])

nb_dfranzen = get_cells('e:/projects/arc-agi-3/scratch/bench_dfranzen_arc-agi-3-milestone-2-solution/arc-agi-3-milestone-2-solution.ipynb')
nb_3121 = get_cells('e:/projects/arc-agi-3/scratch/bench_laimerbotrolenk_lb-score-31-21/lb-score-31-21.ipynb')
nb_dprime = get_cells('e:/projects/arc-agi-3/scratch/bench_dennis6886_arc3-d-prime-public-base/arc3-d-prime-public-base.ipynb')

print(f"dfranzen cells: {len(nb_dfranzen)}")
print(f"31.21 cells: {len(nb_3121)}")
print(f"dprime cells: {len(nb_dprime)}")

# Look at dataset sources attached in metadata
for name in ['bench_dfranzen_arc-agi-3-milestone-2-solution', 'bench_laimerbotrolenk_lb-score-31-21', 'bench_dennis6886_arc3-d-prime-public-base']:
    meta_p = Path('e:/projects/arc-agi-3/scratch') / name / 'kernel-metadata.json'
    if meta_p.exists():
        with open(meta_p, 'r') as f:
            meta = json.load(f)
        print(f"\n{name} datasets: {meta.get('dataset_sources')}")

# Print first markdown cell or title/notes of 31.21
print("\n--- 31.21 Header / Description ---")
for c in nb_3121[:5]:
    src = "".join(c.get('source', []))
    print(f"[{c.get('cell_type')}]: {src[:200]}")
