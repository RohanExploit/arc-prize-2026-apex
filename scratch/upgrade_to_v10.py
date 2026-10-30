from pathlib import Path

dispatch_file = Path("scripts/dispatch_00utc.py")
d_text = dispatch_file.read_text(encoding="utf-8")
d_text = d_text.replace('"version": 9,', '"version": 10,')
d_text = d_text.replace(
    'Cavity-Aware Multi-Specialist BFS Explorer v9',
    'Deep-Horizon Multi-Specialist BFS Explorer v10 (500 steps)'
)
dispatch_file.write_text(d_text, encoding="utf-8")

auto_file = Path("autopilot.py")
a_text = auto_file.read_text(encoding="utf-8")
a_text = a_text.replace('-v 9 -f', '-v 10 -f')
a_text = a_text.replace(
    'Autonomous Cavity-Aware Multi-Specialist BFS Explorer v9',
    'Autonomous Deep-Horizon Multi-Specialist BFS Explorer v10'
)
auto_file.write_text(a_text, encoding="utf-8")
print("Dispatcher and Autopilot upgraded to Version 10!")
