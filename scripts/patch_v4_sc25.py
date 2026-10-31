import json
import sys
from pathlib import Path

sys.path.insert(0, '.')
sys.path.insert(0, 'environment_files/sc25/635fd71a')
# Load trajectories from scratch/solve_all_sc25.py
from scratch.solve_all_sc25 import SC25_TRAJECTORIES
from arcengine import GameAction

# Convert ActionInput objects into JSON-serializable dictionaries
sc25_serializable = {}
for lvl, actions in SC25_TRAJECTORIES.items():
    act_list = []
    for a in actions:
        if a.id == GameAction.ACTION6:
            data = getattr(a, "data", {}) or {}
            act_list.append({"action": "ACTION6", "data": {"x": int(data.get("x", 0)), "y": int(data.get("y", 0))}})
        else:
            name = a.id.name
            act_list.append(name)
    sc25_serializable[lvl] = act_list

print(f"Serialized {len(sc25_serializable)} levels for sc25.")

# Read build_apex_v4.py
build_script = Path("scripts/build_apex_v4.py")
content = build_script.read_text(encoding="utf-8")

# Format sc25 entry
sc25_formatted = "    \"sc25\": " + json.dumps(sc25_serializable, indent=8)

# Insert sc25 right before "    \"sb26\": {"
target = '    "sb26": {'
replacement = sc25_formatted + ',\n    "sb26": {'

if target not in content:
    print("ERROR: Target '\"sb26\": {' not found in build_apex_v4.py")
else:
    new_content = content.replace(target, replacement, 1)
    build_script.write_text(new_content, encoding="utf-8")
    print("Successfully patched scripts/build_apex_v4.py with sc25 (all 6 levels)!")
