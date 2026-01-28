"""MEV: Sandwich Attack Value Extraction"""
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

# Initial AMM pool
x = 10000  # ETH
y = 10000  # USDC
k = x * y  # Constant product

# Victim wants to buy ETH by selling this much USDC
dx_victim = 100

# Sweep front-run sizes
dx_front_range = np.linspace(1, 500, 100)
profits = []
prices_before = []
prices_after_front = []
prices_after_victim = []

for dx_front in dx_front_range:
    # Step 1: Attacker front-runs (sells USDC to buy ETH)
    y1 = y + dx_front
    x1 = k / y1
    attacker_eth = x - x1  # ETH attacker receives

    # Step 2: Victim sells USDC to buy ETH
    y2 = y1 + dx_victim
    x2 = k / y2
    victim_eth = x1 - x2  # ETH victim receives

    # Step 3: Attacker back-runs (sells ETH back to USDC)
    x3 = x2 + attacker_eth
    y3 = k / x3
    attacker_usdc_back = y2 - y3  # USDC attacker receives

    # Attacker profit
    profit = attacker_usdc_back - dx_front
    profits.append(profit)

    # Track prices for the example case
    if abs(dx_front - 200) < 3:  # Close to 200
        prices_before.append(y / x)
        prices_after_front.append(y1 / x1)
        prices_after_victim.append(y2 / x2)

# Convert to numpy array
profits = np.array(profits)
optimal_idx = np.argmax(profits)
optimal_front = dx_front_range[optimal_idx]
optimal_profit = profits[optimal_idx]

# Calculate prices for the dx_front=200 example
dx_front_example = 200
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

# Create two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left subplot: Price manipulation steps
steps = ['Initial', 'After\nFront-run', 'After\nVictim', 'After\nBack-run']
prices = [y/x, price_after_front, price_after_victim, price_after_back]
colors = [MLBLUE, MLRED, MLORANGE, MLGREEN]

bars = ax1.bar(steps, prices, color=colors, alpha=0.7, edgecolor='black')
ax1.set_ylabel('ETH Price (USDC/ETH)')
ax1.set_title(f'Price Manipulation (Front-run: {dx_front_example} USDC)')
ax1.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bar, price in zip(bars, prices):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'${price:.2f}',
            ha='center', va='bottom', fontsize=11)

# Right subplot: Profit vs front-run size
ax2.plot(dx_front_range, profits, color=MLPURPLE, linewidth=2)
ax2.plot(optimal_front, optimal_profit, 'o', color=MLRED, markersize=10,
        label=f'Optimal: {optimal_front:.0f} USDC → ${optimal_profit:.2f} profit')
ax2.axhline(0, color='black', linestyle='--', linewidth=1)
ax2.set_xlabel('Front-run Size (USDC)')
ax2.set_ylabel('Attacker Profit (USDC)')
ax2.set_title('Profit vs Front-run Size')
ax2.legend()
ax2.grid(alpha=0.3)

fig.suptitle('MEV Sandwich Attack: Extraction Mechanics', fontsize=18, y=1.02)
plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
