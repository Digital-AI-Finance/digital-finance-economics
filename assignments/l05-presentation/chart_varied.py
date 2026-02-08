"""Winner-Take-All Market Dynamics: Gibrat's Law Variations

Compares four scenarios to isolate drivers of market concentration.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 11, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.figsize': (16, 12), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'

def gibrat_simulation(n_firms=100, n_periods=100, mu=0.02, sigma=0.25, failure_threshold=0.1):
    """
    Simulate Gibrat's Law: Size_t = Size_{t-1} * (1 + eps_t), where eps_t ~ N(mu, sigma^2)

    Parameters:
    -----------
    n_firms : int
        Initial number of firms (platforms)
    n_periods : int
        Number of time periods to simulate
    mu : float
        Mean growth rate (slight advantage for larger firms via drift)
    sigma : float
        Standard deviation of growth rate
    failure_threshold : float
        Minimum size threshold (firms below this fail/exit)

    Returns:
    --------
    sizes_history : list of arrays
        Size distribution at each time period
    active_history : list of arrays
        Boolean mask of active firms at each time period
    """
    # Initialize with equal sizes
    sizes = np.ones(n_firms)
    sizes_history = [sizes.copy()]
    active_history = [np.ones(n_firms, dtype=bool)]

    for t in range(n_periods):
        # Gibrat's Law: proportional random growth
        growth_rates = 1 + np.random.normal(mu, sigma, n_firms)
        sizes = sizes * growth_rates

        # Firms below threshold fail
        active = sizes >= failure_threshold
        sizes[~active] = 0

        sizes_history.append(sizes.copy())
        active_history.append(active.copy())

    return sizes_history, active_history

def calculate_hhi(shares):
    """Calculate Herfindahl-Hirschman Index (sum of squared market shares)"""
    return np.sum(shares ** 2)

def calculate_gini(shares):
    """Calculate Gini coefficient of market concentration"""
    shares = shares[shares > 0]
    if len(shares) == 0:
        return 0
    shares = np.sort(shares)
    n = len(shares)
    index = np.arange(1, n + 1)
    return (np.sum((2 * index - n - 1) * shares)) / (n * np.sum(shares))

# Create 2x2 subplot
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

scenarios = [
    {'name': 'Baseline', 'n_firms': 100, 'mu': 0.02, 'sigma': 0.25, 'seed': 42, 'color_hhi': MLBLUE, 'color_gini': MLORANGE},
    {'name': 'Variation 1: Low Volatility', 'n_firms': 100, 'mu': 0.02, 'sigma': 0.05, 'seed': 42, 'color_hhi': MLGREEN, 'color_gini': MLRED},
    {'name': 'Variation 2: High Mean Growth', 'n_firms': 100, 'mu': 0.10, 'sigma': 0.25, 'seed': 42, 'color_hhi': MLPURPLE, 'color_gini': MLORANGE},
    {'name': 'Variation 3: Fewer Firms', 'n_firms': 10, 'mu': 0.02, 'sigma': 0.25, 'seed': 42, 'color_hhi': MLRED, 'color_gini': MLGREEN}
]

for idx, scenario in enumerate(scenarios):
    ax = axes[idx]

    # Set seed for reproducibility
    np.random.seed(scenario['seed'])

    # Run simulation
    sizes_history, active_history = gibrat_simulation(
        n_firms=scenario['n_firms'],
        n_periods=100,
        mu=scenario['mu'],
        sigma=scenario['sigma'],
        failure_threshold=0.1
    )

    # Calculate metrics over time
    hhi_history = []
    gini_history = []

    for sizes in sizes_history:
        active_sizes = sizes[sizes > 0]
        if len(active_sizes) > 0:
            shares = active_sizes / np.sum(active_sizes)
            hhi_history.append(calculate_hhi(shares))
            gini_history.append(calculate_gini(shares))
        else:
            hhi_history.append(0)
            gini_history.append(0)

    # Plot HHI on left y-axis
    ax_twin = ax.twinx()

    line1 = ax.plot(hhi_history, color=scenario['color_hhi'], linewidth=2.5, label='HHI')
    ax.set_xlabel('Simulation Periods', fontsize=11)
    ax.set_ylabel('HHI (Herfindahl-Hirschman Index)', fontsize=11, color=scenario['color_hhi'])
    ax.tick_params(axis='y', labelcolor=scenario['color_hhi'])
    ax.grid(True, alpha=0.3, linestyle='--')

    # Plot Gini on right y-axis
    line2 = ax_twin.plot(gini_history, color=scenario['color_gini'], linewidth=2.5, linestyle='--', label='Gini')
    ax_twin.set_ylabel('Gini Coefficient', fontsize=11, color=scenario['color_gini'])
    ax_twin.tick_params(axis='y', labelcolor=scenario['color_gini'])
    ax_twin.set_ylim(0, 1)

    # Add scenario title and parameters
    param_text = f"n={scenario['n_firms']}, μ={scenario['mu']}, σ={scenario['sigma']}"
    ax.set_title(f"{scenario['name']}\n{param_text}", fontsize=12, fontweight='bold')

    # Add legend
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='upper left', frameon=True, fancybox=True)

    # Add final values annotation
    final_hhi = hhi_history[-1]
    final_gini = gini_history[-1]
    ax.text(0.98, 0.50, f'Final:\nHHI = {final_hhi:.3f}\nGini = {final_gini:.3f}',
            transform=ax.transAxes, fontsize=9, ha='right', va='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                     edgecolor='gray', linewidth=1, alpha=0.9))

fig.suptitle('Gibrat\'s Law: How Growth Parameters Affect Market Concentration',
             fontsize=15, fontweight='bold', y=0.995)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart_varied.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart_varied.png', dpi=150, bbox_inches='tight')
plt.close()
print("Variation chart saved to chart_varied.pdf and chart_varied.png")
