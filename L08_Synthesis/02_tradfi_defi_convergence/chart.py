"""TradFi-DeFi Convergence: Dual Technology Adoption

Coupled S-curve model showing mutual influence and convergence dynamics.
Theory: Rogers (1962) Diffusion of Innovations, Moore (1991) Technology Adoption Lifecycle.

Based on: Zetzsche et al. (2020) - DeFi Decentralized Finance
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (10, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Time axis: 1990-2035
years = np.linspace(1990, 2035, 500)
t = years - 1990  # Time since 1990

# Parameters for TradFi digitization S-curve
K_T = 85  # Maximum adoption (%)
t0_T = 10  # Inflection point (year 2000)
r_T_base = 0.25  # Base growth rate (slower start)

# Parameters for DeFi adoption S-curve
K_D = 70  # Maximum adoption (%)
t0_D = 30  # Inflection point (year 2020)
r_D_base = 0.35  # Base growth rate (faster initial growth)

# Spillover parameters
alpha_T = 0.003  # TradFi learns from DeFi
alpha_D = 0.004  # DeFi benefits from TradFi
reg_friction = 0.85  # Regulatory friction (slows convergence)
tech_friction = 0.92  # Technology friction (limits interoperability)

# Coupled S-curve model with spillover
def coupled_adoption(t, K_T, K_D, t0_T, t0_D, r_T_base, r_D_base, alpha_T, alpha_D):
    S_T = np.zeros_like(t)
    S_D = np.zeros_like(t)

    # Initial conditions
    S_T[0] = 10  # TradFi starts at 10%
    S_D[0] = 0.1  # DeFi starts near zero

    # Iterative calculation with spillover effects
    dt = t[1] - t[0]
    for i in range(1, len(t)):
        # Growth rates with spillover
        r_T = r_T_base + alpha_T * S_D[i-1] / 100
        r_D = r_D_base + alpha_D * S_T[i-1] / 100

        # S-curve differential equations
        dS_T = r_T * S_T[i-1] * (1 - S_T[i-1] / K_T) * tech_friction
        dS_D = r_D * S_D[i-1] * (1 - S_D[i-1] / K_D) * reg_friction

        S_T[i] = S_T[i-1] + dS_T * dt
        S_D[i] = S_D[i-1] + dS_D * dt

        # Ensure non-negative
        S_T[i] = max(0, min(S_T[i], K_T))
        S_D[i] = max(0, min(S_D[i], K_D))

    return S_T, S_D

# Baseline model
S_T, S_D = coupled_adoption(t, K_T, K_D, t0_T, t0_D, r_T_base, r_D_base, alpha_T, alpha_D)

# Uncertainty bands (Monte Carlo)
n_sims = 50
S_T_sims = []
S_D_sims = []

for _ in range(n_sims):
    # Vary parameters
    K_T_sim = K_T + np.random.uniform(-5, 5)
    K_D_sim = K_D + np.random.uniform(-10, 15)
    r_T_sim = r_T_base * np.random.uniform(0.9, 1.1)
    r_D_sim = r_D_base * np.random.uniform(0.85, 1.15)
    alpha_T_sim = alpha_T * np.random.uniform(0.8, 1.2)
    alpha_D_sim = alpha_D * np.random.uniform(0.8, 1.2)

    S_T_sim, S_D_sim = coupled_adoption(t, K_T_sim, K_D_sim, t0_T, t0_D,
                                         r_T_sim, r_D_sim, alpha_T_sim, alpha_D_sim)
    S_T_sims.append(S_T_sim)
    S_D_sims.append(S_D_sim)

S_T_sims = np.array(S_T_sims)
S_D_sims = np.array(S_D_sims)

# Calculate percentiles for uncertainty bands
S_T_lower = np.percentile(S_T_sims, 10, axis=0)
S_T_upper = np.percentile(S_T_sims, 90, axis=0)
S_D_lower = np.percentile(S_D_sims, 10, axis=0)
S_D_upper = np.percentile(S_D_sims, 90, axis=0)

# Convergence analysis (70% feature overlap threshold)
convergence_threshold = 0.7
feature_overlap = 1 - np.abs(S_T - S_D) / 100
convergence_idx = np.where(feature_overlap >= convergence_threshold)[0]
if len(convergence_idx) > 0:
    convergence_year = years[convergence_idx[0]]
else:
    convergence_year = None

# Visualization
fig, ax = plt.subplots(figsize=(12, 7))

# Uncertainty bands
ax.fill_between(years, S_T_lower, S_T_upper, color=MLBLUE, alpha=0.2, label='TradFi Uncertainty')
ax.fill_between(years, S_D_lower, S_D_upper, color=MLORANGE, alpha=0.2, label='DeFi Uncertainty')

# Main S-curves
ax.plot(years, S_T, color=MLBLUE, linewidth=2.5, label='TradFi Digitization')
ax.plot(years, S_D, color=MLORANGE, linewidth=2.5, label='DeFi Adoption')

# Convergence corridor
if convergence_year:
    convergence_idx_end = min(convergence_idx[-1] + 50, len(years) - 1)
    ax.axvspan(years[convergence_idx[0]], years[convergence_idx_end],
               color=MLPURPLE, alpha=0.15, label='Convergence Corridor')
    ax.axvline(convergence_year, color=MLPURPLE, linestyle='--', alpha=0.6, linewidth=1.5)
    ax.text(convergence_year + 1, 50, f'Convergence\n~{int(convergence_year)}',
            fontsize=11, color=MLPURPLE, fontweight='bold')

# Key event annotations
events = [
    (2008, 20, '2008 Financial Crisis', MLRED),
    (2020, 15, '2020 DeFi Summer', MLGREEN),
    (2024, 60, '2024 Spot ETFs', MLGREEN)
]

for year, y_pos, label, color in events:
    ax.axvline(year, color=color, linestyle=':', alpha=0.5, linewidth=1)
    ax.text(year, y_pos, label, rotation=90, fontsize=10,
            color=color, ha='right', va='bottom', alpha=0.8)

ax.set_xlabel('Year', fontsize=14, fontweight='bold')
ax.set_ylabel('Adoption / Feature Coverage (%)', fontsize=14, fontweight='bold')
ax.set_title('TradFi-DeFi Convergence: Dual Technology Adoption\n' +
             'Coupled S-Curves with Cross-Platform Spillover Effects',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlim(1990, 2035)
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', fontsize=12, framealpha=0.95)

# Educational annotation
ax.text(0.02, 0.98, 'S-Curve: S(t) = K/(1+e^(-r(t-t₀)))\nConvergence when |ST - SD| < ε',
        transform=ax.transAxes, fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))

# Citations
ax.text(0.98, 0.02,
        'Theory: Rogers (1962) Diffusion of Innovations; Moore (1991) Technology Adoption Lifecycle',
        transform=ax.transAxes, fontsize=9, ha='right', va='bottom',
        style='italic', color='gray')

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
