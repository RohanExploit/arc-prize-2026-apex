with open(r'E:\projects\arc-agi-3\scripts\dispatch_00utc.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Make Track 1 version None so it dynamically submits the latest complete version
text = text.replace('"version": 1,\n        "file": "submission.parquet",\n        "message": "Autonomous Top-10 Push: SGLang v4', '"version": None,\n        "file": "submission.parquet",\n        "message": "Autonomous Top-10 Push: SGLang v4')

old_cmd = '''    cmd = [
        str(KAGGLE_BIN), "competitions", "submit", COMPETITION,
        "-k", track["kernel"],
        "-v", str(track["version"]),
        "-f", track["file"],
        "-m", track["message"],
    ]'''

new_cmd = '''    cmd = [
        str(KAGGLE_BIN), "competitions", "submit", COMPETITION,
        "-k", track["kernel"],
    ]
    if track.get("version") is not None:
        cmd.extend(["-v", str(track["version"])])
    cmd.extend(["-f", track["file"], "-m", track["message"]])'''

text = text.replace(old_cmd, new_cmd)

with open(r'E:\projects\arc-agi-3\scripts\dispatch_00utc.py', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated dispatch_00utc.py successfully!')
