"""Token Supply Schedule: Vesting Economics

Modeling token unlock schedules and their market impact.
Theory: Token vesting economics and selling pressure dynamics showing cliff-and-linear vesting patterns.

Economic Model:
  Vesting function: $S_i(t) = 0$ for $t < \\text{cliff}_i$
  $S_i(t) = A_i \\cdot (t - \\text{cliff}_i) / T_i$ for $\\text{cliff}_i \\leq t \\leq \\text{cliff}_i + T_i$
  Total circulating supply: $C(t) = \\sum_i S_i(t)$
  Price impact: $P(t) = P(t-1) \\cdot (1 + \\delta)$
  where $\\delta = -0.5 \\cdot (\\text{unlock}_t / \\text{Total}) + \\mu + \\varepsilon$

Citation: Cong et al. (2021) - Tokenomics: Dynamic Adoption and Valuation
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 12, 'axes.titlesize': 14,
    'xtick.labelsize': 11, 'ytick.labelsize': 11, 'legend.fontsize': 10,
    'figure.figsize': (14, 11), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'
MLGRAY = '#7F7F7F'
MLMAGENTA = '#C2185B'  # Distinct color for Team

# Token allocation structure (100M total tokens)
TOTAL_SUPPLY = 100_000_000
ALLOCATIONS = {
    'Team': {'amount': 0.20 * TOTAL_SUPPLY, 'cliff_months': 12, 'vesting_months': 48},
    'Investors': {'amount': 0.25 * TOTAL_SUPPLY, 'cliff_months': 6, 'vesting_months': 24},
    'Advisors': {'amount': 0.05 * TOTAL_SUPPLY, 'cliff_months': 6, 'vesting_months': 18},
    'Community': {'amount': 0.30 * TOTAL_SUPPLY, 'cliff_months': 0, 'vesting_months': 36},
    'Treasury': {'amount': 0.20 * TOTAL_SUPPLY, 'cliff_months': 0, 'vesting_months': 60}
}

# Simulation parameters
months = 60
t_months = np.arange(0, months + 1)


def calculate_vesting_schedule(amount, cliff_months, vesting_months):
    """Calculate cliff + linear vesting schedule"""
    schedule = np.zeros(months + 1)

    if cliff_months >= months:
        return schedule

    # Cliff period: no tokens
    # After cliff: linear release over vesting period
    vesting_start = cliff_months
    vesting_end = min(cliff_months + vesting_months, months)

    if vesting_start < vesting_end:
        # Linear vesting
        monthly_release = amount / vesting_months
        for month in range(vesting_start, vesting_end + 1):
            schedule[month] = monthly_release

    return schedule


# Calculate vesting schedules for each allocation
vesting_schedules = {}
cumulative_schedules = {}
colors = {'Team': MLMAGENTA, 'Investors': MLBLUE, 'Advisors': MLORANGE,
          'Community': MLGREEN, 'Treasury': MLGRAY}

for category, params in ALLOCATIONS.items():
    schedule = calculate_vesting_schedule(
        params['amount'],
        params['cliff_months'],
        params['vesting_months']
    )
    vesting_schedules[category] = schedule
    cumulative_schedules[category] = np.cumsum(schedule)

# Total circulating supply
total_circulating = np.sum([cumulative_schedules[cat] for cat in ALLOCATIONS.keys()], axis=0)

# Simulate price impact from unlock events
# Use moderate impact with mean-reversion so price shows dips but does not flatline
base_price = 10.0
price_trajectory = np.zeros(months + 1)
price_trajectory[0] = base_price
long_run_price = base_price  # mean-reversion anchor grows slowly

for month in range(1, months + 1):
    # Calculate total unlock for this month
    monthly_unlock = sum([vesting_schedules[cat][month] for cat in ALLOCATIONS.keys()])

    # Selling pressure: moderate impact factor
    unlock_pct = monthly_unlock / TOTAL_SUPPLY
    price_impact = -0.03 * unlock_pct * 100  # ~3% drop per 1% of supply unlocked

    # Mean-reversion: price recovers toward slowly-growing anchor
    long_run_price *= 1.005  # 0.5% monthly appreciation of fundamentals
    mean_reversion = 0.05 * (long_run_price - price_trajectory[month - 1]) / price_trajectory[month - 1]

    # Growth trend and noise
    growth_trend = 0.01  # 1% monthly base growth
    noise = np.random.normal(0, 0.025)  # 2.5% volatility

    # Apply price change
    price_change = price_impact + mean_reversion + growth_trend + noise
    price_trajectory[month] = price_trajectory[month - 1] * (1 + price_change)

    # Floor at $1
    price_trajectory[month] = max(price_trajectory[month], 1.0)


# Create figure with subplots
fig = plt.figure(figsize=(14, 11))
fig.suptitle('Tokenomics: From Vesting Schedule to Price Impact',
             fontsize=16, fontweight='bold', y=0.98)
gs = fig.add_gridspec(3, 2, hspace=0.40, wspace=0.3, top=0.93)

# Subplot 1: Vesting schedules (monthly unlock rate)
ax1 = fig.add_subplot(gs[0, :])
for category, schedule in vesting_schedules.items():
    ax1.plot(t_months, schedule / 1e6, linewidth=2, color=colors[category],
             label=category, alpha=0.8)

ax1.set_xlabel('Months Since Launch (months)')
ax1.set_ylabel('Monthly Token Unlock (millions)')
ax1.set_title('(1) Token Vesting Schedule: Monthly Unlock Rate by Category')
ax1.legend(loc='best', fontsize=10, ncol=5)
ax1.grid(True, alpha=0.3, linestyle='--')

# Fix investor cliff annotation: compute actual y-value at month 6
investor_unlock_at_cliff = vesting_schedules['Investors'][6] / 1e6
ax1.annotate('Investor cliff:\nMajor unlock event',
            xy=(6, investor_unlock_at_cliff),
            xytext=(50, -30), textcoords='offset points',
            fontsize=9, fontweight='bold', color=MLBLUE,
            arrowprops=dict(arrowstyle='->', color=MLBLUE, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=MLBLUE, alpha=0.8))

# Mark major cliff events
for category, params in ALLOCATIONS.items():
    cliff = params['cliff_months']
    if 0 < cliff <= months:
        ax1.axvline(cliff, color=colors[category], linestyle=':', alpha=0.4, linewidth=1)
        ax1.text(cliff, ax1.get_ylim()[1] * 0.95, f'{category}\ncliff',
                fontsize=8, ha='center', va='top', color=colors[category])

# Subplot 2: Cumulative circulating supply
ax2 = fig.add_subplot(gs[1, 0])
for category, cum_schedule in cumulative_schedules.items():
    ax2.plot(t_months, cum_schedule / 1e6, linewidth=2, color=colors[category],
             label=category, alpha=0.7)

ax2.plot(t_months, total_circulating / 1e6, linewidth=3, color='black',
         label='Total Circulating', linestyle='--', alpha=0.9)

ax2.set_xlabel('Months Since Launch')
ax2.set_ylabel('Cumulative Tokens (millions)')
ax2.set_title('(2) Circulating Supply Over Time')

# Fix "X months" placeholder
ax2.text(0.02, 0.35, 'Vesting terms:\n- Cliff: No tokens released until\n  e.g., 12 months for Team\n- Linear vesting: Tokens unlock\n  gradually after cliff period',
        transform=ax2.transAxes, fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

ax2.legend(loc='best', fontsize=10)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.axhline(TOTAL_SUPPLY / 1e6, color='red', linestyle=':', alpha=0.3, linewidth=1.5)
ax2.text(months * 0.98, TOTAL_SUPPLY / 1e6 * 1.02, 'Max Supply',
         fontsize=9, ha='right', color='red')

# Subplot 3: Supply distribution pie chart at 24 months
ax3 = fig.add_subplot(gs[1, 1])
mid_month = 24
mid_supply = {cat: cumulative_schedules[cat][mid_month] for cat in ALLOCATIONS.keys()}
unlocked = [mid_supply[cat] for cat in ALLOCATIONS.keys()]
locked_supply = TOTAL_SUPPLY - sum(unlocked)

pie_labels = list(ALLOCATIONS.keys()) + ['Locked']
pie_values = unlocked + [locked_supply]
pie_colors = [colors[cat] for cat in ALLOCATIONS.keys()] + ['#CCCCCC']

wedges, texts, autotexts = ax3.pie(pie_values, labels=pie_labels, colors=pie_colors,
                                     autopct='%1.1f%%', startangle=90,
                                     pctdistance=0.85,
                                     textprops={'fontsize': 9})
# Make percentage text smaller for readability
for t in autotexts:
    t.set_fontsize(8)
ax3.set_title(f'(3) Token Distribution at Month {mid_month}')

# Subplot 4: Price impact simulation
ax4 = fig.add_subplot(gs[2, :])
ax4.plot(t_months, price_trajectory, linewidth=2.5, color=MLRED, label='Token Price')

# Identify major unlock events (>2% of total supply)
major_unlocks = []
for month in range(1, months + 1):
    monthly_unlock = sum([vesting_schedules[cat][month] for cat in ALLOCATIONS.keys()])
    if monthly_unlock / TOTAL_SUPPLY > 0.02:
        major_unlocks.append((month, monthly_unlock, price_trajectory[month]))

# Mark major unlock events
for month, unlock, price in major_unlocks:
    ax4.axvline(month, color=MLRED, linestyle=':', alpha=0.3, linewidth=1)
    ax4.scatter([month], [price], color=MLRED, s=50, zorder=5, alpha=0.7)

ax4.set_xlabel('Months Since Launch')
ax4.set_ylabel('Token Price (USD)')
ax4.set_title('(4) Simulated Price Impact from Token Unlocks')

# Add unlock price explanation
ax4.text(0.5, 0.92, '(Large unlocks create selling pressure, potentially depressing price)',
        transform=ax4.transAxes, fontsize=8, ha='center', style='italic', color='gray')

ax4.legend(loc='best', fontsize=10)
ax4.grid(True, alpha=0.3, linestyle='--')

# Add annotation box explaining the simulation
textstr = 'Price Impact Model:\n\u2022 Unlock pressure: -3% price per 1% supply unlocked\n\u2022 Growth trend: +1% monthly + mean reversion\n\u2022 Volatility: \u00b12.5% random noise'
ax4.text(0.98, 0.05, textstr, transform=ax4.transAxes, fontsize=9,
         verticalalignment='bottom', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

# 4-panel reading guide
fig.text(0.99, 0.96,
         'Read top-to-bottom:\n'
         '(1) When tokens unlock\n'
         '(2) How supply accumulates\n'
         '(3) Distribution at month 24\n'
         '(4) How unlocks affect price',
         fontsize=9, ha='right', va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='lightcyan',
                  edgecolor=MLBLUE, linewidth=1.5, alpha=0.9))

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
