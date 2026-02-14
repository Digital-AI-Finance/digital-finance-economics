r"""Cross-Border Settlement Efficiency: Correspondent Banking vs Multi-CBDC

Two-panel comparison of settlement costs and efficiency metrics.

Economic Model:
    Settlement cost: $C_{corr} = f_{orig} + f_{corr} + \Delta_{FX} + f_{recv}$.
    CBDC alternative: $C_{CBDC} = f_{CB} + \Delta_{FX,CBDC}$
    where $f_{CB} \ll f_{corr}$ and $\Delta_{FX,CBDC} \ll \Delta_{FX}$.

    Based on BIS (2022) and mBridge pilot data.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Multi-panel override: comparative statics requires simultaneous visibility

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10,
    'figure.figsize': (14, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ============================================================
# Panel (a): Efficiency Comparison -- Grouped Bars
# ============================================================

metrics = ['Cost\n(% of transfer)', 'Time\n(normalized 0-10)', 'Counterparty\nRisk (1-10)']
corr_values = [6.0, 10.0, 8.0]   # Correspondent banking
cbdc_values = [1.0, 0.02, 2.0]   # Multi-CBDC
improvements = ['-83%', '-99.8%', '-75%']

x = np.arange(len(metrics))
bar_width = 0.32

bars_corr = ax1.bar(x - bar_width / 2, corr_values, bar_width,
                     label='Correspondent Banking', color=MLBLUE,
                     edgecolor='white', linewidth=0.8, zorder=3)
bars_cbdc = ax1.bar(x + bar_width / 2, cbdc_values, bar_width,
                     label='Multi-CBDC (mBridge)', color=MLPURPLE,
                     edgecolor='white', linewidth=0.8, zorder=3)

# Percentage improvement labels above each pair
for i, (cv, bv, imp) in enumerate(zip(corr_values, cbdc_values, improvements)):
    y_top = max(cv, bv) + 0.6
    ax1.annotate(imp, xy=(x[i], y_top), ha='center', va='bottom',
                 fontsize=12, fontweight='bold', color=MLGREEN,
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#e8f5e9',
                           edgecolor=MLGREEN, alpha=0.9))

# Value labels on bars
for bar in bars_corr:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.15,
             f'{h:.1f}', ha='center', va='bottom', fontsize=9,
             fontweight='bold', color=MLBLUE)

for bar in bars_cbdc:
    h = bar.get_height()
    label = f'{h:.2f}' if h < 0.1 else f'{h:.1f}'
    ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.15,
             label, ha='center', va='bottom', fontsize=9,
             fontweight='bold', color=MLPURPLE)

ax1.set_xticks(x)
ax1.set_xticklabels(metrics)
ax1.set_ylabel('Score', fontweight='bold')
ax1.set_title('(a) Efficiency Comparison', fontweight='bold', pad=12)
ax1.set_ylim(0, 13)
ax1.legend(loc='upper right', framealpha=0.95)
ax1.grid(axis='y', alpha=0.3, linestyle='--', zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# ============================================================
# Panel (b): Cost Waterfall -- $10,000 transfer
# ============================================================

# Correspondent banking cost components (cumulative waterfall)
corr_labels = ['Originating\nBank', 'Correspondent\nBank', 'FX\nMarkup', 'Receiving\nBank', 'TOTAL']
corr_amounts = [25, 250, 200, 125]  # individual components
corr_total = sum(corr_amounts)      # 600

# CBDC cost components
cbdc_labels_short = ['CB\nProcessing', 'FX Atomic\nSwap', 'Receiving\nFee', 'TOTAL']
cbdc_amounts = [10, 50, 40]         # individual components
cbdc_total = sum(cbdc_amounts)      # 100

# --- Draw correspondent banking waterfall (left-side bars) ---
x_pos = np.arange(len(corr_labels))
bar_w = 0.35

# Compute cumulative bottoms for waterfall
corr_bottoms = [0]
for i in range(1, len(corr_amounts)):
    corr_bottoms.append(corr_bottoms[-1] + corr_amounts[i - 1])

# Draw stacking bars for correspondent
for i, (amt, bot) in enumerate(zip(corr_amounts, corr_bottoms)):
    color = MLRED if corr_labels[i].startswith('FX') else MLBLUE
    ax2.bar(x_pos[i] - bar_w / 2, amt, bar_w, bottom=bot,
            color=color, edgecolor='white', linewidth=0.8, zorder=3)
    ax2.text(x_pos[i] - bar_w / 2, bot + amt / 2,
             f'${amt}', ha='center', va='center', fontsize=9,
             fontweight='bold', color='white')
    # Connect with thin line to next bar
    if i < len(corr_amounts) - 1:
        top = bot + amt
        ax2.plot([x_pos[i] - bar_w / 2 + bar_w / 2, x_pos[i + 1] - bar_w],
                 [top, top], color='grey', linewidth=0.8, linestyle='--',
                 alpha=0.6, zorder=2)

# Total bar for correspondent
ax2.bar(x_pos[4] - bar_w / 2, corr_total, bar_w, bottom=0,
        color=MLBLUE, edgecolor='black', linewidth=1.2, zorder=3,
        alpha=0.85)
ax2.text(x_pos[4] - bar_w / 2, corr_total / 2,
         f'${corr_total}', ha='center', va='center', fontsize=10,
         fontweight='bold', color='white')

# --- Draw CBDC waterfall (right-side bars, same x positions 0-3 mapped to 0-2 + total) ---
# Map CBDC bars to positions 0, 2, 3 (skip position 1 which is correspondent-only)
cbdc_x_map = [0, 2, 3]  # CB Processing at 0, FX at 2, Receiving at 3

cbdc_bottoms = [0]
for i in range(1, len(cbdc_amounts)):
    cbdc_bottoms.append(cbdc_bottoms[-1] + cbdc_amounts[i - 1])

for i, (amt, bot) in enumerate(zip(cbdc_amounts, cbdc_bottoms)):
    ax2.bar(x_pos[cbdc_x_map[i]] + bar_w / 2, amt, bar_w, bottom=bot,
            color=MLPURPLE, edgecolor='white', linewidth=0.8, zorder=3,
            alpha=0.85)
    ax2.text(x_pos[cbdc_x_map[i]] + bar_w / 2, bot + amt / 2,
             f'${amt}', ha='center', va='center', fontsize=9,
             fontweight='bold', color='white')
    # Connect lines
    if i < len(cbdc_amounts) - 1:
        top = bot + amt
        next_x = x_pos[cbdc_x_map[i + 1]] + bar_w / 2
        curr_x = x_pos[cbdc_x_map[i]] + bar_w / 2
        ax2.plot([curr_x + bar_w / 2 - bar_w / 2, next_x],
                 [top, top], color=MLPURPLE, linewidth=0.8, linestyle='--',
                 alpha=0.4, zorder=2)

# Total bar for CBDC
ax2.bar(x_pos[4] + bar_w / 2, cbdc_total, bar_w, bottom=0,
        color=MLPURPLE, edgecolor='black', linewidth=1.2, zorder=3,
        alpha=0.85)
ax2.text(x_pos[4] + bar_w / 2, cbdc_total / 2,
         f'${cbdc_total}', ha='center', va='center', fontsize=10,
         fontweight='bold', color='white')

# "No correspondent" marker at position 1 for CBDC
ax2.text(x_pos[1] + bar_w / 2, 15, 'Eliminated',
         ha='center', va='bottom', fontsize=8, fontstyle='italic',
         color=MLPURPLE, alpha=0.7)

# Savings annotation between the two total bars
mid_x = x_pos[4]
savings = corr_total - cbdc_total
ax2.annotate('', xy=(mid_x + bar_w / 2, cbdc_total + 5),
             xytext=(mid_x - bar_w / 2, corr_total - 5),
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=2.5,
                             connectionstyle='arc3,rad=-0.2'))
ax2.annotate(f'Savings:\n${savings} ({savings/corr_total*100:.0f}%)',
             xy=(mid_x + 0.55, corr_total * 0.55),
             fontsize=11, fontweight='bold', color=MLGREEN,
             ha='left', va='center',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#e8f5e9',
                       edgecolor=MLGREEN, alpha=0.95))

ax2.set_xticks(x_pos)
ax2.set_xticklabels(corr_labels, fontsize=9)
ax2.set_ylabel('Cumulative Cost ($)', fontweight='bold')
ax2.set_title('(b) Cost Waterfall: $10,000 Transfer', fontweight='bold', pad=12)
ax2.set_ylim(0, 750)
ax2.grid(axis='y', alpha=0.3, linestyle='--', zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Legends for panel (b)
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=MLBLUE, edgecolor='white', label='Correspondent Banking'),
    Patch(facecolor=MLPURPLE, edgecolor='white', label='Multi-CBDC'),
    Patch(facecolor=MLRED, edgecolor='white', label='FX Markup'),
    Patch(facecolor=MLGREEN, edgecolor='white', label='Savings'),
]
ax2.legend(handles=legend_elements, loc='upper left', framealpha=0.95,
           fontsize=9)

# Source annotation
fig.text(0.5, 0.01, 'Data: BIS (2022), mBridge pilot',
         ha='center', va='bottom', fontsize=9, fontstyle='italic',
         color='grey')

plt.tight_layout(rect=[0, 0.03, 1, 1])

out_dir = Path(__file__).parent
plt.savefig(out_dir / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(out_dir / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
