"""Quantity Theory of Money: Digital vs Fiat Velocity

Visualizes the Fisher equation MV=PY with different velocity regimes.
Shows how digital currencies with higher velocity affect price levels.

Citation: Fisher (1911) - The Purchasing Power of Money
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

# Parameters
Y = 100  # Fixed real output
V_fiat = 1.5
V_digital = 10

# Money supply range
M = np.linspace(10, 200, 100)

# Calculate price levels using MV = PY => P = MV/Y
P_fiat = M * V_fiat / Y
P_digital = M * V_digital / Y

# Find equilibrium points where P = 1
M_eq_fiat = Y / V_fiat  # M = PY/V when P=1
M_eq_digital = Y / V_digital

# Create plot
fig, ax = plt.subplots()

# Plot lines
ax.plot(M, P_fiat, color=MLBLUE, linewidth=2.5, label='Fiat Money (V=1.5)')
ax.plot(M, P_digital, color=MLORANGE, linewidth=2.5, label='Digital Currency (V=10)')

# Shade area between curves
ax.fill_between(M, P_fiat, P_digital, alpha=0.15, color=MLLAVENDER)

# Mark equilibrium points
ax.plot(M_eq_fiat, 1, 'o', color=MLBLUE, markersize=10, zorder=5)
ax.plot(M_eq_digital, 1, 'o', color=MLORANGE, markersize=10, zorder=5)

# Add annotations
ax.annotate('Fiat velocity V=1.5\n(slower circulation)',
            xy=(M_eq_fiat, 1), xytext=(90, 0.8),
            arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.5),
            fontsize=12, color=MLBLUE, ha='center')

ax.annotate('Digital velocity V=10\n(faster circulation)',
            xy=(M_eq_digital, 1), xytext=(30, 8),
            arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=1.5),
            fontsize=12, color=MLORANGE, ha='center')

# Add horizontal line at P=1
ax.axhline(y=1, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Baseline P=1')

# Labels and title
ax.set_xlabel('Money Supply (M)', fontweight='bold')
ax.set_ylabel('Price Level (P)', fontweight='bold')
ax.set_title('Quantity Theory of Money: MV = PY', fontweight='bold', pad=15)
ax.legend(loc='upper left', framealpha=0.95)
ax.grid(True, alpha=0.3, linestyle='--')

# Set reasonable y-axis limits
ax.set_ylim(0, max(P_digital.max(), 20))

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
