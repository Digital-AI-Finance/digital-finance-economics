"""Multi-Platform Market Share: Gibrat Process with Network Effects

Multi-panel chart showing market concentration evolution through stochastic growth.

Economic Model:
  Gibrat with network effects: $S_{i,t+1} = S_i^{1+\gamma} \cdot (1 + \mu + \sigma \varepsilon)$
  where $\gamma > 0$ gives larger platforms a growth advantage.
  Based on Gibrat (1931), Shapiro \& Varian (1999).

# Multi-panel override: comparative statics requires simultaneous visibility

Citation: Gibrat (1931) - Law of Proportionate Effect; Shapiro & Varian (1999)
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

colors = [MLBLUE, MLORANGE, MLGREEN, MLPURPLE, MLRED]
names = ['Platform A', 'Platform B', 'Platform C', 'Platform D', 'Platform E']

# --- Model parameters ---
n_platforms = 5
T = 100
mu = 0.0
sigma = 0.15
gamma = 0.1  # network effect advantage for larger platforms

# Initial shares: equal at 20% each
shares_init = np.ones(n_platforms) / n_platforms

# --- Simulation: S_{i,t+1} = S_i^{1+gamma} * (1 + mu + sigma*eps), then renormalize ---
shares_history = np.zeros((T + 1, n_platforms))
shares_history[0] = shares_init

for t in range(T):
    eps = np.random.normal(0, 1, n_platforms)
    growth = (1 + mu + sigma * eps)
    # Network effect: larger share grows faster (S^(1+gamma))
    new_sizes = shares_history[t] ** (1 + gamma) * growth
    new_sizes = np.maximum(new_sizes, 1e-10)  # floor
    shares_history[t + 1] = new_sizes / new_sizes.sum()

# --- HHI over time ---
hhi_history = np.sum(shares_history ** 2, axis=1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# --- Panel (a): Market share evolution ---
for i in range(n_platforms):
    ax1.plot(range(T + 1), shares_history[:, i] * 100, color=colors[i],
             linewidth=2.5, label=names[i], alpha=0.85)

# Mark the winner at T=100
final_shares = shares_history[-1]
winner_idx = np.argmax(final_shares)
ax1.annotate(f'{names[winner_idx]}: {final_shares[winner_idx]*100:.1f}%',
             xy=(T, final_shares[winner_idx] * 100),
             xytext=(T - 25, final_shares[winner_idx] * 100 + 8),
             fontsize=10, fontweight='bold', color=colors[winner_idx],
             arrowprops=dict(arrowstyle='->', color=colors[winner_idx], lw=2),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=colors[winner_idx], alpha=0.9))

# Mark equal start
ax1.axhline(y=20, color='gray', linestyle=':', alpha=0.5, linewidth=1)
ax1.text(3, 21, 'Equal start (20% each)', fontsize=9, color='gray')

# Tipping point annotation (where divergence becomes clear)
# Find when max share first exceeds 30%
tipping_idx = np.argmax(np.max(shares_history, axis=1) > 0.30)
if tipping_idx > 0:
    ax1.axvline(x=tipping_idx, color=MLPURPLE, linestyle='--', alpha=0.5, linewidth=1.5)
    ax1.text(tipping_idx + 2, 5, f'Tipping\npoint\n(t={tipping_idx})',
             fontsize=9, color=MLPURPLE, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLPURPLE, alpha=0.8))

ax1.set_xlabel('Time Period')
ax1.set_ylabel('Market Share (%)')
ax1.set_title(r'(a) Market Share Evolution ($\gamma$=0.1)')
ax1.legend(loc='upper right', fontsize=9, ncol=2, framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(0, T)
ax1.set_ylim(0, 80)

# Model box
ax1.text(0.02, 0.98,
         r'$S_{i,t+1} = S_i^{1+\gamma}(1+\mu+\sigma\epsilon)$' + '\n'
         r'$\gamma=0.1$, $\mu=0$, $\sigma=0.15$' + '\n'
         'Network effects amplify\nrandom advantages',
         transform=ax1.transAxes, fontsize=9, va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor=MLLAVENDER, alpha=0.3))

# --- Panel (b): HHI evolution with comparison ---
# Also simulate pure Gibrat (gamma=0) for comparison
np.random.seed(42)
shares_pure = np.zeros((T + 1, n_platforms))
shares_pure[0] = shares_init
for t in range(T):
    eps = np.random.normal(0, 1, n_platforms)
    growth = (1 + mu + sigma * eps)
    new_sizes = shares_pure[t] * growth  # no network effect (gamma=0)
    new_sizes = np.maximum(new_sizes, 1e-10)
    shares_pure[t + 1] = new_sizes / new_sizes.sum()
hhi_pure = np.sum(shares_pure ** 2, axis=1)

ax2.plot(range(T + 1), hhi_history, color=MLRED, linewidth=2.5,
         label=r'With network effects ($\gamma$=0.1)')
ax2.plot(range(T + 1), hhi_pure, color=MLBLUE, linewidth=2.5,
         linestyle='--', label=r'Pure Gibrat ($\gamma$=0)')

# HHI thresholds (DOJ/FTC)
ax2.axhline(y=0.25, color='darkred', linestyle=':', alpha=0.6, linewidth=1.5)
ax2.text(5, 0.26, 'Highly concentrated (HHI > 0.25)', fontsize=9,
         color='darkred', alpha=0.8)
ax2.axhline(y=0.15, color=MLORANGE, linestyle=':', alpha=0.6, linewidth=1.5)
ax2.text(5, 0.155, 'Moderately concentrated', fontsize=9,
         color=MLORANGE, alpha=0.8)

# Equal share baseline
ax2.axhline(y=1.0/n_platforms, color='gray', linestyle=':', alpha=0.4, linewidth=1)
ax2.text(T - 30, 1.0/n_platforms + 0.01, 'Equal shares (HHI=0.20)',
         fontsize=8, color='gray')

# Final HHI annotations
ax2.annotate(f'HHI = {hhi_history[-1]:.3f}',
             xy=(T, hhi_history[-1]),
             xytext=(T - 30, hhi_history[-1] + 0.05),
             fontsize=10, fontweight='bold', color=MLRED,
             arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                       edgecolor=MLRED, alpha=0.9))

ax2.set_xlabel('Time Period')
ax2.set_ylabel('Herfindahl-Hirschman Index (HHI)')
ax2.set_title('(b) Concentration: Network Effects Accelerate')
ax2.legend(loc='upper left', fontsize=9, framealpha=0.95)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(0, T)
ax2.set_ylim(0.15, max(hhi_history.max(), 0.5) + 0.05)

# Insight box
ax2.text(0.55, 0.45,
         r'Network effects ($\gamma > 0$)' + '\n'
         'accelerate concentration:\n'
         'larger platforms grow faster,\n'
         'creating winner-take-all',
         transform=ax2.transAxes, fontsize=9, va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
                   edgecolor=MLORANGE, alpha=0.9))

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
