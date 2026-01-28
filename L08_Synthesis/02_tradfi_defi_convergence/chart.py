"""TradFi-DeFi Convergence Scenarios"""
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

# Time axis
years = np.linspace(0, 20, 100)

# Sigmoid transition function
def sigmoid_transition(t, start_val, end_val, midpoint=10, steepness=0.5):
    return start_val + (end_val - start_val) / (1 + np.exp(-steepness * (t - midpoint)))

# Scenario A: Absorption
tradfi_a = sigmoid_transition(years, 0.9, 0.85, midpoint=10, steepness=0.3)
defi_a = sigmoid_transition(years, 0.1, 0.02, midpoint=10, steepness=0.3)
hybrid_a = 1 - tradfi_a - defi_a

# Scenario B: Coexistence
tradfi_b = sigmoid_transition(years, 0.9, 0.5, midpoint=10, steepness=0.4)
defi_b = sigmoid_transition(years, 0.1, 0.3, midpoint=10, steepness=0.4)
hybrid_b = 1 - tradfi_b - defi_b

# Scenario C: Displacement
tradfi_c = sigmoid_transition(years, 0.9, 0.15, midpoint=10, steepness=0.5)
defi_c = sigmoid_transition(years, 0.1, 0.6, midpoint=10, steepness=0.5)
hybrid_c = 1 - tradfi_c - defi_c

# Visualization
fig, axes = plt.subplots(1, 3, figsize=(14, 4))

scenarios = [
    ('A: Absorption', tradfi_a, defi_a, hybrid_a),
    ('B: Coexistence', tradfi_b, defi_b, hybrid_b),
    ('C: Displacement', tradfi_c, defi_c, hybrid_c)
]

for ax, (title, tradfi, defi, hybrid) in zip(axes, scenarios):
    ax.stackplot(years, tradfi, defi, hybrid,
                 colors=[MLBLUE, MLORANGE, MLPURPLE],
                 labels=['TradFi', 'DeFi', 'Hybrid'],
                 alpha=0.8)

    ax.set_xlabel('Years')
    ax.set_ylabel('Market Share')
    ax.set_title(title)
    ax.set_ylim(0, 1)
    ax.grid(alpha=0.3)
    ax.legend(loc='upper right', fontsize=11)

plt.suptitle('TradFi-DeFi Convergence Scenarios', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
