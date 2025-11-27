import numpy as np
from utils import iterate_memristive_fhn
from config import MEMRISTOR_PARAMS, FHN_DISCRETE_PARAMS

print("Attempting to reproduce unpacking error...")

try:
    # Simulate memristive FHN as done in the notebook
    # This expects 3 return values but the function returns one array of shape (N, 3)
    x_traj, y_traj, z_traj = iterate_memristive_fhn(
        initial_state=[0.1, 0.1, 0.1],
        params={**MEMRISTOR_PARAMS, **FHN_DISCRETE_PARAMS},
        n_steps=100
    )
    print("Success! (Unexpected)")
except ValueError as e:
    print(f"Caught expected ValueError: {e}")
except Exception as e:
    print(f"Caught unexpected exception: {e}")
