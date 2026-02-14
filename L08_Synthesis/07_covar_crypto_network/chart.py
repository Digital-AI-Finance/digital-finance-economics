r"""CoVaR Crypto Systemic Risk Network
# Multi-panel override: comparative statics requires simultaneous visibility

$\Delta CoVaR^{j|i}$. BTC->ETH=0.25, USDT->all=0.35.
Based on Adrian & Brunnermeier (2016).

Economic Model:
Conditional Value-at-Risk measures systemic spillovers:
$CoVaR_q^{j|i} = VaR_q^{j} \;\big|\; R^i = VaR_q^{i}$
$\Delta CoVaR^{j|i} = CoVaR_q^{j|i} - VaR_q^{j}$
Positive delta indicates institution $i$ amplifies tail risk at institution $j$.

Citation: Adrian & Brunnermeier (2016) - CoVaR, American Economic Review
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

# ── Node definitions ──
nodes = {
    'BTC':  {'pos': (0.2, 0.7),  'color': MLORANGE, 'size': 0.09},
    'ETH':  {'pos': (0.8, 0.7),  'color': MLPURPLE, 'size': 0.08},
    'USDT': {'pos': (0.2, 0.3),  'color': MLGREEN,  'size': 0.07},
    'USDC': {'pos': (0.8, 0.3),  'color': MLBLUE,   'size': 0.065},
    'BNB':  {'pos': (0.5, 0.5),  'color': MLRED,    'size': 0.06},
    'DeFi': {'pos': (0.5, 0.1),  'color': MLLAVENDER, 'size': 0.06},
}

# ── Delta-CoVaR edges (source -> target : delta_covar) ──
edges = [
    ('BTC',  'ETH',  0.25),
    ('BTC',  'BNB',  0.20),
    ('BTC',  'DeFi', 0.15),
    ('ETH',  'BTC',  0.18),
    ('ETH',  'DeFi', 0.22),
    ('USDT', 'BTC',  0.35),
    ('USDT', 'ETH',  0.35),
    ('USDT', 'BNB',  0.30),
    ('USDT', 'DeFi', 0.35),
    ('USDC', 'DeFi', 0.30),
    ('USDC', 'ETH',  0.20),
    ('BNB',  'ETH',  0.12),
]

# ── Panel (a): Network diagram ──
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Draw edges as curved arrows with width proportional to delta-CoVaR
for src, tgt, delta in edges:
    src_pos = np.array(nodes[src]['pos'])
    tgt_pos = np.array(nodes[tgt]['pos'])
    # Offset start/end to node boundary
    direction = tgt_pos - src_pos
    dist = np.linalg.norm(direction)
    unit = direction / dist
    start = src_pos + unit * (nodes[src]['size'] + 0.01)
    end = tgt_pos - unit * (nodes[tgt]['size'] + 0.01)

    lw = 0.5 + delta * 8
    alpha = 0.3 + delta * 0.7
    color = MLRED if delta >= 0.30 else (MLORANGE if delta >= 0.20 else '#888888')

    ax1.annotate('', xy=end, xytext=start,
                 arrowprops=dict(arrowstyle='->', lw=lw, color=color,
                                 alpha=alpha, connectionstyle='arc3,rad=0.15'))

# Draw nodes
for name, info in nodes.items():
    circle = plt.Circle(info['pos'], info['size'], facecolor=info['color'],
                        edgecolor='black', linewidth=1.5, zorder=5, alpha=0.85)
    ax1.add_patch(circle)
    ax1.text(info['pos'][0], info['pos'][1], name,
             ha='center', va='center', fontsize=9,
             fontweight='bold', color='white', zorder=6)

# Legend for edge severity
legend_els = [
    plt.Line2D([0], [0], color=MLRED, lw=3, label='High (>=0.30)'),
    plt.Line2D([0], [0], color=MLORANGE, lw=2, label='Medium (0.20-0.29)'),
    plt.Line2D([0], [0], color='#888888', lw=1, label='Low (<0.20)'),
]
ax1.legend(handles=legend_els, loc='upper right', fontsize=8,
           title='Edge severity', title_fontsize=9, framealpha=0.9)

ax1.set_xlim(0, 1)
ax1.set_ylim(-0.05, 0.95)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title(r'(a) $\Delta$CoVaR Network', fontsize=12, fontweight='bold')
ax1.text(0.5, -0.02, r'Arrow width $\propto$ $\Delta CoVaR^{j|i}$',
         ha='center', fontsize=9, style='italic', transform=ax1.transAxes)

# ── Panel (b): Horizontal bar ranking of systemic importance ──
# Compute average outgoing delta-CoVaR for each source
outgoing = {name: [] for name in nodes}
for src, tgt, delta in edges:
    outgoing[src].append(delta)
avg_delta = {name: np.mean(vals) if vals else 0 for name, vals in outgoing.items()}

# Sort by avg delta descending
sorted_names = sorted(avg_delta.keys(), key=lambda x: avg_delta[x])
y_positions = np.arange(len(sorted_names))
bar_values = [avg_delta[n] for n in sorted_names]
bar_colors = [nodes[n]['color'] for n in sorted_names]

ax2.barh(y_positions, bar_values, color=bar_colors, edgecolor='black',
         linewidth=0.8, alpha=0.85, height=0.6)
ax2.set_yticks(y_positions)
ax2.set_yticklabels(sorted_names, fontsize=10, fontweight='bold')
ax2.set_xlabel(r'Mean outgoing $\Delta$CoVaR', fontsize=11)
ax2.set_title(r'(b) Systemic importance ranking', fontsize=12, fontweight='bold')
ax2.grid(axis='x', alpha=0.3, linestyle='--')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Annotate bars with values
for i, (name, val) in enumerate(zip(sorted_names, bar_values)):
    ax2.text(val + 0.005, i, f'{val:.2f}', va='center', fontsize=9, fontweight='bold')

# Highlight USDT
usdt_idx = sorted_names.index('USDT')
ax2.annotate('Highest systemic\nspillover risk',
             xy=(avg_delta['USDT'], usdt_idx),
             xytext=(avg_delta['USDT'] - 0.08, usdt_idx - 1.5),
             fontsize=9, fontweight='bold', color=MLRED,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLRED, alpha=0.9))

fig.suptitle(r'$\Delta CoVaR^{j|i}$: Crypto Systemic Risk Spillovers',
             fontsize=14, fontweight='bold', y=1.01)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
