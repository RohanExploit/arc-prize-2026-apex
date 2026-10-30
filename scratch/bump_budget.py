from pathlib import Path

p = Path("agent/my_agent.py")
text = p.read_text(encoding="utf-8")
text = text.replace("MAX_ACTIONS = 100", "MAX_ACTIONS = 500")
p.write_text(text, encoding="utf-8")
print("Updated MAX_ACTIONS to 500 in agent/my_agent.py!")
