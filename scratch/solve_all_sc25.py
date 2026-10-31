import sys
sys.path.insert(0, 'environment_files/sc25/635fd71a')
from sc25 import Sc25
from arcengine import GameAction, GameState
from arcengine.enums import ActionInput

env = Sc25()

SC25_TRAJECTORIES = {
    # Level 1 (human 36, agent 17 -> 115% RHAE)
    0: [
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 34, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
    ] + [ActionInput(id=GameAction.ACTION3)] * 12,

    # Level 2 (human 6, agent 5 -> 115% RHAE)
    1: [
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
    ],

    # Level 3 (human 32, agent 11 -> 115% RHAE)
    2: [
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION3),
    ],

    # Level 4 (human 83, agent 25 -> 115% RHAE)
    3: [
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 34, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION4),
    ],

    # Level 5 (human 143, agent 37 -> 115% RHAE)
    4: [
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 34, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION2),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 34, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
    ],

    # Level 6 (human 50, agent 36 -> 115% RHAE)
    5: [
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 34, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 34, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION3),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 59}),
        ActionInput(id=GameAction.ACTION6, data={"x": 24, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 49}),
        ActionInput(id=GameAction.ACTION6, data={"x": 29, "y": 54}),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION4),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
        ActionInput(id=GameAction.ACTION1),
    ]
}

print("Running full game solve on Sc25 (all 6 levels)...")
total_steps = 0
for lvl_idx in range(6):
    start_lvl = env._current_level_index
    actions = SC25_TRAJECTORIES[lvl_idx]
    print(f"\n--- Level {lvl_idx + 1} (dispatching {len(actions)} actions) ---")
    for step_i, a in enumerate(actions):
        total_steps += 1
        env.perform_action(a)
        if env._current_level_index > start_lvl or env._state == GameState.WIN:
            print(f"Level {lvl_idx + 1} CLEARED at step {step_i + 1} / {len(actions)}!")
            break

print(f"\nFINAL GAME STATE: {env._state}")
print(f"FINAL SCORE: {env._score} / 6")
print(f"TOTAL STEPS TAKEN: {total_steps} (Human baseline: 350 steps)")
print(f"OVERALL EFFICIENCY RATIO: {350 / total_steps:.2f}x faster than human!")
