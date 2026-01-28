"""Global Digital Payments Growth - Transaction volume trends"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (10, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLLAVENDER = '#ADADE0'

fig, ax = plt.subplots(figsize=(10, 6))

# Simulated data based on realistic trends
years = np.arange(2017, 2028)

# Digital payments transaction value (trillion USD)
digital_payments = np.array([3.0, 3.6, 4.4, 5.2, 6.7, 8.5, 9.5, 10.8, 12.2, 13.8, 15.5])

# Mobile payments subset
mobile_payments = np.array([0.8, 1.2, 1.8, 2.5, 3.8, 5.2, 6.2, 7.4, 8.6, 10.0, 11.5])

# Cryptocurrency transactions (smaller scale)
crypto_transactions = np.array([0.05, 0.15, 0.25, 0.45, 1.2, 2.1, 1.8, 2.3, 2.8, 3.5, 4.2])

# Plot lines
ax.fill_between(years, digital_payments, alpha=0.3, color=MLPURPLE, label='_nolegend_')
ax.plot(years, digital_payments, 'o-', color=MLPURPLE, linewidth=2.5,
        markersize=8, label='Total Digital Payments')

ax.fill_between(years, mobile_payments, alpha=0.3, color=MLBLUE, label='_nolegend_')
ax.plot(years, mobile_payments, 's-', color=MLBLUE, linewidth=2.5,
        markersize=8, label='Mobile Payments')

ax.fill_between(years, crypto_transactions, alpha=0.3, color=MLORANGE, label='_nolegend_')
ax.plot(years, crypto_transactions, '^-', color=MLORANGE, linewidth=2.5,
        markersize=8, label='Crypto Transactions')

# Mark projection region
ax.axvline(x=2024, color='gray', linestyle='--', alpha=0.5)
ax.text(2025.5, 14, 'Projected', fontsize=11, color='gray', style='italic')

# Annotations
ax.annotate('COVID-19\nacceleration', xy=(2020, 5.2), xytext=(2019.2, 8),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Transaction Value (Trillion USD)', fontweight='bold')
ax.set_title('Global Digital Payments Growth', fontsize=16, fontweight='bold',
             color=MLPURPLE)

ax.legend(loc='upper left', framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_xlim(2016.5, 2027.5)
ax.set_ylim(0, 17)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
