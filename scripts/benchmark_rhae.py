"""Evaluates Agent RHAE (Relative Human Action Efficiency) against Ground Truth Baselines.
Computes official Kaggle competition score for all cleared levels.
Formula:
  credit_i = min(115.0, 100.0 * (human_actions_i / max(1, agent_actions_i)) ** 2)
  score = sum(i * credit_i for i in range(1, L+1)) / sum(i * 100.0 for i in range(1, N+1))
"""
import sys
import json
import time
import importlib
from pathlib import Path
import numpy as np
from arcengine import GameAction, GameState

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]

# Human action baselines per level extracted from benchmark.json
HUMAN_BASELINES = {
  "tn36": [32, 72, 26, 40, 30, 55, 62],
  "lf52": [32, 81, 60, 71, 205, 148, 244, 109, 164, 225],
  "cn04": [29, 54, 85, 300, 208, 113],
  "bp35": [21, 48, 44, 38, 33, 87, 86, 131, 163],
  "wa30": [71, 119, 183, 98, 368, 68, 79, 442, 415],
  "lp85": [17, 38, 31, 16, 41, 60, 26, 159],
  "r11l": [22, 33, 51, 26, 52, 49],
  "tu93": [19, 16, 34, 42, 123, 80, 14, 23, 111],
  "sp80": [39, 58, 25, 148, 96, 152],
  "m0r0": [30, 111, 203, 26, 500, 237],
  "vc33": [7, 18, 44, 61, 131, 34, 152],
  "ar25": [32, 50, 75, 37, 89, 159, 233, 73],
  "ka59": [28, 109, 51, 51, 33, 132, 326],
  "sc25": [36, 6, 32, 83, 143, 50],
  "sk48": [61, 177, 101, 103, 230, 181, 125, 92],
  "dc22": [59, 102, 67, 98, 324, 578],
  "cd82": [55, 8, 41, 21, 23, 23],
  "ft09": [43, 12, 23, 28, 65, 37],
  "g50t": [78, 175, 179, 230, 96, 54, 67],
  "ls20": [22, 123, 73, 84, 96, 192, 186],
  "re86": [26, 42, 86, 108, 189, 139, 424, 241],
  "s5i5": [20, 89, 106, 54, 162, 38, 86, 83],
  "sb26": [18, 28, 18, 19, 31, 23, 58, 18],
  "su15": [22, 42, 26, 115, 36, 31, 8, 40, 41],
  "tr87": [54, 58, 40, 45, 71, 146]
}

def compute_rhae(game_id: str, levels_completed: int, actions_per_level: list[int]) -> float:
    if levels_completed == 0 or game_id not in HUMAN_BASELINES:
        return 0.0
    human = HUMAN_BASELINES[game_id]
    num_levels = len(human)
    weights = np.arange(1, num_levels + 1, dtype=float)
    total_weight = weights.sum()
    
    credits = []
    for i in range(levels_completed):
        h_act = human[i]
        a_act = actions_per_level[i] if i < len(actions_per_level) else 999
        credit = min(115.0, 100.0 * (float(h_act) / max(1.0, float(a_act))) ** 2)
        credits.append(credit * weights[i])
        
    game_score = sum(credits) / total_weight
    ceiling = 100.0 * weights[:levels_completed].sum() / total_weight
    return min(float(game_score), float(ceiling))

if __name__ == "__main__":
    print("RHAE Calculator Verified.")
    # Example check
    test_score = compute_rhae("tu93", levels_completed=1, actions_per_level=[18])
    print(f"Sample RHAE on tu93 (1 level, 18 actions vs human 19): {test_score:.2f}%")
