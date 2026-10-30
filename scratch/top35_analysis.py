import sys
sys.stdout.reconfigure(encoding='utf-8')
import zipfile, pandas as pd
from pathlib import Path

zip_file = Path('e:/projects/arc-agi-3/scratch/lb_check/arc-prize-2026-arc-agi-3.zip')
with zipfile.ZipFile(zip_file) as z:
    df = pd.read_csv(z.open(z.namelist()[0]))

print("=== TOP 35 TEAMS ===")
for idx, row in df.head(35).iterrows():
    r = int(row['Rank'])
    t = row['TeamName']
    s = float(row['Score'])
    c = int(row['SubmissionCount'])
    print(f"Rank {r:2d}: {t:35s} | Score: {s:6.2f}% | Subs: {c}")
