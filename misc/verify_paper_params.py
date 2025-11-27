import numpy as np
import matplotlib.pyplot as plt
from utils import iterate_memristive_fhn

# Exact parameters from Shatnawi et al. (2023) Section 3.2
# "Herein, we took the parameters of the system as gamma = -0.2, delta = 0.08, theta = 0.108, k1 = -0.06, and k2 = 0.2."
# "positive external input current is fixed to I = 2"

PAPER_PARAMS = {
    'gamma': -0.2,
    'theta': 0.108,
    'delta': 0.08,
    'I_ext': 2.0,   # Fixed to 2.0 as per text
    'k1': -0.06,
    'k2': 0.2
}

# Initial conditions from Figure 5b caption
# "(x0, y0, z0) = (0.01, 0.02, 0.1)"
initial_state = [0.01, 0.02, 0.1]

print("Simulating with Paper Parameters:")
print(PAPER_PARAMS)
print(f"Initial State: {initial_state}")

# Simulate
n_steps = 10000
transient = 1000
trajectory = iterate_memristive_fhn(initial_state, PAPER_PARAMS, n_steps, transient=transient)

x = trajectory[:, 0]
y = trajectory[:, 1]
z = trajectory[:, 2]

print(f"\nSimulation Results:")
print(f"Number of points: {len(trajectory)}")
print(f"x range: [{x.min():.4f}, {x.max():.4f}]")
print(f"y range: [{y.min():.4f}, {y.max():.4f}]")
print(f"z range: [{z.min():.4f}, {z.max():.4f}]")
print(f"x variance: {np.var(x):.4f}")

# Check for "flat line" (low variance)
if np.var(x) < 1e-4:
    print("\nWARNING: Signal is flat!")
else:
    print("\nSUCCESS: Signal has variance, likely chaotic/periodic.")

# Plot 3D attractor (simple projection)
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, s=0.5, alpha=0.6)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Replicated Figure 5b (Paper Parameters)')
plt.savefig('paper_verification.png')
print("\nPlot saved to paper_verification.png")
