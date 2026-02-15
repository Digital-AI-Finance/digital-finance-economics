r"""Barter Cost Reduction: Money as Transaction Cost Innovation

Multi-panel override: comparative statics requires simultaneous visibility

Panel (a): Number of exchange rates under barter vs money as goods increase.
Panel (b): Transaction cost savings from adopting money.

Economic Model:
$P_{barter}(n) = \frac{n(n-1)}{2}$, $P_{money}(n) = n-1$.
Transaction cost: $TC = c \cdot P(n)$.
Based on Kiyotaki \& Wright (1989), Jevons (1875).
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 11,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Parameters
c_b = 5.0   # cost per barter trade ($/trade)
c_m = 0.50  # cost per money trade ($/trade)
n = np.arange(2, 101)

# Models
P_barter = n * (n - 1) / 2        # barter exchange rates
P_money = n - 1                    # money prices
TC_barter = c_b * P_barter        # total barter cost
TC_money = c_m * P_money           # total money cost
TC_savings = TC_barter - TC_money  # savings from money

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Exchange rates ---
ax1.plot(n, P_barter, color=MLRED, linewidth=2.5, label='Barter: $n(n-1)/2$')
ax1.plot(n, P_money, color=MLBLUE, linewidth=2.5, label='Money: $n-1$')

# Annotation at n=50 where divergence is dramatic
n_mark = 50
P_b_50 = n_mark * (n_mark - 1) / 2  # 1225
P_m_50 = n_mark - 1                  # 49
ax1.annotate(f'n=50: {int(P_b_50):,} barter rates\nvs {int(P_m_50)} money prices',
             xy=(n_mark, P_b_50), xytext=(25, 3200),
             fontsize=10, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                       edgecolor=MLRED, alpha=0.9))
ax1.plot(n_mark, P_b_50, 'o', color=MLRED, markersize=8, zorder=5)
ax1.plot(n_mark, P_m_50, 'o', color=MLBLUE, markersize=8, zorder=5)

ax1.set_xlabel('Number of Goods ($n$)', fontweight='bold')
ax1.set_ylabel('Number of Exchange Rates / Prices', fontweight='bold')
ax1.set_title('(a) Exchange Rate Complexity:\nBarter vs Money', fontweight='bold', color=MLPURPLE)
ax1.legend(loc='upper left', framealpha=0.9)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(2, 100)
ax1.set_ylim(0, 5200)

# --- Panel (b): Transaction cost savings ---
ax2.fill_between(n, 0, TC_savings, color=MLGREEN, alpha=0.3,
                 label='TC savings from money')
ax2.plot(n, TC_barter, color=MLRED, linewidth=2, linestyle='--',
         label=f'Barter TC ($c_b$=\\${c_b:.1f}/trade)')
ax2.plot(n, TC_money, color=MLBLUE, linewidth=2, linestyle='--',
         label=f'Money TC ($c_m$=\\${c_m:.2f}/trade)')
ax2.plot(n, TC_savings, color=MLGREEN, linewidth=2.5,
         label='Savings = Barter TC $-$ Money TC')

ax2.set_xlabel('Number of Goods ($n$)', fontweight='bold')
ax2.set_ylabel('Transaction Cost (\\$)', fontweight='bold')
ax2.set_title('(b) Transaction Cost Savings\nfrom Adopting Money', fontweight='bold', color=MLPURPLE)
ax2.legend(loc='upper left', framealpha=0.9, fontsize=10)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(2, 100)

fig.suptitle('Barter Inefficiency and Money as Transaction Cost Innovation\n'
             'Kiyotaki & Wright (1989), Jevons (1875)',
             fontweight='bold', fontsize=14, color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
