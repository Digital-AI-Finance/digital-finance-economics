r"""Adoption Threshold Phase Diagram: Katz-Shapiro Fulfilled Expectations

Multi-panel override: comparative statics requires simultaneous visibility

Panel (a): 2D heatmap/contour of equilibrium adoption regions.
Panel (b): Cross-section at sigma=1.5 showing benefit vs cost curves.

Economic Model:
Katz-Shapiro fulfilled expectations: $b(n^e) = c$ where
$b(n) = \frac{\sigma n}{1 + \sigma n}$.
Based on Katz \& Shapiro (1985).
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 11,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

def benefit(n, sigma):
    """Network benefit: b(n) = sigma*n / (1 + sigma*n)"""
    return sigma * n / (1 + sigma * n)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): 2D heatmap/contour ---
sigma_range = np.linspace(0.01, 3.0, 300)
c_range = np.linspace(0.01, 0.50, 300)
S, C = np.meshgrid(sigma_range, c_range)

# For each (sigma, c), find equilibrium n* where b(n*) = c
# b(n) = sigma*n / (1 + sigma*n) = c  =>  n* = c / (sigma*(1-c))
# Adoption is viable if n* < N_max (say 1.0 normalized)
N_star = C / (S * (1 - C))
N_star = np.clip(N_star, 0, 2)

# Contour: regions where adoption is viable (n* < 1)
contour = ax1.contourf(S, C, N_star, levels=[0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0],
                       cmap='RdYlGn_r', alpha=0.8)
cbar = fig.colorbar(contour, ax=ax1, label='Critical Mass $n^*$ (normalized)')

# Overlay equilibrium boundary: n* = 1 => c = sigma/(1+sigma)
sigma_eq = np.linspace(0.01, 3.0, 200)
c_eq = sigma_eq / (1 + sigma_eq)
ax1.plot(sigma_eq, c_eq, color='black', linewidth=2.5, linestyle='-',
         label='Equilibrium boundary: $n^*=1$')

# Plot specific technologies
techs = [
    ('BTC', 2.5, 0.15, MLORANGE),
    ('ETH', 2.0, 0.20, MLBLUE),
    ('Failed\nToken', 0.5, 0.35, MLRED),
]
for name, s, c, color in techs:
    ax1.plot(s, c, 'o', color=color, markersize=12, zorder=5,
             markeredgecolor='white', markeredgewidth=2)
    ax1.annotate(name, xy=(s, c), xytext=(s + 0.15, c + 0.03),
                 fontsize=10, fontweight='bold', color=color,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                           edgecolor=color, alpha=0.9))

# Region labels
ax1.text(2.0, 0.08, 'VIABLE\nADOPTION', fontsize=12, fontweight='bold',
         color=MLGREEN, ha='center',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
ax1.text(0.5, 0.45, 'ADOPTION\nFAILURE', fontsize=12, fontweight='bold',
         color=MLRED, ha='center',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax1.set_xlabel('Network Effect Strength ($\\sigma$)', fontweight='bold')
ax1.set_ylabel('Adoption Cost ($c$)', fontweight='bold')
ax1.set_title('(a) Adoption Phase Diagram\nKatz-Shapiro (1985)', fontweight='bold', color=MLPURPLE)
ax1.legend(loc='upper left', framealpha=0.9, fontsize=9)
ax1.set_xlim(0, 3)
ax1.set_ylim(0, 0.50)

# --- Panel (b): Cross-section at sigma=1.5 ---
sigma_cross = 1.5
n_range = np.linspace(0, 1.0, 200)
b_vals = benefit(n_range, sigma_cross)

# Different cost levels
cost_levels = [
    ('Low cost ($c=0.15$)', 0.15, MLGREEN),
    ('Medium cost ($c=0.30$)', 0.30, MLORANGE),
    ('High cost ($c=0.45$)', 0.45, MLRED),
]

ax2.plot(n_range, b_vals, color=MLPURPLE, linewidth=3,
         label=f'Benefit: $b(n)$ at $\\sigma={sigma_cross}$')

for label, c_val, color in cost_levels:
    ax2.axhline(y=c_val, color=color, linestyle='--', linewidth=2,
                label=label, alpha=0.8)
    # Find equilibrium
    n_eq = c_val / (sigma_cross * (1 - c_val))
    if 0 < n_eq < 1:
        ax2.plot(n_eq, c_val, 'o', color=color, markersize=10, zorder=5)
        ax2.annotate(f'$n^*={n_eq:.2f}$',
                     xy=(n_eq, c_val), xytext=(n_eq + 0.08, c_val + 0.04),
                     fontsize=9, fontweight='bold', color=color,
                     arrowprops=dict(arrowstyle='->', color=color, lw=1.2))

# Shade viable region
ax2.fill_between(n_range, 0, b_vals, alpha=0.1, color=MLGREEN)

# Mark unstable region
ax2.annotate('Below critical mass:\nadoption collapses',
             xy=(0.05, 0.05), xytext=(0.3, 0.08),
             fontsize=9, fontweight='bold', color=MLRED,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.3),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow',
                       edgecolor=MLRED, alpha=0.9))

ax2.set_xlabel('Network Size $n$ (normalized)', fontweight='bold')
ax2.set_ylabel('Benefit $b(n)$ / Cost $c$', fontweight='bold')
ax2.set_title('(b) Cross-Section at $\\sigma=1.5$:\nBenefit vs Cost', fontweight='bold', color=MLPURPLE)
ax2.legend(loc='center right', framealpha=0.9, fontsize=9)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 0.65)

fig.suptitle('Adoption Threshold Analysis: Katz-Shapiro Fulfilled Expectations\n'
             r'$b(n) = \frac{\sigma n}{1 + \sigma n}$, equilibrium $b(n^e) = c$'
             ' -- Katz & Shapiro (1985)',
             fontweight='bold', fontsize=14, color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
