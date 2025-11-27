
import numpy as np
from utils import iterate_memristive_fhn
from config import FHN_DISCRETE_PARAMS, MEMRISTOR_PARAMS

# Proposed parameters
params = {**FHN_DISCRETE_PARAMS, **MEMRISTOR_PARAMS}
params['I_ext'] = 1.5
params['k1'] = -0.06
params['k2'] = 0.2

print("Testing Proposed Parameters:")
print(params)

# Run simulation
print(f"\nSimulating...")
try:
    trajectory = iterate_memristive_fhn(
        [0.01, 0.02, 0.1], 
        params,
        10000
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
    
    if np.var(x) > 0.1:
        print("\nCONCLUSION: Good dynamics found!")
    else:
        print("\nCONCLUSION: Dynamics too small.")

except Exception as e:
    print(f"\nERROR: {e}")
