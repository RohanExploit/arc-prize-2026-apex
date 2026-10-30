import sys
import kaggle

sys.stdout.reconfigure(encoding='utf-8')
api = kaggle.KaggleApi()
api.authenticate()
ks = api.kernels_list(competition='arc-prize-2026-arc-agi-3', page_size=25, sort_by='voteCount')
print("=== TOP ARC-AGI-3 NOTEBOOKS BY VOTES ===")
for k in ks:
    votes = getattr(k, 'total_votes', getattr(k, 'totalVotes', 'N/A'))
    print(f"{k.ref} | votes: {votes} | title: {k.title}")
