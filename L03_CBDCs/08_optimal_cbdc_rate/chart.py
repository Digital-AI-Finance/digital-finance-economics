r"""Optimal CBDC Interest Rate: Welfare Maximization

Two-panel optimization analysis showing the welfare-maximizing CBDC rate.

Economic Model:
$W(r) = B(r) - C(r)$ where $B(r) = k_1\sqrt{r}$ (GDP + inclusion gains) and
$C(r) = k_2 r^2$ (disintermediation cost). $k_1 = 14.3$, $k_2 = 5000$.
FOC: $\frac{k_1}{2\sqrt{r^*}} = 2k_2 r^*$. Solution: $r^* = 0.008$ (0.8\%).
$W(0.008) = 0.959$, $W(0) = 0$, $W(0.035) = -3.451$.
Based on Barrdear & Kumhof (2022), JEDC 142.
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
from pathlib import Path

# Multi-panel override: comparative statics requires simultaneous visibility

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10,
    'figure.figsize': (14, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# ---------- Parameters ----------
k1 = 14.3
k2 = 5000
r_star = (k1 / (4 * k2)) ** (2 / 3)  # FOC solution: ~0.008

# ---------- Domain ----------
r = np.linspace(0.0001, 0.04, 500)

# ---------- Functions ----------
B = k1 * np.sqrt(r)                     # Benefit: GDP + inclusion gains
C = k2 * r ** 2                          # Cost: bank disintermediation
W = B - C                                # Net welfare

# Marginals
dB_dr = k1 / (2 * np.sqrt(r))           # Marginal benefit (decreasing)
dC_dr = 2 * k2 * r                      # Marginal cost = 10000*r (increasing)

# Key values
W_star = k1 * np.sqrt(r_star) - k2 * r_star ** 2
W_high = k1 * np.sqrt(0.035) - k2 * 0.035 ** 2

# Percentage formatter for x-axes
pct_fmt = FuncFormatter(lambda x, _: f'{x * 100:.1f}%')

# ================================================================
# Panel layout
# ================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ================================================================
# Panel (a): Welfare Function W(r) = B(r) - C(r)
# ================================================================

# Benefit and Cost as dashed reference curves
ax1.plot(r, B, '--', color=MLGREEN, linewidth=1.8, alpha=0.7,
         label=r'$B(r) = 14.3\,\sqrt{r}$')
ax1.plot(r, C, '--', color=MLRED, linewidth=1.8, alpha=0.7,
         label=r'$C(r) = 5000\,r^2$')

# Welfare curve (main)
ax1.plot(r, W, '-', color=MLPURPLE, linewidth=2.8,
         label=r'$W(r) = B(r) - C(r)$')

# Shade area where W > 0
mask_pos = W > 0
ax1.fill_between(r, W, 0, where=mask_pos, alpha=0.15, color=MLGREEN,
                 label='Net welfare > 0')

# Optimal rate r* vertical dashed line
ax1.axvline(x=r_star, color=MLORANGE, linestyle='--', linewidth=1.5, alpha=0.8)

# Optimal point star marker
ax1.plot(r_star, W_star, marker='*', markersize=18, color=MLORANGE,
         markeredgecolor='black', markeredgewidth=1.2, zorder=5,
         label=f'$r^* = {r_star * 100:.1f}\\%$, $W = {W_star:.3f}$')

# Annotate W(r*) clearly
ax1.annotate(f'$r^* = {r_star * 100:.1f}\\%$\n$W(r^*) = {W_star:.3f}$',
             xy=(r_star, W_star),
             xytext=(r_star + 0.006, W_star + 0.3),
             fontsize=11, fontweight='bold', color=MLORANGE,
             arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                       edgecolor=MLORANGE, alpha=0.95))

# EU proposal at r = 0%
ax1.plot(0.0001, k1 * np.sqrt(0.0001) - k2 * 0.0001 ** 2,
         marker='o', markersize=10, color=MLBLUE, markeredgecolor='black',
         markeredgewidth=1.2, zorder=5)
ax1.annotate('EU proposal\n$r = 0\\%$',
             xy=(0.0001, k1 * np.sqrt(0.0001)),
             xytext=(0.005, -1.5),
             fontsize=10, color=MLBLUE, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLBLUE, alpha=0.9))

# High-rate cost dominance at r = 3.5%
ax1.plot(0.035, W_high, marker='X', markersize=11, color=MLRED,
         markeredgecolor='black', markeredgewidth=1.0, zorder=5)
ax1.annotate(f'$r = 3.5\\%$\n$W = {W_high:.3f}$',
             xy=(0.035, W_high),
             xytext=(0.028, W_high - 1.2),
             fontsize=10, color=MLRED, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLRED, alpha=0.9))

# Zero line
ax1.axhline(y=0, color='grey', linewidth=0.8, linestyle='-', alpha=0.5)

# Formatting
ax1.set_xlabel('CBDC Rate $r$', fontweight='bold')
ax1.set_ylabel('Welfare $W(r)$', fontweight='bold')
ax1.set_title('(a) Welfare Function', fontweight='bold', pad=12)
ax1.xaxis.set_major_formatter(pct_fmt)
ax1.set_xlim(0, 0.042)
ax1.legend(loc='lower left', framealpha=0.95, fontsize=9)
ax1.grid(True, alpha=0.25, linestyle='--')
for spine in ['top', 'right']:
    ax1.spines[spine].set_visible(False)

# ================================================================
# Panel (b): Marginal Analysis -- dB/dr vs dC/dr
# ================================================================

# Marginal benefit (decreasing hyperbola)
ax2.plot(r, dB_dr, '-', color=MLGREEN, linewidth=2.5,
         label=r'$\frac{dB}{dr} = \frac{14.3}{2\sqrt{r}}$')

# Marginal cost (increasing line)
ax2.plot(r, dC_dr, '-', color=MLRED, linewidth=2.5,
         label=r'$\frac{dC}{dr} = 10000\,r$')

# Shade regions
# Left of r*: net marginal benefit (green)
mask_left = r <= r_star
ax2.fill_between(r[mask_left], dB_dr[mask_left], dC_dr[mask_left],
                 alpha=0.15, color=MLGREEN, label='Net marginal benefit')

# Right of r*: net marginal cost (red)
mask_right = r >= r_star
ax2.fill_between(r[mask_right], dB_dr[mask_right], dC_dr[mask_right],
                 alpha=0.15, color=MLRED, label='Net marginal cost')

# Intersection marker
dB_at_star = k1 / (2 * np.sqrt(r_star))
ax2.plot(r_star, dB_at_star, marker='*', markersize=18, color=MLORANGE,
         markeredgecolor='black', markeredgewidth=1.2, zorder=5)

# Optimal rate vertical line
ax2.axvline(x=r_star, color=MLORANGE, linestyle='--', linewidth=1.5, alpha=0.8)

# Annotate intersection
ax2.annotate(f'$r^* = {r_star * 100:.1f}\\%$',
             xy=(r_star, dB_at_star),
             xytext=(r_star + 0.008, dB_at_star + 40),
             fontsize=11, fontweight='bold', color=MLORANGE,
             arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                       edgecolor=MLORANGE, alpha=0.95))

# Region labels
ax2.text(0.003, 30, 'Raise rate\n(MB > MC)', fontsize=11, fontweight='bold',
         color=MLGREEN, ha='center',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                   edgecolor=MLGREEN, alpha=0.9))

ax2.text(0.028, 30, 'Lower rate\n(MC > MB)', fontsize=11, fontweight='bold',
         color=MLRED, ha='center',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                   edgecolor=MLRED, alpha=0.9))

# Formatting
ax2.set_xlabel('CBDC Rate $r$', fontweight='bold')
ax2.set_ylabel('Marginal Value', fontweight='bold')
ax2.set_title('(b) Marginal Analysis', fontweight='bold', pad=12)
ax2.xaxis.set_major_formatter(pct_fmt)
ax2.set_xlim(0, 0.042)
ax2.set_ylim(0, 250)
ax2.legend(loc='upper right', framealpha=0.95, fontsize=9)
ax2.grid(True, alpha=0.25, linestyle='--')
for spine in ['top', 'right']:
    ax2.spines[spine].set_visible(False)

# ================================================================
# Save
# ================================================================
plt.tight_layout()

out_dir = Path(__file__).parent
plt.savefig(out_dir / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(out_dir / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
