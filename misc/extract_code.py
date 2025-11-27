import json

notebook_path = r'c:\Users\narsi\sbio\03_memristive_synapse.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        output_str += f"\n# --- Cell {i} ---\n"
        output_str += ''.join(cell['source']) + "\n"

with open(r'c:\Users\narsi\sbio\notebook_code.txt', 'w', encoding='utf-8') as f:
    f.write(output_str)
print("Code extracted to notebook_code.txt")
