"""AMM Constant Product Variations — Assignment A6
2x2 subplot showing baseline, deep pool, imbalanced pool, and fee comparison
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 14,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# --- Trade computation helper ---
def trade_buy_x(k, x_pool, y_pool, dx_out, fee=0.0):
    """Buy dx_out of token X from the pool.
    fee: fraction of output taken as fee (e.g., 0.003 for 0.3%)
    """
    new_x = x_pool - dx_out
    new_y = k / new_x
    cost_y = new_y - y_pool
    # Apply fee to the amount received (reduce dx_out)
    dx_out_effective = dx_out * (1 - fee)
    effective_price = cost_y / dx_out_effective if dx_out_effective > 0 else cost_y / dx_out
    return new_x, new_y, effective_price

# --- Create 2x2 subplot grid ---
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
ax1, ax2, ax3, ax4 = axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]

# ============================================
# PANEL 1: BASELINE (k=1M, x0=y0=1000)
# ============================================
k1 = 1_000_000
x0_1, y0_1 = 1000, 1000
spot_price_1 = y0_1 / x0_1

x_curve_1 = np.linspace(200, 3500, 800)
y_curve_1 = k1 / x_curve_1

ax1.plot(x_curve_1, y_curve_1, color=MLPURPLE, lw=2.5, label=r'$x \cdot y = 10^6$')
ax1.plot(x0_1, y0_1, 'o', color=MLBLUE, ms=10, zorder=5, label=f'Start ({x0_1}, {y0_1}), P={spot_price_1:.1f}')

# Trade arrows for 100 and 500
trades_1 = [100, 500]
trade_colors = [MLORANGE, MLRED]

for dx_out, col in zip(trades_1, trade_colors):
    nx, ny, ep = trade_buy_x(k1, x0_1, y0_1, dx_out)
    ax1.annotate('', xy=(nx, ny), xytext=(x0_1, y0_1),
                 arrowprops=dict(arrowstyle='->', color=col, lw=2))
    ax1.plot(nx, ny, 's', color=col, ms=8, zorder=5)
    slip = (ep - spot_price_1) / spot_price_1 * 100
    ax1.text(nx - 200, ny + 100, f'Buy {dx_out} X\nslip {slip:.1f}%',
             fontsize=9, color=col, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=col, alpha=0.9))

ax1.set_xlabel('Token X reserve')
ax1.set_ylabel('Token Y reserve')
ax1.set_title('BASELINE: k = 1M, balanced pool')
ax1.legend(loc='upper right', fontsize=9)
ax1.set_xlim(200, 3500)
ax1.set_ylim(200, 3500)
ax1.grid(True, alpha=0.3)

# ============================================
# PANEL 2: VARIATION 1 (k=10M, deeper pool)
# ============================================
k2 = 10_000_000
x0_2, y0_2 = int(np.sqrt(k2)), int(np.sqrt(k2))  # ~3162 each
spot_price_2 = y0_2 / x0_2

x_curve_2 = np.linspace(500, 10000, 800)
y_curve_2 = k2 / x_curve_2

ax2.plot(x_curve_2, y_curve_2, color=MLGREEN, lw=2.5, label=r'$x \cdot y = 10^7$')
ax2.plot(x0_2, y0_2, 'o', color=MLBLUE, ms=10, zorder=5, label=f'Start ({x0_2}, {y0_2}), P={spot_price_2:.2f}')

# Same trades (100, 500) on deeper pool
for dx_out, col in zip(trades_1, trade_colors):
    nx, ny, ep = trade_buy_x(k2, x0_2, y0_2, dx_out)
    ax2.annotate('', xy=(nx, ny), xytext=(x0_2, y0_2),
                 arrowprops=dict(arrowstyle='->', color=col, lw=2))
    ax2.plot(nx, ny, 's', color=col, ms=8, zorder=5)
    slip = (ep - spot_price_2) / spot_price_2 * 100
    ax2.text(nx - 300, ny + 200, f'Buy {dx_out} X\nslip {slip:.1f}%',
             fontsize=9, color=col, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=col, alpha=0.9))

ax2.set_xlabel('Token X reserve')
ax2.set_ylabel('Token Y reserve')
ax2.set_title('VARIATION 1: k = 10M (10x deeper) — reduced slippage')
ax2.legend(loc='upper right', fontsize=9)
ax2.set_xlim(500, 10000)
ax2.set_ylim(500, 10000)
ax2.grid(True, alpha=0.3)

# ============================================
# PANEL 3: VARIATION 2 (imbalanced pool)
# ============================================
k3 = 1_000_000
x0_3, y0_3 = 500, 2000  # Initial price = 4.0
spot_price_3 = y0_3 / x0_3

x_curve_3 = np.linspace(100, 3000, 800)
y_curve_3 = k3 / x_curve_3

ax3.plot(x_curve_3, y_curve_3, color=MLPURPLE, lw=2.5, label=r'$x \cdot y = 10^6$')
ax3.plot(x0_3, y0_3, 'o', color=MLRED, ms=10, zorder=5, label=f'Start ({x0_3}, {y0_3}), P={spot_price_3:.1f}')

# Show asymmetric shape with one trade on each side
# Buy 100 X (expensive direction)
nx_x, ny_x, ep_x = trade_buy_x(k3, x0_3, y0_3, 100)
slip_x = (ep_x - spot_price_3) / spot_price_3 * 100
ax3.annotate('', xy=(nx_x, ny_x), xytext=(x0_3, y0_3),
             arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=2))
ax3.plot(nx_x, ny_x, 's', color=MLORANGE, ms=8, zorder=5)
ax3.text(nx_x - 150, ny_x + 200, f'Buy 100 X\nslip {slip_x:.1f}%\n(scarce asset)',
         fontsize=9, color=MLORANGE, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=MLORANGE, alpha=0.9))

# Buy 400 Y (cheap direction) — simulate by selling X to get Y
# Reverse trade: add X, remove Y
dy_out = 400
new_y_rev = y0_3 - dy_out
new_x_rev = k3 / new_y_rev
cost_x = new_x_rev - x0_3
ep_y = cost_x / dy_out
slip_y = (ep_y - (1/spot_price_3)) / (1/spot_price_3) * 100
ax3.annotate('', xy=(new_x_rev, new_y_rev), xytext=(x0_3, y0_3),
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=2))
ax3.plot(new_x_rev, new_y_rev, '^', color=MLGREEN, ms=8, zorder=5)
ax3.text(new_x_rev + 50, new_y_rev - 200, f'Buy 400 Y\nslip {slip_y:.1f}%\n(abundant asset)',
         fontsize=9, color=MLGREEN, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=MLGREEN, alpha=0.9))

ax3.set_xlabel('Token X reserve')
ax3.set_ylabel('Token Y reserve')
ax3.set_title('VARIATION 2: Imbalanced pool (x₀=500, y₀=2000, P=4.0)')
ax3.legend(loc='upper right', fontsize=9)
ax3.set_xlim(100, 2500)
ax3.set_ylim(200, 3500)
ax3.grid(True, alpha=0.3)

# ============================================
# PANEL 4: VARIATION 3 (fee comparison)
# ============================================
k4 = 1_000_000
x0_4, y0_4 = 1000, 1000
spot_price_4 = y0_4 / x0_4

trade_sizes = [10, 50, 100, 200, 500]
slippages_no_fee = []
slippages_with_fee = []

for s in trade_sizes:
    # No fee
    _, _, ep_no_fee = trade_buy_x(k4, x0_4, y0_4, s, fee=0.0)
    slip_no_fee = (ep_no_fee - spot_price_4) / spot_price_4 * 100
    slippages_no_fee.append(slip_no_fee)

    # With 0.3% fee
    _, _, ep_with_fee = trade_buy_x(k4, x0_4, y0_4, s, fee=0.003)
    slip_with_fee = (ep_with_fee - spot_price_4) / spot_price_4 * 100
    slippages_with_fee.append(slip_with_fee)

x_pos = np.arange(len(trade_sizes))
width = 0.35

bars1 = ax4.bar(x_pos - width/2, slippages_no_fee, width, label='No fee',
                color=MLLAVENDER, edgecolor=MLPURPLE, lw=1.2)
bars2 = ax4.bar(x_pos + width/2, slippages_with_fee, width, label='With 0.3% fee',
                color=MLORANGE, edgecolor=MLRED, lw=1.2)

# Annotate bars
for i, (no_fee, with_fee) in enumerate(zip(slippages_no_fee, slippages_with_fee)):
    ax4.text(x_pos[i] - width/2, no_fee + 1, f'{no_fee:.1f}%',
             ha='center', va='bottom', fontsize=9, color=MLPURPLE)
    ax4.text(x_pos[i] + width/2, with_fee + 1, f'{with_fee:.1f}%',
             ha='center', va='bottom', fontsize=9, color=MLRED)

ax4.set_xlabel('Trade size (tokens)')
ax4.set_ylabel('Slippage (%)')
ax4.set_title('VARIATION 3: Impact of 0.3% swap fee on slippage')
ax4.set_xticks(x_pos)
ax4.set_xticklabels([str(s) for s in trade_sizes])
ax4.legend(loc='upper left', fontsize=10)
ax4.grid(axis='y', alpha=0.3)

# Add annotation box
ax4.text(0.98, 0.55, 'For large trades:\nSlippage >> Fees\n(100% vs 0.3%)',
         transform=ax4.transAxes, fontsize=10, ha='right',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.7))

# ============================================
# Save figure
# ============================================
plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart_varied.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart_varied.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart_varied.pdf and chart_varied.png")
