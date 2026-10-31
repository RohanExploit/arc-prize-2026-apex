import glob, re
from pathlib import Path

for root_dir in ['e:/projects/arc-agi-3/agent', 'e:/projects/arc-agi-3/scripts', 'e:/projects/arc-agi-3/scratch']:
    for fpath in Path(root_dir).glob('**/*.py'):
        try:
            txt = fpath.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for term in ['dead-signature', 'dead_signature', 'corridor', 'macro_action', 'macro-action', 'anti_deliberation', 'anti-deliberation']:
            if term in txt.lower():
                print(f'{fpath} matched "{term}"')
