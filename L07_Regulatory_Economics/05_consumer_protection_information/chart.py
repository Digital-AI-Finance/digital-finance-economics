"""Adverse Selection in Token Markets (Akerlof's Lemons)"""
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

# Initialize 1000 projects with random quality
n_projects = 1000
quality = np.random.uniform(0, 1, n_projects)
periods = 50

# Simulate no regulation scenario (adverse selection)
market_size_no_reg = []
avg_quality_no_reg = []
remaining_quality = quality.copy()

for t in range(periods):
    if len(remaining_quality) == 0:
        market_size_no_reg.append(0)
        avg_quality_no_reg.append(0)
        continue

    # Buyer price = mean quality of remaining projects
    price = remaining_quality.mean()

    # Projects with quality > price exit (good projects leave)
    remaining_quality = remaining_quality[remaining_quality <= price]

    market_size_no_reg.append(len(remaining_quality))
    avg_quality_no_reg.append(remaining_quality.mean() if len(remaining_quality) > 0 else 0)

# With regulation: all projects stay, buyers see true quality
market_size_with_reg = [n_projects] * periods
avg_quality_with_reg = [quality.mean()] * periods

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Top plot: Market size over time
time = np.arange(1, periods + 1)
ax1.plot(time, market_size_no_reg, color=MLRED, linewidth=2.5, label='No Regulation')
ax1.plot(time, market_size_with_reg, color=MLGREEN, linewidth=2.5, linestyle='--', label='With Disclosure')

ax1.set_ylabel('Number of Projects in Market')
ax1.set_title('Market Size Over Time')
ax1.legend(loc='best')
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, n_projects * 1.1)

# Bottom plot: Average quality over time
ax2.plot(time, avg_quality_no_reg, color=MLRED, linewidth=2.5, label='No Regulation')
ax2.plot(time, avg_quality_with_reg, color=MLGREEN, linewidth=2.5, linestyle='--', label='With Disclosure')

ax2.set_xlabel('Period')
ax2.set_ylabel('Average Project Quality')
ax2.set_title('Average Quality Over Time')
ax2.legend(loc='best')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 1.1)
ax2.set_xlim(1, periods)

# Overall title
fig.suptitle('Adverse Selection: Mandatory Disclosure vs No Regulation',
             fontsize=16, fontweight='bold', y=0.995)

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
