"""Digital Finance Trilemma"""
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

# Triangle vertices
A = np.array([0.5, np.sqrt(3)/2])  # Efficiency (top)
B = np.array([0, 0])                # Stability (bottom-left)
C = np.array([1, 0])                # Innovation (bottom-right)

# Systems with barycentric coordinates (efficiency, stability, innovation)
systems = {
    'Bitcoin': (0.2, 0.3, 0.5, MLORANGE),
    'Ethereum': (0.3, 0.25, 0.45, MLPURPLE),
    'CBDC': (0.35, 0.5, 0.15, MLBLUE),
    'Visa': (0.5, 0.4, 0.1, MLGREEN),
    'Stablecoins': (0.3, 0.35, 0.35, MLRED),
    'DeFi': (0.15, 0.15, 0.7, MLLAVENDER)
}

def barycentric_to_cartesian(eff, stab, innov):
    """Convert barycentric coordinates to Cartesian"""
    # Normalize
    total = eff + stab + innov
    a, b, c = eff/total, stab/total, innov/total

    x = a * A[0] + b * B[0] + c * C[0]
    y = a * A[1] + b * B[1] + c * C[1]
    return x, y

# Visualization
fig, ax = plt.subplots(figsize=(10, 9))

# Draw triangle
triangle = np.array([A, B, C, A])
ax.plot(triangle[:, 0], triangle[:, 1], 'k-', linewidth=2)

# Label vertices
offset = 0.08
ax.text(A[0], A[1] + offset, 'Efficiency', ha='center', va='bottom',
        fontsize=14, fontweight='bold')
ax.text(B[0] - offset, B[1], 'Stability', ha='right', va='center',
        fontsize=14, fontweight='bold')
ax.text(C[0] + offset, C[1], 'Innovation', ha='left', va='center',
        fontsize=14, fontweight='bold')

# Plot systems
for name, (eff, stab, innov, color) in systems.items():
    x, y = barycentric_to_cartesian(eff, stab, innov)
    ax.scatter(x, y, s=200, c=color, alpha=0.7, edgecolors='black', linewidth=2)
    ax.text(x, y - 0.05, name, ha='center', va='top', fontsize=11, fontweight='bold')

# Draw arrow from Ethereum toward Efficiency (showing movement)
eth_x, eth_y = barycentric_to_cartesian(0.3, 0.25, 0.45)
target_x, target_y = barycentric_to_cartesian(0.4, 0.2, 0.4)
ax.annotate('', xy=(target_x, target_y), xytext=(eth_x, eth_y),
            arrowprops=dict(arrowstyle='->', lw=2, color='black', alpha=0.5))

# Add grid lines (optional)
for i in np.linspace(0, 1, 6):
    # Lines parallel to BC (constant efficiency)
    p1 = i * A + (1-i) * B
    p2 = i * A + (1-i) * C
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'gray', alpha=0.2, linewidth=0.5)

    # Lines parallel to AC (constant stability)
    p1 = i * B + (1-i) * A
    p2 = i * B + (1-i) * C
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'gray', alpha=0.2, linewidth=0.5)

    # Lines parallel to AB (constant innovation)
    p1 = i * C + (1-i) * A
    p2 = i * C + (1-i) * B
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'gray', alpha=0.2, linewidth=0.5)

ax.set_xlim(-0.15, 1.15)
ax.set_ylim(-0.15, 1.0)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Digital Finance Trilemma', fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
