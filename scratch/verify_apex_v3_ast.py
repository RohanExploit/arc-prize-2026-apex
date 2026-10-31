import ast
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

nb_path = Path("e:/projects/arc-agi-3/notebooks/arc3-apex-sglang-v3/arc3-apex-sglang-v3.ipynb")
assert nb_path.exists(), f"Missing {nb_path}"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Inspecting Notebook: {nb_path.name}")
print(f"Total cells: {len(nb['cells'])}\n")

code_cells = [(i, c) for i, c in enumerate(nb["cells"]) if c.get("cell_type") == "code"]
print(f"Found {len(code_cells)} code cells.")

ast_errors = []
import_contracts = {}
defined_symbols = {}

for cell_idx, cell in code_cells:
    source = "".join(cell.get("source", []))
    lines = source.splitlines()
    clean_lines = []
    # Strip IPython magics like %%writefile or !pip for pure AST check
    for line in lines:
        if line.strip().startswith("%%") or line.strip().startswith("%") or line.strip().startswith("!"):
            clean_lines.append("# " + line)
        else:
            clean_lines.append(line)
    clean_source = "\n".join(clean_lines)
    
    try:
        tree = ast.parse(clean_source, filename=f"Cell_{cell_idx}")
        # Extract imports and defined functions/classes
        cell_imports = []
        cell_defs = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    cell_imports.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                cell_imports.append(f"{node.module}")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                cell_defs.append(f"def {node.name}")
            elif isinstance(node, ast.ClassDef):
                cell_defs.append(f"class {node.name}")
        import_contracts[cell_idx] = cell_imports
        defined_symbols[cell_idx] = cell_defs
        print(f"Cell {cell_idx:02d}: AST OK ({len(lines)} lines) | Imports: {len(cell_imports)} | Defs: {len(cell_defs)}")
    except SyntaxError as e:
        ast_errors.append((cell_idx, str(e)))
        print(f"Cell {cell_idx:02d}: AST SYNTAX ERROR: {e}")

print("\n" + "="*80)
print(f"AST SYNTAX AUDIT SUMMARY: {len(ast_errors)} ERRORS")
print("="*80)
for idx, err in ast_errors:
    print(f"  Cell {idx}: {err}")

# Now inspect execution paths and critical variables
print("\n" + "="*80)
print("CRITICAL RUNTIME EXECUTION PATH AUDIT")
print("="*80)
for idx, cell in code_cells:
    src = "".join(cell.get("source", []))
    if "TRUE_SUBMISSION" in src:
        print(f"Cell {idx} contains TRUE_SUBMISSION logic:")
        for line in src.splitlines():
            if any(k in line for k in ["TRUE_SUBMISSION", "COMPETITION", "submission.parquet", "arcade", "soft_end"]):
                print("   ", line.strip())

