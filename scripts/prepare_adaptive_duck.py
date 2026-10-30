"""Prepares the state-of-the-art Adaptive Duck SGLang kernel for Kaggle push.
Combines:
  1. Daniel Franzen / Tufa Labs SGLang Speculative Drafting engine
  2. Intel AutoRound INT4 Qwen 3.8 Flash Next + Albucino MTP drafter
  3. Laimer Botrolenk Adaptive Duck tools:
     - bounded A* / symbolic search (bounded_search)
     - direct character grid computation (board())
     - cross-step memory persistence (adaptive_notes)
  4. Resilient dataset and model mount resolver for Kaggle runtime
  5. Smoke practice mode for fast 3-minute zero-quota commit
"""
import json
import os
import shutil
from pathlib import Path

ROOT = Path("e:/projects/arc-agi-3")
SRC_NOTEBOOK = ROOT / "scratch/bench_laimerbotrolenk_lb-score-31-21/lb-score-31-21.ipynb"
DEST_DIR = ROOT / "notebooks/arc3-adaptive-duck-sglang"
DEST_DIR.mkdir(parents=True, exist_ok=True)
DEST_NOTEBOOK = DEST_DIR / "arc3-adaptive-duck-sglang.ipynb"
METADATA_FILE = DEST_DIR / "kernel-metadata.json"

with open(SRC_NOTEBOOK, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Inspect cells and adjust:
# 1. In Cell 2 (Run controls), ensure PRACTICE_MODE = 'smoke' for fast commit
for i, cell in enumerate(nb["cells"]):
    src = "".join(cell.get("source", []))
    if "PRACTICE_MODE =" in src and "PROFILE =" in src:
        # Update run controls
        new_src = src.replace("PRACTICE_MODE = 'full'", "PRACTICE_MODE = 'smoke'")
        cell["source"] = [new_src]
        print(f"Updated Cell {i} run controls to smoke mode.")

    # 2. In Cell 8 (Paths and configuration), make dataset and model path resolution resilient
    if "WHEELHOUSE_DIR" in src and "MODEL_DIR" in src and "ORIG_BUNDLE_DIR" in src:
        # Ensure path resolution probes both flat and nested /kaggle/input paths
        path_probe_logic = '''
def _resolve_dir(candidates):
    for c in candidates:
        p = Path(c)
        if p.is_dir():
            return str(p)
    return str(candidates[0])

WHEELHOUSE_DIR = _resolve_dir([
    '/kaggle/input/datasets/dfranzen/pennyroyal-v253',
    '/kaggle/input/pennyroyal-v253',
    '/kaggle/input/datasets/mirzamilanfarabi/pennyroyal-v253'
])
MODEL_DIR = _resolve_dir([
    '/kaggle/input/models/dfranzen/intel-qwen3.8-flash-next-w4a16-autoround/transformers/default/1',
    '/kaggle/input/intel-qwen3.8-flash-next-w4a16-autoround/transformers/default/1',
    '/kaggle/input/models/dfranzen/intel-qwen3.8-flash-next-w4a16-autoround/Transformers/default/1',
    '/kaggle/input/intel-qwen3.8-flash-next-w4a16-autoround/Transformers/default/1'
])
DRAFT_MODEL_DIR = _resolve_dir([
    '/kaggle/input/models/dfranzen/albucino-qwen3-8-flash-next-drafter/transformers/default/1',
    '/kaggle/input/albucino-qwen3-8-flash-next-drafter/transformers/default/1',
    '/kaggle/input/models/dfranzen/albucino-qwen3-8-flash-next-drafter/Transformers/default/1',
    '/kaggle/input/albucino-qwen3-8-flash-next-drafter/Transformers/default/1'
])
ORIG_BUNDLE_DIR = _resolve_dir([
    '/kaggle/input/datasets/dfranzen/taaf-kaggle-source-bundle-copy',
    '/kaggle/input/taaf-kaggle-source-bundle-copy'
])
'''
        # Replace the hardcoded paths with resilient resolver
        target_block = """WHEELHOUSE_DIR    = '/kaggle/input/datasets/dfranzen/pennyroyal-v253'
MODEL_DIR         = '/kaggle/input/models/dfranzen/intel-qwen3.8-flash-next-w4a16-autoround/transformers/default/1'
DRAFT_MODEL_DIR   = '/kaggle/input/models/dfranzen/albucino-qwen3-8-flash-next-drafter/transformers/default/1'
ORIG_BUNDLE_DIR   = '/kaggle/input/datasets/dfranzen/taaf-kaggle-source-bundle-copy'"""
        if target_block in src:
            new_src = src.replace(target_block, path_probe_logic.strip())
            cell["source"] = [new_src]
            print(f"Injected resilient path resolver into Cell {i}.")

# Save modified notebook
with open(DEST_NOTEBOOK, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)

print(f"Saved optimized notebook to: {DEST_NOTEBOOK}")

# Create metadata
metadata = {
    "id": "rohanexploit/arc3-adaptive-duck-sglang",
    "title": "ARC3 Adaptive Duck SGLang",
    "code_file": "arc3-adaptive-duck-sglang.ipynb",
    "language": "python",
    "kernel_type": "notebook",
    "is_private": True,
    "enable_gpu": True,
    "enable_tpu": False,
    "enable_internet": False,
    "keywords": ["gpu"],
    "dataset_sources": [
        "dfranzen/pennyroyal-v253",
        "dfranzen/taaf-kaggle-source-bundle-copy"
    ],
    "kernel_sources": [],
    "competition_sources": [
        "arc-prize-2026-arc-agi-3"
    ],
    "model_sources": [
        "dfranzen/albucino-qwen3-8-flash-next-drafter/Transformers/default/1",
        "dfranzen/intel-qwen3.8-flash-next-w4a16-autoround/Transformers/default/1"
    ],
    "docker_image": "gcr.io/kaggle-private-byod/python@sha256:57e612b484cf3df5026ee4dcc3cb176974b22b2bc0937fb1e16132a8be4cb13c",
    "machine_shape": "NvidiaRtxPro6000"
}

with open(METADATA_FILE, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print(f"Saved kernel metadata to: {METADATA_FILE}")
