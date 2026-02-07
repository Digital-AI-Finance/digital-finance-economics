r"""Compliance Cost and Firm Scale: U-Shaped Cost Curve

Modeling economies and diseconomies of scale in regulatory compliance.

Economic Model: U-Shaped Average Compliance Cost
Economic Formula: $AC(Q) = \frac{FC}{Q} + vc + rc \cdot Q^{\alpha - 1}$
where:
  - AC = Average compliance cost as percentage of revenue
  - FC = Fixed compliance costs (licensing, legal, systems)
  - Q = Firm revenue (scale measure)
  - vc = Variable compliance cost rate
  - rc = Regulatory complexity cost scaling factor
  - alpha = Complexity exponent (>1 creates U-shape from diseconomies)

U-Shape Mechanism:
  - Small scale: FC/Q dominates -> high AC (economies of scale)
  - Medium scale: FC/Q decreases -> AC minimum (MES)
  - Large scale: rc*Q^(alpha-1) increases -> rising AC (diseconomies: complexity, scrutiny)

Citation: Stigler (1958) - The Economies of Scale (cost curve foundations);
          Stigler (1971) - The Theory of Economic Regulation (regulatory barrier interpretation)
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (10, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Firm size (revenue in millions)
revenue = np.logspace(0, 4, 200)  # $1M to $10B

def average_cost_curve(revenue, fc, vc_rate, rc_scale, rc_exponent):
    """
    U-shaped average compliance cost curve.

    Parameters:
    -----------
    revenue : array
        Firm revenue (scale measure)
    fc : float
        Fixed compliance costs ($ millions)
    vc_rate : float
        Variable cost rate (fraction of revenue)
    rc_scale : float
        Regulatory complexity cost scaling factor
    rc_exponent : float
        Exponent for diseconomies (>0 creates U-shape)

    Returns:
    --------
    ac_pct : array
        Average compliance cost as % of revenue
    """
    # Total costs
    total_cost = fc + vc_rate * revenue + rc_scale * revenue**rc_exponent

    # Average cost as percentage
    ac_pct = (total_cost / revenue) * 100

    return ac_pct

# Traditional finance firm (banks, broker-dealers)
# Higher fixed costs, steeper initial decline, earlier diseconomies
trad_fc = 5.0        # $5M fixed costs (licensing, systems, legal)
trad_vc = 0.008      # 0.8% variable cost rate
trad_rc_scale = 0.00015
trad_rc_exp = 1.3    # Diseconomies from complexity, scrutiny

trad_ac = average_cost_curve(revenue, trad_fc, trad_vc, trad_rc_scale, trad_rc_exp)

# Crypto/fintech firm
# Lower fixed costs, flatter curve, different MES
crypto_fc = 1.5      # $1.5M fixed costs (lighter licensing)
crypto_vc = 0.005    # 0.5% variable cost rate
crypto_rc_scale = 0.0001
crypto_rc_exp = 1.4  # Steeper diseconomies (regulatory uncertainty)

crypto_ac = average_cost_curve(revenue, crypto_fc, crypto_vc, crypto_rc_scale, crypto_rc_exp)

# Find Minimum Efficient Scale (MES) for each
trad_mes_idx = np.argmin(trad_ac)
trad_mes_revenue = revenue[trad_mes_idx]
trad_mes_cost = trad_ac[trad_mes_idx]

crypto_mes_idx = np.argmin(crypto_ac)
crypto_mes_revenue = revenue[crypto_mes_idx]
crypto_mes_cost = crypto_ac[crypto_mes_idx]

# Create plot
fig, ax = plt.subplots()

# Plot U-shaped curves
ax.semilogx(revenue, trad_ac, color=MLPURPLE, linewidth=2.5,
            label='Traditional Finance', zorder=3)
ax.semilogx(revenue, crypto_ac, color=MLORANGE, linewidth=2.5,
            label='Crypto/Fintech', zorder=3)

# Mark MES points
ax.plot(trad_mes_revenue, trad_mes_cost, 'o', color=MLPURPLE,
        markersize=10, zorder=5, markeredgecolor='black', markeredgewidth=1.5)
ax.plot(crypto_mes_revenue, crypto_mes_cost, 's', color=MLORANGE,
        markersize=10, zorder=5, markeredgecolor='black', markeredgewidth=1.5)

# Annotate MES points
ax.annotate(f'MES: ${trad_mes_revenue:.1f}M\n{trad_mes_cost:.2f}%',
            xy=(trad_mes_revenue, trad_mes_cost),
            xytext=(trad_mes_revenue * 0.3, trad_mes_cost * 1.5),
            fontsize=11,
            arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5))

ax.annotate(f'MES: ${crypto_mes_revenue:.1f}M\n{crypto_mes_cost:.2f}%',
            xy=(crypto_mes_revenue, crypto_mes_cost),
            xytext=(crypto_mes_revenue * 3, crypto_mes_cost * 0.6),
            fontsize=11,
            arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=1.5))

# Add regulatory sandbox zone annotation
sandbox_revenue = 10  # $10M threshold
ax.axvspan(revenue.min(), sandbox_revenue, alpha=0.15, color=MLGREEN, zorder=1)
ax.text(3, ax.get_ylim()[1] * 0.95, 'Regulatory\nSandbox Zone',
        fontsize=11, color=MLGREEN, weight='bold', ha='center', va='top')

# Add reference line for "sustainable" cost level
sustainable_threshold = 2.0
ax.axhline(sustainable_threshold, color=MLRED, linestyle='--',
           linewidth=1.5, alpha=0.6, label='2% Illustrative Threshold', zorder=2)

ax.set_xlabel('Firm Revenue ($ millions)')
ax.set_ylabel('Average Compliance Cost (% of Revenue)')
ax.set_title('U-Shaped Compliance Cost Curve: Stigler (1958, 1971) Economies of Scale')
ax.legend(loc='upper right', framealpha=0.95)
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim(revenue.min(), revenue.max())
ax.set_ylim(0, max(trad_ac.max(), crypto_ac.max()) * 1.05)

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
print(f"\nMinimum Efficient Scale:")
print(f"  Traditional Finance: ${trad_mes_revenue:.1f}M revenue ({trad_mes_cost:.2f}% cost)")
print(f"  Crypto/Fintech: ${crypto_mes_revenue:.1f}M revenue ({crypto_mes_cost:.2f}% cost)")
