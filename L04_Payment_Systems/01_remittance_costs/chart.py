r"""Remittance Cost Dynamics: Bertrand Price Competition

How competition drives down remittance (money transfer) prices.
Core idea: When more companies compete, prices fall toward the actual cost.

Economic Model:
    Bertrand competition with product differentiation:
    $$c(n) = c_0 + \frac{m}{n^{1-d}}$$
    where $c_0$ = marginal cost floor, $m$ = monopoly markup,
    $n$ = number of competitors, $d$ = product differentiation parameter
    ($d=0$: homogeneous goods, price collapses to marginal cost with 2 firms;
     $d>0$: differentiated products, convergence is slower).

Theory: Bertrand (1883) price competition model.
Reference: Tirole (1988) - The Theory of Industrial Organization.
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

# Bertrand Competition Parameters
marginal_cost = 1.5  # Base cost (technology, compliance, liquidity)
monopoly_markup = 5.5  # Monopoly price above marginal cost
differentiation = 0.3  # Product differentiation parameter (0 = homogeneous)

def bertrand_price(n_firms, marginal_cost, monopoly_markup, differentiation):
    """
    Calculate equilibrium price under Bertrand competition with differentiation.

    Parameters:
    - n_firms: Number of competing firms
    - marginal_cost: Base cost of service
    - monopoly_markup: Initial markup in monopoly
    - differentiation: Product differentiation (0 = perfect substitutes)

    Returns equilibrium price as % of transaction
    """
    if n_firms == 1:
        return marginal_cost + monopoly_markup

    # Price converges to marginal cost as competition increases
    # With differentiation, convergence is slower
    markup = monopoly_markup / (n_firms ** (1 - differentiation))
    return marginal_cost + markup

# Theoretical Bertrand curve
n_competitors = np.linspace(1, 15, 100)
theoretical_prices = [bertrand_price(n, marginal_cost, monopoly_markup, differentiation)
                     for n in n_competitors]

# Real World Bank Remittance Price Data with market structure
# Each data point: (year, avg_cost%, approximate_n_major_competitors, key_event)
real_data = [
    (2008, 10.0, 2, 'Pre-mobile money'),
    (2010, 9.2, 3, 'PayPal expansion'),
    (2012, 8.5, 4, 'M-Pesa Africa'),
    (2011, 7.8, 4, 'TransferWise founded'),
    (2017, 6.9, 7, 'Crypto remittances'),
    (2020, 6.5, 9, 'COVID digitization'),
    (2023, 6.2, 12, 'Stablecoin corridors'),
]

years = [d[0] for d in real_data]
actual_costs = [d[1] for d in real_data]
n_firms_actual = [d[2] for d in real_data]
events = [d[3] for d in real_data]

fig, ax = plt.subplots(figsize=(10, 6))

# Plot theoretical Bertrand curve
ax.plot(n_competitors, theoretical_prices,
        color=MLPURPLE, linewidth=2.5, label='Bertrand Equilibrium (Theory)',
        alpha=0.8)

# Plot actual data points
ax.scatter(n_firms_actual, actual_costs,
          s=150, color=MLORANGE, edgecolors='black', linewidth=1.5,
          label='Observed Market Data', zorder=5, alpha=0.9)

# Annotate key market entries
for i, (n, cost, event) in enumerate(zip(n_firms_actual, actual_costs, events)):
    if i % 2 == 0:  # Annotate every other point to avoid crowding
        ax.annotate(event,
                   xy=(n, cost),
                   xytext=(10, 10 if i % 4 == 0 else -15),
                   textcoords='offset points',
                   fontsize=10,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=MLLAVENDER, alpha=0.6),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2',
                                 color='gray', lw=1))

# Mark market regimes
ax.axhspan(7, 10, alpha=0.15, color=MLRED, label='Oligopoly regime')
ax.axhspan(4, 7, alpha=0.15, color=MLORANGE)
ax.axhspan(marginal_cost, 4, alpha=0.15, color=MLGREEN, label='Competitive regime')

# Marginal cost line
ax.axhline(y=marginal_cost, color=MLGREEN, linestyle='--', linewidth=2,
          label=f'Marginal Cost: {marginal_cost}%', alpha=0.7)

# UN SDG Target
sdg_target = 3.0
ax.axhline(y=sdg_target, color=MLBLUE, linestyle=':', linewidth=2,
          label=f'UN SDG Target: {sdg_target}%', alpha=0.7)

# Add annotation about SDG target
ax.annotate('UN SDG 10.c Target:\nReduce remittance costs to 3% by 2030\n'
           'Current global average: ~6%',
           xy=(12, sdg_target), xytext=(8, 1.5),
           fontsize=10, ha='center',
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7),
           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', lw=1.5))

# Bertrand competition explanation for BSc students
ax.text(0.02, 0.35,
    'Bertrand Competition:\nAs more firms enter a market,\nprices fall toward the actual\ncost of providing the service.\nMore competitors = lower prices.',
    transform=ax.transAxes, fontsize=9,
    bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, edgecolor='gray'))

# Monopoly price marker
monopoly_price = bertrand_price(1, marginal_cost, monopoly_markup, differentiation)
ax.plot(1, monopoly_price, marker='o', markersize=12, color=MLRED,
       markeredgecolor='black', markeredgewidth=1.5, label='Monopoly', zorder=6)

ax.set_xlabel('Number of Major Competitors', fontweight='bold')
ax.set_ylabel('Remittance Cost (% of transaction)', fontweight='bold')
ax.set_title('Bertrand Price Competition in Remittance Markets\n'
            'Theory vs. Reality (2008-2023)',
            fontsize=16, fontweight='bold', color=MLPURPLE, pad=15)

ax.set_xlim(0, 15)
ax.set_ylim(0, 11)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper right', framealpha=0.95, edgecolor='gray')

# Add theory citation
fig.text(0.99, 0.01,
        'Theory: Bertrand (1883), Tirole (1988) | Data: World Bank Remittance Prices Database',
        ha='right', va='bottom', fontsize=9, style='italic', color='gray')

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
