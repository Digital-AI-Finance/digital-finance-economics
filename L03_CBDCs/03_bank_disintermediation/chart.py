"""Bank Disintermediation: CBDC-Induced Deposit Dynamics

Differential equation model of deposit flight to CBDC.
Theory: Brunnermeier & Niepelt (2019) on CBDC and monetary policy.

Based on: Bindseil (2020) - Tiered CBDC and the financial system
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.integrate import odeint

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10,
    'figure.figsize': (12, 7), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Differential equation model: dD/dt = -alpha*(r_CBDC - r_D)*D + beta*confidence(t)
# D = bank deposits (normalized to 100 at t=0)
# r_CBDC = CBDC interest rate
# r_D = bank deposit rate (assumed constant at 0.5%)
# alpha = sensitivity to rate differential
# beta = confidence restoration parameter

def deposit_dynamics(D, t, r_cbdc, r_deposit, alpha, beta, crisis_start, crisis_duration):
    """
    Deposit flight differential equation.

    Parameters:
    - D: current deposit level (% of initial)
    - t: time (quarters)
    - r_cbdc: CBDC interest rate
    - r_deposit: bank deposit rate
    - alpha: rate sensitivity parameter
    - beta: confidence parameter
    - crisis_start: quarter when crisis begins (if applicable)
    - crisis_duration: length of crisis shock
    """
    # Confidence shock during crisis
    if crisis_start is not None and crisis_start <= t < crisis_start + crisis_duration:
        confidence_shock = -5.0  # Sharp confidence loss
    else:
        confidence_shock = 0.0

    # Rate differential effect (accelerates with lower deposits - bank run dynamics)
    rate_effect = -alpha * (r_cbdc - r_deposit) * D

    # Confidence effect
    confidence_effect = beta * confidence_shock

    dDdt = rate_effect + confidence_effect
    return dDdt

# Time grid: 20 quarters (5 years)
t = np.linspace(0, 20, 200)

# Parameters
r_deposit = 0.005  # 0.5% bank deposit rate
alpha = 0.8  # Rate sensitivity
beta = 1.2  # Confidence sensitivity
D0 = 100.0  # Initial deposits (normalized to 100%)

# Define scenarios
scenarios = [
    {'name': 'A: Low CBDC Rate (0%)', 'r_cbdc': 0.0, 'crisis': None, 'color': MLGREEN, 'style': '-'},
    {'name': 'B: Medium CBDC Rate (1%)', 'r_cbdc': 0.01, 'crisis': None, 'color': MLBLUE, 'style': '-'},
    {'name': 'C: High CBDC Rate (2%)', 'r_cbdc': 0.02, 'crisis': None, 'color': MLORANGE, 'style': '-'},
    {'name': 'D: Crisis + CBDC (1%)', 'r_cbdc': 0.01, 'crisis': 8, 'color': MLRED, 'style': '--'},
]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), height_ratios=[2, 1])

# Main plot: deposit dynamics
for scenario in scenarios:
    crisis_start = scenario['crisis']
    crisis_duration = 3 if crisis_start is not None else 0

    # Solve ODE
    D = odeint(deposit_dynamics, D0, t,
               args=(scenario['r_cbdc'], r_deposit, alpha, beta, crisis_start, crisis_duration))

    ax1.plot(t, D, label=scenario['name'], color=scenario['color'],
             linewidth=2.5, linestyle=scenario['style'])

# Mark tipping point threshold (when deposits fall below 70%, accelerated instability)
tipping_threshold = 70
ax1.axhline(tipping_threshold, color='gray', linestyle=':', linewidth=1.5, alpha=0.7)
ax1.text(19.5, tipping_threshold + 2, 'Tipping Point', ha='right', va='bottom',
         fontsize=10, color='gray', style='italic')

# Mark central bank intervention zone
intervention_time = 12
ax1.axvline(intervention_time, color=MLPURPLE, linestyle='-.', linewidth=1.5, alpha=0.5)
ax1.annotate('CB Intervention:\nRate Ceiling +\nQuantity Limits',
             xy=(intervention_time, 85), xytext=(intervention_time + 1.5, 85),
             fontsize=9, color=MLPURPLE, fontweight='bold',
             arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=1.5))

ax1.set_xlabel('Time (Quarters)', fontweight='bold')
ax1.set_ylabel('Bank Deposits (% of Pre-CBDC Level)', fontweight='bold')
ax1.set_title('Bank Disintermediation Dynamics Induced by CBDC Introduction',
              fontsize=14, fontweight='bold', color=MLPURPLE, pad=15)
ax1.legend(loc='lower left', framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(0, 20)
ax1.set_ylim(0, 105)

# Annotate crisis period for scenario D
crisis_start = 8
crisis_end = crisis_start + 3
ax1.axvspan(crisis_start, crisis_end, alpha=0.1, color=MLRED)
ax1.text((crisis_start + crisis_end) / 2, 5, 'Crisis Period',
         ha='center', fontsize=9, color=MLRED, style='italic')

# Bottom plot: Policy intervention effects
# Simulate two policy interventions
t_policy = np.linspace(0, 20, 200)

# Baseline: High CBDC rate (2%) with no intervention
D_baseline = odeint(deposit_dynamics, D0, t_policy,
                    args=(0.02, r_deposit, alpha, beta, None, 0))

# Policy 1: Rate ceiling at 1% (activated at quarter 12)
def policy_rate_ceiling(t):
    return 0.02 if t < 12 else 0.01

D_ceiling = []
D_current = D0
for i, time in enumerate(t_policy):
    if i == 0:
        D_ceiling.append(D0)
    else:
        dt = t_policy[i] - t_policy[i-1]
        r_cbdc = policy_rate_ceiling(time)
        dD = deposit_dynamics(D_current, time, r_cbdc, r_deposit, alpha, beta, None, 0)
        D_current = D_current + dD * dt
        D_ceiling.append(D_current)
D_ceiling = np.array(D_ceiling)

# Policy 2: Quantity limit (reduces alpha by 50% after quarter 12)
D_quantity = []
D_current = D0
for i, time in enumerate(t_policy):
    if i == 0:
        D_quantity.append(D0)
    else:
        dt = t_policy[i] - t_policy[i-1]
        alpha_adj = alpha * 0.5 if time >= 12 else alpha
        dD = deposit_dynamics(D_current, time, 0.02, r_deposit, alpha_adj, beta, None, 0)
        D_current = D_current + dD * dt
        D_quantity.append(D_current)
D_quantity = np.array(D_quantity)

ax2.plot(t_policy, D_baseline, label='No Intervention', color=MLRED, linewidth=2.5, linestyle='-')
ax2.plot(t_policy, D_ceiling, label='Rate Ceiling (1% cap)', color=MLBLUE, linewidth=2.5, linestyle='--')
ax2.plot(t_policy, D_quantity, label='Quantity Limits', color=MLGREEN, linewidth=2.5, linestyle='-.')

ax2.axvline(intervention_time, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax2.text(intervention_time, 95, 'Policy Activated', ha='center', fontsize=9,
         color='gray', style='italic')

ax2.set_xlabel('Time (Quarters)', fontweight='bold')
ax2.set_ylabel('Deposits (%)', fontweight='bold')
ax2.set_title('Central Bank Policy Interventions: Equilibrium Effects',
              fontsize=12, fontweight='bold', color=MLPURPLE)
ax2.legend(loc='lower left', framealpha=0.95)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(0, 20)
ax2.set_ylim(40, 105)

# Add caption with theoretical reference
fig.text(0.5, -0.02,
         'Theory: Brunnermeier & Niepelt (2019) - CBDC and Private Banks\n'
         'Model: dD/dt = -α(r_CBDC - r_D)D + β·confidence(t) | α=0.8, β=1.2, r_D=0.5%',
         ha='center', fontsize=9, style='italic', color='gray')

# Add disintermediation formula annotation on top panel
ax1.text(0.72, 0.98,
        'Disintermediation Dynamics:\n'
        'dD/dt = -α(rCBDC - rD)D + β·confidence(t)\n\n'
        'Rate differential drives deposit flight\n'
        'Accelerates as bank stability weakens\n'
        'Policy tools: rate ceiling or quantity limits',
        transform=ax1.transAxes, fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
