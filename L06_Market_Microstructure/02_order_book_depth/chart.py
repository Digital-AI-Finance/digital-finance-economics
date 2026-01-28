"""Order Book Depth Chart (Glosten-Milgrom)"""
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

# Generate bid orders
bid_prices = np.random.normal(99.5, 0.8, 200)
bid_prices = np.clip(bid_prices, 95, 100)
bid_volumes = np.random.exponential(50, 200)

# Generate ask orders
ask_prices = np.random.normal(100.5, 0.8, 200)
ask_prices = np.clip(ask_prices, 100, 105)
ask_volumes = np.random.exponential(50, 200)

# Sort bids descending, asks ascending
bid_sort_idx = np.argsort(bid_prices)[::-1]
bid_prices = bid_prices[bid_sort_idx]
bid_volumes = bid_volumes[bid_sort_idx]

ask_sort_idx = np.argsort(ask_prices)
ask_prices = ask_prices[ask_sort_idx]
ask_volumes = ask_volumes[ask_sort_idx]

# Compute cumulative volumes
bid_cumvol = np.cumsum(bid_volumes)
ask_cumvol = np.cumsum(ask_volumes)

# Calculate mid-price
best_bid = bid_prices[0]
best_ask = ask_prices[0]
mid_price = (best_bid + best_ask) / 2

# Create depth chart
fig, ax = plt.subplots()

ax.fill_betweenx(bid_cumvol, bid_prices, mid_price,
                  step='post', alpha=0.6, color=MLGREEN, label='Bids')
ax.fill_betweenx(ask_cumvol, mid_price, ask_prices,
                  step='post', alpha=0.6, color=MLRED, label='Asks')

# Add vertical line at mid-price
ax.axvline(mid_price, color='black', linestyle='--', linewidth=1.5,
           label=f'Mid-Price: ${mid_price:.2f}')

# Shade the spread region
ax.axvspan(best_bid, best_ask, alpha=0.2, color='gray', label='Spread')

ax.set_xlabel('Price ($)')
ax.set_ylabel('Cumulative Volume')
ax.set_title('Order Book Depth and Bid-Ask Spread')
ax.legend()
ax.grid(alpha=0.3)

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
