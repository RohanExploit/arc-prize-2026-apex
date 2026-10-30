import re
from pathlib import Path

p = Path("autopilot.py")
text = p.read_text(encoding="utf-8")

# Replace 20-minute sleep with continuous 15-second pause
text = text.replace("Sleeping 20 minutes before next cycle...", "Continuous execution: running next cycle in 15s...")
text = text.replace("time.sleep(20 * 60)", "time.sleep(15)")

# Expand test games to all 25 environments
old_games = 'test_games = ["ls20", "vc33", "wa30", "re86", "tu93", "su15"]'
new_games = '''all_25_games = [
        "ar25", "bp35", "cd82", "cn04", "dc22", "ft09", "g50t", "ka59",
        "lf52", "lp85", "ls20", "m0r0", "r11l", "re86", "s5i5", "sb26",
        "sc25", "sk48", "sp80", "su15", "tn36", "tr87", "tu93", "vc33", "wa30"
    ]
    # Rotate 8 games per cycle with deep 120-step exploration budget
    start_idx = ((cycle_num - 1) * 8) % len(all_25_games)
    test_games = [all_25_games[(start_idx + i) % len(all_25_games)] for i in range(8)]'''

text = text.replace(old_games, new_games)
text = text.replace("max_steps=50", "max_steps=120")

p.write_text(text, encoding="utf-8")
print("Autopilot upgraded to continuous non-stop execution (15s cycle, rotating 25 games, 120 steps)!")
