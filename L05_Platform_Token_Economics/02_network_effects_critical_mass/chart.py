"""Network Effects: Critical Mass and Multiple Equilibria

Based on: Katz & Shapiro (1985) - Network Externalities
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

# Agent utility: U_i = theta_i * x - c
# theta_i ~ Uniform(0,1), x = fraction adopting
# Equilibrium: x* = P(theta > c/x*) = max(0, 1 - c/x*)

c_values = np.linspace(0.05, 0.5, 200)
x_grid = np.linspace(0.001, 1, 1000)

stable_equilibria = []
unstable_equilibria = []

def find_fixed_points(c):
    """Find fixed points where f(x) = x, f(x) = max(0, 1 - c/x)"""
    fixed_points = []

    # Check x = 0
    if c > 0:
        fixed_points.append((0, 'stable'))

    # For x > 0: x = 1 - c/x => x^2 = x - c => x^2 - x + c = 0
    discriminant = 1 - 4*c

    if discriminant >= 0:
        x1 = (1 - np.sqrt(discriminant)) / 2
        x2 = (1 + np.sqrt(discriminant)) / 2

        # Check if solutions are in valid range (0, 1]
        for x_star in [x1, x2]:
            if 0 < x_star <= 1:
                # Check stability: stable if f'(x*) < 1
                # f(x) = 1 - c/x, f'(x) = c/x^2
                derivative = c / (x_star**2)
                if derivative < 1:
                    fixed_points.append((x_star, 'stable'))
                else:
                    fixed_points.append((x_star, 'unstable'))

    return fixed_points

# Compute equilibria for each cost level
for c in c_values:
    fps = find_fixed_points(c)
    for x_star, stability in fps:
        if stability == 'stable':
            stable_equilibria.append((c, x_star))
        else:
            unstable_equilibria.append((c, x_star))

# Separate into arrays
if stable_equilibria:
    stable_c, stable_x = zip(*stable_equilibria)
else:
    stable_c, stable_x = [], []

if unstable_equilibria:
    unstable_c, unstable_x = zip(*unstable_equilibria)
else:
    unstable_c, unstable_x = [], []

# Plot bifurcation diagram
fig, ax = plt.subplots()

if stable_equilibria:
    ax.plot(stable_c, stable_x, linewidth=2.5, color=MLPURPLE, label='Stable Equilibria')

if unstable_equilibria:
    ax.plot(unstable_c, unstable_x, linewidth=2.5, linestyle='--', color=MLRED, label='Unstable Equilibria')

# Mark critical mass region
critical_c = 0.25
ax.axvline(critical_c, color='gray', linestyle=':', alpha=0.5, linewidth=1.5)
ax.text(critical_c + 0.01, 0.5, 'Critical Mass\nThreshold', fontsize=11, color='gray')

ax.set_xlabel('Adoption Cost (c)')
ax.set_ylabel('Equilibrium Adoption Rate (x*)')
ax.set_title('Critical Mass: Multiple Equilibria in Platform Adoption')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(0.05, 0.5)
ax.set_ylim(0, 1)

# Add Metcalfe's Law annotation
ax.text(0.02, 0.98, r"Metcalfe's Law: $V = n(n-1)/2$" + "\n" + r"Network value $\propto$ $n^2$",
        transform=ax.transAxes, fontsize=11,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
