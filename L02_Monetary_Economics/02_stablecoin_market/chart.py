r"""Stablecoin Reserve Dynamics: Bank Run Simulation

Monte Carlo simulation of reserve depletion under stress scenarios.
Based on Diamond & Dybvig (1983) bank run model.

Economic Model:
    Reserve depletion with inflow/outflow:
    $R_{t+1} = R_t \cdot (1 - \max(0, r_{out} - r_{in} + \epsilon_t))$

    Normal regime: $r_{in} = 0.018$, $r_{out} = 0.02$ (net outflow 0.2%/day)
    Panic regime:  $r_{in} = 0$, $r_{out} = 0.12$ (post confidence breach)
    De-peg occurs when $R_t < 0.50$.

Citation: Diamond & Dybvig (1983) - Bank Runs, Deposit Insurance, and Liquidity
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

# Simulation parameters
N_SIMS = 500  # Number of Monte Carlo simulations
T_DAYS = 90   # Simulation horizon in days (extended per D7)
NORMAL_INFLOW_RATE = 0.018     # 1.8% per day inflows (new deposits)
NORMAL_REDEMPTION_RATE = 0.02  # 2% per day outflows (net outflow ~0.2%/day)
PANIC_REDEMPTION_RATE = 0.12   # 12% per day during panic
CONFIDENCE_THRESHOLD = 0.80    # Reserve ratio triggering panic
DEPEG_THRESHOLD = 0.50         # Reserve ratio causing de-peg

def simulate_reserves(initial_reserve_ratio, n_sims=N_SIMS, t_days=T_DAYS):
    """
    Simulate reserve dynamics under Diamond-Dybvig bank run model
    with inflow/outflow dynamics.

    Normal regime: inflow=1.8%/day, outflow=2%/day (net -0.2%/day)
    Panic regime: inflow=0, outflow=12%/day (after confidence breach)

    Returns:
        reserve_ratios: Array of shape (n_sims, t_days+1) with reserve ratios
        depeg_times: Array of de-peg timing for each simulation (NaN if no de-peg)
    """
    reserve_ratios = np.zeros((n_sims, t_days + 1))
    reserve_ratios[:, 0] = initial_reserve_ratio
    depeg_times = np.full(n_sims, np.nan)

    for sim in range(n_sims):
        in_panic = False
        for t in range(t_days):
            current_ratio = reserve_ratios[sim, t]

            # Diamond-Dybvig: Once confidence threshold breached, stay in panic
            if current_ratio < CONFIDENCE_THRESHOLD:
                in_panic = True

            if in_panic:
                # Panic regime: no inflows, high redemption
                inflow_rate = 0.0
                redemption_rate = PANIC_REDEMPTION_RATE
            else:
                # Normal regime: steady inflows and outflows
                inflow_rate = NORMAL_INFLOW_RATE
                redemption_rate = NORMAL_REDEMPTION_RATE

            # Add stochastic noise to net flow
            noise = np.random.normal(0, 0.005)
            net_outflow = max(0, redemption_rate - inflow_rate + noise)

            # Update reserve ratio: R_{t+1} = R_t * (1 - net_outflow)
            new_ratio = current_ratio * (1 - net_outflow)
            reserve_ratios[sim, t + 1] = max(0, new_ratio)

            # Check for de-peg event
            if new_ratio < DEPEG_THRESHOLD and np.isnan(depeg_times[sim]):
                depeg_times[sim] = t + 1

            # Stop simulation if reserves depleted
            if new_ratio <= 0:
                reserve_ratios[sim, t+1:] = 0
                break

    return reserve_ratios, depeg_times

# Run simulations for different initial reserve ratios
scenarios = {
    'Full Reserve (100%)': 1.00,
    'Partial Reserve (85%)': 0.85,
    'Fractional Reserve (70%)': 0.70
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

colors = [MLGREEN, MLBLUE, MLORANGE]
days = np.arange(T_DAYS + 1)

for (label, initial_ratio), color in zip(scenarios.items(), colors):
    reserve_ratios, depeg_times = simulate_reserves(initial_ratio)

    # Calculate statistics
    mean_ratio = np.mean(reserve_ratios, axis=0)
    percentile_5 = np.percentile(reserve_ratios, 5, axis=0)
    percentile_95 = np.percentile(reserve_ratios, 95, axis=0)

    # Plot mean trajectory with confidence bands
    ax1.plot(days, mean_ratio * 100, color=color, linewidth=2.5, label=label)
    ax1.fill_between(days, percentile_5 * 100, percentile_95 * 100,
                     color=color, alpha=0.2)

    # Calculate de-peg probability over time
    depeg_prob = np.zeros(T_DAYS + 1)
    for t in range(T_DAYS + 1):
        depeg_prob[t] = np.mean(depeg_times <= t)

    ax2.plot(days, depeg_prob * 100, color=color, linewidth=2.5, label=label)

# Main plot: Reserve ratio trajectories
ax1.axhline(y=CONFIDENCE_THRESHOLD * 100, color='gray', linestyle='--',
           linewidth=1.5, alpha=0.7, label='Confidence Threshold (80%)')
ax1.axhline(y=DEPEG_THRESHOLD * 100, color=MLRED, linestyle='--',
           linewidth=2, alpha=0.8, label='De-peg Threshold (50%)')

# B5: Add annotation highlighting key data point - fractional reserve rapid depletion
ax1.annotate('Fractional reserve\nrapid depletion',
            xy=(30, 20), xytext=(40, 40),
            fontsize=10, fontweight='bold', color=MLORANGE,
            arrowprops=dict(arrowstyle='->', color=MLORANGE, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLORANGE, alpha=0.8))

ax1.set_xlabel('Days', fontweight='bold')
ax1.set_ylabel('Reserve Ratio (%)', fontweight='bold')
ax1.set_title('Stablecoin Reserve Dynamics Under Bank Run Stress', fontsize=16, fontweight='bold', color=MLPURPLE)
ax1.legend(loc='upper right', framealpha=0.95, fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, T_DAYS)
ax1.set_ylim(0, 105)

# Second plot: De-peg probability
ax2.set_xlabel('Days', fontweight='bold')
ax2.set_ylabel('De-peg Probability (%)', fontweight='bold')
ax2.set_title('Cumulative De-peg Risk Over Simulation Period', fontsize=16, fontweight='bold', color=MLPURPLE)
ax2.legend(loc='upper left', framealpha=0.95, fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, T_DAYS)
ax2.set_ylim(0, 100)

# Add citation
fig.text(0.5, 0.02, 'Based on Diamond & Dybvig (1983) bank run model',
         ha='center', fontsize=10, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
