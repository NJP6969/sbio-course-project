
# Simulation Parameters
# ---------------------

# Continuous FitzHugh-Nagumo Parameters (for notebooks 1, 2, 4)
FHN_PARAMS = {
    'a': 0.7,
    'b': 0.8,
    'tau': 12.5,
    'I_ext': 0.5
}

# Learning/Plasticity Parameters (for notebook 4)
LEARNING_PARAMS = {
    'alpha': 0.01,    # Learning rate (weight increase)
    'beta': 0.001,    # Forgetting rate (weight decay)
    'g_max': 1.0      # Maximum synaptic weight
}

# Discrete FitzHugh-Nagumo Parameters
# Source: Shatnawi et al. (2023) - Section 3.2
# gamma = -0.2, delta = 0.08, theta = 0.108, I_ext = 2.0
FHN_DISCRETE_PARAMS = {
    'gamma': -0.2,   # Recovery variable coefficient
    'theta': 0.108,  # Coupling parameter
    'delta': 0.08,   # Offset parameter  
    'I_ext': 2.0     # External current (paper value for chaotic dynamics)
}

# Memristor Parameters
# Source: Shatnawi et al. (2023)
# Section 3.2: k1 = -0.06, k2 = 0.2
MEMRISTOR_PARAMS = {
    'alpha': 0.1,
    'beta': 0.1,
    'k1': -0.06,   # Feedback strength
    'k2': 0.2,     # Feedback strength
    'a': 0.005,    # Memristor internal parameter
    'b': -2,       # Memristor internal parameter
    'h': 0.001     # Time step for memristor
}

# Simulation Settings
SIM_PARAMS = {
    'n_steps': 10000,
    'transient': 2000,
    'x0': 0.01,
    'y0': 0.02,
    'z0': 0.1
}

# Visualization
VIZ_PARAMS = {
    'teacher_color': '#2C3E50',  # Dark Blue
    'student_color': '#E74C3C',  # Red
    'memristor_color': '#8E44AD', # Purple
    'coupling_color': '#27AE60',  # Green
    'figure_size': (12, 8),
    'dpi': 100,
    'linewidth': 1.5,
    'figsize': (10, 6)
}
