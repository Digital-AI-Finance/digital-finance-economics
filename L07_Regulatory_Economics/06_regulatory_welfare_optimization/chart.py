r"""Regulatory Welfare Optimization: Marginal Benefit vs Marginal Cost

# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  $MB(r) = \frac{a}{1+br}$, $MC(r) = c + dr$. Based on Harberger (1964), Posner (1974).
  Welfare: $W(r) = \int_0^r [MB(s) - MC(s)]\,ds$
  Optimal regulation $r^*$ where $MB(r^*) = MC(r^*)$

Citation: Harberger (1964) - Taxation, Resource Allocation, and Welfare;
          Posner (1974) - Theories of Economic Regulation
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
a, b = 100, 2
c, d = 10, 15
r = np.linspace(0, 5, 500)

# Marginal benefit and cost
MB = a / (1 + b * r)
MC = c + d * r

# Find intersection: a/(1+b*r) = c + d*r
# a = (c + d*r)(1 + b*r) = c + cb*r + d*r + db*r^2
# db*r^2 + (cb + d)*r + (c - a) = 0
coeffs = [d * b, c * b + d, c - a]
roots = np.roots(coeffs)
r_star = roots[roots > 0].min().real  # positive root

MB_star = a / (1 + b * r_star)
MC_star = c + d * r_star

# Welfare: cumulative integral of (MB - MC) from 0 to r
net_benefit = MB - MC
W = np.cumsum(net_benefit) * (r[1] - r[0])

W_star_idx = np.argmin(np.abs(r - r_star))
W_star = W[W_star_idx]

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Panel (a): MB/MC curves with intersection
ax1.plot(r, MB, color=MLBLUE, lw=2.5, label=r'$MB(r) = \frac{100}{1+2r}$')
ax1.plot(r, MC, color=MLRED, lw=2.5, label=r'$MC(r) = 10 + 15r$')

# Shade net benefit region (MB > MC)
mask_positive = r <= r_star
ax1.fill_between(r[mask_positive], MC[mask_positive], MB[mask_positive],
                 alpha=0.2, color=MLGREEN, label='Net benefit (MB > MC)')

# Shade deadweight loss region (MC > MB)
mask_beyond = r > r_star
r_beyond = r[mask_beyond]
MB_beyond = MB[mask_beyond]
MC_beyond = MC[mask_beyond]
# Only shade up to r=4 for visual clarity
mask_show = r_beyond <= 4
if mask_show.any():
    ax1.fill_between(r_beyond[mask_show], MB_beyond[mask_show], MC_beyond[mask_show],
                     alpha=0.2, color=MLRED, label='DWL (over-regulation)')

# Intersection point
ax1.plot(r_star, MB_star, 'o', color=MLPURPLE, ms=12, zorder=5, markeredgecolor='black', markeredgewidth=1.5)
ax1.axvline(r_star, color=MLPURPLE, ls='--', alpha=0.5, lw=1.5)
ax1.annotate(f'$r^* = {r_star:.2f}$\nMB = MC = ${MB_star:.1f}',
             xy=(r_star, MB_star), xytext=(r_star + 0.8, MB_star + 15),
             fontsize=11, color=MLPURPLE,
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLPURPLE, alpha=0.9))

ax1.set_xlabel('Regulation intensity $r$')
ax1.set_ylabel('Marginal value ($/unit)')
ax1.set_title('(a) Marginal Benefit vs. Marginal Cost')
ax1.legend(loc='upper right', fontsize=10)
ax1.set_xlim(0, 4.5)
ax1.set_ylim(0, 110)
ax1.grid(True, alpha=0.3)

# Worked example annotation
ax1.text(0.03, 0.03, 'KYC example: $25/customer cost\n'
         'vs. $150/prevented fraud case\n'
         'Net benefit positive until $r^*$',
         transform=ax1.transAxes, fontsize=9,
         verticalalignment='bottom',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor=MLORANGE, alpha=0.9))

# Panel (b): Welfare W(r) inverted-U
ax2.plot(r, W, color=MLPURPLE, lw=2.5, label=r'$W(r) = \int_0^r [MB(s) - MC(s)]\,ds$')
ax2.axhline(0, color='black', ls='-', lw=0.5, alpha=0.5)

# Mark optimal
ax2.plot(r[W_star_idx], W_star, 'o', color=MLRED, ms=12, zorder=5,
         markeredgecolor='black', markeredgewidth=1.5)
ax2.axvline(r_star, color=MLPURPLE, ls='--', alpha=0.5, lw=1.5)
ax2.annotate(f'Maximum welfare\n$W(r^*) = {W_star:.1f}$',
             xy=(r_star, W_star), xytext=(r_star + 1.0, W_star - 15),
             fontsize=11, color=MLRED,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLRED, alpha=0.9))

# Mark zero-crossing (where W returns to 0)
zero_crossings = np.where(np.diff(np.sign(W[W_star_idx:])))[0]
if len(zero_crossings) > 0:
    r_zero = r[W_star_idx + zero_crossings[0]]
    ax2.plot(r_zero, 0, 's', color=MLORANGE, ms=10, zorder=5)
    ax2.annotate(f'$W = 0$ at $r = {r_zero:.2f}$\n(regulation exceeds\nall benefits)',
                 xy=(r_zero, 0), xytext=(r_zero + 0.5, -30),
                 fontsize=10, color=MLORANGE,
                 arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=1.5),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLORANGE, alpha=0.9))

# Shade regions
ax2.fill_between(r[:W_star_idx+1], 0, W[:W_star_idx+1], alpha=0.15, color=MLGREEN)
if len(zero_crossings) > 0:
    end_idx = W_star_idx + zero_crossings[0] + 1
    ax2.fill_between(r[W_star_idx:end_idx], 0, W[W_star_idx:end_idx], alpha=0.15, color=MLRED)

ax2.set_xlabel('Regulation intensity $r$')
ax2.set_ylabel('Total welfare $W(r)$')
ax2.set_title('(b) Welfare as Inverted-U Function of Regulation')
ax2.legend(loc='upper right', fontsize=10)
ax2.set_xlim(0, 4.5)
ax2.grid(True, alpha=0.3)

# Economic insight
ax2.text(0.03, 0.03, 'Under-regulation: welfare gains available\n'
         'Over-regulation: costs exceed benefits\n'
         'DWL = $0.5 \\times \\Delta P \\times \\Delta Q$ (Harberger)',
         transform=ax2.transAxes, fontsize=9,
         verticalalignment='bottom',
         bbox=dict(boxstyle='round', facecolor=MLLAVENDER, alpha=0.3))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
