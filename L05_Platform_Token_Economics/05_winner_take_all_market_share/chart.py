"""Winner-Take-All Market Dynamics: Gibrat's Law Simulation

Emergence of market concentration through stochastic growth.
Theory: Gibrat (1931) "Law of Proportionate Effect"
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (12, 7), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

colors = [MLBLUE, MLORANGE, MLGREEN, MLPURPLE, MLRED]

def gibrat_simulation(n_firms=100, n_periods=50, mu=0.0, sigma=0.15, failure_threshold=0.01):
    """
    Simulate Gibrat's Law: Size_t = Size_{t-1} * (1 + ε_t), where ε_t ~ N(μ, σ²)

    Parameters:
    -----------
    n_firms : int
        Initial number of firms (platforms)
    n_periods : int
        Number of time periods to simulate
    mu : float
        Mean growth rate
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
    shares = shares[shares > 0]  # Remove zeros
    shares = np.sort(shares)
    n = len(shares)
    if n == 0:
        return 0
    cumulative = np.cumsum(shares)
    return (2 * np.sum((n - np.arange(n)) * shares)) / (n * np.sum(shares)) - (n + 1) / n

def calculate_cr4(shares):
    """Calculate Concentration Ratio (top 4 firms)"""
    shares_sorted = np.sort(shares)[::-1]
    return np.sum(shares_sorted[:4])

# Main simulation
n_firms = 100
n_periods = 50

sizes_history, active_history = gibrat_simulation(
    n_firms=n_firms,
    n_periods=n_periods,
    mu=0.0,
    sigma=0.15,
    failure_threshold=0.01
)

# Calculate metrics over time
hhi_history = []
gini_history = []
cr4_history = []
n_active_history = []

for sizes in sizes_history:
    active_sizes = sizes[sizes > 0]
    if len(active_sizes) > 0:
        shares = active_sizes / np.sum(active_sizes)
        hhi_history.append(calculate_hhi(shares))
        gini_history.append(calculate_gini(shares))
        cr4_history.append(calculate_cr4(shares))
        n_active_history.append(len(active_sizes))
    else:
        hhi_history.append(0)
        gini_history.append(0)
        cr4_history.append(0)
        n_active_history.append(0)

# Create figure with subplots
fig = plt.figure(figsize=(14, 8))
gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

# Main plot: Market share distribution at T=0, T=25, T=50
ax_main = fig.add_subplot(gs[0, :])

periods_to_show = [0, 25, 50]
x_positions = [0, 1, 2]
width = 0.8

for idx, period in enumerate(periods_to_show):
    sizes = sizes_history[period]
    active_sizes = sizes[sizes > 0]
    shares = active_sizes / np.sum(active_sizes)
    shares_sorted = np.sort(shares)[::-1][:20]  # Top 20 firms

    x_offset = x_positions[idx] * (len(shares_sorted) + 5)
    bars = ax_main.bar(np.arange(len(shares_sorted)) + x_offset, shares_sorted,
                       width=width, alpha=0.7,
                       color=MLBLUE if idx == 0 else (MLORANGE if idx == 1 else MLGREEN))

    # Add label
    ax_main.text(x_offset + len(shares_sorted)/2 - 2, max(shares_sorted) * 1.05,
                f'T={period}\n({len(active_sizes)} firms)',
                ha='center', fontsize=12, fontweight='bold')

ax_main.set_xlabel('Firm Rank (Top 20)', fontsize=13)
ax_main.set_ylabel('Market Share', fontsize=13)
ax_main.set_title('Winner-Take-All Emergence via Gibrat\'s Law (1931)', fontsize=16, fontweight='bold')
ax_main.grid(True, alpha=0.3, linestyle='--', axis='y')
ax_main.set_ylim(0, max([max(sizes_history[p][sizes_history[p] > 0] / np.sum(sizes_history[p][sizes_history[p] > 0]))
                         for p in periods_to_show]) * 1.2)

# Remove x-ticks (not meaningful across periods)
ax_main.set_xticks([])

# Subplot 1: HHI over time
ax1 = fig.add_subplot(gs[1, 0])
ax1.plot(hhi_history, color=MLBLUE, linewidth=2)
ax1.set_xlabel('Time Period', fontsize=12)
ax1.set_ylabel('HHI', fontsize=12)
ax1.set_title('Herfindahl-Hirschman Index', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.axhline(y=0.15, color='red', linestyle='--', alpha=0.5, linewidth=1)
ax1.text(n_periods * 0.5, 0.16, 'Moderate Concentration', fontsize=9, color='red', alpha=0.7)

# Subplot 2: Gini coefficient over time
ax2 = fig.add_subplot(gs[1, 1])
ax2.plot(gini_history, color=MLORANGE, linewidth=2)
ax2.set_xlabel('Time Period', fontsize=12)
ax2.set_ylabel('Gini Coefficient', fontsize=12)
ax2.set_title('Inequality (Gini)', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, linestyle='--')

# Subplot 3: CR4 and Number of active firms
ax3 = fig.add_subplot(gs[1, 2])
ax3_twin = ax3.twinx()

ax3.plot(cr4_history, color=MLGREEN, linewidth=2, label='CR4 (Top 4)')
ax3.set_xlabel('Time Period', fontsize=12)
ax3.set_ylabel('CR4 (Top 4 Share)', fontsize=12, color=MLGREEN)
ax3.tick_params(axis='y', labelcolor=MLGREEN)
ax3.grid(True, alpha=0.3, linestyle='--')

ax3_twin.plot(n_active_history, color=MLRED, linewidth=2, linestyle='--', label='Active Firms')
ax3_twin.set_ylabel('Number of Active Firms', fontsize=12, color=MLRED)
ax3_twin.tick_params(axis='y', labelcolor=MLRED)

ax3.set_title('Concentration & Survival', fontsize=13, fontweight='bold')

# Add annotation
fig.text(0.5, 0.01,
         'Gibrat (1931): Proportional random growth → Power law distribution → Winner-Take-All',
         ha='center', fontsize=11, style='italic', color='gray')

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
