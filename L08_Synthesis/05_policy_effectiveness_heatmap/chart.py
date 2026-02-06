r"""Policy Effectiveness: Welfare Analysis Matrix

Quantifying policy impacts across multiple objectives and stakeholders.
Theory: Multi-criteria welfare economics.

Economic Model:
Policy effectiveness as weighted impact:
$E = \sum_i w_i \cdot impact_i$
where w_i are stakeholder weights and impact_i are policy effects.

Citation: Bank for International Settlements (2021) - Policy Framework Analysis
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 11, 'axes.titlesize': 13,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 10,
    'figure.figsize': (10, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Policy matrix (-1 to +1 scale for welfare analysis)
policies = ['CBDC', 'Stablecoin\nRegulation', 'DeFi\nRules',
            'Crypto Tax', 'KYC/AML']
objectives = ['Financial\nInclusion', 'Stability', 'Innovation',
              'Consumer\nProtection']

# Effectiveness scores (normalized to -1 to +1)
effectiveness = np.array([
    [0.8, 0.6, 0.2, 0.5],      # CBDC: High inclusion, good stability
    [0.1, 0.9, -0.4, 0.8],     # Stablecoin Reg: Excellent stability, hinders innovation
    [0.0, 0.5, -0.6, 0.6],     # DeFi Rules: Stability vs innovation tradeoff
    [-0.3, 0.4, -0.5, 0.3],    # Crypto Tax: Revenue but reduces innovation
    [-0.2, 0.7, -0.7, 0.9]     # KYC/AML: Security vs innovation & inclusion
])

# Stakeholder welfare weights (how much each stakeholder values each objective)
# Columns: [Inclusion, Stability, Innovation, Protection]
stakeholder_weights = {
    'Consumers': np.array([0.4, 0.3, 0.1, 0.2]),    # Value inclusion & protection
    'Firms': np.array([0.1, 0.2, 0.5, 0.2]),        # Value innovation most
    'Regulators': np.array([0.2, 0.4, 0.1, 0.3])    # Value stability & protection
}

# Calculate welfare change per policy per stakeholder: ΔW = Σ w_i * Effect_i
welfare_changes = {}
for stakeholder, weights in stakeholder_weights.items():
    welfare_changes[stakeholder] = effectiveness @ weights  # Matrix-vector product

# Total welfare (equal weight across stakeholders for aggregate)
total_welfare = np.mean(list(welfare_changes.values()), axis=0)

# Visualization
fig = plt.figure(figsize=(14, 8))
gs = fig.add_gridspec(1, 3, width_ratios=[3, 1, 0.8], wspace=0.35)

# Main heatmap
ax_heat = fig.add_subplot(gs[0, 0])
im = ax_heat.imshow(effectiveness, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)

ax_heat.set_xticks(np.arange(len(objectives)))
ax_heat.set_yticks(np.arange(len(policies)))
ax_heat.set_xticklabels(objectives)
ax_heat.set_yticklabels(policies)

plt.setp(ax_heat.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

# Annotate cells with effectiveness scores
for i in range(len(policies)):
    for j in range(len(objectives)):
        score = effectiveness[i, j]
        text_str = f'{score:+.1f}'
        color = 'white' if abs(score) > 0.5 else 'black'
        ax_heat.text(j, i, text_str, ha='center', va='center',
                    color=color, fontweight='bold', fontsize=11)

ax_heat.set_title('Policy Effectiveness Matrix\n(Effect on Each Objective)',
                 pad=15, fontweight='bold')
ax_heat.set_xlabel('Policy Objectives (category)', fontweight='bold')
ax_heat.set_ylabel('Policy Instruments (category)', fontweight='bold')
ax_heat.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, color='gray')

# B5: Add annotation highlighting KYC/AML innovation tradeoff
kycaml_idx = policies.index('KYC/AML')
innovation_idx = objectives.index('Innovation')
ax_heat.annotate('Hinders\ninnovation',
                xy=(innovation_idx, kycaml_idx),
                xytext=(innovation_idx + 0.6, kycaml_idx - 0.6),
                fontsize=9, fontweight='bold', color='yellow',
                arrowprops=dict(arrowstyle='->', color='yellow', lw=1.5))

# Add colorbar
cbar = plt.colorbar(im, ax=ax_heat, fraction=0.046, pad=0.04)
cbar.set_label('Effectiveness (score)\n(-1: Harmful, +1: Highly Effective)',
              rotation=270, labelpad=25, fontsize=10)

# Welfare impact panel
ax_welfare = fig.add_subplot(gs[0, 1])
ax_welfare.axis('off')

y_pos = 0.95
ax_welfare.text(0.5, y_pos, 'Welfare Impact (ΔW)',
               ha='center', va='top', fontweight='bold', fontsize=12,
               transform=ax_welfare.transAxes)

y_pos -= 0.08
ax_welfare.text(0.5, y_pos, 'Per Stakeholder',
               ha='center', va='top', fontsize=10, style='italic',
               transform=ax_welfare.transAxes)

y_pos -= 0.12
colors = {'Consumers': MLBLUE, 'Firms': MLORANGE, 'Regulators': MLPURPLE}
bar_width = 0.15
x_positions = np.arange(len(policies))

for idx, policy_idx in enumerate(x_positions):
    y_pos -= 0.12
    policy_name = policies[policy_idx].replace('\n', ' ')
    ax_welfare.text(0.05, y_pos, policy_name,
                   ha='left', va='center', fontweight='bold', fontsize=9,
                   transform=ax_welfare.transAxes)

    y_pos -= 0.04
    for stakeholder, color in colors.items():
        welfare = welfare_changes[stakeholder][policy_idx]
        bar_length = abs(welfare) * 0.35
        x_start = 0.5 if welfare >= 0 else 0.5 - bar_length

        ax_welfare.barh(y_pos, bar_length, left=x_start, height=0.025,
                       color=color, alpha=0.7, transform=ax_welfare.transAxes)

        label = f'{stakeholder[:4]}: {welfare:+.2f}'
        ax_welfare.text(0.87, y_pos, label, ha='right', va='center',
                       fontsize=7, color=color, transform=ax_welfare.transAxes)
        y_pos -= 0.03

# Add legend for stakeholders
ax_legend = fig.add_subplot(gs[0, 2])
ax_legend.axis('off')

legend_y = 0.90
ax_legend.text(0.1, legend_y, 'Stakeholder', ha='left', va='top',
              fontweight='bold', fontsize=10, transform=ax_legend.transAxes)
legend_y -= 0.08
ax_legend.text(0.1, legend_y, 'Preferences', ha='left', va='top',
              fontsize=9, style='italic', transform=ax_legend.transAxes)

legend_y -= 0.12
for stakeholder, color in colors.items():
    ax_legend.add_patch(plt.Rectangle((0.1, legend_y - 0.02), 0.08, 0.03,
                                     color=color, alpha=0.7,
                                     transform=ax_legend.transAxes))
    ax_legend.text(0.22, legend_y, stakeholder, ha='left', va='center',
                  fontsize=9, transform=ax_legend.transAxes)

    legend_y -= 0.08
    weights = stakeholder_weights[stakeholder]
    obj_labels = ['Inc', 'Stab', 'Innov', 'Prot']
    weight_str = ', '.join([f'{obj_labels[i]}:{weights[i]:.1f}'
                           for i in range(len(weights))])
    ax_legend.text(0.12, legend_y, f'w={weight_str}', ha='left', va='center',
                  fontsize=7, style='italic', transform=ax_legend.transAxes)
    legend_y -= 0.12

# Add tradeoff annotations
legend_y -= 0.05
ax_legend.text(0.1, legend_y, 'Key Tradeoffs:', ha='left', va='top',
              fontweight='bold', fontsize=9, transform=ax_legend.transAxes)
legend_y -= 0.08
tradeoffs = [
    'KYC/AML:\nSecurity vs\nInnovation',
    'Stablecoin:\nStability vs\nFlexibility',
    'DeFi Rules:\nProtection vs\nPermissionless'
]
for tradeoff in tradeoffs:
    ax_legend.text(0.12, legend_y, tradeoff, ha='left', va='top',
                  fontsize=7, style='italic', color=MLRED,
                  transform=ax_legend.transAxes)
    legend_y -= 0.14

plt.suptitle('Policy Effectiveness & Welfare Analysis: Multi-Stakeholder Perspective',
            fontsize=14, fontweight='bold', y=0.98)

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
