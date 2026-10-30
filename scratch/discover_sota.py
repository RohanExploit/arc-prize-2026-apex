import sys
sys.stdout.reconfigure(encoding='utf-8')
import kaggle

api = kaggle.KaggleApi()
api.authenticate()

print("=== RECENT KERNELS BY DATE RUN (Page 1 & 2) ===")
for page in [1, 2, 3]:
    ks = api.kernels_list(competition='arc-prize-2026-arc-agi-3', sort_by='dateRun', page=page, page_size=50)
    for k in ks:
        votes = getattr(k, 'total_votes', 0)
        print(f"{k.ref:55s} | votes={votes:3d} | {k.title}")

print("\n=== SEARCH KERNELS FOR: 35, 36, 37, 38, 39, 40, lora, ple, thinkingcap, v19, dprime ===")
for kw in ['lora', 'ple', 'thinkingcap', 'albucino', 'dprime', 'v19', '32', '33', '34', '35', '38', '40']:
    ks = api.kernels_list(competition='arc-prize-2026-arc-agi-3', search=kw, page_size=20)
    if ks:
        print(f"--- Keyword: {kw} ---")
        for k in ks:
            print(f"  {k.ref:55s} | votes={getattr(k, 'total_votes', 0):3d} | {k.title}")
