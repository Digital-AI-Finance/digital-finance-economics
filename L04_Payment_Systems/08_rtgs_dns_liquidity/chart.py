r"""RTGS vs DNS Liquidity Comparison

Multi-panel chart comparing liquidity requirements under RTGS, DNS, and
hybrid settlement systems as a function of the number of participating banks.

# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model: Settlement System Liquidity
- $L_{RTGS} = \sum |P_{ij}|$ (gross liquidity = sum of all bilateral payments)
- $L_{DNS} = \sum |Net_i|$ (net liquidity = sum of net positions after netting)
- Netting ratio: $NR = 1 - L_{DNS}/L_{RTGS} = 0.7 + 0.05\ln(N)$
- Hybrid: $L_{Hybrid} = 0.5 \cdot (L_{RTGS} + L_{DNS})$ (partial netting with RTGS finality)

Calibration: N = [5, 10, 20, 50, 100]. Average bilateral flow = 1B USD.

Citation: Kahn & Roberds (2009), BIS (2005)
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

# --- Model parameters ---
N_banks = np.array([5, 10, 20, 50, 100])
avg_bilateral = 1.0  # 1 billion USD average bilateral flow

# Dense grid for smooth curves
N_dense = np.linspace(5, 100, 200)


def rtgs_liquidity(N, avg_flow):
    """RTGS: total gross liquidity = N*(N-1) bilateral pairs * avg flow."""
    return N * (N - 1) * avg_flow


def netting_ratio(N):
    """NR = 0.7 + 0.05 * ln(N). Logarithmic improvement with more banks."""
    return 0.7 + 0.05 * np.log(N)


def dns_liquidity(N, avg_flow):
    """DNS liquidity = RTGS * (1 - NR)."""
    nr = netting_ratio(N)
    return rtgs_liquidity(N, avg_flow) * (1 - nr)


def hybrid_liquidity(N, avg_flow):
    """Hybrid: partial netting achieves ~60-70% of full netting benefit."""
    return 0.5 * (rtgs_liquidity(N, avg_flow) + dns_liquidity(N, avg_flow))


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Liquidity vs N ---
L_rtgs = rtgs_liquidity(N_dense, avg_bilateral)
L_dns = dns_liquidity(N_dense, avg_bilateral)
L_hybrid = hybrid_liquidity(N_dense, avg_bilateral)

ax1.plot(N_dense, L_rtgs, color=MLRED, linewidth=2.5, label='RTGS (gross)')
ax1.plot(N_dense, L_hybrid, color=MLORANGE, linewidth=2.5, linestyle='--',
         label='Hybrid (partial netting)')
ax1.plot(N_dense, L_dns, color=MLGREEN, linewidth=2.5, label='DNS (net)')

# Mark specific N values
for N in N_banks:
    ax1.plot(N, rtgs_liquidity(N, avg_bilateral), 'o', color=MLRED,
             markersize=7, zorder=5)
    ax1.plot(N, dns_liquidity(N, avg_bilateral), 's', color=MLGREEN,
             markersize=7, zorder=5)

# Shade savings region
ax1.fill_between(N_dense, L_dns, L_rtgs, alpha=0.1, color=MLBLUE,
                 label='Liquidity savings')

# Annotate savings at N=50
N_ann = 50
savings_pct = netting_ratio(N_ann) * 100
ax1.annotate(f'{savings_pct:.0f}% liquidity\nsavings at N={N_ann}',
             xy=(N_ann, (rtgs_liquidity(N_ann, avg_bilateral) +
                         dns_liquidity(N_ann, avg_bilateral)) / 2),
             xytext=(60, 4000),
             fontsize=11,
             bbox=dict(boxstyle='round,pad=0.4', facecolor=MLLAVENDER, alpha=0.9),
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5))

ax1.set_xlabel('Number of Banks (N)')
ax1.set_ylabel('Liquidity Required ($ billions)')
ax1.set_title('(a) Liquidity: RTGS vs DNS vs Hybrid')
ax1.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax1.grid(True, alpha=0.2, linestyle='--')

# --- Panel (b): Netting ratio vs N ---
NR_dense = netting_ratio(N_dense)
NR_points = netting_ratio(N_banks)

ax2.plot(N_dense, NR_dense * 100, color=MLPURPLE, linewidth=2.5)
ax2.plot(N_banks, NR_points * 100, 'o', color=MLPURPLE, markersize=9, zorder=5)

# Label each point
for N, nr in zip(N_banks, NR_points):
    ax2.annotate(f'NR={nr:.1%}',
                 xy=(N, nr * 100), xytext=(10, 10),
                 textcoords='offset points', fontsize=10,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor=MLLAVENDER, alpha=0.8))

# Reference line at worked example NR=0.82 (N=10)
nr_10 = netting_ratio(10)
ax2.axhline(y=nr_10 * 100, color=MLORANGE, linestyle=':', linewidth=1.5, alpha=0.7)
ax2.text(80, nr_10 * 100 + 0.5, f'Worked example: NR(10)={nr_10:.2f}',
         fontsize=10, color=MLORANGE, ha='center')

ax2.set_xlabel('Number of Banks (N)')
ax2.set_ylabel('Netting Ratio (%)')
ax2.set_title('(b) Netting Efficiency vs Number of Banks')
ax2.set_ylim(75, 95)
ax2.grid(True, alpha=0.2, linestyle='--')

# Theory note
ax2.text(0.5, 0.05, r'$NR = 0.7 + 0.05\,\ln(N)$',
         transform=ax2.transAxes, fontsize=12, ha='center',
         bbox=dict(boxstyle='round,pad=0.4', facecolor=MLLAVENDER, alpha=0.9,
                   edgecolor=MLPURPLE))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
