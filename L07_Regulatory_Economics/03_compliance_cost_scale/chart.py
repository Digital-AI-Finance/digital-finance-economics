"""Compliance Cost Burden by Firm Size"""
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

# Generate firm revenue values (log-spaced)
revenue = np.logspace(6, 10, 200)

# Average compliance cost as percentage of revenue
avg_cost_pct = (5e6 / revenue + 0.001) * 100

# Find crossing point with 2% threshold
threshold = 2.0
crossing_idx = np.argmin(np.abs(avg_cost_pct - threshold))
crossing_revenue = revenue[crossing_idx]

# Calculate excluded fraction (firms below threshold)
excluded_fraction = crossing_idx / len(revenue)

# Create log-log plot
fig, ax = plt.subplots()

ax.loglog(revenue, avg_cost_pct, color=MLPURPLE, linewidth=2.5, label='Compliance Cost (%)')
ax.axhline(threshold, color=MLRED, linestyle='--', linewidth=2, label='2% Threshold')

# Mark crossing point
ax.plot(crossing_revenue, threshold, 'o', color='black', markersize=10, zorder=5)

# Annotate crossing point and excluded fraction
ax.annotate(f'Crossing: ${crossing_revenue/1e6:.1f}M\n{excluded_fraction*100:.0f}% firms excluded',
            xy=(crossing_revenue, threshold),
            xytext=(crossing_revenue * 0.3, threshold * 3),
            fontsize=12,
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

ax.set_xlabel('Firm Revenue ($)')
ax.set_ylabel('Compliance Cost (% of Revenue)')
ax.set_title('Compliance Cost vs Firm Size: Scale Economies')
ax.legend(loc='best')
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim(revenue.min(), revenue.max())

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
