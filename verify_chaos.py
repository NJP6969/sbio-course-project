
import numpy as np
import matplotlib.pyplot as plt
from utils import iterate_memristive_fhn
from config import FHN_DISCRETE_PARAMS, MEMRISTOR_PARAMS

def verify(i_ext, k1, k2):
    params = {**FHN_DISCRETE_PARAMS, **MEMRISTOR_PARAMS}
    params['I_ext'] = i_ext
    params['k1'] = k1
    params['k2'] = k2
    
    print(f"Testing I_ext={i_ext}, k1={k1}, k2={k2}")
    
    trajectory = iterate_memristive_fhn(
        [0.01, 0.02, 0.1], 
        params,
        5000,
        transient=1000
    )
    
    x = trajectory[:, 0]
    y = trajectory[:, 1]
    z = trajectory[:, 2]
    
    print(f"Variance x: {np.var(x):.4f}")
    print(f"Unique points (rounded): {len(np.unique(np.round(x, 4)))}")
    print(f"Range x: [{np.min(x):.4f}, {np.max(x):.4f}]")
    
    return x, y, z

if __name__ == "__main__":
    # Best candidate from previous search
    verify(1.90, -0.02, 0.30)
