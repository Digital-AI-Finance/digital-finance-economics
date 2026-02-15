"""Platform HHI Evolution: Market Concentration Across Industries

Multi-panel chart showing HHI trends for blockchain L1s vs traditional tech platforms.

Economic Model:
  $HHI = \sum s_i^2$. L1 HHI: 2015=0.65, 2024=0.35. Based on DOJ/FTC guidelines.
  HHI ranges: < 0.15 (competitive), 0.15-0.25 (moderate), > 0.25 (concentrated).
  Reference benchmarks: Search=0.92, Social=0.70, Ride-hailing=0.60.

# Multi-panel override: comparative statics requires simultaneous visibility

Citation: DOJ/FTC Horizontal Merger Guidelines; DeFiLlama data for L1 market shares
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): L1 blockchain HHI evolution ---
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
# L1 HHI: Bitcoin dominance was very high in 2015, declined as ETH, SOL, etc. emerged
l1_hhi = [0.65, 0.62, 0.45, 0.55, 0.52, 0.48, 0.40, 0.42, 0.38, 0.35]

# DEX HHI (Uniswap dominance declining)
dex_hhi = [None, None, None, 0.95, 0.90, 0.85, 0.55, 0.50, 0.45, 0.40]
dex_years = [y for y, h in zip(years, dex_hhi) if h is not None]
dex_vals = [h for h in dex_hhi if h is not None]

# CEX HHI (Binance dominance)
cex_hhi = [0.30, 0.28, 0.25, 0.35, 0.40, 0.45, 0.50, 0.55, 0.50, 0.45]

ax1.plot(years, l1_hhi, 'o-', color=MLBLUE, linewidth=2.5, markersize=8, label='L1 Blockchains')
ax1.plot(dex_years, dex_vals, 's-', color=MLGREEN, linewidth=2.5, markersize=8, label='DEX Market')
ax1.plot(years, cex_hhi, '^-', color=MLORANGE, linewidth=2.5, markersize=8, label='CEX Market')

# HHI threshold bands
ax1.axhspan(0.25, 1.0, alpha=0.08, color=MLRED, zorder=0)
ax1.axhspan(0.15, 0.25, alpha=0.08, color=MLORANGE, zorder=0)
ax1.axhspan(0, 0.15, alpha=0.08, color=MLGREEN, zorder=0)

ax1.axhline(y=0.25, color=MLRED, linestyle='--', alpha=0.4, linewidth=1)
ax1.text(2015.2, 0.26, 'Highly concentrated', fontsize=8, color=MLRED, alpha=0.8)
ax1.axhline(y=0.15, color=MLORANGE, linestyle='--', alpha=0.4, linewidth=1)
ax1.text(2015.2, 0.155, 'Moderately concentrated', fontsize=8, color=MLORANGE, alpha=0.8)

# Key events
ax1.annotate('ICO boom\n(ETH rises)', xy=(2017, 0.45),
             xytext=(2017.5, 0.58), fontsize=8, color=MLBLUE,
             arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1),
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

ax1.annotate('Alt-L1\nseason', xy=(2021, 0.40),
             xytext=(2020, 0.30), fontsize=8, color=MLBLUE,
             arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1),
             bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

ax1.set_xlabel('Year')
ax1.set_ylabel('HHI')
ax1.set_title('(a) Blockchain Market Concentration Over Time')
ax1.legend(loc='upper right', fontsize=9, framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(2014.5, 2024.5)
ax1.set_ylim(0, 1.0)

# --- Panel (b): Cross-industry HHI comparison (2024) ---
industries = ['Web\nSearch', 'Social\nMedia', 'Ride-\nhailing', 'L1\nBlockchain',
              'DEX', 'CEX', 'Cloud\nCompute', 'Streaming']
hhi_values = [0.92, 0.70, 0.60, 0.35, 0.40, 0.45, 0.45, 0.35]
bar_colors = []
for h in hhi_values:
    if h > 0.25:
        bar_colors.append(MLRED)
    elif h > 0.15:
        bar_colors.append(MLORANGE)
    else:
        bar_colors.append(MLGREEN)

bars = ax2.bar(industries, hhi_values, color=bar_colors, alpha=0.8,
               edgecolor='black', linewidth=0.8)

# Value labels on bars
for bar, val in zip(bars, hhi_values):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
             f'{val:.2f}', ha='center', fontsize=10, fontweight='bold')

# Threshold lines
ax2.axhline(y=0.25, color=MLRED, linestyle='--', alpha=0.5, linewidth=1.5)
ax2.axhline(y=0.15, color=MLORANGE, linestyle='--', alpha=0.5, linewidth=1.5)

# Legend for colors
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=MLRED, alpha=0.8, edgecolor='black', label='Highly concentrated (>0.25)'),
    Patch(facecolor=MLORANGE, alpha=0.8, edgecolor='black', label='Moderately concentrated (0.15-0.25)'),
    Patch(facecolor=MLGREEN, alpha=0.8, edgecolor='black', label='Competitive (<0.15)'),
]
ax2.legend(handles=legend_elements, loc='upper right', fontsize=8, framealpha=0.95)

# Key insight
ax2.text(0.02, 0.95,
         'Crypto markets are LESS\nconcentrated than Big Tech\n'
         'Web Search: Google ~95%\n'
         'L1 Blockchain: ETH ~55%\n'
         '(more competitors)',
         transform=ax2.transAxes, fontsize=9, va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                   edgecolor=MLORANGE, alpha=0.9))

ax2.set_ylabel('HHI (2024 est.)')
ax2.set_title('(b) Cross-Industry Concentration Comparison')
ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
ax2.set_ylim(0, 1.1)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
