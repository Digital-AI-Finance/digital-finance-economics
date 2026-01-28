"""Global Remittance Costs by Corridor - Cost comparison"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 12, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (10, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'

fig, ax = plt.subplots(figsize=(10, 6))

# Remittance corridors and costs (World Bank data, simulated)
corridors = [
    'USA -> Mexico',
    'UAE -> India',
    'UK -> Nigeria',
    'Saudi -> Pakistan',
    'USA -> Philippines',
    'South Africa -> Zimbabwe',
    'Singapore -> Indonesia',
    'Germany -> Turkey',
    'Global Average',
    'SDG Target 2030'
]

costs = [4.2, 3.8, 9.5, 5.2, 4.8, 15.2, 6.5, 5.8, 6.2, 3.0]
colors = [MLBLUE if c <= 5 else MLORANGE if c <= 8 else MLRED for c in costs[:-1]]
colors.append(MLGREEN)  # SDG target

y_pos = np.arange(len(corridors))
bars = ax.barh(y_pos, costs, color=colors, alpha=0.8, height=0.6)

# Add cost labels
for bar, cost in zip(bars, costs):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f'{cost}%', va='center', fontsize=11, fontweight='bold')

# SDG target line
ax.axvline(x=3.0, color=MLGREEN, linestyle='--', linewidth=2, alpha=0.7)
ax.text(3.2, -0.8, 'UN SDG Target: 3%', fontsize=10, color=MLGREEN,
        fontweight='bold')

# 5% line (acceptable threshold)
ax.axvline(x=5.0, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax.text(5.2, 9.5, '5% threshold', fontsize=9, color='gray')

ax.set_yticks(y_pos)
ax.set_yticklabels(corridors)
ax.set_xlabel('Cost to Send $200 (%)', fontweight='bold')
ax.set_title('Remittance Costs by Corridor (2024)', fontsize=16,
             fontweight='bold', color=MLPURPLE)

ax.set_xlim(0, 18)
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
