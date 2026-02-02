"""Price Discovery in Fragmented Markets: Information Share

Multi-venue price discovery with Hasbrouck information share calculation.
Theory: Hasbrouck (1995) "One Security, Many Markets: Determining the Contributions to Price Discovery"

Based on: Hasbrouck (1995) - Information Shares
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 14, 'axes.titlesize': 16,
    'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 13,
    'figure.figsize': (14, 10), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'

# Simulate multi-venue trading: CEX (leader), DEX (follower), P2P (noise)
steps = 300
dt = 1.0

# True efficient price: random walk with information shocks
true_price = np.zeros(steps)
true_price[0] = 100.0
for i in range(1, steps):
    shock = 0.0
    if i == 100:  # Information event
        shock = 2.5
    elif i == 200:  # Second information event
        shock = -1.8
    true_price[i] = true_price[i-1] + np.random.normal(0, 0.15) + shock

# Venue 1: CEX - Fast, high volume, leads price discovery
# Observes true price with minimal delay + small noise
cex_lag = 1
cex_noise = 0.08
price_cex = np.zeros(steps)
price_cex[0] = true_price[0]
for i in range(1, steps):
    lag_idx = max(0, i - cex_lag)
    price_cex[i] = true_price[lag_idx] + np.random.normal(0, cex_noise)

# Venue 2: DEX - Slower, smaller volume, follows with delay
# Observes CEX price with lag + moderate noise
dex_lag = 3
dex_noise = 0.25
price_dex = np.zeros(steps)
price_dex[0] = true_price[0]
for i in range(1, steps):
    lag_idx = max(0, i - dex_lag)
    price_dex[i] = price_cex[lag_idx] + np.random.normal(0, dex_noise)

# Venue 3: P2P - Very slow, minimal volume, high noise
# Observes stale prices + high noise (minimal contribution)
p2p_lag = 5
p2p_noise = 0.45
price_p2p = np.zeros(steps)
price_p2p[0] = true_price[0]
for i in range(1, steps):
    lag_idx = max(0, i - p2p_lag)
    price_p2p[i] = price_dex[lag_idx] + np.random.normal(0, p2p_noise)

# Calculate Hasbrouck Information Share
# IS_i = variance contribution of venue i to common efficient price
# Approximate using variance decomposition of price innovations

# Price changes (returns)
returns_cex = np.diff(price_cex)
returns_dex = np.diff(price_dex)
returns_p2p = np.diff(price_p2p)
returns_true = np.diff(true_price)

# Covariance matrix of returns
returns_matrix = np.vstack([returns_cex, returns_dex, returns_p2p])
cov_matrix = np.cov(returns_matrix)

# Correlation with true price innovations (proxy for information contribution)
corr_cex = np.corrcoef(returns_cex, returns_true)[0, 1]
corr_dex = np.corrcoef(returns_dex, returns_true)[0, 1]
corr_p2p = np.corrcoef(returns_p2p, returns_true)[0, 1]

# Information share: squared correlation (variance contribution)
# Normalized to sum to 1
is_cex = corr_cex**2
is_dex = corr_dex**2
is_p2p = corr_p2p**2
total_is = is_cex + is_dex + is_p2p

info_share = {
    'CEX': is_cex / total_is,
    'DEX': is_dex / total_is,
    'P2P': is_p2p / total_is
}

# Identify arbitrage opportunities (price divergence > threshold)
arb_threshold = 1.0
arb_cex_dex = np.abs(price_cex - price_dex)
arb_opportunities = np.where(arb_cex_dex > arb_threshold)[0]

# Create comprehensive figure
fig = plt.figure(figsize=(14, 10))
gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)

# Panel 1: Price series across venues (lead-lag relationship)
ax1 = fig.add_subplot(gs[0, :])
time = np.arange(steps)
ax1.plot(time, true_price, label='True Efficient Price', color='black', linewidth=2, linestyle='--', alpha=0.7)
ax1.plot(time, price_cex, label='CEX (Leader)', color=MLBLUE, linewidth=2, alpha=0.9)
ax1.plot(time, price_dex, label='DEX (Follower)', color=MLGREEN, linewidth=1.5, alpha=0.8)
ax1.plot(time, price_p2p, label='P2P (Noise)', color=MLORANGE, linewidth=1.2, alpha=0.7)

# Mark information shocks
ax1.axvline(x=100, color=MLRED, linestyle=':', alpha=0.5, linewidth=1.5)
ax1.axvline(x=200, color=MLRED, linestyle=':', alpha=0.5, linewidth=1.5)
ax1.text(100, ax1.get_ylim()[1], 'Info Shock', ha='center', va='bottom', fontsize=10, color=MLRED)

ax1.set_xlabel('Time Steps (steps)')
ax1.set_ylabel('Price ($)')
ax1.set_title('Multi-Venue Price Discovery: Lead-Lag Relationships', fontweight='bold')
ax1.legend(loc='upper left', framealpha=0.95)
ax1.grid(alpha=0.3, linestyle='--')

# B5: Add annotation highlighting information shock response
ax1.annotate('Info shock:\nCEX leads response',
            xy=(100, true_price[100]), xytext=(110, true_price[100] + 2),
            fontsize=10, fontweight='bold', color=MLBLUE,
            arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLBLUE, alpha=0.8))

# Add information share formula annotation
ax1.text(0.98, 0.98, r'Hasbrouck Information Share:' + '\n' +
         r'$IS_i = \frac{\text{Cov}(\Delta p_i, \Delta m)^2}{\sum_j \text{Cov}(\Delta p_j, \Delta m)^2}$' + '\n' +
         r'Measures venue contribution to price discovery',
         transform=ax1.transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Panel 2: Information Share by Venue
ax2 = fig.add_subplot(gs[1, 0])
venues = list(info_share.keys())
shares = list(info_share.values())
colors_bar = [MLBLUE, MLGREEN, MLORANGE]

bars = ax2.bar(venues, shares, color=colors_bar, alpha=0.8, edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Information Share')
ax2.set_title('Hasbrouck Information Share\n(Contribution to Price Discovery)', fontweight='bold')
ax2.set_ylim(0, 1)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Add percentage labels on bars
for bar, share in zip(bars, shares):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{share*100:.1f}%',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

# Panel 3: Arbitrage Opportunities (CEX-DEX spread)
ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(time, arb_cex_dex, color=MLPURPLE, linewidth=1.5, alpha=0.8)
ax3.axhline(y=arb_threshold, color=MLRED, linestyle='--', linewidth=2, alpha=0.7, label=f'Arb Threshold (${arb_threshold})')
ax3.fill_between(time, 0, arb_cex_dex, where=(arb_cex_dex > arb_threshold),
                 color=MLRED, alpha=0.2, label='Arb Opportunity')
ax3.set_xlabel('Time Steps')
ax3.set_ylabel('|CEX Price - DEX Price| ($)')
ax3.set_title('Arbitrage Opportunities\n(Price Divergence Between Venues)', fontweight='bold')
ax3.legend(loc='upper right', framealpha=0.95)
ax3.grid(alpha=0.3, linestyle='--')

# Panel 4: Cross-correlation heatmap (lead-lag structure)
ax4 = fig.add_subplot(gs[2, 0])
corr_matrix_full = np.corrcoef([returns_cex, returns_dex, returns_p2p])
im = ax4.imshow(corr_matrix_full, cmap='RdYlBu_r', vmin=-1, vmax=1, aspect='auto')
ax4.set_xticks([0, 1, 2])
ax4.set_yticks([0, 1, 2])
ax4.set_xticklabels(['CEX', 'DEX', 'P2P'])
ax4.set_yticklabels(['CEX', 'DEX', 'P2P'])
ax4.set_title('Return Correlation Matrix\n(Lead-Lag Structure)', fontweight='bold')

# Add correlation values
for i in range(3):
    for j in range(3):
        text_color = 'white' if abs(corr_matrix_full[i, j]) > 0.5 else 'black'
        ax4.text(j, i, f'{corr_matrix_full[i, j]:.2f}',
                ha="center", va="center", color=text_color, fontsize=11, fontweight='bold')

cbar = plt.colorbar(im, ax=ax4, fraction=0.046, pad=0.04)
cbar.set_label('Correlation', rotation=270, labelpad=20)

# Panel 5: Summary statistics
ax5 = fig.add_subplot(gs[2, 1])
ax5.axis('off')

summary_text = f"""
Price Discovery Statistics
{'='*40}

Information Share (Hasbrouck 1995):
  CEX:    {info_share['CEX']*100:.1f}%  (Leader)
  DEX:    {info_share['DEX']*100:.1f}%  (Follower)
  P2P:    {info_share['P2P']*100:.1f}%  (Noise)

Lead-Lag Structure:
  CEX lag:     {cex_lag} step(s)
  DEX lag:     {dex_lag} step(s)
  P2P lag:     {p2p_lag} step(s)

Arbitrage:
  Opportunities: {len(arb_opportunities)} periods
  Avg spread:    ${np.mean(arb_cex_dex):.3f}
  Max spread:    ${np.max(arb_cex_dex):.3f}

Interpretation:
• CEX dominates price discovery (~{info_share['CEX']*100:.0f}%)
• DEX follows with lag, contributes ~{info_share['DEX']*100:.0f}%
• P2P has minimal impact (~{info_share['P2P']*100:.0f}%)
• Arbitrageurs exploit temporary spreads
"""

ax5.text(0.05, 0.95, summary_text, transform=ax5.transAxes,
        fontsize=11, verticalalignment='top', family='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
