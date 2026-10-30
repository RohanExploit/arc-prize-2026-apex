import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import zipfile
import kaggle
import pandas as pd
from pathlib import Path

api = kaggle.KaggleApi()
api.authenticate()

scratch = Path('e:/projects/arc-agi-3/scratch')
scratch.mkdir(exist_ok=True)
dest = scratch / 'lb_check'
dest.mkdir(exist_ok=True)

api.competition_leaderboard_download('arc-prize-2026-arc-agi-3', str(dest))
zip_file = dest / 'arc-prize-2026-arc-agi-3.zip'
if zip_file.exists():
    with zipfile.ZipFile(zip_file) as z:
        csv_name = z.namelist()[0]
        df = pd.read_csv(z.open(csv_name))
    
    total_teams = len(df)
    rohan = df[df['TeamName'] == 'ROHAN Exploit']
    if not rohan.empty:
        r = rohan.iloc[0]
        rank = int(r['Rank'])
        score = float(r['Score'])
        percentile = (rank / total_teams) * 100
        print(f"TEAM: ROHAN Exploit")
        print(f"CURRENT RANK: {rank} / {total_teams} (Top {percentile:.1f}%)")
        print(f"CURRENT SCORE: {score:.2f}%")
    else:
        print("Team not found in leaderboard CSV")

    # Top 20 threshold
    if len(df) >= 20:
        row20 = df.iloc[19]
        row1 = df.iloc[0]
        print(f"RANK 1: {row1['TeamName']} - {float(row1['Score']):.2f}%")
        print(f"RANK 20 CUTOFF: {row20['TeamName']} - {float(row20['Score']):.2f}%")
    
    # Context around our rank
    if not rohan.empty:
        start_idx = max(0, rank - 4)
        end_idx = min(total_teams, rank + 3)
        print("\n--- Surrounding Teams ---")
        for idx in range(start_idx, end_idx):
            row = df.iloc[idx]
            marker = ">>>" if row['TeamName'] == 'ROHAN Exploit' else "   "
            print(f"{marker} Rank {int(row['Rank'])}: {row['TeamName']} - {float(row['Score']):.2f}%")
