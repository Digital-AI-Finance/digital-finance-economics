r"""Composability Risk in DeFi Protocol Stacks
# Multi-panel override: comparative statics requires simultaneous visibility

$P(fail) = 1 - \prod (1-p_i)$. Based on Werner et al. (2022).

Economic Model:
Chain failure probability for composed protocols:
$P(\text{chain failure}) = 1 - \prod_{i=1}^{n}(1 - p_i)$
Each layer adds independent failure risk. Even small per-layer probabilities
compound rapidly as stack depth increases.

Citation: Werner, Perez, Gudgeon, Klages-Mundt, Harz & Knottenbelt (2022) - SoK: Decentralized Finance
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 11, 'axes.titlesize': 13,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# ── Parameters ──
p_values = [0.001, 0.005, 0.01, 0.02, 0.05]
n_layers = np.arange(1, 21)

# DeFi stack example
defi_stack = [
    ('L1 Consensus', 0.001, MLPURPLE),
    ('Bridge', 0.02, MLRED),
    ('Lending', 0.01, MLBLUE),
    ('AMM', 0.005, MLORANGE),
    ('Yield Agg.', 0.015, MLGREEN),
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ── Panel (a): Failure probability vs stack depth ──
colors_curve = [MLGREEN, MLBLUE, MLORANGE, MLRED, MLPURPLE]
for p, color in zip(p_values, colors_curve):
    chain_fail = 1 - (1 - p) ** n_layers
    ax1.plot(n_layers, chain_fail * 100, color=color, linewidth=2.2,
             label=f'p={p}', marker='o', markersize=3, alpha=0.85)

# Annotate the 10-link, p=0.01 case
p_target = 0.01
n_target = 10
fail_10 = (1 - (1 - p_target) ** n_target) * 100
ax1.annotate(f'10 links, p=0.01\nP(fail)={fail_10:.1f}%',
             xy=(n_target, fail_10),
             xytext=(n_target + 3, fail_10 + 8),
             fontsize=9, fontweight='bold', color=MLORANGE,
             arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLORANGE, alpha=0.9))

ax1.set_xlabel('Number of composed layers (n)', fontsize=11)
ax1.set_ylabel('Chain failure probability (%)', fontsize=11)
ax1.set_title(r'(a) $P(fail) = 1 - \prod(1-p_i)$ vs depth', fontsize=12, fontweight='bold')
ax1.legend(title='Per-layer p', fontsize=9, title_fontsize=9, framealpha=0.9)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(1, 20)
ax1.set_ylim(0, 100)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ── Panel (b): Annotated DeFi stack ──
layer_names = [s[0] for s in defi_stack]
layer_probs = [s[1] for s in defi_stack]
layer_colors = [s[2] for s in defi_stack]

# Draw stacked bars (bottom-up)
bar_height = 0.6
y_positions = np.arange(len(defi_stack))

# Cumulative chain failure at each layer
cumulative_fail = []
running_prod = 1.0
for p in layer_probs:
    running_prod *= (1 - p)
    cumulative_fail.append((1 - running_prod) * 100)

# Horizontal bars for individual probability
bars = ax2.barh(y_positions, [p * 100 for p in layer_probs],
                color=layer_colors, edgecolor='black', linewidth=0.8,
                alpha=0.85, height=bar_height)

ax2.set_yticks(y_positions)
ax2.set_yticklabels(layer_names, fontsize=10, fontweight='bold')
ax2.set_xlabel('Individual failure probability (%)', fontsize=11)
ax2.set_title('(b) DeFi stack: per-layer risk', fontsize=12, fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='x', alpha=0.3, linestyle='--')

# Annotate each bar with individual and cumulative probability
for i, (p, cum) in enumerate(zip(layer_probs, cumulative_fail)):
    ax2.text(p * 100 + 0.15, i, f'{p*100:.1f}%  (cum: {cum:.1f}%)',
             va='center', fontsize=9, fontweight='bold')

# Highlight total stack risk
total_fail = cumulative_fail[-1]
ax2.text(0.95, 0.05,
         f'Total stack failure:\n{total_fail:.1f}%',
         transform=ax2.transAxes, ha='right', va='bottom',
         fontsize=11, fontweight='bold', color=MLRED,
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                   edgecolor=MLRED, alpha=0.9))

# Arrow from bottom layer to annotation
ax2.annotate('',
             xy=(layer_probs[-1] * 100, len(defi_stack) - 1),
             xytext=(3.5, len(defi_stack) - 0.5),
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5, alpha=0.6))

fig.suptitle(r'Composability Risk: $P(\mathrm{chain\;fail}) = 1 - \prod_{i=1}^{n}(1-p_i)$',
             fontsize=14, fontweight='bold', y=1.01)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
