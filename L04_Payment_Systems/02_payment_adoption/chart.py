"""Payment System Adoption: Bass Diffusion Model

Innovation and imitation dynamics in payment technology diffusion.
Theory: Bass (1969) "A New Product Growth Model for Consumer Durables"
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.integrate import odeint

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 11,
    'figure.figsize': (12, 8), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'

np.random.seed(42)

# Bass Diffusion Model: dN/dt = (p + q*N/M) * (M - N)
# p = coefficient of innovation (external influence)
# q = coefficient of imitation (internal influence)
# M = market potential
# Peak adoption at t* = (1/(p+q)) * ln(q/p)

def bass_model(N, t, p, q, M):
    """Bass diffusion model differential equation"""
    dNdt = (p + q * N / M) * (M - N)
    return dNdt

def solve_bass(p, q, M, years):
    """Solve Bass model and return cumulative adoption, innovation, and imitation components"""
    N0 = 0.01 * M  # Start with 1% adoption
    N = odeint(bass_model, N0, years, args=(p, q, M))
    N = N.flatten()

    # Decompose into innovation and imitation effects
    innovation_rate = p * (M - N)
    imitation_rate = (q * N / M) * (M - N)

    # Peak adoption time
    t_peak = (1 / (p + q)) * np.log(q / p) if q > p else None

    return N, innovation_rate, imitation_rate, t_peak

# Time array
years = np.linspace(0, 30, 300)

# Define payment systems with different Bass parameters
payment_systems = {
    'Mobile Payments': {
        'p': 0.01,   # Low innovation (needs infrastructure)
        'q': 0.5,    # High imitation (visible, social)
        'M': 90,     # High potential
        'color': MLGREEN
    },
    'Crypto Payments': {
        'p': 0.03,   # High innovation (ideological early adopters)
        'q': 0.3,    # Moderate imitation (network effects)
        'M': 40,     # Lower potential (regulatory uncertainty)
        'color': MLORANGE
    },
    'CBDC': {
        'p': 0.02,   # Moderate innovation (institutional push)
        'q': 0.35,   # Moderate imitation (trust + network)
        'M': 75,     # Moderate-high potential
        'color': MLBLUE
    },
    'Credit Cards': {
        'p': 0.008,  # Low innovation (required infrastructure)
        'q': 0.4,    # High imitation (widespread acceptance)
        'M': 85,     # High potential (mature market)
        'color': MLPURPLE
    }
}

# Create figure with main plot and inset
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)

# Store results for inset
results = {}

# Plot adoption curves
for name, params in payment_systems.items():
    N, innov, imit, t_peak = solve_bass(params['p'], params['q'], params['M'], years)
    results[name] = {'N': N, 'innov': innov, 'imit': imit, 't_peak': t_peak, 'params': params}

    # Plot cumulative adoption
    line_style = '--' if 'Crypto' in name else '-'
    ax.plot(years, N, line_style, color=params['color'], linewidth=2.5,
            label=f"{name} (p={params['p']}, q={params['q']})")

    # Mark peak adoption time
    if t_peak and 0 < t_peak < 30:
        peak_idx = np.argmin(np.abs(years - t_peak))
        ax.plot(t_peak, N[peak_idx], 'o', color=params['color'], markersize=8,
                markeredgewidth=2, markeredgecolor='white')
        ax.annotate(f"Peak: {t_peak:.1f}y",
                   xy=(t_peak, N[peak_idx]),
                   xytext=(t_peak + 2, N[peak_idx] - 5),
                   fontsize=9, color=params['color'],
                   arrowprops=dict(arrowstyle='->', color=params['color'], lw=1))

# Critical mass line
ax.axhline(y=16, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
ax.text(28, 17, 'Critical mass\n(~16%)', fontsize=9, color='gray', va='bottom', ha='right')

# Main plot styling
ax.set_xlabel('Years Since Introduction', fontweight='bold')
ax.set_ylabel('Cumulative Adoption (%)', fontweight='bold')
ax.set_title('Payment System Adoption: Bass Diffusion Model\nInnovation (p) vs. Imitation (q) Effects',
             fontsize=16, fontweight='bold', color=MLPURPLE, pad=15)
ax.legend(loc='upper left', framealpha=0.95, fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 30)
ax.set_ylim(0, 100)

# Add inset showing innovation vs imitation decomposition for Mobile Payments
ax_inset = fig.add_axes([0.55, 0.15, 0.32, 0.25])  # [left, bottom, width, height]

mobile_data = results['Mobile Payments']
ax_inset.fill_between(years, 0, mobile_data['innov'],
                       alpha=0.6, color=MLBLUE, label='Innovation (p)')
ax_inset.fill_between(years, mobile_data['innov'],
                       mobile_data['innov'] + mobile_data['imit'],
                       alpha=0.6, color=MLRED, label='Imitation (q)')
ax_inset.plot(years, mobile_data['innov'] + mobile_data['imit'],
              'k-', linewidth=1.5, label='Total adoption rate')

ax_inset.set_xlabel('Years', fontsize=10)
ax_inset.set_ylabel('Adoption Rate', fontsize=10)
ax_inset.set_title('Mobile Payments: Innovation vs Imitation', fontsize=10, fontweight='bold')
ax_inset.legend(loc='upper right', fontsize=8, framealpha=0.9)
ax_inset.grid(True, alpha=0.2)
ax_inset.set_xlim(0, 30)

# Add citation
fig.text(0.99, 0.01, 'Bass (1969) "A New Product Growth Model for Consumer Durables"',
         fontsize=9, ha='right', style='italic', color='gray')

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
