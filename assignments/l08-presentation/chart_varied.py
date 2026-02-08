r"""Financial Contagion Variations: 2x2 Comparison

Compares baseline contagion model with three variations:
1. Doubled capital buffers [0.10, 0.40]
2. Dense network (p=0.7 instead of 0.3)
3. Three initial failures instead of one
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.patches import Patch

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 14,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

def simulate_contagion(N=20, buffer_range=(0.05, 0.2), conn_prob=0.3, initial_failures=None):
    """Run contagion simulation with specified parameters"""
    # Network setup
    angles = 2 * np.pi * np.arange(N) / N
    x = np.cos(angles)
    y = np.sin(angles)

    # Create adjacency matrix (symmetric, no self-loops)
    adj = np.random.rand(N, N) < conn_prob
    adj = np.triu(adj, 1)
    adj = adj + adj.T
    np.fill_diagonal(adj, 0)

    # Capital buffers
    buffers = np.random.uniform(buffer_range[0], buffer_range[1], N)
    original_buffers = buffers.copy()

    # Degree of each node
    degrees = adj.sum(axis=1)
    degrees = np.maximum(degrees, 1)

    # Contagion simulation
    failed = np.zeros(N, dtype=bool)
    stressed = np.zeros(N, dtype=bool)

    # Set initial failures
    if initial_failures is None:
        initial_failures = [0]
    for node in initial_failures:
        failed[node] = True

    round_failures = [len(initial_failures)]

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

    return x, y, adj, failed, stressed, original_buffers, initial_failures

def plot_network(ax, x, y, adj, failed, stressed, original_buffers, initial_failures, title):
    """Plot network visualization"""
    N = len(x)

    # Draw edges
    for i in range(N):
        for j in range(i+1, N):
            if adj[i, j]:
                ax.plot([x[i], x[j]], [y[i], y[j]], 'gray', alpha=0.3, linewidth=0.5)

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
    ax.scatter(x, y, s=sizes, c=colors, alpha=0.7, edgecolors='black', linewidth=1)

    # Label initial shock nodes
    for shock_node in initial_failures:
        ax.text(x[shock_node], y[shock_node], 'S', ha='center', va='center',
                fontsize=9, fontweight='bold', color='white')

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=12, fontweight='bold')

    # Add failure count
    total_failures = failed.sum()
    ax.text(0.5, 0.95, f'Total failures: {total_failures}',
            transform=ax.transAxes, fontsize=11, fontweight='bold',
            ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                     edgecolor=MLRED, linewidth=2, alpha=0.9))

# Create 2x2 subplot
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

# Panel 1: BASELINE
np.random.seed(42)
x, y, adj, failed, stressed, buffers, init = simulate_contagion(
    buffer_range=(0.05, 0.2), conn_prob=0.3, initial_failures=[0]
)
plot_network(axes[0], x, y, adj, failed, stressed, buffers, init,
            'Baseline: Standard Buffers [0.05, 0.20], p=0.3')

# Panel 2: VARIATION 1 - Doubled Buffers
np.random.seed(42)
x, y, adj, failed, stressed, buffers, init = simulate_contagion(
    buffer_range=(0.10, 0.4), conn_prob=0.3, initial_failures=[0]
)
plot_network(axes[1], x, y, adj, failed, stressed, buffers, init,
            'Variation 1: Doubled Buffers [0.10, 0.40], p=0.3')

# Panel 3: VARIATION 2 - Dense Network
np.random.seed(42)
x, y, adj, failed, stressed, buffers, init = simulate_contagion(
    buffer_range=(0.05, 0.2), conn_prob=0.7, initial_failures=[0]
)
plot_network(axes[2], x, y, adj, failed, stressed, buffers, init,
            'Variation 2: Dense Network [0.05, 0.20], p=0.7')

# Panel 4: VARIATION 3 - Three Initial Failures
np.random.seed(42)
x, y, adj, failed, stressed, buffers, init = simulate_contagion(
    buffer_range=(0.05, 0.2), conn_prob=0.3, initial_failures=[0, 1, 2]
)
plot_network(axes[3], x, y, adj, failed, stressed, buffers, init,
            'Variation 3: Three Initial Failures [0.05, 0.20], p=0.3')

# Add shared legend
legend_elements = [
    Patch(facecolor=MLGREEN, label='Healthy', edgecolor='black'),
    Patch(facecolor=MLORANGE, label='Stressed (>50% buffer lost)', edgecolor='black'),
    Patch(facecolor=MLRED, label='Failed', edgecolor='black')
]
fig.legend(handles=legend_elements, loc='upper center', ncol=3,
          fontsize=12, frameon=True, fancybox=True, shadow=True,
          bbox_to_anchor=(0.5, 0.98))

plt.suptitle('Financial Contagion: Comparing Network Variations',
            fontsize=16, fontweight='bold', y=0.995)

plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.savefig(Path(__file__).parent / 'chart_varied.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart_varied.png', dpi=150, bbox_inches='tight')
plt.close()
print("Variation comparison chart saved to chart_varied.pdf and chart_varied.png")
