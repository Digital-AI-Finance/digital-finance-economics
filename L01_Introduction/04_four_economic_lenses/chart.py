"""Four Economic Lenses Framework - Radar chart showing digital finance phenomena scores"""
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

# Define categories (lenses)
categories = ['Monetary\nEconomics', 'Platform\nEconomics',
              'Market\nMicrostructure', 'Regulatory\nEconomics']
N = len(categories)

# Define phenomena and their scores across the four lenses
phenomena = {
    'Bitcoin': np.array([9, 3, 7, 8]) + np.random.uniform(-0.3, 0.3, 4),
    'Stablecoins': np.array([8, 5, 6, 9]) + np.random.uniform(-0.3, 0.3, 4),
    'CBDCs': np.array([10, 4, 3, 10]) + np.random.uniform(-0.3, 0.3, 4),
    'DeFi/AMMs': np.array([3, 8, 10, 6]) + np.random.uniform(-0.3, 0.3, 4),
    'Neobanks': np.array([2, 9, 4, 7]) + np.random.uniform(-0.3, 0.3, 4)
}

colors = [MLPURPLE, MLBLUE, MLORANGE, MLGREEN, MLRED]

# Compute angle for each axis
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]  # Complete the circle

# Create radar chart
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

# Plot each phenomenon
for (name, values), color in zip(phenomena.items(), colors):
    values_plot = values.tolist()
    values_plot += values_plot[:1]  # Complete the circle
    ax.plot(angles, values_plot, 'o-', linewidth=2, label=name, color=color)
    ax.fill(angles, values_plot, alpha=0.15, color=color)

# Set category labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=13)

# Set y-axis limits and labels
ax.set_ylim(0, 11)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(['2', '4', '6', '8', '10'], size=11)
ax.grid(True, linestyle='--', alpha=0.6)

# Add title and legend
ax.set_title('Four Economic Lenses: Digital Finance Phenomena',
             size=16, weight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=True,
          fancybox=True, shadow=True)

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
