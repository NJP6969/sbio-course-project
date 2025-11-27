
import numpy as np
from utils import iterate_memristive_fhn
from config import FHN_DISCRETE_PARAMS, MEMRISTOR_PARAMS

# Paper parameters
PAPER_FHN_PARAMS = FHN_DISCRETE_PARAMS.copy()
PAPER_FHN_PARAMS['I_ext'] = 2.0

PAPER_MEMRISTOR_PARAMS = MEMRISTOR_PARAMS.copy()
PAPER_MEMRISTOR_PARAMS['k1'] = -0.06
PAPER_MEMRISTOR_PARAMS['k2'] = 0.2

# Paper initial conditions
x0 = 0.01
y0 = 0.02
z0 = 0.1
n_steps = 10000

print("Testing Paper Parameters:")
print("FHN:", PAPER_FHN_PARAMS)
print("Memristor:", PAPER_MEMRISTOR_PARAMS)
print(f"Initial Conditions: x0={x0}, y0={y0}, z0={z0}")

# Run simulation
print(f"\nSimulating...")
trajectory = iterate_memristive_fhn(
    [x0, y0, z0],
    {**PAPER_FHN_PARAMS, **PAPER_MEMRISTOR_PARAMS},
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

if np.var(x) > 0.01:
    print("\nCONCLUSION: The system exhibits significant dynamics (likely chaotic/oscillatory).")
else:
    print("\nCONCLUSION: The system dynamics are still small/flat.")
