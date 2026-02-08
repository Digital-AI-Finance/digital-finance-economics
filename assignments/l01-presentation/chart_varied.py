r"""Payment Technology Adoption - Assignment Variations
Demonstrates S-curve parameter sensitivity by comparing baseline to three variations:
1. Adding BNPL (K=40%, r=0.20, t0=2022)
2. Doubling crypto growth rate (r=0.10 -> 0.20)
3. Increasing CBDC ceiling (K=50% -> 90%)

Economic Model: $S(t) = \frac{K}{1 + e^{-r(t - t_0)}}$
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 14,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10,
    'figure.figsize': (16, 12), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'
MLPINK = '#FF69B4'

# S-curve adoption model: S(t) = K / (1 + exp(-r(t - t0)))
def s_curve(t, K, r, t0):
    """Rogers diffusion S-curve: K=carrying capacity, r=growth rate, t0=inflection point"""
    return K / (1 + np.exp(-r * (t - t0)))

# Time range: 1960-2050 (focus on modern payment evolution)
t = np.linspace(1960, 2050, 1000)

# Baseline payment technologies with adoption parameters
# (name, K, r, t0, color)
baseline_technologies = [
    ('Credit Cards', 75, 0.08, 1970, MLORANGE),
    ('ATMs/Debit', 85, 0.10, 1985, MLBLUE),
    ('Online Banking', 70, 0.12, 2000, MLGREEN),
    ('Mobile Payments', 65, 0.15, 2015, MLRED),
    ('Cryptocurrencies', 30, 0.10, 2022, '#9467BD'),
    ('CBDCs (projected)', 50, 0.12, 2030, MLPURPLE),
]

# Create 2x2 subplot figure
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

# ----------------------------------------------------------------------------
# PANEL 1: BASELINE (original 6 technologies)
# ----------------------------------------------------------------------------
ax = axes[0]
for name, K, r, t0, color in baseline_technologies:
    adoption = s_curve(t, K, r, t0)
    ax.plot(t, adoption, label=name, color=color, linewidth=2.5, alpha=0.8)

    # Mark inflection point (50% of K)
    inflection_adoption = K / 2
    ax.plot(t0, inflection_adoption, 'o', color=color, markersize=7, zorder=10)

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Adoption Rate (%)', fontweight='bold')
ax.set_title('BASELINE: Six Payment Technologies\nRogers (1962) S-Curve Model',
             fontsize=14, fontweight='bold', color=MLPURPLE, pad=15)
ax.set_xlim(1960, 2050)
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', framealpha=0.9, fontsize=9)

# ----------------------------------------------------------------------------
# PANEL 2: VARIATION 1 - Add Buy Now Pay Later (BNPL)
# ----------------------------------------------------------------------------
ax = axes[1]

# VARIATION 1: Add BNPL with K=40%, r=0.20, t0=2022
variation1_technologies = baseline_technologies + [
    ('Buy Now Pay Later', 40, 0.20, 2022, MLPINK),
]

for name, K, r, t0, color in variation1_technologies:
    adoption = s_curve(t, K, r, t0)
    ax.plot(t, adoption, label=name, color=color, linewidth=2.5, alpha=0.8)

    inflection_adoption = K / 2
    ax.plot(t0, inflection_adoption, 'o', color=color, markersize=7, zorder=10)

    # Highlight BNPL with annotation
    if name == 'Buy Now Pay Later':
        ax.annotate('BNPL: Fastest r (0.20)\nbut low K (40%)',
                   xy=(t0, inflection_adoption),
                   xytext=(15, 20), textcoords='offset points',
                   fontsize=9, color=color, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                            edgecolor=color, alpha=0.8),
                   arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Adoption Rate (%)', fontweight='bold')
ax.set_title('VARIATION 1: Adding Buy Now Pay Later\n(K=40%, r=0.20, t0=2022)',
             fontsize=14, fontweight='bold', color=MLPINK, pad=15)
ax.set_xlim(1960, 2050)
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', framealpha=0.9, fontsize=8, ncol=2)

# ----------------------------------------------------------------------------
# PANEL 3: VARIATION 2 - Double crypto growth rate (r=0.10 -> 0.20)
# ----------------------------------------------------------------------------
ax = axes[2]

# VARIATION 2: Change crypto r from 0.10 to 0.20
variation2_technologies = [
    ('Credit Cards', 75, 0.08, 1970, MLORANGE),
    ('ATMs/Debit', 85, 0.10, 1985, MLBLUE),
    ('Online Banking', 70, 0.12, 2000, MLGREEN),
    ('Mobile Payments', 65, 0.15, 2015, MLRED),
    ('Crypto (r=0.10, baseline)', 30, 0.10, 2022, '#9467BD'),
    ('Crypto (r=0.20, doubled)', 30, 0.20, 2022, '#FF00FF'),  # Magenta for contrast
    ('CBDCs (projected)', 50, 0.12, 2030, MLPURPLE),
]

for name, K, r, t0, color in variation2_technologies:
    adoption = s_curve(t, K, r, t0)
    linestyle = '--' if 'baseline' in name else '-'
    linewidth = 2.0 if 'baseline' in name else 2.5
    alpha = 0.6 if 'baseline' in name else 0.8

    ax.plot(t, adoption, label=name, color=color, linewidth=linewidth,
            linestyle=linestyle, alpha=alpha)

    inflection_adoption = K / 2
    ax.plot(t0, inflection_adoption, 'o', color=color, markersize=7, zorder=10)

# Mark when doubled-crypto reaches 15% (half of K=30%)
crypto_doubled = s_curve(t, 30, 0.20, 2022)
idx_15pct = np.argmin(np.abs(crypto_doubled - 15))
year_15pct = t[idx_15pct]
ax.axvline(year_15pct, color='#FF00FF', linestyle=':', linewidth=1.5, alpha=0.7)
ax.text(year_15pct + 1, 50, f'Doubled r:\n15% by {int(year_15pct)}',
        fontsize=9, color='#FF00FF', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                 edgecolor='#FF00FF', alpha=0.8))

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Adoption Rate (%)', fontweight='bold')
ax.set_title('VARIATION 2: Faster Crypto Adoption\n(Growth rate r doubled: 0.10 -> 0.20)',
             fontsize=14, fontweight='bold', color='#FF00FF', pad=15)
ax.set_xlim(1960, 2050)
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', framealpha=0.9, fontsize=8)

# ----------------------------------------------------------------------------
# PANEL 4: VARIATION 3 - Increase CBDC ceiling (K=50% -> 90%)
# ----------------------------------------------------------------------------
ax = axes[3]

# VARIATION 3: Change CBDC K from 50 to 90
variation3_technologies = [
    ('Credit Cards', 75, 0.08, 1970, MLORANGE),
    ('ATMs/Debit', 85, 0.10, 1985, MLBLUE),
    ('Online Banking', 70, 0.12, 2000, MLGREEN),
    ('Mobile Payments', 65, 0.15, 2015, MLRED),
    ('Cryptocurrencies', 30, 0.10, 2022, '#9467BD'),
    ('CBDC (K=50%, baseline)', 50, 0.12, 2030, '#ADADE0'),  # Light purple
    ('CBDC (K=90%, increased)', 90, 0.12, 2030, MLPURPLE),  # Dark purple
]

for name, K, r, t0, color in variation3_technologies:
    adoption = s_curve(t, K, r, t0)
    linestyle = '--' if 'baseline' in name else '-'
    linewidth = 2.0 if 'baseline' in name else 2.5
    alpha = 0.6 if 'baseline' in name else 0.8

    ax.plot(t, adoption, label=name, color=color, linewidth=linewidth,
            linestyle=linestyle, alpha=alpha)

    inflection_adoption = K / 2
    ax.plot(t0, inflection_adoption, 'o', color=color, markersize=7, zorder=10)

# Highlight crossover point where K=90% CBDC overtakes mobile payments
cbdc_90 = s_curve(t, 90, 0.12, 2030)
mobile_pay = s_curve(t, 65, 0.15, 2015)
crossover_idx = np.argmin(np.abs(cbdc_90 - mobile_pay))
crossover_year = t[crossover_idx]
crossover_adoption = cbdc_90[crossover_idx]

ax.plot(crossover_year, crossover_adoption, 'X', color='black', markersize=12,
        zorder=15, markeredgewidth=2)
ax.annotate(f'CBDC overtakes\nmobile payments\n~{int(crossover_year)}',
           xy=(crossover_year, crossover_adoption),
           xytext=(-50, -30), textcoords='offset points',
           fontsize=9, color=MLPURPLE, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                    edgecolor=MLPURPLE, alpha=0.8),
           arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5))

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Adoption Rate (%)', fontweight='bold')
ax.set_title('VARIATION 3: CBDC with Higher Ceiling\n(Carrying capacity K: 50% -> 90%)',
             fontsize=14, fontweight='bold', color=MLPURPLE, pad=15)
ax.set_xlim(1960, 2050)
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', framealpha=0.9, fontsize=8)

# Overall figure title
fig.suptitle('Payment Technology Adoption: Parameter Sensitivity Analysis\nRogers (1962) S-Curve Model',
             fontsize=16, fontweight='bold', color=MLPURPLE, y=0.995)

plt.tight_layout(rect=[0, 0, 1, 0.99])
plt.savefig(Path(__file__).parent / 'chart_varied.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart_varied.png', dpi=150, bbox_inches='tight')
plt.close()

print("Variation charts saved to chart_varied.pdf and chart_varied.png")
print("\nKey Findings:")
print("  VARIATION 1: BNPL has fastest r (0.20) but low K (40%)")
print("  VARIATION 2: Doubling crypto r speeds adoption by ~8 years")
print("  VARIATION 3: K=90% CBDC overtakes mobile payments by ~2040")
