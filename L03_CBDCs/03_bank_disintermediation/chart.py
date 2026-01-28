"""Bank Balance Sheet Impact - Disintermediation scenarios"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

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

fig, axes = plt.subplots(1, 3, figsize=(10, 6))

# Scenario data (stylized balance sheets)
scenarios = ['Pre-CBDC', 'Moderate CBDC\nAdoption', 'High CBDC\nAdoption']

# Assets (same in all scenarios, just reserves change)
# Liabilities change with CBDC adoption

for idx, (ax, scenario) in enumerate(zip(axes, scenarios)):
    # Balance sheet bars (stacked)

    if idx == 0:  # Pre-CBDC
        # Assets
        assets = {'Reserves': 10, 'Loans': 70, 'Securities': 20}
        # Liabilities
        liabilities = {'Deposits': 80, 'Equity': 10, 'Wholesale': 10}
    elif idx == 1:  # Moderate CBDC
        assets = {'Reserves': 8, 'Loans': 65, 'Securities': 20}
        liabilities = {'Deposits': 65, 'Equity': 10, 'Wholesale': 18}
    else:  # High CBDC
        assets = {'Reserves': 5, 'Loans': 55, 'Securities': 20}
        liabilities = {'Deposits': 45, 'Equity': 10, 'Wholesale': 25}

    # Draw asset bars
    bottom = 0
    asset_colors = [MLGREEN, MLBLUE, MLLAVENDER]
    for i, (name, val) in enumerate(assets.items()):
        ax.barh(1, val, left=bottom, height=0.35, color=asset_colors[i],
                alpha=0.8, edgecolor='white', linewidth=1)
        if val > 10:
            ax.text(bottom + val/2, 1, f'{name}\n{val}', ha='center', va='center',
                    fontsize=9, fontweight='bold')
        bottom += val

    # Draw liability bars
    bottom = 0
    liab_colors = [MLORANGE, MLPURPLE, 'gray']
    for i, (name, val) in enumerate(liabilities.items()):
        ax.barh(0, val, left=bottom, height=0.35, color=liab_colors[i],
                alpha=0.8, edgecolor='white', linewidth=1)
        if val > 10:
            ax.text(bottom + val/2, 0, f'{name}\n{val}', ha='center', va='center',
                    fontsize=9, fontweight='bold')
        bottom += val

    ax.set_xlim(0, 105)
    ax.set_ylim(-0.5, 1.5)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Liabilities', 'Assets'])
    ax.set_title(scenario, fontsize=12, fontweight='bold', color=MLPURPLE)
    ax.set_xlabel('Balance (%)', fontsize=10)

    # Add CBDC outflow annotation for scenarios 2 and 3
    if idx > 0:
        deposit_loss = 80 - liabilities['Deposits']
        ax.annotate(f'-{deposit_loss}% deposits\nto CBDC', xy=(45, -0.35),
                    fontsize=9, ha='center', color=MLRED, fontweight='bold')

fig.suptitle('Bank Disintermediation Risk: Balance Sheet Impact',
             fontsize=16, fontweight='bold', color=MLPURPLE, y=1.02)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
