r"""Welfare Surplus Decomposition: Pre- vs Post-CBDC Deposit Market

Two-panel comparative statics of consumer surplus, producer surplus,
and deadweight loss in the deposit market before and after CBDC introduction.

Economic Model:
    Supply of deposits: $D(r_D) = a + b \cdot r_D$ with $a=5.4$T, $b=200$.
    Bank demand: horizontal at $r_L = 0.035$ (lending rate = marginal value of deposits).
    Inverse supply: $r_D(D) = (D - a)/b$.

    CS = depositor surplus = $\frac{1}{2} r_D^* (D^* - a)$ (triangle above supply, below $r_D^*$).
    PS = bank profit = $(r_L - r_D^*) \cdot D^*$.
    DWL = $\frac{1}{2}(r_L - r_D^*)(D_{comp} - D^*)$.

    Using Andolfatto (2021) calibration: $a=5.4$, $b=200$, $r_L=0.035$.
    Pre-CBDC monopoly: $r_D^*=0.004$, $D^*=6.2$T $\Rightarrow$ DWL = 96.1B.
    Post-CBDC ($r_{CBDC}=0.01$ floor): $r_D=0.01$, $D=7.4$T $\Rightarrow$ DWL = 62.5B.
    CBDC reduces DWL by 33.6B.

Citation: Andolfatto (2021) - Assessing the Impact of Central Bank Digital Currency
         on Private Banks.
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

# ── Model parameters ─────────────────────────────────────────────────
a = 5.4       # Autonomous deposits (trillions EUR) at r_D = 0
b = 200.0     # Deposit supply sensitivity (trillions per unit rate)
r_L = 0.035   # Lending rate / bank's marginal value of deposits

# Derived equilibria
D_comp = a + b * r_L          # 12.4T  (competitive: r_D = r_L)
r_mono = 0.004                # Monopoly deposit rate
D_mono = a + b * r_mono       # 6.2T
r_cbdc = 0.01                 # CBDC floor rate
D_cbdc = a + b * r_cbdc       # 7.4T

# Inverse supply function: r_D(D) = (D - a) / b
def inv_supply(D):
    return (D - a) / b

# ── Surplus calculations (in billions) ───────────────────────────────
# Pre-CBDC
CS_pre = 0.5 * r_mono * (D_mono - a) * 1000    # Triangle: 1.6B
PS_pre = (r_L - r_mono) * D_mono * 1000         # Rectangle: 192.2B
DWL_pre = 0.5 * (r_L - r_mono) * (D_comp - D_mono) * 1000  # 96.1B

# Post-CBDC
CS_post = 0.5 * r_cbdc * (D_cbdc - a) * 1000   # 10.0B
PS_post = (r_L - r_cbdc) * D_cbdc * 1000        # 185.0B
DWL_post = 0.5 * (r_L - r_cbdc) * (D_comp - D_cbdc) * 1000  # 62.5B

DWL_reduction = DWL_pre - DWL_post               # 33.6B

# ── Dense D grid for plotting ────────────────────────────────────────
D_grid = np.linspace(a, D_comp + 0.5, 500)
r_supply = inv_supply(D_grid)


def draw_panel(ax, title, r_eq, D_eq, cs_val, ps_val, dwl_val,
               marker='*', marker_label='Monopoly Equilibrium',
               extra_annotations=None):
    """Draw one surplus-decomposition panel."""

    # ── Supply curve ──────────────────────────────────────────────
    ax.plot(D_grid, r_supply, color=MLPURPLE, linewidth=2.5,
            label=r'Supply: $r_D = (D - a)/b$')

    # ── Demand (horizontal at r_L) ───────────────────────────────
    ax.axhline(r_L, color=MLBLUE, linewidth=2, linestyle='--',
               label=f'Bank Demand ($r_L$ = {r_L:.1%})')

    # ── Shading: CS (between r_eq line and supply, from a to D_eq) ──
    D_cs = np.linspace(a, D_eq, 300)
    r_cs_supply = inv_supply(D_cs)
    ax.fill_between(D_cs, r_cs_supply, r_eq, alpha=0.30, color=MLBLUE,
                    label=f'CS (depositor surplus) = {cs_val:.1f}B')

    # ── Shading: PS (rectangle from 0 to D_eq, between r_eq and r_L) ──
    ax.fill_between([a - 0.05, D_eq], r_eq, r_L, alpha=0.25, color=MLORANGE,
                    label=f'PS (bank profit) = {ps_val:.1f}B')
    # Extend PS rectangle visually from D=0 to D_eq for the full deposit base
    # The bank earns spread on ALL D_eq deposits, but geometrically in
    # the (D, r_D) plane the PS rectangle sits between the supply intercept
    # and D_eq.  For visual clarity we shade from just below a to D_eq.

    # ── Shading: DWL (triangle between supply curve and r_L, from D_eq to D_comp) ──
    D_dwl = np.linspace(D_eq, D_comp, 300)
    r_dwl_supply = inv_supply(D_dwl)
    ax.fill_between(D_dwl, r_dwl_supply, r_L, alpha=0.25, color=MLRED,
                    label=f'DWL = {dwl_val:.1f}B')

    # ── Equilibrium marker ────────────────────────────────────────
    ax.plot(D_eq, r_eq, marker=marker, markersize=14, color=MLRED,
            markeredgecolor='black', markeredgewidth=1.5, zorder=5)
    ax.annotate(f'{marker_label}\n$r_D^*$ = {r_eq:.1%}, D = {D_eq:.1f}T',
                xy=(D_eq, r_eq),
                xytext=(D_eq + 1.2, r_eq + 0.006),
                fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='black', lw=1.2),
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                          edgecolor='gray', alpha=0.95))

    # ── Competitive equilibrium reference ─────────────────────────
    ax.plot(D_comp, r_L, 'o', markersize=8, color=MLGREEN,
            markeredgecolor='black', markeredgewidth=1.2, zorder=5)
    ax.annotate(f'Competitive\nD = {D_comp:.1f}T',
                xy=(D_comp, r_L),
                xytext=(D_comp - 1.8, r_L + 0.005),
                fontsize=8, ha='center',
                arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=MLGREEN, alpha=0.9))

    # ── Area value labels (centroid placement) ────────────────────
    # CS label -- place at centroid of CS triangle, but ensure visible
    cs_cx = (a + D_eq) / 2
    cs_cy = max(r_eq * 0.45, 0.003)  # Floor so text stays readable
    ax.text(cs_cx, cs_cy, f'CS\n{cs_val:.1f}B', ha='center', va='center',
            fontsize=9, fontweight='bold', color=MLBLUE)

    # PS label
    ps_cx = (a + D_eq) / 2
    ps_cy = (r_eq + r_L) / 2
    ax.text(ps_cx, ps_cy, f'PS\n{ps_val:.1f}B', ha='center', va='center',
            fontsize=9, fontweight='bold', color=MLORANGE)

    # DWL label
    dwl_cx = (D_eq + D_comp) / 2
    dwl_cy = (r_eq + r_L) / 2
    ax.text(dwl_cx, dwl_cy, f'DWL\n{dwl_val:.1f}B', ha='center', va='center',
            fontsize=9, fontweight='bold', color=MLRED)

    # ── Extra annotations (e.g., CBDC floor) ─────────────────────
    if extra_annotations:
        extra_annotations(ax)

    # ── Formatting ────────────────────────────────────────────────
    ax.set_xlabel('Deposits D (EUR Trillions)', fontweight='bold')
    ax.set_ylabel('Deposit Rate $r_D$', fontweight='bold')
    ax.set_title(title, fontsize=13, fontweight='bold', color=MLPURPLE, pad=10)
    ax.set_xlim(a - 0.5, D_comp + 1.5)
    ax.set_ylim(-0.002, 0.050)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.25, linestyle='--')
    ax.legend(loc='upper left', fontsize=8, framealpha=0.92)

    # Format y-axis as percentage
    from matplotlib.ticker import FuncFormatter
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:.1%}'))


# ── Create figure ─────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))


# ── Panel (a): Pre-CBDC Monopoly ─────────────────────────────────────
draw_panel(ax1,
           '(a) Pre-CBDC Monopoly',
           r_eq=r_mono, D_eq=D_mono,
           cs_val=CS_pre, ps_val=PS_pre, dwl_val=DWL_pre,
           marker='*', marker_label='Monopoly Eq.')


# ── Panel (b): Post-CBDC Competition ─────────────────────────────────
def cbdc_annotations(ax):
    """Add CBDC-specific annotations to post-CBDC panel."""
    # CBDC floor line
    ax.axhline(r_cbdc, color=MLGREEN, linewidth=1.8, linestyle=':',
               label=f'CBDC Floor ($r_{{CBDC}}$ = {r_cbdc:.1%})', zorder=2)

    # DWL reduction annotation -- place below the DWL triangle
    ax.annotate(
        f'DWL reduced by {DWL_reduction:.1f}B ({DWL_reduction/DWL_pre:.0%})',
        xy=(9.5, 0.018),
        xytext=(7.5, 0.003),
        fontsize=9, fontweight='bold', color=MLGREEN,
        arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=2),
        bbox=dict(boxstyle='round,pad=0.4', facecolor='honeydew',
                  edgecolor=MLGREEN, alpha=0.95))


draw_panel(ax2,
           '(b) Post-CBDC Competition',
           r_eq=r_cbdc, D_eq=D_cbdc,
           cs_val=CS_post, ps_val=PS_post, dwl_val=DWL_post,
           marker='D', marker_label='CBDC Eq.',
           extra_annotations=cbdc_annotations)


# ── Suptitle and caption ─────────────────────────────────────────────
fig.suptitle('Welfare Surplus Decomposition: Deposit Market',
             fontsize=15, fontweight='bold', color=MLPURPLE, y=1.02)

fig.text(0.5, -0.04,
         'Model: D(r$_D$) = a + b$\\cdot$r$_D$ | '
         'CS = depositor surplus, PS = (r$_L$ $-$ r$_D$)$\\cdot$D, '
         'DWL = $\\frac{1}{2}$(r$_L$ $-$ r$_D^*$)(D$_{comp}$ $-$ D$^*$)\n'
         'Calibration: a=5.4T, b=200, r$_L$=3.5% | '
         'Andolfatto (2021) -- Assessing the Impact of CBDC on Private Banks',
         ha='center', fontsize=9, style='italic', color='gray')

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
