"""Bitcoin Volatility vs Traditional Currencies - Store of value comparison"""
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

fig, ax = plt.subplots(figsize=(10, 6))

# Simulated annualized volatility data (30-day rolling, realistic values)
years = np.arange(2015, 2025)

# Bitcoin volatility (%)
btc_volatility = np.array([85, 75, 95, 80, 65, 75, 85, 70, 55, 50])

# EUR/USD volatility
eur_volatility = np.array([10, 8, 7, 6, 5, 6, 7, 9, 10, 8])

# Gold volatility
gold_volatility = np.array([15, 14, 12, 11, 13, 18, 17, 14, 13, 15])

# S&P 500 volatility
sp500_volatility = np.array([15, 13, 11, 16, 14, 34, 18, 22, 17, 14])

# Bar positions
x = np.arange(len(years))
width = 0.2

# Create bars
bars1 = ax.bar(x - 1.5*width, btc_volatility, width, label='Bitcoin', color=MLORANGE, alpha=0.8)
bars2 = ax.bar(x - 0.5*width, gold_volatility, width, label='Gold', color='gold', alpha=0.8)
bars3 = ax.bar(x + 0.5*width, sp500_volatility, width, label='S&P 500', color=MLBLUE, alpha=0.8)
bars4 = ax.bar(x + 1.5*width, eur_volatility, width, label='EUR/USD', color=MLGREEN, alpha=0.8)

# Add horizontal lines for context
ax.axhline(y=10, color='gray', linestyle='--', alpha=0.5, label='_nolegend_')
ax.text(9.3, 11, 'Currency\nthreshold', fontsize=9, color='gray', va='bottom')

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Annualized Volatility (%)', fontweight='bold')
ax.set_title('Bitcoin Volatility vs Traditional Assets', fontsize=16,
             fontweight='bold', color=MLPURPLE)

ax.set_xticks(x)
ax.set_xticklabels(years)
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 100)

plt.tight_layout()
plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf")
