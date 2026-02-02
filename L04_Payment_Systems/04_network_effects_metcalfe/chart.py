"""Network Effects: Metcalfe's Law in Payment Systems

This chart demonstrates how network value grows with the number of users
according to different models: Metcalfe's Law (quadratic), Odlyzko-Tilly
(n*log(n)), and linear growth. It shows the critical mass threshold where
network value exceeds switching costs.

Citation: Metcalfe (2013) - Metcalfe's Law after 40 Years of Ethernet; Odlyzko and Tilly (2005)
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

# Simulation parameters
n = np.arange(1, 1001)
switching_cost_threshold = 500

# Network value models
V_metcalfe = n**2 / 1000  # Metcalfe's Law: V ~ n^2
V_odlyzko = n * np.log(n) / 10  # Odlyzko-Tilly: V ~ n*log(n)
V_linear = n  # Linear: V ~ n

# Find critical mass (first point where V > threshold)
critical_metcalfe = n[np.where(V_metcalfe > switching_cost_threshold)[0][0]]
critical_odlyzko = n[np.where(V_odlyzko > switching_cost_threshold)[0][0]]
critical_linear = n[np.where(V_linear > switching_cost_threshold)[0][0]]

# Create plot
fig, ax = plt.subplots()

# Plot curves
ax.plot(n, V_metcalfe, label="Metcalfe's Law ($V \propto n^2$)",
        color=MLPURPLE, linewidth=2.5)
ax.plot(n, V_odlyzko, label="Odlyzko-Tilly ($V \propto n \log n$)",
        color=MLBLUE, linewidth=2.5)
ax.plot(n, V_linear, label="Linear Growth ($V \propto n$)",
        color=MLORANGE, linewidth=2.5)

# Switching cost threshold
ax.axhline(y=switching_cost_threshold, color=MLRED, linestyle='--',
           linewidth=1.5, label='Switching Cost Threshold', alpha=0.8)

# Shade viable region
ax.fill_between(n, switching_cost_threshold, 1200, alpha=0.1,
                 color=MLGREEN, label='Viable Region')

# Mark critical mass points
ax.axvline(x=critical_metcalfe, color=MLPURPLE, linestyle=':',
           linewidth=1, alpha=0.6)
ax.axvline(x=critical_odlyzko, color=MLBLUE, linestyle=':',
           linewidth=1, alpha=0.6)
ax.axvline(x=critical_linear, color=MLORANGE, linestyle=':',
           linewidth=1, alpha=0.6)

# Annotations for critical mass
ax.text(critical_metcalfe, 50, f'  {critical_metcalfe}',
        color=MLPURPLE, fontsize=11, rotation=90, va='bottom')
ax.text(critical_odlyzko, 50, f'  {critical_odlyzko}',
        color=MLBLUE, fontsize=11, rotation=90, va='bottom')
ax.text(critical_linear, 50, f'  {critical_linear}',
        color=MLORANGE, fontsize=11, rotation=90, va='bottom')

# Labels and title
ax.set_xlabel('Network Size (users)')
ax.set_ylabel('Network Value (log scale)')
ax.set_title('Network Value Growth Models in Payment Systems')
ax.set_yscale('log')
ax.set_ylim(1, 1200)
ax.set_xlim(0, 1000)
ax.legend(loc='upper left', framealpha=0.95)
ax.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
