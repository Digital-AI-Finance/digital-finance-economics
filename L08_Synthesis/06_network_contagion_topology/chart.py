r"""Acemoglu Network Contagion Topology Comparison
# Multi-panel override: comparative statics requires simultaneous visibility

Acemoglu contagion: $L_i = \max(0, \sum_j a_{ij}L_j - c_i)$. Ring, complete, star.
Based on Acemoglu et al. (2015).

Economic Model:
Loss propagation in financial networks:
$L_i = \max\bigl(0,\; \sum_j a_{ij} L_j - c_i\bigr)$
where $a_{ij}$ is the exposure weight from node $i$ to node $j$,
$L_j$ is the loss at node $j$, and $c_i$ is the capital buffer of node $i$.
Dense networks are robust-yet-fragile: small shocks absorbed, large shocks cascade everywhere.

Citation: Acemoglu, Ozdaglar & Tahbaz-Salehi (2015) - Systemic Risk and Stability in Financial Networks
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 11, 'axes.titlesize': 13,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# ── Parameters ──
N = 10            # number of nodes
c_i = 0.5        # capital buffer per node
shock = 1.0       # initial shock to node 0
theta_A = c_i     # cascade threshold (= capital buffer)


def build_adjacency(topology, n):
    """Build adjacency matrix for ring, complete, or star topology."""
    A = np.zeros((n, n))
    if topology == 'ring':
        for i in range(n):
            A[i, (i + 1) % n] = 1.0 / 1.0  # each node exposed to next
            A[i, (i - 1) % n] = 1.0 / 1.0
        # Normalize: each node's total outgoing = 1
        for i in range(n):
            row_sum = A[i].sum()
            if row_sum > 0:
                A[i] /= row_sum
    elif topology == 'complete':
        for i in range(n):
            for j in range(n):
                if i != j:
                    A[i, j] = 1.0 / (n - 1)
    elif topology == 'star':
        center = 0
        for i in range(1, n):
            A[center, i] = 1.0 / (n - 1)  # center -> periphery
            A[i, center] = 1.0             # periphery -> center only
    return A


def simulate_contagion(A, n, c, shock_val, shocked_node=0):
    """Simulate Acemoglu contagion: L_i = max(0, sum_j a_ij * L_j - c_i)."""
    L = np.zeros(n)
    L[shocked_node] = shock_val
    failed = np.zeros(n, dtype=bool)
    failed[shocked_node] = True

    for _ in range(20):  # iterate until convergence
        L_new = np.zeros(n)
        L_new[shocked_node] = shock_val
        for i in range(n):
            if i == shocked_node:
                continue
            incoming = sum(A[j, i] * L[j] for j in range(n) if j != i)
            L_new[i] = max(0.0, incoming - c)
        if np.allclose(L_new, L, atol=1e-8):
            break
        L = L_new.copy()

    failed = L > 0
    failed[shocked_node] = True
    return L, failed


def get_positions(topology, n):
    """Get (x, y) positions for nodes."""
    if topology == 'star':
        positions = np.zeros((n, 2))
        positions[0] = [0, 0]  # center
        angles = np.linspace(0, 2 * np.pi, n - 1, endpoint=False)
        for i, ang in enumerate(angles):
            positions[i + 1] = [np.cos(ang), np.sin(ang)]
        return positions
    else:  # ring and complete both use circle layout
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False) + np.pi / 2
        return np.column_stack([np.cos(angles), np.sin(angles)])


def draw_network(ax, A, positions, failed, losses, topology_name, n):
    """Draw network with matplotlib primitives."""
    # Draw edges
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] > 0 or A[j, i] > 0:
                weight = max(A[i, j], A[j, i])
                lw = 0.3 + weight * 1.5
                alpha = 0.15 + weight * 0.3
                # Color edge red if both endpoints failed
                edge_color = MLRED if (failed[i] and failed[j]) else '#888888'
                line = plt.Line2D(
                    [positions[i, 0], positions[j, 0]],
                    [positions[i, 1], positions[j, 1]],
                    linewidth=lw, color=edge_color, alpha=alpha, zorder=1
                )
                ax.add_line(line)

    # Draw nodes
    for i in range(n):
        if i == 0:  # shocked node
            color = MLRED
            edge_c = '#8B0000'
        elif failed[i]:
            color = MLORANGE
            edge_c = '#CC6600'
        else:
            color = MLGREEN
            edge_c = '#006600'

        radius = 0.12
        circle = plt.Circle(
            positions[i], radius, facecolor=color,
            edgecolor=edge_c, linewidth=1.8, zorder=3, alpha=0.85
        )
        ax.add_patch(circle)
        ax.text(positions[i, 0], positions[i, 1], str(i),
                ha='center', va='center', fontsize=7,
                fontweight='bold', color='white', zorder=4)

    n_failed = int(failed.sum())
    total_loss = losses.sum()
    ax.set_title(f'{topology_name}\n{n_failed} failed, total loss={total_loss:.2f}',
                 fontsize=11, fontweight='bold')
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')


# ── Build and simulate ──
topologies = ['ring', 'complete', 'star']
titles = ['Ring (sequential)', 'Complete (dense)', 'Star (hub-spoke)']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for idx, (topo, title) in enumerate(zip(topologies, titles)):
    A = build_adjacency(topo, N)
    positions = get_positions(topo, N)
    losses, failed = simulate_contagion(A, N, c_i, shock)
    draw_network(axes[idx], A, positions, failed, losses, title, N)

# Add shared legend
legend_elements = [
    mpatches.Patch(facecolor=MLRED, edgecolor='#8B0000', label='Shocked node'),
    mpatches.Patch(facecolor=MLORANGE, edgecolor='#CC6600', label='Failed (cascade)'),
    mpatches.Patch(facecolor=MLGREEN, edgecolor='#006600', label='Healthy'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3,
           fontsize=10, framealpha=0.9, edgecolor='gray',
           bbox_to_anchor=(0.5, -0.02))

fig.suptitle(r'Acemoglu Contagion: $L_i = \max(0,\;\sum_j a_{ij}L_j - c_i)$'
             '\nN=10 nodes, capital buffer=0.5, shock=1.0 to node 0',
             fontsize=13, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
