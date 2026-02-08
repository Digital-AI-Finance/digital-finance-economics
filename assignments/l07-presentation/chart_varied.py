r"""Regulatory Arbitrage: Variations on Payoff Matrix and Repeated Game

Demonstrates how penalties, subsidies, and repeated interaction affect Nash equilibria
in regulatory competition games.

Economic Model: Regulatory Arbitrage Payoff Function
Economic Formula: $\Pi = B(a) - C(r) - P(d) \cdot F$
where:
  - Π = Regulatory arbitrage payoff
  - B(a) = Regulatory benefit from action a
  - C(r) = Compliance cost for regulatory stringency r
  - P(d) = Probability of detection d
  - F = Regulatory fine/penalty

Citation: Kanbur & Keen (1993) - Jeux Sans Frontières: Tax Competition and Tax Coordination
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 11,
    'figure.figsize': (16, 12), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

strategies = ['Strict', 'Medium', 'Lax']

# Baseline payoff matrix
baseline_matrix = np.array([[7, 4, 2],
                           [8, 6, 3],
                           [9, 7, 4]])

# Variation 1: Lax penalty (-5)
# Subtract 5 from Lax row AND Lax column
penalty_matrix = baseline_matrix.copy()
penalty_matrix[2, :] = [4, 2, -1]  # Lax row: [9-5, 7-5, 4-5]
penalty_matrix[:, 2] = [-3, -2, -1]  # Lax column: [2-5, 3-5, 4-5]

# Variation 2: Strict subsidy (+3)
# Add 3 to Strict row
subsidy_matrix = baseline_matrix.copy()
subsidy_matrix[0, :] = [10, 7, 5]  # Strict row: [7+3, 4+3, 2+3]

# Create figure with 2x2 subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Panel 1: Baseline
im1 = ax1.imshow(baseline_matrix, cmap='YlOrRd', aspect='auto', vmin=-3, vmax=10)
for i in range(3):
    for j in range(3):
        ax1.text(j, i, int(baseline_matrix[i, j]), ha='center', va='center',
                fontsize=14, fontweight='bold', color='black')

# Highlight Nash (Lax, Lax) in red
nash_rect1 = plt.Rectangle((2-0.5, 2-0.5), 1, 1, fill=False, edgecolor=MLRED, linewidth=4)
ax1.add_patch(nash_rect1)

ax1.set_xticks(range(3))
ax1.set_yticks(range(3))
ax1.set_xticklabels(strategies)
ax1.set_yticklabels(strategies)
ax1.set_xlabel('Country B Strategy (category)')
ax1.set_ylabel('Country A Strategy (category)')
ax1.set_title('Baseline: Nash = (Lax, Lax) = 4')

ax1.annotate('Nash (4)', xy=(2, 2), xytext=(1.5, 0.8),
            fontsize=10, fontweight='bold', color=MLRED,
            arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLRED, alpha=0.8))

# Panel 2: Variation 1 (Lax penalty)
im2 = ax2.imshow(penalty_matrix, cmap='YlOrRd', aspect='auto', vmin=-3, vmax=10)
for i in range(3):
    for j in range(3):
        ax2.text(j, i, int(penalty_matrix[i, j]), ha='center', va='center',
                fontsize=14, fontweight='bold', color='black')

# Highlight Nash (Medium, Medium) in green
nash_rect2 = plt.Rectangle((1-0.5, 1-0.5), 1, 1, fill=False, edgecolor=MLGREEN, linewidth=4)
ax2.add_patch(nash_rect2)

ax2.set_xticks(range(3))
ax2.set_yticks(range(3))
ax2.set_xticklabels(strategies)
ax2.set_yticklabels(strategies)
ax2.set_xlabel('Country B Strategy (category)')
ax2.set_ylabel('Country A Strategy (category)')
ax2.set_title('Variation 1: Lax Penalty (-5), Nash = (Medium, Medium) = 6')

ax2.annotate('Nash (6)', xy=(1, 1), xytext=(2.2, 0.5),
            fontsize=10, fontweight='bold', color=MLGREEN,
            arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLGREEN, alpha=0.8))

# Panel 3: Variation 2 (Strict subsidy)
im3 = ax3.imshow(subsidy_matrix, cmap='YlOrRd', aspect='auto', vmin=-3, vmax=10)
for i in range(3):
    for j in range(3):
        ax3.text(j, i, int(subsidy_matrix[i, j]), ha='center', va='center',
                fontsize=14, fontweight='bold', color='black')

# Highlight Nash (Strict, Strict) in green
nash_rect3 = plt.Rectangle((0-0.5, 0-0.5), 1, 1, fill=False, edgecolor=MLGREEN, linewidth=4)
ax3.add_patch(nash_rect3)

ax3.set_xticks(range(3))
ax3.set_yticks(range(3))
ax3.set_xticklabels(strategies)
ax3.set_yticklabels(strategies)
ax3.set_xlabel('Country B Strategy (category)')
ax3.set_ylabel('Country A Strategy (category)')
ax3.set_title('Variation 2: Strict Subsidy (+3), Nash = (Strict, Strict) = 10')

ax3.annotate('Nash (10)', xy=(0, 0), xytext=(1.5, 1.5),
            fontsize=10, fontweight='bold', color=MLGREEN,
            arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLGREEN, alpha=0.8))

# Panel 4: Variation 3 (200 rounds)
rounds = 200
time = np.arange(1, rounds + 1)

# Nash strategy: constant payoff at Nash equilibrium
nash_payoff = np.ones(rounds) * 4  # Payoff at (Lax, Lax)

# Tit-for-tat strategy: mostly cooperative (payoff=7), occasional punishment (payoff=2)
tit_for_tat_payoff = np.ones(rounds) * 7
# Add defections/punishments at rounds 10, 25, 40 (each lasts 2 rounds)
defection_rounds = [10, 25, 40]
for r in defection_rounds:
    if r+2 <= rounds:
        tit_for_tat_payoff[r:r+2] = 2

# Calculate cumulative payoffs
nash_cumulative = np.cumsum(nash_payoff)
tft_cumulative = np.cumsum(tit_for_tat_payoff)

ax4.plot(time, nash_cumulative, color=MLRED, linewidth=2.5, label='Always-Lax (Nash)')
ax4.plot(time, tft_cumulative, color=MLGREEN, linewidth=2.5, label='Tit-for-Tat')

# Add annotations at key points
ax4.annotate(f'50 rounds:\nNash=200\nTfT=320',
            xy=(50, nash_cumulative[49]), xytext=(80, 350),
            fontsize=9, color='black',
            arrowprops=dict(arrowstyle='->', color='black', lw=1),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black', alpha=0.8))

ax4.annotate(f'200 rounds:\nNash=800\nTfT=1370\n(advantage=570)',
            xy=(200, tft_cumulative[-1]), xytext=(120, 1100),
            fontsize=9, color=MLGREEN, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLGREEN, alpha=0.8))

ax4.set_xlabel('Round')
ax4.set_ylabel('Cumulative Payoff')
ax4.set_title('Variation 3: Extended Game (200 Rounds) - Cooperation Scales with Time')
ax4.legend(loc='upper left')
ax4.grid(True, alpha=0.3)

# Add colorbar for heatmaps
cbar = plt.colorbar(im1, ax=[ax1, ax2, ax3], location='right', pad=0.05, fraction=0.03)
cbar.set_label('Payoff (utility)', rotation=270, labelpad=20)

# Overall title
fig.suptitle('Regulatory Competition: How Penalties, Subsidies, and Repetition Change Equilibria',
             fontsize=16, fontweight='bold', y=0.995)

# Add economic model formula as text
formula_text = r'$\Pi = B(a) - C(r) - P(d) \cdot F$'
fig.text(0.5, 0.01, f'Economic Model (Regulatory Arbitrage Payoff): {formula_text}',
         ha='center', fontsize=11, style='italic', color='#333333')

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart_varied.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart_varied.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart_varied.pdf and chart_varied.png")
