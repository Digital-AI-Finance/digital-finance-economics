r"""LP Profitability Frontier: Fee Income vs Impermanent Loss
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  Impermanent Loss: $IL = \frac{2\sqrt{r}}{1+r} - 1$ where $r = P_T/P_0$
  Fee Income (annualized): $F = f \times \frac{V}{TVL} \times 365$
  Net LP Return: $R_{net} = F + IL$
  Breakeven volatility: $\sigma^*$ where $F = |IL|$
  Based on Adams et al. (2024), Lambert et al. (2022).

  Panel (a): Net return heatmap (volatility vs fee tier).
  Panel (b): Breakeven frontier curves.
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
fee_tiers = [0.0005, 0.003, 0.01]  # 0.05%, 0.3%, 1%
fee_labels = ['0.05%', '0.30%', '1.00%']
fee_colors = [MLBLUE, MLGREEN, MLORANGE]
V_TVL = 2.0  # daily volume / TVL ratio

# Annualized volatility range
sigma_range = np.linspace(0.05, 1.0, 200)

# For a given annualized volatility sigma, approximate expected IL over 1 year:
# Price follows GBM: ln(P_T/P_0) ~ N(-sigma^2/2, sigma^2)
# E[IL] = E[2*sqrt(r)/(1+r) - 1] where r = exp(ln(P_T/P_0))
# Monte Carlo estimate for IL at each sigma
n_sims = 10000

def expected_il(sigma, n=n_sims):
    """Monte Carlo expected IL for given annualized volatility."""
    ln_r = np.random.normal(-sigma**2 / 2, sigma, n)
    r = np.exp(ln_r)
    il = 2 * np.sqrt(r) / (1 + r) - 1
    return np.mean(il)

# Compute expected IL for each sigma
np.random.seed(42)
expected_ils = np.array([expected_il(s) for s in sigma_range])

# Annualized fee income for each tier: f * V/TVL * 365
annual_fees = np.array([f * V_TVL * 365 for f in fee_tiers])

# Net returns: fee - |IL| (IL is negative, so net = fee + IL)
net_returns = {}
for i, (f, label) in enumerate(zip(fee_tiers, fee_labels)):
    annual_fee = f * V_TVL * 365
    net = annual_fee + expected_ils  # IL is negative
    net_returns[label] = net

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Net return vs volatility for each fee tier ---
for i, (label, net) in enumerate(net_returns.items()):
    ax1.plot(sigma_range * 100, net * 100, color=fee_colors[i], linewidth=2.5,
             label=f'Fee tier: {label}')
    # Find breakeven (where net crosses zero)
    zero_crossings = np.where(np.diff(np.sign(net)))[0]
    if len(zero_crossings) > 0:
        idx = zero_crossings[0]
        be_sigma = sigma_range[idx] * 100
        ax1.plot(be_sigma, 0, 'o', color=fee_colors[i], markersize=10,
                 markeredgecolor='black', markeredgewidth=2, zorder=5)
        ax1.annotate(f'Break-even\n{be_sigma:.0f}% vol',
                     xy=(be_sigma, 0), xytext=(be_sigma + 8, 15),
                     fontsize=9, color=fee_colors[i], fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color=fee_colors[i], lw=1.5),
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                               edgecolor=fee_colors[i], alpha=0.8))

ax1.axhline(y=0, color='black', linestyle='--', linewidth=1.5, alpha=0.7)
ax1.fill_between(sigma_range * 100, -60, 0, alpha=0.05, color=MLRED)
ax1.fill_between(sigma_range * 100, 0, 200, alpha=0.05, color=MLGREEN)
ax1.text(15, -10, 'LOSS ZONE', fontsize=12, color=MLRED, fontweight='bold', alpha=0.5)
ax1.text(15, 50, 'PROFIT ZONE', fontsize=12, color=MLGREEN, fontweight='bold', alpha=0.5)

ax1.set_xlabel('Annualized Volatility (%)')
ax1.set_ylabel('Net LP Return (%)')
ax1.set_title('(a) Net LP Return vs Volatility', fontweight='bold')
ax1.legend(loc='upper right', framealpha=0.95)
ax1.set_xlim(5, 100)
ax1.set_ylim(-60, 200)
ax1.grid(alpha=0.3, linestyle='--')

# --- Panel (b): IL curve and fee lines ---
ax2.plot(sigma_range * 100, expected_ils * 100, color=MLRED, linewidth=3,
         label='Expected IL (negative)')

for i, (f, label) in enumerate(zip(fee_tiers, fee_labels)):
    annual_fee = f * V_TVL * 365
    ax2.axhline(y=-annual_fee * 100, color=fee_colors[i], linestyle='--', linewidth=2,
                label=f'Fee offset {label}: {annual_fee*100:.0f}%/yr', alpha=0.8)

ax2.set_xlabel('Annualized Volatility (%)')
ax2.set_ylabel('Expected Impermanent Loss (%)')
ax2.set_title('(b) IL vs Fee Offset by Tier', fontweight='bold')
ax2.legend(loc='lower left', fontsize=9, framealpha=0.95)
ax2.set_xlim(5, 100)
ax2.grid(alpha=0.3, linestyle='--')

# Formula annotation
ax2.text(0.98, 0.98, r'$IL = \frac{2\sqrt{r}}{1+r} - 1$' + '\n\n' +
         r'$R_{net} = f \cdot \frac{V}{TVL} \cdot 365 + IL$' + '\n\n' +
         f'V/TVL = {V_TVL:.1f} (daily)',
         transform=ax2.transAxes, fontsize=10, va='top', ha='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Reading guide
ax2.text(0.02, 0.02, 'LP profitable when fee line\n'
         'is below (more negative than)\n'
         'the IL curve at that volatility.',
         transform=ax2.transAxes, fontsize=9, va='bottom',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

fig.suptitle('LP Profitability Frontier: When Do Fees Offset Impermanent Loss?\n'
             'Adams et al. (2024): ~49.5% of Uniswap v3 LPs lose vs HODL',
             fontsize=15, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
