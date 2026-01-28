"""Winner-Take-All: Polya Urn Market Concentration"""
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

colors = [MLBLUE, MLORANGE, MLGREEN, MLPURPLE, MLRED]

def polya_urn_simulation(n_platforms, n_users, seed):
    """Simulate Polya urn process for market share evolution"""
    np.random.seed(seed)

    # Initialize with 1 user per platform
    counts = np.ones(n_platforms, dtype=int)
    history = [counts.copy()]

    # Add remaining users
    for _ in range(n_users - n_platforms):
        # Probability proportional to (current count + 1)
        probs = (counts + 1) / (counts.sum() + n_platforms)
        chosen = np.random.choice(n_platforms, p=probs)
        counts[chosen] += 1
        history.append(counts.copy())

    return np.array(history)

# Main simulation
n_platforms = 5
n_users = 10000

history = polya_urn_simulation(n_platforms, n_users, seed=42)
market_shares = history / history.sum(axis=1, keepdims=True)

# Create figure with main plot and inset
fig, ax = plt.subplots()

# Stacked area chart
x = np.arange(len(history))
ax.stackplot(x, market_shares.T, colors=colors, alpha=0.8,
             labels=[f'Platform {i+1}' for i in range(n_platforms)])

ax.set_xlabel('Number of Users')
ax.set_ylabel('Market Share')
ax.set_title('Winner-Take-All Dynamics: Path Dependence')
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3, linestyle='--', axis='y')
ax.set_xlim(0, n_users)
ax.set_ylim(0, 1)

# Format x-axis for readability
ax.set_xticks([0, 2500, 5000, 7500, 10000])
ax.set_xticklabels(['0', '2.5k', '5k', '7.5k', '10k'])

# Create inset showing path dependence across different seeds
inset_ax = fig.add_axes([0.55, 0.15, 0.38, 0.35])

seeds_to_show = [43, 44, 45, 46]
bar_width = 0.15
x_pos = np.arange(n_platforms)

for idx, seed in enumerate(seeds_to_show):
    final_shares = polya_urn_simulation(n_platforms, n_users, seed)[-1]
    final_shares = final_shares / final_shares.sum()

    offset = (idx - len(seeds_to_show)/2 + 0.5) * bar_width
    bars = inset_ax.bar(x_pos + offset, final_shares, bar_width,
                        label=f'Seed {seed}', alpha=0.7)

    # Color bars by platform
    for bar, color in zip(bars, colors):
        bar.set_color(color)

inset_ax.set_xlabel('Platform', fontsize=10)
inset_ax.set_ylabel('Final Share', fontsize=10)
inset_ax.set_title('Path Dependence\n(Different Random Seeds)', fontsize=11)
inset_ax.set_xticks(x_pos)
inset_ax.set_xticklabels([f'{i+1}' for i in range(n_platforms)], fontsize=9)
inset_ax.tick_params(labelsize=9)
inset_ax.grid(True, alpha=0.3, linestyle='--', axis='y')
inset_ax.set_ylim(0, 1)
inset_ax.legend(fontsize=8, loc='upper right')

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
