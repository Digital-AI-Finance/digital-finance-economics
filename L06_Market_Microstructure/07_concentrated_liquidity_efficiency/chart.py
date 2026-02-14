r"""Concentrated Liquidity Efficiency: Uniswap v3
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  Capital efficiency multiplier: $\eta = \frac{1}{\sqrt{1+r} - \sqrt{1-r}}$
  where r = half-width of price range as fraction of current price.
  Concentrated IL: $IL_{conc} = IL_{v2} \times \eta$
  Based on Adams et al. (2021), Uniswap v3 whitepaper.

  Full-range (v2): liquidity spread across [0, inf).
  Concentrated (v3): liquidity focused in [P_low, P_high].
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

# --- Parameters ---
P_current = 1800  # USDC/ETH
ranges_pct = np.array([1, 2, 5, 10, 20, 50, 100])  # half-width percent
r_vals = ranges_pct / 100.0

# Capital efficiency: eta = 1 / (sqrt(1+r) - sqrt(1-r))
# For r < 1 only; r=100% means full range which is eta=1 by convention
eta = np.zeros_like(r_vals, dtype=float)
for i, r in enumerate(r_vals):
    if r >= 1.0:
        eta[i] = 1.0  # full range = Uniswap v2
    else:
        eta[i] = 1.0 / (np.sqrt(1 + r) - np.sqrt(1 - r))

# Price bounds
P_low = P_current * (1 - r_vals)
P_high = P_current * (1 + r_vals)

# Fee earning comparison: concentrated earns eta times more per dollar
# Assume $100K deposited, 0.3% fee tier, V/TVL = 2.0 daily
deposit = 100_000
fee_rate = 0.003
daily_vol_tvl = 2.0

# Daily fee income per $100K: fee_rate * V/TVL * deposit * eta_effective
# But concentrated only earns when price is in range
# Probability price stays in range (assume normal, sigma=2% daily for ETH)
sigma_daily = 0.02
prob_in_range = np.zeros_like(r_vals, dtype=float)
for i, r in enumerate(r_vals):
    if r >= 1.0:
        prob_in_range[i] = 1.0
    else:
        from scipy.stats import norm
        prob_in_range[i] = norm.cdf(r / sigma_daily) - norm.cdf(-r / sigma_daily)

expected_fee_daily = fee_rate * daily_vol_tvl * deposit * eta * prob_in_range
full_range_fee = fee_rate * daily_vol_tvl * deposit  # eta=1, prob=1

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Capital efficiency multiplier ---
bar_colors = [MLRED if e > 10 else MLORANGE if e > 3 else MLBLUE for e in eta]
bars = ax1.bar([f'+/-{p}%' for p in ranges_pct], eta, color=bar_colors,
               edgecolor='black', linewidth=1.2, alpha=0.85)

for bar, e, pir in zip(bars, eta, prob_in_range):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             f'{e:.1f}x', ha='center', va='bottom', fontsize=11, fontweight='bold')
    # Show prob in range below the bar
    ax1.text(bar.get_x() + bar.get_width() / 2, 0.5,
             f'P(in)={pir:.0%}', ha='center', va='bottom', fontsize=8, color='white',
             fontweight='bold')

ax1.set_xlabel('Price Range (half-width %)')
ax1.set_ylabel('Capital Efficiency Multiplier (eta)')
ax1.set_title('(a) Capital Efficiency by Range Width', fontweight='bold')
ax1.set_yscale('log')
ax1.set_ylim(0.5, max(eta) * 2)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Annotation
ax1.text(0.02, 0.98, r'$\eta = \frac{1}{\sqrt{1+r} - \sqrt{1-r}}$' + '\n\n' +
         'Narrower range = higher efficiency\n'
         'but higher out-of-range risk',
         transform=ax1.transAxes, fontsize=10, va='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# --- Panel (b): Expected daily fee income ---
ax2.bar([f'+/-{p}%' for p in ranges_pct], expected_fee_daily,
        color=MLGREEN, edgecolor='black', linewidth=1.2, alpha=0.85, label='Concentrated')
ax2.axhline(y=full_range_fee, color=MLPURPLE, linestyle='--', linewidth=2,
            label=f'Full range (v2): ${full_range_fee:,.0f}')

for i, (fee, e) in enumerate(zip(expected_fee_daily, eta)):
    improvement = fee / full_range_fee
    ax2.text(i, fee + 10, f'{improvement:.1f}x', ha='center', fontsize=10,
             fontweight='bold', color=MLPURPLE)

ax2.set_xlabel('Price Range (half-width %)')
ax2.set_ylabel('Expected Daily Fee Income ($)')
ax2.set_title('(b) Fee Income: $100K Deposit, 0.3% Tier', fontweight='bold')
ax2.legend(loc='upper right', framealpha=0.95)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Annotation for trade-off
ax2.text(0.02, 0.98, 'Trade-off: narrow range earns\n'
         'more per dollar but risks being\n'
         'out of range (earning zero).\n\n'
         f'ETH daily vol ~ {sigma_daily:.0%}\n'
         f'Current price: ${P_current:,}',
         transform=ax2.transAxes, fontsize=10, va='top',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

fig.suptitle('Uniswap v3 Concentrated Liquidity: Efficiency vs Risk\n'
             'Adams et al. (2021): 4000x efficiency possible but with amplified IL and range risk',
             fontsize=15, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
