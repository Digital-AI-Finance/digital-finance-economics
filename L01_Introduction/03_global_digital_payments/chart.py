"""Global Digital Payments: Econometric Growth Projection

Monte Carlo simulation with confidence intervals for payment market growth.
Models: Exponential growth Y(t) = Y0 * (1 + g)^t and logistic saturation.

Based on: McKinsey (2022) - Global Payments Report, digital payments growth trends
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy.optimize import curve_fit

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

# Historical data: global digital payments (trillion USD)
hist_years = np.array([2015, 2018, 2020, 2022, 2024])
hist_values = np.array([3.0, 4.5, 5.5, 7.0, 9.0])

# Calculate CAGR from historical data
n_years = hist_years[-1] - hist_years[0]
cagr = (hist_values[-1] / hist_values[0]) ** (1 / n_years) - 1

print(f"Historical CAGR: {cagr*100:.2f}%")

# Exponential growth model: Y(t) = Y0 * (1 + g)^t
def exponential_growth(t, Y0, g):
    return Y0 * (1 + g) ** (t - hist_years[0])

# Logistic saturation model: Y(t) = K / (1 + exp(-r(t-t0)))
def logistic_growth(t, K, r, t0):
    return K / (1 + np.exp(-r * (t - t0)))

# Fit exponential model
popt_exp, _ = curve_fit(exponential_growth, hist_years, hist_values,
                         p0=[hist_values[0], cagr])
Y0_fit, g_fit = popt_exp

# Fit logistic model with generous bounds
popt_log, _ = curve_fit(logistic_growth, hist_years, hist_values,
                         p0=[20, 0.2, 2020],
                         bounds=([15, 0.05, 2015], [50, 0.5, 2025]))
K_fit, r_fit, t0_fit = popt_log

print(f"Fitted exponential: Y0={Y0_fit:.2f}T, g={g_fit*100:.2f}%")
print(f"Fitted logistic: K={K_fit:.2f}T, r={r_fit:.3f}, t0={t0_fit:.1f}")

# Monte Carlo simulation
N_SIMS = 1000
projection_years = np.arange(2015, 2031)
n_proj = len(projection_years)

# Estimate standard deviation of growth rate from residuals
residuals = hist_values - exponential_growth(hist_years, Y0_fit, g_fit)
sigma_g = 0.015  # ~1.5% std dev in growth rate

# Run simulations
simulations = np.zeros((N_SIMS, n_proj))

for i in range(N_SIMS):
    # Stochastic growth rate: g ~ N(g_fit, sigma_g)
    g_sim = np.random.normal(g_fit, sigma_g)

    # Add small noise term
    noise = np.random.normal(0, 0.15, n_proj)

    simulations[i, :] = exponential_growth(projection_years, Y0_fit, g_sim) + noise

# Calculate confidence intervals
ci_90_lower = np.percentile(simulations, 5, axis=0)
ci_90_upper = np.percentile(simulations, 95, axis=0)
ci_95_lower = np.percentile(simulations, 2.5, axis=0)
ci_95_upper = np.percentile(simulations, 97.5, axis=0)
median_projection = np.median(simulations, axis=0)

# Deterministic projections for comparison
exp_projection = exponential_growth(projection_years, Y0_fit, g_fit)
log_projection = logistic_growth(projection_years, K_fit, r_fit, t0_fit)

# Visualization
fig, ax = plt.subplots(figsize=(12, 7))

# 95% CI band (lighter)
ax.fill_between(projection_years, ci_95_lower, ci_95_upper,
                alpha=0.15, color=MLPURPLE, label='95% Confidence Interval')

# 90% CI band (darker)
ax.fill_between(projection_years, ci_90_lower, ci_90_upper,
                alpha=0.25, color=MLPURPLE, label='90% Confidence Interval')

# Historical data points
ax.scatter(hist_years, hist_values, s=120, color=MLRED, zorder=5,
           edgecolors='black', linewidths=1.5, label='Historical Data')

# Fitted trend line (median of simulations)
ax.plot(projection_years, median_projection, color=MLPURPLE,
        linewidth=3, label='Exponential Trend (Monte Carlo Median)', zorder=4)

# Logistic projection for comparison
ax.plot(projection_years, log_projection, '--', color=MLGREEN,
        linewidth=2.5, label='Logistic Saturation Model', alpha=0.8)

# Mark projection region
ax.axvline(x=2024, color='gray', linestyle=':', alpha=0.6, linewidth=2)
ax.text(2024.5, 18.5, 'Projection →', fontsize=12, color='gray',
        style='italic', fontweight='bold')

# CAGR annotation
textstr = f'Historical CAGR: {cagr*100:.1f}%\nFitted Growth: {g_fit*100:.1f}%'
ax.text(0.03, 0.97, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=dict(boxstyle='round',
        facecolor='wheat', alpha=0.8))

# 2030 projection annotation
proj_2030 = median_projection[-1]
ci90_range_2030 = ci_90_upper[-1] - ci_90_lower[-1]
ax.annotate(f'2030: ${proj_2030:.1f}T\n±${ci90_range_2030/2:.1f}T (90% CI)',
            xy=(2030, proj_2030), xytext=(2027.5, proj_2030 + 3),
            fontsize=11, ha='center',
            arrowprops=dict(arrowstyle='->', color=MLPURPLE, lw=2),
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9,
                     edgecolor=MLPURPLE, linewidth=2))

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Global Digital Payments (Trillion USD)', fontweight='bold')
ax.set_title('Global Digital Payments: Econometric Growth Projection with Uncertainty',
             fontsize=16, fontweight='bold', color=MLPURPLE, pad=15)

ax.legend(loc='upper left', framealpha=0.95, fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(2014.5, 2030.5)
ax.set_ylim(0, 22)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
