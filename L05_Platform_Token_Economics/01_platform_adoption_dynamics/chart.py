"""Platform Adoption: Katz-Shapiro Network Externalities

Multiple equilibria under network effects and expectations coordination.
Theory: Katz & Shapiro (1985) "Network Externalities, Competition, and Compatibility"

Economic Model:
  User utility: $u_i(n^e) = v_0 + \\theta \\cdot n^e - p$
  Response function: $n = R(n^e)$ where $n$ is actual adoption given expectations $n^e$
  Fulfilled-expectations equilibrium: $n^e = n$ (45-degree line)
  Stable equilibrium: $R'(n^*) < 1$; Unstable: $R'(n^*) > 1$

Citation: Katz & Shapiro (1985) - Network Externalities, Competition, and Compatibility
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (10, 7), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Katz-Shapiro Model Parameters
# User utility: u(n) = v(n^e) - p
# v(n) = v_0 + theta*n (intrinsic value + network value)
# Fulfilled expectations equilibrium: n^e = n

N_max = 100       # Market size

# Expected adoption (what users believe will happen)
n_e = np.linspace(0, N_max, 500)

# Response function: actual adoption based on expected network size
# Explicitly designed to create 3 equilibria with correct stability
def actual_adoption(n_expected, N_max):
    """
    Response function showing actual adoption given expectations.

    Key: Stable equilibria occur where response crosses 45-degree line from ABOVE (slope < 1)
         Unstable equilibria occur where response crosses from BELOW (slope > 1)

    Creates exactly 3 equilibria:
    - Low stable: ~15 users (curve crosses from above)
    - Unstable (critical mass): ~50 users (curve crosses from below)
    - High stable: ~90 users (curve crosses from above)
    """
    x = n_expected / N_max  # Normalize to [0, 1]

    # Need a function that goes:
    # - Above 45-degree line for x < 0.15 (so it crosses down to create stable point)
    # - Below 45-degree line for 0.15 < x < 0.50 (below the line)
    # - Above 45-degree line for 0.50 < x < 0.90 (so it crosses down at 0.50 unstable, up at 0.90)
    # - Below 45-degree line for x > 0.90 (so it crosses down to create stable point)

    # Invert the cubic: use NEGATIVE amplitude
    # This makes the response curve go above-below-above-below relative to 45-degree line
    deviation = -15 * (x - 0.15) * (x - 0.50) * (x - 0.90)
    y = x + deviation

    # Ensure bounds [0, 1]
    y = np.clip(y, 0, 1)

    return y * N_max

n_actual = actual_adoption(n_e, N_max)

# Find equilibria (intersections with 45-degree line)
# Equilibrium condition: n_actual = n_expected
# Use sign changes in (n_actual - n_e) to find crossings
diff = n_actual - n_e
equilibria_idx = []
for i in range(1, len(diff)):
    if diff[i-1] * diff[i] < 0:  # Sign change indicates crossing
        equilibria_idx.append(i)

# Also check if starting point is an equilibrium
if abs(n_actual[0] - n_e[0]) < 1:
    equilibria_idx.insert(0, 0)
if abs(n_actual[-1] - n_e[-1]) < 1:
    equilibria_idx.append(len(n_e) - 1)

# Classify equilibria as stable or unstable
# Stable if slope of response < 1, unstable if > 1
stable_eq = []
unstable_eq = []
for idx in equilibria_idx:
    if idx > 5 and idx < len(n_actual) - 5:
        # Use larger window for slope calculation
        slope = (n_actual[idx+5] - n_actual[idx-5]) / (n_e[idx+5] - n_e[idx-5])
        if slope < 1:
            stable_eq.append(idx)
        else:
            unstable_eq.append(idx)

# Create figure
fig, ax = plt.subplots()

# Plot 45-degree line (fulfilled expectations)
ax.plot(n_e, n_e, 'k--', linewidth=2, label='Fulfilled Expectations ($n^e = n$)', alpha=0.6)

# Plot response function (actual adoption given expectations)
ax.plot(n_e, n_actual, linewidth=3, label='Actual Adoption $R(n^e)$', color=MLBLUE)

# Mark equilibria
for idx in stable_eq:
    ax.plot(n_e[idx], n_actual[idx], 'o', markersize=12, color=MLGREEN,
            markeredgecolor='darkgreen', markeredgewidth=2, zorder=5)
    ax.annotate(f'Stable\n$n^*={n_e[idx]:.0f}$',
                xy=(n_e[idx], n_actual[idx]),
                xytext=(15, -25 if n_e[idx] > 50 else 15),
                textcoords='offset points',
                fontsize=11, color='darkgreen', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=MLGREEN,
                         edgecolor='darkgreen', alpha=0.3),
                arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.5))

for idx in unstable_eq:
    ax.plot(n_e[idx], n_actual[idx], 'o', markersize=12, color=MLRED,
            markeredgecolor='darkred', markeredgewidth=2, zorder=5)
    ax.annotate(f'Unstable\n(Critical Mass)\n$n^*={n_e[idx]:.0f}$',
                xy=(n_e[idx], n_actual[idx]),
                xytext=(20, 15), textcoords='offset points',
                fontsize=10, color='darkred', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor=MLRED,
                         edgecolor='darkred', alpha=0.3),
                arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5))

# Add arrows showing dynamics
# If n_actual > n_e, expectations should rise (arrow right)
# If n_actual < n_e, expectations should fall (arrow left)
arrow_points = [20, 45, 75]
for n_pt in arrow_points:
    idx = np.argmin(np.abs(n_e - n_pt))
    if n_actual[idx] > n_e[idx] + 3:
        ax.annotate('', xy=(n_e[idx] + 8, n_e[idx]), xytext=(n_e[idx], n_e[idx]),
                   arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=2.5))
    elif n_actual[idx] < n_e[idx] - 3:
        ax.annotate('', xy=(n_e[idx] - 8, n_e[idx]), xytext=(n_e[idx], n_e[idx]),
                   arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=2.5))

# Add subsidy arrow: from low stable equilibrium past the unstable equilibrium
if len(stable_eq) >= 1 and len(unstable_eq) >= 1:
    low_stable_idx = stable_eq[0]
    unstable_idx = unstable_eq[0]
    subsidy_start_x = n_e[low_stable_idx]
    subsidy_start_y = n_e[low_stable_idx]  # on the 45-degree line
    subsidy_end_x = n_e[unstable_idx] + 12  # past tipping point
    subsidy_end_y = subsidy_start_y
    ax.annotate('',
                xy=(subsidy_end_x, subsidy_end_y),
                xytext=(subsidy_start_x, subsidy_start_y),
                arrowprops=dict(arrowstyle='->', color=MLGREEN, lw=3, linestyle='--'))
    ax.text((subsidy_start_x + subsidy_end_x) / 2, subsidy_start_y - 6,
            'Subsidy pushes\npast tipping point',
            fontsize=9, color='darkgreen', ha='center', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen',
                     edgecolor=MLGREEN, alpha=0.8))

# Coordination problem annotation -- lower-left to avoid legend overlap
ax.text(0.05, 0.25,
        'Coordination Problem:\n"Penguin Effect" -- Each user waits for\n'
        'others to adopt first, since joining early\n'
        'means paying costs without network benefits.\n'
        'This traps the platform at the low equilibrium.',
        transform=ax.transAxes, fontsize=9.5, verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='lightyellow',
                 edgecolor=MLORANGE, linewidth=2, alpha=0.9))

# Dynamic arrow legend
ax.text(0.72, 0.55,
        'Purple arrows: adoption grows\nOrange arrows: adoption shrinks',
        transform=ax.transAxes, fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                 edgecolor='gray', linewidth=1, alpha=0.9))

# Reading guide box
ax.text(0.62, 0.98,
        'How to read:\n'
        '- Blue above dashed: platform grows\n'
        '- Blue below dashed: platform shrinks\n'
        '- Green dots: stable equilibria\n'
        '- Red dot: tipping point (critical mass)',
        transform=ax.transAxes, fontsize=9, verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcyan',
                 edgecolor=MLBLUE, linewidth=1.5, alpha=0.9))

ax.set_xlabel('Expected Adoption ($n^e$)')
ax.set_ylabel('Actual Adoption ($n$)')
ax.set_title('Platform Adoption: Why Platforms Tip to Success or Failure\n' +
             'Multiple equilibria: same conditions can lead to different outcomes')
ax.legend(loc='lower right', framealpha=0.95)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(0, N_max)
ax.set_ylim(0, N_max)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
