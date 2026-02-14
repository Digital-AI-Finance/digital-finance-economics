"""FATF Greylisting Coordination Game Tree

# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  Stage game: (C,C)=(5,5), (D,C)=(7,3), (C,D)=(3,7), (D,D)=(2,2)
  Detection probability p=0.8
  Expected defect payoff: E[D] = (1-p)*7 + p*1 = 0.2*7 + 0.8*1 = 2.2 < 5
  Cooperation sustained when discount factor delta_g > 0.4 via trigger strategies

  Based on FATF Mutual Evaluation methodology, Masciandaro (2022).
  NO networkx. Game tree drawn with matplotlib patches only.

Citation: FATF (2023) - Methodology for Assessing Compliance;
          Masciandaro (2022) - The Governance of Financial Supervision
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (14, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# --- Game parameters ---
p_detect = 0.8  # Detection probability
payoffs = {
    'CC': (5, 5),   # Both comply
    'DC_caught': (1, 4),  # Defect, caught (greylisted)
    'DC_escaped': (7, 3),  # Defect, not caught
    'DD': (2, 2),   # Both defect
}

# Expected payoff from defection
E_defect = (1 - p_detect) * payoffs['DC_escaped'][0] + p_detect * payoffs['DC_caught'][0]
E_comply = payoffs['CC'][0]

# Trigger strategy threshold: delta_g > (7-5)/(7-2) = 0.4
delta_threshold = (payoffs['DC_escaped'][0] - payoffs['CC'][0]) / \
                  (payoffs['DC_escaped'][0] - payoffs['DD'][0])

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel (a): Game tree with matplotlib
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title('(a) FATF Compliance Game Tree', fontsize=16, pad=15)

# Root node: Country decision
root = (5, 9)
ax1.add_patch(FancyBboxPatch((root[0]-0.8, root[1]-0.35), 1.6, 0.7,
              boxstyle='round,pad=0.1', facecolor=MLBLUE, edgecolor='black', lw=2, alpha=0.8))
ax1.text(root[0], root[1], 'Country', ha='center', va='center',
         fontsize=12, fontweight='bold', color='white')

# Comply branch
comply_node = (2.5, 6.5)
ax1.annotate('', xy=comply_node, xytext=root,
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=2.5))
ax1.text(3.2, 8.0, 'Comply', fontsize=11, color=MLGREEN, fontweight='bold')

ax1.add_patch(FancyBboxPatch((comply_node[0]-0.8, comply_node[1]-0.35), 1.6, 0.7,
              boxstyle='round,pad=0.1', facecolor=MLGREEN, edgecolor='black', lw=2, alpha=0.8))
ax1.text(comply_node[0], comply_node[1], 'FATF', ha='center', va='center',
         fontsize=12, fontweight='bold', color='white')

# Comply outcome
comply_payoff = (2.5, 4.0)
ax1.annotate('', xy=comply_payoff, xytext=comply_node,
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=2))
ax1.add_patch(FancyBboxPatch((comply_payoff[0]-1.2, comply_payoff[1]-0.6), 2.4, 1.2,
              boxstyle='round,pad=0.1', facecolor='#E8F5E9', edgecolor=MLGREEN, lw=2))
ax1.text(comply_payoff[0], comply_payoff[1] + 0.2, '(5, 5)', ha='center', va='center',
         fontsize=14, fontweight='bold', color=MLGREEN)
ax1.text(comply_payoff[0], comply_payoff[1] - 0.2, 'Cooperation', ha='center', va='center',
         fontsize=9, color='gray')

# Defect branch
defect_node = (7.5, 6.5)
ax1.annotate('', xy=defect_node, xytext=root,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=2.5))
ax1.text(7.0, 8.0, 'Defect', fontsize=11, color=MLRED, fontweight='bold')

ax1.add_patch(FancyBboxPatch((defect_node[0]-0.8, defect_node[1]-0.35), 1.6, 0.7,
              boxstyle='round,pad=0.1', facecolor=MLORANGE, edgecolor='black', lw=2, alpha=0.8))
ax1.text(defect_node[0], defect_node[1], 'FATF\nDetects?', ha='center', va='center',
         fontsize=10, fontweight='bold', color='white')

# Detected (p=0.8)
detected_payoff = (6.0, 4.0)
ax1.annotate('', xy=detected_payoff, xytext=defect_node,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=2))
ax1.text(6.2, 5.6, f'Detected\np = {p_detect:.1f}', fontsize=10, color=MLRED, fontweight='bold')

ax1.add_patch(FancyBboxPatch((detected_payoff[0]-1.2, detected_payoff[1]-0.6), 2.4, 1.2,
              boxstyle='round,pad=0.1', facecolor='#FFEBEE', edgecolor=MLRED, lw=2))
ax1.text(detected_payoff[0], detected_payoff[1] + 0.2, '(1, 4)', ha='center', va='center',
         fontsize=14, fontweight='bold', color=MLRED)
ax1.text(detected_payoff[0], detected_payoff[1] - 0.2, 'Greylisted', ha='center', va='center',
         fontsize=9, color='gray')

# Not detected (p=0.2)
escaped_payoff = (9.0, 4.0)
ax1.annotate('', xy=escaped_payoff, xytext=defect_node,
             arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=2))
ax1.text(8.8, 5.6, f'Escaped\np = {1-p_detect:.1f}', fontsize=10, color=MLORANGE, fontweight='bold')

ax1.add_patch(FancyBboxPatch((escaped_payoff[0]-1.2, escaped_payoff[1]-0.6), 2.4, 1.2,
              boxstyle='round,pad=0.1', facecolor='#FFF3E0', edgecolor=MLORANGE, lw=2))
ax1.text(escaped_payoff[0], escaped_payoff[1] + 0.2, '(7, 3)', ha='center', va='center',
         fontsize=14, fontweight='bold', color=MLORANGE)
ax1.text(escaped_payoff[0], escaped_payoff[1] - 0.2, 'Free-riding', ha='center', va='center',
         fontsize=9, color='gray')

# Expected value annotation
ax1.text(5, 1.8, f'Expected defect payoff:\n'
         f'$E[D] = {1-p_detect:.1f} \\times 7 + {p_detect:.1f} \\times 1 = {E_defect:.1f}$\n'
         f'Comply payoff = {E_comply:.0f}\n'
         f'Since ${E_defect:.1f} < {E_comply:.0f}$: compliance is rational',
         ha='center', va='center', fontsize=11,
         bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', edgecolor=MLPURPLE, lw=2, alpha=0.95))

# Panel (b): Expected payoff bars and discount factor analysis
strategies = ['Comply', 'Defect\n(Expected)']
payoff_values = [E_comply, E_defect]
bar_colors = [MLGREEN, MLRED]

bars = ax2.bar(strategies, payoff_values, color=bar_colors, alpha=0.8,
               edgecolor='black', lw=2, width=0.5)

# Value labels
for bar, val in zip(bars, payoff_values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
             f'{val:.1f}', ha='center', va='bottom', fontsize=16, fontweight='bold')

ax2.set_ylabel('Expected payoff')
ax2.set_title('(b) Expected Payoffs and Cooperation Threshold', fontsize=14)
ax2.set_ylim(0, 7)
ax2.grid(True, alpha=0.3, axis='y')

# Add discount factor analysis
ax2_inset = ax2.inset_axes([0.55, 0.35, 0.40, 0.55])
delta_range = np.linspace(0, 1, 100)

# Payoff from cooperating forever: 5 / (1 - delta)
# Payoff from deviating: 7 + delta * 2 / (1 - delta)  (one-shot deviate, then punished to DD)
V_coop = E_comply / (1 - delta_range + 1e-10)
V_deviate = payoffs['DC_escaped'][0] + delta_range * payoffs['DD'][0] / (1 - delta_range + 1e-10)

# Avoid division issues near delta=1
valid = delta_range < 0.95
ax2_inset.plot(delta_range[valid], V_coop[valid], color=MLGREEN, lw=2, label='Cooperate')
ax2_inset.plot(delta_range[valid], V_deviate[valid], color=MLRED, lw=2, label='Deviate')
ax2_inset.axvline(delta_threshold, color=MLPURPLE, ls='--', lw=2, alpha=0.7)
ax2_inset.text(delta_threshold + 0.03, ax2_inset.get_ylim()[0] + 5,
               f'$\\delta_g^* = {delta_threshold:.1f}$',
               fontsize=10, color=MLPURPLE, fontweight='bold')
ax2_inset.set_xlabel('Discount factor $\\delta_g$', fontsize=10)
ax2_inset.set_ylabel('Total payoff', fontsize=10)
ax2_inset.set_title('Trigger strategy', fontsize=11)
ax2_inset.legend(fontsize=8, loc='upper left')
ax2_inset.grid(True, alpha=0.3)
ax2_inset.tick_params(labelsize=9)

# Key insight
ax2.text(0.02, 0.97, f'With detection p = {p_detect}:\n'
         f'Defection yields {E_defect:.1f} < {E_comply:.0f}\n'
         f'Cooperation rational even\n'
         f'without repeated game\n'
         f'$\\delta_g > {delta_threshold:.1f}$ sustains via\n'
         f'trigger strategies',
         transform=ax2.transAxes, fontsize=9,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor=MLLAVENDER, alpha=0.3))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
