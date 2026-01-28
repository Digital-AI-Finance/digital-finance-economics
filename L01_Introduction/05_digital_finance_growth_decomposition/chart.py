"""Digital Finance Growth Decomposition - Extensive vs Intensive Margin Analysis"""
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

# Time series: 2010-2035
years = np.arange(2010, 2036)
t = years - 2010

# Extensive margin: users (logistic S-curve)
L_users = 3e9  # 3 billion users asymptote
k_users = 0.3
t0_users = 10  # inflection at 2020
users = L_users / (1 + np.exp(-k_users * (t - t0_users)))

# Intensive margin: transactions per user per year (logistic)
L_txns = 200  # 200 txns/user/year asymptote
k_txns = 0.25
t0_txns = 15  # inflection at 2025
txns_per_user = L_txns / (1 + np.exp(-k_txns * (t - t0_txns)))

# Total volume
total_volume = users * txns_per_user / 1e9  # in billions of transactions

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Top subplot: Two margins
ax1_right = ax1.twinx()

# Plot extensive margin (users)
line1 = ax1.plot(years, users / 1e9, color=MLBLUE, linewidth=2.5,
                 label='Extensive Margin (Users)', marker='o', markersize=3)
ax1.set_ylabel('Digital Finance Users (Billions)', color=MLBLUE, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=MLBLUE)
ax1.grid(True, alpha=0.3, linestyle='--')

# Plot intensive margin (txns per user)
line2 = ax1_right.plot(years, txns_per_user, color=MLORANGE, linewidth=2.5,
                       label='Intensive Margin (Txns/User/Year)', marker='s', markersize=3)
ax1_right.set_ylabel('Transactions per User per Year', color=MLORANGE, fontweight='bold')
ax1_right.tick_params(axis='y', labelcolor=MLORANGE)

# Annotate inflection points
ax1.axvline(2020, color=MLBLUE, linestyle=':', alpha=0.5, linewidth=1.5)
ax1.text(2020, users[10] / 1e9 * 1.1, 'User Growth\nInflection',
         ha='center', fontsize=10, color=MLBLUE, weight='bold')

ax1_right.axvline(2025, color=MLORANGE, linestyle=':', alpha=0.5, linewidth=1.5)
ax1_right.text(2025, txns_per_user[15] * 1.15, 'Usage\nIntensification',
               ha='center', fontsize=10, color=MLORANGE, weight='bold')

# Combine legends
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', frameon=True, fancybox=True, shadow=True)
ax1.set_title('Digital Finance Growth: Two Margins', fontweight='bold', size=16)

# Bottom subplot: Stacked area showing total volume decomposition
# We decompose as: contribution from extensive = (users_t / users_max) * total_volume
# contribution from intensive = (txns_per_user_t / txns_max) * total_volume
# But this doesn't stack properly. Instead, show cumulative growth decomposition

# Compute growth contributions (simplified representation)
base_volume = (users / users.max()) * (txns_per_user / txns_per_user.max()) * total_volume.max()
extensive_contribution = (users / users.max()) * total_volume.max() * 0.5
intensive_contribution = (txns_per_user / txns_per_user.max()) * total_volume.max() * 0.5

ax2.fill_between(years, 0, extensive_contribution, color=MLBLUE, alpha=0.6,
                 label='Extensive Margin Contribution')
ax2.fill_between(years, extensive_contribution,
                 extensive_contribution + intensive_contribution,
                 color=MLORANGE, alpha=0.6, label='Intensive Margin Contribution')
ax2.plot(years, total_volume, color=MLPURPLE, linewidth=3,
         label='Total Transaction Volume', linestyle='--')

ax2.set_xlabel('Year', fontweight='bold')
ax2.set_ylabel('Transaction Volume (Billions/Year)', fontweight='bold')
ax2.set_title('Total Volume Decomposition', fontweight='bold', size=16)
ax2.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
ax2.grid(True, alpha=0.3, linestyle='--')

# Add annotations for key milestones
ax2.annotate('Early Adoption\n(User Focus)',
             xy=(2015, total_volume[5]), xytext=(2013, total_volume[5] * 2),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
             fontsize=10, ha='center', weight='bold')

ax2.annotate('Maturity\n(Usage Deepening)',
             xy=(2030, total_volume[20]), xytext=(2028, total_volume[20] * 1.15),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
             fontsize=10, ha='center', weight='bold')

plt.tight_layout()

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
