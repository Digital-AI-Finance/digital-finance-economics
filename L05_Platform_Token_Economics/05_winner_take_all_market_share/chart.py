"""Winner-Take-All Market Dynamics: Gibrat's Law Simulation

Emergence of market concentration through stochastic growth.
Theory: Gibrat (1931) "Law of Proportionate Effect"

Economic Model:
  Gibrat's Law: $S_{i,t} = S_{i,t-1} \\cdot (1 + \\varepsilon_{i,t})$, $\\varepsilon \\sim N(\\mu, \\sigma^2)$
  Herfindahl-Hirschman Index: $HHI = \\sum_i s_i^2$
  Gini coefficient: $G = \\frac{\\sum_{i=1}^{n} (2i - n - 1) x_i}{n \\sum_{i=1}^{n} x_i}$ (sorted ascending)
  Concentration Ratio: $CR_4 = \\sum_{i=1}^{4} s_i$ (top 4 shares)

Citation: Gibrat (1931), Arthur (1989) - Increasing Returns and Path Dependence

Based on: Arthur (1989) - Increasing Returns and Path Dependence
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

def calculate_cr4(shares):
    """Calculate Concentration Ratio (top 4 firms)"""
    shares_sorted = np.sort(shares)[::-1]
    return np.sum(shares_sorted[:4])

# Main simulation
n_firms = 100
n_periods = 100

sizes_history, active_history = gibrat_simulation(
    n_firms=n_firms,
    n_periods=n_periods,
    mu=0.02,
    sigma=0.25,
    failure_threshold=0.1
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
gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)

# Main plot: Market share distribution at T=0, T=50, T=100
ax_main = fig.add_subplot(gs[0, :])

periods_to_show = [0, 50, 100]
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
ax_main.set_ylabel('Market Share (fraction)', fontsize=13)
ax_main.set_title('How Random Growth Creates Market Concentration', fontsize=16, fontweight='bold')
ax_main.grid(True, alpha=0.3, linestyle='--', axis='y')
ax_main.set_ylim(0, max([max(sizes_history[p][sizes_history[p] > 0] / np.sum(sizes_history[p][sizes_history[p] > 0]))
                         for p in periods_to_show]) * 1.2)

# Annotation highlighting winner dominance at final period
sizes_final = sizes_history[n_periods]
active_sizes_final = sizes_final[sizes_final > 0]
shares_final = active_sizes_final / np.sum(active_sizes_final)
max_share = np.max(shares_final)
x_offset_final = x_positions[2] * (20 + 5)
ax_main.annotate(f'Leader: {max_share*100:.1f}%',
                xy=(x_offset_final, max_share),
                xytext=(x_offset_final + 8, max_share * 0.55),
                fontsize=10, fontweight='bold', color=MLGREEN,
                arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLGREEN, alpha=0.8))

# Remove x-ticks (not meaningful across periods)
ax_main.set_xticks([])

# Add legend for time periods -- upper center to avoid T=50/T=100 labels
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=MLBLUE, alpha=0.7, label='T=0 (Equal start)'),
    Patch(facecolor=MLORANGE, alpha=0.7, label='T=50 (Diverging)'),
    Patch(facecolor=MLGREEN, alpha=0.7, label=f'T={n_periods} (Winner emerges)')
]
ax_main.legend(handles=legend_elements, loc='upper center', frameon=True, fancybox=True,
               ncol=3, bbox_to_anchor=(0.5, 0.98))

# Gibrat's Law boxed annotation in main plot
ax_main.text(0.98, 0.70,
             "Gibrat's Law: Each firm grows by\n"
             "a random percentage. Over time,\n"
             "this concentrates the market.",
             transform=ax_main.transAxes, fontsize=10, ha='right', va='top',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                      edgecolor=MLORANGE, linewidth=1.5, alpha=0.9))

# Subplot 1: HHI over time
ax1 = fig.add_subplot(gs[1, 0])
ax1.plot(hhi_history, color=MLBLUE, linewidth=2)
ax1.set_xlabel('Simulation Rounds', fontsize=12)
ax1.set_ylabel('HHI', fontsize=12)
ax1.set_title('Herfindahl-Hirschman Index', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3, linestyle='--')

# Only add DOJ threshold line if HHI reaches close to it
max_hhi = max(hhi_history)
if max_hhi > 0.10:
    ax1.axhline(y=0.15, color='red', linestyle='--', alpha=0.5, linewidth=1)
    ax1.text(n_periods * 0.3, 0.155, 'U.S. DOJ: moderately\nconcentrated', fontsize=8, color='red', alpha=0.7)
    ax1.axhline(y=0.25, color='darkred', linestyle='--', alpha=0.4, linewidth=1)
    ax1.text(n_periods * 0.3, 0.255, 'U.S. DOJ: highly\nconcentrated', fontsize=8, color='darkred', alpha=0.6)

# Add HHI explanation annotation
ax1.text(0.02, 0.95, 'Sum of squared market shares\n(Higher = more concentrated)',
        transform=ax1.transAxes, fontsize=8,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.6))

# Subplot 2: Gini coefficient over time
ax2 = fig.add_subplot(gs[1, 1])
ax2.plot(gini_history, color=MLORANGE, linewidth=2)
ax2.set_xlabel('Simulation Rounds', fontsize=12)
ax2.set_ylabel('Gini Coefficient', fontsize=12)
ax2.set_title('Inequality (Gini)', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, linestyle='--')

# Add Gini explanation annotation
ax2.text(0.02, 0.95, 'Inequality: 0 = equal, 1 = monopoly',
        transform=ax2.transAxes, fontsize=8,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.6))

# Subplot 3: CR4 and Number of active firms
ax3 = fig.add_subplot(gs[1, 2])

# Check if firms actually exit
final_active = n_active_history[-1]
if final_active < n_firms * 0.95:
    # Firms exited -- show dual-axis
    ax3_twin = ax3.twinx()
    ax3.plot(cr4_history, color=MLGREEN, linewidth=2, label='CR4 (Top 4)')
    ax3.set_xlabel('Simulation Rounds', fontsize=12)
    ax3.set_ylabel('CR4 (Top 4 Share)', fontsize=12, color=MLGREEN)
    ax3.tick_params(axis='y', labelcolor=MLGREEN)
    ax3.grid(True, alpha=0.3, linestyle='--')

    ax3_twin.plot(n_active_history, color=MLRED, linewidth=2, linestyle='--', label='Active Firms')
    ax3_twin.set_ylabel('Active Firms', fontsize=12, color=MLRED)
    ax3_twin.tick_params(axis='y', labelcolor=MLRED)
else:
    # No meaningful exits -- show only CR4
    ax3.plot(cr4_history, color=MLGREEN, linewidth=2, label='CR4 (Top 4)')
    ax3.set_xlabel('Simulation Rounds', fontsize=12)
    ax3.set_ylabel('CR4 (Top 4 Share)', fontsize=12, color=MLGREEN)
    ax3.tick_params(axis='y', labelcolor=MLGREEN)
    ax3.grid(True, alpha=0.3, linestyle='--')

ax3.set_title('Concentration & Survival', fontsize=13, fontweight='bold')

fig.subplots_adjust(left=0.06, right=0.94, top=0.93, bottom=0.08, hspace=0.35, wspace=0.3)
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
