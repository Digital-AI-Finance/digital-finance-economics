r"""Multi-Criteria Policy Evaluation with Stakeholder Weights
# Multi-panel override: comparative statics requires simultaneous visibility

MCDA. 6 instruments x 5 objectives. Based on MCDA framework.

Economic Model:
Multi-Criteria Decision Analysis (MCDA):
$W_i = \sum_{j=1}^{m} w_j \cdot s_{ij}$
where $W_i$ is the weighted score for policy $i$, $w_j$ is the weight for
objective $j$, and $s_{ij}$ is the raw score of policy $i$ on objective $j$.
Three stakeholder profiles: regulator, industry, consumer.

Citation: Belton & Stewart (2002) - Multiple Criteria Decision Analysis
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 11, 'axes.titlesize': 13,
    'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 9,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# ── 6 policy instruments x 5 objectives ──
instruments = ['CBDC', 'Stablecoin\nRegulation', 'DeFi\nRules',
               'Crypto\nTaxation', 'KYC/AML', 'Sandbox']
objectives = ['Inclusion', 'Stability', 'Innovation', 'Consumer\nProtection', 'Efficiency']

# Score matrix: instruments (rows) x objectives (cols), scale 0-10
scores = np.array([
    [8, 7, 4, 6, 7],   # CBDC
    [3, 9, 3, 8, 5],   # Stablecoin Regulation
    [2, 6, 2, 7, 4],   # DeFi Rules
    [4, 5, 3, 4, 6],   # Crypto Taxation
    [2, 8, 2, 9, 3],   # KYC/AML
    [6, 4, 9, 5, 7],   # Sandbox
])

# ── 3 weight profiles ──
weight_profiles = {
    'Regulator': np.array([0.15, 0.30, 0.10, 0.30, 0.15]),
    'Industry':  np.array([0.20, 0.10, 0.35, 0.15, 0.20]),
    'Consumer':  np.array([0.25, 0.15, 0.15, 0.30, 0.15]),
}
profile_colors = {'Regulator': MLPURPLE, 'Industry': MLORANGE, 'Consumer': MLBLUE}

# ── Compute weighted totals: W_i = sum(w_j * s_ij) ──
weighted_totals = {}
for profile_name, weights in weight_profiles.items():
    weighted_totals[profile_name] = scores @ weights  # (6,5) @ (5,) = (6,)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6),
                                gridspec_kw={'width_ratios': [1.2, 1]})

# ── Panel (a): Heatmap ──
im = ax1.imshow(scores, cmap='YlGnBu', aspect='auto', vmin=0, vmax=10)

ax1.set_xticks(np.arange(len(objectives)))
ax1.set_yticks(np.arange(len(instruments)))
ax1.set_xticklabels(objectives, fontsize=9)
ax1.set_yticklabels(instruments, fontsize=9)

# Annotate cells
for i in range(len(instruments)):
    for j in range(len(objectives)):
        val = scores[i, j]
        text_color = 'white' if val >= 7 else 'black'
        ax1.text(j, i, f'{val}', ha='center', va='center',
                 fontsize=10, fontweight='bold', color=text_color)

cbar = plt.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)
cbar.set_label('Score (0=low, 10=high)', fontsize=9)

ax1.set_title('(a) Policy effectiveness heatmap', fontsize=12, fontweight='bold')
ax1.set_xlabel('Objectives', fontsize=10)
ax1.set_ylabel('Policy instruments', fontsize=10)

# ── Panel (b): Grouped bar chart of weighted totals ──
n_instruments = len(instruments)
n_profiles = len(weight_profiles)
bar_width = 0.22
x = np.arange(n_instruments)

for k, (profile_name, totals) in enumerate(weighted_totals.items()):
    offset = (k - (n_profiles - 1) / 2) * bar_width
    bars = ax2.bar(x + offset, totals, bar_width, label=profile_name,
                   color=profile_colors[profile_name], edgecolor='black',
                   linewidth=0.6, alpha=0.85)
    # Value labels on bars
    for bar, val in zip(bars, totals):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 f'{val:.1f}', ha='center', va='bottom', fontsize=7,
                 fontweight='bold', color=profile_colors[profile_name])

ax2.set_xticks(x)
ax2.set_xticklabels([inst.replace('\n', ' ') for inst in instruments],
                     fontsize=8, rotation=30, ha='right')
ax2.set_ylabel(r'Weighted total $W_i = \sum w_j \cdot s_{ij}$', fontsize=10)
ax2.set_title('(b) MCDA weighted scores by stakeholder', fontsize=12, fontweight='bold')
ax2.legend(fontsize=9, framealpha=0.9, title='Stakeholder', title_fontsize=9)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_ylim(0, 8.5)

# Annotate best instrument per profile
for profile_name, totals in weighted_totals.items():
    best_idx = np.argmax(totals)
    best_val = totals[best_idx]
    best_name = instruments[best_idx].replace('\n', ' ')
    # Small annotation at top of chart
    ax2.annotate(f'{profile_name}: {best_name}',
                 xy=(best_idx, best_val + 0.3),
                 fontsize=7, fontweight='bold',
                 color=profile_colors[profile_name], ha='center')

fig.suptitle(r'Multi-Criteria Decision Analysis: $W_i = \sum_{j} w_j \cdot s_{ij}$',
             fontsize=14, fontweight='bold', y=1.01)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
