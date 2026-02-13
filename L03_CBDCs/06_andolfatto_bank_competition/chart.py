r"""Andolfatto Bank Competition Model: CBDC as Competitive Constraint

Three-panel comparative statics of deposit market equilibrium
before and after CBDC introduction sets a floor on deposit rates.

Economic Model:
$\Pi_B = (r_L - r_D) \cdot D(r_D)$ where $D(r_D) = a + b \cdot r_D$,
$a = 5.4$ (EUR trillions), $b = 200$ (EUR trillions per unit rate), $r_L = 0.035$.
FOC: $r_D^* = \frac{r_L - a/b}{2} = 0.004$ (0.4\%).
CBDC floor: $r_D \geq r_{CBDC} = 0.01$ (1\%).
Pre-CBDC: $D = 6.2$T, $\Pi = 192.2$B.
Post-CBDC: $D = 7.4$T, $\Pi = 185.0$B.
Based on Andolfatto (2021).
"""
# Multi-panel override: comparative statics requires simultaneous visibility

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10,
    'figure.figsize': (15, 5), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# ── Parameters ──────────────────────────────────────────────────────────
a = 5.4        # EUR trillions: deposits at zero rate
b = 200.0      # EUR trillions per unit rate (sensitivity)
r_L = 0.035    # Lending rate (3.5%)
r_CBDC = 0.01  # CBDC floor rate (1.0%)

# ── Derived equilibrium values ──────────────────────────────────────────
# Monopoly FOC: r_D* = (r_L - a/b) / 2
r_D_star = (r_L - a / b) / 2                    # 0.004 (0.4%)
D_star = a + b * r_D_star                        # 6.2T
Pi_star = (r_L - r_D_star) * D_star              # 0.1922T = 192.2B

# Post-CBDC constrained equilibrium
r_D_cbdc = r_CBDC                                # 0.01 (1.0%)
D_cbdc = a + b * r_D_cbdc                        # 7.4T
Pi_cbdc = (r_L - r_D_cbdc) * D_cbdc              # 0.185T = 185.0B

# Competitive benchmark (r_D = r_L)
D_comp = a + b * r_L                             # 12.4T

# Inverse supply: r_S(D) = (D - a) / b  (for D >= a; 0 for D < a)

# ── Welfare computation ─────────────────────────────────────────────────
# CS = integral_0^D [r_D - max(0, (q-a)/b)] dq
#    = r_D * a + r_D*(D-a) - (D-a)^2 / (2b)    (for D >= a)
def compute_CS(r_D, D_eq):
    return r_D * a + r_D * (D_eq - a) - (D_eq - a)**2 / (2 * b)

# Total surplus at competitive equilibrium
TS = r_L * a + r_L * (D_comp - a) - (D_comp - a)**2 / (2 * b)  # 0.3115T

CS_pre = compute_CS(r_D_star, D_star)            # 0.0232T = 23.2B
CS_post = compute_CS(r_D_cbdc, D_cbdc)           # 0.064T  = 64.0B

DWL_pre = TS - CS_pre - Pi_star                  # 0.0961T = 96.1B
DWL_post = TS - CS_post - Pi_cbdc                # 0.0625T = 62.5B

# Convert to billions for bar chart
CS_pre_B, CS_post_B = CS_pre * 1000, CS_post * 1000
Pi_star_B, Pi_cbdc_B = Pi_star * 1000, Pi_cbdc * 1000
DWL_pre_B, DWL_post_B = DWL_pre * 1000, DWL_post * 1000

# ── Figure ──────────────────────────────────────────────────────────────
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# ════════════════════════════════════════════════════════════════════════
# Panel (a): Deposit Market
# ════════════════════════════════════════════════════════════════════════
r_range = np.linspace(0, 0.04, 300)
D_supply = a + b * r_range                       # Linear deposit supply

ax1.plot(D_supply, r_range * 100, color=MLPURPLE, linewidth=2.5,
         label=r'$D(r_D) = a + b \cdot r_D$')

# Horizontal "demand" at r_L (bank values deposits at lending rate)
ax1.axhline(r_L * 100, color='gray', linewidth=1, linestyle=':', alpha=0.5)
ax1.text(12.8, r_L * 100 + 0.08, r'$r_L = 3.5\%$', fontsize=9, color='gray',
         ha='right', va='bottom')

# CBDC floor
ax1.axhline(r_CBDC * 100, color=MLORANGE, linewidth=2, linestyle='--',
            label=f'CBDC floor $r_{{CBDC}}$ = {r_CBDC*100:.1f}%')

# Pre-CBDC monopoly equilibrium
ax1.plot(D_star, r_D_star * 100, marker='*', markersize=14, color=MLPURPLE,
         zorder=5, label=f'Pre-CBDC: $r_D^*$={r_D_star*100:.1f}%, D={D_star:.1f}T')
ax1.annotate(f'Monopoly\n$r_D^*$={r_D_star*100:.1f}%, D={D_star:.1f}T',
             xy=(D_star, r_D_star * 100),
             xytext=(D_star + 2.0, r_D_star * 100 + 0.6),
             fontsize=9, color=MLPURPLE, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.3))

# Post-CBDC constrained equilibrium
ax1.plot(D_cbdc, r_D_cbdc * 100, marker='D', markersize=10, color=MLGREEN,
         zorder=5, label=f'Post-CBDC: $r_D$={r_D_cbdc*100:.1f}%, D={D_cbdc:.1f}T')
ax1.annotate(f'Post-CBDC\n$r_D$={r_D_cbdc*100:.1f}%, D={D_cbdc:.1f}T',
             xy=(D_cbdc, r_D_cbdc * 100),
             xytext=(D_cbdc + 1.8, r_D_cbdc * 100 + 0.8),
             fontsize=9, color=MLGREEN, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.3))

# Shade CS area (pre-CBDC): area between r_D* horizontal and supply curve
D_fill_pre = np.linspace(a, D_star, 100)
r_supply_pre = (D_fill_pre - a) / b * 100
ax1.fill_between(D_fill_pre, r_supply_pre, r_D_star * 100,
                 alpha=0.12, color=MLPURPLE, label='CS (pre-CBDC)')
# Also rectangular CS block from 0 to a at height r_D*
ax1.fill_between([a - 0.05, a], [0, 0], [r_D_star * 100, r_D_star * 100],
                 alpha=0.08, color=MLPURPLE)

# Shade CS area (post-CBDC)
D_fill_post = np.linspace(a, D_cbdc, 100)
r_supply_post = (D_fill_post - a) / b * 100
ax1.fill_between(D_fill_post, r_supply_post, r_D_cbdc * 100,
                 alpha=0.12, color=MLGREEN)

# Shade DWL (pre-CBDC): triangle between D* and D_comp above supply
D_fill_dwl = np.linspace(D_star, D_comp, 100)
r_supply_dwl = (D_fill_dwl - a) / b * 100
r_L_line = np.full_like(D_fill_dwl, r_L * 100)
ax1.fill_between(D_fill_dwl, r_supply_dwl, r_L_line,
                 alpha=0.10, color=MLRED, hatch='///', label='DWL (pre-CBDC)')

ax1.set_xlabel('Deposits (EUR trillions)', fontweight='bold')
ax1.set_ylabel('Deposit Rate $r_D$ (%)', fontweight='bold')
ax1.set_title('(a) Deposit Market', fontsize=13, fontweight='bold', color=MLPURPLE)
ax1.set_xlim(4.5, 13.5)
ax1.set_ylim(-0.2, 4.2)
ax1.legend(loc='upper left', fontsize=7.5, framealpha=0.9)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.grid(True, alpha=0.2, linestyle='--')

# ════════════════════════════════════════════════════════════════════════
# Panel (b): Bank Profit
# ════════════════════════════════════════════════════════════════════════
r_D_range = np.linspace(0, r_L, 300)
Pi_range = (r_L - r_D_range) * (a + b * r_D_range)  # in trillions
Pi_range_B = Pi_range * 1000                          # convert to billions

ax2.plot(r_D_range * 100, Pi_range_B, color=MLBLUE, linewidth=2.5,
         label=r'$\Pi(r_D) = (r_L - r_D)(a + b \cdot r_D)$')

# CBDC floor vertical line
ax2.axvline(r_CBDC * 100, color=MLORANGE, linewidth=2, linestyle='--',
            label=f'CBDC floor = {r_CBDC*100:.1f}%')

# Mark pre-CBDC optimum (peak)
ax2.plot(r_D_star * 100, Pi_star_B, marker='*', markersize=14, color=MLPURPLE,
         zorder=5, label=f'Pre-CBDC peak: {Pi_star_B:.1f}B')
ax2.annotate(f'$r_D^*$={r_D_star*100:.1f}%\n$\\Pi$={Pi_star_B:.1f}B',
             xy=(r_D_star * 100, Pi_star_B),
             xytext=(r_D_star * 100 + 0.6, Pi_star_B + 3),
             fontsize=9, color=MLPURPLE, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.3))

# Mark post-CBDC constrained point
ax2.plot(r_D_cbdc * 100, Pi_cbdc_B, marker='D', markersize=10, color=MLGREEN,
         zorder=5, label=f'Post-CBDC: {Pi_cbdc_B:.1f}B')
ax2.annotate(f'$r_D$={r_D_cbdc*100:.1f}%\n$\\Pi$={Pi_cbdc_B:.1f}B',
             xy=(r_D_cbdc * 100, Pi_cbdc_B),
             xytext=(r_D_cbdc * 100 + 0.6, Pi_cbdc_B - 12),
             fontsize=9, color=MLGREEN, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.3))

# Shade profit loss region between the two rates
r_fill = np.linspace(r_D_star, r_D_cbdc, 100)
Pi_fill_top = np.full_like(r_fill, Pi_star_B)
Pi_fill_bot = (r_L - r_fill) * (a + b * r_fill) * 1000
ax2.fill_between(r_fill * 100, Pi_fill_bot, Pi_fill_top,
                 alpha=0.15, color=MLRED, label=f'Profit loss: {Pi_star_B - Pi_cbdc_B:.1f}B')

ax2.set_xlabel('Deposit Rate $r_D$ (%)', fontweight='bold')
ax2.set_ylabel('Bank Profit $\\Pi$ (EUR billions)', fontweight='bold')
ax2.set_title('(b) Bank Profit', fontsize=13, fontweight='bold', color=MLPURPLE)
ax2.set_xlim(-0.1, 3.8)
ax2.set_ylim(0, 210)
ax2.legend(loc='upper right', fontsize=7.5, framealpha=0.9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(True, alpha=0.2, linestyle='--')

# ════════════════════════════════════════════════════════════════════════
# Panel (c): Welfare Decomposition (grouped bar chart)
# ════════════════════════════════════════════════════════════════════════
categories = ['Consumer\nSurplus (CS)', 'Producer\nSurplus (PS)', 'Deadweight\nLoss (DWL)',
              'Total\nWelfare']
pre_vals = [CS_pre_B, Pi_star_B, DWL_pre_B, CS_pre_B + Pi_star_B]
post_vals = [CS_post_B, Pi_cbdc_B, DWL_post_B, CS_post_B + Pi_cbdc_B]
bar_colors_pre = [MLPURPLE, MLPURPLE, MLRED, MLPURPLE]
bar_colors_post = [MLGREEN, MLGREEN, MLGREEN, MLGREEN]

x = np.arange(len(categories))
width = 0.35

bars_pre = ax3.bar(x - width/2, pre_vals, width, color=bar_colors_pre,
                   alpha=0.7, edgecolor='white', linewidth=0.5, label='Pre-CBDC')
bars_post = ax3.bar(x + width/2, post_vals, width, color=bar_colors_post,
                    alpha=0.7, edgecolor='white', linewidth=0.5, label='Post-CBDC')

# Value labels on bars
for bar_group in [bars_pre, bars_post]:
    for bar in bar_group:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 2,
                 f'{height:.1f}B', ha='center', va='bottom', fontsize=8,
                 fontweight='bold')

# Change arrows showing direction of welfare change
for i, (pre_v, post_v) in enumerate(zip(pre_vals, post_vals)):
    delta = post_v - pre_v
    sign = '+' if delta > 0 else ''
    color = MLGREEN if delta > 0 else MLRED
    ax3.text(x[i], max(pre_v, post_v) + 16, f'{sign}{delta:.1f}B',
             ha='center', fontsize=8, color=color, fontweight='bold')

ax3.set_xlabel('')
ax3.set_ylabel('EUR billions', fontweight='bold')
ax3.set_title('(c) Welfare Decomposition', fontsize=13, fontweight='bold', color=MLPURPLE)
ax3.set_xticks(x)
ax3.set_xticklabels(categories, fontsize=9)
ax3.set_ylim(0, 280)
ax3.legend(loc='upper left', fontsize=9, framealpha=0.9)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.grid(True, alpha=0.2, linestyle='--', axis='y')

# ── Supertitle and source ──────────────────────────────────────────────
fig.suptitle('Andolfatto (2021): CBDC as Competitive Constraint on Bank Deposit Pricing',
             fontsize=14, fontweight='bold', color=MLPURPLE, y=1.02)
fig.text(0.5, -0.04,
         'Model: $\\Pi_B = (r_L - r_D) \\cdot D(r_D)$, '
         '$D(r_D) = a + b \\cdot r_D$ | '
         f'$a={a}$T, $b={int(b)}$, $r_L={r_L*100:.1f}\\%$, '
         f'$r_{{CBDC}}={r_CBDC*100:.1f}\\%$ | '
         'Based on Andolfatto (2021, JPE)',
         ha='center', fontsize=9, style='italic', color='gray')

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
