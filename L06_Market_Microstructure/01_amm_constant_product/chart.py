"""AMM Constant Product Market Maker (x*y=k)"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (10, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# --- Parameters ---
k = 1_000_000
x0, y0 = 1000, 1000
spot_price = y0 / x0  # 1.0

x_curve = np.linspace(200, 5000, 800)
y_curve = k / x_curve

# --- Trade computations (buying token X = removing X from pool = x decreases) ---
def trade_buy_x(x_pool, y_pool, dx_out):
    """Buy dx_out of token X from the pool. Trader sends Y, receives X."""
    new_x = x_pool - dx_out
    new_y = k / new_x
    cost_y = new_y - y_pool
    effective_price = cost_y / dx_out  # Y per X
    return new_x, new_y, effective_price

# Two highlighted trades
trades = [100, 500]
trade_colors = [MLORANGE, MLRED]

# Slippage for various sizes
sizes = [10, 50, 100, 200, 500]
slippages = []
for s in sizes:
    _, _, ep = trade_buy_x(x0, y0, s)
    slip = (ep - spot_price) / spot_price * 100
    slippages.append(slip)

# --- Figure ---
fig, ax_main = plt.subplots(figsize=(10, 6))

# Main curve
ax_main.plot(x_curve, y_curve, color=MLPURPLE, lw=2.5, label=r'$x \cdot y = k$  ($k = 10^6$)')
ax_main.plot(x0, y0, 'o', color=MLBLUE, ms=10, zorder=5, label=f'Start ({x0}, {y0}), price = {spot_price:.1f}')

# Annotate trades
for dx_out, col in zip(trades, trade_colors):
    nx, ny, ep = trade_buy_x(x0, y0, dx_out)
    ax_main.annotate('', xy=(nx, ny), xytext=(x0, y0),
                     arrowprops=dict(arrowstyle='->', color=col, lw=2))
    ax_main.plot(nx, ny, 's', color=col, ms=8, zorder=5)
    ax_main.annotate(f'Buy {dx_out} X\nprice {ep:.3f} Y/X\nslip {(ep-spot_price)/spot_price*100:.1f}%',
                     xy=(nx, ny), xytext=(nx - 250, ny + 150),
                     fontsize=10, color=col,
                     arrowprops=dict(arrowstyle='->', color=col, lw=1),
                     bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=col, alpha=0.9))

ax_main.set_xlabel('Token X reserve')
ax_main.set_ylabel('Token Y reserve')
ax_main.set_title('AMM Constant Product Market Maker ($x \\cdot y = k$)')
ax_main.legend(loc='upper right', fontsize=11)
ax_main.set_xlim(200, 3500)
ax_main.set_ylim(200, 3500)
ax_main.grid(True, alpha=0.3)

# --- Inset: slippage bar chart ---
ax_ins = fig.add_axes([0.58, 0.45, 0.30, 0.30])
bars = ax_ins.bar([str(s) for s in sizes], slippages, color=MLLAVENDER, edgecolor=MLPURPLE, lw=1.2)
for bar, sl in zip(bars, slippages):
    ax_ins.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f'{sl:.1f}%', ha='center', va='bottom', fontsize=9, color=MLPURPLE)
ax_ins.set_xlabel('Trade size (X)', fontsize=10)
ax_ins.set_ylabel('Slippage %', fontsize=10)
ax_ins.set_title('Price slippage', fontsize=11)
ax_ins.tick_params(labelsize=9)
ax_ins.grid(axis='y', alpha=0.3)

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
