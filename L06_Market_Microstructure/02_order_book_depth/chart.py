"""Order Book Depth: Kyle's Lambda Price Impact

Measuring market liquidity through price impact coefficient.
Theory: Kyle (1985) "Continuous Auctions and Insider Trading"
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 12,
    'figure.figsize': (12, 7), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Kyle (1985) Model: Price Impact ΔP = λ * Q
# λ = Kyle's lambda = σ_v / (2 * σ_u)
# where σ_v = information asymmetry, σ_u = noise trading volatility

# Market parameters: (sigma_v, sigma_u) -> lambda
markets = {
    'BTC': {'sigma_v': 0.15, 'sigma_u': 0.10, 'color': MLORANGE, 'label': 'Bitcoin'},
    'ETH': {'sigma_v': 0.12, 'sigma_u': 0.12, 'color': MLBLUE, 'label': 'Ethereum'},
    'S&P500': {'sigma_v': 0.05, 'sigma_u': 0.20, 'color': MLGREEN, 'label': 'S&P 500 Futures'}
}

# Calculate Kyle's lambda for each market
for market, params in markets.items():
    lambda_val = params['sigma_v'] / (2 * params['sigma_u'])
    params['lambda'] = lambda_val

# Order sizes (in standard units: BTC, ETH, contracts)
order_sizes = np.linspace(0, 100, 200)

# Create main figure
fig = plt.figure(figsize=(12, 7))
gs = fig.add_gridspec(2, 2, height_ratios=[2, 1], width_ratios=[3, 1],
                      hspace=0.3, wspace=0.3)

# Main plot: Price impact vs order size
ax_main = fig.add_subplot(gs[0, :])

for market, params in markets.items():
    lambda_val = params['lambda']
    price_impact = lambda_val * order_sizes

    ax_main.plot(order_sizes, price_impact,
                label=f"{params['label']}: λ = {lambda_val:.4f}",
                color=params['color'], linewidth=2.5)

    # Add annotation at midpoint
    mid_idx = len(order_sizes) // 2
    ax_main.annotate(f"λ = {lambda_val:.4f}",
                    xy=(order_sizes[mid_idx], price_impact[mid_idx]),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=11, color=params['color'],
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                             edgecolor=params['color'], alpha=0.8))

ax_main.set_xlabel('Order Size (units)', fontsize=14)
ax_main.set_ylabel('Price Impact ΔP (%)', fontsize=14)
ax_main.set_title("Kyle's Lambda: Price Impact Across Markets\nΔP = λ × Q",
                 fontsize=16, pad=15)
ax_main.legend(loc='upper left', framealpha=0.95)
ax_main.grid(alpha=0.3, linestyle='--')
ax_main.set_xlim(0, 100)

# Add theory box
theory_text = (
    "Kyle (1985) Model:\n"
    "λ = σᵥ / (2σᵤ)\n"
    "• σᵥ: Info asymmetry\n"
    "• σᵤ: Noise trading\n"
    "• Higher λ → Less liquid"
)
ax_main.text(0.98, 0.05, theory_text, transform=ax_main.transAxes,
            fontsize=11, verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Bottom left: Lambda comparison bar chart
ax_lambda = fig.add_subplot(gs[1, 0])

market_names = [params['label'] for params in markets.values()]
lambda_values = [params['lambda'] for params in markets.values()]
colors = [params['color'] for params in markets.values()]

bars = ax_lambda.barh(market_names, lambda_values, color=colors, alpha=0.7, edgecolor='black')

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, lambda_values)):
    ax_lambda.text(val + 0.002, i, f'{val:.4f}',
                  va='center', fontsize=11, fontweight='bold')

ax_lambda.set_xlabel("Kyle's Lambda (λ)", fontsize=12)
ax_lambda.set_title('Illiquidity Coefficient by Market', fontsize=13)
ax_lambda.grid(axis='x', alpha=0.3)
ax_lambda.set_xlim(0, max(lambda_values) * 1.2)

# Bottom right: Order book depth visualization (illustrative)
ax_depth = fig.add_subplot(gs[1, 1])

# Simplified order book for illustration
depth_prices = np.array([98, 99, 99.5, 100, 100.5, 101, 102])
depth_volumes_bid = np.array([150, 100, 50, 0, 0, 0, 0])  # Cumulative
depth_volumes_ask = np.array([0, 0, 0, 0, 50, 100, 150])  # Cumulative

mid_price = 100

# Plot bid and ask depth
ax_depth.plot(depth_prices, depth_volumes_bid, color=MLGREEN, linewidth=2,
             label='Bid depth', marker='o', markersize=4)
ax_depth.plot(depth_prices, depth_volumes_ask, color=MLRED, linewidth=2,
             label='Ask depth', marker='o', markersize=4)

# Shade spread
ax_depth.axvspan(99.5, 100.5, alpha=0.2, color='gray')
ax_depth.axvline(mid_price, color='black', linestyle='--', linewidth=1, alpha=0.5)

ax_depth.set_xlabel('Price ($)', fontsize=11)
ax_depth.set_ylabel('Depth', fontsize=11)
ax_depth.set_title('Order Book\nDepth', fontsize=12)
ax_depth.legend(loc='upper right', fontsize=9)
ax_depth.grid(alpha=0.3)
ax_depth.tick_params(labelsize=10)

# Add citation
fig.text(0.99, 0.01, 'Source: Kyle (1985) "Continuous Auctions and Insider Trading"',
        ha='right', va='bottom', fontsize=10, style='italic', color='gray')

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
