from pathlib import Path

p = Path("autopilot.py")
text = p.read_text(encoding="utf-8")

# Make check_kaggle_submissions and submit_latest_if_ready non-blocking / delegated
text = text.replace(
    "    # 1. Check Kaggle submission status\n    latest_sub = check_kaggle_submissions()\n    if latest_sub:\n        update_checkpoint(f\"Cycle #{cycle_num} Kaggle Status: {latest_sub[:90]}\")\n",
    "    # 1. Submission checking is handled asynchronously by dispatch_00utc daemon\n"
)

text = text.replace(
    "    # 3. Check quota & attempt submission if new quota available\n    submit_latest_if_ready()\n",
    "    # 3. Quota dispatch handled by dispatch_00utc daemon\n"
)

p.write_text(text, encoding="utf-8")
print("Successfully streamlined autopilot.py into 100% offline non-blocking execution!")
