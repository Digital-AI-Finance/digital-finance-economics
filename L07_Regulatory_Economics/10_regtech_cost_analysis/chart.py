"""RegTech Compliance Cost Analysis: Manual vs Basic vs AI

# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  C_manual(V) = 500,000 + 5V   (high variable, low fixed)
  C_basic(V)  = 1,500,000 + V  (moderate both)
  C_AI(V)     = 3,000,000 + 0.2V (high fixed, low variable)

  Crossover V1: manual = basic => 500K + 5V = 1.5M + V => V1 = 250,000
  Crossover V2: basic = AI => 1.5M + V = 3M + 0.2V => V2 = 1,875,000

  Based on Deloitte RegTech Universe (2023).

Citation: Deloitte (2023) - RegTech Universe Report
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

# --- Cost functions ---
V = np.linspace(0, 5_000_000, 1000)

# Fixed + variable costs
F_manual, m_manual = 500_000, 5
F_basic, m_basic = 1_500_000, 1
F_ai, m_ai = 3_000_000, 0.2

C_manual = F_manual + m_manual * V
C_basic = F_basic + m_basic * V
C_ai = F_ai + m_ai * V

# Crossovers
V1 = (F_basic - F_manual) / (m_manual - m_basic)   # 250,000
V2 = (F_ai - F_basic) / (m_basic - m_ai)           # 1,875,000

# Minimum cost envelope
C_min = np.minimum(np.minimum(C_manual, C_basic), C_ai)

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel (a): Cost curves
ax1.plot(V / 1e6, C_manual / 1e6, color=MLRED, lw=2.5, label=f'Manual: ${F_manual/1e3:.0f}K + ${m_manual}V')
ax1.plot(V / 1e6, C_basic / 1e6, color=MLORANGE, lw=2.5, label=f'Basic RegTech: ${F_basic/1e6:.1f}M + ${m_basic}V')
ax1.plot(V / 1e6, C_ai / 1e6, color=MLGREEN, lw=2.5, label=f'AI RegTech: ${F_ai/1e6:.0f}M + ${m_ai}V')

# Minimum cost envelope
ax1.fill_between(V / 1e6, 0, C_min / 1e6, alpha=0.08, color=MLPURPLE, label='Optimal cost region')

# Crossover points
V1_cost = F_manual + m_manual * V1
V2_cost = F_basic + m_basic * V2

ax1.plot(V1 / 1e6, V1_cost / 1e6, 'D', color=MLPURPLE, ms=12, zorder=5,
         markeredgecolor='black', markeredgewidth=1.5)
ax1.plot(V2 / 1e6, V2_cost / 1e6, 'D', color=MLPURPLE, ms=12, zorder=5,
         markeredgecolor='black', markeredgewidth=1.5)

# Crossover annotations
ax1.annotate(f'$V_1 = {V1/1e3:.0f}K$\nManual = Basic\nCost = ${V1_cost/1e6:.2f}M',
             xy=(V1/1e6, V1_cost/1e6), xytext=(V1/1e6 + 0.5, V1_cost/1e6 + 5),
             fontsize=10, color=MLPURPLE,
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLPURPLE, alpha=0.9))

ax1.annotate(f'$V_2 = {V2/1e6:.3f}M$\nBasic = AI\nCost = ${V2_cost/1e6:.2f}M',
             xy=(V2/1e6, V2_cost/1e6), xytext=(V2/1e6 + 0.5, V2_cost/1e6 + 3),
             fontsize=10, color=MLPURPLE,
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLPURPLE, alpha=0.9))

# Region labels
ax1.text(0.05, 12, 'Manual\ncheapest', fontsize=10, color=MLRED, fontweight='bold',
         ha='center', bbox=dict(boxstyle='round', facecolor='white', edgecolor=MLRED, alpha=0.7))
ax1.text(1.0, 8, 'Basic RegTech\ncheapest', fontsize=10, color=MLORANGE, fontweight='bold',
         ha='center', bbox=dict(boxstyle='round', facecolor='white', edgecolor=MLORANGE, alpha=0.7))
ax1.text(3.5, 6, 'AI RegTech\ncheapest', fontsize=10, color=MLGREEN, fontweight='bold',
         ha='center', bbox=dict(boxstyle='round', facecolor='white', edgecolor=MLGREEN, alpha=0.7))

ax1.set_xlabel('Transaction volume V (millions)')
ax1.set_ylabel('Total compliance cost ($M)')
ax1.set_title('(a) Compliance Cost by Technology Choice')
ax1.legend(loc='upper left', fontsize=9)
ax1.set_xlim(0, 5)
ax1.set_ylim(0, 28)
ax1.grid(True, alpha=0.3)

# Panel (b): Cost savings and ROI
volumes = np.array([100_000, 250_000, 500_000, 1_000_000, 1_875_000, 3_000_000, 5_000_000])
vol_labels = ['100K', '250K', '500K', '1M', '1.875M', '3M', '5M']

# Calculate savings from optimal choice vs manual
savings_basic = (F_manual + m_manual * volumes) - (F_basic + m_basic * volumes)
savings_ai = (F_manual + m_manual * volumes) - (F_ai + m_ai * volumes)

# Best savings
best_savings = np.maximum(savings_basic, savings_ai)
best_labels = ['Basic' if sb > sa else 'AI' for sb, sa in zip(savings_basic, savings_ai)]

bar_colors = [MLORANGE if l == 'Basic' else MLGREEN for l in best_labels]

x_pos = np.arange(len(volumes))
bars = ax2.bar(x_pos, best_savings / 1e6, color=bar_colors, alpha=0.8,
               edgecolor='black', lw=1.2)

# Value labels
for bar, val, label in zip(bars, best_savings, best_labels):
    color = 'black' if val > 0 else MLRED
    ax2.text(bar.get_x() + bar.get_width()/2,
             max(bar.get_height(), 0) + 0.3,
             f'${val/1e6:.1f}M\n({label})',
             ha='center', va='bottom', fontsize=9, fontweight='bold', color=color)

ax2.axhline(0, color='black', lw=1)
ax2.set_xlabel('Transaction volume V')
ax2.set_ylabel('Savings vs manual process ($M)')
ax2.set_title('(b) Cost Savings from RegTech Adoption')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(vol_labels, fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')

# Insight
ax2.text(0.03, 0.97, 'Below V = 250K: manual is cheapest\n'
         'V = 250K - 1.875M: basic RegTech wins\n'
         'Above V = 1.875M: AI RegTech wins\n'
         'Break-even shifts with technology costs',
         transform=ax2.transAxes, fontsize=9,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor=MLLAVENDER, alpha=0.3))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
