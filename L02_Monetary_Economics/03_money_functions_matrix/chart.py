r"""Money Functions Assessment Matrix - Comparing crypto vs fiat

Based on: Menger (1892) - On the origin of money, classical functions of money

Economic Model:
    Without money, direct barter requires a double coincidence of wants.
    With $n$ goods, the number of required barter exchange pairs is:
    $\text{Barter pairs} = \frac{n(n-1)}{2}$

    Money reduces this to $n$ exchange rates (one per good priced in money).
    The three classical functions -- medium of exchange, unit of account,
    store of value -- each reduce distinct transaction costs.
"""
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

fig, ax = plt.subplots(figsize=(10, 6))

# Categories
functions = ['Medium of\nExchange', 'Unit of\nAccount', 'Store of\nValue']
assets = ['USD (Fiat)', 'Bitcoin', 'USDT (Stablecoin)', 'CBDC (proposed)']

# Scores (0-10) - Illustrative assessment, not empirical measurement
scores = np.array([
    [9, 9, 8],   # USD
    [4, 2, 5],   # Bitcoin
    [7, 6, 6],   # USDT
    [8, 8, 7],   # CBDC (proposed, not yet proven at scale)
])

# Colors for each asset
colors = [MLGREEN, MLORANGE, MLBLUE, MLPURPLE]

x = np.arange(len(functions))
width = 0.2

# Create grouped bars
for i, (asset, color) in enumerate(zip(assets, colors)):
    offset = (i - 1.5) * width
    bars = ax.bar(x + offset, scores[i], width, label=asset, color=color, alpha=0.8)
    # Add value labels
    for bar, score in zip(bars, scores[i]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                str(score), ha='center', va='bottom', fontsize=10, fontweight='bold')

# Reference lines
ax.axhline(y=7, color='gray', linestyle='--', alpha=0.5)
ax.text(2.6, 7.2, 'Good threshold', fontsize=9, color='gray')

# Add annotation about money functions
ax.text(0.02, 0.98,
        'Three Functions of Money:\n'
        '• Medium of Exchange: Facilitates transactions\n'
        '• Unit of Account: Measuring value\n'
        '• Store of Value: Preserving purchasing power\n\n'
        'Good money scores ≥7 on all dimensions',
        transform=ax.transAxes, fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

ax.set_xlabel('Money Function', fontweight='bold')
ax.set_ylabel('Score (0-10)', fontweight='bold')
ax.set_title('Money Functions Assessment: Crypto vs Fiat', fontsize=16,
             fontweight='bold', color=MLPURPLE)

ax.set_xticks(x)
ax.set_xticklabels(functions)
ax.legend(loc='upper right', framealpha=0.9, ncol=2)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 11)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
