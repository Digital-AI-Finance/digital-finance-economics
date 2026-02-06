r"""Gresham's Law: Currency Substitution Simulation

Agent-based model demonstrating how bad money drives out good.
Agents choose which currency to spend based on depreciation rates.

Economic model: $\frac{dM_g}{dt} < 0$ when $\frac{V_b}{V_g} > 1$ (bad money drives out good).
Circulation share evolves based on relative depreciation rates.

Citation: Selgin (1996) - Salvaging Gresham's Law: The Good, the Bad, and the Illegal
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

# Simulation parameters
N_agents = 1000
T_periods = 100
r_A = -0.02  # Currency A depreciates 2% per period
r_B = 0.03   # Currency B appreciates 3% per period

# Calculate spending probability for currency A (bad money)
# Higher probability when r_B - r_A is large (big difference favoring B)
r_diff = r_B - r_A
prob_spend_A = 1 / (1 + np.exp(-5 * r_diff))

# Initialize tracking arrays
circulation_A = np.zeros(T_periods)
circulation_B = np.zeros(T_periods)

# Run simulation
for t in range(T_periods):
    # Each agent makes spending decision
    spend_A = np.random.rand(N_agents) < prob_spend_A

    # Calculate circulation shares
    circulation_A[t] = spend_A.sum() / N_agents
    circulation_B[t] = 1 - circulation_A[t]

# Find tipping point (where A > 80%)
tipping_idx = np.where(circulation_A > 0.80)[0]
tipping_point = tipping_idx[0] if len(tipping_idx) > 0 else None

# Create plot
fig, ax = plt.subplots()

# Plot circulation shares
periods = np.arange(T_periods)
ax.plot(periods, circulation_A * 100, color=MLRED, linewidth=2.5,
        label='Currency A (depreciating, r=-2%)', marker='o', markevery=10, markersize=5)
ax.plot(periods, circulation_B * 100, color=MLGREEN, linewidth=2.5,
        label='Currency B (appreciating, r=+3%)', marker='s', markevery=10, markersize=5)

# Add 80% threshold line
ax.axhline(y=80, color='gray', linestyle=':', linewidth=1.5, alpha=0.6, label='80% threshold')

# Mark tipping point
if tipping_point is not None:
    ax.axvline(x=tipping_point, color=MLPURPLE, linestyle='--', linewidth=2, alpha=0.7)
    ax.annotate('Tipping point:\nA dominates circulation',
                xy=(tipping_point, 80), xytext=(tipping_point + 15, 60),
                arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5),
                fontsize=11, color=MLPURPLE, ha='left',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=MLPURPLE, alpha=0.8))

# Add annotation for Gresham's Law dynamics
ax.annotate('Currency A (depreciating)\ndominates spending',
            xy=(70, circulation_A[70] * 100), xytext=(50, 95),
            arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
            fontsize=11, color=MLRED, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=MLRED, alpha=0.8))

ax.annotate('Currency B (appreciating)\nis hoarded',
            xy=(70, circulation_B[70] * 100), xytext=(50, 15),
            arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5),
            fontsize=11, color=MLGREEN, ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=MLGREEN, alpha=0.8))

# Labels and title
ax.set_xlabel('Time Period', fontweight='bold')
ax.set_ylabel('Circulation Share (%)', fontweight='bold')
ax.set_title("Gresham's Law: How Bad Money Drives Out Good Money", fontweight='bold', pad=15)
ax.legend(loc='center right', framealpha=0.95)
ax.grid(True, alpha=0.3, linestyle='--')

# Set axis limits
ax.set_xlim(0, T_periods - 1)
ax.set_ylim(0, 105)

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
