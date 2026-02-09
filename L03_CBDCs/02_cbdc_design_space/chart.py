r"""CBDC Design Space: Multi-Attribute Utility Optimization

Pareto frontier showing tradeoffs between privacy, programmability, accessibility.
Theory: Keeney & Raiffa (1976) - Decisions with Multiple Objectives: Preferences and Value Tradeoffs.

Based on: Auer & Böhme (2020) - The technology of retail central bank digital currency

Economic Model:
    Multi-attribute utility optimization:
    $U = \sum_i w_i \cdot a_i$ subject to $\sum_i a_i \leq C$
    where $a_i \in \{privacy, programmability, accessibility\}$
    and $w_i$ reflects central bank policy preferences.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 12, 'axes.titlesize': 14,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 10,
    'figure.figsize': (14, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'

np.random.seed(42)

# Generate feasible CBDC design points
# Attributes: Privacy (P), Programmability (R), Accessibility (A)
# Constraint: P + R + A <= 2.4 (cannot maximize all three)
n_designs = 300
designs = []
for _ in range(n_designs):
    p = np.random.uniform(0, 1)
    r = np.random.uniform(0, 1)
    a = np.random.uniform(0, 1)
    # Enforce tradeoff constraint
    total = p + r + a
    if total > 2.4:
        scale = 2.4 / total
        p, r, a = p * scale, r * scale, a * scale
    designs.append([p, r, a])

designs = np.array(designs)

# Find Pareto frontier
def is_pareto_efficient(costs):
    """Find Pareto-efficient points (maximize all three attributes)"""
    is_efficient = np.ones(costs.shape[0], dtype=bool)
    for i, c in enumerate(costs):
        if is_efficient[i]:
            # Remove dominated points (all worse or equal in all dimensions)
            is_efficient[is_efficient] = np.any(costs[is_efficient] > c, axis=1)
            is_efficient[i] = True
    return is_efficient

pareto_mask = is_pareto_efficient(designs)
pareto_designs = designs[pareto_mask]
dominated_designs = designs[~pareto_mask]

# Define user preference profiles (weights for utility function)
# U = w_P * u(P) + w_R * u(R) + w_A * u(A)
profiles = {
    'Retail Users': np.array([0.6, 0.2, 0.2]),  # Privacy priority
    'Businesses': np.array([0.2, 0.6, 0.2]),     # Programmability priority
    'Policy Makers': np.array([0.2, 0.2, 0.6])   # Accessibility priority
}

# Find optimal design for each profile
optimal_designs = {}
for name, weights in profiles.items():
    utilities = pareto_designs @ weights
    optimal_idx = np.argmax(utilities)
    optimal_designs[name] = pareto_designs[optimal_idx]

# Specific CBDC examples (approximate attributes)
cbdc_examples = {
    'e-CNY': np.array([0.35, 0.55, 0.75]),    # "Controllable anonymity" = government has full access
    'e-Krona': np.array([0.45, 0.70, 0.80]),  # Lower privacy, high programmability
    'Sand Dollar': np.array([0.50, 0.40, 0.85])  # Moderate privacy, high accessibility
}

# Normalize examples to constraint
for name, attrs in cbdc_examples.items():
    total = attrs.sum()
    if total > 2.4:
        cbdc_examples[name] = attrs * (2.4 / total)

# Create figure with 2 subplots
fig = plt.figure(figsize=(14, 6))

# Left: 3D scatter plot
ax1 = fig.add_subplot(121, projection='3d')

# Plot dominated designs
ax1.scatter(dominated_designs[:, 0], dominated_designs[:, 1], dominated_designs[:, 2],
           c='lightgray', alpha=0.3, s=20, label='Dominated Designs')

# Plot Pareto frontier
ax1.scatter(pareto_designs[:, 0], pareto_designs[:, 1], pareto_designs[:, 2],
           c=MLBLUE, alpha=0.6, s=40, edgecolors='navy', linewidths=0.5,
           label='Pareto Frontier')

# Plot optimal designs for each profile
colors = [MLGREEN, MLORANGE, MLPURPLE]
for (name, design), color in zip(optimal_designs.items(), colors):
    ax1.scatter(design[0], design[1], design[2],
               c=color, s=200, marker='*', edgecolors='black', linewidths=1.5,
               label=f'{name} Optimum', zorder=10)

# Plot CBDC examples
example_colors = {'e-CNY': MLRED, 'e-Krona': '#8B4513', 'Sand Dollar': '#FF1493'}
for name, attrs in cbdc_examples.items():
    ax1.scatter(attrs[0], attrs[1], attrs[2],
               c=example_colors[name], s=150, marker='D', edgecolors='black', linewidths=1,
               label=name, zorder=9)

ax1.set_xlabel('Privacy (P, score 0-1)', fontsize=11, labelpad=8)
ax1.set_ylabel('Programmability (R, score 0-1)', fontsize=11, labelpad=8)
ax1.set_zlabel('Accessibility (A, score 0-1)', fontsize=11, labelpad=8)
ax1.set_title('CBDC Design Space: Multi-Attribute Utility Trade-offs', fontsize=12, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=8, framealpha=0.9)
ax1.view_init(elev=20, azim=45)

# B5: Add annotation for e-CNY balanced design
ecny_attrs = cbdc_examples['e-CNY']
ax1.text(ecny_attrs[0], ecny_attrs[1], ecny_attrs[2] + 0.08,
        'e-CNY:\nBalanced', fontsize=9, ha='center', color=MLRED,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

# Right: 2D projection (Privacy vs Programmability, size = Accessibility)
ax2 = fig.add_subplot(122)

# Plot dominated designs
ax2.scatter(dominated_designs[:, 0], dominated_designs[:, 1],
           s=dominated_designs[:, 2] * 100, c='lightgray', alpha=0.3,
           label='Dominated Designs')

# Plot Pareto frontier
ax2.scatter(pareto_designs[:, 0], pareto_designs[:, 1],
           s=pareto_designs[:, 2] * 150, c=MLBLUE, alpha=0.6,
           edgecolors='navy', linewidths=0.5, label='Pareto Frontier')

# Plot optimal designs
for (name, design), color in zip(optimal_designs.items(), colors):
    ax2.scatter(design[0], design[1], s=design[2] * 400,
               c=color, marker='*', edgecolors='black', linewidths=1.5,
               label=f'{name}', zorder=10)

# Plot CBDC examples
for name, attrs in cbdc_examples.items():
    ax2.scatter(attrs[0], attrs[1], s=attrs[2] * 300,
               c=example_colors[name], marker='D', edgecolors='black', linewidths=1,
               label=name, zorder=9)

# Draw indifference curves (iso-utility lines) for one profile
profile_name = 'Retail Users'
weights = profiles[profile_name]
# Indifference curves: w_P*P + w_R*R = constant (for varying utility levels)
for utility_level in [0.3, 0.5, 0.7]:
    p_range = np.linspace(0, 1, 100)
    r_from_utility = (utility_level - weights[0] * p_range) / weights[1]
    valid = (r_from_utility >= 0) & (r_from_utility <= 1)
    ax2.plot(p_range[valid], r_from_utility[valid], '--', color=MLGREEN,
            alpha=0.5, linewidth=1)

ax2.set_xlabel('Privacy (P)', fontsize=12)
ax2.set_ylabel('Programmability (R)', fontsize=12)
ax2.set_title('2D Projection: Privacy vs Programmability\n(Bubble size = Accessibility)',
             fontsize=12, fontweight='bold')
ax2.legend(loc='upper right', fontsize=8, framealpha=0.9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-0.05, 1.05)
ax2.set_ylim(-0.05, 1.05)

# B5: Add annotation highlighting e-CNY's balanced tradeoffs
ecny_attrs = cbdc_examples['e-CNY']
ax2.annotate('e-CNY:\nBalanced\ntradeoffs',
            xy=(ecny_attrs[0], ecny_attrs[1]), xytext=(ecny_attrs[0] + 0.15, ecny_attrs[1] + 0.15),
            fontsize=9, fontweight='bold', color=MLRED,
            arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

# Add annotation for theory
fig.text(0.5, 0.02,
        'Theory: Keeney & Raiffa (1976) Multi-Attribute Utility Theory | '
        'Constraint: Cannot maximize all three attributes simultaneously',
        ha='center', fontsize=9, style='italic', color='gray')

# Add design dimensions annotation on 3D plot
ax1.text2D(0.02, 0.95,
          'Design Space Constraint:\n'
          'P + R + A ≤ 2.4\n'
          'Pareto frontier shows optimal\n'
          'tradeoffs given stakeholder\n'
          'utility functions',
          transform=ax1.transAxes, fontsize=9,
          verticalalignment='top',
          bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Enhanced CBDC design space chart saved with Pareto frontier and multi-attribute utility optimization")
