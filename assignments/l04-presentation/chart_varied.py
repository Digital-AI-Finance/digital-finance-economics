r"""Network Effects Variations: Multiple Threshold Scenarios

This chart shows how critical mass (the point where network value exceeds
switching costs) changes under different switching cost thresholds and with
different network value models.

Economic Model:
    Four variations exploring critical mass sensitivity:
    1. Baseline (threshold = 500): Standard switching cost scenario
    2. Low barrier (threshold = 100): Easy to switch systems
    3. High barrier (threshold = 2000): Difficult to switch systems
    4. Reed's Law: Exponential value from group formation

    Models: Metcalfe $V = \frac{n^2}{1000}$, Odlyzko-Tilly
    $V = \frac{n \ln(n)}{10}$, Linear $V = n$, Reed $V = 2^{n/10}$
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 11, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.figsize': (16, 12), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLMAGENTA = '#9467BD'

# Simulation parameters
n = np.arange(1, 1001)

# Network value models
V_metcalfe = n**2 / 1000
V_odlyzko = n * np.log(n) / 10
V_linear = n
V_reed = 2**(n/10)  # Reed's Law for variation 3

# Create 2x2 subplot
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

# Helper function to find critical mass
def find_critical_mass(V, threshold, n):
    idx = np.where(V > threshold)[0]
    return n[idx[0]] if len(idx) > 0 else None

# Helper function to plot network models
def plot_network_models(ax, threshold, include_reed=False):
    # Plot curves
    ax.plot(n, V_metcalfe, label=r"Metcalfe's Law ($V \propto n^2$)",
            color=MLPURPLE, linewidth=2)
    ax.plot(n, V_odlyzko, label=r"Odlyzko-Tilly ($V \propto n \log n$)",
            color=MLBLUE, linewidth=2)
    ax.plot(n, V_linear, label=r"Linear Growth ($V \propto n$)",
            color=MLORANGE, linewidth=2)

    if include_reed:
        ax.plot(n, V_reed, label=r"Reed's Law ($V = 2^{n/10}$)",
                color=MLMAGENTA, linewidth=2)

    # Threshold line
    ax.axhline(y=threshold, color=MLRED, linestyle='--',
               linewidth=1.5, label=f'Switching Cost = {threshold}', alpha=0.8)

    # Find and mark critical mass points
    critical_metcalfe = find_critical_mass(V_metcalfe, threshold, n)
    critical_odlyzko = find_critical_mass(V_odlyzko, threshold, n)
    critical_linear = find_critical_mass(V_linear, threshold, n)

    if critical_metcalfe:
        ax.axvline(x=critical_metcalfe, color=MLPURPLE, linestyle=':',
                   linewidth=1, alpha=0.5)
        ax.plot(critical_metcalfe, threshold, 'o', color=MLPURPLE,
                markersize=6, zorder=5)
        ax.text(critical_metcalfe, threshold*0.5, f'n={critical_metcalfe}',
                color=MLPURPLE, fontsize=9, rotation=90, va='bottom', ha='right')

    if critical_odlyzko:
        ax.axvline(x=critical_odlyzko, color=MLBLUE, linestyle=':',
                   linewidth=1, alpha=0.5)
        ax.plot(critical_odlyzko, threshold, 'o', color=MLBLUE,
                markersize=6, zorder=5)
        ax.text(critical_odlyzko, threshold*0.5, f'n={critical_odlyzko}',
                color=MLBLUE, fontsize=9, rotation=90, va='bottom', ha='right')

    if critical_linear:
        ax.axvline(x=critical_linear, color=MLORANGE, linestyle=':',
                   linewidth=1, alpha=0.5)
        ax.plot(critical_linear, threshold, 'o', color=MLORANGE,
                markersize=6, zorder=5)
        ax.text(critical_linear, threshold*0.5, f'n={critical_linear}',
                color=MLORANGE, fontsize=9, rotation=90, va='bottom', ha='right')

    if include_reed:
        critical_reed = find_critical_mass(V_reed, threshold, n)
        if critical_reed:
            ax.axvline(x=critical_reed, color=MLMAGENTA, linestyle=':',
                       linewidth=1, alpha=0.5)
            ax.plot(critical_reed, threshold, 'o', color=MLMAGENTA,
                    markersize=6, zorder=5)
            ax.text(critical_reed, threshold*0.5, f'n={critical_reed}',
                    color=MLMAGENTA, fontsize=9, rotation=90, va='bottom', ha='right')

    # Styling
    ax.set_xlabel('Network Size (users)')
    ax.set_ylabel('Network Value (log scale)')
    ax.set_yscale('log')
    ax.set_xlim(0, 1000)
    ax.legend(loc='upper left', framealpha=0.95, fontsize=9)
    ax.grid(True, alpha=0.3, linestyle='--')

# PANEL 1: Baseline (threshold = 500)
ax = axes[0]
plot_network_models(ax, 500)
ax.set_title('Panel 1: Baseline (Switching Cost = 500)', fontweight='bold')
ax.set_ylim(1, 2000)
ax.annotate('Critical mass:\nLinear = 500\nMetcalfe = 708\nOdlyzko ≈ 750',
           xy=(700, 500), xytext=(400, 1200),
           fontsize=9, ha='left',
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8),
           arrowprops=dict(arrowstyle='->', lw=1))

# PANEL 2: VARIATION 1 - Low threshold (100)
ax = axes[1]
plot_network_models(ax, 100)
ax.set_title('Panel 2: VARIATION 1 - Low Barrier (Switching Cost = 100)',
             fontweight='bold')
ax.set_ylim(1, 2000)
ax.annotate('Lower switching costs\nmean earlier critical mass',
           xy=(317, 100), xytext=(600, 600),
           fontsize=9, ha='left',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
           arrowprops=dict(arrowstyle='->', lw=1))

# PANEL 3: VARIATION 2 - High threshold (2000)
ax = axes[2]
plot_network_models(ax, 2000)
ax.set_title('Panel 3: VARIATION 2 - High Barrier (Switching Cost = 2000)',
             fontweight='bold')
ax.set_ylim(1, 3000)
ax.annotate('No model reaches\ncritical mass\nwithin 1000 users',
           xy=(500, 2000), xytext=(200, 2500),
           fontsize=9, ha='left',
           bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8),
           arrowprops=dict(arrowstyle='->', lw=1))

# PANEL 4: VARIATION 3 - Reed's Law
ax = axes[3]
plot_network_models(ax, 500, include_reed=True)
ax.set_title('Panel 4: VARIATION 3 - Reed\'s Law (Switching Cost = 500)',
             fontweight='bold')
ax.set_ylim(1, 10000)
ax.annotate('Reed\'s Law:\nExponential value\nfrom group formation\n(n ≈ 90)',
           xy=(90, 500), xytext=(300, 3000),
           fontsize=9, ha='left',
           bbox=dict(boxstyle='round', facecolor='plum', alpha=0.8),
           arrowprops=dict(arrowstyle='->', lw=1))

plt.suptitle('Network Effects Variations: Sensitivity of Critical Mass to Switching Costs',
             fontsize=14, fontweight='bold', y=0.995)
plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart_varied.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart_varied.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart_varied.pdf and chart_varied.png")
