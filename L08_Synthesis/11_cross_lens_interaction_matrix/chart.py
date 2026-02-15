r"""Cross-Lens Interaction Matrix: Four Economic Lenses
# Multi-panel override: comparative statics requires simultaneous visibility

Cross-lens: 4x4 matrix. M->P:7, P->Mi:9, R->M:9. Based on course synthesis.

Economic Model:
Interaction strength matrix $I$ where $I_{ij}$ quantifies how strongly
lens $i$ influences lens $j$ (scale 0-10). Diagonal = self-reinforcement = 10.
High off-diagonal values reveal critical cross-domain feedback loops:
M (Monetary) -> P (Platform) = 7: money supply affects platform adoption.
P -> Mi (Microstructure) = 9: network effects dominate liquidity provision.
R (Regulatory) -> M = 9: regulation shapes monetary policy transmission.

Citation: Course synthesis integrating Acemoglu (2015), Adrian & Brunnermeier (2016), Cong & He (2019)
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

# ── 4x4 interaction matrix ──
lenses = ['Monetary\n(M)', 'Platform\n(P)', 'Microstructure\n(Mi)', 'Regulatory\n(R)']
short_names = ['M', 'P', 'Mi', 'R']
lens_colors = [MLORANGE, MLBLUE, MLGREEN, MLPURPLE]

# I[i,j] = influence of lens i on lens j
interaction = np.array([
    [10,  7,  5,  8],   # M -> M,P,Mi,R
    [ 6, 10,  9,  7],   # P -> M,P,Mi,R
    [ 4,  8, 10,  6],   # Mi -> M,P,Mi,R
    [ 9,  8,  7, 10],   # R -> M,P,Mi,R
])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6),
                                gridspec_kw={'width_ratios': [1, 1]})

# ══════════════════════════════════════════════════════════
# Panel (a): Annotated heatmap
# ══════════════════════════════════════════════════════════
im = ax1.imshow(interaction, cmap='YlOrRd', aspect='equal', vmin=0, vmax=10)

ax1.set_xticks(np.arange(len(lenses)))
ax1.set_yticks(np.arange(len(lenses)))
ax1.set_xticklabels(lenses, fontsize=9)
ax1.set_yticklabels(lenses, fontsize=9)

# Annotate cells
for i in range(len(lenses)):
    for j in range(len(lenses)):
        val = interaction[i, j]
        text_color = 'white' if val >= 8 else 'black'
        ax1.text(j, i, f'{val}', ha='center', va='center',
                 fontsize=12, fontweight='bold', color=text_color)

cbar = plt.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
cbar.set_label('Interaction strength (0-10)', fontsize=9)

ax1.set_title('(a) Cross-lens interaction matrix', fontsize=12, fontweight='bold')
ax1.set_xlabel('Target lens (influenced)', fontsize=10)
ax1.set_ylabel('Source lens (influencer)', fontsize=10)

# Highlight strongest off-diagonal interactions
# P->Mi = 9
ax1.add_patch(plt.Rectangle((2 - 0.45, 1 - 0.45), 0.9, 0.9,
              fill=False, edgecolor='yellow', linewidth=2.5, zorder=10))
# R->M = 9
ax1.add_patch(plt.Rectangle((0 - 0.45, 3 - 0.45), 0.9, 0.9,
              fill=False, edgecolor='yellow', linewidth=2.5, zorder=10))

ax1.text(0.98, 0.02, 'Yellow = strongest\ncross-domain effects',
         transform=ax1.transAxes, ha='right', va='bottom',
         fontsize=8, style='italic', color='#666666',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# ══════════════════════════════════════════════════════════
# Panel (b): Network with matplotlib (4 nodes, weighted edges)
# ══════════════════════════════════════════════════════════

# Node positions in a diamond layout
positions = {
    0: np.array([0.5, 0.85]),   # M (top)
    1: np.array([0.15, 0.5]),   # P (left)
    2: np.array([0.85, 0.5]),   # Mi (right)
    3: np.array([0.5, 0.15]),   # R (bottom)
}
node_radius = 0.08

# Draw edges (off-diagonal only)
for i in range(4):
    for j in range(4):
        if i == j:
            continue
        val = interaction[i, j]
        if val < 4:
            continue  # skip very weak connections
        src = positions[i]
        tgt = positions[j]
        direction = tgt - src
        dist = np.linalg.norm(direction)
        unit = direction / dist
        # Offset from node boundary
        start = src + unit * (node_radius + 0.02)
        end = tgt - unit * (node_radius + 0.02)

        lw = 0.5 + val * 0.4
        alpha = 0.3 + (val / 10) * 0.5
        color = MLRED if val >= 8 else (MLORANGE if val >= 6 else '#888888')

        ax2.annotate('', xy=end, xytext=start,
                     arrowprops=dict(arrowstyle='->', lw=lw, color=color,
                                     alpha=alpha, connectionstyle='arc3,rad=0.2'))
        # Label on edge
        mid = (start + end) / 2
        # Perpendicular offset for label
        perp = np.array([-unit[1], unit[0]]) * 0.04
        ax2.text(mid[0] + perp[0], mid[1] + perp[1], str(val),
                 ha='center', va='center', fontsize=7, fontweight='bold',
                 color=color, alpha=0.9,
                 bbox=dict(boxstyle='round,pad=0.1', facecolor='white',
                           edgecolor='none', alpha=0.7))

# Draw nodes
for i in range(4):
    circle = plt.Circle(positions[i], node_radius, facecolor=lens_colors[i],
                        edgecolor='black', linewidth=1.8, zorder=5, alpha=0.9)
    ax2.add_patch(circle)
    ax2.text(positions[i][0], positions[i][1], short_names[i],
             ha='center', va='center', fontsize=11,
             fontweight='bold', color='white', zorder=6)

# Legend
legend_els = [
    plt.Line2D([0], [0], color=MLRED, lw=3, label='Strong (8-9)'),
    plt.Line2D([0], [0], color=MLORANGE, lw=2, label='Moderate (6-7)'),
    plt.Line2D([0], [0], color='#888888', lw=1, label='Weak (4-5)'),
]
ax2.legend(handles=legend_els, loc='lower right', fontsize=8,
           title='Edge weight', title_fontsize=8, framealpha=0.9)

ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('(b) Interaction network', fontsize=12, fontweight='bold')

fig.suptitle('Cross-Lens Interaction: How Economic Frameworks Interconnect',
             fontsize=14, fontweight='bold', y=1.01)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
