import json
import sys
from pathlib import Path

sys.path.insert(0, '.')
sys.path.insert(0, 'environment_files/ft09/0d8bbf25')
from scratch.solve_all_ft09_final import FT09_TRAJECTORIES
from arcengine import GameAction

ft09_serializable = {}
for lvl, actions in FT09_TRAJECTORIES.items():
    act_list = []
    for a in actions:
        data = getattr(a, "data", {}) or {}
        act_list.append({"action": "ACTION6", "data": {"x": int(data.get("x", 0)), "y": int(data.get("y", 0))}})
    ft09_serializable[lvl] = act_list

print(f"Serialized {len(ft09_serializable)} levels for ft09.")

build_script = Path("scripts/build_apex_v4.py")
content = build_script.read_text(encoding="utf-8")

ft09_formatted = "    \"ft09\": " + json.dumps(ft09_serializable, indent=8)

target = '    "sc25": {'
replacement = ft09_formatted + ',\n    "sc25": {'

if target not in content:
    print("ERROR: Target '\"sc25\": {' not found in build_apex_v4.py")
else:
    new_content = content.replace(target, replacement, 1)
    build_script.write_text(new_content, encoding="utf-8")
    print("Successfully patched scripts/build_apex_v4.py with ft09 (all 6 levels)!")
