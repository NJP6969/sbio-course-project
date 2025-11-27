import json

notebook_path = r'c:\Users\narsi\sbio\03_memristive_synapse.ipynb'

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    modified = False
    
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source_text = ''.join(cell['source'])
            # Aggressive check for Cell 12
            if "iterate_memristive_fhn" in source_text and "x_traj" in source_text and "y_traj" in source_text and "z_traj" in source_text and "trajectory =" not in source_text:
                print(f"Found target Cell {i}. Replacing source.")
                cell['source'] = [
                    "# Run simulation\n",
                    "trajectory = iterate_memristive_fhn(initial_state, params, n_steps=5000, transient=1000)\n",
                    "x_traj, y_traj, z_traj = trajectory.T"
                ]
                modified = True
            
            # Check if Cell 14 is already fixed (just to be sure)
            if "n_points = min(2000, len(trajectory))" in source_text:
                 print(f"Found target Cell {i} (Cell 14). Replacing source.")
                 new_source = []
                 for line in cell['source']:
                     if "n_points = min(2000, len(trajectory))" in line:
                         new_source.append("n_points = min(2000, len(x_traj))\n")
                     else:
                         new_source.append(line)
                 cell['source'] = new_source
                 modified = True

    if modified:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f"Successfully modified {notebook_path}")
    else:
        print("No changes were made. Target cells not found or already fixed.")

except Exception as e:
    print(f"Error modifying notebook: {e}")
