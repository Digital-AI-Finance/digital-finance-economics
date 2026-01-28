"""Correspondent Banking Network - Hub and spoke visualization"""
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

fig, ax = plt.subplots(figsize=(10, 6))

# Hub banks (large)
hubs = [
    (0.3, 0.7, 'JPMorgan\n(USD)'),
    (0.7, 0.7, 'Deutsche Bank\n(EUR)'),
    (0.5, 0.3, 'HSBC\n(Multi)'),
]

# Spoke banks (smaller)
spokes = [
    (0.1, 0.5, 'Bank A'),
    (0.15, 0.85, 'Bank B'),
    (0.4, 0.9, 'Bank C'),
    (0.9, 0.6, 'Bank D'),
    (0.85, 0.85, 'Bank E'),
    (0.3, 0.15, 'Bank F'),
    (0.7, 0.15, 'Bank G'),
    (0.9, 0.3, 'Bank H'),
]

# Draw spoke banks
for x, y, name in spokes:
    circle = plt.Circle((x, y), 0.04, color=MLBLUE, alpha=0.6)
    ax.add_patch(circle)
    ax.text(x, y - 0.07, name, ha='center', va='top', fontsize=9, color='gray')

# Draw hub banks
for x, y, name in hubs:
    circle = plt.Circle((x, y), 0.08, color=MLPURPLE, alpha=0.8)
    ax.add_patch(circle)
    ax.text(x, y, name, ha='center', va='center', fontsize=10,
            fontweight='bold', color='white')

# Draw connections (spoke to hub)
connections = [
    # Bank A to JPMorgan
    ((0.1, 0.5), (0.3, 0.7)),
    ((0.15, 0.85), (0.3, 0.7)),
    ((0.4, 0.9), (0.3, 0.7)),
    # To Deutsche Bank
    ((0.9, 0.6), (0.7, 0.7)),
    ((0.85, 0.85), (0.7, 0.7)),
    # To HSBC
    ((0.3, 0.15), (0.5, 0.3)),
    ((0.7, 0.15), (0.5, 0.3)),
    ((0.9, 0.3), (0.5, 0.3)),
]

for (x1, y1), (x2, y2) in connections:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1, alpha=0.5))

# Draw inter-hub connections (thick)
hub_connections = [
    ((0.3, 0.7), (0.7, 0.7)),
    ((0.3, 0.7), (0.5, 0.3)),
    ((0.7, 0.7), (0.5, 0.3)),
]

for (x1, y1), (x2, y2) in hub_connections:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='<->', color=MLORANGE, lw=3, alpha=0.7))

# Legend
hub_patch = mpatches.Patch(color=MLPURPLE, label='Hub Banks (Correspondents)', alpha=0.8)
spoke_patch = mpatches.Patch(color=MLBLUE, label='Spoke Banks', alpha=0.6)
ax.legend(handles=[hub_patch, spoke_patch], loc='lower left', framealpha=0.9)

# Cost annotation
ax.text(0.5, 0.55, 'Each hop:\n+fees, +time,\n+FX spread',
        ha='center', va='center', fontsize=10, color=MLORANGE,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor=MLORANGE))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('Correspondent Banking: Hub-and-Spoke Network', fontsize=16,
             fontweight='bold', color=MLPURPLE, pad=10)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
