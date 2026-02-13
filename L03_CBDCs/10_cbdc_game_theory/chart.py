r"""International CBDC Competition Game: Payoff Matrix and Best Responses

Two-country strategic interaction over CBDC launch timing.

Economic Model:
    Payoff: $V_i(s_i, s_j) = B_i(s_i) - C_i(s_i) + \gamma \cdot \mathbf{1}[s_i=\text{Launch}, s_j=\text{Wait}]$
    where $\gamma$ = first-mover advantage. Nash equilibrium: (Launch, Launch) when $\gamma > C - B$.
    Prisoner's dilemma structure: dominant strategy is Launch for both players,
    but mutual Wait (4,4) Pareto-dominates mutual Launch (3,3).

Citation: Benigno, Schilling & Uhlig (2022) - Cryptocurrencies, currency competition,
and the impossible trinity.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
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

# ── Payoff matrix data ──────────────────────────────────────────────
# Rows: Country A strategies, Cols: Country B strategies
# Format: (A's payoff, B's payoff)
payoffs = {
    ('Launch', 'Launch'): (3, 3),
    ('Launch', 'Wait'):   (5, 1),
    ('Wait',   'Launch'): (1, 5),
    ('Wait',   'Wait'):   (4, 4),
}

strategies = ['Launch', 'Wait']

# Cell background colors based on joint payoff sum
cell_colors = {
    ('Launch', 'Launch'): '#FFD700',   # yellow-gold  (sum=6, Nash)
    ('Launch', 'Wait'):   '#FFD700',   # yellow-gold  (sum=6, asymmetric)
    ('Wait',   'Launch'): '#FFD700',   # yellow-gold  (sum=6, asymmetric)
    ('Wait',   'Wait'):   '#90EE90',   # light green  (sum=8, cooperative best)
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ═══════════════════════════════════════════════════════════════════
# Panel (a): Payoff Matrix
# ═══════════════════════════════════════════════════════════════════
ax1.set_xlim(-0.6, 2.5)
ax1.set_ylim(-0.6, 2.8)
ax1.set_aspect('equal')
ax1.axis('off')

cell_w, cell_h = 1.0, 0.9

# Origin for the 2x2 grid
ox, oy = 0.4, 0.1

# Draw column headers ("Country B")
ax1.text(ox + cell_w, oy + 2 * cell_h + 0.45, 'Country B',
         fontsize=13, fontweight='bold', ha='center', color=MLBLUE)
for j, s in enumerate(strategies):
    ax1.text(ox + j * cell_w + cell_w / 2, oy + 2 * cell_h + 0.18,
             s, fontsize=12, fontweight='bold', ha='center', va='center',
             color=MLBLUE)

# Draw row headers ("Country A")
ax1.text(ox - 0.42, oy + cell_h, 'Country A',
         fontsize=13, fontweight='bold', ha='center', va='center',
         rotation=90, color=MLRED)
for i, s in enumerate(strategies):
    ax1.text(ox - 0.15, oy + (1 - i) * cell_h + cell_h / 2,
             s, fontsize=12, fontweight='bold', ha='center', va='center',
             color=MLRED)

# Draw cells
for i, row_s in enumerate(strategies):
    for j, col_s in enumerate(strategies):
        x = ox + j * cell_w
        y = oy + (1 - i) * cell_h

        pa, pb = payoffs[(row_s, col_s)]
        bg = cell_colors[(row_s, col_s)]

        # Cell rectangle
        rect = patches.FancyBboxPatch(
            (x + 0.02, y + 0.02), cell_w - 0.04, cell_h - 0.04,
            boxstyle='round,pad=0.03', facecolor=bg, edgecolor='#555555',
            linewidth=1.5, alpha=0.85)
        ax1.add_patch(rect)

        # Payoff text
        ax1.text(x + cell_w / 2, y + cell_h / 2,
                 f'A: {pa},  B: {pb}',
                 fontsize=12, fontweight='bold', ha='center', va='center',
                 color='#222222')

# Highlight Nash equilibrium (Launch, Launch) with thick purple border
nash_x = ox + 0 * cell_w
nash_y = oy + 1 * cell_h
nash_rect = patches.Rectangle(
    (nash_x, nash_y), cell_w, cell_h,
    linewidth=3.5, edgecolor=MLPURPLE, facecolor='none', zorder=10,
    linestyle='-')
ax1.add_patch(nash_rect)
ax1.text(nash_x + cell_w / 2, nash_y + cell_h + 0.02,
         'Nash Equilibrium', fontsize=9, fontweight='bold',
         ha='center', va='bottom', color=MLPURPLE,
         bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                   edgecolor=MLPURPLE, alpha=0.95))

# Highlight cooperative outcome (Wait, Wait) with dashed orange border
coop_x = ox + 1 * cell_w
coop_y = oy + 0 * cell_h
coop_rect = patches.Rectangle(
    (coop_x, coop_y), cell_w, cell_h,
    linewidth=3, edgecolor=MLORANGE, facecolor='none', zorder=10,
    linestyle='--')
ax1.add_patch(coop_rect)
ax1.text(coop_x + cell_w / 2, coop_y - 0.08,
         'Cooperative Outcome', fontsize=9, fontweight='bold',
         ha='center', va='top', color=MLORANGE,
         bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                   edgecolor=MLORANGE, alpha=0.95))

# Panel title
ax1.set_title('(a) Payoff Matrix: Prisoner\'s Dilemma',
              fontsize=13, fontweight='bold', pad=15)

# Legend note
ax1.text(ox + cell_w, oy - 0.48,
         'Dominant strategy: Launch for both\n'
         '(Launch,Launch) = Nash  |  (Wait,Wait) = Pareto superior',
         fontsize=9, ha='center', va='top', style='italic',
         color='#444444',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8F8FF',
                   edgecolor='#CCCCCC', alpha=0.9))


# ═══════════════════════════════════════════════════════════════════
# Panel (b): Best Response / Reaction Functions (grouped bars)
# ═══════════════════════════════════════════════════════════════════

# Data for grouped bars
# When B = Launch: A gets 3 (Launch) or 1 (Wait)
# When B = Wait:   A gets 5 (Launch) or 4 (Wait)
b_strategies = ['B = Launch', 'B = Wait']
a_launch_payoffs = [3, 5]   # A's payoff from Launch given B's choice
a_wait_payoffs   = [1, 4]   # A's payoff from Wait given B's choice

x_pos = np.array([0, 1.2])
bar_w = 0.35

# A = Launch bars
bars_launch = ax2.bar(x_pos - bar_w / 2, a_launch_payoffs, bar_w,
                       color=MLPURPLE, alpha=0.85, edgecolor='black',
                       linewidth=1.2, label='A chooses Launch', zorder=3)

# A = Wait bars
bars_wait = ax2.bar(x_pos + bar_w / 2, a_wait_payoffs, bar_w,
                     color=MLLAVENDER, alpha=0.7, edgecolor='black',
                     linewidth=1.2, label='A chooses Wait', zorder=3)

# Highlight best responses with star markers
for idx in range(2):
    # Launch is always the best response (dominant strategy)
    best_val = a_launch_payoffs[idx]
    ax2.plot(x_pos[idx] - bar_w / 2, best_val + 0.15, '*',
             color=MLRED, markersize=18, zorder=5,
             markeredgecolor='black', markeredgewidth=0.8)

# Value labels on bars
for bar_group, values in [(bars_launch, a_launch_payoffs),
                           (bars_wait, a_wait_payoffs)]:
    for bar, val in zip(bar_group, values):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08,
                 str(val), ha='center', va='bottom', fontsize=12,
                 fontweight='bold', color='#222222')

# Mark Nash equilibrium
ax2.annotate('Nash\nEquilibrium',
             xy=(x_pos[0] - bar_w / 2, a_launch_payoffs[0]),
             xytext=(x_pos[0] - bar_w / 2 - 0.45, a_launch_payoffs[0] + 1.3),
             fontsize=10, fontweight='bold', color=MLPURPLE, ha='center',
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLPURPLE, alpha=0.95))

# Arrow from Nash (3) to Cooperative (4) with annotation
ax2.annotate('',
             xy=(x_pos[1] + bar_w / 2, a_wait_payoffs[1]),
             xytext=(x_pos[0] - bar_w / 2, a_launch_payoffs[0]),
             arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=2.5,
                             linestyle='--', connectionstyle='arc3,rad=0.3'))

ax2.text(0.6, 4.7,
         'Pareto improvement\nrequires coordination',
         fontsize=9, fontweight='bold', ha='center', color=MLORANGE,
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                   edgecolor=MLORANGE, alpha=0.95))

# Dominant strategy annotation
ax2.text(0.6, -0.8,
         'Both countries have dominant strategy: Launch\n'
         r'($\star$ = best response)',
         fontsize=10, ha='center', va='top', style='italic',
         color='#333333',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#F8F8FF',
                   edgecolor='#CCCCCC', alpha=0.9))

# Formatting
ax2.set_xticks(x_pos)
ax2.set_xticklabels(b_strategies, fontsize=12, fontweight='bold')
ax2.set_ylabel("Country A's Payoff", fontweight='bold')
ax2.set_ylim(0, 5.8)
ax2.set_xlim(-0.7, 1.9)
ax2.set_title("(b) Best Responses: Dominant Strategy Analysis",
              fontsize=13, fontweight='bold', pad=15)
ax2.legend(loc='upper left', framealpha=0.95, fontsize=10)
ax2.grid(axis='y', alpha=0.3, linestyle='--', zorder=0)

# Remove top and right spines
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# ═══════════════════════════════════════════════════════════════════
# Save
# ═══════════════════════════════════════════════════════════════════
plt.tight_layout(w_pad=3)

out_dir = Path(__file__).parent
plt.savefig(out_dir / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(out_dir / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
