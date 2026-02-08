r"""Gresham's Law: Variations in Feedback Strength and Depreciation

This script generates a 2x2 panel showing how parameter changes affect tipping dynamics:
- Panel 1 (Top Left): Baseline (k=15, r_A=0.05, r_B=0.01)
- Panel 2 (Top Right): Variation 1 - Weak Feedback (k=5)
- Panel 3 (Bottom Left): Variation 2 - Strong Feedback (k=25)
- Panel 4 (Bottom Right): Variation 3 - Equal Depreciation (r_A=r_B=0.03)

Each panel shows circulation shares and marks tipping point (if it exists).
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 11, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.figsize': (16, 12), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Shared simulation parameters
N_agents = 1000
T_periods = 100
base_bias = 0.10

def run_simulation(k_feedback, r_A, r_B):
    """Run Gresham's Law simulation with given parameters."""
    np.random.seed(42)  # Reset seed for each simulation

    share_A = np.zeros(T_periods)
    share_A[0] = 0.50

    for t in range(1, T_periods):
        depreciation_bias = (r_A - r_B) * 10  # Depreciation differential drives Gresham's Law
        logit_arg = k_feedback * (share_A[t-1] - 0.5) + depreciation_bias + base_bias * t / T_periods
        prob_spend_A = 1 / (1 + np.exp(-logit_arg))
        n_spend_A = np.sum(np.random.random(N_agents) < prob_spend_A)
        share_A[t] = 0.95 * share_A[t-1] + 0.05 * (n_spend_A / N_agents)

    circulation_A = share_A
    circulation_B = 1 - share_A

    # Find tipping point (where A > 80%)
    tipping_idx = np.where(circulation_A > 0.80)[0]
    tipping_point = tipping_idx[0] if len(tipping_idx) > 0 else None

    return circulation_A, circulation_B, tipping_point

def plot_panel(ax, circulation_A, circulation_B, tipping_point, title, k_val, r_A_val, r_B_val):
    """Plot a single panel with circulation shares and tipping point."""
    periods = np.arange(T_periods)

    ax.plot(periods, circulation_A * 100, color=MLRED, linewidth=2,
            label=f'Currency A (r={r_A_val*100:.0f}%)', marker='o', markevery=15, markersize=4)
    ax.plot(periods, circulation_B * 100, color=MLGREEN, linewidth=2,
            label=f'Currency B (r={r_B_val*100:.0f}%)', marker='s', markevery=15, markersize=4)

    ax.axhline(y=80, color='gray', linestyle=':', linewidth=1.2, alpha=0.5)

    if tipping_point is not None:
        ax.axvline(x=tipping_point, color=MLPURPLE, linestyle='--', linewidth=1.5, alpha=0.6)
        ax.annotate(f'Tipping: t={tipping_point}',
                    xy=(tipping_point, 80), xytext=(tipping_point + 10, 65),
                    arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.2),
                    fontsize=9, color=MLPURPLE, ha='left',
                    bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                             edgecolor=MLPURPLE, alpha=0.7))
    else:
        ax.text(50, 90, 'No tipping:\nCurrencies coexist',
                fontsize=9, color=MLPURPLE, ha='center',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                         edgecolor=MLPURPLE, alpha=0.7))

    ax.set_xlabel('Time Period', fontweight='bold')
    ax.set_ylabel('Circulation Share (%)', fontweight='bold')
    ax.set_title(f'{title}\n(k={k_val}, r_A={r_A_val*100:.0f}%, r_B={r_B_val*100:.0f}%)',
                 fontweight='bold', pad=10)
    ax.legend(loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(0, T_periods - 1)
    ax.set_ylim(0, 105)

# Create 2x2 subplot figure
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Panel 1: Baseline (k=15, r_A=0.05, r_B=0.01)
circ_A, circ_B, tip = run_simulation(k_feedback=15.0, r_A=0.05, r_B=0.01)
plot_panel(axes[0, 0], circ_A, circ_B, tip,
           'BASELINE', k_val=15.0, r_A_val=0.05, r_B_val=0.01)

# Panel 2: Variation 1 - Weak Feedback (k=5)
circ_A, circ_B, tip = run_simulation(k_feedback=5.0, r_A=0.05, r_B=0.01)
plot_panel(axes[0, 1], circ_A, circ_B, tip,
           'VARIATION 1: Weak Feedback', k_val=5.0, r_A_val=0.05, r_B_val=0.01)

# Panel 3: Variation 2 - Strong Feedback (k=25)
circ_A, circ_B, tip = run_simulation(k_feedback=25.0, r_A=0.05, r_B=0.01)
plot_panel(axes[1, 0], circ_A, circ_B, tip,
           'VARIATION 2: Strong Feedback', k_val=25.0, r_A_val=0.05, r_B_val=0.01)

# Panel 4: Variation 3 - Equal Depreciation (r_A=r_B=0.03)
circ_A, circ_B, tip = run_simulation(k_feedback=15.0, r_A=0.03, r_B=0.03)
plot_panel(axes[1, 1], circ_A, circ_B, tip,
           'VARIATION 3: Equal Depreciation', k_val=15.0, r_A_val=0.03, r_B_val=0.03)

plt.suptitle("Gresham's Law: How Feedback Strength and Depreciation Difference Control Tipping",
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout(rect=[0, 0, 1, 0.99])

plt.savefig(Path(__file__).parent / 'chart_varied.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart_varied.png', dpi=150, bbox_inches='tight')
plt.close()
print("Variations chart saved to chart_varied.pdf and chart_varied.png")
