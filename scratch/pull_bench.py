import kaggle
import os
from pathlib import Path

api = kaggle.KaggleApi()
api.authenticate()

targets = [
    'laimerbotrolenk/lb-score-31-21',
    'skarin/arc-agi-3-27-80-lb-100-trajectory-audit',
    'romantamrazov/the-agi-boys-i-am-better',
    'dfranzen/arc-agi-3-milestone-2-solution',
    'dennis6886/arc3-d-prime-public-base',
    'yongjiehishi/arc3-duck-lab-t06'
]

scratch = Path('e:/projects/arc-agi-3/scratch')
for t in targets:
    try:
        slug = t.replace('/', '_')
        dest = scratch / f'bench_{slug}'
        dest.mkdir(parents=True, exist_ok=True)
        api.kernels_pull(t, str(dest))
        print(f'Successfully pulled: {t}')
    except Exception as e:
        print(f'Failed {t}: {e}')
