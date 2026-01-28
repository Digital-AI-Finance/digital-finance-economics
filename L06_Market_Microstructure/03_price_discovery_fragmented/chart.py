"""Price Discovery in Fragmented Markets"""
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

# Generate Exchange 1 with shock at step 100
steps = 200
returns = np.random.normal(0, 0.5, steps)
returns[100] += 3  # Add shock
exchange1 = 100 + np.cumsum(returns)

# Generate other exchanges with lags and noise
exchange2 = np.zeros(steps)
exchange3 = np.zeros(steps)
exchange4 = np.zeros(steps)

exchange2[0] = exchange1[0]
exchange3[0] = exchange1[0]
exchange4[0] = exchange1[0]

for i in range(1, steps):
    exchange2[i] = exchange1[max(0, i-1)] + np.random.normal(0, 0.2)
    exchange3[i] = exchange1[max(0, i-2)] + np.random.normal(0, 0.3)
    exchange4[i] = exchange1[max(0, i-3)] + np.random.normal(0, 0.4)

# Create main plot with inset
fig, ax = plt.subplots()

time = np.arange(steps)
ax.plot(time, exchange1, label='Exchange 1 (Leader)', color=MLBLUE, linewidth=2)
ax.plot(time, exchange2, label='Exchange 2 (Lag 1)', color=MLGREEN, alpha=0.8)
ax.plot(time, exchange3, label='Exchange 3 (Lag 2)', color=MLORANGE, alpha=0.8)
ax.plot(time, exchange4, label='Exchange 4 (Lag 3)', color=MLRED, alpha=0.8)

ax.set_xlabel('Time Steps')
ax.set_ylabel('Price ($)')
ax.set_title('Price Discovery Across Fragmented Exchanges')
ax.legend()
ax.grid(alpha=0.3)

# Add inset with correlation heatmap
ax_inset = fig.add_axes([0.65, 0.15, 0.25, 0.25])
prices_matrix = np.vstack([exchange1, exchange2, exchange3, exchange4])
corr_matrix = np.corrcoef(prices_matrix)

im = ax_inset.imshow(corr_matrix, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto')
ax_inset.set_xticks([0, 1, 2, 3])
ax_inset.set_yticks([0, 1, 2, 3])
ax_inset.set_xticklabels(['E1', 'E2', 'E3', 'E4'], fontsize=10)
ax_inset.set_yticklabels(['E1', 'E2', 'E3', 'E4'], fontsize=10)
ax_inset.set_title('Correlation', fontsize=11)

# Add correlation values
for i in range(4):
    for j in range(4):
        text = ax_inset.text(j, i, f'{corr_matrix[i, j]:.2f}',
                            ha="center", va="center", color="black", fontsize=9)

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
