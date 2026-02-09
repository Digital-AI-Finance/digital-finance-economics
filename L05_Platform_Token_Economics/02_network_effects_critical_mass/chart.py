"""Network Effects: Critical Mass and Multiple Equilibria

Based on: Katz & Shapiro (1985) - Network Externalities

Economic Model:
  Agent utility: $U_i = \\theta_i \\cdot x - c$ where $\\theta_i \\sim U(0,1)$
  Equilibrium: $x^* = \\max(0, 1 - c/x^*)$
  Fixed-point equation: $x^2 - x + c = 0$
  Discriminant: $\\Delta = 1 - 4c$ (multiple equilibria when $c < 0.25$)
  Stability: $f'(x^*) = c/{x^*}^2 < 1$ for stable equilibrium

Citation: Katz & Shapiro (1985) - Network Externalities, Competition, and Compatibility
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

# Agent utility: U_i = theta_i * x - c
# theta_i ~ Uniform(0,1), x = fraction adopting
# Equilibrium: x* = P(theta > c/x*) = max(0, 1 - c/x*)

c_values = np.linspace(0.001, 0.5, 500)
critical_c = 0.25

# Compute the three branches separately
# Branch 1: x=0 stable equilibrium (exists for all c > 0)
zero_branch_c = c_values.copy()
zero_branch_x = np.zeros_like(zero_branch_c)

# For c < 0.25, two additional equilibria exist from x^2 - x + c = 0
mask_multi = c_values < critical_c

# Branch 2: Upper stable equilibrium x = (1 + sqrt(1-4c))/2
upper_c = c_values[mask_multi]
upper_x = (1 + np.sqrt(1 - 4 * upper_c)) / 2

# Branch 3: Lower unstable equilibrium x = (1 - sqrt(1-4c))/2
lower_c = c_values[mask_multi]
lower_x = (1 - np.sqrt(1 - 4 * lower_c)) / 2

# Plot bifurcation diagram
fig, ax = plt.subplots()

# Plot x=0 branch (stable) -- separate line
ax.plot(zero_branch_c, zero_branch_x, linewidth=2.5, color=MLPURPLE,
        label='Stable: $x^*=0$ (no adoption)')

# Plot upper stable branch -- separate line
ax.plot(upper_c, upper_x, linewidth=2.5, color=MLBLUE,
        label='Stable: $x^* = (1+\\sqrt{1-4c})/2$')

# Plot unstable branch
ax.plot(lower_c, lower_x, linewidth=2.5, linestyle='--', color=MLRED,
        label='Unstable: $x^* = (1-\\sqrt{1-4c})/2$')

# Mark critical mass threshold
ax.axvline(critical_c, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
ax.text(critical_c + 0.008, 0.62,
        'Critical Mass\nThreshold\n(Beyond $c=0.25$:\nno positive\nequilibrium exists)',
        fontsize=10, color='gray',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.7))

# Mark the bifurcation point
ax.plot(critical_c, 0.5, 'o', markersize=10, color=MLRED, markeredgecolor='darkred',
        markeredgewidth=2, zorder=5)
ax.annotate('Saddle-node\nbifurcation\n$(c=0.25, x^*=0.5)$',
            xy=(critical_c, 0.5), xytext=(critical_c - 0.08, 0.7),
            fontsize=9, fontweight='bold', color='darkred',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor=MLRED, edgecolor='darkred', alpha=0.2))

ax.set_xlabel('Adoption Cost $c$ (normalized, 0--1)')
ax.set_ylabel('Equilibrium Adoption Rate $x^*$ (fraction, 0--1)')
ax.set_title('Critical Mass: Multiple Equilibria in Platform Adoption')

# Reading guide -- accurate for bifurcation diagram
ax.text(0.02, 0.55,
        'Reading this diagram:\n'
        '- For a given cost (x-axis), read vertically\n'
        '  to find equilibria\n'
        '- Solid line: where platform settles\n'
        '- Dashed line: tipping point\n'
        '- Below tipping point: collapse to zero',
        transform=ax.transAxes, fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

# Model equation annotation (replaces Metcalfe tangent)
ax.text(0.02, 0.98, r"$x^2 - x + c = 0$" + "\n" + r"$\Delta = 1 - 4c$",
        transform=ax.transAxes, fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.legend(loc='upper right', fontsize=11)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(0, 0.5)
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
