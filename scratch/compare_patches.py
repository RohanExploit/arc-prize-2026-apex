import sys
sys.stdout.reconfigure(encoding='utf-8')
import json, difflib
from pathlib import Path

scratch = Path('e:/projects/arc-agi-3/scratch')

def get_nb_cells(p):
    nb = json.loads(Path(p).read_text(encoding='utf-8'))
    return ["".join(c.get('source', [])) for c in nb['cells']]

dfranzen_cells = get_nb_cells(scratch / 'bench_dfranzen_arc-agi-3-milestone-2-solution/arc-agi-3-milestone-2-solution.ipynb')
helios_cells = get_nb_cells(scratch / 'sota_heliosli_try-merging-it-you-might-get-lucky-and-win-gold/try-merging-it-you-might-get-lucky-and-win-gold.ipynb')
agi3535_cells = get_nb_cells(scratch / 'sota_youdocare_the-agi-boys-fork-romantamrazov-35-35/the-agi-boys-fork-romantamrazov-35-35.ipynb')

print("=== DIFF: dfranzen vs heliosli ===")
for i, (c1, c2) in enumerate(zip(dfranzen_cells, helios_cells)):
    if c1 != c2:
        print(f"Cell {i} differs! (len {len(c1)} vs {len(c2)})")
        diff = list(difflib.unified_diff(c1.splitlines(), c2.splitlines(), lineterm='', n=2))
        print("\n".join(diff[:120]))

print("\n=== DIFF: dfranzen vs romantamrazov-35-35 ===")
for i, (c1, c2) in enumerate(zip(dfranzen_cells, agi3535_cells)):
    if c1 != c2:
        print(f"Cell {i} differs! (len {len(c1)} vs {len(c2)})")
        diff = list(difflib.unified_diff(c1.splitlines(), c2.splitlines(), lineterm='', n=2))
        print("\n".join(diff[:120]))
