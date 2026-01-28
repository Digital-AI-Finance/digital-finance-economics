"""Policy Tool Effectiveness Matrix"""
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

# Data
tools = ['Capital Req', 'Licensing', 'Disclosure', 'Sandbox',
         'CBDC', 'Stablecoin Reg', 'DeFi Reg', 'Cross-border']
objectives = ['Stability', 'Inclusion', 'Innovation', 'Consumer\nProtection', 'AML']

scores = np.array([
    [2, -1, -1, 1, 1],    # Capital Req
    [1, -1, -2, 1, 1],    # Licensing
    [1, 0, 0, 2, 1],      # Disclosure
    [-1, 1, 2, 0, -1],    # Sandbox
    [1, 2, 0, 1, 1],      # CBDC
    [2, 0, -1, 2, 2],     # Stablecoin Reg
    [1, 0, -1, 1, 1],     # DeFi Reg
    [1, 1, 1, 1, 2]       # Cross-border
])

# Visualization
fig, ax = plt.subplots(figsize=(10, 8))

im = ax.imshow(scores, cmap='RdYlBu', aspect='auto', vmin=-2, vmax=2)

# Set ticks and labels
ax.set_xticks(np.arange(len(objectives)))
ax.set_yticks(np.arange(len(tools)))
ax.set_xticklabels(objectives)
ax.set_yticklabels(tools)

# Rotate x labels
plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

# Annotate cells
for i in range(len(tools)):
    for j in range(len(objectives)):
        score = scores[i, j]
        # Format with + for positive values
        text_str = f'{score:+d}' if score != 0 else '0'
        color = 'white' if abs(score) > 1 else 'black'
        text = ax.text(j, i, text_str,
                      ha='center', va='center', color=color, fontweight='bold',
                      fontsize=12)

# Colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Effectiveness Score\n(-2: Harmful, +2: Highly Effective)',
               rotation=270, labelpad=30)
cbar.set_ticks([-2, -1, 0, 1, 2])
cbar.set_ticklabels(['-2', '-1', '0', '+1', '+2'])

ax.set_title('Policy Effectiveness Matrix', pad=20, fontweight='bold')
ax.set_xlabel('Policy Objectives')
ax.set_ylabel('Policy Tools')

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
