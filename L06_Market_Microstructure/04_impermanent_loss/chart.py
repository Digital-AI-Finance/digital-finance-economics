"""Impermanent Loss for Liquidity Providers

Based on: Pintail (2019) - Impermanent Loss in Uniswap
"""
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

# Price ratio from 0.1 to 10
r = np.logspace(np.log10(0.1), np.log10(10), 500)

# Initial deposit: $10k with 50/50 split ($5k each side)
hold_value = 5000 * (1 + r)  # Hold strategy value
lp_value = 10000 * np.sqrt(r)  # LP position value
IL_pct = (lp_value / hold_value - 1) * 100  # Impermanent loss percentage

# Create two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9))

# Top subplot: IL% vs price ratio
ax1.plot(r, IL_pct, color=MLRED, linewidth=2)
ax1.set_xscale('log')
ax1.axhline(0, color='black', linestyle='--', linewidth=1)

# Mark specific points
r_2x = 2.0
r_5x = 5.0
IL_2x = (10000 * np.sqrt(r_2x) / (5000 * (1 + r_2x)) - 1) * 100
IL_5x = (10000 * np.sqrt(r_5x) / (5000 * (1 + r_5x)) - 1) * 100

ax1.plot(r_2x, IL_2x, 'o', color=MLORANGE, markersize=8, label=f'2x: {IL_2x:.1f}%')
ax1.plot(r_5x, IL_5x, 'o', color=MLBLUE, markersize=8, label=f'5x: {IL_5x:.1f}%')

# B5: Add annotation highlighting the 5x loss point
ax1.annotate(f'5x price change:\n{IL_5x:.1f}% loss',
            xy=(r_5x, IL_5x), xytext=(r_5x * 1.5, IL_5x + 5),
            fontsize=10, fontweight='bold', color=MLBLUE,
            arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLBLUE, alpha=0.8))

ax1.set_xlabel('Price Ratio (Final/Initial, ratio)')
ax1.set_ylabel('Impermanent Loss (%)')
ax1.set_title('Impermanent Loss: LP Position vs Hold Strategy')
ax1.legend()
ax1.grid(alpha=0.3)

# Add impermanent loss formula annotation
ax1.text(0.02, 0.02, r'Impermanent Loss:' + '\n' +
         r'$IL = \frac{2\sqrt{p}}{1+p} - 1$' + '\n' +
         r'where $p = $ price ratio' + '\n' +
         r'$V_{LP} = V_0 \sqrt{p}$, $V_{hold} = V_0(1+p)/2$',
         transform=ax1.transAxes, fontsize=10,
         verticalalignment='bottom',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Bottom subplot: Dollar values
ax2.plot(r, lp_value, color=MLPURPLE, linewidth=2, label='LP Position')
ax2.plot(r, hold_value, color=MLBLUE, linewidth=2, label='Hold Strategy')

# Shade the loss region
loss_mask = lp_value < hold_value
ax2.fill_between(r, lp_value, hold_value, where=loss_mask,
                  alpha=0.3, color=MLRED, label='Loss Region')

ax2.set_xscale('log')
ax2.set_xlabel('Price Ratio (Final/Initial)')
ax2.set_ylabel('Portfolio Value ($)')
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
