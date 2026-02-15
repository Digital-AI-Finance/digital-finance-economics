r"""Network Valuation Models: Metcalfe, Odlyzko, and Linear

Multi-panel override: comparative statics requires simultaneous visibility

Panel (a): Log-log comparison of three network value models.
Panel (b): Ratio of Metcalfe to Odlyzko valuation.
Panel (c): Ethereum network value overlay with fitted curves.

Economic Model:
$V_{Metcalfe} = \alpha n^2$, $V_{Odlyzko} = \beta n \ln(n)$, $V_{linear} = \gamma n$.
Fitted to Ethereum. Based on Metcalfe (2013), Odlyzko \& Tilly (2005).
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 11, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 10,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Parameters
alpha = 0.001
beta = 0.05
gamma = 1.0

# Network sizes (log scale): 100 to 1,000,000
n = np.logspace(2, 6, 500)

# Models
V_metcalfe = alpha * n**2
V_odlyzko = beta * n * np.log(n)
V_linear = gamma * n

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5.5))

# --- Panel (a): Log-log three curves ---
ax1.loglog(n, V_metcalfe, color=MLRED, linewidth=2.5, label=r'Metcalfe: $\alpha n^2$')
ax1.loglog(n, V_odlyzko, color=MLBLUE, linewidth=2.5, label=r'Odlyzko: $\beta n \ln(n)$')
ax1.loglog(n, V_linear, color=MLGREEN, linewidth=2.5, label=r'Linear: $\gamma n$')

ax1.fill_between(n, V_odlyzko, V_metcalfe, alpha=0.1, color=MLORANGE,
                 label='Metcalfe premium')
ax1.set_xlabel('Network Size $n$ (users)', fontweight='bold')
ax1.set_ylabel('Network Value $V$', fontweight='bold')
ax1.set_title('(a) Three Network Valuation\nModels (log-log)', fontweight='bold', color=MLPURPLE)
ax1.legend(loc='upper left', framealpha=0.9, fontsize=9)
ax1.grid(True, alpha=0.3, linestyle='--', which='both')

# --- Panel (b): Ratio Metcalfe / Odlyzko ---
ratio = V_metcalfe / V_odlyzko
ax2.semilogx(n, ratio, color=MLPURPLE, linewidth=2.5)
ax2.axhline(y=1, color='gray', linestyle=':', linewidth=1, alpha=0.7)
ax2.fill_between(n, 1, ratio, where=(ratio > 1), alpha=0.15, color=MLRED,
                 label='Metcalfe overvalues')

# Mark crossover and key points
cross_idx = np.argmin(np.abs(ratio - 1))
if ratio[0] < 1:
    ax2.plot(n[cross_idx], 1, 'o', color=MLRED, markersize=10, zorder=5)
    ax2.annotate(f'Crossover at\nn={n[cross_idx]:,.0f}',
                 xy=(n[cross_idx], 1), xytext=(n[cross_idx] * 3, 0.5),
                 fontsize=9, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.3),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                           edgecolor=MLRED, alpha=0.9))

ax2.set_xlabel('Network Size $n$ (users)', fontweight='bold')
ax2.set_ylabel('$V_{Metcalfe} / V_{Odlyzko}$', fontweight='bold')
ax2.set_title('(b) Metcalfe / Odlyzko Ratio\n(overvaluation risk)', fontweight='bold', color=MLPURPLE)
ax2.legend(loc='upper left', framealpha=0.9, fontsize=9)
ax2.grid(True, alpha=0.3, linestyle='--')

# --- Panel (c): Ethereum overlay ---
# Simulated Ethereum data: users and market cap (illustrative)
eth_users = np.array([1e3, 5e3, 2e4, 1e5, 3e5, 8e5, 2e6, 5e6,
                      1e7, 2e7, 5e7, 1e8])
# Market cap in $M (illustrative trajectory)
eth_mcap = np.array([0.5, 8, 100, 800, 3000, 12000, 50000, 120000,
                     250000, 350000, 400000, 420000])

# Fit curves to Ethereum range
n_eth = np.logspace(3, 8, 300)
V_met_eth = alpha * n_eth**2 / 1e6   # scale to $M
V_odl_eth = beta * n_eth * np.log(n_eth) / 1e3  # scale to $M
# Rescale for visual fit
scale_met = eth_mcap[6] / (alpha * eth_users[6]**2)
scale_odl = eth_mcap[6] / (beta * eth_users[6] * np.log(eth_users[6]))
V_met_fit = scale_met * alpha * n_eth**2
V_odl_fit = scale_odl * beta * n_eth * np.log(n_eth)

ax3.loglog(eth_users, eth_mcap, 'o', color=MLORANGE, markersize=8,
           label='Ethereum (illustrative)', zorder=5)
ax3.loglog(n_eth, V_met_fit, color=MLRED, linewidth=2, linestyle='--',
           label=r'Metcalfe fit: $\alpha n^2$')
ax3.loglog(n_eth, V_odl_fit, color=MLBLUE, linewidth=2, linestyle='--',
           label=r'Odlyzko fit: $\beta n \ln(n)$')

ax3.set_xlabel('Active Addresses ($n$)', fontweight='bold')
ax3.set_ylabel('Market Cap (\\$M)', fontweight='bold')
ax3.set_title('(c) Ethereum: Metcalfe vs\nOdlyzko Fit', fontweight='bold', color=MLPURPLE)
ax3.legend(loc='upper left', framealpha=0.9, fontsize=9)
ax3.grid(True, alpha=0.3, linestyle='--', which='both')

# Annotate saturation
ax3.annotate('Saturation:\nMetcalfe diverges',
             xy=(eth_users[-1], eth_mcap[-1]),
             xytext=(eth_users[-1] / 10, eth_mcap[-1] * 3),
             fontsize=9, fontweight='bold', color=MLRED,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.3),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                       edgecolor=MLRED, alpha=0.9))

fig.suptitle('Network Value Estimation: Metcalfe, Odlyzko & Empirical Fit\n'
             'Metcalfe (2013), Odlyzko & Tilly (2005), Briscoe et al. (2006)',
             fontweight='bold', fontsize=13, color=MLPURPLE, y=1.03)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
