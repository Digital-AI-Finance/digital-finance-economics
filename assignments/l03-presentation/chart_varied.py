r"""Bank Disintermediation: CBDC Variations

Explores sensitivity of deposit dynamics to policy parameters.

Economic Model: $\frac{dD}{dt} = -\alpha(r_{CBDC} - r_D)D + \beta \cdot confidence(t)$

Variations:
1. Baseline (α=0.8, original scenarios)
2. High rate sensitivity (α=2.0)
3. Zero CBDC rate (all r_CBDC=0%)
4. Early crisis (crisis starts quarter 2 instead of 8)
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.integrate import odeint

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

    # Rate differential effect
    rate_effect = -alpha * (r_cbdc - r_deposit) * D

    # Confidence effect
    confidence_effect = beta * confidence_shock

    dDdt = rate_effect + confidence_effect
    return dDdt

# Time grid: 20 quarters (5 years)
t = np.linspace(0, 20, 200)

# Base parameters
r_deposit = 0.005  # 0.5% bank deposit rate
alpha_base = 0.8  # Base rate sensitivity
beta = 1.2  # Confidence sensitivity
D0 = 100.0  # Initial deposits (normalized to 100%)

# Define scenarios
scenarios_base = [
    {'name': 'A: 0% CBDC', 'r_cbdc': 0.0, 'crisis': None, 'color': MLGREEN, 'style': '-'},
    {'name': 'B: 1% CBDC', 'r_cbdc': 0.01, 'crisis': None, 'color': MLBLUE, 'style': '-'},
    {'name': 'C: 2% CBDC', 'r_cbdc': 0.02, 'crisis': None, 'color': MLORANGE, 'style': '-'},
    {'name': 'D: Crisis+1%', 'r_cbdc': 0.01, 'crisis': 8, 'color': MLRED, 'style': '--'},
]

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Panel 1: BASELINE (α=0.8, original scenarios)
for scenario in scenarios_base:
    crisis_start = scenario['crisis']
    crisis_duration = 3 if crisis_start is not None else 0

    D = odeint(deposit_dynamics, D0, t,
               args=(scenario['r_cbdc'], r_deposit, alpha_base, beta, crisis_start, crisis_duration))

    ax1.plot(t, D, label=scenario['name'], color=scenario['color'],
             linewidth=2.5, linestyle=scenario['style'])

ax1.axhline(70, color='gray', linestyle=':', linewidth=1, alpha=0.7)
ax1.text(19.5, 72, 'Tipping Point', ha='right', fontsize=9, color='gray', style='italic')
ax1.set_xlabel('Time (Quarters)', fontweight='bold')
ax1.set_ylabel('Bank Deposits (% of Initial)', fontweight='bold')
ax1.set_title('Panel 1: BASELINE (α=0.8, original scenarios)', fontsize=12, fontweight='bold', color=MLPURPLE)
ax1.legend(loc='lower left', framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(0, 20)
ax1.set_ylim(0, 105)

# Panel 2: VARIATION 1 — High rate sensitivity (α=2.0)
alpha_high = 2.0
for scenario in scenarios_base:
    crisis_start = scenario['crisis']
    crisis_duration = 3 if crisis_start is not None else 0

    D = odeint(deposit_dynamics, D0, t,
               args=(scenario['r_cbdc'], r_deposit, alpha_high, beta, crisis_start, crisis_duration))

    ax2.plot(t, D, label=scenario['name'], color=scenario['color'],
             linewidth=2.5, linestyle=scenario['style'])

ax2.axhline(70, color='gray', linestyle=':', linewidth=1, alpha=0.7)
ax2.text(19.5, 72, 'Tipping Point', ha='right', fontsize=9, color='gray', style='italic')
ax2.set_xlabel('Time (Quarters)', fontweight='bold')
ax2.set_ylabel('Bank Deposits (% of Initial)', fontweight='bold')
ax2.set_title('Panel 2: VARIATION 1 — High Rate Sensitivity (α=2.0)', fontsize=12, fontweight='bold', color=MLPURPLE)
ax2.legend(loc='lower left', framealpha=0.95)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(0, 20)
ax2.set_ylim(0, 105)

# Panel 3: VARIATION 2 — All CBDC rates set to 0%
scenarios_zero = [
    {'name': 'A: 0% CBDC', 'r_cbdc': 0.0, 'crisis': None, 'color': MLGREEN, 'style': '-'},
    {'name': 'B: 0% CBDC', 'r_cbdc': 0.0, 'crisis': None, 'color': MLBLUE, 'style': '-'},
    {'name': 'C: 0% CBDC', 'r_cbdc': 0.0, 'crisis': None, 'color': MLORANGE, 'style': '-'},
    {'name': 'D: Crisis+0%', 'r_cbdc': 0.0, 'crisis': 8, 'color': MLRED, 'style': '--'},
]

for scenario in scenarios_zero:
    crisis_start = scenario['crisis']
    crisis_duration = 3 if crisis_start is not None else 0

    D = odeint(deposit_dynamics, D0, t,
               args=(scenario['r_cbdc'], r_deposit, alpha_base, beta, crisis_start, crisis_duration))

    ax3.plot(t, D, label=scenario['name'], color=scenario['color'],
             linewidth=2.5, linestyle=scenario['style'])

ax3.axhline(70, color='gray', linestyle=':', linewidth=1, alpha=0.7)
ax3.text(19.5, 72, 'Tipping Point', ha='right', fontsize=9, color='gray', style='italic')
ax3.set_xlabel('Time (Quarters)', fontweight='bold')
ax3.set_ylabel('Bank Deposits (% of Initial)', fontweight='bold')
ax3.set_title('Panel 3: VARIATION 2 — Zero CBDC Rate (all r_CBDC=0%)', fontsize=12, fontweight='bold', color=MLPURPLE)
ax3.legend(loc='lower left', framealpha=0.95)
ax3.grid(True, alpha=0.3, linestyle='--')
ax3.set_xlim(0, 20)
ax3.set_ylim(0, 105)

# Panel 4: VARIATION 3 — Early crisis (quarter 2 instead of 8)
scenarios_early = [
    {'name': 'A: 0% CBDC', 'r_cbdc': 0.0, 'crisis': None, 'color': MLGREEN, 'style': '-'},
    {'name': 'B: 1% CBDC', 'r_cbdc': 0.01, 'crisis': None, 'color': MLBLUE, 'style': '-'},
    {'name': 'C: 2% CBDC', 'r_cbdc': 0.02, 'crisis': None, 'color': MLORANGE, 'style': '-'},
    {'name': 'D: Crisis+1% (Q2)', 'r_cbdc': 0.01, 'crisis': 2, 'color': MLRED, 'style': '--'},
]

for scenario in scenarios_early:
    crisis_start = scenario['crisis']
    crisis_duration = 3 if crisis_start is not None else 0

    D = odeint(deposit_dynamics, D0, t,
               args=(scenario['r_cbdc'], r_deposit, alpha_base, beta, crisis_start, crisis_duration))

    ax4.plot(t, D, label=scenario['name'], color=scenario['color'],
             linewidth=2.5, linestyle=scenario['style'])

# Highlight early crisis period
ax4.axvspan(2, 5, alpha=0.1, color=MLRED)
ax4.text(3.5, 5, 'Crisis (Q2-Q5)', ha='center', fontsize=9, color=MLRED, style='italic')

ax4.axhline(70, color='gray', linestyle=':', linewidth=1, alpha=0.7)
ax4.text(19.5, 72, 'Tipping Point', ha='right', fontsize=9, color='gray', style='italic')
ax4.set_xlabel('Time (Quarters)', fontweight='bold')
ax4.set_ylabel('Bank Deposits (% of Initial)', fontweight='bold')
ax4.set_title('Panel 4: VARIATION 3 — Early Crisis (quarter 2 instead of 8)', fontsize=12, fontweight='bold', color=MLPURPLE)
ax4.legend(loc='lower left', framealpha=0.95)
ax4.grid(True, alpha=0.3, linestyle='--')
ax4.set_xlim(0, 20)
ax4.set_ylim(0, 105)

# Add overall caption
fig.text(0.5, 0.01,
         'Model: dD/dt = -α(r_CBDC - r_D)D + β·confidence(t) | Base parameters: α=0.8, β=1.2, r_D=0.5%\n'
         'Source: Brunnermeier & Niepelt (2019) - On the Equivalence of Private and Public Money',
         ha='center', fontsize=9, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(Path(__file__).parent / 'chart_varied.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart_varied.png', dpi=150, bbox_inches='tight')
plt.close()
print("Variation chart saved to chart_varied.pdf and chart_varied.png")
