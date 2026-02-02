"""MEV Sandwich Attack: Optimal Extraction

Profit maximization in blockchain front-running attacks.
Theory: Daian et al. (2020) "Flash Boys 2.0: Frontrunning in DEXes"

Based on: Daian et al. (2020) - Flash Boys 2.0
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

# Initial AMM pool (constant product market maker: x*y = k)
x = 10000  # ETH reserve
y = 10000  # USDC reserve
k = x * y  # Constant product
initial_price = y / x  # Initial price: 1 ETH = 1 USDC

# Victim wants to buy ETH by selling this much USDC
dx_victim = 100
gas_cost = 2.0  # Gas cost per transaction (in USDC)

# Sweep front-run sizes to find optimal sandwich size
dx_front_range = np.linspace(1, 500, 100)
profits = []
victim_losses = []  # Track welfare extraction from victim

for dx_front in dx_front_range:
    # Step 1: Attacker front-runs (buys ETH by selling USDC)
    y1 = y + dx_front
    x1 = k / y1
    attacker_eth = x - x1  # ETH attacker receives

    # Step 2: Victim buys ETH (executes at inflated price P' > P)
    y2 = y1 + dx_victim
    x2 = k / y2
    victim_eth = x1 - x2  # ETH victim receives (less than expected)

    # Victim expected to get (at initial price, no front-run):
    y_no_attack = y + dx_victim
    x_no_attack = k / y_no_attack
    victim_eth_expected = x - x_no_attack
    victim_loss = (victim_eth_expected - victim_eth) * (y2/x2)  # Value lost in USDC
    victim_losses.append(victim_loss)

    # Step 3: Attacker back-runs (sells ETH back for USDC at P')
    x3 = x2 + attacker_eth
    y3 = k / x3
    attacker_usdc_back = y2 - y3  # USDC attacker receives

    # Attacker profit: revenue from back-run minus front-run cost minus 2x gas
    # π = Q_f * (P' - P_initial) - 2*gas_cost
    profit = attacker_usdc_back - dx_front - 2*gas_cost
    profits.append(profit)

# Convert to numpy arrays
profits = np.array(profits)
victim_losses = np.array(victim_losses)

# Find optimal sandwich size (maximizes profit)
optimal_idx = np.argmax(profits)
optimal_front = dx_front_range[optimal_idx]
optimal_profit = profits[optimal_idx]
optimal_victim_loss = victim_losses[optimal_idx]

# Calculate prices for the optimal sandwich attack
dx_front_example = optimal_front
y1_ex = y + dx_front_example
x1_ex = k / y1_ex
price_after_front = y1_ex / x1_ex

y2_ex = y1_ex + dx_victim
x2_ex = k / y2_ex
price_after_victim = y2_ex / x2_ex

attacker_eth_ex = x - x1_ex
x3_ex = x2_ex + attacker_eth_ex
y3_ex = k / x3_ex
price_after_back = y3_ex / x3_ex

# Create figure with main plot and inset
fig = plt.figure(figsize=(12, 7))

# Main plot: Price dynamics during sandwich attack
ax_main = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=3)

steps = ['Initial\nP = $1.00', 'After\nFront-run', 'After\nVictim Trade', 'After\nBack-run']
prices = [y/x, price_after_front, price_after_victim, price_after_back]
colors = [MLBLUE, MLRED, MLORANGE, MLGREEN]

bars = ax_main.bar(steps, prices, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax_main.set_ylabel('ETH Price (USDC/ETH)', fontsize=14)
ax_main.set_title('Price Dynamics During Sandwich Attack', fontsize=16, pad=15)
ax_main.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars with price changes
for i, (bar, price) in enumerate(zip(bars, prices)):
    height = bar.get_height()
    ax_main.text(bar.get_x() + bar.get_width()/2., height,
            f'${price:.3f}',
            ha='center', va='bottom', fontsize=12, fontweight='bold')
    if i > 0:
        change = ((price - prices[0]) / prices[0]) * 100
        ax_main.text(bar.get_x() + bar.get_width()/2., height * 0.5,
                f'+{change:.1f}%' if change > 0 else f'{change:.1f}%',
                ha='center', va='center', fontsize=10, color='white', fontweight='bold')

# Add annotations
ax_main.annotate('Attacker\nFront-runs', xy=(1, price_after_front), xytext=(1, price_after_front + 0.008),
            arrowprops=dict(arrowstyle='->', color=MLRED, lw=2), fontsize=10, ha='center', color=MLRED)
ax_main.annotate('Victim\nExecutes', xy=(2, price_after_victim), xytext=(2, price_after_victim + 0.008),
            arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=2), fontsize=10, ha='center', color=MLORANGE)
ax_main.annotate('Attacker\nBack-runs', xy=(3, price_after_back), xytext=(3, price_after_back - 0.008),
            arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=2), fontsize=10, ha='center', color=MLGREEN, va='top')

# Inset: Profit optimization curve
ax_inset = plt.subplot2grid((3, 3), (0, 2), rowspan=2)
ax_inset.plot(dx_front_range, profits, color=MLPURPLE, linewidth=2.5, label='Profit π(Q_f)')
ax_inset.plot(optimal_front, optimal_profit, 'o', color=MLRED, markersize=12,
         markeredgecolor='black', markeredgewidth=2, zorder=5,
         label=f'Optimal Q_f* = {optimal_front:.0f}')
ax_inset.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax_inset.axvline(optimal_front, color=MLRED, linestyle=':', linewidth=1.5, alpha=0.5)
ax_inset.set_xlabel('Sandwich Size Q_f (USDC)', fontsize=11)
ax_inset.set_ylabel('Profit π (USDC)', fontsize=11)
ax_inset.set_title('Profit Optimization', fontsize=13, pad=10)
ax_inset.legend(fontsize=9, loc='upper right')
ax_inset.grid(alpha=0.3, linestyle='--')
ax_inset.tick_params(labelsize=10)

# Add profit equation annotation
ax_inset.text(0.5, 0.15, r'MEV Extraction:' + '\n' +
              r'$\pi = Q_f(P^\prime - P) - 2 \cdot \text{gas}$' + '\n' +
              r'$P^\prime = \frac{y + \Delta y}{x - \Delta x}$ (manipulated price)',
         transform=ax_inset.transAxes, fontsize=9, ha='center',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Welfare analysis panel (bottom right)
ax_welfare = plt.subplot2grid((3, 3), (2, 2))
welfare_data = [optimal_profit, optimal_victim_loss, 2*gas_cost]
welfare_labels = ['Attacker\nProfit', 'Victim\nLoss', 'Gas\nBurned']
welfare_colors = [MLGREEN, MLRED, '#888888']

bars_welfare = ax_welfare.bar(welfare_labels, welfare_data, color=welfare_colors, alpha=0.7,
                          edgecolor='black', linewidth=1.5)
ax_welfare.set_ylabel('Value (USDC)', fontsize=10)
ax_welfare.set_title('Welfare Distribution', fontsize=12, pad=8)
ax_welfare.grid(axis='y', alpha=0.3, linestyle='--')
ax_welfare.tick_params(labelsize=9)

# Add value labels
for bar, value in zip(bars_welfare, welfare_data):
    height = bar.get_height()
    ax_welfare.text(bar.get_x() + bar.get_width()/2., height,
            f'${value:.2f}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

# Add zero-sum note
net_welfare = optimal_profit - optimal_victim_loss - 2*gas_cost
ax_welfare.text(0.5, -0.25, f'Net: ${net_welfare:.2f} (zero-sum minus gas)',
         transform=ax_welfare.transAxes, fontsize=8, ha='center', style='italic',
         bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

fig.suptitle('MEV Sandwich Attack: Optimal Extraction Strategy\n' +
             f'Daian et al. (2020): Victim Trade = {dx_victim} USDC, Optimal Front-run = {optimal_front:.0f} USDC',
             fontsize=17, y=0.98, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
