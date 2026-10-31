import math
import sys
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

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

def credit_fn(h, a):
    return min(115.0, 100.0 * (float(h) / max(1.0, float(a))) ** 2)

sqrt_115 = math.sqrt(1.15)
inv_sqrt_115 = 1.0 / sqrt_115

print(f"sqrt(1.15) = {sqrt_115:.8f}")
print(f"1 / sqrt(1.15) = {inv_sqrt_115:.8f} (fraction of human actions allowed to cap)")

target_games = ["vc33", "tu93", "r11l", "lp85", "ft09"]

print("\n" + "="*80)
print("EXACT ACTION THRESHOLDS FOR 115% SCORE CAP ACROSS TARGET ARCHETYPES")
print("="*80)

for g in target_games:
    baselines = HUMAN_BASELINES[g]
    N = len(baselines)
    total_w = sum(range(1, N + 1))
    print(f"\n--- Game: {g} (N = {N} levels, sum weights = {total_w}) ---")
    rows = []
    for idx, h in enumerate(baselines):
        lv = idx + 1
        w = lv
        w_frac = w / total_w
        thresh_float = h * inv_sqrt_115
        thresh_int = math.floor(thresh_float)
        cred_at_thresh = credit_fn(h, thresh_int)
        cred_at_plus1 = credit_fn(h, thresh_int + 1)
        cred_at_human = credit_fn(h, h)
        drop_1 = cred_at_thresh - cred_at_plus1
        # derivative at human baseline: -200 / h
        deriv_human = -200.0 / h
        rows.append({
            "Level": lv,
            "Human (H)": h,
            "Float Thresh": f"{thresh_float:.2f}",
            "Max Cap Actions (A*)": thresh_int,
            "Credit @ A*": f"{cred_at_thresh:.2f}%",
            "Credit @ A*+1": f"{cred_at_plus1:.2f}%",
            "Drop (-Δ)": f"{drop_1:.2f}%",
            "Level Weight": f"{w_frac*100:.1f}%",
            "Game Impact/Act": f"{(drop_1 * w_frac):.3f}%",
            "dC/da @ H": f"{deriv_human:.2f}"
        })
    df = pd.DataFrame(rows)
    print(df.to_string(index=False))

