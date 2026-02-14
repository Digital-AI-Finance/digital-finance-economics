r"""Brunnermeier-Niepelt Equivalence: Balance Sheet Mechanics & Parameter Space

Two-panel figure showing (a) T-account balance sheet transformation when CBDC
is introduced with pass-through central bank funding, and (b) the parameter
space where the equivalence result holds vs. breaks down.

Economic Model:
    Equivalence holds when: Eq(D, 0) = Eq(D-x, x) for CBDC amount x.
    Requires: pass-through funding at rate r_CB = r_D, no bank runs,
              no friction differences.
    Brunnermeier & Niepelt (2019), JME 106.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10,
    'figure.figsize': (12, 7), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Multi-panel override: comparative statics requires simultaneous visibility
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ---------------------------------------------------------------------------
# Panel (a): Balance Sheet Mechanics -- T-account diagram
# ---------------------------------------------------------------------------

ax1.set_xlim(-0.5, 10.5)
ax1.set_ylim(-0.3, 10.5)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('(a) Balance Sheet Mechanics', fontsize=13,
              fontweight='bold', color=MLPURPLE, pad=12)

# Helper: draw a labeled rectangle
def draw_rect(ax, x, y, w, h, color, label, fontsize=9, text_color='white'):
    rect = plt.Rectangle((x, y), w, h, linewidth=1.2, edgecolor='black',
                          facecolor=color, alpha=0.85, zorder=2)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, label, ha='center', va='center',
            fontsize=fontsize, fontweight='bold', color=text_color, zorder=3)

# Dimensions
col_w = 2.5   # column width
gap = 0.25    # gap between asset/liability columns
hdr_h = 0.35  # header row height
left_x = 0.0  # left edge of T-accounts

# ---- PRE-CBDC T-account (top half) ----
top_y = 5.8   # baseline for top T-account
top_h = 2.4   # total height of asset/liability blocks

# Header bar
ax1.text(left_x + col_w + gap / 2, top_y + top_h + hdr_h + 0.2,
         'Pre-CBDC Bank Balance Sheet',
         ha='center', va='bottom', fontsize=10, fontweight='bold', color='#333333')

# Assets header
draw_rect(ax1, left_x, top_y + top_h, col_w, hdr_h, '#555555', 'Assets', fontsize=9)
# Liabilities header
draw_rect(ax1, left_x + col_w + gap, top_y + top_h, col_w, hdr_h, '#555555',
          'Liabilities', fontsize=9)

# Assets: Loans 100B
draw_rect(ax1, left_x, top_y, col_w, top_h, MLORANGE, 'Loans\n100B', fontsize=10)
# Liabilities: Deposits 100B
draw_rect(ax1, left_x + col_w + gap, top_y, col_w, top_h, MLBLUE,
          'Deposits\n100B', fontsize=10)

# ---- POST-CBDC T-account (bottom half) ----
bot_y = 0.5
total_h = 2.4          # same total height as pre-CBDC
dep_h = total_h * 0.70  # 70B deposits
cb_h = total_h * 0.30   # 30B CB funding

ax1.text(left_x + col_w + gap / 2, bot_y + total_h + hdr_h + 0.2,
         'Post-CBDC Bank Balance Sheet',
         ha='center', va='bottom', fontsize=10, fontweight='bold', color='#333333')

# Asset/liability headers
draw_rect(ax1, left_x, bot_y + total_h, col_w, hdr_h, '#555555',
          'Assets', fontsize=9)
draw_rect(ax1, left_x + col_w + gap, bot_y + total_h, col_w, hdr_h,
          '#555555', 'Liabilities', fontsize=9)

# Assets: Loans 100B (unchanged)
draw_rect(ax1, left_x, bot_y, col_w, total_h, MLORANGE,
          'Loans\n100B', fontsize=10)

# Liabilities: Deposits 70B (bottom) + CB Funding 30B (top)
draw_rect(ax1, left_x + col_w + gap, bot_y, col_w, dep_h, MLBLUE,
          'Deposits\n70B', fontsize=10)
draw_rect(ax1, left_x + col_w + gap, bot_y + dep_h, col_w, cb_h, MLGREEN,
          'CB Funding 30B', fontsize=8)

# ---- Separate CBDC holdings block (far right) ----
cbdc_x = 7.2
cbdc_y = bot_y + 0.2
cbdc_h = 1.6
cbdc_w = 2.8

ax1.text(cbdc_x + cbdc_w / 2, cbdc_y + cbdc_h + hdr_h + 0.2,
         'Public Holdings', ha='center', va='bottom',
         fontsize=10, fontweight='bold', color='#333333')
draw_rect(ax1, cbdc_x, cbdc_y + cbdc_h, cbdc_w, hdr_h, '#555555',
          'CBDC', fontsize=9)
draw_rect(ax1, cbdc_x, cbdc_y, cbdc_w, cbdc_h, MLPURPLE,
          'CBDC Holdings\n30B', fontsize=10)

# ---- Arrows showing flows between pre- and post-CBDC ----

# Arrow 1: Deposits -> CBDC (30B flows from deposits down to CBDC block)
# Starts from right edge of pre-CBDC liabilities, curves right to CBDC block top
arrow1 = FancyArrowPatch(
    posA=(left_x + 2 * col_w + gap, top_y + 0.5),
    posB=(cbdc_x + cbdc_w / 2, cbdc_y + cbdc_h + hdr_h + 0.4),
    connectionstyle='arc3,rad=0.3',
    arrowstyle='->', mutation_scale=18,
    color=MLRED, linewidth=2.2, zorder=4
)
ax1.add_patch(arrow1)
ax1.text(7.2, 5.8, 'Deposit\nflight\n30B', fontsize=8.5,
         ha='center', va='center', color=MLRED, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=MLRED, alpha=0.9),
         zorder=5)

# Arrow 2: CB pass-through funding back to bank (30B)
# From left side of CBDC block, curves down-left to CB Funding block
arrow2 = FancyArrowPatch(
    posA=(cbdc_x, cbdc_y + cbdc_h * 0.3),
    posB=(left_x + 2 * col_w + gap, bot_y + dep_h + cb_h * 0.5),
    connectionstyle='arc3,rad=-0.35',
    arrowstyle='->', mutation_scale=18,
    color=MLGREEN, linewidth=2.2, zorder=4
)
ax1.add_patch(arrow2)
ax1.text(6.5, 0.3, 'CB pass-through\nfunding 30B', fontsize=8.5,
         ha='center', va='center', color=MLGREEN, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.2', fc='white', ec=MLGREEN, alpha=0.9),
         zorder=5)

# Equivalence annotation at top
ax1.text(5.0, 10.2,
         'Equivalence: bank balance sheet unchanged\n'
         r'if CB lends back at $r_{CB} = r_D$',
         ha='center', va='top', fontsize=9.5, style='italic', color='#444444',
         bbox=dict(boxstyle='round,pad=0.4', fc='#F5F5DC', ec='gray', alpha=0.7))

# ---------------------------------------------------------------------------
# Panel (b): Equivalence Parameter Space
# ---------------------------------------------------------------------------

# Grid
friction = np.linspace(0, 0.05, 300)   # funding friction (x-axis)
run_prob = np.linspace(0, 0.30, 300)   # run probability (y-axis)
F, R = np.meshgrid(friction, run_prob)

# Welfare loss function: increases with both friction and run probability.
# Equivalence holds when welfare loss < threshold.
# Model: W(f, p) = f * 200 + p * 50 + f * p * 5000
# Equivalence threshold: W < 3.0
W = F * 200 + R * 50 + F * R * 5000

threshold = 3.0

# Binary equivalence mask
equiv_mask = (W < threshold).astype(float)

# Green/red regions via contourf
levels_binary = [-0.5, 0.5, 1.5]
cmap_binary = plt.matplotlib.colors.ListedColormap([MLRED, MLGREEN])
ax2.contourf(F, R, equiv_mask, levels=levels_binary, cmap=cmap_binary, alpha=0.30)

# Contour lines for welfare loss
contour_levels = [1.0, 2.0, 3.0, 5.0, 8.0, 12.0]
cs = ax2.contour(F, R, W, levels=contour_levels, colors='#444444',
                 linewidths=1.0, linestyles='--', alpha=0.6)
ax2.clabel(cs, inline=True, fontsize=8, fmt='W=%.0f')

# Equivalence boundary (thick)
ax2.contour(F, R, W, levels=[threshold], colors='black',
            linewidths=2.5, linestyles='-')

# Mark real-world economies
economies = [
    {'name': 'EU',      'f': 0.010, 'p': 0.05, 'color': MLBLUE},
    {'name': 'China',   'f': 0.020, 'p': 0.03, 'color': MLORANGE},
    {'name': 'Bahamas', 'f': 0.005, 'p': 0.01, 'color': MLPURPLE},
]
# Per-economy annotation offsets to avoid collision
offsets = {
    'EU':      (0.002, 0.012),
    'China':   (0.002, 0.012),
    'Bahamas': (-0.003, 0.015),
}
for econ in economies:
    ax2.scatter(econ['f'], econ['p'], s=110, color=econ['color'],
                edgecolors='black', linewidths=1.2, zorder=5)
    ox, oy = offsets[econ['name']]
    ax2.annotate(econ['name'],
                 xy=(econ['f'], econ['p']),
                 xytext=(econ['f'] + ox, econ['p'] + oy),
                 fontsize=10, fontweight='bold', color=econ['color'],
                 arrowprops=dict(arrowstyle='-', color=econ['color'],
                                 lw=1.0),
                 zorder=6)

# Region labels
ax2.text(0.005, 0.045, 'Equivalence\nholds', fontsize=11, fontweight='bold',
         color=MLGREEN, ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=MLGREEN, alpha=0.8))
ax2.text(0.038, 0.22, 'Equivalence\nbreaks', fontsize=11, fontweight='bold',
         color=MLRED, ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=MLRED, alpha=0.8))

# Axes formatting
ax2.set_xlabel('Funding Friction (cost spread)', fontweight='bold')
ax2.set_ylabel('Run Probability', fontweight='bold')
ax2.set_title('(b) Equivalence Parameter Space', fontsize=13,
              fontweight='bold', color=MLPURPLE, pad=12)
ax2.set_xlim(0, 0.05)
ax2.set_ylim(0, 0.30)

# Format tick labels as percentages
ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.1%}'))
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f'{v:.0%}'))

# Remove top/right spines on panel (b)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

ax2.grid(True, alpha=0.2, linestyle='--')

# Legend for panel (b)
legend_elements = [
    mpatches.Patch(facecolor=MLGREEN, alpha=0.3, edgecolor=MLGREEN,
                   label='Equivalence holds (W < 3)'),
    mpatches.Patch(facecolor=MLRED, alpha=0.3, edgecolor=MLRED,
                   label='Equivalence breaks (W >= 3)'),
    plt.Line2D([0], [0], color='black', linewidth=2.5, label='Boundary'),
]
ax2.legend(handles=legend_elements, loc='upper left', framealpha=0.9,
           fontsize=9)

# Caption
fig.text(0.5, -0.02,
         'Brunnermeier & Niepelt (2019, JME 106): '
         r'Eq(D,0) = Eq(D$-$x, x) requires $r_{CB} = r_D$, '
         'no bank runs, no friction differences.',
         ha='center', fontsize=9, style='italic', color='gray')

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
