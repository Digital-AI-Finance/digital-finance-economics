r"""Kyle Lambda Comparison Across Markets
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  Kyle $\lambda = \frac{\sigma_v}{2\sigma_u}$
  S&P=0.0125, BTC-Binance=0.06, ETH-Uniswap=0.12
  Based on Kyle (1985), Barbon & Ranaldo (2022).

  Price impact per unit traded: $\Delta P = \lambda \cdot Q$
  Higher $\lambda$ implies greater adverse selection risk.
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

# --- Data: Kyle lambda for each market ---
# lambda = sigma_v / (2 * sigma_u)
markets = ['S&P 500', 'AAPL', 'BTC-Binance', 'BTC-Coinbase', 'ETH-Uniswap', 'SOL-DEX']
sigma_v = np.array([0.01, 0.016, 0.024, 0.03, 0.048, 0.06])
sigma_u = np.array([0.40, 0.40, 0.20, 0.20, 0.20, 0.20])
lambdas = sigma_v / (2 * sigma_u)
# Verification: S&P=0.0125, AAPL=0.02, BTC-Bin=0.06, BTC-CB=0.075, ETH-Uni=0.12, SOL=0.15

colors = [MLBLUE, MLBLUE, MLORANGE, MLORANGE, MLRED, MLRED]

# Sort by lambda for panel (a)
sort_idx = np.argsort(lambdas)
markets_sorted = [markets[i] for i in sort_idx]
lambdas_sorted = lambdas[sort_idx]
colors_sorted = [colors[i] for i in sort_idx]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Horizontal bar chart sorted by lambda ---
bars = ax1.barh(markets_sorted, lambdas_sorted, color=colors_sorted, edgecolor='black',
                linewidth=1.2, alpha=0.85)
for bar, lam in zip(bars, lambdas_sorted):
    ax1.text(bar.get_width() + 0.003, bar.get_y() + bar.get_height() / 2,
             f'{lam:.4f}', va='center', fontsize=12, fontweight='bold')

ax1.set_xlabel('Kyle Lambda (price impact per unit)')
ax1.set_title('(a) Kyle Lambda by Market', fontweight='bold')
ax1.set_xlim(0, max(lambdas) * 1.35)
ax1.grid(axis='x', alpha=0.3, linestyle='--')

# Annotation: TradFi vs Crypto grouping
ax1.axvline(x=0.03, color=MLPURPLE, linestyle=':', linewidth=1.5, alpha=0.6)
ax1.text(0.03, len(markets) - 0.3, 'TradFi | Crypto', fontsize=10, color=MLPURPLE,
         ha='center', va='bottom',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=MLPURPLE, alpha=0.8))

# --- Panel (b): sigma_v / sigma_u decomposition stacked bars ---
x_pos = np.arange(len(markets))
width = 0.35

bars_v = ax2.bar(x_pos - width / 2, sigma_v, width, label=r'$\sigma_v$ (info volatility)',
                 color=MLRED, alpha=0.8, edgecolor='black', linewidth=1)
bars_u = ax2.bar(x_pos + width / 2, sigma_u, width, label=r'$\sigma_u$ (noise trading)',
                 color=MLBLUE, alpha=0.8, edgecolor='black', linewidth=1)

ax2.set_xticks(x_pos)
ax2.set_xticklabels(markets, rotation=30, ha='right', fontsize=11)
ax2.set_ylabel('Standard Deviation')
ax2.set_title(r'(b) $\sigma_v$ / $\sigma_u$ Decomposition', fontweight='bold')
ax2.legend(loc='upper left', framealpha=0.95)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Add lambda values above each market pair
for i, lam in enumerate(lambdas):
    y_top = max(sigma_v[i], sigma_u[i]) + 0.02
    ax2.text(i, y_top, f'$\\lambda$={lam:.3f}', ha='center', fontsize=10,
             fontweight='bold', color=MLPURPLE)

# Formula annotation
ax2.text(0.98, 0.98, r'$\lambda = \frac{\sigma_v}{2\sigma_u}$' + '\n\n' +
         r'Higher $\sigma_v$ (more insider info)' + '\n' +
         r'$\Rightarrow$ higher price impact' + '\n\n' +
         r'Higher $\sigma_u$ (more noise)' + '\n' +
         r'$\Rightarrow$ lower price impact',
         transform=ax2.transAxes, fontsize=10, va='top', ha='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

fig.suptitle('Kyle (1985) Price Impact: Traditional vs Crypto Markets\n'
             'Barbon & Ranaldo (2022): Crypto lambda 5-12x higher than TradFi',
             fontsize=16, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
