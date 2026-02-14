r"""Akerlof Lemons Model Applied to Crypto Markets

# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  Akerlof: $q \sim U[0,1]$. Based on Akerlof (1970).
  Without regulation: sellers with $q > p$ exit, buyers expect $E[q|q < p] = p/2$
  Market unraveling: only lowest-quality projects survive
  With quality floor $q_{min}$: $E[q] = (1 + q_{min})/2$, Volume $= 1 - q_{min}$

Citation: Akerlof (1970) - The Market for Lemons
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

# --- Akerlof unraveling dynamics ---
# Iterative market collapse: buyers offer p, sellers with q>p leave
# New expected quality E[q|q<p] = p/2, so new offer = p/2, repeat
rounds = 8
prices = [1.0]  # Initial: buyers willing to pay for average quality
avg_qualities = [0.5]  # E[q] = 0.5 when q~U[0,1]
volumes = [1.0]  # Full market

p = 1.0
for i in range(rounds - 1):
    # Sellers with q > p exit; remaining q ~ U[0, p]
    new_avg = p / 2
    new_volume = p  # fraction of sellers remaining
    p = new_avg * 2 * 0.9  # buyers discount slightly below fair value
    p = max(p, 0.01)
    prices.append(p)
    avg_qualities.append(new_avg)
    volumes.append(new_volume)

# --- Quality floor regulatory intervention ---
q_min_values = np.array([0.0, 0.2, 0.4, 0.6])
avg_quality_floor = (1 + q_min_values) / 2
volume_floor = 1 - q_min_values
total_value = avg_quality_floor * volume_floor  # quality * volume

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel (a): Unraveling dynamics
rounds_x = np.arange(1, rounds + 1)
ax1_twin = ax1.twinx()

line1, = ax1.plot(rounds_x, avg_qualities, 'o-', color=MLRED, lw=2.5, ms=8,
                  label='Average quality $E[q]$', zorder=5)
line2, = ax1.plot(rounds_x, prices, 's--', color=MLBLUE, lw=2, ms=7,
                  label='Market price $p$', zorder=4)
line3, = ax1_twin.plot(rounds_x, volumes, '^-', color=MLGREEN, lw=2, ms=7,
                       label='Market volume (fraction)')

ax1.set_xlabel('Trading round')
ax1.set_ylabel('Quality / Price', color=MLRED)
ax1_twin.set_ylabel('Volume (fraction of sellers)', color=MLGREEN)
ax1.set_title('(a) Akerlof Unraveling in Crypto Markets')
ax1.set_ylim(0, 1.1)
ax1_twin.set_ylim(0, 1.1)

# Combine legends
lines = [line1, line2, line3]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center right', fontsize=10)

ax1.grid(True, alpha=0.3)

# Annotate unraveling
ax1.annotate('Market collapse:\nonly lemons remain',
             xy=(rounds, avg_qualities[-1]), xytext=(rounds - 3, 0.7),
             fontsize=10, color=MLRED,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLRED, alpha=0.9))

# ICO fact
ax1.text(0.03, 0.97, 'ICO market 2017-2018:\n80% of projects were scams\n(Dowlat & Hodapp, 2018)',
         transform=ax1.transAxes, fontsize=9, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor=MLORANGE, alpha=0.9))

# Panel (b): Regulatory quality floor intervention
x_pos = np.arange(len(q_min_values))
width = 0.35

bars1 = ax2.bar(x_pos - width/2, avg_quality_floor, width, color=MLBLUE, alpha=0.8,
                edgecolor='black', lw=1, label='Avg quality $(1+q_{min})/2$')
bars2 = ax2.bar(x_pos + width/2, volume_floor, width, color=MLORANGE, alpha=0.8,
                edgecolor='black', lw=1, label='Volume $1 - q_{min}$')

# Value line on twin axis
ax2_twin = ax2.twinx()
ax2_twin.plot(x_pos, total_value, 'D-', color=MLPURPLE, lw=2.5, ms=10,
              markeredgecolor='black', markeredgewidth=1, label='Total value (Q x V)', zorder=5)

# Value labels on bars
for bar, val in zip(bars1, avg_quality_floor):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold', color=MLBLUE)
for bar, val in zip(bars2, volume_floor):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold', color=MLORANGE)

ax2.set_xlabel('Quality floor $q_{min}$ (minimum standard)')
ax2.set_ylabel('Quality / Volume')
ax2_twin.set_ylabel('Total market value', color=MLPURPLE)
ax2.set_title('(b) Regulatory Quality Floor: Quality vs Volume Trade-off')
ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'$q_{{min}}={v:.1f}$' for v in q_min_values])
ax2.set_ylim(0, 1.15)
ax2_twin.set_ylim(0, 0.7)
ax2.grid(True, alpha=0.3, axis='y')

# Combined legend
lines2, labels2 = ax2.get_legend_handles_labels()
lines2t, labels2t = ax2_twin.get_legend_handles_labels()
ax2.legend(lines2 + lines2t, labels2 + labels2t, loc='upper right', fontsize=9)

# Optimal annotation
optimal_idx = np.argmax(total_value)
ax2.annotate(f'Optimal: $q_{{min}}={q_min_values[optimal_idx]:.1f}$\nmax total value = {total_value[optimal_idx]:.2f}',
             xy=(x_pos[optimal_idx], avg_quality_floor[optimal_idx]),
             xytext=(x_pos[optimal_idx] + 0.8, 0.95),
             fontsize=10, color=MLPURPLE,
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLPURPLE, alpha=0.9))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
