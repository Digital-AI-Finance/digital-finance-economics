"""Token Value Heatmap: Equation of Exchange Applied to Crypto Tokens

Multi-panel chart showing token price as function of velocity and money supply.

Economic Model:
  $P_{token} = \frac{GDP_{network}}{M \times V}$. Based on Samani (2017).
  Fisher's equation of exchange: MV = PQ, rearranged for token price.
  Effective velocity with staking: $V_{eff} = V_{base} \times (1 - \theta)$
  where $\theta$ = stake ratio (fraction of tokens locked).

# Multi-panel override: comparative statics requires simultaneous visibility

Citation: Samani (2017) - Understanding Token Velocity; Burniske (2017)
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

# --- Model: P_token = GDP / (M * V) ---
GDP = 1e9  # $1B network GDP

# Panel (a): Heatmap of token price over V and M
V_range = np.logspace(0, 2, 200)        # V from 1 to 100
M_range = np.logspace(np.log10(1e6), np.log10(1e9), 200)  # M from 1M to 1B

V_grid, M_grid = np.meshgrid(V_range, M_range)
P_grid = GDP / (M_grid * V_grid)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Token Price Heatmap ---
levels = np.logspace(-3, 3, 25)  # $0.001 to $1000
cmap = plt.cm.RdYlGn_r  # Red=low price, Green=high price
cs = ax1.contourf(V_range, M_range, P_grid, levels=levels,
                  norm=plt.matplotlib.colors.LogNorm(vmin=0.001, vmax=1000),
                  cmap=cmap, alpha=0.85)
cbar = fig.colorbar(cs, ax=ax1, label='Token Price ($)', format='$%.2g')

# Contour lines for key prices
contour_prices = [0.01, 0.1, 1, 10, 100]
cs_lines = ax1.contour(V_range, M_range, P_grid, levels=contour_prices,
                       colors='black', linewidths=1.0, alpha=0.5)
ax1.clabel(cs_lines, fmt='$%.2g', fontsize=8)

# Mark real tokens: BTC (V~5, MC~800B), ETH (V~15, MC~300B), SOL (V~25, MC~50B)
tokens = [
    ('BTC', 5, 800e9, MLORANGE),
    ('ETH', 15, 300e9, MLBLUE),
    ('SOL', 25, 50e9, MLGREEN),
]
# Note: MC = M * P, so M = MC / P, but P = GDP/(M*V), so MC = GDP/V
# For plotting: we need M (supply). Use MC/P = M, but P = GDP/(M*V)
# Actually MC = M*P = M * GDP/(M*V) = GDP/V
# So for BTC: P = GDP/(M*V), need M. BTC supply ~19M, ETH ~120M, SOL ~400M
token_supplies = {
    'BTC': (19e6, 5),     # 19M tokens, V=5
    'ETH': (120e6, 15),   # 120M tokens, V=15
    'SOL': (400e6, 25),   # 400M tokens, V=25
}

for name, (m_supply, v_val), color in zip(
    ['BTC', 'ETH', 'SOL'],
    [token_supplies['BTC'], token_supplies['ETH'], token_supplies['SOL']],
    [MLORANGE, MLBLUE, MLGREEN]
):
    p_val = GDP / (m_supply * v_val)
    ax1.plot(v_val, m_supply, '*', color=color, markersize=15,
             markeredgecolor='black', markeredgewidth=1.5, zorder=5)
    ax1.annotate(f'{name}\nV={v_val}, M={m_supply/1e6:.0f}M\nP=${p_val:.2f}',
                 xy=(v_val, m_supply),
                 xytext=(v_val * 1.8, m_supply * 1.5),
                 fontsize=9, fontweight='bold', color=color,
                 arrowprops=dict(arrowstyle='->', color=color, lw=1.5),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                           edgecolor=color, alpha=0.9))

ax1.set_xlabel('Token Velocity (V)')
ax1.set_ylabel('Token Supply (M)')
ax1.set_title('(a) Token Price Heatmap: P = GDP / (M x V)')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3, linestyle='--')

# Model box
ax1.text(0.02, 0.98, 'GDP = $1B\n$P = GDP/(M \\times V)$\nHigher V or M\n= lower token price',
         transform=ax1.transAxes, fontsize=9, va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor=MLLAVENDER, alpha=0.4))

# --- Panel (b): Effective velocity with staking ---
# V_eff = V_base * (1 - theta), theta = stake ratio
theta_range = np.linspace(0, 0.9, 100)
V_base_vals = [5, 15, 25]
V_base_labels = ['V_base = 5 (BTC-like)', 'V_base = 15 (ETH-like)', 'V_base = 25 (SOL-like)']
V_base_colors = [MLORANGE, MLBLUE, MLGREEN]

M_fixed = 100e6  # 100M tokens for comparison

for v_base, v_label, v_color in zip(V_base_vals, V_base_labels, V_base_colors):
    V_eff = v_base * (1 - theta_range)
    P_tokens = GDP / (M_fixed * V_eff)
    ax2.plot(theta_range, P_tokens, color=v_color, linewidth=2.5, label=v_label)

# Mark ETH staking example: theta=0.25
theta_eth = 0.25
V_eff_eth = 15 * (1 - theta_eth)
P_eth = GDP / (M_fixed * V_eff_eth)
ax2.plot(theta_eth, P_eth, 'o', color=MLBLUE, markersize=12,
         markeredgecolor='black', markeredgewidth=2, zorder=5)
ax2.annotate(f'ETH: theta=0.25\nV_eff={V_eff_eth:.2f}\nP=${P_eth:.2f}',
             xy=(theta_eth, P_eth),
             xytext=(theta_eth + 0.15, P_eth * 1.3),
             fontsize=10, fontweight='bold', color=MLBLUE,
             arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLBLUE, alpha=0.9))

# Danger zone
ax2.axvspan(0.7, 0.9, alpha=0.15, color=MLRED, zorder=0)
ax2.text(0.80, 0.25, 'Danger:\nIlliquidity',
         transform=ax2.transAxes, fontsize=9, ha='center', color=MLRED,
         fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                   edgecolor=MLRED, alpha=0.8))

ax2.set_xlabel(r'Stake Ratio ($\theta$)')
ax2.set_ylabel('Token Price ($)')
ax2.set_title(r'(b) Staking Effect: $V_{eff} = V_{base} \times (1-\theta)$')
ax2.legend(loc='upper left', fontsize=9, framealpha=0.95)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(0, 0.9)

# Model box
ax2.text(0.55, 0.55, 'M = 100M tokens\nGDP = $1B\nStaking reduces V,\nraising token price',
         transform=ax2.transAxes, fontsize=9, va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                   edgecolor=MLORANGE, alpha=0.9))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
