r"""Seigniorage Distribution Across Money Types
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
    Seigniorage: $S = \frac{dM}{dt} \cdot \frac{1}{P}$.
    CB \$50B, Banks \$30B, Stablecoin \$8B, Miners \$12B.
    Based on seigniorage theory.

    As fraction of money supply managed:
    CB = 0.25% (of ~$20T M2), Banks = 0.15% (of ~$20T deposits),
    Stablecoin = 6% (of ~$130B market cap), Miners = 1.5% (of ~$800B BTC market cap).

    Key insight: stablecoin issuers earn disproportionately high seigniorage
    rates relative to money supply managed, because they invest reserves
    at market rates while paying holders 0%.

Citation: Seigniorage theory (Friedman 1971, Mundell 1971).
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 10,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# --- Parameters ---
entities = ['Central\nBanks', 'Commercial\nBanks', 'Stablecoin\nIssuers', 'Crypto\nMiners']
absolute_bn = [50, 30, 8, 12]  # $ billions
pct_of_supply = [0.25, 0.15, 6.0, 1.5]  # % of money supply managed
colors = [MLBLUE, MLLAVENDER, MLGREEN, MLORANGE]
colors_pct = [MLBLUE, MLLAVENDER, MLGREEN, MLORANGE]

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# === Panel (a): Absolute Seigniorage ($B) ===
x_pos = np.arange(len(entities))
bars1 = ax1.bar(x_pos, absolute_bn, color=colors, edgecolor='white',
                linewidth=1.5, alpha=0.85, width=0.55)

# Value labels
for i, val in enumerate(absolute_bn):
    ax1.text(i, val + 1.5, f'${val}B', ha='center', fontweight='bold',
             fontsize=12, color=colors[i])

# Total annotation
total = sum(absolute_bn)
ax1.axhline(y=total, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax1.text(3.3, total + 1, f'Total: ${total}B', fontsize=9, color='gray',
         ha='right', fontweight='bold')

# Highlight stablecoin profitability
ax1.annotate('Tether alone:\n~$6.2B (2023)',
             xy=(2, 8), xytext=(2.8, 30),
             fontsize=9, fontweight='bold', color=MLGREEN,
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=MLGREEN, alpha=0.9))

# Formula
ax1.text(0.03, 0.97, '$S = \\frac{dM}{dt} \\cdot \\frac{1}{P}$',
         transform=ax1.transAxes, fontsize=11,
         verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=MLLAVENDER, alpha=0.3))

ax1.set_xticks(x_pos)
ax1.set_xticklabels(entities, fontweight='bold')
ax1.set_ylabel('Annual Seigniorage ($B)', fontweight='bold')
ax1.set_title('(a) Absolute Seigniorage Revenue', fontweight='bold', color=MLPURPLE)
ax1.grid(True, alpha=0.3, axis='y')
ax1.set_ylim(0, 65)

# === Panel (b): Seigniorage as % of Money Supply Managed ===
bars2 = ax2.bar(x_pos, pct_of_supply, color=colors_pct, edgecolor='white',
                linewidth=1.5, alpha=0.85, width=0.55)

# Value labels
for i, val in enumerate(pct_of_supply):
    ax2.text(i, val + 0.15, f'{val:.2f}%' if val < 1 else f'{val:.1f}%',
             ha='center', fontweight='bold', fontsize=12, color=colors_pct[i])

# Highlight disproportionate stablecoin rate
ax2.annotate('24x higher rate\nthan central banks!',
             xy=(2, 6.0), xytext=(0.8, 5.5),
             fontsize=9, fontweight='bold', color=MLRED,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=MLRED, alpha=0.9))

# Explanation
ax2.text(0.97, 0.97,
         'Stablecoin issuers invest\nreserves at 4-5% but pay\nholders 0% = pure profit',
         transform=ax2.transAxes, fontsize=9,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                  edgecolor='gray', alpha=0.9))

# Show money supply bases
supply_labels = ['~$20T M2', '~$20T deposits', '~$130B mcap', '~$800B mcap']
for i, label in enumerate(supply_labels):
    ax2.text(i, -0.4, label, ha='center', fontsize=8, color='gray', style='italic')

ax2.set_xticks(x_pos)
ax2.set_xticklabels(entities, fontweight='bold')
ax2.set_ylabel('Seigniorage Rate (% of supply)', fontweight='bold')
ax2.set_title('(b) Seigniorage as % of Money Managed', fontweight='bold', color=MLPURPLE)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim(-0.8, 8)

fig.suptitle('Seigniorage Distribution: Who Profits from Money Creation?',
             fontsize=14, fontweight='bold', color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Seigniorage distribution chart saved to chart.pdf and chart.png")
