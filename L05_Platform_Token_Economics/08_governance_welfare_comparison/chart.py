"""Governance Welfare Comparison: 1T1V vs Quadratic Voting

Multi-panel chart comparing welfare outcomes under different voting mechanisms.

Economic Model:
  One-Token-One-Vote welfare: $W_{1T1V} = \sum_i v_i \cdot w_i$
  where $w_i = t_i / \sum t_j$ (vote weight proportional to token holdings).
  Quadratic Voting welfare: $W_{QV} = \sum_i v_i \cdot \sqrt{t_i}$
  where cost of $k$ votes = $k^2$ tokens.
  Based on Weyl \& Lalley (2018), Buterin et al. (2019).

# Multi-panel override: comparative statics requires simultaneous visibility

Citation: Weyl & Lalley (2018) - Quadratic Voting; Buterin, Hitzig & Weyl (2019)
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

# --- Model ---
# Generate voters with varying token holdings and preference intensities
n_voters = 1000

def generate_voters(n, gini_target):
    """Generate token holdings with approximate target Gini coefficient.
    Uses Pareto distribution to control inequality."""
    # Pareto shape parameter: higher shape = lower inequality
    # Gini for Pareto = 1/(2*alpha - 1), so alpha = (1 + 1/Gini)/2
    if gini_target < 0.05:
        gini_target = 0.05
    alpha = (1.0 + 1.0 / gini_target) / 2.0
    alpha = max(alpha, 1.01)  # ensure valid Pareto
    holdings = np.random.pareto(alpha, n) + 1.0
    holdings = holdings / holdings.sum()  # normalize to shares
    return holdings

def compute_gini(shares):
    """Compute Gini coefficient."""
    shares_sorted = np.sort(shares)
    n = len(shares_sorted)
    index = np.arange(1, n + 1)
    return float(np.sum((2 * index - n - 1) * shares_sorted) / (n * np.sum(shares_sorted)))

def welfare_1t1v(values, holdings):
    """1T1V welfare: weight by token holdings."""
    weights = holdings / holdings.sum()
    return np.sum(values * weights)

def welfare_qv(values, holdings):
    """QV welfare: weight by sqrt of token holdings."""
    weights = np.sqrt(holdings)
    weights = weights / weights.sum()
    return np.sum(values * weights)

def welfare_equal(values):
    """Equal-weight (one-person-one-vote) welfare (benchmark)."""
    return np.mean(values)

# --- Sweep over Gini values ---
gini_targets = np.linspace(0.1, 0.9, 30)
welfare_1t1v_vals = []
welfare_qv_vals = []
welfare_equal_vals = []
actual_ginis = []

for g in gini_targets:
    holdings = generate_voters(n_voters, g)
    actual_g = compute_gini(holdings)
    actual_ginis.append(actual_g)

    # Preference intensity: random, independent of wealth
    values = np.random.normal(0.5, 0.2, n_voters)
    values = np.clip(values, 0, 1)

    w_1t1v = welfare_1t1v(values, holdings)
    w_qv = welfare_qv(values, holdings)
    w_eq = welfare_equal(values)

    welfare_1t1v_vals.append(w_1t1v)
    welfare_qv_vals.append(w_qv)
    welfare_equal_vals.append(w_eq)

welfare_1t1v_vals = np.array(welfare_1t1v_vals)
welfare_qv_vals = np.array(welfare_qv_vals)
welfare_equal_vals = np.array(welfare_equal_vals)
actual_ginis = np.array(actual_ginis)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Welfare comparison across Gini ---
ax1.plot(actual_ginis, welfare_equal_vals, color=MLLAVENDER, linewidth=2,
         linestyle=':', label='1-Person-1-Vote (benchmark)', zorder=2)
ax1.plot(actual_ginis, welfare_qv_vals, color=MLGREEN, linewidth=2.5,
         label='Quadratic Voting', zorder=3)
ax1.plot(actual_ginis, welfare_1t1v_vals, color=MLRED, linewidth=2.5,
         label='1-Token-1-Vote', zorder=3)

# Shade the welfare gap
ax1.fill_between(actual_ginis, welfare_qv_vals, welfare_1t1v_vals,
                 alpha=0.2, color=MLGREEN, label='QV welfare gain')

# Mark crypto-relevant Gini levels
crypto_ginis = [0.65, 0.85]
crypto_labels = ['ETH (Gini~0.65)', 'BTC (Gini~0.85)']
crypto_colors = [MLBLUE, MLORANGE]

for cg, cl, cc in zip(crypto_ginis, crypto_labels, crypto_colors):
    idx = np.argmin(np.abs(actual_ginis - cg))
    ax1.axvline(x=actual_ginis[idx], color=cc, linestyle='--', alpha=0.6, linewidth=1.5)
    ax1.text(actual_ginis[idx] + 0.01, ax1.get_ylim()[0] + 0.01, cl,
             fontsize=9, color=cc, fontweight='bold', rotation=90, va='bottom')

ax1.set_xlabel('Token Inequality (Gini Coefficient)')
ax1.set_ylabel('Social Welfare (W)')
ax1.set_title('(a) Welfare: QV vs 1T1V Across Inequality')
ax1.legend(loc='lower left', fontsize=9, framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--')

# Annotation
ax1.text(0.55, 0.92, 'Higher Gini = more concentrated tokens\n'
         'QV protects minority preferences\n'
         '1T1V amplifies whale dominance',
         transform=ax1.transAxes, fontsize=9, va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                   edgecolor=MLORANGE, alpha=0.9))

# --- Panel (b): Voting power distribution for specific Gini ---
# Show vote weight distribution for Gini ~ 0.8
holdings_high = generate_voters(n_voters, 0.8)
holdings_sorted = np.sort(holdings_high)[::-1]  # descending

# Top 10 holders: 1T1V weight vs QV weight
top_n = 10
top_holdings = holdings_sorted[:top_n]
rest_holdings = holdings_sorted[top_n:]

# 1T1V weights
w_1t1v_top = top_holdings / holdings_sorted.sum()
w_1t1v_rest = rest_holdings.sum() / holdings_sorted.sum()

# QV weights
sqrt_all = np.sqrt(holdings_sorted)
w_qv_top = sqrt_all[:top_n] / sqrt_all.sum()
w_qv_rest = sqrt_all[top_n:].sum() / sqrt_all.sum()

x_pos = np.arange(top_n + 1)
width = 0.35

bars_1t1v = np.append(w_1t1v_top, w_1t1v_rest)
bars_qv = np.append(w_qv_top, w_qv_rest)

rects1 = ax2.bar(x_pos - width/2, bars_1t1v * 100, width, color=MLRED, alpha=0.8,
                 label='1T1V Weight (%)')
rects2 = ax2.bar(x_pos + width/2, bars_qv * 100, width, color=MLGREEN, alpha=0.8,
                 label='QV Weight (%)')

labels = [f'#{i+1}' for i in range(top_n)] + ['Rest\n(990)']
ax2.set_xticks(x_pos)
ax2.set_xticklabels(labels, fontsize=9)

# Highlight the whale
ax2.annotate(f'Whale: {bars_1t1v[0]*100:.1f}% (1T1V)\nvs {bars_qv[0]*100:.1f}% (QV)',
             xy=(0, bars_1t1v[0] * 100),
             xytext=(2.5, bars_1t1v[0] * 100 * 0.85),
             fontsize=10, fontweight='bold', color=MLRED,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLRED, alpha=0.9))

# Community power
ax2.annotate(f'Community: {bars_1t1v[-1]*100:.1f}% (1T1V)\nvs {bars_qv[-1]*100:.1f}% (QV)',
             xy=(top_n, bars_qv[-1] * 100),
             xytext=(top_n - 3.5, max(bars_qv[-1], bars_1t1v[-1]) * 100 + 5),
             fontsize=10, fontweight='bold', color=MLGREEN,
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLGREEN, alpha=0.9))

ax2.set_xlabel('Voter Rank')
ax2.set_ylabel('Voting Weight (%)')
ax2.set_title('(b) Vote Weight Distribution (Gini = 0.8)')
ax2.legend(loc='upper right', fontsize=9, framealpha=0.95)
ax2.grid(True, alpha=0.3, linestyle='--', axis='y')

# QV formula box
ax2.text(0.35, 0.95, 'QV: cost of k votes = $k^2$ tokens\n'
         'Whales pay quadratically more\nfor marginal influence',
         transform=ax2.transAxes, fontsize=9, va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor=MLLAVENDER, alpha=0.3))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
