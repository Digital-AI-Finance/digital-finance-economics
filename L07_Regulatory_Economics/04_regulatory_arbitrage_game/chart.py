"""Regulatory Arbitrage: Game Theory"""
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

# Payoff matrix (rows: Country A strategy, cols: Country B strategy)
# Strategies: Strict, Medium, Lax
payoff_matrix = np.array([[7, 4, 2],
                          [8, 6, 3],
                          [9, 7, 4]])

strategies = ['Strict', 'Medium', 'Lax']

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left plot: Heatmap of payoff matrix
im = ax1.imshow(payoff_matrix, cmap='YlOrRd', aspect='auto')

# Add text annotations for payoffs
for i in range(3):
    for j in range(3):
        text = ax1.text(j, i, payoff_matrix[i, j], ha='center', va='center',
                       fontsize=16, fontweight='bold', color='black')

# Highlight Nash equilibrium (Lax, Lax) with red border
nash_rect = plt.Rectangle((2-0.5, 2-0.5), 1, 1, fill=False, edgecolor=MLRED, linewidth=4)
ax1.add_patch(nash_rect)

# Highlight cooperative outcome (Strict, Strict) with green border
coop_rect = plt.Rectangle((0-0.5, 0-0.5), 1, 1, fill=False, edgecolor=MLGREEN, linewidth=4)
ax1.add_patch(coop_rect)

ax1.set_xticks(range(3))
ax1.set_yticks(range(3))
ax1.set_xticklabels(strategies)
ax1.set_yticklabels(strategies)
ax1.set_xlabel('Country B Strategy')
ax1.set_ylabel('Country A Strategy')
ax1.set_title('Payoff Matrix\n(Red=Nash, Green=Cooperative)')

# Colorbar
cbar = plt.colorbar(im, ax=ax1)
cbar.set_label('Payoff', rotation=270, labelpad=20)

# Right plot: Repeated game dynamics
rounds = 50
time = np.arange(1, rounds + 1)

# Nash strategy: constant payoff at Nash equilibrium
nash_payoff = np.ones(rounds) * 4  # Payoff at (Lax, Lax)

# Tit-for-tat strategy: mostly cooperative (payoff=7), occasional punishment (payoff=2)
tit_for_tat_payoff = np.ones(rounds) * 7
# Add occasional defections/punishments
defection_rounds = [10, 25, 40]
for r in defection_rounds:
    tit_for_tat_payoff[r:r+2] = 2

# Calculate cumulative payoffs
nash_cumulative = np.cumsum(nash_payoff)
tft_cumulative = np.cumsum(tit_for_tat_payoff)

ax2.plot(time, nash_cumulative, color=MLRED, linewidth=2.5, label='Nash (Always Lax)')
ax2.plot(time, tft_cumulative, color=MLGREEN, linewidth=2.5, label='Tit-for-Tat')

ax2.set_xlabel('Round')
ax2.set_ylabel('Cumulative Payoff')
ax2.set_title('Repeated Game: Cumulative Payoffs')
ax2.legend(loc='best')
ax2.grid(True, alpha=0.3)

# Overall title
fig.suptitle('Regulatory Competition: Race to Bottom vs Cooperation',
             fontsize=16, fontweight='bold', y=1.02)

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
