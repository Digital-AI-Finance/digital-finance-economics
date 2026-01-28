"""Financial Contagion: Network Cascade Simulation"""
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

# Network setup
N = 20
angles = 2 * np.pi * np.arange(N) / N
x = np.cos(angles)
y = np.sin(angles)

# Create adjacency matrix (symmetric, no self-loops)
adj = np.random.rand(N, N) < 0.3
adj = np.triu(adj, 1)  # Upper triangle only
adj = adj + adj.T  # Make symmetric
np.fill_diagonal(adj, 0)

# Capital buffers
buffers = np.random.uniform(0.05, 0.2, N)
original_buffers = buffers.copy()

# Degree of each node
degrees = adj.sum(axis=1)
degrees = np.maximum(degrees, 1)  # Avoid division by zero

# Contagion simulation
shock_node = 0
failed = np.zeros(N, dtype=bool)
stressed = np.zeros(N, dtype=bool)
failed[shock_node] = True

cascade_rounds = []
round_failures = [1]  # Initial shock

for round_num in range(10):
    new_failures = 0
    cumulative_losses = np.zeros(N)

    # Failed nodes spread losses to neighbors
    for i in range(N):
        if failed[i]:
            neighbors = np.where(adj[i])[0]
            loss_per_neighbor = original_buffers[i] / degrees[i]
            for j in neighbors:
                if not failed[j]:
                    cumulative_losses[j] += loss_per_neighbor

    # Check for new failures
    for i in range(N):
        if not failed[i]:
            if cumulative_losses[i] > buffers[i]:
                failed[i] = True
                new_failures += 1
            elif cumulative_losses[i] > 0.5 * buffers[i]:
                stressed[i] = True

    round_failures.append(new_failures)
    if new_failures == 0:
        break

# Visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left panel: Network visualization
for i in range(N):
    for j in range(i+1, N):
        if adj[i, j]:
            ax1.plot([x[i], x[j]], [y[i], y[j]], 'gray', alpha=0.3, linewidth=0.5)

# Color nodes based on status
colors = []
for i in range(N):
    if failed[i]:
        colors.append(MLRED)
    elif stressed[i]:
        colors.append(MLORANGE)
    else:
        colors.append(MLGREEN)

sizes = original_buffers * 2000
ax1.scatter(x, y, s=sizes, c=colors, alpha=0.7, edgecolors='black', linewidth=1)

# Label shock node
ax1.text(x[shock_node], y[shock_node], 'Shock', ha='center', va='center',
         fontsize=10, fontweight='bold')

ax1.set_xlim(-1.3, 1.3)
ax1.set_ylim(-1.3, 1.3)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('Network Contagion Map')

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=MLGREEN, label='Healthy'),
    Patch(facecolor=MLORANGE, label='Stressed'),
    Patch(facecolor=MLRED, label='Failed')
]
ax1.legend(handles=legend_elements, loc='upper left')

# Right panel: Failures per round
rounds = np.arange(len(round_failures))
ax2.bar(rounds, round_failures, color=MLRED, alpha=0.7, edgecolor='black')
ax2.set_xlabel('Cascade Round')
ax2.set_ylabel('New Failures')
ax2.set_title('Contagion Cascade Dynamics')
ax2.grid(axis='y', alpha=0.3)
ax2.set_xticks(rounds)

plt.suptitle('Financial Contagion: Network Cascade Simulation', fontsize=16, fontweight='bold')
plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
