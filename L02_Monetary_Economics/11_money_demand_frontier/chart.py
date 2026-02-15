r"""Money Demand Frontier: Mean-Variance Analysis
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
    Mean-variance frontier: $E[r]$ vs $\sigma$.
    Based on Markowitz (1952) applied to money.

    Assets: Cash(0, 0), Savings(0.03, 0.01), BTC(0.50, 0.65),
    USDT(0.0, 0.05), CBDC(0.01, 0.005), ETH(0.40, 0.75).

    Efficient frontier: minimum variance portfolio for each target return.
    Money demand = intersection of investor risk preference with frontier.
    Key insight: traditional money clusters near origin (low risk, low return);
    crypto assets are far in the upper-right (high risk, high return).

Citation: Markowitz (1952) - Portfolio Selection, applied to money taxonomy.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.optimize import minimize

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

# --- Asset parameters: (name, E[r], sigma, color, marker) ---
assets = [
    ('Cash',     0.00, 0.000, MLBLUE,    'o'),
    ('Savings',  0.03, 0.010, MLLAVENDER, 's'),
    ('CBDC',     0.01, 0.005, MLGREEN,   'D'),
    ('USDT',     0.00, 0.050, MLGREEN,   '^'),
    ('BTC',      0.50, 0.650, MLORANGE,  'P'),
    ('ETH',      0.40, 0.750, MLPURPLE,  '*'),
]

names = [a[0] for a in assets]
returns = np.array([a[1] for a in assets])
sigmas = np.array([a[2] for a in assets])
colors = [a[3] for a in assets]
markers = [a[4] for a in assets]

# --- Build covariance matrix (simplified: diagonal + mild correlations) ---
n_assets = len(assets)
# Correlation matrix
corr = np.eye(n_assets)
# BTC-ETH correlation ~0.7
corr[4, 5] = corr[5, 4] = 0.70
# BTC-USDT mild negative ~-0.1
corr[3, 4] = corr[4, 3] = -0.10
corr[3, 5] = corr[5, 3] = -0.10
# Cash/Savings/CBDC very low correlation with crypto
for i in range(3):
    for j in range(3, 6):
        corr[i, j] = corr[j, i] = 0.05

cov = np.outer(sigmas, sigmas) * corr

# Fix Cash: zero variance means we need to handle it as risk-free
# For frontier computation, use assets 1-5 (exclude cash)
risky_idx = [1, 2, 3, 4, 5]
mu_risky = returns[risky_idx]
cov_risky = cov[np.ix_(risky_idx, risky_idx)]
# Add small regularization
cov_risky += np.eye(len(risky_idx)) * 1e-8

def min_var_portfolio(target_ret, mu, cov_mat):
    """Find minimum variance portfolio for target return."""
    n = len(mu)
    def objective(w):
        return w @ cov_mat @ w
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'eq', 'fun': lambda w: w @ mu - target_ret}
    ]
    bounds = [(-0.5, 1.5)] * n  # allow mild short
    w0 = np.ones(n) / n
    result = minimize(objective, w0, method='SLSQP',
                     constraints=constraints, bounds=bounds)
    if result.success:
        port_var = result.x @ cov_mat @ result.x
        return np.sqrt(max(0, port_var)), target_ret
    return None, None

# Compute frontier
target_returns = np.linspace(-0.02, 0.55, 200)
frontier_sigma = []
frontier_ret = []
for tr in target_returns:
    s, r = min_var_portfolio(tr, mu_risky, cov_risky)
    if s is not None:
        frontier_sigma.append(s)
        frontier_ret.append(r)

frontier_sigma = np.array(frontier_sigma)
frontier_ret = np.array(frontier_ret)

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# === Panel (a): Full scatter with frontier ===
# Plot frontier
ax1.plot(frontier_sigma * 100, frontier_ret * 100, color=MLRED, linewidth=2,
         linestyle='-', alpha=0.6, label='Efficient Frontier', zorder=3)
ax1.fill_betweenx(frontier_ret * 100, frontier_sigma * 100,
                   frontier_sigma * 100 + 10, alpha=0.03, color=MLRED)

# Plot individual assets
for i, (name, ret, sig, color, marker) in enumerate(assets):
    ax1.scatter(sig * 100, ret * 100, c=color, marker=marker, s=150,
                edgecolors='black', linewidths=0.8, zorder=5, label=name)
    # Labels with offset
    offsets = {
        'Cash': (1, 2), 'Savings': (1, 2), 'CBDC': (1, -3),
        'USDT': (2, -3), 'BTC': (-5, 3), 'ETH': (2, -4)
    }
    dx, dy = offsets.get(name, (2, 2))
    ax1.annotate(name, (sig * 100, ret * 100),
                xytext=(sig * 100 + dx, ret * 100 + dy),
                fontsize=10, fontweight='bold', color=color,
                arrowprops=dict(arrowstyle='-', color='gray', alpha=0.5, lw=0.5))

# Regions
ax1.axhspan(-5, 5, xmin=0, xmax=0.15, color=MLBLUE, alpha=0.03)
ax1.text(2, -2, 'Money region\n(low risk, low return)', fontsize=8,
         color=MLBLUE, alpha=0.7, style='italic')
ax1.text(55, 15, 'Speculative region\n(high risk, high return)', fontsize=8,
         color=MLORANGE, alpha=0.7, style='italic')

ax1.set_xlabel('Volatility $\\sigma$ (%)', fontweight='bold')
ax1.set_ylabel('Expected Return E[r] (%)', fontweight='bold')
ax1.set_title('(a) Full Money Demand Frontier', fontweight='bold', color=MLPURPLE)
ax1.legend(loc='upper left', framealpha=0.9, fontsize=8, ncol=2)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(-2, 80)
ax1.set_ylim(-5, 60)

# === Panel (b): Zoomed low-risk region ===
ax2.plot(frontier_sigma * 100, frontier_ret * 100, color=MLRED, linewidth=2,
         linestyle='-', alpha=0.6, label='Efficient Frontier', zorder=3)

# Only plot low-risk assets with bigger markers
low_risk_assets = [0, 1, 2, 3]  # Cash, Savings, CBDC, USDT
for i in low_risk_assets:
    name, ret, sig, color, marker = assets[i]
    ax2.scatter(sig * 100, ret * 100, c=color, marker=marker, s=250,
                edgecolors='black', linewidths=1, zorder=5, label=name)
    # Explicit labels
    offsets_zoom = {
        'Cash': (0.3, 0.3), 'Savings': (0.3, 0.3),
        'CBDC': (0.3, -0.5), 'USDT': (0.3, -0.5)
    }
    dx, dy = offsets_zoom.get(name, (0.3, 0.3))
    ax2.annotate(f'{name}\n(r={ret*100:.1f}%, $\\sigma$={sig*100:.1f}%)',
                (sig * 100, ret * 100),
                xytext=(sig * 100 + dx, ret * 100 + dy),
                fontsize=9, fontweight='bold', color=color,
                arrowprops=dict(arrowstyle='->', color=color, lw=1),
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                         edgecolor=color, alpha=0.8))

# CBDC advantage annotation
ax2.annotate('CBDC: best risk-return\namong stable monies',
             xy=(0.5, 1.0), xytext=(2.5, 3.0),
             fontsize=9, fontweight='bold', color=MLGREEN,
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                      edgecolor=MLGREEN, alpha=0.9))

ax2.set_xlabel('Volatility $\\sigma$ (%)', fontweight='bold')
ax2.set_ylabel('Expected Return E[r] (%)', fontweight='bold')
ax2.set_title('(b) Zoomed: Low-Risk Money', fontweight='bold', color=MLPURPLE)
ax2.legend(loc='upper left', framealpha=0.9, fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-0.5, 7)
ax2.set_ylim(-1.5, 5)

fig.suptitle('Money Demand Frontier: Markowitz Applied to Digital Money',
             fontsize=14, fontweight='bold', color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Money demand frontier chart saved to chart.pdf and chart.png")
