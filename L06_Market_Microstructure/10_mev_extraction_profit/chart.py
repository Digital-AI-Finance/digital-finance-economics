r"""MEV Extraction Profit: Sandwich Attack with Interior Maximum
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  Sandwich profit: $\pi = Q_f \cdot (P' - P) - Q_f \cdot f_{AMM} \cdot (P + P')/2 - 2 \cdot gas - c_{PGA}$
  where $c_{PGA} = 0.5 \cdot \pi$ (priority gas auction cost, quadratic in Q_f)
  Pool: 100 ETH / 180,000 USDC. f_AMM = 0.003. gas = 50 USD.
  Victim trade: 1..20 ETH. Interior maximum from AMM fees + quadratic PGA cost.
  Based on Daian et al. (2020), Qin et al. (2022).

  Panel (a): Profit vs front-run size for different victim sizes.
  Panel (b): Optimal front-run and max profit vs victim size.
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

# --- Pool parameters ---
x0 = 100.0     # ETH reserve
y0 = 180000.0  # USDC reserve
k = x0 * y0    # Constant product: 18,000,000
P0 = y0 / x0   # Initial price: 1800 USDC/ETH
f_AMM = 0.003  # 0.3% AMM fee
gas = 50.0      # Gas cost per transaction (USD)
pga_coeff = 50.0  # PGA quadratic coefficient: c_PGA = pga_coeff * Q_f^2 (high competition)


def sandwich_profit(Q_f, Q_victim):
    """Calculate sandwich profit with AMM fees and quadratic PGA cost.

    Interior maximum exists because:
    - Revenue grows sub-linearly (AMM price impact is concave in Q_f)
    - AMM fees grow linearly with Q_f
    - PGA cost grows quadratically with Q_f
    """
    if Q_f <= 0 or Q_f >= x0 * 0.8:
        return -np.inf, 0, 0

    # Step 1: Front-run - buy Q_f ETH
    # Trader sends USDC, receives Q_f ETH (after fee)
    x1 = x0 - Q_f
    y1 = k / x1
    cost_front = (y1 - y0)  # USDC cost before fee
    amm_fee_front = cost_front * f_AMM
    total_cost_front = cost_front + amm_fee_front
    P_after_front = y1 / x1

    # Step 2: Victim buys Q_victim ETH
    x2 = x1 - Q_victim
    if x2 <= 0:
        return -np.inf, 0, 0
    y2 = k / x2
    P_after_victim = y2 / x2

    # Step 3: Back-run - sell Q_f ETH back
    x3 = x2 + Q_f
    y3 = k / x3
    revenue_back = (y2 - y3)
    amm_fee_back = revenue_back * f_AMM
    total_revenue_back = revenue_back - amm_fee_back

    # Profit calculation
    gross = total_revenue_back - total_cost_front
    total_gas = 2 * gas
    c_pga = pga_coeff * Q_f**2  # Quadratic PGA cost
    profit = gross - total_gas - c_pga

    return profit, P_after_front, P_after_victim


# --- Panel (a): Profit curves for different victim sizes ---
victim_sizes_panel_a = [2, 5, 10, 15, 20]
victim_colors = [MLBLUE, MLGREEN, MLORANGE, MLRED, MLPURPLE]
Q_f_range = np.linspace(0.1, 40, 300)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

for Q_v, color in zip(victim_sizes_panel_a, victim_colors):
    profits = [sandwich_profit(qf, Q_v)[0] for qf in Q_f_range]
    profits = np.array(profits)
    # Replace -inf with nan for plotting
    profits[profits < -1e6] = np.nan
    ax1.plot(Q_f_range, profits, color=color, linewidth=2, label=f'Victim = {Q_v} ETH')

    # Mark optimal
    valid = ~np.isnan(profits)
    if np.any(valid):
        opt_idx = np.nanargmax(profits)
        if profits[opt_idx] > 0:
            ax1.plot(Q_f_range[opt_idx], profits[opt_idx], 'o', color=color,
                     markersize=8, markeredgecolor='black', markeredgewidth=1.5, zorder=5)

ax1.axhline(y=0, color='black', linestyle='--', linewidth=1.5, alpha=0.7)
ax1.set_xlabel('Front-run Size Q_f (ETH)')
ax1.set_ylabel('Sandwich Profit (USDC)')
ax1.set_title('(a) Profit vs Front-Run Size', fontweight='bold')
ax1.legend(loc='upper right', fontsize=10, framealpha=0.95)
ax1.grid(alpha=0.3, linestyle='--')
ax1.set_xlim(0, 40)

# Annotate interior maximum
ax1.annotate('Interior maximum:\nAMM fees + PGA cost\ndominate at large Q_f',
             xy=(25, -200), xytext=(28, 500),
             fontsize=9, color=MLRED,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=MLRED, alpha=0.8))

# --- Panel (b): Optimal Q_f and max profit vs victim size ---
victim_range = np.linspace(1, 20, 100)
opt_qf = []
max_profit = []

for Q_v in victim_range:
    best_profit = -np.inf
    best_qf = 0
    for qf in np.linspace(0.1, min(Q_v * 3, x0 * 0.7), 500):
        p, _, _ = sandwich_profit(qf, Q_v)
        if p > best_profit:
            best_profit = p
            best_qf = qf
    opt_qf.append(best_qf)
    max_profit.append(max(best_profit, 0))

opt_qf = np.array(opt_qf)
max_profit = np.array(max_profit)

ax2_twin = ax2.twinx()

line1, = ax2.plot(victim_range, max_profit, color=MLRED, linewidth=2.5,
                  label='Max Profit (USDC)')
line2, = ax2_twin.plot(victim_range, opt_qf, color=MLBLUE, linewidth=2.5,
                       linestyle='--', label='Optimal Q_f (ETH)')

ax2.set_xlabel('Victim Trade Size (ETH)')
ax2.set_ylabel('Maximum Profit (USDC)', color=MLRED)
ax2_twin.set_ylabel('Optimal Front-Run Size (ETH)', color=MLBLUE)
ax2.set_title('(b) Optimal Extraction vs Victim Size', fontweight='bold')

# Combine legends
lines = [line1, line2]
labels = [l.get_label() for l in lines]
ax2.legend(lines, labels, loc='upper left', framealpha=0.95)
ax2.grid(alpha=0.3, linestyle='--')

# Add profit equation
ax2.text(0.98, 0.4, r'$\pi = Q_f(P\prime - P)$' + '\n' +
         r'$- Q_f \cdot f_{AMM} \cdot \frac{P + P\prime}{2}$' + '\n' +
         r'$- 2 \cdot gas - c_{PGA}$' + '\n\n' +
         r'$c_{PGA} = \alpha Q_f^2$' + '\n' +
         f'Pool: {x0:.0f} ETH / {y0:,.0f} USDC\n'
         f'f_AMM = {f_AMM}, gas = ${gas:.0f}',
         transform=ax2.transAxes, fontsize=9, va='center', ha='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Mark minimum viable victim size
min_viable_idx = np.argmax(max_profit > 0)
if max_profit[min_viable_idx] > 0:
    min_victim = victim_range[min_viable_idx]
    ax2.axvline(x=min_victim, color=MLPURPLE, linestyle=':', linewidth=1.5, alpha=0.6)
    ax2.text(min_victim + 0.3, max(max_profit) * 0.8,
             f'Min viable\nvictim: {min_victim:.1f} ETH',
             fontsize=9, color=MLPURPLE, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                       edgecolor=MLPURPLE, alpha=0.8))

fig.suptitle('MEV Sandwich Attack: Profit Optimization with Interior Maximum\n'
             'Daian et al. (2020), Qin et al. (2022): AMM fees + PGA costs create optimal extraction size',
             fontsize=15, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
