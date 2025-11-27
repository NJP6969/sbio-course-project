import json
import nbformat

notebook_path = r'c:\Users\narsi\sbio\03_memristive_synapse.ipynb'

def fix_notebook():
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find the simulation cell (Section 6)
    sim_cell_idx = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown' and 'Section 6' in cell.source:
            sim_cell_idx = i + 1
            break
    
    if sim_cell_idx != -1 and sim_cell_idx < len(nb.cells):
        print(f"Updating simulation cell at index {sim_cell_idx}")
        # Update simulation code with stable parameters
        nb.cells[sim_cell_idx].source = """# System parameters (Shatnawi et al. 2023)
# gamma=-0.2, theta=0.108, delta=0.08
# I_ext=1.80 (Adjusted from 2.0 for stability)
# k1=-0.06, k2=0.2
params = {
    'gamma': -0.2,
    'theta': 0.108,
    'delta': 0.08,
    'I_ext': 1.80,
    'k1': -0.06,
    'k2': 0.2
}

# Initial condition (Figure 5b caption)
initial_state = [0.01, 0.02, 0.1]  # [x, y, z]

# Iterate the map
n_steps = 10000
transient = 2000

print(f"Simulating memristive FHN system with Stable Parameters (I_ext=1.80)...")
trajectory = iterate_memristive_fhn(initial_state, params, n_steps, transient=transient)

x_traj = trajectory[:, 0]
y_traj = trajectory[:, 1]
z_traj = trajectory[:, 2]

print(f"✓ Simulation complete: {len(trajectory)} points after transient")
print(f"  x range: [{x_traj.min():.3f}, {x_traj.max():.3f}]")
print(f"  y range: [{y_traj.min():.3f}, {y_traj.max():.3f}]")
print(f"  z range: [{z_traj.min():.3f}, {z_traj.max():.3f}]")

# Plot time series
n_points = min(500, len(x_traj))
time_indices = np.arange(n_points)

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# Membrane potential
axes[0].plot(time_indices, x_traj[:n_points], color='#2C3E50', linewidth=1)
axes[0].set_ylabel('x (membrane potential)', fontsize=11)
axes[0].set_title('Memristive FHN Neuron Dynamics (Stable Parameters)', fontsize=13, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Recovery variable
axes[1].plot(time_indices, y_traj[:n_points], color='#E74C3C', linewidth=1)
axes[1].set_ylabel('y (recovery variable)', fontsize=11)
axes[1].grid(True, alpha=0.3)

# Memristor state
axes[2].plot(time_indices, z_traj[:n_points], color='#8E44AD', linewidth=1)
axes[2].set_ylabel('z (memristor state)', fontsize=11)
axes[2].set_xlabel('Iteration', fontsize=11)
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()"""

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Notebook updated successfully.")

if __name__ == "__main__":
    try:
        fix_notebook()
    except Exception as e:
        print(f"Error: {e}")
