import json

notebook_path = r'c:\Users\narsi\sbio\03_memristive_synapse.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    modified = False
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            new_source = []
            cell_modified = False
            
            for line in source:
                # Fix Cell 12: Unpacking error
                # Use substring match to be safer
                if "iterate_memristive_fhn(initial_state, params, n_steps=5000, transient=1000)" in line and "x_traj, y_traj, z_traj =" in line:
                    new_source.append("trajectory = iterate_memristive_fhn(initial_state, params, n_steps=5000, transient=1000)\n")
                    new_source.append("x_traj, y_traj, z_traj = trajectory.T")
                    cell_modified = True
                    modified = True
                    print("Fixed Cell 12 unpacking error.")
                else:
                    new_source.append(line)
            
            if cell_modified:
                cell['source'] = new_source

    if modified:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f"Successfully modified {notebook_path}")
    else:
        print("No changes were made.")

except Exception as e:
    print(f"Error modifying notebook: {e}")
