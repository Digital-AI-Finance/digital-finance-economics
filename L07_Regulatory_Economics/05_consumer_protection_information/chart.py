r"""Consumer Protection: Akerlof's Market for Lemons

Information asymmetry and market unraveling in crypto/DeFi markets.

Economic Model: Akerlof Adverse Selection with Regulatory Interventions
Economic Formula: $p = v \cdot \bar{q}; \quad \text{seller stays if } c \cdot q_i \leq p$
where:
  - p = Market price (pooling equilibrium)
  - v = Buyer valuation coefficient (v=1.2: buyers value quality 20% above cost)
  - q_bar = Average quality of remaining sellers
  - c = Seller cost coefficient (c=1.0: seller's reservation price equals quality)
  - q_i = Individual project quality (drawn from Uniform[0,1])
  - Market unravels when high-quality sellers (q > p/c) exit, lowering q_bar

Regulatory interventions modeled:
  1. No regulation: pooling equilibrium -> adverse selection spiral
  2. Disclosure: buyers see true q, pay v*q -> separating equilibrium (market survives)
  3. Certification: high-q sellers (q>0.6) get certified at cost 0.05
  4. Minimum standard: ban projects with q < 0.3

Citation: Akerlof (1970) - The Market for Lemons: Quality Uncertainty and the Market Mechanism
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 14, 'axes.labelsize': 12, 'axes.titlesize': 13,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 10,
    'figure.figsize': (14, 9), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'
MLGRAY = '#7F7F7F'

# Akerlof Model Parameters
n_projects = 1000
v = 1.2  # Buyer valuation coefficient
c = 1.0  # Seller cost coefficient
min_standard = 0.3  # Minimum quality standard for regulation

# Initialize quality distribution: q ~ Uniform[0, 1]
quality = np.random.uniform(0, 1, n_projects)

# Store quality distributions for selected rounds
rounds_to_show = [0, 5, 10, 20]
quality_distributions = {}

# === Scenario 1: No Regulation (Market Unraveling) ===
market_size_no_reg = []
avg_quality_no_reg = []
avg_price_no_reg = []
remaining_quality = quality.copy()
quality_distributions['No Reg'] = {0: remaining_quality.copy()}

for t in range(50):
    if len(remaining_quality) == 0:
        market_size_no_reg.append(0)
        avg_quality_no_reg.append(0)
        avg_price_no_reg.append(0)
        continue

    # Buyer offers average quality * v (pooling equilibrium price)
    avg_q = remaining_quality.mean()
    price = avg_q * v

    # Sellers exit if price < quality * c (high-quality sellers leave)
    remaining_quality = remaining_quality[remaining_quality * c <= price]

    market_size_no_reg.append(len(remaining_quality))
    avg_quality_no_reg.append(remaining_quality.mean() if len(remaining_quality) > 0 else 0)
    avg_price_no_reg.append(price)

    if t + 1 in rounds_to_show:
        quality_distributions['No Reg'][t + 1] = remaining_quality.copy()

# === Scenario 2: Disclosure Requirement (Separating Equilibrium) ===
# Buyers see true quality, pay q * v, all sellers stay if v >= c
market_size_disclosure = [n_projects] * 50
avg_quality_disclosure = [quality.mean()] * 50
avg_price_disclosure = [quality.mean() * v] * 50

# === Scenario 3: Third-Party Certification ===
# Certification cost: 0.05, high-quality projects (q > 0.6) certify
cert_cost = 0.05
certified = quality > 0.6
remaining_cert = quality.copy()
market_size_cert = []
avg_quality_cert = []
avg_price_cert = []

for t in range(50):
    if len(remaining_cert) == 0:
        market_size_cert.append(0)
        avg_quality_cert.append(0)
        avg_price_cert.append(0)
        continue

    # Certified projects get true value, uncertified get pooling price
    is_cert = remaining_cert > 0.6
    avg_uncert = remaining_cert[~is_cert].mean() if np.sum(~is_cert) > 0 else 0
    price_uncert = avg_uncert * v

    # Certified sellers stay, uncertified exit if quality too high
    mask = is_cert | (remaining_cert * c <= price_uncert)
    remaining_cert = remaining_cert[mask]

    market_size_cert.append(len(remaining_cert))
    avg_quality_cert.append(remaining_cert.mean() if len(remaining_cert) > 0 else 0)
    avg_price_cert.append(remaining_cert.mean() * v if len(remaining_cert) > 0 else 0)

# === Scenario 4: Minimum Quality Standard ===
# Ban projects with q < min_standard
remaining_std = quality[quality >= min_standard].copy()
market_size_std = []
avg_quality_std = []
avg_price_std = []

for t in range(50):
    if len(remaining_std) == 0:
        market_size_std.append(0)
        avg_quality_std.append(0)
        avg_price_std.append(0)
        continue

    avg_q = remaining_std.mean()
    price = avg_q * v

    remaining_std = remaining_std[remaining_std * c <= price]

    market_size_std.append(len(remaining_std))
    avg_quality_std.append(remaining_std.mean() if len(remaining_std) > 0 else 0)
    avg_price_std.append(price)

# === Visualization ===
fig = plt.figure(figsize=(14, 9))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)

# Main plot: Quality distributions shifting left over rounds
ax_main = fig.add_subplot(gs[0:2, :])
colors_rounds = [MLBLUE, MLORANGE, MLRED, MLPURPLE]
alphas = [0.7, 0.6, 0.5, 0.4]

for idx, round_num in enumerate(rounds_to_show):
    if round_num in quality_distributions['No Reg']:
        q_data = quality_distributions['No Reg'][round_num]
        if len(q_data) > 0:
            ax_main.hist(q_data, bins=30, alpha=alphas[idx], color=colors_rounds[idx],
                        label=f'Round {round_num}' if round_num > 0 else 'Initial',
                        edgecolor='black', linewidth=0.5)

ax_main.set_xlabel('Project Quality (q, score 0-1)')
ax_main.set_ylabel('Number of Projects (count)')
ax_main.set_title('Market Unraveling: Quality Distribution Shifts Left Over Time\n(No Regulation Scenario)',
                  fontweight='bold')
ax_main.legend(loc='upper right')
ax_main.grid(True, alpha=0.3, axis='y')
ax_main.axvline(quality.mean(), color=MLGREEN, linestyle='--', linewidth=2,
               label='Initial Mean', alpha=0.7)

# B5: Add annotation highlighting market failure
initial_mean = quality.mean()
final_mean = avg_quality_no_reg[-1] if avg_quality_no_reg[-1] > 0 else avg_quality_no_reg[30]
ax_main.annotate(f'Quality collapse:\n{initial_mean:.2f} → {final_mean:.2f}',
                xy=(final_mean, 50), xytext=(final_mean + 0.15, 80),
                fontsize=10, fontweight='bold', color=MLRED,
                arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.5),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLRED, alpha=0.8))

# Inset: Average quality and price over rounds
ax_inset = ax_main.inset_axes([0.05, 0.55, 0.35, 0.4])
rounds = np.arange(50)
ax_inset.plot(rounds, avg_quality_no_reg, color=MLRED, linewidth=2, label='Avg Quality')
ax_inset.plot(rounds, [p / v for p in avg_price_no_reg], color=MLBLUE, linewidth=2,
             linestyle='--', label='Buyer Offer/v')
ax_inset.set_xlabel('Round', fontsize=9)
ax_inset.set_ylabel('Quality / Price', fontsize=9)
ax_inset.set_title('Market Failure Trajectory', fontsize=10, fontweight='bold')
ax_inset.legend(fontsize=8, loc='upper right')
ax_inset.grid(True, alpha=0.3)
ax_inset.tick_params(labelsize=8)

# Bottom row: Regulatory interventions comparison
ax1 = fig.add_subplot(gs[2, 0])
ax2 = fig.add_subplot(gs[2, 1])
ax3 = fig.add_subplot(gs[2, 2])

# Plot 1: Market Size
ax1.plot(rounds, market_size_no_reg, color=MLRED, linewidth=2, label='No Regulation')
ax1.plot(rounds, market_size_disclosure, color=MLGREEN, linewidth=2,
        linestyle='--', label='Disclosure')
ax1.plot(rounds, market_size_cert, color=MLBLUE, linewidth=2,
        linestyle='-.', label='Certification')
ax1.plot(rounds, market_size_std, color=MLORANGE, linewidth=2,
        linestyle=':', label=f'Min Std (q≥{min_standard})')
ax1.set_xlabel('Round')
ax1.set_ylabel('Market Size')
ax1.set_title('Market Size Over Time', fontweight='bold')
ax1.legend(fontsize=8, loc='best')
ax1.grid(True, alpha=0.3)

# Plot 2: Average Quality
ax2.plot(rounds, avg_quality_no_reg, color=MLRED, linewidth=2, label='No Regulation')
ax2.plot(rounds, avg_quality_disclosure, color=MLGREEN, linewidth=2,
        linestyle='--', label='Disclosure')
ax2.plot(rounds, avg_quality_cert, color=MLBLUE, linewidth=2,
        linestyle='-.', label='Certification')
ax2.plot(rounds, avg_quality_std, color=MLORANGE, linewidth=2,
        linestyle=':', label=f'Min Std (q≥{min_standard})')
ax2.set_xlabel('Round')
ax2.set_ylabel('Average Quality')
ax2.set_title('Average Quality Over Time', fontweight='bold')
ax2.legend(fontsize=8, loc='best')
ax2.grid(True, alpha=0.3)
ax2.set_ylim(0, 1)

# Plot 3: Average Price
ax3.plot(rounds, [p / v for p in avg_price_no_reg], color=MLRED, linewidth=2,
        label='No Regulation')
ax3.plot(rounds, [p / v for p in avg_price_disclosure], color=MLGREEN, linewidth=2,
        linestyle='--', label='Disclosure')
ax3.plot(rounds, [p / v for p in avg_price_cert], color=MLBLUE, linewidth=2,
        linestyle='-.', label='Certification')
ax3.plot(rounds, [p / v for p in avg_price_std], color=MLORANGE, linewidth=2,
        linestyle=':', label=f'Min Std (q≥{min_standard})')
ax3.set_xlabel('Round')
ax3.set_ylabel('Normalized Price (p/v)')
ax3.set_title('Average Price Over Time', fontweight='bold')
ax3.legend(fontsize=8, loc='best')
ax3.grid(True, alpha=0.3)
ax3.set_ylim(0, 1)

# Overall title with citation
fig.suptitle('Akerlof (1970) Market for Lemons: Regulatory Interventions to Prevent Market Unraveling',
             fontsize=14, fontweight='bold', y=0.98)

# Add educational annotation to main plot
ax_main.text(0.60, 0.30, 'Asymmetric Information:\nE[q|trade] < q̄ → adverse selection\nHigh-q sellers exit when p < c·q',
            transform=ax_main.transAxes, fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
