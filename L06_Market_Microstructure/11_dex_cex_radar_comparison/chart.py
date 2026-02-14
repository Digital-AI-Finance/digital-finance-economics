"""DEX vs CEX Radar Comparison
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  6 dimensions: spread, depth, speed, transparency, censorship_resistance, capital_efficiency
  DEX scores: [4, 3, 5, 9, 9, 4] (out of 10)
  CEX scores: [8, 8, 9, 3, 2, 7] (out of 10)
  Based on Barbon & Ranaldo (2022), empirical comparison of venue quality.

  Panel (a): Radar chart overlay. Panel (b): Side-by-side grouped bars.
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

# --- Data ---
categories = ['Spread\n(tightness)', 'Depth\n(liquidity)', 'Speed\n(latency)',
              'Transparency', 'Censorship\nResistance', 'Capital\nEfficiency']
categories_short = ['Spread', 'Depth', 'Speed', 'Transparency', 'Cens. Resist.', 'Cap. Eff.']

dex_scores = np.array([4, 3, 5, 9, 9, 4])
cex_scores = np.array([8, 8, 9, 3, 2, 7])

N = len(categories)

fig = plt.figure(figsize=(14, 6))

# --- Panel (a): Radar chart ---
ax1 = fig.add_subplot(121, polar=True)

angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
# Close the polygon
dex_vals = np.concatenate([dex_scores, [dex_scores[0]]])
cex_vals = np.concatenate([cex_scores, [cex_scores[0]]])
angles_plot = angles + [angles[0]]

ax1.fill(angles_plot, dex_vals, color=MLGREEN, alpha=0.15)
ax1.plot(angles_plot, dex_vals, color=MLGREEN, linewidth=2.5, marker='o',
         markersize=8, label='DEX (Uniswap)')

ax1.fill(angles_plot, cex_vals, color=MLBLUE, alpha=0.15)
ax1.plot(angles_plot, cex_vals, color=MLBLUE, linewidth=2.5, marker='s',
         markersize=8, label='CEX (Binance)')

ax1.set_xticks(angles)
ax1.set_xticklabels(categories, fontsize=10)
ax1.set_ylim(0, 10)
ax1.set_yticks([2, 4, 6, 8, 10])
ax1.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=9)
ax1.set_title('(a) DEX vs CEX: Quality Radar', fontweight='bold', pad=20, fontsize=14)
ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11, framealpha=0.95)

# --- Panel (b): Side-by-side bars ---
ax2 = fig.add_subplot(122)

x_pos = np.arange(N)
width = 0.35

bars_dex = ax2.bar(x_pos - width / 2, dex_scores, width, label='DEX (Uniswap)',
                   color=MLGREEN, edgecolor='black', linewidth=1.2, alpha=0.85)
bars_cex = ax2.bar(x_pos + width / 2, cex_scores, width, label='CEX (Binance)',
                   color=MLBLUE, edgecolor='black', linewidth=1.2, alpha=0.85)

# Value labels
for bar, val in zip(bars_dex, dex_scores):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
             str(val), ha='center', va='bottom', fontsize=11, fontweight='bold', color=MLGREEN)

for bar, val in zip(bars_cex, cex_scores):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
             str(val), ha='center', va='bottom', fontsize=11, fontweight='bold', color=MLBLUE)

# Highlight where DEX wins
for i in range(N):
    if dex_scores[i] > cex_scores[i]:
        ax2.annotate('DEX wins', xy=(i, max(dex_scores[i], cex_scores[i]) + 0.7),
                     fontsize=8, ha='center', color=MLGREEN, fontweight='bold')
    elif cex_scores[i] > dex_scores[i]:
        ax2.annotate('CEX wins', xy=(i, max(dex_scores[i], cex_scores[i]) + 0.7),
                     fontsize=8, ha='center', color=MLBLUE, fontweight='bold')

ax2.set_xticks(x_pos)
ax2.set_xticklabels(categories_short, rotation=25, ha='right', fontsize=11)
ax2.set_ylabel('Score (0-10)')
ax2.set_title('(b) Dimension-by-Dimension Comparison', fontweight='bold')
ax2.set_ylim(0, 12)
ax2.legend(loc='upper center', framealpha=0.95, fontsize=11)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Summary annotation
dex_total = dex_scores.sum()
cex_total = cex_scores.sum()
ax2.text(0.98, 0.02, f'Total scores:\n'
         f'DEX: {dex_total}/60\n'
         f'CEX: {cex_total}/60\n\n'
         'DEX excels: transparency,\ncensorship resistance\n'
         'CEX excels: spread, depth,\nspeed, capital efficiency',
         transform=ax2.transAxes, fontsize=9, va='bottom', ha='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

fig.suptitle('DEX vs CEX Market Quality: Multi-Dimensional Comparison\n'
             'Barbon & Ranaldo (2022): Each venue type has distinct comparative advantages',
             fontsize=15, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
