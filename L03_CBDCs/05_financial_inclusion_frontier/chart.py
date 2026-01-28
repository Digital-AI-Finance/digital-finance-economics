"""Financial Inclusion Possibility Frontier - CBDC frontier shift"""
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

# Pre-CBDC frontier (smaller quarter circle)
theta_pre = np.linspace(0, np.pi/2, 100)
x_pre = np.cos(theta_pre) * 0.8
y_pre = np.sin(theta_pre) * 0.8

# Post-CBDC frontier (larger quarter circle)
theta_post = np.linspace(0, np.pi/2, 100)
x_post = np.cos(theta_post) * 1.0
y_post = np.sin(theta_post) * 1.0

# Country positions (inside pre-CBDC frontier)
countries = {
    'Sweden': (0.55, 0.60),
    'USA': (0.70, 0.50),
    'Kenya': (0.68, 0.35),
    'Singapore': (0.60, 0.55),
    'Nigeria': (0.50, 0.45),
    'India': (0.58, 0.40),
    'Brazil': (0.48, 0.52),
    'Germany': (0.52, 0.58)
}

# Plot
fig, ax = plt.subplots()

# Plot frontiers
ax.plot(x_pre, y_pre, '--', color=MLBLUE, linewidth=2.5,
        label='Pre-CBDC Frontier', alpha=0.8)
ax.plot(x_post, y_post, '-', color=MLPURPLE, linewidth=3,
        label='Post-CBDC Frontier')

# Fill area between frontiers
ax.fill_between(x_post, y_post, 0, alpha=0.1, color=MLLAVENDER)

# Plot country points
for country, (x, y) in countries.items():
    ax.scatter(x, y, s=100, color=MLORANGE, edgecolors='black',
              linewidths=1.5, zorder=5, alpha=0.8)

    # Offset labels to avoid overlap
    offset_x = 0.03 if country not in ['Sweden', 'Germany'] else -0.08
    offset_y = 0.03 if country not in ['USA', 'Kenya'] else -0.03

    ax.annotate(country, xy=(x, y), xytext=(x + offset_x, y + offset_y),
               fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                        edgecolor='gray', alpha=0.9))

# Arrow showing frontier shift
arrow_x = 0.55
arrow_y = 0.55
arrow_dx = 0.12
arrow_dy = 0.12
ax.annotate('', xy=(arrow_x + arrow_dx, arrow_y + arrow_dy),
           xytext=(arrow_x, arrow_y),
           arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=3.5,
                          mutation_scale=25))
ax.text(arrow_x + arrow_dx/2 + 0.05, arrow_y + arrow_dy/2,
       'CBDC\nExpansion', fontsize=13, fontweight='bold',
       color=MLGREEN, ha='left',
       bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                edgecolor=MLGREEN, alpha=0.9))

# Formatting
ax.set_xlabel('Financial Inclusion (Reach)', fontweight='bold')
ax.set_ylabel('Financial Stability (Oversight)', fontweight='bold')
ax.set_title('Financial Inclusion-Stability Frontier', fontweight='bold', pad=20)
ax.set_xlim(0, 1.1)
ax.set_ylim(0, 1.1)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='lower left', framealpha=0.95, fontsize=12)

# Set aspect ratio to be equal for proper circle shape
ax.set_aspect('equal', adjustable='box')

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
