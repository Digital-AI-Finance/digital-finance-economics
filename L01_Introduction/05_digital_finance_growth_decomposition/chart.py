"""Digital Finance Growth Decomposition: Solow-Style Accounting

Decomposing fintech sector growth into technology infrastructure, adoption,
network effects, and total factor productivity (TFP) components.

Citation: Solow, R. M. (1957). Technical change and the aggregate production function.
The Review of Economics and Statistics, 39(3), 312-320.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (12, 8), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Time series: 2010-2025
years = np.arange(2010, 2026)
t = years - 2010

# Growth decomposition: Growth = α*Technology + β*Adoption + γ*Network + TFP_residual
# All contributions in percentage points per year

# 1. Technology Infrastructure (starts small, accelerates)
# Captures: cloud computing, APIs, mobile platforms, blockchain
tech_contribution = 0.5 + 1.8 * (1 - np.exp(-0.25 * t))  # Asymptotes at ~2.3%
tech_contribution[0:2] = [0.3, 0.4]  # Slower start pre-smartphone era

# 2. Adoption/Penetration (S-curve pattern)
# Captures: user growth, market penetration, financial inclusion
adoption_contribution = 3.5 / (1 + np.exp(-0.5 * (t - 8)))  # Inflection at 2018
adoption_contribution[0:3] = [0.5, 0.7, 1.0]  # Early phase

# 3. Network Effects (exponential after critical mass)
# Captures: platform effects, two-sided markets, ecosystem value
network_contribution = np.zeros_like(t, dtype=float)
network_contribution[5:] = 0.8 * (1 - np.exp(-0.3 * (t[5:] - 5)))  # Kicks in after 2015
network_contribution = np.minimum(network_contribution, 2.0)  # Cap at 2%

# 4. Regulatory Environment (step changes)
# Captures: PSD2 (2018), open banking, CBDC pilots
regulatory_contribution = np.zeros_like(t, dtype=float)
regulatory_contribution[0:8] = 0.2  # Pre-PSD2
regulatory_contribution[8:11] = 0.8  # PSD2 effect (2018-2020)
regulatory_contribution[11:] = 1.2  # Pandemic regulatory acceleration (2021+)

# 5. Calculate total observed growth and TFP residual
# Total growth = sum of explained factors + TFP
# We set total growth as a reasonable fintech sector growth path
total_growth = 5.0 + 8.0 / (1 + np.exp(-0.4 * (t - 10)))  # Ranges 5-13% annual growth
total_growth[11] = 18.0  # Pandemic spike (2021)
total_growth[12:] = 12.0 - 0.5 * (t[12:] - 12)  # Gradual normalization

# TFP residual = innovation, efficiency gains not captured by factors
explained_factors = tech_contribution + adoption_contribution + network_contribution + regulatory_contribution
tfp_residual = total_growth - explained_factors
tfp_residual = np.maximum(tfp_residual, 0.1)  # Ensure non-negative

# Create stacked area chart
fig, ax = plt.subplots(figsize=(12, 8))

# Stack the contributions
ax.stackplot(years,
             tech_contribution,
             adoption_contribution,
             network_contribution,
             regulatory_contribution,
             tfp_residual,
             labels=['Technology Infrastructure',
                     'Adoption & Penetration',
                     'Network Effects',
                     'Regulatory Environment',
                     'TFP Residual (Innovation)'],
             colors=[MLBLUE, MLGREEN, MLORANGE, MLLAVENDER, MLPURPLE],
             alpha=0.85)

# Overlay total growth line
ax.plot(years, total_growth, color='black', linewidth=3, linestyle='--',
        label='Total Growth', marker='o', markersize=6)

# Annotate key periods
ax.axvspan(2010, 2013, alpha=0.1, color='gray', label='_nolegend_')
ax.text(2011.5, 16, 'Early\nSmartphone Era', ha='center', fontsize=11,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.axvspan(2017, 2019, alpha=0.1, color='blue', label='_nolegend_')
ax.text(2018, 16, 'PSD2 &\nOpen Banking', ha='center', fontsize=11,
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

ax.axvline(2020, color='red', linestyle=':', linewidth=2, alpha=0.6)
ax.text(2020, 19, 'Pandemic\nAcceleration', ha='center', fontsize=11, color='red',
        weight='bold', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Labels and title
ax.set_xlabel('Year', fontweight='bold', fontsize=14)
ax.set_ylabel('Annual Growth Contribution (Percentage Points)', fontweight='bold', fontsize=14)
ax.set_title('Digital Finance Growth Decomposition: Solow-Style Accounting\n' +
             'Growth = α·Technology + β·Adoption + γ·Network + δ·Regulation + TFP',
             fontweight='bold', fontsize=16, pad=20)

# Legend
ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True, fontsize=12)

# Grid
ax.grid(True, alpha=0.3, linestyle='--', axis='y')
ax.set_xlim(2010, 2025)
ax.set_ylim(0, 20)

# Add citation
fig.text(0.99, 0.01, 'Source: Solow (1957) growth accounting methodology',
         ha='right', fontsize=10, style='italic', color='gray')

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
