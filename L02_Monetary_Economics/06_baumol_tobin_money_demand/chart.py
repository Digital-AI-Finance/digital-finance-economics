r"""Baumol-Tobin Optimal Cash Holdings
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
    $M^* = \sqrt{\frac{bY}{2i}}$, $TC(n) = bn + \frac{iY}{2n}$.
    Three regimes: traditional ($b=2$), digital ($b=0.50$), crypto ($b=0.10$).
    Based on Baumol (1952), Tobin (1956).

    Optimal withdrawal frequency: $n^* = \sqrt{\frac{iY}{2b}}$
    Total cost at optimum: $TC^* = \sqrt{2bYi}$
    Interest-rate elasticity of money demand: $\frac{\partial \ln M^*}{\partial \ln i} = -0.5$
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

# --- Parameters ---
Y = 36_000  # Annual income
b_trad = 2.00   # Traditional transaction cost
b_dig = 0.50    # Digital banking cost
b_crypto = 0.10  # Crypto transaction cost

i_range = np.linspace(0.01, 0.15, 200)

# Baumol-Tobin: M* = sqrt(bY / (2i))
def optimal_cash(b, Y, i):
    return np.sqrt(b * Y / (2.0 * i))

# TC(n) = b*n + i*Y/(2*n)
def total_cost(n, b, i, Y):
    return b * n + i * Y / (2.0 * n)

# Elasticity: d ln M* / d ln i = -0.5 (constant)
# But we show numerical gradient for verification
def numerical_elasticity(b, Y, i_arr):
    M = optimal_cash(b, Y, i_arr)
    dM = np.gradient(M, i_arr)
    return (dM / M) * (i_arr)

# --- Figure: 1x3 layout ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

# Panel (a): M* vs interest rate
for b_val, label, color, ls in [
    (b_trad, f'Traditional (b=${b_trad:.2f})', MLBLUE, '-'),
    (b_dig, f'Digital (b=${b_dig:.2f})', MLORANGE, '--'),
    (b_crypto, f'Crypto (b=${b_crypto:.2f})', MLGREEN, '-.')
]:
    M_star = optimal_cash(b_val, Y, i_range)
    ax1.plot(i_range * 100, M_star, color=color, linewidth=2.2, linestyle=ls, label=label)

# Verify worked example: i=0.05, b=2 -> M*=sqrt(2*36000/(2*0.05))=sqrt(720000)=848.53
M_check = optimal_cash(b_trad, Y, 0.05)
ax1.plot(5.0, M_check, 'ko', markersize=7, zorder=5)
ax1.annotate(f'$M^*=${M_check:.0f}',
             xy=(5.0, M_check), xytext=(7.5, M_check + 300),
             fontsize=9, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='black', lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.9))

ax1.set_xlabel('Interest Rate i (%)', fontweight='bold')
ax1.set_ylabel('Optimal Cash Holdings M* ($)', fontweight='bold')
ax1.set_title('(a) Money Demand vs Interest Rate', fontweight='bold', color=MLPURPLE)
ax1.legend(loc='upper right', framealpha=0.9, fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1, 15)

# Panel (b): Total cost vs number of withdrawals (i=0.05)
i_fixed = 0.05
n_range = np.linspace(1, 50, 200)

for b_val, label, color, ls in [
    (b_trad, f'Traditional (b=${b_trad:.2f})', MLBLUE, '-'),
    (b_dig, f'Digital (b=${b_dig:.2f})', MLORANGE, '--'),
    (b_crypto, f'Crypto (b=${b_crypto:.2f})', MLGREEN, '-.')
]:
    TC = total_cost(n_range, b_val, i_fixed, Y)
    ax2.plot(n_range, TC, color=color, linewidth=2.2, linestyle=ls, label=label)

    # Mark optimum: n* = sqrt(iY/(2b))
    n_star = np.sqrt(i_fixed * Y / (2.0 * b_val))
    TC_star = total_cost(n_star, b_val, i_fixed, Y)
    ax2.plot(n_star, TC_star, 'o', color=color, markersize=7, zorder=5)

# Also show components for traditional case
TC_brokerage = b_trad * n_range
TC_interest = i_fixed * Y / (2.0 * n_range)
ax2.plot(n_range, TC_brokerage, color=MLBLUE, linewidth=1.0, alpha=0.4, linestyle=':')
ax2.plot(n_range, TC_interest, color=MLRED, linewidth=1.0, alpha=0.4, linestyle=':')
ax2.text(42, b_trad * 42 + 5, 'bn', fontsize=8, color=MLBLUE, alpha=0.6)
ax2.text(42, i_fixed * Y / (2.0 * 42) + 5, 'iY/2n', fontsize=8, color=MLRED, alpha=0.6)

ax2.set_xlabel('Number of Withdrawals n', fontweight='bold')
ax2.set_ylabel('Total Cost TC ($)', fontweight='bold')
ax2.set_title('(b) Total Cost at i=5%', fontweight='bold', color=MLPURPLE)
ax2.legend(loc='upper right', framealpha=0.9, fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1, 50)
ax2.set_ylim(0, 200)

# Panel (c): Elasticity of money demand wrt interest rate
for b_val, label, color, ls in [
    (b_trad, 'Traditional', MLBLUE, '-'),
    (b_dig, 'Digital', MLORANGE, '--'),
    (b_crypto, 'Crypto', MLGREEN, '-.')
]:
    elast = numerical_elasticity(b_val, Y, i_range)
    ax3.plot(i_range * 100, elast, color=color, linewidth=2.2, linestyle=ls, label=label)

# Theoretical line at -0.5
ax3.axhline(y=-0.5, color=MLRED, linestyle=':', linewidth=1.5, alpha=0.7, label='Theory: -0.5')
ax3.annotate('All regimes converge\nto elasticity = -0.5',
             xy=(10, -0.5), xytext=(10, -0.35),
             fontsize=9, fontweight='bold', ha='center',
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLRED, alpha=0.9))

ax3.set_xlabel('Interest Rate i (%)', fontweight='bold')
ax3.set_ylabel('Elasticity dln(M*)/dln(i)', fontweight='bold')
ax3.set_title('(c) Interest-Rate Elasticity', fontweight='bold', color=MLPURPLE)
ax3.legend(loc='lower right', framealpha=0.9, fontsize=9)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(1, 15)
ax3.set_ylim(-0.7, -0.2)

fig.suptitle('Baumol-Tobin Money Demand: Traditional vs Digital vs Crypto',
             fontsize=14, fontweight='bold', color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Baumol-Tobin chart saved to chart.pdf and chart.png")
