"""Financial Inclusion Frontier: Production Possibility Analysis

Cost-inclusion tradeoff with CBDC technology shift.
Theory: Standard microeconomic production possibility frontier.
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

# PPF Model: Inclusion = f(Cost) with diminishing returns
# Traditional Banking PPF (inner frontier)
cost_trad = np.linspace(0, 100, 100)
# Concave function: sqrt to show diminishing returns
inclusion_trad = 70 * np.sqrt(cost_trad / 100)

# CBDC Technology PPF (outer frontier - shifted out)
cost_cbdc = np.linspace(0, 100, 100)
# Same functional form but higher multiplier (technology improvement)
inclusion_cbdc = 95 * np.sqrt(cost_cbdc / 100)

# Efficiency Points
# Point A: Current allocation (inefficient - inside frontier)
point_a = (40, 35)
# Point B: Allocatively efficient (on traditional frontier)
point_b = (60, 70 * np.sqrt(60 / 100))
# Point C: After CBDC adoption (on new frontier)
point_c = (60, 95 * np.sqrt(60 / 100))

# Plot
fig, ax = plt.subplots()

# Plot PPF curves
ax.plot(cost_trad, inclusion_trad, '--', color=MLBLUE, linewidth=2.5,
        label='Traditional Banking PPF', alpha=0.8)
ax.plot(cost_cbdc, inclusion_cbdc, '-', color=MLPURPLE, linewidth=3,
        label='CBDC Technology PPF')

# Fill area between frontiers to show technology gain
ax.fill_between(cost_cbdc, inclusion_cbdc, inclusion_trad,
                alpha=0.15, color=MLLAVENDER)

# Plot efficiency points
ax.scatter(*point_a, s=200, color=MLRED, edgecolors='black',
          linewidths=2, zorder=5, marker='o', label='Point A: Inefficient')
ax.scatter(*point_b, s=200, color=MLORANGE, edgecolors='black',
          linewidths=2, zorder=5, marker='s', label='Point B: Efficient (Traditional)')
ax.scatter(*point_c, s=200, color=MLGREEN, edgecolors='black',
          linewidths=2, zorder=5, marker='^', label='Point C: Efficient (CBDC)')

# Annotate points
ax.annotate('A\n(Underutilized)', xy=point_a, xytext=(point_a[0]-15, point_a[1]+8),
           fontsize=12, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                    edgecolor=MLRED, alpha=0.95))

ax.annotate('B\n(On Frontier)', xy=point_b, xytext=(point_b[0]-15, point_b[1]-15),
           fontsize=12, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                    edgecolor=MLORANGE, alpha=0.95))

ax.annotate('C\n(CBDC Gains)', xy=point_c, xytext=(point_c[0]+15, point_c[1]+5),
           fontsize=12, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                    edgecolor=MLGREEN, alpha=0.95))

# Arrow showing technology shift
ax.annotate('', xy=point_c, xytext=point_b,
           arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=3,
                          mutation_scale=20))
ax.text((point_b[0] + point_c[0])/2 + 10, (point_b[1] + point_c[1])/2,
       'Technology\nShift', fontsize=11, fontweight='bold',
       color=MLGREEN, ha='center',
       bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                edgecolor=MLGREEN, alpha=0.9))

# Show opportunity cost region
ax.annotate('', xy=(80, 95 * np.sqrt(80 / 100)), xytext=(80, 70 * np.sqrt(80 / 100)),
           arrowprops=dict(arrowstyle='<->', color=MLPURPLE, lw=2))
ax.text(85, (95 * np.sqrt(80 / 100) + 70 * np.sqrt(80 / 100))/2,
       'Inclusion\nGain', fontsize=10, fontweight='bold',
       color=MLPURPLE, ha='left')

# Formatting
ax.set_xlabel('Cost Efficiency (Lower = Better)', fontweight='bold')
ax.set_ylabel('Financial Inclusion (%)', fontweight='bold')
ax.set_title('Financial Inclusion Production Possibility Frontier',
            fontweight='bold', pad=20)
ax.set_xlim(0, 105)
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='lower right', framealpha=0.95, fontsize=11)

# Invert x-axis so lower cost is better (right side)
ax.invert_xaxis()

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
