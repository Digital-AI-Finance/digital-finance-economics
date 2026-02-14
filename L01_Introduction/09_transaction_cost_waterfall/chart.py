r"""Transaction Cost Waterfall: Coase-Williamson Decomposition

Multi-panel override: comparative statics requires simultaneous visibility

Panel (a): Grouped stacked bar chart of transaction cost components.
Panel (b): Percentage reduction versus cash baseline.

Economic Model:
$TC_{total} = TC_{search} + TC_{verify} + TC_{settle} + TC_{comply}$.
Based on Coase (1937), Williamson (1985).
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 11,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Transaction cost components per $100 transaction
methods = ['Cash', 'Card', 'Crypto', 'CBDC']
components = ['Search', 'Verification', 'Settlement', 'Compliance']
colors = [MLORANGE, MLBLUE, MLGREEN, MLLAVENDER]

# Cost data (per $100 transaction)
costs = {
    'Cash':   [0.50, 0.20, 0.30, 0.00],  # total = $1.00
    'Card':   [0.10, 0.15, 0.25, 0.50],  # total = $1.00
    'Crypto': [0.05, 0.10, 0.05, 0.30],  # total = $0.50
    'CBDC':   [0.05, 0.05, 0.05, 0.15],  # total = $0.30
}

totals = {m: sum(v) for m, v in costs.items()}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Grouped stacked bar ---
x = np.arange(len(methods))
width = 0.6

# Build stacked bars
bottoms = np.zeros(len(methods))
for i, comp in enumerate(components):
    vals = [costs[m][i] for m in methods]
    bars = ax1.bar(x, vals, width, bottom=bottoms, color=colors[i],
                   label=comp, edgecolor='white', linewidth=0.5)
    # Add value labels inside bars if segment is large enough
    for j, v in enumerate(vals):
        if v >= 0.10:
            ax1.text(x[j], bottoms[j] + v / 2, f'${v:.2f}',
                     ha='center', va='center', fontsize=9, fontweight='bold',
                     color='black' if colors[i] != MLBLUE else 'white')
    bottoms += vals

# Add total labels on top
for j, m in enumerate(methods):
    ax1.text(x[j], totals[m] + 0.02, f'${totals[m]:.2f}',
             ha='center', va='bottom', fontsize=11, fontweight='bold',
             color=MLPURPLE)

ax1.set_xlabel('Payment Method', fontweight='bold')
ax1.set_ylabel('Transaction Cost per \\$100 (\\$)', fontweight='bold')
ax1.set_title('(a) Transaction Cost Components\nby Payment Method', fontweight='bold', color=MLPURPLE)
ax1.set_xticks(x)
ax1.set_xticklabels(methods)
ax1.legend(loc='upper right', framealpha=0.9)
ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
ax1.set_ylim(0, 1.25)

# --- Panel (b): Percentage reduction vs cash ---
cash_total = totals['Cash']
reductions = {m: (1 - totals[m] / cash_total) * 100 for m in methods}

bar_colors = [MLRED, MLORANGE, MLBLUE, MLGREEN]
bars = ax2.bar(x, [reductions[m] for m in methods], width,
               color=bar_colors, edgecolor='white', linewidth=0.5, alpha=0.85)

# Add percentage labels
for j, m in enumerate(methods):
    pct = reductions[m]
    ax2.text(x[j], pct + 1.5, f'{pct:.0f}%',
             ha='center', va='bottom', fontsize=12, fontweight='bold',
             color=MLPURPLE)

# Component-level reduction annotations for Crypto and CBDC
for j, m in enumerate(['Crypto', 'CBDC']):
    idx = methods.index(m)
    comp_reductions = []
    for i, comp in enumerate(components):
        if costs['Cash'][i] > 0:
            comp_reductions.append(
                f'{comp}: {(1 - costs[m][i] / costs["Cash"][i]) * 100:.0f}%')
        else:
            comp_reductions.append(f'{comp}: N/A')
    detail = '\n'.join(comp_reductions)
    y_pos = reductions[m] - 15
    ax2.text(x[idx], y_pos, detail, ha='center', va='top',
             fontsize=8, bbox=dict(boxstyle='round,pad=0.3',
                                   facecolor='white', edgecolor='gray',
                                   alpha=0.8))

ax2.set_xlabel('Payment Method', fontweight='bold')
ax2.set_ylabel('Cost Reduction vs Cash (%)', fontweight='bold')
ax2.set_title('(b) Cost Reduction Relative\nto Cash Baseline', fontweight='bold', color=MLPURPLE)
ax2.set_xticks(x)
ax2.set_xticklabels(methods)
ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
ax2.set_ylim(0, 85)

fig.suptitle('Transaction Cost Economics of Digital Finance\n'
             '$TC_{total} = TC_{search} + TC_{verify} + TC_{settle} + TC_{comply}$'
             ' -- Coase (1937), Williamson (1985)',
             fontweight='bold', fontsize=14, color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
