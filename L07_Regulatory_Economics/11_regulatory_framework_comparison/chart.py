"""Regulatory Framework Comparison: Multi-Criteria Decision Analysis

# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
  MCDA: 5 dimensions scored 1-10
  Dimensions: Innovation, Consumer Protection, Market Integrity, Enforcement, Flexibility
  MiCA [7,8,9,7,5], SEC [4,7,5,9,4], MAS [9,6,7,6,7], None [10,1,1,1,10]

  Weighted totals for stakeholder profiles:
  - Startup: w = [0.35, 0.10, 0.10, 0.10, 0.35]
  - Consumer: w = [0.10, 0.35, 0.25, 0.20, 0.10]
  - Regulator: w = [0.10, 0.20, 0.30, 0.30, 0.10]

  Based on FSB (2023) - Crypto-Asset Policy Implementation Framework.

Citation: FSB (2023) - High-level Recommendations for the Regulation of Crypto-Assets
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (14, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# --- Framework scores (5 dimensions, 1-10) ---
dimensions = ['Innovation', 'Consumer\nProtection', 'Market\nIntegrity', 'Enforcement', 'Flexibility']
n_dims = len(dimensions)

frameworks = {
    'MiCA (EU)': np.array([7, 8, 9, 7, 5]),
    'SEC (US)': np.array([4, 7, 5, 9, 4]),
    'MAS (Singapore)': np.array([9, 6, 7, 6, 7]),
    'No Regulation': np.array([10, 1, 1, 1, 10]),
}

framework_colors = {
    'MiCA (EU)': MLBLUE,
    'SEC (US)': MLRED,
    'MAS (Singapore)': MLGREEN,
    'No Regulation': MLLAVENDER,
}

# Stakeholder weight profiles
stakeholders = {
    'Startup': np.array([0.35, 0.10, 0.10, 0.10, 0.35]),
    'Consumer': np.array([0.10, 0.35, 0.25, 0.20, 0.10]),
    'Regulator': np.array([0.10, 0.20, 0.30, 0.30, 0.10]),
}

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), subplot_kw={})

# Panel (a): Radar chart
# Need polar axes for radar
ax1.remove()
ax1 = fig.add_subplot(121, polar=True)

angles = np.linspace(0, 2 * np.pi, n_dims, endpoint=False).tolist()
angles += angles[:1]  # Close the polygon

for name, scores in frameworks.items():
    values = scores.tolist()
    values += values[:1]
    ax1.plot(angles, values, 'o-', linewidth=2, label=name, color=framework_colors[name], ms=6)
    ax1.fill(angles, values, alpha=0.08, color=framework_colors[name])

ax1.set_xticks(angles[:-1])
ax1.set_xticklabels(dimensions, fontsize=10)
ax1.set_ylim(0, 10)
ax1.set_yticks([2, 4, 6, 8, 10])
ax1.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8)
ax1.set_title('(a) Framework Comparison (Radar)', fontsize=14, pad=20)
ax1.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15), fontsize=9)
ax1.grid(True, alpha=0.3)

# Panel (b): Weighted totals for stakeholder profiles
ax2.remove()
ax2 = fig.add_subplot(122)

x_pos = np.arange(len(stakeholders))
width = 0.18
offsets = np.arange(len(frameworks)) - (len(frameworks) - 1) / 2

for i, (fw_name, scores) in enumerate(frameworks.items()):
    weighted_scores = []
    for s_name, weights in stakeholders.items():
        weighted_scores.append(np.dot(scores, weights))

    bars = ax2.bar(x_pos + offsets[i] * width, weighted_scores, width,
                   label=fw_name, color=framework_colors[fw_name], alpha=0.8,
                   edgecolor='black', lw=1)

    # Value labels
    for bar, val in zip(bars, weighted_scores):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 f'{val:.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

ax2.set_xlabel('Stakeholder profile')
ax2.set_ylabel('Weighted score (higher = better)')
ax2.set_title('(b) Framework Scores by Stakeholder Perspective')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(list(stakeholders.keys()), fontsize=11)
ax2.set_ylim(0, 10)
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3, axis='y')

# Winner annotations
for j, (s_name, weights) in enumerate(stakeholders.items()):
    scores_all = {fw: np.dot(sc, weights) for fw, sc in frameworks.items()}
    winner = max(scores_all, key=scores_all.get)
    winner_score = scores_all[winner]
    # Small annotation below group
    ax2.text(x_pos[j], -0.6, f'Best: {winner}',
             ha='center', fontsize=8, color=framework_colors[winner], fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                       edgecolor=framework_colors[winner], alpha=0.8))

# Insight
ax2.text(0.02, 0.97, 'Weights matter:\n'
         'Startups prefer MAS/None\n'
         'Consumers prefer MiCA\n'
         'Regulators prefer MiCA/SEC',
         transform=ax2.transAxes, fontsize=9,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor=MLORANGE, alpha=0.9))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
