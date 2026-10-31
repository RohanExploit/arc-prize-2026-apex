
from pathlib import Path
txt = Path('e:/projects/arc-agi-3/agent/my_agent.py').read_text(encoding='utf-8')
for line in txt.splitlines():
    if any(k in line.lower() for k in ['mask', 'diff', 'action6', 'stride', 'move', 'frontier', 'receptacle']):
        print(line[:100])
