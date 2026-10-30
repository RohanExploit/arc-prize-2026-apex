import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

def analyze():
    with open("scratch/benchmark.json", "r", encoding="utf-8") as f:
        bench = json.load(f)
    game_runs = bench.get("game_runs", [])
    print(f"Total game runs recorded in competitor run: {len(game_runs)}")
    
    total_tokens = 0
    total_actions = 0
    
    for r in game_runs:
        g_id = r.get("game_id", "")
        state = r.get("state", "")
        levels = r.get("levels_completed", 0)
        num_levels = r.get("number_of_levels", 0)
        history = r.get("history", [])
        n_act = len(history)
        toks = sum(step.get("generated_tokens", 0) for step in history)
        total_tokens += toks
        total_actions += n_act
        
        # Check action distribution
        actions_used = [step.get("action", {}).get("id") for step in history]
        unique_actions = set(actions_used)
        
        print(f"\nGame: {g_id[:15]} | State: {state} | Levels: {levels}/{num_levels} | Steps: {n_act} | Tokens: {toks:,}")
        print(f"   Actions used: {list(unique_actions)}")
        if history:
            first_act = history[0].get("action")
            last_act = history[-1].get("action")
            print(f"   First action: {first_act}")
            print(f"   Last action: {last_act}")
            avg_tok_per_act = toks / max(1, n_act)
            print(f"   Avg tokens/action: {avg_tok_per_act:.1f}")

    print(f"\n=== TOTAL ACROSS ALL GAMES ===")
    print(f"Total actions: {total_actions}")
    print(f"Total tokens generated: {total_tokens:,}")

if __name__ == "__main__":
    analyze()
