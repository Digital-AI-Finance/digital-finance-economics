"""Payment Methods Evolution Timeline - From commodity money to digital currencies"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

# Timeline data
eras = [
    ('3000 BC', 'Commodity\nMoney', 'Grain, cattle,\nprecious metals'),
    ('600 BC', 'Coinage', 'Standardized\nmetal coins'),
    ('1000 AD', 'Paper Money', 'Banknotes,\nbills of exchange'),
    ('1950s', 'Credit Cards', 'Payment cards,\nelectronic auth'),
    ('1990s', 'Online\nBanking', 'Internet payments,\ne-commerce'),
    ('2009', 'Crypto-\ncurrencies', 'Bitcoin,\ndecentralized'),
    ('2020s', 'CBDCs', 'Central bank\ndigital money'),
]

# Create timeline
y_base = 0.5
x_positions = np.linspace(0.08, 0.92, len(eras))

# Draw timeline arrow
ax.annotate('', xy=(0.98, y_base), xytext=(0.02, y_base),
            arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=3))

# Colors for different eras
colors = [MLORANGE, MLORANGE, MLBLUE, MLBLUE, MLGREEN, MLRED, MLPURPLE]

for i, (year, name, desc) in enumerate(eras):
    x = x_positions[i]
    color = colors[i]

    # Circle marker
    circle = plt.Circle((x, y_base), 0.025, color=color, zorder=5)
    ax.add_patch(circle)

    # Year label below
    ax.text(x, y_base - 0.12, year, ha='center', va='top', fontsize=11,
            fontweight='bold', color='black')

    # Era name above
    ax.text(x, y_base + 0.08, name, ha='center', va='bottom', fontsize=12,
            fontweight='bold', color=color)

    # Description further above
    ax.text(x, y_base + 0.28, desc, ha='center', va='bottom', fontsize=10,
            color='gray', style='italic')

# Add economic concepts annotations
ax.annotate('Physical\nExchange', xy=(0.15, 0.15), fontsize=10, ha='center',
            color=MLORANGE, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax.annotate('Intermediated\nPayments', xy=(0.50, 0.15), fontsize=10, ha='center',
            color=MLBLUE, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

ax.annotate('Digital\nTransformation', xy=(0.85, 0.15), fontsize=10, ha='center',
            color=MLPURPLE, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=MLLAVENDER, alpha=0.5))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('Evolution of Payment Methods', fontsize=16, fontweight='bold',
             color=MLPURPLE, pad=20)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
