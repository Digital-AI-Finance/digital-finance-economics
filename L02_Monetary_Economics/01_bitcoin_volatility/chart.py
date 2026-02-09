r"""Bitcoin Volatility: GARCH(1,1) Simulation

Modeling volatility clustering in cryptocurrency markets.
Theory: Bollerslev (1986) GARCH model.
Reference: Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity.
Journal of Econometrics, 31(3), 307-327.

Based on: Baur & Dimpfl (2018) - Asymmetric volatility in cryptocurrencies

Economic Model:
    GARCH(1,1) conditional variance:
    $\sigma_t^2 = \omega + \alpha \epsilon_{t-1}^2 + \beta \sigma_{t-1}^2$

    Unconditional (long-run) variance:
    $\bar{\sigma}^2 = \frac{\omega}{1 - \alpha - \beta}$

    Stationarity requires $\alpha + \beta < 1$. Higher persistence
    ($\alpha + \beta$ close to 1) produces stronger volatility clustering.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 14,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 11,
    'figure.figsize': (12, 8), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'


def simulate_garch(T, omega, alpha, beta, initial_sigma2=0.0001):
    """
    Simulate GARCH(1,1) process:
    σ²_t = ω + α*ε²_{t-1} + β*σ²_{t-1}
    r_t = σ_t * z_t, where z_t ~ N(0,1)

    Parameters:
        T: number of periods
        omega: constant term (ω)
        alpha: ARCH parameter (α)
        beta: GARCH parameter (β)

    Returns:
        returns, conditional_volatility
    """
    returns = np.zeros(T)
    sigma2 = np.zeros(T)
    sigma2[0] = initial_sigma2

    for t in range(1, T):
        # Standard normal innovation
        z_t = np.random.randn()

        # Conditional variance
        sigma2[t] = omega + alpha * returns[t-1]**2 + beta * sigma2[t-1]

        # Return
        returns[t] = np.sqrt(sigma2[t]) * z_t

    return returns, np.sqrt(sigma2)


# Simulation parameters
T = 1000  # Number of periods

# Bitcoin-like parameters (high persistence, strong clustering)
# ω + α + β should be < 1 for stationarity
# Unconditional variance = omega/(1-alpha-beta) = 0.0001/0.05 = 0.002
omega_btc = 0.0001
alpha_btc = 0.10
beta_btc = 0.85
# Persistence: α + β = 0.95 (very high)

# S&P 500-like parameters (lower persistence)
# Unconditional variance = omega/(1-alpha-beta) = 0.00001/0.04 = 0.00025
omega_sp = 0.00001
alpha_sp = 0.08
beta_sp = 0.88
# Persistence: α + β = 0.96

# Simulate both processes
returns_btc, sigma_btc = simulate_garch(T, omega_btc, alpha_btc, beta_btc)
returns_sp, sigma_sp = simulate_garch(T, omega_sp, alpha_sp, beta_sp)

# Convert to percentage returns
returns_btc_pct = returns_btc * 100
returns_sp_pct = returns_sp * 100
sigma_btc_pct = sigma_btc * 100
sigma_sp_pct = sigma_sp * 100

# Create figure with 2 panels
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Panel 1: Simulated returns showing volatility clustering
ax1.plot(returns_btc_pct, color=MLORANGE, alpha=0.7, linewidth=0.8, label='BTC-like (α=0.10, β=0.85)')
ax1.plot(returns_sp_pct, color=MLBLUE, alpha=0.6, linewidth=0.8, label='S&P500-like (α=0.08, β=0.88)')
ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3, linewidth=0.8)
ax1.fill_between(range(T), -10, 10, color='gray', alpha=0.1, label='±10% zone')
ax1.set_ylabel('Daily Return (%)', fontweight='bold')
ax1.set_title('GARCH(1,1) Simulated Returns: Volatility Clustering in Crypto vs Traditional Assets',
              fontsize=14, fontweight='bold', color=MLPURPLE, pad=10)
fig.text(0.5, 0.94, '(GARCH = Model showing how big price swings tend to cluster together over time)',
         ha='center', fontsize=10, style='italic', color='#555555')
ax1.legend(loc='upper right', framealpha=0.95)
ax1.grid(True, alpha=0.3, axis='y')
ax1.set_ylim(-15, 15)

# Highlight volatility clusters
cluster_regions = [(200, 350), (600, 750)]
for start, end in cluster_regions:
    ax1.axvspan(start, end, color='red', alpha=0.05)

# Panel 2: Conditional volatility over time
ax2.plot(sigma_btc_pct, color=MLORANGE, linewidth=1.5, label='Bitcoin-like volatility', alpha=0.9)
ax2.plot(sigma_sp_pct, color=MLBLUE, linewidth=1.5, label='S&P500-like volatility', alpha=0.8)
ax2.fill_between(range(T), sigma_btc_pct, alpha=0.3, color=MLORANGE)
ax2.fill_between(range(T), sigma_sp_pct, alpha=0.2, color=MLBLUE)

# Add average levels
avg_btc = np.mean(sigma_btc_pct)
avg_sp = np.mean(sigma_sp_pct)
ax2.axhline(y=avg_btc, color=MLORANGE, linestyle='--', alpha=0.5, linewidth=1)
ax2.axhline(y=avg_sp, color=MLBLUE, linestyle='--', alpha=0.5, linewidth=1)
ax2.text(T-50, avg_btc+0.05, f'BTC avg: {avg_btc:.2f}%', color=MLORANGE, fontsize=9, va='bottom')
ax2.text(T-50, avg_sp+0.05, f'S&P avg: {avg_sp:.2f}%', color=MLBLUE, fontsize=9, va='bottom')

ax2.set_xlabel('Time Period', fontweight='bold')
ax2.set_ylabel('Conditional Volatility σₜ (%)', fontweight='bold')
ax2.legend(loc='upper right', framealpha=0.95)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_ylim(0, max(sigma_btc_pct.max(), sigma_sp_pct.max()) * 1.1)

# Highlight same volatility clusters
for start, end in cluster_regions:
    ax2.axvspan(start, end, color='red', alpha=0.05, label='_nolegend_')

# Add annotation about volatility clustering
ax2.annotate('Volatility\nClusters', xy=(275, sigma_btc_pct[275]), xytext=(350, 3.5),
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
            fontsize=10, color='red', fontweight='bold', ha='center')

# Add GARCH formula annotation
ax1.text(0.02, 0.98,
        'GARCH(1,1) Model:\n'
        'σ²ₜ = ω + α·ε²ₜ₋₁ + β·σ²ₜ₋₁\n'
        'where α+β < 1 for stationarity\n'
        'High persistence (α+β ≈ 1) → volatility clustering',
        transform=ax1.transAxes, fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("GARCH(1,1) simulation chart saved to chart.pdf and chart.png")
