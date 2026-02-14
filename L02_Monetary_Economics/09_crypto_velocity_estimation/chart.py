r"""Crypto Velocity Estimation
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
    Velocity: $V = \frac{PQ}{M}$.
    USD M2 $V \approx 1.2$, BTC $V \approx 12$, ETH $V \approx 18$, USDT $V \approx 55$.
    Based on Samani (2017), Fisher (1911).

    The equation of exchange $MV = PQ$ implies that for a fixed level of
    economic activity ($PQ$), higher velocity means smaller money supply is needed.
    Crypto assets show dramatically higher velocity than fiat because:
    (1) speculative trading dominates, (2) no reserve requirements create friction.

Citation: Fisher (1911), Samani (2017) - Understanding Token Velocity.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 10,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# --- Parameters ---
assets = ['USD M2', 'BTC', 'ETH', 'USDT']
velocities = [1.2, 12.0, 18.0, 55.0]
std_errors = [0.1, 8.0, 12.0, 20.0]
colors = [MLBLUE, MLORANGE, MLPURPLE, MLGREEN]

# --- Time evolution data (simulated annual estimates 2015-2025) ---
years = np.arange(2015, 2026)
n_years = len(years)

# USD M2 velocity: declining trend (Fed data shows decline from ~1.4 to ~1.1)
v_usd = 1.4 - 0.03 * np.arange(n_years) + np.random.normal(0, 0.02, n_years)
v_usd = np.clip(v_usd, 0.9, 1.5)

# BTC velocity: volatile, mean ~12, peak during 2017/2021 bull markets
btc_base = np.array([6, 8, 18, 10, 7, 8, 22, 14, 10, 9, 12], dtype=float)
btc_noise = np.random.normal(0, 1.5, n_years)
v_btc = btc_base + btc_noise
v_btc = np.clip(v_btc, 3, 30)

# ETH velocity: higher, especially during DeFi summer 2020-2021
eth_base = np.array([0, 5, 12, 15, 10, 25, 35, 22, 16, 14, 18], dtype=float)
eth_noise = np.random.normal(0, 2, n_years)
v_eth = eth_base + eth_noise
v_eth[0] = 0  # ETH launched mid-2015
v_eth = np.clip(v_eth, 0, 45)

# USDT velocity: very high, growing with DeFi
usdt_base = np.array([0, 0, 10, 20, 30, 40, 65, 70, 55, 50, 55], dtype=float)
usdt_noise = np.random.normal(0, 3, n_years)
v_usdt = usdt_base + usdt_noise
v_usdt[:2] = 0  # USDT not significant before 2017
v_usdt = np.clip(v_usdt, 0, 80)

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# === Panel (a): Bar chart with error bars ===
x_pos = np.arange(len(assets))
bars = ax1.bar(x_pos, velocities, yerr=std_errors, capsize=8,
               color=colors, edgecolor='white', linewidth=1.5,
               error_kw={'linewidth': 2, 'capthick': 2, 'ecolor': 'gray'},
               alpha=0.85, width=0.6)

# Value labels on bars
for i, (v, se) in enumerate(zip(velocities, std_errors)):
    ax1.text(i, v + se + 1.5, f'V={v:.1f}', ha='center', fontweight='bold',
             fontsize=11, color=colors[i])
    ax1.text(i, v + se + 5.5, f'(SE={se:.1f})', ha='center', fontsize=8,
             color='gray')

# Annotation for velocity gap
ax1.annotate('', xy=(3, 55), xytext=(0, 55),
            arrowprops=dict(arrowstyle='<->', color=MLRED, lw=2))
ax1.text(1.5, 58, '46x velocity gap', ha='center', fontsize=10,
         fontweight='bold', color=MLRED)

# Fisher equation reference
ax1.text(0.03, 0.97, '$V = PQ/M$\n(Fisher, 1911)',
         transform=ax1.transAxes, fontsize=9,
         verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=MLLAVENDER, alpha=0.3))

ax1.set_xticks(x_pos)
ax1.set_xticklabels(assets, fontweight='bold')
ax1.set_ylabel('Velocity (V = PQ/M)', fontweight='bold')
ax1.set_title('(a) Money Velocity by Asset Class', fontweight='bold', color=MLPURPLE)
ax1.grid(True, alpha=0.3, axis='y')
ax1.set_ylim(0, 85)

# === Panel (b): Time Evolution 2015-2025 ===
ax2.plot(years, v_usd, color=MLBLUE, linewidth=2.5, marker='o', markersize=5,
         label=f'USD M2 (mean={np.mean(v_usd):.1f})')
ax2.plot(years, v_btc, color=MLORANGE, linewidth=2.2, marker='s', markersize=5,
         label=f'BTC (mean={np.mean(v_btc):.1f})')
ax2.plot(years, v_eth, color=MLPURPLE, linewidth=2.2, marker='^', markersize=5,
         label=f'ETH (mean={np.mean(v_eth[v_eth>0]):.1f})')
ax2.plot(years, v_usdt, color=MLGREEN, linewidth=2.2, marker='D', markersize=5,
         label=f'USDT (mean={np.mean(v_usdt[v_usdt>0]):.1f})')

# Highlight bull market periods
ax2.axvspan(2017, 2018, color=MLORANGE, alpha=0.08, label='_nolegend_')
ax2.axvspan(2020.5, 2021.5, color=MLORANGE, alpha=0.08, label='_nolegend_')
ax2.text(2017.5, 72, '2017\nbull', ha='center', fontsize=8, color=MLORANGE, alpha=0.7)
ax2.text(2021, 72, '2021\nbull', ha='center', fontsize=8, color=MLORANGE, alpha=0.7)

# DeFi summer annotation
ax2.annotate('DeFi Summer\n2020', xy=(2020, v_eth[5]), xytext=(2018, 42),
             fontsize=9, fontweight='bold', color=MLPURPLE,
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=MLPURPLE, alpha=0.9))

ax2.set_xlabel('Year', fontweight='bold')
ax2.set_ylabel('Estimated Velocity', fontweight='bold')
ax2.set_title('(b) Velocity Evolution 2015-2025', fontweight='bold', color=MLPURPLE)
ax2.legend(loc='upper left', framealpha=0.9, fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(2015, 2025)
ax2.set_ylim(0, 80)

fig.suptitle('Cryptocurrency Velocity: MV=PQ Applied to Digital Assets',
             fontsize=14, fontweight='bold', color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Crypto velocity estimation chart saved to chart.pdf and chart.png")
