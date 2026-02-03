"""Four Economic Lenses Framework - Radar chart showing digital finance phenomena scores

Multidimensional assessment of digital finance phenomena across four economic perspectives:
monetary economics, platform economics, market microstructure, and regulatory economics.

Citation: Course Framework - Osterrieder & Lorenz (2024) - Digital Finance Economics
"""
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
ax.set_xlabel('Economic Lenses (category)', size=11, labelpad=30)

# Set y-axis limits and labels (B6: Add unit indicator "score")
ax.set_ylim(0, 11)
ax.set_yticks([2, 4, 6, 8, 10])
ax.set_yticklabels(['2', '4', '6', '8', '10 (score)'], size=11)
ax.set_ylabel('Relevance Score (0-10)', size=13, labelpad=20)
ax.grid(True, linestyle='--', alpha=0.6)

# B5: Add annotation highlighting CBDCs' strong regulatory score
cbdc_values = phenomena['CBDCs']
max_idx = np.argmax(cbdc_values)
max_angle = angles[max_idx]
max_value = cbdc_values[max_idx]
ax.annotate(f'CBDC Peak:\n{max_value:.1f}', xy=(max_angle, max_value),
           xytext=(max_angle + 0.5, max_value + 1),
           fontsize=10, fontweight='bold', color=MLORANGE,
           arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=1.5),
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLORANGE, alpha=0.8))

# Add title and legend
ax.set_title('Four Economic Lenses: Digital Finance Phenomena',
             size=16, weight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), frameon=True,
          fancybox=True, shadow=True)

# C3: Add theory explanation annotation
theory_text = ('Four Analytical Dimensions:\n'
               '1. Monetary: Money properties, velocity, stability\n'
               '2. Platform: Network effects, competition\n'
               '3. Microstructure: Trading, liquidity, price formation\n'
               '4. Regulatory: Policy design, compliance, supervision')
ax.text(0.5, -0.15, theory_text, transform=ax.transAxes,
        fontsize=9, ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=MLLAVENDER, edgecolor=MLPURPLE, alpha=0.7))

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
