"""Digital Finance Trilemma: Constraint Optimization

Impossible trinity in blockchain design - decentralization, security, scalability.
Theory: Adapted from monetary policy trilemma (Mundell-Fleming).
Constraint: Systems cannot simultaneously maximize all three properties.

Based on: Auer et al. (2021) - CBDC Trilemma
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

# Triangle vertices for ternary plot
# Decentralization (top), Security (bottom-left), Scalability (bottom-right)
A = np.array([0.5, np.sqrt(3)/2])  # Decentralization (top)
B = np.array([0, 0])                # Security (bottom-left)
C = np.array([1, 0])                # Scalability (bottom-right)

# Systems with barycentric coordinates (decentralization, security, scalability)
# Constraint: Can optimize at most 2 of 3 dimensions
# Values sum to ~2 (normalized to 1), showing the tradeoff
systems = {
    'Bitcoin': (0.45, 0.45, 0.10, MLORANGE),      # High D+S, Low Sc
    'Ethereum': (0.40, 0.40, 0.20, MLPURPLE),     # High D+S, Low Sc (improving)
    'Visa': (0.05, 0.45, 0.50, MLGREEN),          # Low D, High S+Sc
    'Solana': (0.25, 0.30, 0.45, MLBLUE),         # Medium D+S, High Sc
    'BSC': (0.15, 0.35, 0.50, MLRED),             # Low D, Medium S, High Sc
    'Lightning': (0.35, 0.35, 0.30, MLLAVENDER)   # Balanced compromise
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
ax.text(A[0], A[1] + offset, 'Decentralization', ha='center', va='bottom',
        fontsize=14, fontweight='bold', color='#1a1a1a')
ax.text(B[0] - offset, B[1], 'Security', ha='right', va='center',
        fontsize=14, fontweight='bold', color='#1a1a1a')
ax.text(C[0] + offset, C[1], 'Scalability', ha='left', va='center',
        fontsize=14, fontweight='bold', color='#1a1a1a')

# Plot feasible region (interior of triangle with slight constraint boundary)
# The constraint boundary shows that maximizing all three is impossible
constraint_threshold = 0.8  # Systems can't be above this level on all dimensions
feasible_region = plt.Polygon([A, B, C], alpha=0.05, facecolor='green',
                              edgecolor='none', zorder=0)
ax.add_patch(feasible_region)

# Add constraint boundary annotation
constraint_center = (A + B + C) / 3
ax.text(constraint_center[0], constraint_center[1] - 0.15,
        'Feasible Region\n(D + S + Sc ≤ K)',
        ha='center', va='center', fontsize=10, style='italic',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.7, edgecolor='gray'))

# Plot systems
for name, (dec, sec, scal, color) in systems.items():
    x, y = barycentric_to_cartesian(dec, sec, scal)
    ax.scatter(x, y, s=250, c=color, alpha=0.8, edgecolors='black', linewidth=2.5, zorder=5, label=name)

    # Position labels to avoid overlap
    if name == 'Bitcoin':
        offset_y = -0.06
    elif name == 'Lightning':
        offset_y = 0.06
    else:
        offset_y = -0.06

    ax.text(x, y + offset_y, name, ha='center',
            va='bottom' if offset_y > 0 else 'top',
            fontsize=11, fontweight='bold', zorder=6)

# Add legend
ax.legend(loc='upper left', framealpha=0.95, fontsize=11, title='Systems', title_fontsize=12)

# Draw tradeoff arrows showing impossible movements
# Arrow 1: Bitcoin cannot easily increase scalability without sacrificing D or S
btc_x, btc_y = barycentric_to_cartesian(0.45, 0.45, 0.10)
btc_target_x, btc_target_y = barycentric_to_cartesian(0.35, 0.35, 0.30)
ax.annotate('', xy=(btc_target_x, btc_target_y), xytext=(btc_x, btc_y),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='red', alpha=0.6,
                          linestyle='--'), zorder=4)
ax.text((btc_x + btc_target_x)/2 - 0.05, (btc_y + btc_target_y)/2,
        'Scaling\ntradeoff', fontsize=9, style='italic', color='red',
        ha='right', va='center')

# Arrow 2: Visa cannot easily increase decentralization without sacrificing performance
visa_x, visa_y = barycentric_to_cartesian(0.05, 0.45, 0.50)
visa_target_x, visa_target_y = barycentric_to_cartesian(0.25, 0.35, 0.40)
ax.annotate('', xy=(visa_target_x, visa_target_y), xytext=(visa_x, visa_y),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='blue', alpha=0.6,
                          linestyle='--'), zorder=4)
ax.text((visa_x + visa_target_x)/2 + 0.08, (visa_y + visa_target_y)/2,
        'Decentralization\ntradeoff', fontsize=9, style='italic', color='blue',
        ha='left', va='center')

# Add educational annotation - Trilemma principle
ax.text(0.5, 0.05, 'Trilemma: Choose 2 of 3\nD + S + Sc ≤ K (constraint)',
        transform=ax.transAxes, fontsize=11, fontweight='bold',
        ha='center', va='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

# Add grid lines
ax.grid(True, alpha=0.3, linestyle='--')
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

# Add legend explaining the constraint
legend_text = (
    'Trilemma Constraint:\n'
    'Systems can optimize at most 2 of 3 properties.\n'
    '• Bitcoin/Ethereum: D+S, sacrifice Sc\n'
    '• Visa/BSC: S+Sc, sacrifice D\n'
    '• Solana: Balanced compromise'
)
ax.text(1.15, 0.85, legend_text, fontsize=9, va='top', ha='left',
        bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow',
                  alpha=0.8, edgecolor='gray', linewidth=1.5))

# Add "Pick any two" annotation at edges
edge_annotation_size = 9
# D+S edge (left)
mid_AB = (A + B) / 2
ax.text(mid_AB[0] - 0.12, mid_AB[1], 'D + S\n(crypto)', fontsize=edge_annotation_size,
        ha='right', va='center', style='italic', color='#555')
# S+Sc edge (bottom)
mid_BC = (B + C) / 2
ax.text(mid_BC[0], mid_BC[1] - 0.08, 'S + Sc\n(traditional)', fontsize=edge_annotation_size,
        ha='center', va='top', style='italic', color='#555')
# D+Sc edge (right)
mid_AC = (A + C) / 2
ax.text(mid_AC[0] + 0.12, mid_AC[1], 'D + Sc\n(rare)', fontsize=edge_annotation_size,
        ha='left', va='center', style='italic', color='#555')

ax.set_xlim(-0.2, 1.35)
ax.set_ylim(-0.15, 1.0)
ax.set_aspect('equal')
ax.set_xlabel('Trilemma Space (normalized)', fontsize=13, labelpad=10)
ax.set_ylabel('Trade-off Dimension (normalized)', fontsize=13, labelpad=10)
ax.xaxis.set_visible(True)
ax.yaxis.set_visible(True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('Blockchain Trilemma: Constraint Optimization in Digital Finance',
             fontsize=17, fontweight='bold', pad=20)

# B5: Add annotation highlighting Bitcoin's decentralization-security tradeoff
btc_x, btc_y = barycentric_to_cartesian(0.45, 0.45, 0.10)
ax.annotate('Bitcoin:\nD+S optimized',
           xy=(btc_x, btc_y), xytext=(btc_x - 0.25, btc_y + 0.12),
           fontsize=9, fontweight='bold', color=MLORANGE,
           arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=1.5),
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLORANGE, alpha=0.8))

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
