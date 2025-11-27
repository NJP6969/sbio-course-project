import json

notebook_path = r'c:\Users\narsi\sbio\03_memristive_synapse.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source = cell['source']
            source_text = ''.join(source)
            if "iterate_memristive_fhn" in source_text:
                print(f"--- Cell {i} Source ---")
                print(repr(source))
                print("--- End Cell ---")

except Exception as e:
    print(f"Error: {e}")
