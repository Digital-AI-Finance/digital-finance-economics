r"""Network Adoption with Subsidies

Multi-panel chart showing how subsidies affect payment network adoption
equilibria under different network effect strengths.

# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model: Network Adoption Dynamics
- $\frac{dx}{dt} = (\sigma x - c + s)(1-x) - \delta x$
- Steady states: stable adoption as function of subsidy $s$ for different $\sigma$
- Bifurcation diagram shows critical mass threshold

Calibration: sigma = [0.5, 1.0, 1.5], c = 0.3, delta_d = 0.1, s in [0, 0.5]

Citation: Katz & Shapiro (1985), Cabral (2011)
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.optimize import brentq

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# --- Model parameters ---
c = 0.3       # adoption cost
delta_d = 0.1  # decay/churn rate
sigmas = [0.5, 1.0, 1.5]
sigma_colors = [MLBLUE, MLORANGE, MLRED]
sigma_labels = [r'$\sigma=0.5$ (weak)', r'$\sigma=1.0$ (moderate)',
                r'$\sigma=1.5$ (strong)']

s_range = np.linspace(0, 0.5, 300)


def dxdt(x, sigma, s):
    """dx/dt = (sigma*x - c + s)*(1-x) - delta_d*x"""
    return (sigma * x - c + s) * (1 - x) - delta_d * x


def find_equilibria(sigma, s):
    """Find all steady states for given sigma and s."""
    x_grid = np.linspace(0.001, 0.999, 1000)
    f_vals = np.array([dxdt(x, sigma, s) for x in x_grid])

    # Find sign changes
    equilibria = []
    for i in range(len(f_vals) - 1):
        if f_vals[i] * f_vals[i + 1] < 0:
            try:
                x_eq = brentq(dxdt, x_grid[i], x_grid[i + 1], args=(sigma, s))
                # Check stability: d(dxdt)/dx < 0 means stable
                eps = 1e-6
                deriv = (dxdt(x_eq + eps, sigma, s) - dxdt(x_eq - eps, sigma, s)) / (2 * eps)
                equilibria.append((x_eq, deriv < 0))
            except ValueError:
                pass

    # Also check x=0 boundary
    if dxdt(0.001, sigma, s) < 0:
        equilibria.append((0.0, True))
    else:
        equilibria.append((0.0, False))

    return equilibria


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Bifurcation diagram ---
for k, (sigma, color, label) in enumerate(zip(sigmas, sigma_colors, sigma_labels)):
    stable_x = []
    stable_s = []
    unstable_x = []
    unstable_s = []

    for s_val in s_range:
        eqs = find_equilibria(sigma, s_val)
        for x_eq, is_stable in eqs:
            if is_stable and x_eq > 0.01:
                stable_x.append(x_eq)
                stable_s.append(s_val)
            elif not is_stable and x_eq > 0.01:
                unstable_x.append(x_eq)
                unstable_s.append(s_val)

    ax1.plot(stable_s, stable_x, '-', color=color, linewidth=2.5,
             label=label, zorder=4)
    if unstable_s:
        ax1.plot(unstable_s, unstable_x, '--', color=color, linewidth=1.5,
                 alpha=0.5, zorder=3)

# Mark critical mass threshold region
ax1.axhline(y=0.16, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax1.text(0.42, 0.17, 'Critical mass (~16%)', fontsize=10, color='gray')

# Annotate the bifurcation point for sigma=1.0
# Find where stable branch appears for sigma=1.0
for s_val in s_range:
    eqs = find_equilibria(1.0, s_val)
    high_stable = [x for x, st in eqs if st and x > 0.3]
    if high_stable:
        ax1.annotate(f'Tipping point\n(s={s_val:.2f})',
                     xy=(s_val, high_stable[0]),
                     xytext=(s_val + 0.1, high_stable[0] - 0.15),
                     fontsize=10,
                     bbox=dict(boxstyle='round,pad=0.3', facecolor=MLLAVENDER,
                               alpha=0.9),
                     arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5))
        break

ax1.set_xlabel('Subsidy Level ($s$)')
ax1.set_ylabel('Stable Adoption Rate ($x^*$)')
ax1.set_title('(a) Adoption vs Subsidy (Bifurcation)')
ax1.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax1.set_xlim(0, 0.5)
ax1.set_ylim(0, 1.0)
ax1.grid(True, alpha=0.2, linestyle='--')

# --- Panel (b): Optimal subsidy vs sigma ---
sigma_range = np.linspace(0.3, 2.0, 50)
optimal_subsidies = []
max_adoption_gains = []

for sigma in sigma_range:
    best_s = 0
    best_gain = 0
    for s_val in np.linspace(0, 0.5, 200):
        eqs = find_equilibria(sigma, s_val)
        high_eq = [x for x, st in eqs if st and x > 0.1]
        eqs_no_sub = find_equilibria(sigma, 0)
        base_eq = [x for x, st in eqs_no_sub if st and x > 0.01]
        base_max = max(base_eq) if base_eq else 0

        if high_eq:
            gain = max(high_eq) - base_max
            # Net benefit: gain - cost_of_subsidy
            net = gain - s_val * 0.5  # cost weight
            if net > best_gain:
                best_gain = net
                best_s = s_val

    optimal_subsidies.append(best_s)

ax2.plot(sigma_range, optimal_subsidies, '-', color=MLPURPLE, linewidth=2.5,
         zorder=4)
ax2.fill_between(sigma_range, optimal_subsidies, alpha=0.1, color=MLPURPLE)

# Mark the three specific sigma values
for sigma, color, label_short in zip(sigmas, sigma_colors,
                                      ['weak', 'moderate', 'strong']):
    idx = np.argmin(np.abs(sigma_range - sigma))
    s_opt = optimal_subsidies[idx]
    ax2.plot(sigma, s_opt, 'o', color=color, markersize=10, zorder=5)
    ax2.annotate(f'{label_short}\n$s^*$={s_opt:.2f}',
                 xy=(sigma, s_opt), xytext=(15, 10),
                 textcoords='offset points', fontsize=10,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor=MLLAVENDER,
                           alpha=0.8))

# Diminishing returns annotation
ax2.annotate('Diminishing returns:\nstrong networks need\nless subsidy',
             xy=(1.5, optimal_subsidies[np.argmin(np.abs(sigma_range - 1.5))]),
             xytext=(1.6, 0.35),
             fontsize=10,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#d4edda', alpha=0.9),
             arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=1.5))

ax2.set_xlabel(r'Network Effect Strength ($\sigma$)')
ax2.set_ylabel('Optimal Subsidy ($s^*$)')
ax2.set_title(r'(b) Optimal Subsidy vs $\sigma$')
ax2.set_xlim(0.3, 2.0)
ax2.grid(True, alpha=0.2, linestyle='--')

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
