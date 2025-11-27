import numpy as np
from utils import iterate_memristive_fhn
from config import MEMRISTOR_PARAMS, FHN_DISCRETE_PARAMS

print("Diagnosing simulation values...")

try:
    # Run simulation as in the notebook
    initial_state = [0.1, 0.1, 0.1]
    params = {**MEMRISTOR_PARAMS, **FHN_DISCRETE_PARAMS}
    
    print(f"Parameters: {params}")
    
    trajectory = iterate_memristive_fhn(
        initial_state=initial_state,
        params=params,
        n_steps=1000,
        transient=0
    )
    
    x_traj, y_traj, z_traj = trajectory.T
    
    print(f"Trajectory shape: {trajectory.shape}")
    print(f"X range: [{np.min(x_traj)}, {np.max(x_traj)}]")
    print(f"Y range: [{np.min(y_traj)}, {np.max(y_traj)}]")
    print(f"Z range: [{np.min(z_traj)}, {np.max(z_traj)}]")
    
    if np.any(np.isnan(trajectory)):
        print("!!! DETECTED NaNs IN TRAJECTORY !!!")
    if np.any(np.isinf(trajectory)):
        print("!!! DETECTED Infs IN TRAJECTORY !!!")
        
    # Print first few steps to see divergence
    print("\nFirst 10 steps:")
    for i in range(10):
        print(f"Step {i}: {trajectory[i]}")

except Exception as e:
    print(f"Simulation failed: {e}")
