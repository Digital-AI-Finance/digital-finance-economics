"""Stablecoin Market Share Evolution - Growth and composition"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

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

fig, ax = plt.subplots(figsize=(10, 6))

# Quarterly data from 2019 to 2024
quarters = ['Q1\n2019', 'Q3\n2019', 'Q1\n2020', 'Q3\n2020', 'Q1\n2021', 'Q3\n2021',
            'Q1\n2022', 'Q3\n2022', 'Q1\n2023', 'Q3\n2023', 'Q1\n2024']

# Market cap in billions USD (simulated but realistic)
tether = np.array([2, 4, 5, 16, 35, 68, 83, 68, 70, 84, 95])
usdc = np.array([0.3, 0.5, 1, 3, 10, 30, 55, 45, 32, 25, 30])
dai = np.array([0.1, 0.3, 0.2, 1, 3, 7, 10, 6, 5, 5, 5])
others = np.array([0.5, 0.7, 1, 2, 5, 15, 20, 12, 8, 10, 15])

x = np.arange(len(quarters))

# Stacked area chart
ax.fill_between(x, 0, tether, alpha=0.8, color=MLGREEN, label='USDT (Tether)')
ax.fill_between(x, tether, tether + usdc, alpha=0.8, color=MLBLUE, label='USDC (Circle)')
ax.fill_between(x, tether + usdc, tether + usdc + dai, alpha=0.8, color=MLORANGE, label='DAI (MakerDAO)')
ax.fill_between(x, tether + usdc + dai, tether + usdc + dai + others, alpha=0.8, color=MLLAVENDER, label='Others')

# Add total line
total = tether + usdc + dai + others
ax.plot(x, total, 'k-', linewidth=2, label='Total Market Cap')

# Annotation for Terra collapse
ax.annotate('Terra/UST\ncollapse', xy=(6.3, 140), xytext=(7.5, 155),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_xlabel('Quarter', fontweight='bold')
ax.set_ylabel('Market Cap (Billion USD)', fontweight='bold')
ax.set_title('Stablecoin Market Evolution', fontsize=16, fontweight='bold', color=MLPURPLE)

ax.set_xticks(x)
ax.set_xticklabels(quarters)
ax.legend(loc='upper left', framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y')
ax.set_xlim(-0.5, len(quarters) - 0.5)
ax.set_ylim(0, 180)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
