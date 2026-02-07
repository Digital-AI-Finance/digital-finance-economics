"""Token Velocity and Value Capture - Equation of Exchange Application

Demonstrates how staking mechanisms reduce token velocity and increase market capitalization.
Based on the Equation of Exchange (MV=PQ) applied to tokenomics, where velocity sinks
through staking create value capture for token holders.

Economic Model:
  $V = \\frac{PQ}{M}$ (Token Velocity)
  $M = \\frac{PQ}{V}$ (Market Cap from Velocity)

Where:
  - M: Market capitalization (monetary stock)
  - V: Token velocity (turnover rate)
  - P: Average price level of transactions
  - Q: Real transaction volume

Citation: Fisher (1911) - The Purchasing Power of Money; adapted to token economics
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

# Equation of Exchange: M*V = P*Q
# Market Cap = M = P*Q / V

PQ = 1e9  # Transaction volume in dollars
V = np.linspace(1, 50, 100)  # Velocity

# Scenario 1: No staking
MarketCap_no_staking = PQ / V

# Scenario 2: With staking (effective velocity reduced by 50%)
V_effective = V * 0.5
MarketCap_with_staking = PQ / V_effective

# Plot
fig, ax = plt.subplots()

ax.plot(V, MarketCap_no_staking / 1e6, linewidth=2.5, color=MLBLUE, label='No Staking')
ax.plot(V, MarketCap_with_staking / 1e6, linewidth=2.5, color=MLORANGE, label='With Staking (50% locked)')

# Add arrows showing velocity sink effect at V=8 where gap is dramatic
arrow_v = 8
arrow_y1 = (PQ / arrow_v) / 1e6
arrow_y2 = (PQ / (arrow_v * 0.5)) / 1e6

ax.annotate('', xy=(arrow_v, arrow_y2), xytext=(arrow_v, arrow_y1),
            arrowprops=dict(arrowstyle='->', lw=2.5, color=MLGREEN))
ax.text(arrow_v + 1.5, (arrow_y1 + arrow_y2) / 2, 'Velocity Sink\nEffect',
        fontsize=11, color=MLGREEN, va='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=MLGREEN, alpha=0.8))

# Highlight specific points with value labels
highlight_v = [5, 10, 20]
for v in highlight_v:
    mc = (PQ / v) / 1e6
    ax.plot(v, mc, 'o', color=MLBLUE, markersize=7, zorder=5)
    ax.annotate(f'${mc:.0f}M',
                xy=(v, mc), xytext=(5, 8), textcoords='offset points',
                fontsize=9, fontweight='bold', color=MLBLUE,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                         edgecolor=MLBLUE, alpha=0.7))

ax.set_xlabel('Token Velocity $V$ (times each token changes hands per year)')
ax.set_ylabel('Market Cap ($ millions)')
ax.set_title('Token Value vs Velocity: Effect of Staking')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(1, 50)
ax.set_ylim(0, 1000)

# Expanded equation text box
textstr = ('$M \\cdot V = P \\cdot Q$\n'
           'where $P \\cdot Q$ = \\$1B (total economic activity)\n'
           'Market Cap $= P \\cdot Q \\,/\\, V$\n'
           'Staking locks 50% of tokens,\n'
           'halving effective $V$ $\\rightarrow$ doubling Market Cap')
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor=MLLAVENDER, alpha=0.3))

# Staking explanation annotation
ax.text(0.55, 0.42,
        'Staking locks tokens out of circulation.\n'
        'Fewer tokens available to transact =\n'
        'lower effective velocity = higher value per token.',
        transform=ax.transAxes, fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                 edgecolor=MLORANGE, linewidth=1.5, alpha=0.9))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
