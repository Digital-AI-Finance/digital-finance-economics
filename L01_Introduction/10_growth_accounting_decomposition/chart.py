r"""Digital Finance Growth Decomposition: Solow-Style Accounting

Multi-panel override: comparative statics requires simultaneous visibility

Panel (a): Stacked area chart of growth factor contributions over time.
Panel (b): Dominant growth driver by era (bar chart).

Economic Model:
$g_{total} = g_{tech} + g_{adopt} + g_{network} + g_{reg}$.
Based on Solow (1957).
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

# Time period: 2010-2030
years = np.arange(2010, 2031)
t = years - 2010  # 0..20

# Growth contributions (percentage points of total growth)
# Technology: 60% early -> 20% late
g_tech = 60 - 2.0 * t
g_tech = np.clip(g_tech, 20, 60)

# Adoption: 20% -> peaks 40% around 2020, then stabilizes
g_adopt = 20 + 25 * np.exp(-0.5 * ((t - 10) / 4)**2)

# Network: 10% -> 30% (grows steadily)
g_network = 10 + 1.0 * t
g_network = np.clip(g_network, 10, 30)

# Regulation: 10% -> 20% (gradual increase)
g_reg = 10 + 0.5 * t
g_reg = np.clip(g_reg, 10, 20)

# Normalize to 100% each year
total_raw = g_tech + g_adopt + g_network + g_reg
g_tech_n = g_tech / total_raw * 100
g_adopt_n = g_adopt / total_raw * 100
g_network_n = g_network / total_raw * 100
g_reg_n = g_reg / total_raw * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Stacked area ---
ax1.stackplot(years, g_tech_n, g_adopt_n, g_network_n, g_reg_n,
              labels=['Technology', 'Adoption', 'Network Effects', 'Regulation'],
              colors=[MLBLUE, MLGREEN, MLORANGE, MLLAVENDER],
              alpha=0.85)

# Era annotations
ax1.axvline(2015, color='gray', linestyle=':', alpha=0.5)
ax1.axvline(2020, color='gray', linestyle=':', alpha=0.5)
ax1.axvline(2025, color='gray', linestyle=':', alpha=0.5)
ax1.text(2012.5, 95, 'Tech Era', ha='center', fontsize=9, fontweight='bold',
         color='white',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=MLBLUE, alpha=0.7))
ax1.text(2017.5, 95, 'Adoption Era', ha='center', fontsize=9, fontweight='bold',
         color='white',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=MLGREEN, alpha=0.7))
ax1.text(2022.5, 95, 'Network Era', ha='center', fontsize=9, fontweight='bold',
         color='white',
         bbox=dict(boxstyle='round,pad=0.3', facecolor=MLORANGE, alpha=0.7))
ax1.text(2027.5, 95, 'Regulation Era', ha='center', fontsize=9, fontweight='bold',
         color=MLPURPLE,
         bbox=dict(boxstyle='round,pad=0.3', facecolor=MLLAVENDER, alpha=0.7))

ax1.set_xlabel('Year', fontweight='bold')
ax1.set_ylabel('Share of Total Growth (%)', fontweight='bold')
ax1.set_title('(a) Growth Factor Contributions\nOver Time', fontweight='bold', color=MLPURPLE)
ax1.legend(loc='center left', framealpha=0.9, fontsize=10)
ax1.grid(True, alpha=0.3, linestyle='--', axis='y')
ax1.set_xlim(2010, 2030)
ax1.set_ylim(0, 105)

# --- Panel (b): Dominant driver by era ---
eras = ['2010-2014\n(Early)', '2015-2019\n(Growth)', '2020-2024\n(Maturity)',
        '2025-2030\n(Regulation)']
era_ranges = [(0, 5), (5, 10), (10, 15), (15, 21)]

# Average contribution per era
era_data = {'Technology': [], 'Adoption': [], 'Network Effects': [], 'Regulation': []}
for start, end in era_ranges:
    era_data['Technology'].append(np.mean(g_tech_n[start:end]))
    era_data['Adoption'].append(np.mean(g_adopt_n[start:end]))
    era_data['Network Effects'].append(np.mean(g_network_n[start:end]))
    era_data['Regulation'].append(np.mean(g_reg_n[start:end]))

x = np.arange(len(eras))
width = 0.2
era_colors = [MLBLUE, MLGREEN, MLORANGE, MLLAVENDER]
era_labels = ['Technology', 'Adoption', 'Network Effects', 'Regulation']

for i, (label, color) in enumerate(zip(era_labels, era_colors)):
    vals = era_data[label]
    bars = ax2.bar(x + (i - 1.5) * width, vals, width, color=color,
                   label=label, edgecolor='white', linewidth=0.5)

# Mark dominant driver per era
for j, era in enumerate(eras):
    max_val = 0
    max_label = ''
    for label in era_labels:
        if era_data[label][j] > max_val:
            max_val = era_data[label][j]
            max_label = label
    ax2.annotate(f'{max_label}\ndominant',
                 xy=(j, max_val + 1), xytext=(j, max_val + 6),
                 fontsize=8, ha='center', fontweight='bold', color=MLPURPLE,
                 arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1))

ax2.set_xlabel('Era', fontweight='bold')
ax2.set_ylabel('Average Share of Growth (%)', fontweight='bold')
ax2.set_title('(b) Dominant Growth Driver\nby Era', fontweight='bold', color=MLPURPLE)
ax2.set_xticks(x)
ax2.set_xticklabels(eras, fontsize=9)
ax2.legend(loc='upper right', framealpha=0.9, fontsize=9)
ax2.grid(True, alpha=0.3, linestyle='--', axis='y')

fig.suptitle('Digital Finance Growth Accounting: Solow-Style Decomposition\n'
             r'$g_{total} = g_{tech} + g_{adopt} + g_{network} + g_{reg}$'
             ' -- Solow (1957)',
             fontweight='bold', fontsize=14, color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
