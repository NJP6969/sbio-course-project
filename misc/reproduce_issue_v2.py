
import numpy as np
from utils import iterate_memristive_fhn
from config import FHN_DISCRETE_PARAMS, MEMRISTOR_PARAMS

# Current parameters from config.py
print("Current FHN Parameters:", FHN_DISCRETE_PARAMS)
print("Current Memristor Parameters:", MEMRISTOR_PARAMS)

# Simulation settings from notebook
x0 = 0.01
y0 = -0.1
z0 = 0.01
n_steps = 10000

# Run simulation
print(f"\nSimulating with x0={x0}, y0={y0}, z0={z0}, n_steps={n_steps}...")
trajectory = iterate_memristive_fhn(
    [x0, y0, z0],
    {**FHN_DISCRETE_PARAMS, **MEMRISTOR_PARAMS},
    n_steps
)
x, y, z = trajectory[:, 0], trajectory[:, 1], trajectory[:, 2]

# Analyze results
print("\nResults Analysis:")
print(f"x range: [{np.min(x):.6f}, {np.max(x):.6f}]")
print(f"y range: [{np.min(y):.6f}, {np.max(y):.6f}]")
print(f"z range: [{np.min(z):.6f}, {np.max(z):.6f}]")

print(f"x mean: {np.mean(x):.6f}")
print(f"y mean: {np.mean(y):.6f}")
print(f"z mean: {np.mean(z):.6f}")

print(f"x variance: {np.var(x):.6f}")

if np.var(x) < 1e-6:
    print("\nCONCLUSION: The system is effectively stationary (flat lines).")
else:
    print("\nCONCLUSION: The system exhibits some dynamics.")
