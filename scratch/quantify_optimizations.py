import math
import sys
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

HUMAN_BASELINES = {
  "vc33": [7, 18, 44, 61, 131, 34, 152],
  "tu93": [19, 16, 34, 42, 123, 80, 14, 23, 111],
  "r11l": [22, 33, 51, 26, 52, 49],
  "lp85": [17, 38, 31, 16, 41, 60, 26, 159],
  "ft09": [43, 12, 23, 28, 65, 37],
}

def compute_game_rhae(game_id, actions_per_level):
    human = HUMAN_BASELINES[game_id]
    N = len(human)
    weights = np.arange(1, N + 1, dtype=float)
    total_w = weights.sum()
    
    L = len(actions_per_level)
    credits = []
    for i in range(L):
        h = human[i]
        a = actions_per_level[i]
        c = min(115.0, 100.0 * (float(h) / max(1.0, float(a))) ** 2)
        credits.append(c * weights[i])
    score = sum(credits) / total_w
    ceiling = 100.0 * weights[:L].sum() / total_w
    return min(float(score), float(ceiling))

print("="*80)
print("1. DEAD-SIGNATURE SPATIAL MASKING: EXACT RHAE SCORE IMPACT")
print("="*80)

# Pure Click Games: vc33, r11l, lp85, ft09
# Masking eliminates dead background clicks (typically 10-30 clicks per level)
# Let's evaluate across realistic empirical regimes:
# Case A: Optimal (at 115% cap threshold A*)
# Case B: Masked Centroid (agent clicks only real objects, 1.05x - 1.15x human actions)
# Case C: Unmasked Grid Probe (+15 wasted clicks per level)
# Case D: Unmasked Blind Search (+35 wasted clicks per level)

click_games = ["vc33", "r11l", "lp85", "ft09"]
for g in click_games:
    human = HUMAN_BASELINES[g]
    N = len(human)
    # A*: cap threshold
    a_cap = [math.floor(h / math.sqrt(1.15)) for h in human]
    # Masked: optimal clean clicks (~ human count or slightly better)
    a_masked = [math.floor(h * 0.95) for h in human]
    # Unmasked +15 clicks per level
    a_unmasked_15 = [h + 15 for h in human]
    # Unmasked +35 clicks per level
    a_unmasked_35 = [h + 35 for h in human]
    
    s_cap = compute_game_rhae(g, a_cap)
    s_masked = compute_game_rhae(g, a_masked)
    s_unmasked_15 = compute_game_rhae(g, a_unmasked_15)
    s_unmasked_35 = compute_game_rhae(g, a_unmasked_35)
    
    gain_15 = s_masked - s_unmasked_15
    gain_35 = s_masked - s_unmasked_35
    
    print(f"\nGame {g} (N={N}):")
    print(f"  Cap Score (A*):                {s_cap:.2f}%")
    print(f"  Masked Centroid Score:         {s_masked:.2f}%")
    print(f"  Unmasked (+15 wasted clicks):  {s_unmasked_15:.2f}%  --> Net Gain from Masking: +{gain_15:.2f}%")
    print(f"  Unmasked (+35 wasted clicks):  {s_unmasked_35:.2f}%  --> Net Gain from Masking: +{gain_35:.2f}%")

print("\n" + "="*80)
print("2. MACRO-ACTION CORRIDOR COMPRESSION: EXACT RHAE SCORE IMPACT ON TU93")
print("="*80)

# tu93 is a pure navigation maze game with 9 levels.
# In mazes, corridor compression eliminates:
# 1. 2-tile oscillation loops (forward/back steps)
# 2. Wall bumping / no-op direction tests
# Let's model tu93 level-by-level:
tu93_human = HUMAN_BASELINES["tu93"]
tu93_weights = np.arange(1, len(tu93_human) + 1, dtype=float)
tu93_tot_w = tu93_weights.sum()

# Empirical trajectory comparisons from benchmark / BFS explorer logs:
# Uncompressed: agent oscillates in corridors and bumps into walls -> ~2.2x to 3.0x human actions
# Semi-compressed (momentum only): ~1.3x to 1.5x human actions
# Fully compressed (macro run-length corridor compression): reaches optimal Dijkstra path (~0.90x to 1.0x human actions)

scenarios = {
    "Macro Compressed (A* Cap)": [math.floor(h / math.sqrt(1.15)) for h in tu93_human],
    "Macro Compressed (Optimal Dijkstra, ~0.95h)": [math.floor(h * 0.95) for h in tu93_human],
    "Momentum Traversal (~1.25h)": [math.floor(h * 1.25) for h in tu93_human],
    "Uncompressed Wandering (~2.0h)": [math.floor(h * 2.00) for h in tu93_human],
    "Oscillation Loop Trap (~3.0h)": [math.floor(h * 3.00) for h in tu93_human],
}

tu_rows = []
for name, acts in scenarios.items():
    score = compute_game_rhae("tu93", acts)
    credits = [min(115.0, 100.0 * (h / a)**2) for h, a in zip(tu93_human, acts)]
    tu_rows.append({
        "Scenario": name,
        "Total Actions": sum(acts),
        "Avg Level Credit": f"{np.mean(credits):.2f}%",
        "Final RHAE Score": f"{score:.2f}%"
    })

df_tu = pd.DataFrame(tu_rows)
print(df_tu.to_string(index=False))

# Now detail level-by-level for tu93 comparing Uncompressed (2.0x) vs Macro Compressed (0.95x)
print("\nTU93 Level-by-Level Breakdown (Uncompressed 2.0x vs Macro Compressed 0.95x):")
tu_detail = []
for i, h in enumerate(tu93_human):
    lv = i + 1
    w = lv
    w_frac = w / tu93_tot_w
    a_comp = math.floor(h * 0.95)
    a_uncomp = math.floor(h * 2.0)
    c_comp = min(115.0, 100.0 * (h / a_comp)**2)
    c_uncomp = min(115.0, 100.0 * (h / a_uncomp)**2)
    delta_c = c_comp - c_uncomp
    game_contrib = delta_c * w_frac
    tu_detail.append({
        "Level": lv,
        "Human": h,
        "Comp Act": a_comp,
        "Comp Cred": f"{c_comp:.1f}%",
        "Uncomp Act": a_uncomp,
        "Uncomp Cred": f"{c_uncomp:.1f}%",
        "Credit Gain": f"+{delta_c:.1f}%",
        "Weight": f"{w_frac*100:.1f}%",
        "Net Game Score Gain": f"+{game_contrib:.2f}%"
    })
df_detail = pd.DataFrame(tu_detail)
print(df_detail.to_string(index=False))
print(f"Total Net Game Score Gain on tu93 from Corridor Compression: +{sum(float(r['Net Game Score Gain'].replace('+', '').replace('%', '')) for r in tu_detail):.2f}%")

