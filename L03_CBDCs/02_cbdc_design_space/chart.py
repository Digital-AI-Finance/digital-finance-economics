"""CBDC Design Space - 2x2 Matrix of design choices"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
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

fig, ax = plt.subplots(figsize=(10, 6))

# 2x2 matrix positions
quadrants = [
    # (x, y, title, description, examples, color)
    (0.25, 0.72, 'RETAIL + TOKEN',
     'Anonymous, cash-like\nP2P transfers\nOffline capable',
     'e-CNY (partial)', MLGREEN),
    (0.75, 0.72, 'RETAIL + ACCOUNT',
     'Identity-linked\nProgrammable\nInterest-bearing possible',
     'Digital Euro (proposed)', MLBLUE),
    (0.25, 0.28, 'WHOLESALE + TOKEN',
     'Interbank settlement\nSecurities trading\nCross-border',
     'Project Jasper, Ubin', MLORANGE),
    (0.75, 0.28, 'WHOLESALE + ACCOUNT',
     'Reserve accounts\nCentral bank operated\nLimited access',
     'Traditional RTGS', MLPURPLE),
]

# Draw quadrants
for x, y, title, desc, example, color in quadrants:
    box = FancyBboxPatch((x - 0.22, y - 0.18), 0.44, 0.36,
                         boxstyle="round,pad=0.02,rounding_size=0.02",
                         facecolor=color, alpha=0.15, edgecolor=color, linewidth=2)
    ax.add_patch(box)

    ax.text(x, y + 0.12, title, ha='center', va='center', fontsize=12,
            fontweight='bold', color=color)
    ax.text(x, y - 0.02, desc, ha='center', va='center', fontsize=10,
            color='black')
    ax.text(x, y - 0.14, f'Ex: {example}', ha='center', va='center', fontsize=9,
            color='gray', style='italic')

# Axes labels
ax.annotate('', xy=(0.98, 0.5), xytext=(0.02, 0.5),
            arrowprops=dict(arrowstyle='->', color='gray', lw=2))
ax.text(0.5, 0.52, 'Token-based                                    Account-based',
        ha='center', va='bottom', fontsize=11, color='gray')

ax.annotate('', xy=(0.5, 0.95), xytext=(0.5, 0.05),
            arrowprops=dict(arrowstyle='->', color='gray', lw=2))
ax.text(0.52, 0.15, 'Wholesale', ha='left', va='center', fontsize=11, color='gray', rotation=90)
ax.text(0.52, 0.85, 'Retail', ha='left', va='center', fontsize=11, color='gray', rotation=90)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('CBDC Design Space: Key Trade-offs', fontsize=16,
             fontweight='bold', color=MLPURPLE, pad=10)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
