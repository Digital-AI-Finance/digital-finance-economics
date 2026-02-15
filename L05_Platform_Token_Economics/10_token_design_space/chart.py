"""Token Design Space: Iso-GDP Curves in Velocity-Supply Space

Multi-panel chart showing token design trade-offs through the equation of exchange.

Economic Model:
  $MV = PQ$. Iso-GDP: $GDP \in [\$100M, \$100B]$. Based on Samani (2017), Burniske (2017).
  For a given GDP level, tokens can trade off velocity vs supply:
  $M = GDP / (V \times P_{target})$, or equivalently, iso-GDP curve: $M \times V = GDP / P_{target}$.

# Multi-panel override: comparative statics requires simultaneous visibility

Citation: Samani (2017) - Understanding Token Velocity; Burniske (2017) - Cryptoasset Valuations
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Iso-GDP curves in (V, MarketCap) space ---
# MV = PQ = GDP, so MarketCap (= M*P) = GDP/V at P=1 normalization
# Actually: P_token = GDP / (M * V), so MarketCap = M * P = GDP / V
V_range = np.linspace(1, 100, 500)

gdp_levels = [100e6, 1e9, 10e9, 100e9]
gdp_labels = ['GDP = $100M', 'GDP = $1B', 'GDP = $10B', 'GDP = $100B']
gdp_colors = [MLLAVENDER, MLBLUE, MLGREEN, MLPURPLE]

for gdp, label, color in zip(gdp_levels, gdp_labels, gdp_colors):
    mc = gdp / V_range
    ax1.plot(V_range, mc / 1e9, color=color, linewidth=2.5, label=label)

# Mark real tokens
tokens = [
    ('BTC', 5, 800, MLORANGE),   # V=5, MC=$800B
    ('ETH', 15, 300, MLBLUE),    # V=15, MC=$300B
    ('SOL', 25, 50, MLGREEN),    # V=25, MC=$50B
]

for name, v, mc_b, color in tokens:
    ax1.plot(v, mc_b, '*', color=color, markersize=18,
             markeredgecolor='black', markeredgewidth=1.5, zorder=5)
    # Compute implied GDP = MC * V
    implied_gdp = mc_b * 1e9 * v
    gdp_str = f'${implied_gdp/1e12:.1f}T' if implied_gdp >= 1e12 else f'${implied_gdp/1e9:.0f}B'
    ax1.annotate(f'{name}\nV={v}, MC=${mc_b}B\nGDP={gdp_str}',
                 xy=(v, mc_b),
                 xytext=(v + 8, mc_b * 1.2),
                 fontsize=9, fontweight='bold', color=color,
                 arrowprops=dict(arrowstyle='->', color=color, lw=1.5),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                           edgecolor=color, alpha=0.9))

ax1.set_xlabel('Token Velocity (V)')
ax1.set_ylabel('Market Cap ($B)')
ax1.set_title('(a) Iso-GDP Curves: MC = GDP / V')
ax1.set_yscale('log')
ax1.legend(loc='upper right', fontsize=9, framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(1, 100)
ax1.set_ylim(1, 2000)

# Design insight box
ax1.text(0.02, 0.35,
         'Design trade-off:\n'
         'Low V (staking) = high MC per GDP\n'
         'High V (payment) = low MC per GDP\n'
         'Move up = grow network GDP\n'
         'Move left = add velocity sinks',
         transform=ax1.transAxes, fontsize=9, va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                   edgecolor=MLORANGE, alpha=0.9))

# --- Panel (b): Token classification by design choices ---
# Scatter plot: x = V (velocity), y = GDP (network activity)
# Size = market cap, color = token type

# Simulated token universe
np.random.seed(42)
n_tokens = 50

# Payment tokens: high V, moderate GDP
v_payment = np.random.uniform(20, 80, 15)
gdp_payment = np.random.lognormal(np.log(500e6), 0.8, 15)
mc_payment = gdp_payment / v_payment

# Store-of-value tokens: low V, high GDP
v_sov = np.random.uniform(2, 10, 10)
gdp_sov = np.random.lognormal(np.log(5e9), 1.0, 10)
mc_sov = gdp_sov / v_sov

# Utility/governance tokens: medium V, medium GDP
v_utility = np.random.uniform(8, 30, 15)
gdp_utility = np.random.lognormal(np.log(1e9), 0.7, 15)
mc_utility = gdp_utility / v_utility

# DeFi tokens: medium-high V, varying GDP
v_defi = np.random.uniform(15, 50, 10)
gdp_defi = np.random.lognormal(np.log(2e9), 1.2, 10)
mc_defi = gdp_defi / v_defi

# Plot each category
def plot_category(ax, v, gdp, mc, color, label):
    sizes = np.clip(mc / 1e8, 5, 500)  # scale for visibility
    ax.scatter(v, gdp / 1e9, s=sizes, color=color, alpha=0.6,
               edgecolors='black', linewidths=0.5, label=label, zorder=3)

plot_category(ax2, v_payment, gdp_payment, mc_payment, MLRED, 'Payment')
plot_category(ax2, v_sov, gdp_sov, mc_sov, MLORANGE, 'Store of Value')
plot_category(ax2, v_utility, gdp_utility, mc_utility, MLBLUE, 'Utility/Governance')
plot_category(ax2, v_defi, gdp_defi, mc_defi, MLGREEN, 'DeFi')

# Mark real tokens
for name, v, mc_b, color in tokens:
    implied_gdp = mc_b * 1e9 * v
    ax2.plot(v, implied_gdp / 1e9, '*', color=color, markersize=20,
             markeredgecolor='black', markeredgewidth=2, zorder=5)
    ax2.annotate(name, xy=(v, implied_gdp / 1e9),
                 xytext=(5, 5), textcoords='offset points',
                 fontsize=11, fontweight='bold', color='black')

# Quadrant labels
ax2.text(60, 0.3, 'Low GDP\nHigh V\n(struggling\npayment tokens)',
         fontsize=8, ha='center', color='gray', style='italic',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
ax2.text(5, 100, 'High GDP\nLow V\n(dominant SoV)',
         fontsize=8, ha='center', color='gray', style='italic',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

ax2.set_xlabel('Token Velocity (V)')
ax2.set_ylabel('Network GDP ($B)')
ax2.set_title('(b) Token Design Space')
ax2.set_yscale('log')
ax2.legend(loc='upper right', fontsize=9, framealpha=0.95)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(0, 85)

# Size legend
ax2.text(0.02, 0.15, 'Bubble size = market cap\nBigger = higher valuation',
         transform=ax2.transAxes, fontsize=8, va='top',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=MLLAVENDER, alpha=0.3))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
