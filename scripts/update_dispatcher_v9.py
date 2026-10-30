from pathlib import Path

# Update dispatch_00utc.py
dispatch_file = Path("scripts/dispatch_00utc.py")
d_text = dispatch_file.read_text(encoding="utf-8")
d_text = d_text.replace(
    '"name": "Track 1: Multi-Band HUD & Hybrid BFS Explorer v8",\n        "kernel": "rohanexploit/arc-prize-2026-bfs-explorer-agent",\n        "version": 8,\n        "file": "submission.parquet",\n        "message": "Autonomous Multi-Band HUD & Hybrid BFS Explorer v8",',
    '"name": "Track 1: Cavity-Aware Multi-Specialist BFS Explorer v9",\n        "kernel": "rohanexploit/arc-prize-2026-bfs-explorer-agent",\n        "version": 9,\n        "file": "submission.parquet",\n        "message": "Autonomous Cavity-Aware Receptacle BFS Explorer v9",'
)
dispatch_file.write_text(d_text, encoding="utf-8")

# Update autopilot.py
auto_file = Path("autopilot.py")
a_text = auto_file.read_text(encoding="utf-8")
a_text = a_text.replace(
    '-k {KERNEL_ID} -v 8 -f submission.parquet -m "Autonomous Multi-Band HUD & Hybrid BFS Explorer v8"',
    '-k {KERNEL_ID} -v 9 -f submission.parquet -m "Autonomous Cavity-Aware Multi-Specialist BFS Explorer v9"'
)
auto_file.write_text(a_text, encoding="utf-8")
print("Target version successfully upgraded from v8 to v9 across dispatchers!")
