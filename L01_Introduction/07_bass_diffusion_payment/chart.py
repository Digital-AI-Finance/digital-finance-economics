r"""Bass Diffusion Model for Payment Technology Adoption

Multi-panel override: comparative statics requires simultaneous visibility

Panel (a): Cumulative adoption S-curves F(t) for cash, cards, digital payments.
Panel (b): Instantaneous adoption rate dF/dt showing peak adoption timing.

Economic Model:
$\frac{dF}{dt} = (p + qF)(1-F)$, $F(t) = \frac{1 - e^{-(p+q)t}}{1 + (q/p)e^{-(p+q)t}}$.
Inflection at $t^* = \frac{\ln(q/p)}{p+q}$.
Based on Bass (1969).
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

def bass_F(t, p, q):
    """Bass cumulative adoption: F(t)"""
    return (1 - np.exp(-(p + q) * t)) / (1 + (q / p) * np.exp(-(p + q) * t))

def bass_dFdt(t, p, q):
    """Bass instantaneous adoption rate: dF/dt"""
    F = bass_F(t, p, q)
    return (p + q * F) * (1 - F)

def bass_inflection(p, q):
    """Time of peak adoption: t* = ln(q/p) / (p+q)"""
    return np.log(q / p) / (p + q)

# Time horizon: 0 to 60 years
t = np.linspace(0, 60, 500)

# Payment technologies with Bass parameters
technologies = [
    ('Cash', 0.01, 0.20, MLRED, '--'),
    ('Cards', 0.02, 0.35, MLORANGE, '-'),
    ('Digital Payments', 0.03, 0.50, MLBLUE, '-'),
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Cumulative S-curves ---
for name, p, q, color, ls in technologies:
    F = bass_F(t, p, q)
    ax1.plot(t, F * 100, color=color, linewidth=2.5, linestyle=ls, label=name)

    # Mark inflection point
    t_star = bass_inflection(p, q)
    F_star = bass_F(t_star, p, q) * 100
    ax1.plot(t_star, F_star, 'o', color=color, markersize=9, zorder=5)
    ax1.annotate(f'$t^*$={t_star:.1f}y',
                 xy=(t_star, F_star), xytext=(t_star + 3, F_star - 12),
                 fontsize=9, fontweight='bold', color=color,
                 arrowprops=dict(arrowstyle='->', color=color, lw=1.2),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                           edgecolor=color, alpha=0.8))

ax1.set_xlabel('Time (years)', fontweight='bold')
ax1.set_ylabel('Cumulative Adoption $F(t)$ (%)', fontweight='bold')
ax1.set_title('(a) Cumulative Adoption S-Curves\nBass Diffusion Model', fontweight='bold', color=MLPURPLE)
ax1.legend(loc='lower right', framealpha=0.9)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(0, 60)
ax1.set_ylim(0, 105)
ax1.axhline(y=50, color='gray', linestyle=':', alpha=0.5, linewidth=1)
ax1.text(58, 52, '50%', fontsize=9, color='gray', ha='right')

# --- Panel (b): Adoption rate dF/dt ---
for name, p, q, color, ls in technologies:
    dFdt = bass_dFdt(t, p, q)
    ax2.plot(t, dFdt * 100, color=color, linewidth=2.5, linestyle=ls, label=name)

    # Mark peak
    t_star = bass_inflection(p, q)
    dF_peak = bass_dFdt(t_star, p, q) * 100
    ax2.plot(t_star, dF_peak, 'o', color=color, markersize=9, zorder=5)

ax2.set_xlabel('Time (years)', fontweight='bold')
ax2.set_ylabel('Adoption Rate $dF/dt$ (% per year)', fontweight='bold')
ax2.set_title('(b) Instantaneous Adoption Rate\nPeak Timing Comparison', fontweight='bold', color=MLPURPLE)
ax2.legend(loc='upper right', framealpha=0.9)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(0, 60)

# Annotate speed comparison
ax2.annotate('Digital peaks\nearlier and higher',
             xy=(bass_inflection(0.03, 0.50), bass_dFdt(bass_inflection(0.03, 0.50), 0.03, 0.50) * 100),
             xytext=(20, 6),
             fontsize=10, fontweight='bold', color=MLBLUE,
             arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                       edgecolor=MLBLUE, alpha=0.9))

fig.suptitle('Bass Diffusion Model: Payment Technology Adoption\n'
             '$dF/dt = (p + qF)(1-F)$ -- Bass (1969), Rogers (1962)',
             fontweight='bold', fontsize=14, color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
