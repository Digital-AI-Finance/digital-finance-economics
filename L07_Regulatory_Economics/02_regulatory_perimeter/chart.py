r"""Regulatory Perimeter: Firm Response to Regulation Intensity

Illustrates how firms respond to increasing regulatory burden through compliance,
informalization, or exit/relocation decisions based on cost-benefit analysis.

Economic Model: Regulatory Perimeter Firm Decision
Economic Formula: $\text{Firm stays compliant if: } \pi_{\text{regulated}} - C(r) \geq \pi_{\text{unregulated}}$
where:
  - pi_regulated = Profit from operating within the regulated perimeter
  - C(r) = Compliance cost as a function of regulation intensity r
  - pi_unregulated = Profit from operating outside (informal sector or relocation)
  - Compliant fraction = max(0, 1-r)
  - Informal fraction = min(r, 0.3)
  - Relocated fraction = max(0, r-0.3)

Citation: De Soto (1989) - The Other Path; Porta & Shleifer (2014) - Informality and Development
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

# Generate regulation intensity values
r = np.linspace(0, 1, 200)

# Firm responses to regulation
Compliant = np.maximum(0, 1 - r)
Informal = np.minimum(r, 0.3)
Relocated = np.maximum(0, r - 0.3)

# Create stacked area plot
fig, ax = plt.subplots()

ax.fill_between(r, 0, Compliant, alpha=0.8, color=MLGREEN, label='Compliant Firms')
ax.fill_between(r, Compliant, Compliant + Informal, alpha=0.8, color=MLORANGE, label='Informal Sector')
ax.fill_between(r, Compliant + Informal, Compliant + Informal + Relocated,
                alpha=0.8, color=MLRED, label='Relocated/Exit')

ax.set_xlabel('Regulation Intensity (r)')
ax.set_ylabel('Proportion of Firms')
ax.set_title('Regulatory Perimeter: Firm Response to Regulation Intensity')
ax.legend(loc='best')
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.1)

# Add educational annotation
ax.text(0.02, 0.98, 'Perimeter Effect: Profit(inside) - C(r) ≥ Profit(outside)\nFirms exit when compliance cost > profit',
        transform=ax.transAxes, fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
