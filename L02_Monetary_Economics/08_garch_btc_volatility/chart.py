r"""GARCH(1,1) BTC vs S&P 500 Volatility Comparison
# Multi-panel override: comparative statics requires simultaneous visibility

Economic Model:
    GARCH(1,1): $\sigma_t^2 = \omega + \alpha\epsilon_{t-1}^2 + \beta\sigma_{t-1}^2$.
    BTC: $\omega=10^{-5}$, $\alpha=0.10$, $\beta=0.85$.
    S\&P: $\omega=2\times10^{-6}$, $\alpha=0.08$, $\beta=0.88$.
    Based on Bollerslev (1986).

    Unconditional variance: $\bar{\sigma}^2 = \frac{\omega}{1-\alpha-\beta}$
    BTC: $\bar{\sigma}^2 = 10^{-5}/0.05 = 2\times10^{-4}$, annualized $\approx 22.4\%$
    S&P: $\bar{\sigma}^2 = 2\times10^{-6}/0.04 = 5\times10^{-5}$, annualized $\approx 11.2\%$
    Stationarity: $\alpha + \beta < 1$

Citation: Bollerslev (1986), Engle (1982).
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

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
T = 1000  # Number of periods

# BTC GARCH(1,1)
omega_btc = 1e-5
alpha_btc = 0.10
beta_btc = 0.85
# Persistence: 0.95, Unconditional var: 1e-5/0.05 = 2e-4
# Unconditional vol (daily): sqrt(2e-4) = 0.01414, annualized: 0.01414*sqrt(252) = 22.4%

# S&P 500 GARCH(1,1)
omega_sp = 2e-6
alpha_sp = 0.08
beta_sp = 0.88
# Persistence: 0.96, Unconditional var: 2e-6/0.04 = 5e-5
# Unconditional vol (daily): sqrt(5e-5) = 0.00707, annualized: 0.00707*sqrt(252) = 11.2%

def simulate_garch(T, omega, alpha, beta):
    """Simulate GARCH(1,1): sigma_t^2 = omega + alpha*eps_{t-1}^2 + beta*sigma_{t-1}^2"""
    sigma2 = np.zeros(T)
    eps = np.zeros(T)
    z = np.random.randn(T)

    # Initialize at unconditional variance
    sigma2[0] = omega / (1.0 - alpha - beta)
    eps[0] = np.sqrt(sigma2[0]) * z[0]

    for t in range(1, T):
        sigma2[t] = omega + alpha * eps[t-1]**2 + beta * sigma2[t-1]
        eps[t] = np.sqrt(sigma2[t]) * z[t]

    sigma_daily = np.sqrt(sigma2)
    sigma_annual = sigma_daily * np.sqrt(252) * 100  # annualized %
    return eps, sigma_daily, sigma_annual

eps_btc, sig_d_btc, sig_a_btc = simulate_garch(T, omega_btc, alpha_btc, beta_btc)
eps_sp, sig_d_sp, sig_a_sp = simulate_garch(T, omega_sp, alpha_sp, beta_sp)

# --- Figure: 1x2 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

# === Panel (a): Conditional Volatility Paths (annualized) ===
ax1.plot(sig_a_btc, color=MLORANGE, linewidth=1.2, alpha=0.85, label='BTC GARCH(1,1)')
ax1.plot(sig_a_sp, color=MLBLUE, linewidth=1.2, alpha=0.85, label='S&P 500 GARCH(1,1)')

ax1.fill_between(range(T), sig_a_btc, alpha=0.15, color=MLORANGE)
ax1.fill_between(range(T), sig_a_sp, alpha=0.15, color=MLBLUE)

# Unconditional levels
uncond_btc = np.sqrt(omega_btc / (1 - alpha_btc - beta_btc)) * np.sqrt(252) * 100
uncond_sp = np.sqrt(omega_sp / (1 - alpha_sp - beta_sp)) * np.sqrt(252) * 100

ax1.axhline(y=uncond_btc, color=MLORANGE, linestyle='--', linewidth=1.5, alpha=0.6)
ax1.axhline(y=uncond_sp, color=MLBLUE, linestyle='--', linewidth=1.5, alpha=0.6)

ax1.text(T - 5, uncond_btc + 1, f'BTC long-run: {uncond_btc:.1f}%',
         fontsize=9, color=MLORANGE, ha='right', fontweight='bold')
ax1.text(T - 5, uncond_sp + 1, f'S&P long-run: {uncond_sp:.1f}%',
         fontsize=9, color=MLBLUE, ha='right', fontweight='bold')

# UoA viability threshold
ax1.axhline(y=5.0, color=MLGREEN, linestyle=':', linewidth=1.5, alpha=0.7)
ax1.text(10, 5.5, 'UoA viability threshold (~5%)', fontsize=9, color=MLGREEN, fontweight='bold')

# Highlight volatility spike region
spike_idx = np.argmax(sig_a_btc)
ax1.annotate('Volatility spike',
             xy=(spike_idx, sig_a_btc[spike_idx]),
             xytext=(spike_idx + 80, sig_a_btc[spike_idx] + 10),
             fontsize=9, fontweight='bold', color=MLRED,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=MLRED, alpha=0.9))

ax1.set_xlabel('Trading Day', fontweight='bold')
ax1.set_ylabel('Annualized Volatility (%)', fontweight='bold')
ax1.set_title('(a) Conditional Volatility Paths', fontweight='bold', color=MLPURPLE)
ax1.legend(loc='upper right', framealpha=0.9, fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, T)

# === Panel (b): Volatility Distribution (Histograms) ===
bins = np.linspace(0, max(sig_a_btc.max(), sig_a_sp.max()) * 1.05, 60)

ax2.hist(sig_a_btc, bins=bins, color=MLORANGE, alpha=0.55, density=True,
         edgecolor='white', linewidth=0.5, label=f'BTC (mean={np.mean(sig_a_btc):.1f}%)')
ax2.hist(sig_a_sp, bins=bins, color=MLBLUE, alpha=0.55, density=True,
         edgecolor='white', linewidth=0.5, label=f'S&P (mean={np.mean(sig_a_sp):.1f}%)')

# Vertical lines at means
ax2.axvline(x=np.mean(sig_a_btc), color=MLORANGE, linestyle='--', linewidth=2, alpha=0.8)
ax2.axvline(x=np.mean(sig_a_sp), color=MLBLUE, linestyle='--', linewidth=2, alpha=0.8)

# UoA threshold
ax2.axvline(x=5.0, color=MLGREEN, linestyle=':', linewidth=2, alpha=0.7)
ax2.text(5.5, ax2.get_ylim()[1] * 0.1 if ax2.get_ylim()[1] > 0 else 0.01,
         'UoA\nviable', fontsize=9, color=MLGREEN, fontweight='bold')

# Add GARCH parameter box
param_text = (
    'GARCH(1,1) Parameters:\n'
    f'BTC: $\\omega$={omega_btc:.0e}, $\\alpha$={alpha_btc}, $\\beta$={beta_btc}\n'
    f'S&P: $\\omega$={omega_sp:.0e}, $\\alpha$={alpha_sp}, $\\beta$={beta_sp}\n'
    f'Stationarity: $\\alpha+\\beta$ < 1'
)
ax2.text(0.97, 0.97, param_text, transform=ax2.transAxes, fontsize=8,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.4', facecolor=MLLAVENDER, alpha=0.3))

ax2.set_xlabel('Annualized Volatility (%)', fontweight='bold')
ax2.set_ylabel('Density', fontweight='bold')
ax2.set_title('(b) Volatility Distribution', fontweight='bold', color=MLPURPLE)
ax2.legend(loc='upper right', framealpha=0.9, fontsize=9)
ax2.grid(True, alpha=0.3, axis='y')

fig.suptitle('GARCH(1,1) Volatility: Bitcoin vs S&P 500',
             fontsize=14, fontweight='bold', color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("GARCH BTC vs S&P volatility chart saved to chart.pdf and chart.png")
