# Adaptive Synchronization in Biological Networks

**Project**: Modeling Hebbian Learning and Synaptic Plasticity using a Memristive FitzHugh-Nagumo System

**Authors**: Narasimha and Vanshika  
**Course**: Systems Biology  
**Date**: November 2025

---

## 📋 Project Overview

This project implements a computational model to study **synaptic plasticity** and **Hebbian learning** in neural networks. We combine the **FitzHugh-Nagumo neuron model** with **memristive coupling** to demonstrate self-organized learning and synchronization.

### Key Features:
- ✅ Self-organized Hebbian learning ("cells that fire together, wire together")
- ✅ Discrete memristor implementation with hysteresis loops
- ✅ Robustness analysis (parameter mismatch, noise, perturbations)
- ✅ Complete coverage of all 5 Systems Biology course units
- ✅ Interactive Jupyter notebooks with visualizations

---

## 🎯 Course Unit Coverage

| Unit | Topic | Implementation |
|------|-------|----------------|
| **Unit 1** | Network Motifs | 2-node feed-forward motif with adaptive edge |
| **Unit 2** | Design Principles | Adaptation through Hebbian plasticity |
| **Unit 3** | Dynamic Modeling | 5D ODE system + 3D discrete map |
| **Unit 4** | Switches & Clocks | Excitable neuron + memristor conductance switch |
| **Unit 5** | Robustness | Parameter mismatch, noise, structural stability |

---

## 📂 Project Structure

```
sbio/
├── 01_neuron_basics.ipynb              # Single FHN neuron dynamics
├── 02_coupled_neurons.ipynb            # Static coupling & synchronization
├── 03_memristive_synapse.ipynb         # Discrete memristor implementation
├── 04_learning_dynamics.ipynb          # Hebbian learning demonstration
├── 05_robustness_analysis.ipynb        # Robustness testing
├── 06_systems_biology_analysis.ipynb   # Course unit mapping & synthesis
├── config.py                           # Parameter configurations
├── utils.py                            # Helper functions & models
├── requirements.txt                    # Python dependencies
├── project.md                          # Original project proposal
├── paper.txt                           # Reference paper (Shatnawi et al. 2023)
└── README.md                           # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab

### Installation Steps

1. **Clone or navigate to the project directory**:
   ```bash
   cd c:\Users\narsi\sbio
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch Jupyter**:
   ```bash
   jupyter notebook
   ```

4. **Open notebooks in order** (01 → 02 → 03 → 04 → 05 → 06)

---

## 📘 Notebook Descriptions

### Notebook 1: Single Neuron Basics
- Implements FitzHugh-Nagumo equations
- Phase plane analysis with nullclines
- Demonstrates excitability vs oscillatory regimes
- Pulse response and action potentials

### Notebook 2: Coupled Neurons
- Two-neuron system with static coupling
- Synchronization threshold analysis
- Cross-correlation metrics
- Preparation for adaptive coupling

### Notebook 3: Memristive Synapse
- Discrete memristor model (Shatnawi et al. 2023)
- Pinched hysteresis loops (frequency/amplitude dependent)
- Multistability demonstration
- 3D memristive FHN attractor

### Notebook 4: Learning Dynamics
- Hebbian plasticity implementation
- Self-organized learning (M: 0 → 1)
- Synchronization emergence
- Learning parameter effects (α, β)

### Notebook 5: Robustness Analysis
- Parameter mismatch tolerance (±30%)
- Noise robustness testing
- Parameter space exploration (heatmaps)
- Recovery from perturbations

### Notebook 6: Systems Biology Analysis
- Comprehensive course unit mapping
- Biological interpretations
- Project synthesis
- References and further reading

---

## 🧮 Mathematical Models

### Continuous-Time (Hebbian Plasticity)
5D ODE system:
```
dv₁/dt = v₁ - v₁³/3 - w₁ + I_ext
dw₁/dt = (v₁ + a - b·w₁)/τ
dv₂/dt = v₂ - v₂³/3 - w₂ + M·(v₁ - v₂)
dw₂/dt = (v₂ + a - b·w₂)/τ
dM/dt = α·(v₁ - v₂)²·(1-M) - β·M
```

### Discrete-Time (Memristive FHN)
3D map:
```
x_{n+1} = x_n - x_n³/3 - y_n + I_ext + k₁·z_n·x_n
y_{n+1} = γ·y_n + θ·x_n + δ
z_{n+1} = z_n + sin(z_n) - k₂·x_n
```

---

## 📊 Key Results

### Learning Demonstration
- **Initial state**: M = 0 (unconnected neurons)
- **Final state**: M ≈ 1 (strongly connected)
- **Synchronization**: 0.2 → 0.95
- **Learning time**: ~150 time units

### Robustness Findings
- ✅ Tolerates **30% parameter mismatch**
- ✅ Robust to **noise** (σ ≤ 0.1)
- ✅ **Recovers** from synaptic damage
- ✅ **Wide parameter range** supports learning

### Memristor Properties
- ✅ Pinched hysteresis loops confirmed
- ✅ Frequency-dependent memory
- ✅ Multistability (initial condition dependent)
- ✅ Nonvolatile memory (POP analysis)

---

## 🧬 Biological Relevance

### Hebbian Learning
Our model captures the essence of **Long-Term Potentiation (LTP)**:
- Repeated co-activation strengthens synapses
- Enables associative learning and memory
- Foundation of neural network algorithms

### Memristive Synapses
The discrete memristor mimics **biological synapses**:
- State-dependent conductance
- History-dependent plasticity
- Energy-efficient computation

### Design Principles
Demonstrates key biological principles:
- **Adaptation**: Self-optimization through plasticity
- **Robustness**: Function maintained despite perturbations
- **Self-organization**: Emergent order without central control

---

## 🔧 Dependencies

```
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
jupyter>=1.0.0
notebook>=6.4.0
ipywidgets>=7.6.0
seaborn>=0.11.0
```

---

## 📚 References

### Primary Reference
**Shatnawi, M.T., et al. (2023)**. "A Multistable Discrete Memristor and Its Application to Discrete-Time FitzHugh–Nagumo Model." *Electronics*, 12(13), 2929.

### Key Concepts
- **FitzHugh-Nagumo Model**: Simplified neuron dynamics
- **Hebbian Plasticity**: Activity-dependent synaptic strengthening
- **Memristors**: Memory resistors with history-dependent conductance
- **Systems Biology**: Design principles in biological circuits

### Textbooks
- Alon, U. (2019). *An Introduction to Systems Biology: Design Principles of Biological Circuits*
- Izhikevich, E.M. (2007). *Dynamical Systems in Neuroscience*
- Strogatz, S.H. (2015). *Nonlinear Dynamics and Chaos*

---

## 🎓 Learning Outcomes

By completing this project, you will:
1. ✅ Understand **neuronal excitability** and dynamics
2. ✅ Implement **synaptic plasticity** mathematically
3. ✅ Analyze **synchronization** in coupled systems
4. ✅ Test **robustness** of biological systems
5. ✅ Connect **mathematical models** to **biological function**
6. ✅ Master **numerical methods** for ODEs and discrete maps

---

## 🌟 Highlights

> **"Cells that fire together, wire together"** - Donald Hebb

This project demonstrates that:
- Simple plasticity rules can lead to complex adaptive behavior
- Learning emerges without external supervision
- Robustness arises from distributed, local control
- Mathematical models bridge theory and biology

---

## 🤝 Contributing

This project was developed for educational purposes. Feel free to:
- Extend the models (e.g., add more neurons, different plasticity rules)
- Explore other parameter regimes
- Apply to different biological systems
- Implement in hardware (neuromorphic chips)

---

## 📧 Contact

**Students**: Narasimha and Vanshika  
**Course**: Systems Biology  
**Institution**: [Your University]  
**Date**: November 2025

---

## 📝 License

This project is for educational purposes as part of a Systems Biology course.

---

## 🙏 Acknowledgments

- **Shatnawi et al.** for the memristive FHN model
- **Uri Alon** for Systems Biology design principles
- Course instructors and TAs for guidance

---



