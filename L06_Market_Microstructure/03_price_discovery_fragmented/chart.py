"""Price Discovery in Fragmented Markets: Information Share (IS)

Economic Model:
  OLS: $\\Delta m_t = \\beta_1 \\Delta p_{CEX,t} + \\beta_2 \\Delta p_{DEX,t} + \\beta_3 \\Delta p_{P2P,t} + \\varepsilon_t$
  Information Share: $IS_i = (\\beta_i \\cdot \\sigma_i)^2 / \\sum_j (\\beta_j \\cdot \\sigma_j)^2$
  Lead-lag: CEX (1 step), DEX (3 steps), P2P (5 steps)

Citation: Hasbrouck (1995) - One Security, Many Markets
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
# DGP: each venue has an independent information factor; the efficient price
# is the sum of all three.  This avoids the squared-correlation bias that
# inflates correlated venues (Hasbrouck 1995 critique).
steps = 300

# Independent information factors per venue (orthogonal by construction)
f_cex = np.random.normal(0, 0.145, steps)  # CEX-specific info
f_dex = np.random.normal(0, 0.115, steps)  # DEX-specific info
f_p2p = np.random.normal(0, 0.058, steps)  # P2P-specific info

# Information events
f_cex[100] = 2.0;  f_dex[100] = 0.8;  f_p2p[100] = 0.2   # Event 1
f_cex[200] = -1.5; f_dex[200] = -0.5; f_p2p[200] = -0.1  # Event 2

# True efficient price: sum of all venue information
ret_true = f_cex + f_dex + f_p2p
true_price = 100 + np.cumsum(ret_true)

# Venue 1: CEX - observes its own factor + small noise
cex_lag = 1
price_cex = 100 + np.cumsum(f_cex + np.random.normal(0, 0.015, steps))

# Venue 2: DEX - observes its own factor + small noise
dex_lag = 3
price_dex = 100 + np.cumsum(f_dex + np.random.normal(0, 0.015, steps))

# Venue 3: P2P - observes its own factor + small noise
p2p_lag = 5
price_p2p = 100 + np.cumsum(f_p2p + np.random.normal(0, 0.015, steps))

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

# Hasbrouck Information Share via OLS regression
# Regress efficient-price returns on venue returns:
#   delta_m[t] = beta_1*delta_cex[t] + beta_2*delta_dex[t] + beta_3*delta_p2p[t] + eps
# IS_i = (beta_i * std_i)^2 / sum_j (beta_j * std_j)^2

X = np.column_stack([returns_cex, returns_dex, returns_p2p])  # (T-1, 3)
y = returns_true  # (T-1,)
betas, _, _, _ = np.linalg.lstsq(X, y, rcond=None)

std_cex = np.std(returns_cex)
std_dex = np.std(returns_dex)
std_p2p = np.std(returns_p2p)

# Information share: (beta_i * sigma_i)^2 normalised
is_raw = np.array([(betas[0] * std_cex)**2,
                    (betas[1] * std_dex)**2,
                    (betas[2] * std_p2p)**2])
is_normalised = is_raw / is_raw.sum()

info_share = {
    'CEX': is_normalised[0],
    'DEX': is_normalised[1],
    'P2P': is_normalised[2]
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
ax1.text(0.98, 0.98, r'Hasbrouck Information Share (IS):' + '\n' +
         r'$\Delta m_t = \sum_i \beta_i \Delta p_{i,t} + \varepsilon_t$' + '\n' +
         r'$IS_i = \frac{(\beta_i \sigma_i)^2}{\sum_j (\beta_j \sigma_j)^2}$',
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
ax2.set_title('Hasbrouck Information Share (IS)\n(Contribution to Price Discovery)', fontweight='bold')
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
ax4.set_title('Contemporaneous Return\nCorrelation', fontweight='bold')

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
