"""Token Supply Schedules Compared"""
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

years = 20
t = np.arange(0, years + 1)

# Bitcoin: halving every 4 years, starting at 6.25 BTC per block
btc_supply = np.zeros(years + 1)
btc_supply[0] = 19e6
block_reward = 6.25
blocks_per_year = 144 * 365  # ~52,560 blocks/year

for year in range(1, years + 1):
    # Determine current block reward (halving every 4 years)
    halvings = year // 4
    current_reward = block_reward / (2 ** halvings)

    # Add new supply
    new_supply = current_reward * blocks_per_year
    btc_supply[year] = min(btc_supply[year - 1] + new_supply, 21e6)

# Ethereum: start 120M, +0.5M issuance, -0.8M burn (net -0.3M)
eth_supply = np.zeros(years + 1)
eth_supply[0] = 120e6
net_change = -0.3e6  # Net deflation per year

for year in range(1, years + 1):
    eth_supply[year] = eth_supply[year - 1] + net_change

# Inflationary: 5% compound annual growth
inf_supply = np.zeros(years + 1)
inf_supply[0] = 100e6
for year in range(1, years + 1):
    inf_supply[year] = inf_supply[year - 1] * 1.05

# Deflationary: 2% burn per year
def_supply = np.zeros(years + 1)
def_supply[0] = 100e6
for year in range(1, years + 1):
    def_supply[year] = def_supply[year - 1] * 0.98

# Plot
fig, ax = plt.subplots()

ax.plot(t, btc_supply / 1e6, linewidth=2.5, color=MLORANGE, label='Bitcoin (Capped)', marker='o', markersize=3)
ax.plot(t, eth_supply / 1e6, linewidth=2.5, color=MLBLUE, label='Ethereum (Net Deflationary)', marker='s', markersize=3)
ax.plot(t, inf_supply / 1e6, linewidth=2.5, color=MLRED, label='Inflationary (+5%/year)', marker='^', markersize=3)
ax.plot(t, def_supply / 1e6, linewidth=2.5, color=MLGREEN, label='Deflationary (-2%/year)', marker='v', markersize=3)

# Mark Bitcoin halvings
halving_years = [4, 8, 12, 16, 20]
for hy in halving_years:
    if hy <= years:
        ax.axvline(hy, color=MLORANGE, linestyle=':', alpha=0.4, linewidth=1.5)
        ax.text(hy, ax.get_ylim()[1] * 0.95, 'Halving', fontsize=9,
                color=MLORANGE, ha='center', rotation=90, va='top')

# Mark BTC cap
ax.axhline(21, color=MLORANGE, linestyle='--', alpha=0.3, linewidth=1.5)
ax.text(years * 0.98, 21.5, '21M cap', fontsize=10, color=MLORANGE, ha='right')

ax.set_xlabel('Years')
ax.set_ylabel('Total Supply (millions)')
ax.set_title('Token Supply Schedules (20-Year Projection)')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(0, years)
ax.set_ylim(0, 150)

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
