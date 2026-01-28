"""Payment System Adoption S-Curves - Technology diffusion patterns"""
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

fig, ax = plt.subplots(figsize=(10, 6))

# Logistic S-curve function
def logistic(t, L, k, t0):
    return L / (1 + np.exp(-k * (t - t0)))

years = np.linspace(0, 30, 100)

# Different payment technologies
# Credit cards (started ~1960, mature)
credit_cards = logistic(years, 85, 0.25, 15)

# Online banking (started ~1995)
online_banking = logistic(years, 75, 0.3, 12)

# Mobile payments (started ~2010)
mobile_payments = logistic(years, 90, 0.4, 10)

# Crypto payments (started ~2015, early stage)
crypto_payments = logistic(years, 40, 0.25, 18)

# Plot curves
ax.plot(years, credit_cards, '-', color=MLPURPLE, linewidth=2.5,
        label='Credit Cards (1960s)')
ax.plot(years, online_banking, '-', color=MLBLUE, linewidth=2.5,
        label='Online Banking (1990s)')
ax.plot(years, mobile_payments, '-', color=MLGREEN, linewidth=2.5,
        label='Mobile Payments (2010s)')
ax.plot(years, crypto_payments, '--', color=MLORANGE, linewidth=2.5,
        label='Crypto Payments (2020s)')

# Annotations for phases
ax.annotate('Innovation\nPhase', xy=(3, 10), fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
ax.annotate('Growth\nPhase', xy=(12, 50), fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
ax.annotate('Maturity\nPhase', xy=(25, 80), fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Critical mass line
ax.axhline(y=16, color='gray', linestyle=':', alpha=0.5)
ax.text(28, 17, 'Critical mass\n(~16%)', fontsize=9, color='gray', va='bottom')

ax.set_xlabel('Years Since Introduction', fontweight='bold')
ax.set_ylabel('Adoption Rate (%)', fontweight='bold')
ax.set_title('Payment System Adoption: S-Curve Dynamics', fontsize=16,
             fontweight='bold', color=MLPURPLE)

ax.legend(loc='lower right', framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 30)
ax.set_ylim(0, 100)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
