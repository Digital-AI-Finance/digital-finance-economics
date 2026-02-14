r"""Blockchain Trilemma: Technology Frontier (Ternary + Radar)
# Multi-panel override: comparative statics requires simultaneous visibility

Trilemma: $D + S + Sc \leq K$. BTC(0.45,0.45,0.10), ETH(0.35,0.40,0.25).
Based on Buterin (2017).

Economic Model:
Blockchain impossibility constraint:
$D + S + Sc \leq K$
where $D$ = decentralization, $S$ = security, $Sc$ = scalability,
and $K$ is the technology frontier parameter.
Technological progress shifts $K$ outward but does not eliminate the trade-off.

Citation: Buterin (2017) - The Blockchain Trilemma; Abadi & Brunnermeier (2018) - Blockchain Economics
"""
import matplotlib.pyplot as plt
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

# ── Barycentric to Cartesian transform (matplotlib-native ternary) ──
# Vertices: Decentralization (top), Security (bottom-left), Scalability (bottom-right)
def bary_to_cart(d, s, sc):
    """Convert barycentric (D, S, Sc) to Cartesian (x, y).
    x = 0.5*(2*b + c)/(a+b+c), y = (sqrt(3)/2)*c/(a+b+c)
    Mapping: a=S (bottom-left), b=Sc (bottom-right), c=D (top)
    """
    total = d + s + sc
    a, b, c = s / total, sc / total, d / total
    x = 0.5 * (2 * b + c) / (a + b + c)
    y = (np.sqrt(3) / 2) * c / (a + b + c)
    return x, y


# ── Systems (Decentralization, Security, Scalability) ──
systems = {
    'BTC':  (0.45, 0.45, 0.10, MLORANGE, 's'),
    'ETH':  (0.35, 0.40, 0.25, MLPURPLE, 'D'),
    'SOL':  (0.15, 0.30, 0.55, MLBLUE,   '^'),
    'Visa': (0.05, 0.45, 0.50, MLGREEN,  'v'),
    'CBDC': (0.10, 0.50, 0.40, MLRED,    'o'),
}

# Frontier K values
K_values = [1.0, 1.2, 1.5]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5))

# ══════════════════════════════════════════════════════════
# Panel (a): Matplotlib-native ternary plot
# ══════════════════════════════════════════════════════════

# Triangle vertices in Cartesian
# Bottom-left = Security, Bottom-right = Scalability, Top = Decentralization
v_S = np.array([0.0, 0.0])      # Security (bottom-left)
v_Sc = np.array([1.0, 0.0])     # Scalability (bottom-right)
v_D = np.array([0.5, np.sqrt(3) / 2])  # Decentralization (top)

# Draw triangle border
triangle = plt.Polygon([v_S, v_Sc, v_D], fill=False, edgecolor='black',
                         linewidth=2, zorder=2)
ax1.add_patch(triangle)

# Draw grid lines (lines of constant barycentric coordinate)
n_grid = 5
for i in range(1, n_grid):
    frac = i / n_grid
    # Constant D lines (parallel to S-Sc edge)
    p1 = (1 - frac) * v_S + frac * v_D
    p2 = (1 - frac) * v_Sc + frac * v_D
    ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color='gray', alpha=0.25,
             linewidth=0.7, zorder=1)
    # Constant S lines (parallel to D-Sc edge)
    p1 = (1 - frac) * v_Sc + frac * v_S
    p2 = (1 - frac) * v_D + frac * v_S
    ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color='gray', alpha=0.25,
             linewidth=0.7, zorder=1)
    # Constant Sc lines (parallel to D-S edge)
    p1 = (1 - frac) * v_S + frac * v_Sc
    p2 = (1 - frac) * v_D + frac * v_Sc
    ax1.plot([p1[0], p2[0]], [p1[1], p2[1]], color='gray', alpha=0.25,
             linewidth=0.7, zorder=1)

# Axis labels
offset = 0.06
ax1.text(v_D[0], v_D[1] + offset, 'Decentralization', ha='center', va='bottom',
         fontsize=11, fontweight='bold', color=MLPURPLE)
ax1.text(v_S[0] - offset, v_S[1] - offset, 'Security', ha='right', va='top',
         fontsize=11, fontweight='bold', color=MLPURPLE)
ax1.text(v_Sc[0] + offset, v_Sc[1] - offset, 'Scalability', ha='left', va='top',
         fontsize=11, fontweight='bold', color=MLPURPLE)

# Draw frontier curves for different K values
frontier_colors = ['#cccccc', '#999999', '#555555']
frontier_styles = [':', '--', '-']
for K, fc, fs in zip(K_values, frontier_colors, frontier_styles):
    # Sample points on the frontier D + S + Sc = K (renormalized to sum=1 for ternary)
    # For a given K, the "edge" of feasible region in normalized coords
    # shifts outward. We draw a curved line showing normalized allocations
    # at the boundary.
    if K <= 1.0:
        # K=1 is the outer triangle itself, skip drawing
        continue
    # For K>1, technology expands possibility: show as inner triangle scaled
    # The frontier shrinks the infeasible region
    scale = 1.0 / K  # points closer to center become feasible
    # Draw the iso-K curve as a smaller triangle (inverted meaning)
    # Actually: K>1 means more total budget, so the frontier expands
    # We show this as annotation only
    ax1.text(0.5, 0.02 + (K - 1.0) * 0.15,
             f'K={K}', ha='center', fontsize=8, color=fc, fontweight='bold')

# Plot systems
for name, (d, s, sc, color, marker) in systems.items():
    x, y = bary_to_cart(d, s, sc)
    ax1.scatter(x, y, s=180, c=color, marker=marker, edgecolors='black',
                linewidth=1.5, zorder=5, alpha=0.9, label=name)
    # Label offset to avoid overlap
    offsets = {'BTC': (-0.07, 0.03), 'ETH': (0.07, 0.03),
               'SOL': (0.07, -0.04), 'Visa': (-0.07, -0.04),
               'CBDC': (0.00, -0.05)}
    dx, dy = offsets.get(name, (0.05, 0.02))
    ax1.text(x + dx, y + dy, name, fontsize=9, fontweight='bold', color=color,
             ha='center', va='center', zorder=6)

ax1.legend(loc='upper left', fontsize=8, framealpha=0.9, markerscale=0.8,
           bbox_to_anchor=(-0.02, 1.0))
ax1.set_xlim(-0.15, 1.15)
ax1.set_ylim(-0.15, 1.0)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('(a) Ternary: D + S + Sc = K', fontsize=12, fontweight='bold')

# ══════════════════════════════════════════════════════════
# Panel (b): Radar chart
# ══════════════════════════════════════════════════════════
categories = ['Decentralization', 'Security', 'Scalability']
n_cats = len(categories)
angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()
angles += angles[:1]  # close the polygon

ax2 = fig.add_subplot(122, polar=True)
ax2.set_theta_offset(np.pi / 2)
ax2.set_theta_direction(-1)
ax2.set_rlabel_position(30)

# Grid
ax2.set_yticks([0.1, 0.2, 0.3, 0.4, 0.5])
ax2.set_yticklabels(['0.1', '0.2', '0.3', '0.4', '0.5'], fontsize=8, color='gray')
ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(categories, fontsize=10, fontweight='bold')
ax2.set_ylim(0, 0.6)

for name, (d, s, sc, color, marker) in systems.items():
    values = [d, s, sc]
    values += values[:1]  # close polygon
    ax2.plot(angles, values, 'o-', linewidth=2, color=color, alpha=0.8,
             markersize=6, label=name)
    ax2.fill(angles, values, color=color, alpha=0.08)

ax2.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=8, framealpha=0.9)
ax2.set_title('(b) Radar: allocation profiles', fontsize=12, fontweight='bold', pad=20)

fig.suptitle(r'Technology Frontier: $D + S + Sc \leq K$',
             fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
