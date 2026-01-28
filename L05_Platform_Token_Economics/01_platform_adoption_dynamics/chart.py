"""Platform Adoption S-Curves using Bass Diffusion Model"""
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

# Bass Diffusion Model: dN/dt = (p + q*N/M)*(M - N)
# Simulate 3 platforms over 20 years with dt=0.1

platforms = [
    {'name': 'Traditional Bank', 'p': 0.01, 'q': 0.1, 'M': 1e6, 'color': MLBLUE},
    {'name': 'Fintech', 'p': 0.03, 'q': 0.4, 'M': 1e6, 'color': MLORANGE},
    {'name': 'Crypto Exchange', 'p': 0.05, 'q': 0.25, 'M': 1e6, 'color': MLPURPLE}
]

t_max = 20
dt = 0.1
t = np.arange(0, t_max, dt)

fig, ax = plt.subplots()

for platform in platforms:
    p = platform['p']
    q = platform['q']
    M = platform['M']

    N = np.zeros(len(t))
    N[0] = p * M  # Initial adopters

    # Euler integration
    for i in range(1, len(t)):
        dN = (p + q * N[i-1] / M) * (M - N[i-1]) * dt
        N[i] = N[i-1] + dN

    # Plot adoption curve
    ax.plot(t, N / 1e6, linewidth=2.5, label=platform['name'], color=platform['color'])

    # Find inflection point (where second derivative changes sign, or where N ≈ M/2)
    inflection_idx = np.argmin(np.abs(N - M/2))
    inflection_t = t[inflection_idx]
    inflection_N = N[inflection_idx] / 1e6

    # Annotate inflection point
    ax.plot(inflection_t, inflection_N, 'o', color=platform['color'], markersize=8)
    ax.annotate(f'{inflection_t:.1f}y',
                xy=(inflection_t, inflection_N),
                xytext=(10, 10), textcoords='offset points',
                fontsize=11, color=platform['color'],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=platform['color'], alpha=0.7))

ax.set_xlabel('Time (years)')
ax.set_ylabel('Cumulative Adoption (millions)')
ax.set_title('Platform Adoption: Bass Diffusion Model')
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(0, t_max)
ax.set_ylim(0, 1.1)

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
