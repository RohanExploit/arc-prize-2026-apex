import kaggle
from pathlib import Path

api = kaggle.KaggleApi()
api.authenticate()

targets = [
    'heliosli/try-merging-it-you-might-get-lucky-and-win-gold',
    'youdocare/the-agi-boys-fork-romantamrazov-35-35',
    'vickyfym/arc-agi-3-lalalia-final',
    'vickyfym/arc-agi-3-lalalia-dprime-m85tuned',
    'shiiin9/affectify-arc-31-54-in-a-single-sub',
    'weitaoguo/arc3-d-prime-plus-solved-level-memory',
    'habanwer/arcaid3-lexicon-dprime-dfranzen-m2',
    'lalalia9/arc3-franzen-v19',
    'cosmorin/why-1-is-1-arc-agi-3-gap-analysis',
    'kirilltym/arc3-persistent-python-verified-planning'
]

scratch = Path('e:/projects/arc-agi-3/scratch')
for t in targets:
    try:
        slug = t.replace('/', '_')
        dest = scratch / f'sota_{slug}'
        dest.mkdir(parents=True, exist_ok=True)
        api.kernels_pull(t, str(dest), metadata=True)
        print(f'Successfully pulled: {t}')
    except Exception as e:
        print(f'Failed {t}: {e}')
