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
        # Update simulation code with explicit chaotic parameters
        nb.cells[sim_cell_idx].source = """# System parameters (Chaotic Regime)
# I_ext=1.80, k1=-0.06, k2=0.30
params = {
    'gamma': 0.5,
    'theta': 0.1,
    'delta': 0.1,
    'I_ext': 1.80,
    'k1': -0.06,
    'k2': 0.30
}

# Initial condition
initial_state = [0.01, 0.02, 0.1]  # [x, y, z]

# Iterate the map
n_steps = 10000
transient = 2000

print(f"Simulating memristive FHN system with I_ext={params['I_ext']}...")
trajectory = iterate_memristive_fhn(initial_state, params, n_steps, transient=transient)

x_traj = trajectory[:, 0]
y_traj = trajectory[:, 1]
z_traj = trajectory[:, 2]

print(f"✓ Simulation complete: {len(trajectory)} points after transient")
print(f"  x range: [{x_traj.min():.3f}, {x_traj.max():.3f}]")
print(f"  y range: [{y_traj.min():.3f}, {y_traj.max():.3f}]")
print(f"  z range: [{z_traj.min():.3f}, {z_traj.max():.3f}]")

# Plot time series
n_points = min(500, len(x_traj)) # Zoom in to see chaos
time_indices = np.arange(n_points)

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# Membrane potential
axes[0].plot(time_indices, x_traj[:n_points], color='#2C3E50', linewidth=1)
axes[0].set_ylabel('x (membrane potential)', fontsize=11)
axes[0].set_title('Memristive FHN Neuron Dynamics (Chaotic)', fontsize=13, fontweight='bold')
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

    # Find the 2D Projections cell (Section 7)
    proj_cell_idx = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown' and 'Section 7' in cell.source:
            proj_cell_idx = i + 1
            break
            
    if proj_cell_idx != -1 and proj_cell_idx < len(nb.cells):
        print(f"Updating projection cell at index {proj_cell_idx}")
        nb.cells[proj_cell_idx].source = """# Plot 2D projections
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Use a subset of points for scatter plot to avoid overcrowding
plot_step = 1
x_plot = x_traj[::plot_step]
y_plot = y_traj[::plot_step]
z_plot = z_traj[::plot_step]

# x-y plane
axes[0].scatter(x_plot, y_plot, s=1, alpha=0.6, c='#2C3E50')
axes[0].set_xlabel('x (membrane potential)')
axes[0].set_ylabel('y (recovery variable)')
axes[0].set_title('Phase Plane (x-y)')
axes[0].grid(True, alpha=0.3)

# x-z plane
axes[1].scatter(x_plot, z_plot, s=1, alpha=0.6, c='#8E44AD')
axes[1].set_xlabel('x (membrane potential)')
axes[1].set_ylabel('z (memristor state)')
axes[1].set_title('Memristive Coupling (x-z)')
axes[1].grid(True, alpha=0.3)

# y-z plane
axes[2].scatter(y_plot, z_plot, s=1, alpha=0.6, c='#E74C3C')
axes[2].set_xlabel('y (recovery variable)')
axes[2].set_ylabel('z (memristor state)')
axes[2].set_title('Internal State (y-z)')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
print("✓ 2D projections generated")"""

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Notebook updated successfully.")

if __name__ == "__main__":
    try:
        fix_notebook()
    except Exception as e:
        print(f"Error: {e}")
