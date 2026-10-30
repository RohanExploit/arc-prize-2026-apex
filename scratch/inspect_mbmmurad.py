import kaggle
import os
import json
from pathlib import Path

api = kaggle.KaggleApi()
api.authenticate()
out_dir = Path("scratch/mbmmurad")
out_dir.mkdir(parents=True, exist_ok=True)
try:
    api.kernels_pull("mbmmurad/arc-agi-3-lb-0-86-3rd-place-candidate-milestone", path=str(out_dir))
    print("Pulled mbmmurad kernel files:", os.listdir(out_dir))
except Exception as e:
    print("Error pulling mbmmurad:", e)
