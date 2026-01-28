"""CBDC Monetary Policy Transmission - impulse response comparison"""
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

# Simulation parameters
months = 12
policy_rate = np.concatenate([np.array([0]), np.ones(months-1)])  # 100bp shock at t=0

# Traditional channel (low friction = 0.3)
traditional_rate = np.zeros(months)
friction_traditional = 0.3

for t in range(1, months):
    traditional_rate[t] = traditional_rate[t-1] + friction_traditional * (policy_rate[t] - traditional_rate[t-1])

# CBDC channel (high friction = 0.9)
cbdc_rate = np.zeros(months)
friction_cbdc = 0.9

for t in range(1, months):
    cbdc_rate[t] = cbdc_rate[t-1] + friction_cbdc * (policy_rate[t] - cbdc_rate[t-1])

# Plot
fig, ax = plt.subplots()

# Plot impulse responses
time = np.arange(months)
ax.plot(time, traditional_rate, '-o', color=MLBLUE, linewidth=2.5,
        label='Traditional Banking Channel', markersize=6)
ax.plot(time, cbdc_rate, '-s', color=MLPURPLE, linewidth=2.5,
        label='CBDC Channel', markersize=6)

# Full pass-through line
ax.axhline(y=1.0, color='black', linestyle='--', linewidth=1.5,
           alpha=0.7, label='Full Pass-through')

# Shade transmission gap
ax.fill_between(time, traditional_rate, cbdc_rate, alpha=0.2, color=MLLAVENDER,
                label='Transmission Gap')

# Annotations
ax.annotate('Traditional:\nslow, incomplete', xy=(8, traditional_rate[8]),
            xytext=(9.5, 0.5), fontsize=12, color=MLBLUE,
            arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=MLBLUE, alpha=0.8))

ax.annotate('CBDC:\nfast, near-complete', xy=(3, cbdc_rate[3]),
            xytext=(4.5, 1.15), fontsize=12, color=MLPURPLE,
            arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=MLPURPLE, alpha=0.8))

# Formatting
ax.set_xlabel('Months Since Policy Rate Shock', fontweight='bold')
ax.set_ylabel('Interest Rate Pass-through (percentage points)', fontweight='bold')
ax.set_title('Monetary Policy Transmission: Traditional vs CBDC', fontweight='bold', pad=20)
ax.set_ylim(-0.1, 1.3)
ax.set_xlim(-0.5, months-0.5)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='lower right', framealpha=0.95)

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
