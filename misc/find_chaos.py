
import numpy as np
from utils import iterate_memristive_fhn
from config import FHN_DISCRETE_PARAMS, MEMRISTOR_PARAMS

def check_chaos(i_ext, k1, k2):
    params = {**FHN_DISCRETE_PARAMS, **MEMRISTOR_PARAMS}
    params['I_ext'] = i_ext
    params['k1'] = k1
    params['k2'] = k2
    
    try:
        # Run simulation
        trajectory = iterate_memristive_fhn(
            [0.01, 0.02, 0.1], 
            params,
            5000,
            transient=2000
        )
        
        if trajectory.shape[0] < 100:
            return False, 0, "Simulation failed"
            
        x = trajectory[:, 0]
        
        # Check for NaNs/Infs
        if np.any(np.isnan(x)) or np.any(np.isinf(x)):
            return False, 0, "Unstable (NaN/Inf)"
            
        # Check variance (must be significant)
        var_x = np.var(x)
        if var_x < 0.01:
            return False, var_x, "Low variance (Fixed point)"
            
        # Check for periodicity by counting unique points (rounded)
        # Chaos should have many unique points
        unique_points = len(np.unique(np.round(x, 4)))
        
        if unique_points < 20:
             return False, var_x, f"Periodic (Period ~{unique_points})"
             
        return True, var_x, f"Chaotic? (Unique points: {unique_points})"
        
    except Exception as e:
        return False, 0, f"Error: {e}"

print("Searching for chaotic parameters...")
print(f"{'I_ext':<10} {'k1':<10} {'k2':<10} {'Status':<30} {'Variance':<10}")
print("-" * 70)

# Coarse sweep
i_ext_vals = np.arange(0.1, 2.0, 0.1)
k1_vals = np.arange(-0.2, 0.0, 0.02)
k2_vals = np.arange(0.1, 0.5, 0.1)

found_params = []

for i_ext in i_ext_vals:
    for k1 in k1_vals:
        for k2 in k2_vals:
            is_chaos, var, msg = check_chaos(i_ext, k1, k2)
            if is_chaos:
                print(f"{i_ext:<10.2f} {k1:<10.2f} {k2:<10.2f} {msg:<30} {var:<10.4f}")
                found_params.append((i_ext, k1, k2, var))

if found_params:
    # Sort by variance (higher variance often means larger attractor)
    found_params.sort(key=lambda x: x[3], reverse=True)
    best = found_params[0]
    result_msg = "\nBest Candidate:\n"
    result_msg += f"I_ext={best[0]:.2f}, k1={best[1]:.2f}, k2={best[2]:.2f}, Var={best[3]:.4f}\n"
    print(result_msg)
    with open('chaos_results.txt', 'w') as f:
        f.write(result_msg)
        for p in found_params:
             f.write(f"I_ext={p[0]:.2f}, k1={p[1]:.2f}, k2={p[2]:.2f}, Var={p[3]:.4f}\n")

else:
    print("\nNo chaotic parameters found.")
