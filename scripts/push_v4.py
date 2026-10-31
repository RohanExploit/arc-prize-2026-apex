import time
import sys
from pathlib import Path
from kaggle.api.kaggle_api_extended import KaggleApi

def push_kernel(folder_path):
    p = Path(folder_path).resolve()
    print(f"Pushing kernel from {p}...")
    api = KaggleApi()
    api.authenticate()
    
    for attempt in range(1, 5):
        try:
            print(f"Attempt {attempt}: calling kernels_push({p})...")
            res = api.kernels_push(str(p))
            print(f"Successfully pushed kernel! Result: {res}")
            return True
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < 4:
                time.sleep(attempt * 4)
            else:
                raise

if __name__ == "__main__":
    push_kernel("notebooks/arc3-apex-sglang-v4")
