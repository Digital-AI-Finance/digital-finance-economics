r"""Two-Sided Market: Interchange Fee Optimization

This chart demonstrates the Rochet-Tirole two-sided market model applied to
payment systems. It shows how the platform balances merchant acceptance and
consumer adoption through interchange fee optimization to maximize transaction
volume and profit.

Economic Model: Rochet-Tirole Two-Sided Pricing
- Price constraint: $p_B + p_S = c + m$ where $p_B$ = buyer price, $p_S$ = seller price
- Platform profit: $\pi = (p_B + p_S - c) \cdot Q(p_B, p_S)$
- Optimal interchange fee $f^*$ balances: $\frac{\partial Q}{\partial p_B} = -\frac{\partial Q}{\partial p_S}$
- Network effects: $Q = D_B(p_B) \cdot D_S(p_S)$ (both sides must participate)

Citation: Rochet & Tirole (2003) - Platform Competition in Two-Sided Markets
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

# Simulation parameters
f = np.linspace(0, 5, 100)  # Interchange fee from 0% to 5%

# Merchant acceptance: declines linearly with fee
merchant_acceptance = np.maximum(0, 1 - f/5)

# Consumer adoption: sigmoid function (higher fee = more rewards = more adoption)
consumer_adoption = 1 / (1 + np.exp(-3*(f - 1.5)))

# Transaction volume
transaction_volume = merchant_acceptance * consumer_adoption * 1000

# Platform profit
platform_profit = (f/100) * transaction_volume

# Find optimal interchange fee
optimal_idx = np.argmax(platform_profit)
optimal_fee = f[optimal_idx]
optimal_profit = platform_profit[optimal_idx]

# Create plot with normalized values
fig, ax1 = plt.subplots()

# Normalize profit for comparison
profit_normalized = platform_profit / np.max(platform_profit)

# Plot all three curves on same scale
ax1.plot(f, merchant_acceptance, label='Merchant Acceptance',
         color=MLGREEN, linewidth=2.5)
ax1.plot(f, consumer_adoption, label='Consumer Adoption',
         color=MLBLUE, linewidth=2.5)
ax1.plot(f, profit_normalized, label='Platform Profit (normalized)',
         color=MLPURPLE, linewidth=3, linestyle='-')

# Mark optimal fee
ax1.axvline(x=optimal_fee, color=MLRED, linestyle='--',
            linewidth=1.5, alpha=0.7)

# Add annotation for optimal fee
ax1.annotate(f'Optimal interchange fee:\n{optimal_fee:.2f}%',
            xy=(optimal_fee, profit_normalized[optimal_idx]),
            xytext=(optimal_fee + 0.8, 0.7),
            fontsize=12,
            bbox=dict(boxstyle='round,pad=0.5', facecolor=MLLAVENDER, alpha=0.8),
            arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5))

# Labels and title
ax1.set_xlabel('Interchange Fee (%)')
ax1.set_ylabel('Normalized Value [0, 1]')
ax1.set_title('Two-Sided Market: Balancing Merchants and Consumers\n(Goal: Set fees to maximize total transactions on the platform)')
ax1.set_xlim(0, 5)
ax1.set_ylim(0, 1.05)
ax1.legend(loc='upper right', framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--')

# C3: Add theory explanation annotation
theory_text = ('Rochet-Tirole Two-Sided Market Model:\n'
               'Platform must balance two sides with opposing fee preferences.\n'
               'Optimal interchange fee maximizes total platform profit\n'
               'by balancing merchant acceptance vs consumer adoption.')
ax1.text(0.5, -0.15, theory_text, transform=ax1.transAxes,
        fontsize=9, ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=MLLAVENDER, edgecolor=MLPURPLE, alpha=0.7))

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
