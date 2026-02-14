r"""Cross-Border Payment Cost Decomposition

Multi-panel chart comparing cost components and settlement times across
four cross-border payment channels.

# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model: Cross-Border Payment Total Cost
- $TC = TC_{FX} + TC_{comply} + TC_{intermed} + TC_{settle}$
- Four channels: Correspondent banking, SWIFT gpi, Stablecoin, Multi-CBDC

Calibration:
  Correspondent: [2.5, 1.5, 1.5, 0.8] = 6.3%
  SWIFT gpi:     [1.5, 1.0, 0.5, 0.5] = 3.5%
  Stablecoin:    [0.3, 0.5, 0.2, 0.2] = 1.2%
  Multi-CBDC:    [0.1, 0.2, 0.1, 0.1] = 0.5%

Citation: BIS (2020), World Bank Remittance Prices
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# --- Cost data (%) ---
channels = ['Correspondent\nBanking', 'SWIFT gpi', 'Stablecoin', 'Multi-CBDC']
components = ['FX markup', 'Compliance', 'Intermediary', 'Settlement']
comp_colors = [MLORANGE, MLBLUE, MLPURPLE, MLGREEN]

# [FX, Compliance, Intermediary, Settlement]
costs = {
    'Correspondent\nBanking': [2.5, 1.5, 1.5, 0.8],
    'SWIFT gpi':              [1.5, 1.0, 0.5, 0.5],
    'Stablecoin':             [0.3, 0.5, 0.2, 0.2],
    'Multi-CBDC':             [0.1, 0.2, 0.1, 0.1],
}

# Settlement times (in hours)
settlement_times = {
    'Correspondent\nBanking': 72,    # 3 days
    'SWIFT gpi':              24,    # 1 day
    'Stablecoin':             0.5,   # 30 minutes
    'Multi-CBDC':             0.05,  # 3 minutes
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Stacked horizontal bar ---
y_pos = np.arange(len(channels))
bar_height = 0.5

# Draw stacked horizontal bars
lefts = np.zeros(len(channels))
for j, comp in enumerate(components):
    widths = [costs[ch][j] for ch in channels]
    bars = ax1.barh(y_pos, widths, bar_height, left=lefts,
                    label=comp, color=comp_colors[j], alpha=0.85,
                    edgecolor='white', linewidth=1)
    # Add component labels inside bars (if wide enough)
    for i, (w, l) in enumerate(zip(widths, lefts)):
        if w >= 0.4:
            ax1.text(l + w / 2, y_pos[i], f'{w:.1f}%',
                     ha='center', va='center', fontsize=9,
                     color='white', fontweight='bold')
    lefts += widths

# Total cost labels at end of each bar
totals = [sum(costs[ch]) for ch in channels]
for i, (total, ch) in enumerate(zip(totals, channels)):
    ax1.text(total + 0.15, y_pos[i], f'{total:.1f}%',
             ha='left', va='center', fontsize=12, fontweight='bold')

ax1.set_yticks(y_pos)
ax1.set_yticklabels(channels)
ax1.set_xlabel('Total Cost (%)')
ax1.set_title('(a) Cost Decomposition by Channel')
ax1.legend(loc='lower right', fontsize=10, framealpha=0.9)
ax1.set_xlim(0, 8)
ax1.grid(True, alpha=0.2, linestyle='--', axis='x')
ax1.invert_yaxis()  # Best channel at bottom

# G20 target line
ax1.axvline(x=3.0, color=MLRED, linestyle='--', linewidth=1.5, alpha=0.7)
ax1.text(3.1, 3.5, 'G20 target\n(3%)', fontsize=10, color=MLRED, va='top')

# --- Panel (b): Settlement time comparison ---
times = [settlement_times[ch] for ch in channels]
bar_colors = [MLRED, MLORANGE, MLBLUE, MLGREEN]

bars2 = ax2.barh(y_pos, times, bar_height, color=bar_colors, alpha=0.85,
                 edgecolor='white', linewidth=1.5)

# Time labels
time_labels = ['3 days', '1 day', '30 min', '3 min']
for i, (t, label) in enumerate(zip(times, time_labels)):
    x_text = max(t + 1, 3)
    ax2.text(x_text, y_pos[i], label,
             ha='left', va='center', fontsize=12, fontweight='bold')

ax2.set_yticks(y_pos)
ax2.set_yticklabels(channels)
ax2.set_xlabel('Settlement Time (hours)')
ax2.set_title('(b) Settlement Speed Comparison')
ax2.set_xscale('log')
ax2.set_xlim(0.01, 200)
ax2.grid(True, alpha=0.2, linestyle='--', axis='x')
ax2.invert_yaxis()

# Speed improvement annotation
ax2.annotate(f'{72 / 0.05:.0f}x faster',
             xy=(0.05, 3), xytext=(0.3, 2.2),
             fontsize=12, fontweight='bold', color=MLGREEN,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#d4edda', alpha=0.9),
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
