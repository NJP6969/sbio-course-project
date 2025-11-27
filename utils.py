"""
Utility functions for Memristive FitzHugh-Nagumo System
Contains core ODE functions, numerical methods, and visualization helpers
"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from config import VIZ_PARAMS


# ============================================================================
# FITZHUGH-NAGUMO NEURON MODELS
# ============================================================================

def fitzhugh_nagumo_ode(state, t, a, b, tau, I_ext):
    """
    Single FitzHugh-Nagumo neuron dynamics (continuous-time)
    
    Parameters:
    -----------
    state : array-like, shape (2,)
        [v, w] where v is membrane potential, w is recovery variable
    t : float
        Time (required by odeint but not used in autonomous system)
    a, b : float
        FHN model parameters
    tau : float
        Time constant for recovery variable
    I_ext : float
        External input current
    
    Returns:
    --------
    derivatives : array, shape (2,)
        [dv/dt, dw/dt]
    """
    v, w = state
    dv_dt = v - (v**3)/3 - w + I_ext
    dw_dt = (v + a - b*w) / tau
    return [dv_dt, dw_dt]


def fhn_nullclines(v_range, a, b, I_ext):
    """
    Calculate FHN nullclines for phase plane analysis
    
    Parameters:
    -----------
    v_range : array
        Range of v values
    a, b : float
        FHN parameters
    I_ext : float
        External current
    
    Returns:
    --------
    w_v_nullcline : array
        w values on v-nullcline (dv/dt = 0)
    w_w_nullcline : array
        w values on w-nullcline (dw/dt = 0)
    """
    # v-nullcline: dv/dt = 0 => w = v - v^3/3 + I_ext
    w_v_nullcline = v_range - (v_range**3)/3 + I_ext
    
    # w-nullcline: dw/dt = 0 => w = (v + a) / b
    w_w_nullcline = (v_range + a) / b
    
    return w_v_nullcline, w_w_nullcline


# ============================================================================
# COUPLED NEURON SYSTEMS
# ============================================================================

def coupled_fhn_static(state, t, params):
    """
    Two FHN neurons with static coupling
    
    Parameters:
    -----------
    state : array, shape (4,)
        [v1, w1, v2, w2] for teacher and student neurons
    t : float
        Time
    params : dict
        Must contain: 'a', 'b', 'tau', 'I_ext', 'g' (coupling strength)
    
    Returns:
    --------
    derivatives : array, shape (4,)
    """
    v1, w1, v2, w2 = state
    a = params['a']
    b = params['b']
    tau = params['tau']
    I_ext = params['I_ext']
    g = params['g']  # Static coupling strength
    
    # Teacher neuron (receives external input)
    dv1_dt = v1 - (v1**3)/3 - w1 + I_ext
    dw1_dt = (v1 + a - b*w1) / tau
    
    # Student neuron (receives coupling from teacher)
    I_syn = g * (v1 - v2)  # Static synaptic current
    dv2_dt = v2 - (v2**3)/3 - w2 + I_syn
    dw2_dt = (v2 + a - b*w2) / tau
    
    return [dv1_dt, dw1_dt, dv2_dt, dw2_dt]


# ============================================================================
# DISCRETE MEMRISTOR (from Shatnawi et al. 2023)
# ============================================================================

def discrete_memristor_step(x_n, v_n, a, b, h):
    """
    Single step of discrete memristor update
    
    x_{n+1} = x_n + h[a*sin(x_n) + b*v_n]
    
    Parameters:
    -----------
    x_n : float
        Current memristor state
    v_n : float
        Input voltage (potential difference)
    a, b, h : float
        Memristor parameters
    
    Returns:
    --------
    x_next : float
        Next memristor state
    """
    return x_n + h * (a * np.sin(x_n) + b * v_n)


def discrete_memristor_current(x_n, v_n):
    """
    Memristor current: i_n = x_n * v_n
    
    Parameters:
    -----------
    x_n : float
        Memristor state
    v_n : float
        Voltage
    
    Returns:
    --------
    i_n : float
        Current through memristor
    """
    return x_n * v_n


# ============================================================================
# MEMRISTIVE FHN SYSTEM (Discrete-time)
# ============================================================================

def memristive_fhn_map(state, params):
    """
    3D discrete memristive FHN neuron map (Shatnawi et al. 2023, Eq. 12)
    
    x(n+1) = x(n) - x³(n)/3 - y(n) + I_ext + k1*z(n)*x(n)
    y(n+1) = γ*y(n) + θ*x(n) + δ
    z(n+1) = z(n) + sin(z(n)) - k2*x(n)
    
    Parameters:
    -----------
    state : array, shape (3,)
        [x, y, z] where x=membrane potential, y=recovery, z=memristor state
    params : dict
        Must contain: 'gamma', 'theta', 'delta', 'I_ext', 'k1', 'k2'
    
    Returns:
    --------
    next_state : array, shape (3,)
    """
    x, y, z = state
    
    gamma = params['gamma']
    theta = params['theta']
    delta = params['delta']
    I_ext = params['I_ext']
    k1 = params['k1']
    k2 = params['k2']
    
    # Membrane potential update
    x_next = x - (x**3)/3 - y + I_ext + k1 * z * x
    
    # Recovery variable update
    y_next = gamma * y + theta * x + delta
    
    # Memristor state update
    z_next = z + np.sin(z) - k2 * x
    
    return np.array([x_next, y_next, z_next])


def iterate_memristive_fhn(initial_state, params, n_steps, transient=0):
    """
    Iterate the memristive FHN map
    
    Parameters:
    -----------
    initial_state : array, shape (3,)
        Initial [x, y, z]
    params : dict
        System parameters
    n_steps : int
        Number of iterations
    transient : int
        Number of initial steps to discard
    
    Returns:
    --------
    trajectory : array, shape (n_steps - transient, 3)
        System trajectory after transient
    """
    state = np.array(initial_state, dtype=float)
    trajectory = []
    
    for i in range(n_steps):
        state = memristive_fhn_map(state, params)
        if i >= transient:
            trajectory.append(state.copy())
    
    return np.array(trajectory)


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def calculate_lyapunov_exponent(trajectory, max_iterations=5000):
    """
    Estimate largest Lyapunov exponent using nearest-neighbor method
    
    Parameters:
    -----------
    trajectory : array, shape (n, dim)
        System trajectory
    max_iterations : int
        Maximum iterations for calculation
    
    Returns:
    --------
    lyapunov : float
        Estimated largest Lyapunov exponent
    """
    n_points = min(len(trajectory), max_iterations)
    d0 = 1e-10  # Initial separation
    sum_log = 0
    
    for i in range(1, n_points):
        # Simplified method: measure rate of separation
        if i > 1:
            separation = np.linalg.norm(trajectory[i] - trajectory[i-1])
            if separation > 1e-15:
                sum_log += np.log(separation / d0)
    
    return sum_log / n_points if n_points > 0 else 0


def phase_difference(v1, v2):
    """
    Calculate instantaneous phase difference between two oscillating signals
    
    Parameters:
    -----------
    v1, v2 : array
        Two time series
    
    Returns:
    --------
    phase_diff : array
        Phase difference over time
    """
    # Simple approach: use Hilbert transform or cross-correlation
    # For now, use normalized difference
    return v1 - v2


def synchronization_index(v1, v2):
    """
    Calculate synchronization index (correlation-based)
    
    Parameters:
    -----------
    v1, v2 : array
        Two time series
    
    Returns:
    --------
    sync_index : float
        Value between 0 (no sync) and 1 (perfect sync)
    """
    correlation = np.corrcoef(v1, v2)[0, 1]
    return abs(correlation)


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_neuron_timeseries(t, v1, v2=None, M=None, labels=None):
    """
    Plot time series of neuron dynamics
    
    Parameters:
    -----------
    t : array
        Time points
    v1 : array
        First neuron membrane potential
    v2 : array, optional
        Second neuron membrane potential
    M : array, optional
        Memristor/synaptic weight
    labels : dict, optional
        Custom labels
    """
    if labels is None:
        labels = {'v1': 'Teacher', 'v2': 'Student', 'M': 'Synaptic Weight'}
    
    n_plots = 1 + (v2 is not None) + (M is not None)
    fig, axes = plt.subplots(n_plots, 1, figsize=(VIZ_PARAMS['figsize'][0], 3*n_plots))
    
    if n_plots == 1:
        axes = [axes]
    
    plot_idx = 0
    
    # Plot teacher neuron
    axes[plot_idx].plot(t, v1, color=VIZ_PARAMS['teacher_color'], 
                        linewidth=VIZ_PARAMS['linewidth'], label=labels['v1'])
    axes[plot_idx].set_ylabel('Membrane Potential (v)')
    axes[plot_idx].legend()
    axes[plot_idx].grid(True, alpha=0.3)
    plot_idx += 1
    
    # Plot student neuron if provided
    if v2 is not None:
        axes[plot_idx].plot(t, v2, color=VIZ_PARAMS['student_color'], 
                           linewidth=VIZ_PARAMS['linewidth'], label=labels['v2'])
        axes[plot_idx].set_ylabel('Membrane Potential (v)')
        axes[plot_idx].legend()
        axes[plot_idx].grid(True, alpha=0.3)
        plot_idx += 1
    
    # Plot memristor/synaptic weight if provided
    if M is not None:
        axes[plot_idx].plot(t, M, color=VIZ_PARAMS['memristor_color'], 
                           linewidth=VIZ_PARAMS['linewidth'], label=labels['M'])
        axes[plot_idx].set_ylabel('Synaptic Weight (M)')
        axes[plot_idx].set_xlabel('Time')
        axes[plot_idx].legend()
        axes[plot_idx].grid(True, alpha=0.3)
    else:
        axes[-1].set_xlabel('Time')
    
    plt.tight_layout()
    return fig, axes


def plot_phase_plane(v, w, params, trajectory=None, title='Phase Plane'):
    """
    Plot phase plane with nullclines
    
    Parameters:
    -----------
    v : array
        Range of v values for nullclines
    w : array
        Range of w values
    params : dict
        FHN parameters
    trajectory : array, optional
        Trajectory to overlay, shape (n, 2) as [v, w]
    title : str
        Plot title
    """
    fig, ax = plt.subplots(figsize=VIZ_PARAMS['figsize'])
    
    # Calculate and plot nullclines
    w_v_null, w_w_null = fhn_nullclines(v, params['a'], params['b'], params['I_ext'])
    
    ax.plot(v, w_v_null, 'b--', linewidth=2, label='v-nullcline (dv/dt=0)', alpha=0.7)
    ax.plot(v, w_w_null, 'r--', linewidth=2, label='w-nullcline (dw/dt=0)', alpha=0.7)
    
    # Plot trajectory if provided
    if trajectory is not None:
        ax.plot(trajectory[:, 0], trajectory[:, 1], 'k-', linewidth=1, alpha=0.6, label='Trajectory')
        ax.plot(trajectory[0, 0], trajectory[0, 1], 'go', markersize=8, label='Start')
        ax.plot(trajectory[-1, 0], trajectory[-1, 1], 'ro', markersize=8, label='End')
    
    ax.set_xlabel('Membrane Potential (v)')
    ax.set_ylabel('Recovery Variable (w)')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig, ax


def plot_bifurcation_diagram(param_values, trajectories, param_name='Parameter'):
    """
    Create bifurcation diagram
    
    Parameters:
    -----------
    param_values : array
        Parameter values used
    trajectories : list of arrays
        List of trajectories for each parameter value
    param_name : str
        Name of bifurcation parameter
    """
    fig, ax = plt.subplots(figsize=VIZ_PARAMS['figsize'])
    
    for i, param_val in enumerate(param_values):
        traj = trajectories[i]
        # Plot last portion of trajectory
        x_vals = traj[:, 0]  # Membrane potential
        param_array = np.full_like(x_vals, param_val)
        ax.plot(param_array, x_vals, ',k', markersize=0.5, alpha=0.5)
    
    ax.set_xlabel(param_name)
    ax.set_ylabel('Membrane Potential (x)')
    ax.set_title(f'Bifurcation Diagram vs {param_name}')
    ax.grid(True, alpha=0.3)
    
    return fig, ax
