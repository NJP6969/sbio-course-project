
import numpy as np
from utils import iterate_memristive_fhn
from config import FHN_DISCRETE_PARAMS, MEMRISTOR_PARAMS

def test_params(i_ext, k1, k2):
    params = FHN_DISCRETE_PARAMS.copy()
    params['I_ext'] = i_ext
    params['k1'] = k1
    params['k2'] = k2
    
    # Also need to update MEMRISTOR_PARAMS for k1, k2 if they are used there, 
    # but iterate_memristive_fhn takes a single params dict.
    # We need to make sure we pass the merged dict.
    
    merged_params = {**FHN_DISCRETE_PARAMS, **MEMRISTOR_PARAMS}
    merged_params['I_ext'] = i_ext
    merged_params['k1'] = k1
    merged_params['k2'] = k2
    
    try:
        trajectory = iterate_memristive_fhn(
            [0.01, 0.02, 0.1], # Paper IC
            merged_params,
            1000 # Shorter run for sweep
        )
        x = trajectory[:, 0]
        if np.any(np.isnan(x)) or np.any(np.isinf(x)):
            return False, 0, 0
        
        var_x = np.var(x)
        range_x = np.max(x) - np.min(x)
        return True, var_x, range_x
    except Exception:
        return False, 0, 0

print("Sweeping I_ext...")
for i_ext in [0.1, 0.2, 0.5, 1.0, 1.5, 2.0]:
    stable, var, rng = test_params(i_ext, -0.06, 0.2)
    print(f"I_ext={i_ext}: Stable={stable}, Var={var:.6f}, Range={rng:.6f}")

print("\nSweeping k1 with I_ext=0.5...")
for k1 in [-0.1, -0.06, -0.01, 0.01, 0.05]:
    stable, var, rng = test_params(0.5, k1, 0.2)
    print(f"k1={k1}: Stable={stable}, Var={var:.6f}, Range={rng:.6f}")

print("\nSweeping k2 with I_ext=0.5...")
for k2 in [0.1, 0.2, 0.5]:
    stable, var, rng = test_params(0.5, -0.06, k2)
    print(f"k2={k2}: Stable={stable}, Var={var:.6f}, Range={rng:.6f}")
