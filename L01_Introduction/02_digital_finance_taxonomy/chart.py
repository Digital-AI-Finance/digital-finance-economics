r"""Digital Finance Taxonomy - Economic perspective on digital finance components

Based on: Course Framework -- Four Economic Lenses for Digital Finance

Economic Model: $T = \{Crypto, Stablecoins, CBDCs, DeFi\}$
Taxonomy framework: $\mathcal{T} = \{M, P, S, R\}$ where M=Monetary, P=Platform, S=Structure, R=Regulatory
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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

# Main categories (2x2 grid)
categories = [
    # (x, y, title, items, color)
    (0.25, 0.72, 'MONETARY\nECONOMICS', ['CBDCs', 'Stablecoins', 'Money Theory'], MLPURPLE),
    (0.75, 0.72, 'PLATFORM\nECONOMICS', ['Network Effects', 'Token Economics', 'Two-Sided Markets\n(platforms connecting buyers & sellers)'], MLBLUE),
    (0.25, 0.28, 'MARKET\nMICROSTRUCTURE', ['Liquidity', 'Price Discovery', 'AMMs (Automated Market Makers) /\nDEXs (Decentralized Exchanges)'], MLORANGE),
    (0.75, 0.28, 'REGULATORY\nECONOMICS', ['Market Failure', 'Competition Policy', 'Consumer Protection'], MLGREEN),
]

# Draw boxes and labels
for x, y, title, items, color in categories:
    # Draw main box
    box = FancyBboxPatch((x - 0.22, y - 0.18), 0.44, 0.36,
                         boxstyle="round,pad=0.02,rounding_size=0.02",
                         facecolor=color, alpha=0.15, edgecolor=color, linewidth=2)
    ax.add_patch(box)

    # Title
    ax.text(x, y + 0.12, title, ha='center', va='center', fontsize=12,
            fontweight='bold', color=color)

    # Items
    item_text = '\n'.join([f'- {item}' for item in items])
    ax.text(x, y - 0.06, item_text, ha='center', va='center', fontsize=10,
            color='black')

# Central label
center_box = FancyBboxPatch((0.35, 0.42), 0.30, 0.16,
                            boxstyle="round,pad=0.02,rounding_size=0.02",
                            facecolor='white', edgecolor=MLPURPLE, linewidth=3)
ax.add_patch(center_box)
ax.text(0.5, 0.50, 'DIGITAL\nFINANCE', ha='center', va='center', fontsize=14,
        fontweight='bold', color=MLPURPLE)

# Connecting arrows from center to each quadrant
arrow_style = dict(arrowstyle='->', color='gray', lw=1.5,
                   connectionstyle='arc3,rad=0.1')

# Draw connecting lines
for x, y, _, _, color in categories:
    ax.annotate('', xy=(x, y - 0.18), xytext=(0.5, 0.50),
                arrowprops=dict(arrowstyle='->', color=color, lw=2, alpha=0.6))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xlabel('Dimension (normalized)', fontsize=10, color='gray')
ax.set_ylabel('Dimension (normalized)', fontsize=10, color='gray')
ax.axis('off')
ax.set_title('Four Economic Lenses for Digital Finance', fontsize=16,
             fontweight='bold', color=MLPURPLE, pad=10)
ax.grid(True, alpha=0.3)

# B5: Add annotation for framework integration
ax.text(0.5, 0.05, 'Each lens provides complementary analysis',
       ha='center', fontsize=9, style='italic', color=MLPURPLE,
       bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.7))

# Add educational annotation
ax.text(0.02, 0.98,
        'Taxonomy Framework:\nEach domain applies distinct economic theory\n'
        'to analyze digital finance innovations.',
        transform=ax.transAxes, fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
