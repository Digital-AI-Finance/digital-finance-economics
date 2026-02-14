"""Katz-Shapiro Network Adoption Equilibria

Multi-panel chart showing fulfilled-expectations equilibria under network effects.

Economic Model:
  Benefit function: $b(n) = \frac{\sigma n}{1 + \sigma n}$. Based on Katz \& Shapiro (1985).
  Equilibrium condition: $b(n^*) = c$ (benefit equals adoption cost).
  Stability: stable if $b'(n^*) < 0$ at crossing from above; unstable if from below.

# Multi-panel override: comparative statics requires simultaneous visibility

Citation: Katz & Shapiro (1985) - Network Externalities, Competition, and Compatibility
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
# b(n) = sigma*n / (1 + sigma*n), n in [0, 1]
# Equilibrium: b(n*) = c => sigma*n* / (1 + sigma*n*) = c => n* = c / (sigma*(1-c))

n = np.linspace(0, 1, 1000)

def benefit(n_val, sigma):
    return sigma * n_val / (1.0 + sigma * n_val)

def equilibria(sigma, c):
    """Find equilibria: n* = c / (sigma * (1 - c)) if in [0,1]."""
    if c <= 0:
        return [0.0]
    if c >= 1:
        return []
    n_star = c / (sigma * (1.0 - c))
    results = [0.0]  # n=0 is always an equilibrium (b(0)=0 < c for c>0 means no adoption)
    if 0 < n_star <= 1:
        results.append(n_star)
    return results

# --- Panel (a): Benefit vs cost lines for sigma=2.0, c=[0.15, 0.25, 0.35] ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

sigma_main = 2.0
cost_vals = [0.15, 0.25, 0.35]
cost_colors = [MLGREEN, MLBLUE, MLRED]
cost_labels = ['c = 0.15 (low cost)', 'c = 0.25 (medium cost)', 'c = 0.35 (high cost)']

# Benefit curve
b_vals = benefit(n, sigma_main)
ax1.plot(n, b_vals, color=MLPURPLE, linewidth=3, label=r'$b(n) = \frac{2n}{1+2n}$', zorder=3)

for c_val, c_col, c_lab in zip(cost_vals, cost_colors, cost_labels):
    ax1.axhline(y=c_val, color=c_col, linestyle='--', linewidth=2, alpha=0.8, label=c_lab)

    # Find equilibrium n* = c / (sigma*(1-c))
    n_star = c_val / (sigma_main * (1.0 - c_val))
    if 0 < n_star <= 1:
        b_star = benefit(n_star, sigma_main)
        # Stable equilibrium (benefit curve crosses cost from above)
        ax1.plot(n_star, b_star, 'o', color=c_col, markersize=10,
                 markeredgecolor='black', markeredgewidth=1.5, zorder=5)
        # Label
        offset_y = 0.04 if c_val != 0.25 else -0.06
        ax1.annotate(f'n* = {n_star:.2f}',
                     xy=(n_star, b_star),
                     xytext=(n_star + 0.08, b_star + offset_y),
                     fontsize=10, fontweight='bold', color=c_col,
                     arrowprops=dict(arrowstyle='->', color=c_col, lw=1.5),
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                               edgecolor=c_col, alpha=0.9))

    # n=0 is the trivial equilibrium (no adoption)
    ax1.plot(0, 0, 's', color=c_col, markersize=7, markeredgecolor='black',
             markeredgewidth=1, zorder=5, alpha=0.6)

# Mark unstable region for c=0.25 worked example
n_star_025 = 0.25 / (2.0 * 0.75)  # = 0.1667
ax1.annotate('Unstable\n(n* = 0.17)',
             xy=(n_star_025, 0.25),
             xytext=(0.05, 0.38),
             fontsize=9, color=MLBLUE, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                       edgecolor=MLBLUE, alpha=0.9))

# Stability annotation
ax1.text(0.55, 0.08, 'Stability: where b(n)\ncrosses c from above\n= stable equilibrium',
         transform=ax1.transAxes, fontsize=9,
         bbox=dict(boxstyle='round,pad=0.4', facecolor=MLLAVENDER, alpha=0.3))

# For sigma=2, c=0.25: stable eq at n*=0.83
n_star_stable = 1.0 - n_star_025  # Approximate: need actual
# Actually n* = c/(sigma*(1-c)) = 0.25/(2*0.75) = 0.1667 -- that's the only interior equilibrium
# Wait: b(n) is monotonically increasing, so it crosses c exactly once.
# At n*=0.1667, b is increasing through c, so for n > n*: b(n) > c (adopt), for n < n*: b(n) < c (don't adopt)
# This means n*=0.1667 is UNSTABLE (tipping point): below it collapses to 0, above it goes to full adoption
# The stable equilibria are n=0 and n=1 (or close to 1)

# Mark the full adoption stable equilibrium
ax1.annotate('Stable\n(full adoption)',
             xy=(0.95, benefit(0.95, sigma_main)),
             xytext=(0.72, 0.55),
             fontsize=9, color=MLPURPLE, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLPURPLE, alpha=0.9))

ax1.set_xlabel('Adoption Fraction (n)')
ax1.set_ylabel('Benefit b(n) / Cost c')
ax1.set_title('(a) Katz-Shapiro Benefit vs Cost')
ax1.legend(loc='lower right', fontsize=9, framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 0.75)

# --- Panel (b): Phase diagram sigma vs c ---
sigma_range = np.linspace(0.1, 5.0, 200)
c_range = np.linspace(0.01, 0.99, 200)
SIGMA, C = np.meshgrid(sigma_range, c_range)

# Interior equilibrium exists when n* = c/(sigma*(1-c)) is in (0,1)
# n* < 1 <=> c < sigma*(1-c) <=> c < sigma/(1+sigma)
# So the critical boundary is c = sigma/(1+sigma)
# Above this line: no interior equilibrium (only n=0)
# Below this line: interior equilibrium exists (tipping point)

c_boundary = sigma_range / (1.0 + sigma_range)

# Region coloring
has_interior = C < SIGMA / (1.0 + SIGMA)

ax2.contourf(SIGMA, C, has_interior.astype(float), levels=[-0.5, 0.5, 1.5],
             colors=[MLRED + '40', MLGREEN + '40'], alpha=0.6)

# Boundary line
ax2.plot(sigma_range, c_boundary, color=MLPURPLE, linewidth=3,
         label=r'$c^* = \frac{\sigma}{1+\sigma}$ (critical boundary)')

# Mark specific points from panel (a)
for c_val, c_col, marker_label in zip(cost_vals, cost_colors, ['Low c', 'Med c', 'High c']):
    ax2.plot(sigma_main, c_val, 'o', color=c_col, markersize=12,
             markeredgecolor='black', markeredgewidth=2, zorder=5)
    ax2.annotate(marker_label,
                 xy=(sigma_main, c_val),
                 xytext=(sigma_main + 0.3, c_val + 0.03),
                 fontsize=10, fontweight='bold', color=c_col)

# Region labels
ax2.text(3.5, 0.3, 'Adoption\nPossible', fontsize=12, fontweight='bold',
         color='darkgreen', ha='center',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.8))
ax2.text(1.0, 0.8, 'No Adoption\n(cost too high)', fontsize=12, fontweight='bold',
         color='darkred', ha='center',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.8))

# Worked example annotation
ax2.annotate(r'Worked example: $\sigma$=2, c=0.25' + '\n' + r'$n^*_{unstable}$=0.17, above tips to full adoption',
             xy=(2.0, 0.25), xytext=(3.0, 0.55),
             fontsize=9, fontweight='bold', color=MLBLUE,
             arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                       edgecolor=MLBLUE, alpha=0.9))

ax2.set_xlabel(r'Network Effect Strength ($\sigma$)')
ax2.set_ylabel('Adoption Cost (c)')
ax2.set_title(r'(b) Phase Diagram: $\sigma$ vs c')
ax2.legend(loc='upper left', fontsize=9, framealpha=0.95)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(0.1, 5.0)
ax2.set_ylim(0, 1.0)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
