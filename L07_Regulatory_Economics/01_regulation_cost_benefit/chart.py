"""Optimal Regulation: Marginal Cost vs Marginal Benefit"""
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

# Generate regulation intensity values
r = np.linspace(0.01, 1, 200)

# Marginal cost and benefit functions
MC = 2 * r**2
MB = 1.5 * np.exp(-2*r)

# Find optimal regulation level where MC = MB
r_star_idx = np.argmin(np.abs(MC - MB))
r_star = r[r_star_idx]

# Create plot
fig, ax = plt.subplots()

# Plot MC and MB curves
ax.plot(r, MC, color=MLRED, linewidth=2.5, label='Marginal Cost (MC)')
ax.plot(r, MB, color=MLGREEN, linewidth=2.5, label='Marginal Benefit (MB)')

# Fill areas for net benefit and deadweight loss
# Net benefit (green) where MB > MC (before optimal point)
ax.fill_between(r[:r_star_idx], MC[:r_star_idx], MB[:r_star_idx],
                alpha=0.3, color=MLGREEN, label='Net Benefit')

# Deadweight loss (red) where MC > MB (after optimal point)
ax.fill_between(r[r_star_idx:], MB[r_star_idx:], MC[r_star_idx:],
                alpha=0.3, color=MLRED, label='Deadweight Loss')

# Vertical line at optimal point
ax.axvline(r_star, color='black', linestyle='--', linewidth=1.5, alpha=0.7)

# Annotations
ax.annotate(f'Optimal r* = {r_star:.2f}',
            xy=(r_star, MC[r_star_idx]),
            xytext=(r_star + 0.15, MC[r_star_idx] + 0.3),
            fontsize=12,
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

ax.set_xlabel('Regulation Intensity (r)')
ax.set_ylabel('Cost / Benefit')
ax.set_title('Optimal Regulation: Marginal Cost vs Marginal Benefit')
ax.legend(loc='best')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1)
ax.set_ylim(0, max(MB.max(), MC.max()) * 1.1)

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
