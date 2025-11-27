
import json
import os

notebook_path = r'c:\Users\narsi\sbio\03_memristive_synapse.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with the simulation loop
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'iterate_memristive_fhn' in source and 'x0_fhn' in source:
            print("Found simulation cell.")
            
            # New code content
            new_source = [
                "# Simulate the memristive FHN system\n",
                "print(\"Simulating memristive FHN system...\")\n",
                "# Initial conditions from Shatnawi et al. (2023)\n",
                "x0_fhn = 0.01\n",
                "y0_fhn = 0.02\n",
                "z0_fhn = 0.1\n",
                "n_steps_fhn = 10000\n",
                "\n",
                "# Combine parameters\n",
                "sim_params = {**FHN_DISCRETE_PARAMS, **MEMRISTOR_PARAMS}\n",
                "\n",
                "trajectory = iterate_memristive_fhn(\n",
                "    [x0_fhn, y0_fhn, z0_fhn], \n",
                "    sim_params,\n",
                "    n_steps_fhn\n",
                ")\n",
                "\n",
                "# Unpack trajectory\n",
                "x_fhn, y_fhn, z_fhn = trajectory[:, 0], trajectory[:, 1], trajectory[:, 2]\n",
                "\n",
                "print(\"✓ Memristive FHN system simulated.\")"
            ]
            
            cell['source'] = new_source
            print("Updated simulation cell.")
            break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook saved.")
