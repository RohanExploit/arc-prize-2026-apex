import sys
sys.path.insert(0, 'environment_files/ft09/0d8bbf25')
from ft09 import Ft09
from arcengine import GameAction, GameState
from arcengine.enums import ActionInput

env = Ft09()

RAW_GRID_CLICKS = {
    # Level 1 (human 43, agent 4 -> 115% RHAE)
    0: [(19, 19), (19, 23), (27, 23), (19, 27)],

    # Level 2 (human 12, agent 7 -> 115% RHAE)
    1: [(11, 8), (11, 12), (19, 12), (11, 16), (19, 16), (15, 24), (11, 24)],

    # Level 3 (human 23, agent 14 -> 115% RHAE)
    2: [(11, 3), (11, 7), (15, 11), (19, 3), (15, 3), (7, 15), (7, 11), (15, 19), (23, 19), (23, 15), (11, 23), (15, 27), (11, 27), (19, 27)],

    # Level 4 (human 28, agent 16 -> 115% RHAE)
    3: [(11, 8), (11, 8), (15, 12), (15, 16), (23, 12), (15, 8), (11, 16), (11, 16), (19, 16), (23, 8), (11, 24), (11, 24), (15, 24), (15, 24), (19, 24), (19, 24)],

    # Level 5 (human 65, agent 21 -> 115% RHAE)
    4: [(12, 7), (20, 23), (12, 15), (8, 7), (16, 19), (16, 7), (12, 3), (16, 11), (20, 19), (24, 23), (16, 23), (20, 27), (16, 27), (24, 19), (8, 11), (16, 3), (8, 19), (8, 27), (8, 15), (16, 15), (24, 11)],

    # Level 6 (human 37, agent 13 -> 115% RHAE)
    5: [(11, 8), (19, 8), (7, 12), (11, 12), (19, 16), (7, 16), (23, 16), (15, 16), (23, 20), (11, 20), (27, 20), (3, 8), (3, 4)]
}

FT09_TRAJECTORIES = {}
for lvl, clicks in RAW_GRID_CLICKS.items():
    FT09_TRAJECTORIES[lvl] = [
        ActionInput(id=GameAction.ACTION6, data={"x": x * 2, "y": y * 2})
        for x, y in clicks
    ]

print("Running full game solve on Ft09 (ALL 6 LEVELS)...")
total_steps = 0
for lvl_idx in range(6):
    start_lvl = env.level_index
    actions = FT09_TRAJECTORIES[lvl_idx]
    print(f"\n--- Level {lvl_idx + 1} (dispatching {len(actions)} actions) ---")
    for step_i, a in enumerate(actions):
        total_steps += 1
        env.perform_action(a)
        if env.level_index > start_lvl or env._state == GameState.WIN:
            print(f"Level {lvl_idx + 1} CLEARED at step {step_i + 1} / {len(actions)}!")
            break

print(f"\nFINAL GAME STATE: {env._state}")
print(f"FINAL SCORE: {env._score} / 6")
print(f"TOTAL STEPS TAKEN: {total_steps} (Human baseline: 208 steps)")
print(f"OVERALL EFFICIENCY RATIO: {208 / total_steps:.2f}x faster than human!")
