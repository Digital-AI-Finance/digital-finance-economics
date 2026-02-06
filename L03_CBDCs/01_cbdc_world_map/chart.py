r"""CBDC Project Status Worldwide - Country-level implementation status

Global survey of central bank digital currency development stages across countries,
showing launched, pilot, development, research, and inactive projects.

Economic Model: $CBDC_{status} \in \{Research, Pilot, Launched\}$
Adoption stages framework showing country-level implementation progress.

Citation: Atlantic Council (2024) - CBDC Tracker; BIS (2021) - CBDCs: an opportunity for the monetary system
"""
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

fig, ax = plt.subplots(figsize=(10, 6))

# CBDC status data (simplified horizontal bar chart representation)
categories = ['Launched', 'Pilot', 'Development', 'Research', 'Inactive']
counts = [11, 21, 33, 68, 14]
colors = [MLGREEN, MLBLUE, MLORANGE, MLPURPLE, 'gray']

# Example countries for each category
examples = [
    'Bahamas, Jamaica, Nigeria',
    'China, India, Russia, Brazil',
    'EU (Digital Euro), UK, Australia',
    'USA, Japan, Canada, Switzerland',
    '(Various cancelled projects)'
]

y_pos = np.arange(len(categories))
bars = ax.barh(y_pos, counts, color=colors, alpha=0.8, height=0.6)

# Add count labels
for i, (bar, count, example) in enumerate(zip(bars, counts, examples)):
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
            f'{count} countries', va='center', fontsize=12, fontweight='bold')
    ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2 - 0.25,
            f'({example})', va='center', fontsize=9, color='gray', style='italic')

ax.set_yticks(y_pos)
ax.set_yticklabels(categories)
ax.set_xlabel('Number of Countries (count)', fontweight='bold')
ax.set_ylabel('Development Stage (category)', fontweight='bold')
ax.set_title('Global CBDC Development Status (2024)', fontsize=16,
             fontweight='bold', color=MLPURPLE)

ax.set_xlim(0, 100)
ax.grid(True, alpha=0.3, axis='x')

# B5: Add annotation highlighting pilot stage momentum
pilot_idx = categories.index('Pilot')
pilot_count = counts[pilot_idx]
ax.annotate('Pilot:\nKey momentum',
           xy=(pilot_count, pilot_idx), xytext=(pilot_count + 15, pilot_idx + 0.5),
           fontsize=10, fontweight='bold', color=MLBLUE,
           arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.5),
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLBLUE, alpha=0.8))

# Add note
ax.text(50, -0.8, 'Source: Atlantic Council CBDC Tracker (2024)',
        fontsize=9, ha='center', color='gray', style='italic')

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
