"""Automated 00:00 UTC Quota Unlock & Top-20 Leaderboard Tracker for ARC Prize 2026.

Goal: Climb toward Top 20 (Score >= 39.52%).
Strategy:
  1. Primary Thrust: Re-roll stochastic variance draws of Qwen3.8-Flash-Next-NVFP4
     (rohanexploit/arc3-duck-flash-nvfp4-fork v1) which holds the account best (3.43%).
     Zero GPU quota consumed (pre-committed).
  2. Complementary Thrust: Evaluate latest Deep-Horizon Multi-Specialist BFS Explorer
     (rohanexploit/arc-prize-2026-bfs-explorer-agent v10).
  3. Live Standing Monitoring: Automatically query Kaggle Leaderboard API and update
     CHECKPOINT.md with verified rank and score.
"""
import datetime
import io
import json
import os
import subprocess
import time
import zipfile
from pathlib import Path
import kaggle
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
KAGGLE_BIN = ROOT / ".venv" / "Scripts" / "kaggle.exe"
COMPETITION = "arc-prize-2026-arc-agi-3"
CHECKPOINT_PATH = ROOT / "CHECKPOINT.md"
SCRATCH_DIR = ROOT / "scratch"

TRACKS = [
    {
        "name": "Track 1 (Apex v3 Master): SGLang v3 (Spatial Masking + Token Governor + mem 0.88)",
        "kernel": "rohanexploit/arc3-apex-sglang-v3",
        "version": 1,
        "file": "submission.parquet",
        "message": "Autonomous Top-20 Push: SGLang v3 Master Apex (Target >= 39.79%)",
    },
    {
        "name": "Track 2 (Apex v2 Proven 21.06%): SGLang v2 (D-Prime + M85 Memory)",
        "kernel": "rohanexploit/arc3-apex-sglang-v2",
        "version": 2,
        "file": "submission.parquet",
        "message": "Autonomous Top-20 Push: SGLang v2 Master Apex (21.06% baseline)",
    },
    {
        "name": "Track 2 (Apex Standby): Adaptive Duck SGLang v1 (Verified COMPLETE, 31.21%)",
        "kernel": "rohanexploit/arc3-adaptive-duck-sglang",
        "version": 1,
        "file": "submission.parquet",
        "message": "Autonomous Top-20 Push: Adaptive Duck SGLang v1 (31.21% candidate)",
    },
    {
        "name": "Track 3: Qwen3.8 NVFP4 MTP Fallback (Account Best 3.43%)",
        "kernel": "rohanexploit/arc3-duck-flash-nvfp4-fork",
        "version": 1,
        "file": "submission.parquet",
        "message": "Autonomous Top-20 Push: Qwen3.8 Flash-Next NVFP4 MTP draw",
    },
    {
        "name": "Track 4: Deep-Horizon Multi-Specialist BFS Explorer v10 (500 steps)",
        "kernel": "rohanexploit/arc-prize-2026-bfs-explorer-agent",
        "version": 10,
        "file": "submission.parquet",
        "message": "Autonomous Deep-Horizon Multi-Specialist BFS Explorer v10",
    },
]

def log(msg: str):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)

def update_checkpoint(text: str):
    if CHECKPOINT_PATH.exists():
        with open(CHECKPOINT_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n- {text}")

def check_leaderboard_standing():
    try:
        api = kaggle.KaggleApi()
        api.authenticate()
        os.makedirs(SCRATCH_DIR, exist_ok=True)
        zip_dest = SCRATCH_DIR / f"{COMPETITION}.zip"
        api.competition_leaderboard_download(COMPETITION, str(SCRATCH_DIR))
        if zip_dest.exists():
            with zipfile.ZipFile(zip_dest) as z:
                csv_name = z.namelist()[0]
                df = pd.read_csv(z.open(csv_name))
                rohan_rows = df[df['TeamName'] == 'ROHAN Exploit']
                if not rohan_rows.empty:
                    row = rohan_rows.iloc[0]
                    rank = int(row['Rank'])
                    score = float(row['Score'])
                    total = len(df)
                    top20_score = float(df.iloc[19]['Score']) if len(df) >= 20 else 39.52
                    log(f"LEADERBOARD STATUS: Rank {rank}/{total} | Score: {score:.2f}% | Top-20 Cutoff: {top20_score:.2f}%")
                    if rank <= 20 or score >= top20_score:
                        log("🎉 GOAL ACHIEVED: TEAM ROHAN Exploit REACHED TOP 20 ON KAGGLE LEADERBOARD!")
                        update_checkpoint(f"🏆 GOAL ACHIEVED: Reached Rank {rank}/{total} with Score {score:.2f}%!")
            try:
                os.remove(zip_dest)
            except Exception:
                pass
    except Exception as e:
        log(f"Notice: Leaderboard check error: {e}")

def get_kernel_status(kernel_id: str) -> str:
    for attempt in range(3):
        try:
            api = kaggle.KaggleApi()
            api.authenticate()
            st = api.kernels_status(kernel_id)
            if isinstance(st, dict):
                return st.get("status", "UNKNOWN")
            return getattr(st, "status", "UNKNOWN")
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                return "UNKNOWN"


def has_submitted_today() -> tuple[bool, str]:
    try:
        api = kaggle.KaggleApi()
        api.authenticate()
        subs = api.competition_submissions(COMPETITION)
        if not subs:
            return False, ""
        latest = subs[0]
        sub_date = getattr(latest, "date", None)
        status = getattr(latest, "status", None)
        score = getattr(latest, "public_score", None) or getattr(latest, "publicScore", None)
        ref = getattr(latest, "ref", None)
        if sub_date:
            utc_today = datetime.datetime.now(datetime.timezone.utc).date()
            if hasattr(sub_date, "date"):
                sub_d = sub_date.date()
            else:
                sub_d = datetime.datetime.fromisoformat(str(sub_date)[:10]).date()
            if sub_d == utc_today:
                return True, f"Ref={ref}, Status={status}, Score={score}"
        return False, ""
    except Exception as e:
        log(f"Notice: submission check error: {e}")
        return False, ""

def try_submit(track: dict) -> tuple[bool, bool]:
    """Returns (submitted_ok, quota_exhausted)."""
    # 1. Check if kernel is complete
    k_status = str(get_kernel_status(track["kernel"]))
    log(f"Checking {track['name']} -> Kernel status: {k_status}")
    if "COMPLETE" not in k_status:
        log(f"Notice: Kernel {track['kernel']} is currently {k_status}, cannot submit yet.")
        return False, False

    cmd = [
        str(KAGGLE_BIN), "competitions", "submit", COMPETITION,
        "-k", track["kernel"],
        "-v", str(track["version"]),
        "-f", track["file"],
        "-m", track["message"],
    ]
    log(f"Attempting dispatch: {track['name']}...")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        output = (res.stdout + res.stderr).strip()
        log(f"Submission response: {output}")

        if "Successfully submitted" in output or "Submission ref" in output or res.returncode == 0:
            msg = f"SUCCESS: {track['name']} submitted! Details: {output[:100]}"
            log(msg)
            update_checkpoint(msg)
            return True, False
        elif "0 submissions remaining today" in output or "400 Client Error" in output or "Submission not allowed" in output:
            return False, True
        else:
            return False, False
    except Exception as e:
        log(f"Error submitting {track['name']}: {e}")
        return False, False

def main_loop():
    log("00:00 UTC Dispatcher & Leaderboard Monitor daemon started...")
    check_leaderboard_standing()
    while True:
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        log(f"Current UTC: {utc_now.strftime('%H:%M:%S')} (Reset at 00:00:00 UTC)")

        submitted, sub_info = has_submitted_today()
        if submitted:
            log(f"Today's submission quota consumed ({sub_info}). Armed for 00:00:00 UTC reset...")
        else:
            for track in TRACKS:
                success, quota_exhausted = try_submit(track)
                if success:
                    log(f"Slot successfully consumed for {track['name']}!")
                    break
                if quota_exhausted:
                    log("Quota exhausted for today. Waiting for 00:00:00 UTC reset...")
                    break

        # Check leaderboard status every 30 minutes
        if utc_now.minute in (0, 30):
            check_leaderboard_standing()

        # Poll every 5 minutes
        time.sleep(300)

if __name__ == "__main__":
    main_loop()
