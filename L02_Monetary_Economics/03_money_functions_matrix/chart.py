"""Money Functions Assessment Matrix - Comparing crypto vs fiat"""
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

# Scores (0-10)
scores = np.array([
    [9, 9, 8],   # USD
    [4, 2, 5],   # Bitcoin
    [7, 6, 6],   # USDT
    [9, 9, 9],   # CBDC
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
