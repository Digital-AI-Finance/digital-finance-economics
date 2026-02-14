r"""Diamond-Dybvig Stablecoin Run Dynamics
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
    Phase dynamics: $\frac{dx}{dt} = -k(R - R_{crit})x(1-x)$
    where $x$ = withdrawal rate, $R$ = reserve ratio.
    Based on Diamond \& Dybvig (1983).

    When $R > R_{crit}$: stable equilibrium at $x=0$ (no run).
    When $R < R_{crit}$: stable equilibrium at $x=1$ (full run).
    Tipping point at $R = R_{crit}$ where both equilibria co-exist.

    Reserve depletion: $\frac{dR}{dt} = -x \cdot \delta$
    where $\delta$ = withdrawal drain rate per unit of $x$.

Citation: Diamond & Dybvig (1983) - Bank Runs, Deposit Insurance, and Liquidity.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.integrate import odeint

np.random.seed(42)

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 10,
    'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# --- Parameters ---
R_crit = 0.80   # Critical reserve ratio
k = 5.0         # Sensitivity parameter
R_init = 0.95   # Initial reserve ratio
x_init = 0.05   # Initial withdrawal fraction
delta = 0.15    # Reserve drain rate per unit withdrawal

# --- Phase dynamics ---
def dxdt(x, R):
    """dx/dt = -k*(R - R_crit)*x*(1-x)"""
    return -k * (R - R_crit) * x * (1.0 - x)

# --- Coupled ODE system for time series ---
def system(state, t):
    x, R = state
    x = np.clip(x, 0.001, 0.999)
    R = np.clip(R, 0.01, 1.0)
    dx = -k * (R - R_crit) * x * (1.0 - x)
    dR = -x * delta  # reserves deplete proportionally to withdrawal rate
    return [dx, dR]

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# === Panel (a): Phase Portrait with Vector Field ===
x_grid = np.linspace(0.01, 0.99, 25)
R_grid = np.linspace(0.50, 1.00, 25)
X, R = np.meshgrid(x_grid, R_grid)

# Vector field
U = -k * (R - R_crit) * X * (1 - X)  # dx/dt
V = -X * delta                         # dR/dt

# Normalize for display
magnitude = np.sqrt(U**2 + V**2)
magnitude[magnitude == 0] = 1
U_norm = U / magnitude
V_norm = V / magnitude

ax1.quiver(X, R, U_norm, V_norm, magnitude, cmap='coolwarm', alpha=0.6,
           scale=35, width=0.004)

# Nullcline: dx/dt = 0 at R = R_crit
ax1.axhline(y=R_crit, color=MLRED, linestyle='--', linewidth=2, alpha=0.8,
            label=f'$R_{{crit}}$ = {R_crit}')

# Nullclines at x=0 and x=1
ax1.axvline(x=0.01, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax1.axvline(x=0.99, color='gray', linestyle=':', linewidth=1, alpha=0.5)

# Plot sample trajectories
t_span = np.linspace(0, 15, 500)
trajectories = [
    (0.05, 0.95, MLGREEN, 'Start: high reserves'),
    (0.05, 0.82, MLBLUE, 'Start: near critical'),
    (0.10, 0.75, MLORANGE, 'Start: below critical'),
    (0.30, 0.70, MLRED, 'Start: stressed'),
]

for x0, R0, color, label in trajectories:
    sol = odeint(system, [x0, R0], t_span)
    x_traj = np.clip(sol[:, 0], 0, 1)
    R_traj = np.clip(sol[:, 1], 0.01, 1)
    ax1.plot(x_traj, R_traj, color=color, linewidth=2.0, label=label, zorder=4)
    ax1.plot(x0, R0, 'o', color=color, markersize=7, zorder=5)
    # Arrow at midpoint
    mid = len(t_span) // 4
    if mid + 1 < len(x_traj):
        dx = x_traj[mid + 1] - x_traj[mid]
        dR = R_traj[mid + 1] - R_traj[mid]
        if abs(dx) + abs(dR) > 1e-6:
            ax1.annotate('', xy=(x_traj[mid + 1], R_traj[mid + 1]),
                        xytext=(x_traj[mid], R_traj[mid]),
                        arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

# Stable/unstable regions
ax1.fill_between([0, 1], R_crit, 1.0, color=MLGREEN, alpha=0.05)
ax1.fill_between([0, 1], 0.5, R_crit, color=MLRED, alpha=0.05)
ax1.text(0.5, 0.92, 'STABLE\n(no run)', ha='center', fontsize=10,
         fontweight='bold', color=MLGREEN, alpha=0.7)
ax1.text(0.5, 0.60, 'UNSTABLE\n(bank run)', ha='center', fontsize=10,
         fontweight='bold', color=MLRED, alpha=0.7)

ax1.set_xlabel('Withdrawal Rate x', fontweight='bold')
ax1.set_ylabel('Reserve Ratio R', fontweight='bold')
ax1.set_title('(a) Phase Portrait: Diamond-Dybvig Dynamics', fontweight='bold', color=MLPURPLE)
ax1.legend(loc='lower left', framealpha=0.9, fontsize=8)
ax1.set_xlim(0, 1)
ax1.set_ylim(0.50, 1.00)
ax1.grid(True, alpha=0.3)

# === Panel (b): UST-style Time Series ===
t_sim = np.linspace(0, 20, 1000)

# Scenario 1: Healthy stablecoin (high initial reserves)
sol_healthy = odeint(system, [0.03, 0.98], t_sim)
# Scenario 2: UST-style collapse
sol_ust = odeint(system, [0.05, 0.85], t_sim)
# Scenario 3: With deposit insurance (capped withdrawal)
def system_insured(state, t):
    x, R = state
    x = np.clip(x, 0.001, 0.999)
    R = np.clip(R, 0.01, 1.0)
    # Insurance: effective R never perceived below R_crit by 0.05 margin
    R_eff = R + 0.10  # Insurance boosts perceived reserves
    dx = -k * (R_eff - R_crit) * x * (1.0 - x)
    dR = -x * delta * 0.5  # Insurance slows outflows
    return [dx, dR]

sol_insured = odeint(system_insured, [0.05, 0.85], t_sim)

ax2_twin = ax2.twinx()

# Plot reserve ratios
ax2.plot(t_sim, np.clip(sol_healthy[:, 1], 0, 1) * 100, color=MLGREEN,
         linewidth=2.2, label='Healthy (R=98%)')
ax2.plot(t_sim, np.clip(sol_ust[:, 1], 0, 1) * 100, color=MLRED,
         linewidth=2.2, label='UST-style (R=85%)')
ax2.plot(t_sim, np.clip(sol_insured[:, 1], 0, 1) * 100, color=MLBLUE,
         linewidth=2.2, linestyle='--', label='Insured (R=85%)')

# Plot withdrawal rates on twin axis
ax2_twin.plot(t_sim, np.clip(sol_ust[:, 0], 0, 1) * 100, color=MLORANGE,
              linewidth=1.5, linestyle=':', alpha=0.8, label='UST withdrawals')

# Critical threshold
ax2.axhline(y=R_crit * 100, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
ax2.text(0.5, R_crit * 100 + 1, f'$R_{{crit}}$ = {R_crit*100:.0f}%', fontsize=9, color='gray')

# Collapse annotation
collapse_idx = np.argmax(sol_ust[:, 1] < R_crit)
if collapse_idx > 0:
    ax2.annotate('Confidence\nbreaches $R_{crit}$',
                 xy=(t_sim[collapse_idx], R_crit * 100),
                 xytext=(t_sim[collapse_idx] + 3, R_crit * 100 + 8),
                 fontsize=9, fontweight='bold', color=MLRED,
                 arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=MLRED, alpha=0.9))

ax2.set_xlabel('Time (periods)', fontweight='bold')
ax2.set_ylabel('Reserve Ratio R (%)', fontweight='bold')
ax2_twin.set_ylabel('Withdrawal Rate x (%)', fontweight='bold', color=MLORANGE)
ax2_twin.tick_params(axis='y', labelcolor=MLORANGE)
ax2.set_title('(b) Stablecoin Run: Time Series', fontweight='bold', color=MLPURPLE)
ax2.legend(loc='upper right', framealpha=0.9, fontsize=9)
ax2_twin.legend(loc='center right', framealpha=0.9, fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 20)
ax2.set_ylim(0, 105)
ax2_twin.set_ylim(0, 105)

fig.suptitle('Diamond-Dybvig Model Applied to Stablecoin Runs',
             fontsize=14, fontweight='bold', color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Diamond-Dybvig stablecoin chart saved to chart.pdf and chart.png")
