r"""Rochet-Tirole Two-Sided Platform Optimization

Multi-panel chart showing platform profit optimization over buyer and seller
prices with cross-side network effects, and welfare comparison.

# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model: Rochet-Tirole Two-Sided Pricing with Cross-Side Effects
- Platform profit: $\Pi = (p_B - c_B)n_B + (p_S - c_S)n_S$
- Buyer demand: $n_B = a_B - b_B p_B + d_B n_S$
- Seller demand: $n_S = a_S - b_S p_S + d_S n_B$
- Solving simultaneous system for equilibrium demands given prices.

Calibration: a_B=100, b_B=20, d_B=0.3, c_B=0.5,
             a_S=80, b_S=15, d_S=0.2, c_S=0.3

Citation: Rochet & Tirole (2003, 2006) - Platform Competition in Two-Sided Markets
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# --- Model parameters ---
a_B, b_B, d_B, c_B = 100, 20, 0.3, 0.5
a_S, b_S, d_S, c_S = 80, 15, 0.2, 0.3


def solve_demands(p_B, p_S):
    """Solve simultaneous demand system:
    n_B = a_B - b_B*p_B + d_B*n_S
    n_S = a_S - b_S*p_S + d_S*n_B
    Substituting: n_B = (a_B - b_B*p_B + d_B*(a_S - b_S*p_S + d_S*n_B))/(1)
    => n_B(1 - d_B*d_S) = a_B - b_B*p_B + d_B*(a_S - b_S*p_S)
    """
    denom = 1 - d_B * d_S
    n_B = (a_B - b_B * p_B + d_B * (a_S - b_S * p_S)) / denom
    n_S = (a_S - b_S * p_S + d_S * (a_B - b_B * p_B)) / denom
    return np.maximum(n_B, 0), np.maximum(n_S, 0)


def profit(p_B, p_S):
    n_B, n_S = solve_demands(p_B, p_S)
    return (p_B - c_B) * n_B + (p_S - c_S) * n_S


def welfare(p_B, p_S):
    """W = CS_B + CS_S + PS. CS approx = 0.5 * n^2 / b (area under demand curve)."""
    n_B, n_S = solve_demands(p_B, p_S)
    cs_B = 0.5 * n_B**2 / b_B
    cs_S = 0.5 * n_S**2 / b_S
    ps = (p_B - c_B) * n_B + (p_S - c_S) * n_S
    return cs_B + cs_S + ps


# --- Panel (a): Contour plot of profit ---
pB_range = np.linspace(0.1, 5.0, 200)
pS_range = np.linspace(0.1, 5.0, 200)
PB, PS = np.meshgrid(pB_range, pS_range)

Pi = np.zeros_like(PB)
for i in range(PB.shape[0]):
    for j in range(PB.shape[1]):
        Pi[i, j] = profit(PB[i, j], PS[i, j])

# Find optimal (p_B*, p_S*) via grid search
opt_idx = np.unravel_index(np.argmax(Pi), Pi.shape)
pB_opt = PB[opt_idx]
pS_opt = PS[opt_idx]
pi_opt = Pi[opt_idx]

# Social optimum: maximize welfare
W_grid = np.zeros_like(PB)
for i in range(PB.shape[0]):
    for j in range(PB.shape[1]):
        W_grid[i, j] = welfare(PB[i, j], PS[i, j])

soc_idx = np.unravel_index(np.argmax(W_grid), W_grid.shape)
pB_soc = PB[soc_idx]
pS_soc = PS[soc_idx]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel (a): Contour
levels = np.linspace(np.percentile(Pi[Pi > 0], 10), pi_opt * 0.98, 12)
cs = ax1.contourf(PB, PS, Pi, levels=levels, cmap='Blues', alpha=0.8)
ax1.contour(PB, PS, Pi, levels=levels, colors=MLPURPLE, linewidths=0.5, alpha=0.6)
cbar = fig.colorbar(cs, ax=ax1, shrink=0.8)
cbar.set_label('Platform Profit', fontsize=12)

# Mark monopoly optimal
ax1.plot(pB_opt, pS_opt, 'o', color=MLRED, markersize=12, zorder=5)
ax1.annotate(f'Monopoly optimum\n($p_B$={pB_opt:.1f}, $p_S$={pS_opt:.1f})',
             xy=(pB_opt, pS_opt), xytext=(pB_opt + 0.8, pS_opt + 0.8),
             fontsize=11,
             bbox=dict(boxstyle='round,pad=0.4', facecolor=MLLAVENDER, alpha=0.9),
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5))

# Mark social optimum
ax1.plot(pB_soc, pS_soc, 's', color=MLGREEN, markersize=12, zorder=5)
ax1.annotate(f'Social optimum\n($p_B$={pB_soc:.1f}, $p_S$={pS_soc:.1f})',
             xy=(pB_soc, pS_soc), xytext=(pB_soc - 1.8, pS_soc - 1.0),
             fontsize=11,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#d4edda', alpha=0.9),
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5))

ax1.set_xlabel('Buyer Price ($p_B$)')
ax1.set_ylabel('Seller Price ($p_S$)')
ax1.set_title('(a) Platform Profit Landscape')
ax1.grid(True, alpha=0.2, linestyle='--')

# --- Panel (b): Welfare comparison bars ---
# Compute welfare components at monopoly and social optima
n_B_mono, n_S_mono = solve_demands(pB_opt, pS_opt)
n_B_soc, n_S_soc = solve_demands(pB_soc, pS_soc)

cs_B_mono = 0.5 * n_B_mono**2 / b_B
cs_S_mono = 0.5 * n_S_mono**2 / b_S
ps_mono = profit(pB_opt, pS_opt)

cs_B_soc = 0.5 * n_B_soc**2 / b_B
cs_S_soc = 0.5 * n_S_soc**2 / b_S
ps_soc = profit(pB_soc, pS_soc)

labels = ['Monopoly\nPricing', 'Socially\nOptimal']
x_pos = np.array([0, 1])
bar_width = 0.5

# Stacked bars
bars1 = ax2.bar(x_pos, [cs_B_mono, cs_B_soc], bar_width,
                label='$CS_B$ (buyer surplus)', color=MLBLUE, alpha=0.85)
bars2 = ax2.bar(x_pos, [cs_S_mono, cs_S_soc], bar_width,
                bottom=[cs_B_mono, cs_B_soc],
                label='$CS_S$ (seller surplus)', color=MLORANGE, alpha=0.85)
bars3 = ax2.bar(x_pos, [ps_mono, ps_soc], bar_width,
                bottom=[cs_B_mono + cs_S_mono, cs_B_soc + cs_S_soc],
                label='$PS$ (platform profit)', color=MLPURPLE, alpha=0.85)

# DWL annotation
total_mono = cs_B_mono + cs_S_mono + ps_mono
total_soc = cs_B_soc + cs_S_soc + ps_soc
dwl = total_soc - total_mono

ax2.annotate(f'DWL = {dwl:.0f}',
             xy=(0, total_mono), xytext=(0.4, total_mono + dwl * 0.4),
             fontsize=12, fontweight='bold', color=MLRED,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8d7da', alpha=0.9),
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5))

# Total welfare labels
for i, total in enumerate([total_mono, total_soc]):
    ax2.text(x_pos[i], total + 15, f'W={total:.0f}',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

ax2.set_xticks(x_pos)
ax2.set_xticklabels(labels)
ax2.set_ylabel('Welfare Components')
ax2.set_title('(b) Welfare Decomposition')
ax2.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax2.grid(True, alpha=0.2, linestyle='--', axis='y')

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
