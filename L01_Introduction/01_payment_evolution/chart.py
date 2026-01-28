"""Payment Technology Adoption - Rogers (1962) Diffusion of Innovations S-Curve Model

Demonstrates technology adoption lifecycle using S-curve (logistic growth) model:
S(t) = K / (1 + exp(-r(t - t0))) where K is carrying capacity, r is growth rate,
and t0 is the inflection point. Shows overlapping adoption curves for successive
payment technologies from credit cards to CBDCs.
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

# S-curve adoption model: S(t) = K / (1 + exp(-r(t - t0)))
def s_curve(t, K, r, t0):
    """Rogers diffusion S-curve: K=carrying capacity, r=growth rate, t0=inflection point"""
    return K / (1 + np.exp(-r * (t - t0)))

# Time range: 1900-2050 (focus on modern payment evolution)
t = np.linspace(1900, 2050, 1000)

# Payment technologies with adoption parameters
# (name, K, r, t0, color)
technologies = [
    ('Credit Cards', 75, 0.08, 1970, MLORANGE),
    ('ATMs/Debit', 85, 0.10, 1985, MLBLUE),
    ('Online Banking', 70, 0.12, 2000, MLGREEN),
    ('Mobile Payments', 65, 0.15, 2015, MLRED),
    ('Cryptocurrencies', 30, 0.10, 2022, '#9467BD'),
    ('CBDCs (projected)', 50, 0.12, 2030, MLPURPLE),
]

fig, ax = plt.subplots(figsize=(12, 7))

# Plot S-curves for each technology
for name, K, r, t0, color in technologies:
    adoption = s_curve(t, K, r, t0)
    ax.plot(t, adoption, label=name, color=color, linewidth=2.5, alpha=0.8)

    # Mark inflection point (50% of K)
    inflection_adoption = K / 2
    ax.plot(t0, inflection_adoption, 'o', color=color, markersize=8, zorder=10)

    # Annotate inflection point for selected technologies
    if name in ['Credit Cards', 'Mobile Payments', 'CBDCs (projected)']:
        ax.annotate(f'{int(t0)}', xy=(t0, inflection_adoption),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=10, color=color, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                            edgecolor=color, alpha=0.7))

# Styling
ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Adoption Rate (%)', fontweight='bold')
ax.set_title('Payment Technology Adoption Lifecycles\nRogers (1962) Diffusion of Innovations Model',
             fontsize=16, fontweight='bold', color=MLPURPLE, pad=20)
ax.set_xlim(1950, 2050)
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper left', framealpha=0.9, fontsize=11)

# Add theory annotation
ax.text(0.98, 0.02, 'S-curve: S(t) = K / (1 + exp(-r(t - t₀)))\nDots mark inflection points (50% of max adoption)',
        transform=ax.transAxes, fontsize=9, verticalalignment='bottom',
        horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6),
        style='italic')

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
