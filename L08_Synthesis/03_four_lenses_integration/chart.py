"""Digital Finance Phenomena x Economic Lenses"""
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
phenomena = ['Bitcoin', 'Stablecoins', 'CBDCs', 'DeFi/AMMs',
             'Payment\nPlatforms', 'Tokenized\nAssets']
lenses = ['Monetary', 'Platform', 'Microstructure', 'Regulatory']

scores = np.array([
    [9, 3, 7, 8],   # Bitcoin
    [8, 5, 6, 9],   # Stablecoins
    [10, 4, 3, 10], # CBDCs
    [3, 8, 10, 6],  # DeFi/AMMs
    [2, 9, 4, 7],   # Payment Platforms
    [5, 6, 8, 7]    # Tokenized Assets
])

# Visualization
fig, ax = plt.subplots(figsize=(10, 7))

im = ax.imshow(scores, cmap='YlOrRd', aspect='auto', vmin=0, vmax=10)

# Set ticks and labels
ax.set_xticks(np.arange(len(lenses)))
ax.set_yticks(np.arange(len(phenomena)))
ax.set_xticklabels(lenses)
ax.set_yticklabels(phenomena)

# Rotate x labels
plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

# Annotate cells
for i in range(len(phenomena)):
    for j in range(len(lenses)):
        text = ax.text(j, i, scores[i, j],
                      ha='center', va='center', color='black', fontweight='bold')

# Colorbar
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Relevance Score', rotation=270, labelpad=20)

ax.set_title('Four Lenses Integration Map', pad=20, fontweight='bold')
ax.set_xlabel('Economic Lenses')
ax.set_ylabel('Digital Finance Phenomena')

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
