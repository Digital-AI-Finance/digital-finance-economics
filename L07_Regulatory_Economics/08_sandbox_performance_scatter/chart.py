"""Regulatory Sandbox Performance: Efficiency Frontier

# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  Efficiency = Graduation Rate / Cost per Firm (normalized)
  Based on FCA (2023), Cornelli et al. (2020).

Data:
  UK FCA: 50 firms, 80% graduation, $2M cost/firm
  MAS (Singapore): 40 firms, 70% graduation, $1.5M cost/firm
  Abu Dhabi ADGM: 30 firms, 60% graduation, $3M cost/firm
  Hong Kong SFC: 20 firms, 50% graduation, $1M cost/firm
  Australia ASIC: 25 firms, 45% graduation, $0.8M cost/firm

Citation: FCA (2023) - Regulatory Sandbox Annual Report;
          Cornelli et al. (2020) - Fintech and Big Tech Credit
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

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

# --- Sandbox data ---
sandboxes = ['UK FCA', 'MAS\n(Singapore)', 'Abu Dhabi\nADGM', 'Hong Kong\nSFC', 'Australia\nASIC']
firms = np.array([50, 40, 30, 20, 25])
graduation_rate = np.array([0.80, 0.70, 0.60, 0.50, 0.45])
cost_per_firm = np.array([2.0, 1.5, 3.0, 1.0, 0.8])  # $M

# Efficiency metric: graduation rate / cost per firm
efficiency = graduation_rate / cost_per_firm

# Colors by efficiency ranking
colors = [MLBLUE, MLGREEN, MLRED, MLORANGE, MLPURPLE]

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel (a): Scatter plot - Graduation rate vs Cost per firm
for i, (name, f, gr, cpf, eff, col) in enumerate(
        zip(sandboxes, firms, graduation_rate, cost_per_firm, efficiency, colors)):
    ax1.scatter(cpf, gr * 100, s=f * 8, color=col, alpha=0.7,
                edgecolors='black', linewidth=1.5, zorder=5)
    # Label with sandbox name
    offset_x = 0.15 if i != 2 else -0.15
    offset_y = 2 if i != 3 else -4
    ha = 'left' if i != 2 else 'right'
    ax1.annotate(name.replace('\n', ' '), xy=(cpf, gr * 100),
                 xytext=(cpf + offset_x, gr * 100 + offset_y),
                 fontsize=10, fontweight='bold', color=col, ha=ha,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=col, alpha=0.8))

# Efficiency frontier line (connecting efficient sandboxes)
# Sort by cost for frontier
sorted_idx = np.argsort(cost_per_firm)
cpf_sorted = cost_per_firm[sorted_idx]
gr_sorted = graduation_rate[sorted_idx] * 100

# Draw frontier connecting best performers
frontier_idx = [4, 3, 1, 0]  # Australia, HK, MAS, FCA (by cost)
ax1.plot(cost_per_firm[frontier_idx], graduation_rate[frontier_idx] * 100,
         '--', color=MLLAVENDER, lw=2, alpha=0.7, label='Efficiency frontier')

ax1.set_xlabel('Cost per firm ($M)')
ax1.set_ylabel('Graduation rate (%)')
ax1.set_title('(a) Sandbox Performance: Graduation vs Cost')
ax1.legend(loc='lower right', fontsize=10)
ax1.set_xlim(0.3, 3.5)
ax1.set_ylim(30, 90)
ax1.grid(True, alpha=0.3)

# Size legend
ax1.text(0.03, 0.03, 'Bubble size = number of firms\nadmitted to sandbox',
         transform=ax1.transAxes, fontsize=9,
         verticalalignment='bottom',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor=MLORANGE, alpha=0.9))

# Panel (b): Efficiency bar chart (graduation_rate / cost_per_firm)
bar_colors = [MLBLUE, MLGREEN, MLRED, MLORANGE, MLPURPLE]
sorted_eff_idx = np.argsort(efficiency)[::-1]

bar_labels = [sandboxes[i].replace('\n', ' ') for i in sorted_eff_idx]
bar_values = efficiency[sorted_eff_idx]
bar_cols = [bar_colors[i] for i in sorted_eff_idx]
bar_grad = [graduation_rate[i] * 100 for i in sorted_eff_idx]
bar_cost = [cost_per_firm[i] for i in sorted_eff_idx]

bars = ax2.barh(range(len(bar_labels)), bar_values, color=bar_cols, alpha=0.8,
                edgecolor='black', lw=1.2)

# Value labels with decomposition
for i, (bar, val, gr_val, c_val) in enumerate(zip(bars, bar_values, bar_grad, bar_cost)):
    ax2.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
             f'{val:.2f} ({gr_val:.0f}% / ${c_val:.1f}M)',
             ha='left', va='center', fontsize=10, fontweight='bold')

ax2.set_yticks(range(len(bar_labels)))
ax2.set_yticklabels(bar_labels)
ax2.set_xlabel('Efficiency = Graduation Rate / Cost per Firm')
ax2.set_title('(b) Sandbox Efficiency Ranking')
ax2.set_xlim(0, 0.75)
ax2.grid(True, alpha=0.3, axis='x')
ax2.invert_yaxis()

# Insight annotation
ax2.text(0.95, 0.95, 'Australia ASIC: highest efficiency\n(low cost, moderate graduation)\n'
         'Abu Dhabi: lowest efficiency\n(high cost, moderate graduation)',
         transform=ax2.transAxes, fontsize=9,
         verticalalignment='top', ha='right',
         bbox=dict(boxstyle='round', facecolor=MLLAVENDER, alpha=0.3))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
