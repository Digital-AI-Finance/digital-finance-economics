r"""Gresham's Law: Currency Substitution Simulation

Agent-based model demonstrating how bad money drives out good.
Agents choose which currency to spend via a logit feedback loop
that produces an S-curve tipping dynamic.

Economic Model:
    Spending probability for Currency A (depreciating) at time $t$:
    $P(\text{spend A})_t = \frac{1}{1 + e^{-z_t}}$

    where the logit argument evolves as:
    $z_t = k \cdot (s_{t-1} - 0.5) + b \cdot \frac{t}{T}$

    $s_t$ = share of agents spending Currency A (smoothed),
    $k = 15.0$ = feedback strength, $b = 0.10$ = base bias from depreciation.
    Positive feedback: as more agents spend A, it becomes rational
    to also spend A, producing an S-curve tipping at period ~40-50.

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
r_A = 0.05   # Currency A depreciates 5% per period (bad money)
r_B = 0.01   # Currency B depreciates 1% per period (good money)

# Logit feedback parameters (per D6, tuned for tipping at ~period 40-50)
k_feedback = 15.0   # Feedback strength: how much past share amplifies
base_bias = 0.10    # Base bias from depreciation difference

# Track share of agents spending Currency A (the depreciating one)
share_A = np.zeros(T_periods)
share_A[0] = 0.50   # Start at equal split

# Run simulation with logit feedback loop
for t in range(1, T_periods):
    # Logit argument: positive feedback from past share + time-increasing bias
    logit_arg = k_feedback * (share_A[t-1] - 0.5) + base_bias * t / T_periods
    prob_spend_A = 1 / (1 + np.exp(-logit_arg))

    # Agent simulation: each agent decides to spend A or B
    n_spend_A = np.sum(np.random.random(N_agents) < prob_spend_A)

    # Smoothed update: 95% persistence + 5% new observation
    share_A[t] = 0.95 * share_A[t-1] + 0.05 * (n_spend_A / N_agents)

# Derive circulation arrays for plotting
circulation_A = share_A
circulation_B = 1 - share_A

# Find tipping point (where A > 80%)
tipping_idx = np.where(circulation_A > 0.80)[0]
tipping_point = tipping_idx[0] if len(tipping_idx) > 0 else None

# Create plot
fig, ax = plt.subplots()

# Plot circulation shares
periods = np.arange(T_periods)
ax.plot(periods, circulation_A * 100, color=MLRED, linewidth=2.5,
        label='Currency A (depreciating, r=5%)', marker='o', markevery=10, markersize=5)
ax.plot(periods, circulation_B * 100, color=MLGREEN, linewidth=2.5,
        label='Currency B (stable, r=1%)', marker='s', markevery=10, markersize=5)

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
