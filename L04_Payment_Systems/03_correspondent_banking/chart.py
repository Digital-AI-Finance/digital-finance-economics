"""Correspondent Banking Network: Scale-Free Topology

Barabasi-Albert preferential attachment model showing hub vulnerability.
Theory: Barabasi & Albert (1999), Network Science.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (14, 7), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# ============================================================================
# Barabasi-Albert Network Generation (Pure Numpy Implementation)
# ============================================================================

def barabasi_albert_network(n=50, m=2):
    """Generate BA scale-free network using preferential attachment.

    Parameters:
    - n: number of nodes (banks)
    - m: number of edges per new node

    Returns:
    - adj_matrix: n x n adjacency matrix (symmetric, undirected)
    """
    # Start with m fully connected nodes
    adj_matrix = np.zeros((n, n), dtype=int)
    for i in range(m):
        for j in range(i+1, m):
            adj_matrix[i, j] = 1
            adj_matrix[j, i] = 1

    # Add nodes one at a time
    for new_node in range(m, n):
        # Calculate attachment probabilities (proportional to degree)
        degrees = adj_matrix[:new_node, :new_node].sum(axis=1)
        total_degree = degrees.sum()

        if total_degree == 0:
            probs = np.ones(new_node) / new_node
        else:
            probs = degrees / total_degree

        # Select m nodes to connect to (without replacement)
        targets = np.random.choice(new_node, size=m, replace=False, p=probs)

        # Add edges
        for target in targets:
            adj_matrix[new_node, target] = 1
            adj_matrix[target, new_node] = 1

    return adj_matrix

def calculate_centralities(adj_matrix):
    """Calculate degree and betweenness centrality."""
    n = len(adj_matrix)

    # Degree centrality: number of connections
    degree = adj_matrix.sum(axis=1)
    degree_centrality = degree / (n - 1)  # Normalized

    # Betweenness centrality: fraction of shortest paths through node
    betweenness = np.zeros(n)

    # BFS for all pairs shortest paths
    for s in range(n):
        # Single source shortest paths
        visited = np.zeros(n, dtype=bool)
        distance = np.full(n, np.inf)
        num_paths = np.zeros(n)
        predecessors = [[] for _ in range(n)]

        distance[s] = 0
        num_paths[s] = 1
        queue = [s]
        visited[s] = True

        # Forward BFS
        while queue:
            v = queue.pop(0)
            for w in np.where(adj_matrix[v] == 1)[0]:
                if not visited[w]:
                    visited[w] = True
                    distance[w] = distance[v] + 1
                    queue.append(w)

                if distance[w] == distance[v] + 1:
                    num_paths[w] += num_paths[v]
                    predecessors[w].append(v)

        # Backward accumulation
        dependency = np.zeros(n)
        # Sort by distance (descending)
        nodes_by_distance = sorted(range(n), key=lambda x: distance[x], reverse=True)

        for w in nodes_by_distance:
            for v in predecessors[w]:
                dependency[v] += (num_paths[v] / num_paths[w]) * (1 + dependency[w])
            if w != s:
                betweenness[w] += dependency[w]

    # Normalize betweenness
    betweenness /= ((n - 1) * (n - 2))

    return degree_centrality, betweenness, degree

def spring_layout(adj_matrix, iterations=50, k=None):
    """Simple force-directed layout (Fruchterman-Reingold style)."""
    n = len(adj_matrix)
    if k is None:
        k = np.sqrt(1.0 / n)

    # Random initial positions
    pos = np.random.rand(n, 2)

    for _ in range(iterations):
        # Repulsive forces between all pairs
        disp = np.zeros((n, 2))
        for i in range(n):
            delta = pos[i] - pos
            dist = np.sqrt((delta ** 2).sum(axis=1))
            dist[dist == 0] = 0.01
            # Repulsion
            disp[i] = (delta / dist[:, np.newaxis] * (k**2 / dist)[:, np.newaxis]).sum(axis=0)

        # Attractive forces for connected nodes
        for i in range(n):
            for j in range(i+1, n):
                if adj_matrix[i, j] == 1:
                    delta = pos[i] - pos[j]
                    dist = np.linalg.norm(delta)
                    if dist > 0:
                        force = dist**2 / k
                        disp[i] -= delta / dist * force
                        disp[j] += delta / dist * force

        # Update positions
        length = np.sqrt((disp**2).sum(axis=1))
        length[length == 0] = 0.1
        pos += disp / length[:, np.newaxis] * np.minimum(length, 0.1)[:, np.newaxis]

        # Keep within bounds
        pos = np.clip(pos, 0.05, 0.95)

    return pos

def calculate_path_metrics(adj_matrix):
    """Calculate mean path length and network diameter."""
    n = len(adj_matrix)
    distances = []

    for s in range(n):
        visited = np.zeros(n, dtype=bool)
        distance = np.full(n, np.inf)
        distance[s] = 0
        queue = [s]
        visited[s] = True

        while queue:
            v = queue.pop(0)
            for w in np.where(adj_matrix[v] == 1)[0]:
                if not visited[w]:
                    visited[w] = True
                    distance[w] = distance[v] + 1
                    queue.append(w)

        # Collect finite distances (excluding self)
        for d in distance:
            if d > 0 and d < np.inf:
                distances.append(d)

    if distances:
        return np.mean(distances), max(distances)
    return np.inf, np.inf

# ============================================================================
# Generate Network and Calculate Metrics
# ============================================================================

N = 50
M = 2

adj_matrix = barabasi_albert_network(n=N, m=M)
degree_cent, betweenness_cent, degree = calculate_centralities(adj_matrix)

# Identify top 5 hubs
hub_indices = np.argsort(degree)[-5:]
hub_scores = degree[hub_indices]

# Calculate vulnerability (remove top hub)
top_hub = hub_indices[-1]
adj_matrix_damaged = adj_matrix.copy()
adj_matrix_damaged[top_hub, :] = 0
adj_matrix_damaged[:, top_hub] = 0

mean_path_before, diameter_before = calculate_path_metrics(adj_matrix)
mean_path_after, diameter_after = calculate_path_metrics(adj_matrix_damaged)

# Layout
pos = spring_layout(adj_matrix, iterations=100)

# ============================================================================
# Visualization: Two-Panel Layout
# ============================================================================

fig = plt.figure(figsize=(14, 7))
gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1], wspace=0.3)

# ============================================================================
# Panel 1: Network Graph
# ============================================================================

ax1 = fig.add_subplot(gs[0])

# Draw edges
for i in range(N):
    for j in range(i+1, N):
        if adj_matrix[i, j] == 1:
            ax1.plot([pos[i, 0], pos[j, 0]], [pos[i, 1], pos[j, 1]],
                    color='gray', alpha=0.3, linewidth=0.5, zorder=1)

# Draw nodes
node_sizes = 50 + 400 * degree_cent
colors = np.where(np.isin(np.arange(N), hub_indices), MLRED, MLBLUE)

for i in range(N):
    ax1.scatter(pos[i, 0], pos[i, 1], s=node_sizes[i], c=colors[i],
               alpha=0.7, edgecolors='white', linewidth=1, zorder=2)

# Annotate top hub
top_hub_pos = pos[top_hub]
ax1.annotate('Top Hub\n"Too Connected\nto Fail"',
            xy=(top_hub_pos[0], top_hub_pos[1]),
            xytext=(top_hub_pos[0] + 0.15, top_hub_pos[1] + 0.15),
            fontsize=10, color=MLRED, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor=MLRED),
            arrowprops=dict(arrowstyle='->', color=MLRED, lw=2))

# Metrics text box
metrics_text = (
    f"Network Metrics:\n"
    f"• Nodes: {N} banks\n"
    f"• Mean path length: {mean_path_before:.2f} hops\n"
    f"• Top hub degree: {hub_scores[-1]:.0f}\n\n"
    f"Vulnerability Analysis:\n"
    f"• If top hub fails:\n"
    f"  Path length: {mean_path_before:.2f} → {mean_path_after:.2f}\n"
    f"  ({((mean_path_after/mean_path_before - 1) * 100):.0f}% increase)"
)

ax1.text(0.02, 0.98, metrics_text, transform=ax1.transAxes,
        fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor=MLPURPLE))

ax1.set_xlim(-0.05, 1.05)
ax1.set_ylim(-0.05, 1.05)
ax1.axis('off')
ax1.set_title('Correspondent Banking Network Topology\n(Barabasi-Albert Scale-Free Model)',
             fontsize=14, fontweight='bold', color=MLPURPLE, pad=10)

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=MLRED,
           markersize=10, label='Hub Banks (Top 5)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=MLBLUE,
           markersize=8, label='Regional Banks')
]
ax1.legend(handles=legend_elements, loc='lower right', framealpha=0.9, fontsize=10)

# ============================================================================
# Panel 2: Degree Distribution (Power Law)
# ============================================================================

ax2 = fig.add_subplot(gs[1])

# Degree distribution
degree_values, degree_counts = np.unique(degree, return_counts=True)

# Log-log plot to show power law
ax2.scatter(degree_values, degree_counts, s=80, color=MLPURPLE, alpha=0.7,
           edgecolors='white', linewidth=1.5, zorder=3)

# Fit power law: P(k) ~ k^(-γ)
log_k = np.log(degree_values[degree_values > 0])
log_p = np.log(degree_counts[degree_values > 0])
if len(log_k) > 1:
    gamma = -np.polyfit(log_k, log_p, 1)[0]

    # Plot fitted line
    k_fit = np.linspace(degree_values.min(), degree_values.max(), 100)
    p_fit = degree_counts.max() * (k_fit / degree_values[0]) ** (-gamma)
    ax2.plot(k_fit, p_fit, '--', color=MLORANGE, linewidth=2,
            label=f'Power law: P(k) ∝ k$^{{-{gamma:.2f}}}$', zorder=2)

ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlabel('Degree (k)', fontweight='bold')
ax2.set_ylabel('Frequency', fontweight='bold')
ax2.set_title('Degree Distribution\n(Scale-Free Property)', fontsize=13,
             fontweight='bold', color=MLPURPLE)
ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
ax2.legend(framealpha=0.9, fontsize=10)

# Annotate hub region
if degree_values.max() > 10:
    ax2.annotate('Hubs', xy=(degree_values.max(), 1),
                xytext=(degree_values.max() * 0.6, degree_counts.max() * 0.5),
                fontsize=10, color=MLRED, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5))

# Citation
fig.text(0.5, 0.02,
        'Theory: Barabási & Albert (1999), "Emergence of Scaling in Random Networks", Science',
        ha='center', fontsize=9, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.04, 1, 1])

# ============================================================================
# Save Output
# ============================================================================

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()

print("Chart saved to chart.pdf and chart.png")
print(f"\nNetwork Statistics:")
print(f"  Total banks: {N}")
print(f"  Total connections: {adj_matrix.sum() // 2}")
print(f"  Mean degree: {degree.mean():.2f}")
print(f"  Top 5 hub degrees: {sorted(hub_scores)[::-1]}")
print(f"  Mean path length: {mean_path_before:.2f} hops")
print(f"  Network diameter: {diameter_before:.0f} hops")
print(f"\nVulnerability:")
print(f"  Path length increase if top hub fails: {((mean_path_after/mean_path_before - 1) * 100):.0f}%")
