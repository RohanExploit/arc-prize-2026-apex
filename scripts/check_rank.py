import kaggle
import sys

def check():
    api = kaggle.KaggleApi()
    api.authenticate()
    print("=== RECENT SUBMISSIONS ===")
    subs = api.competition_submissions("arc-prize-2026-arc-agi-3")
    for s in subs[:10]:
        print(f"Ref: {s.ref} | Date: {s.date} | Status: {s.status} | Score: {getattr(s, 'public_score', getattr(s, 'publicScore', 'N/A'))} | Desc: {s.description}")

    print("\n=== LEADERBOARD STANDING ===")
    lb = api.competition_leaderboard_view("arc-prize-2026-arc-agi-3")
    print(f"Total teams on leaderboard: {len(lb)}")
    found = False
    for rank, entry in enumerate(lb, start=1):
        entry_str = str(entry).lower()
        if "rohan" in entry_str or "duck" in entry_str:
            print(f"Rank {rank}: {entry}")
            found = True
    if not found:
        print("Username/team name not directly matched in visible top entries, checking best score cutoff...")
        # Print top 10 and bottom around 3.4%
        scores = [getattr(e, 'score', None) for e in lb[:10]]
        print(f"Top 10 scores: {scores}")

if __name__ == "__main__":
    check()
