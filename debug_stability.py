import numpy as np
from utils import iterate_memristive_fhn

# Base parameters from paper
params = {
    'gamma': -0.2,
    'theta': 0.108,
    'delta': 0.08,
    'I_ext': 2.0, 
    'k1': -0.06,
    'k2': 0.2
}

initial_state = [0.01, 0.02, 0.1]
n_steps = 1000

print("Sweeping I_ext to find stability threshold...")
print(f"Base params: {params}")

for I_val in np.linspace(0.1, 2.5, 25):
    test_params = params.copy()
    test_params['I_ext'] = I_val
    
    try:
        traj = iterate_memristive_fhn(initial_state, test_params, n_steps)
        x = traj[:, 0]
        
        if np.isnan(x).any() or np.isinf(x).any() or np.max(np.abs(x)) > 1e4:
            status = "UNSTABLE (Overflow)"
        else:
            var = np.var(x)
            if var < 1e-5:
                status = "STABLE (Fixed Point)"
            else:
                status = f"CHAOTIC/PERIODIC (Var={var:.4f})"
                
        with open(r'c:\Users\narsi\sbio\stability_results.txt', 'a') as f:
            f.write(f"I_ext={I_val:.2f}: {status}\n")
        print(f"I_ext={I_val:.2f}: {status}")
        
    except Exception as e:
        with open(r'c:\Users\narsi\sbio\stability_results.txt', 'a') as f:
            f.write(f"I_ext={I_val:.2f}: Error {e}\n")
        print(f"I_ext={I_val:.2f}: Error {e}")
