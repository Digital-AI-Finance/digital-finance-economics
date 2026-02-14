"""AMM Invariant Comparison: Constant-Sum, Constant-Product, StableSwap
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  Constant-sum: x + y = 200 (zero slippage, finite reserves)
  Constant-product: x * y = 10000 (infinite liquidity, high slippage)
  StableSwap (Curve): A * (x + y) + D = A * D + D^3 / (4xy)
    with A=100, D=200 (amplification factor controls curvature)
  Based on Egorov (2019), Curve Finance StableSwap whitepaper.

  Panel (a): Invariant curves. Panel (b): Effective price dy/dx.
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq
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
# Initial: x = y = 100 for all three
D = 200.0
k = 10000.0  # 100 * 100
A = 100  # Curve amplification factor

x_range = np.linspace(50, 150, 500)

# --- Constant-sum ---
y_sum = D - x_range  # x + y = 200

# --- Constant-product ---
y_prod = k / x_range  # x * y = 10000

# --- StableSwap (Curve) ---
# Invariant: A*n^n * sum(x_i) + D = A*n^n*D + D^(n+1)/(n^n * prod(x_i))
# For n=2: 4A(x+y) + D = 4A*D + D^3/(4xy)
# Solve for y given x using Newton/brentq
def stableswap_y(x_val, A_val, D_val):
    """Solve StableSwap invariant for y given x."""
    # 4A(x+y) + D = 4AD + D^3/(4xy)
    # Rearrange: 4A*y + 4A*x + D - 4A*D - D^3/(4*x*y) = 0
    # Multiply by 4xy: 16A*x*y^2 + (16A*x^2 + 4D*x - 16A*D*x)*y - D^3 = 0
    # Quadratic in y: a*y^2 + b*y + c = 0
    a_coeff = 16 * A_val * x_val
    b_coeff = 16 * A_val * x_val**2 + 4 * D_val * x_val - 16 * A_val * D_val * x_val
    c_coeff = -D_val**3

    discriminant = b_coeff**2 - 4 * a_coeff * c_coeff
    if discriminant < 0:
        return np.nan
    y_val = (-b_coeff + np.sqrt(discriminant)) / (2 * a_coeff)
    return y_val

y_stable = np.array([stableswap_y(xi, A, D) for xi in x_range])

# --- Effective price (marginal): dy/dx ---
# Constant-sum: dy/dx = -1 (constant)
price_sum = np.ones_like(x_range) * 1.0  # |dy/dx| = 1

# Constant-product: dy/dx = -k/x^2 => |dy/dx| = k/x^2
price_prod = k / x_range**2

# StableSwap: numerical derivative
dx = x_range[1] - x_range[0]
price_stable = np.abs(np.gradient(y_stable, dx))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Invariant curves ---
ax1.plot(x_range, y_sum, color=MLBLUE, linewidth=2.5, label='Constant-Sum: x + y = 200',
         linestyle='--')
ax1.plot(x_range, y_prod, color=MLRED, linewidth=2.5, label='Constant-Product: xy = 10,000')
ax1.plot(x_range, y_stable, color=MLGREEN, linewidth=2.5,
         label=f'StableSwap: A={A}, D={D:.0f}')

# Mark initial point
ax1.plot(100, 100, 'o', color=MLPURPLE, markersize=12, zorder=5, markeredgecolor='black',
         markeredgewidth=2, label='Initial (100, 100)')

ax1.set_xlabel('Token X Reserve')
ax1.set_ylabel('Token Y Reserve')
ax1.set_title('(a) AMM Invariant Curves', fontweight='bold')
ax1.legend(loc='upper right', fontsize=10, framealpha=0.95)
ax1.set_xlim(50, 150)
ax1.set_ylim(50, 150)
ax1.grid(alpha=0.3, linestyle='--')
ax1.set_aspect('equal')

# Annotations for each curve behavior
ax1.annotate('Constant-sum:\nzero slippage, but\nreserves can deplete',
             xy=(55, 145), xytext=(60, 135), fontsize=9, color=MLBLUE,
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=MLBLUE, alpha=0.8))

ax1.annotate('Constant-product:\ninfinite liquidity,\nhigh slippage',
             xy=(140, 72), xytext=(110, 60), fontsize=9, color=MLRED,
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=MLRED, alpha=0.8))

# --- Panel (b): Effective price dy/dx ---
ax2.plot(x_range, price_sum, color=MLBLUE, linewidth=2.5, linestyle='--',
         label='Constant-Sum (price = 1)')
ax2.plot(x_range, price_prod, color=MLRED, linewidth=2.5,
         label='Constant-Product')
# Filter StableSwap price to valid range
valid = (price_stable > 0.5) & (price_stable < 3.0)
ax2.plot(x_range[valid], price_stable[valid], color=MLGREEN, linewidth=2.5,
         label=f'StableSwap (A={A})')

ax2.axhline(y=1.0, color='black', linestyle=':', linewidth=1, alpha=0.5)

ax2.set_xlabel('Token X Reserve')
ax2.set_ylabel('Effective Price |dy/dx|')
ax2.set_title('(b) Effective Price vs Reserve Level', fontweight='bold')
ax2.legend(loc='upper right', fontsize=10, framealpha=0.95)
ax2.set_xlim(50, 150)
ax2.set_ylim(0.3, 2.5)
ax2.grid(alpha=0.3, linestyle='--')

# Annotation: StableSwap benefit zone
ax2.axvspan(80, 120, alpha=0.1, color=MLGREEN)
ax2.text(100, 2.3, 'StableSwap\nsweet spot:\nnear-zero slippage', fontsize=9,
         ha='center', color=MLGREEN, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=MLGREEN, alpha=0.8))

# Formula annotation
ax2.text(0.02, 0.02, 'StableSwap interpolates between\n'
         'constant-sum (low slippage near peg)\n'
         'and constant-product (safety far from peg).\n'
         f'Amplification A={A} controls curvature.',
         transform=ax2.transAxes, fontsize=9, va='bottom',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

fig.suptitle('AMM Invariant Comparison: Design Trade-offs\n'
             'Egorov (2019): StableSwap achieves 100x lower slippage for pegged assets',
             fontsize=15, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
