import json
from pathlib import Path

scratch = Path('e:/projects/arc-agi-3/scratch')
benchmarks = [d for d in scratch.glob('bench_*') if d.is_dir()]

for b in sorted(benchmarks):
    print(f"\n==================== {b.name} ====================")
    meta_path = b / 'kernel-metadata.json'
    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        print("ID:", meta.get('id'))
        print("Title:", meta.get('title'))
        print("Kernel type:", meta.get('kernel_type'))
        print("Accelerator:", meta.get('accelerator'))
        print("Dataset sources:", meta.get('dataset_sources'))
        print("Kernel sources:", meta.get('kernel_sources'))
    
    # Check notebook or script
    for nb_path in b.glob('*.ipynb'):
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        cells = nb.get('cells', [])
        print(f"Notebook: {nb_path.name} ({len(cells)} cells)")
        # Look for model names, prompts, or key parameters
        full_text = ""
        for cell in cells:
            full_text += "".join(cell.get('source', [])) + "\n"
        
        # Check mentions of models or algorithms
        for keyword in ['vllm', 'qwen', 'gemma', 'llama', 'dataset', 'solver', 'bfs', 'dprime', 'franzen', 'duck', 'score', 'temperature']:
            count = full_text.lower().count(keyword)
            if count > 0:
                print(f"  keyword '{keyword}': {count} occurrences")
