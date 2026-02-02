"""Regulatory Cost-Benefit: Deadweight Loss Analysis

Welfare economics of financial regulation with Harberger triangles.
Theory: Harberger (1954), Welfare Analysis of Taxation.

Based on: Stigler (1971) - Theory of Economic Regulation
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

np.random.seed(42)

plt.rcParams.update({
    'font.size': 12, 'axes.labelsize': 13, 'axes.titlesize': 14,
    'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 11,
    'figure.figsize': (14, 6), 'figure.dpi': 150
})

MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'
MLLAVENDER = '#ADADE0'
MLGRAY = '#7F7F7F'

# Supply and Demand parameters
a = 100  # Demand intercept (max WTP)
b = 0.8  # Demand slope
c = 20   # Supply intercept (min MC)
s = 0.6  # Supply slope

# Quantity range
Q = np.linspace(0, 100, 500)

# Free market equilibrium
Q_star = (a - c) / (b + s)
P_star = a - b * Q_star

# Demand and Supply curves
P_demand = a - b * Q
P_supply = c + s * Q

# Two regulatory scenarios: light and heavy
tau_light = 10  # Light touch regulation cost
tau_heavy = 25  # Heavy regulation cost

# Supply shifts up by compliance cost tau
P_supply_light = c + tau_light + s * Q
P_supply_heavy = c + tau_heavy + s * Q

# New equilibria with regulation
Q_light = (a - c - tau_light) / (b + s)
P_light = a - b * Q_light

Q_heavy = (a - c - tau_heavy) / (b + s)
P_heavy = a - b * Q_heavy

# Calculate surplus values
def consumer_surplus(Q_eq, P_eq):
    """CS = 0.5 * (a - P_eq) * Q_eq"""
    return 0.5 * (a - P_eq) * Q_eq

def producer_surplus(Q_eq, P_eq, tau=0):
    """PS = 0.5 * (P_eq - c - tau) * Q_eq"""
    return 0.5 * (P_eq - c - tau) * Q_eq

def deadweight_loss(Q_before, Q_after):
    """DWL = 0.5 * (b + s) * (Q_before - Q_after)^2"""
    return 0.5 * (b + s) * (Q_before - Q_after)**2

# Free market surpluses
CS_free = consumer_surplus(Q_star, P_star)
PS_free = producer_surplus(Q_star, P_star)
Total_free = CS_free + PS_free

# Light regulation surpluses
CS_light = consumer_surplus(Q_light, P_light)
PS_light = producer_surplus(Q_light, P_light, tau_light)
DWL_light = deadweight_loss(Q_star, Q_light)
Total_light = CS_light + PS_light

# Heavy regulation surpluses
CS_heavy = consumer_surplus(Q_heavy, P_heavy)
PS_heavy = producer_surplus(Q_heavy, P_heavy, tau_heavy)
DWL_heavy = deadweight_loss(Q_star, Q_heavy)
Total_heavy = CS_heavy + PS_heavy

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ========== LEFT PANEL: Light Touch Regulation ==========
ax1.plot(Q, P_demand, color=MLBLUE, linewidth=2.5, label='Demand (WTP)', zorder=3)
ax1.plot(Q, P_supply, color=MLGREEN, linewidth=2.5, label='Supply (MC)', zorder=3)
ax1.plot(Q, P_supply_light, color=MLRED, linewidth=2.5, linestyle='--',
         label=f'Supply + τ = ${tau_light}', zorder=3)

# Fill consumer surplus (light regulation)
Q_fill_cs = Q[Q <= Q_light]
P_fill_cs_demand = a - b * Q_fill_cs
P_fill_cs_supply = c + tau_light + s * Q_fill_cs
ax1.fill_between(Q_fill_cs, P_light, P_fill_cs_demand,
                 alpha=0.35, color=MLBLUE, label=f'CS = ${CS_light:.0f}')

# Fill producer surplus (light regulation)
ax1.fill_between(Q_fill_cs, c + tau_light, P_fill_cs_supply,
                 alpha=0.35, color=MLGREEN, label=f'PS = ${PS_light:.0f}')

# Fill deadweight loss (light regulation)
Q_fill_dwl = Q[(Q >= Q_light) & (Q <= Q_star)]
P_fill_dwl_demand = a - b * Q_fill_dwl
P_fill_dwl_supply = c + tau_light + s * Q_fill_dwl
ax1.fill_between(Q_fill_dwl, P_fill_dwl_supply, P_fill_dwl_demand,
                 alpha=0.5, color=MLRED, label=f'DWL = ${DWL_light:.0f}')

# Equilibrium markers
ax1.plot(Q_star, P_star, 'ko', markersize=8, zorder=5)
ax1.plot(Q_light, P_light, 'ro', markersize=8, zorder=5)

# Vertical lines
ax1.axvline(Q_star, color=MLGRAY, linestyle=':', linewidth=1.5, alpha=0.6)
ax1.axvline(Q_light, color=MLRED, linestyle=':', linewidth=1.5, alpha=0.6)

# Annotations
ax1.annotate(f'Free Market\nQ* = {Q_star:.1f}\nP* = ${P_star:.1f}',
            xy=(Q_star, P_star), xytext=(Q_star - 15, P_star + 15),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2))

ax1.annotate(f'With Regulation\nQ = {Q_light:.1f}\nP = ${P_light:.1f}',
            xy=(Q_light, P_light), xytext=(Q_light + 15, P_light - 15),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.2))

ax1.set_xlabel('Quantity (Q)')
ax1.set_ylabel('Price (P)')
ax1.set_title('Light Touch Financial Regulation Compliance Cost Analysis', fontsize=14)
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 100)
ax1.set_ylim(0, 110)

# Add educational annotation
ax1.text(0.02, 0.98, 'DWL = ½(b+s)(Q*-Q)²\nOptimal when MB = MSC',
        transform=ax1.transAxes, fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ========== RIGHT PANEL: Heavy Regulation ==========
ax2.plot(Q, P_demand, color=MLBLUE, linewidth=2.5, label='Demand (WTP)', zorder=3)
ax2.plot(Q, P_supply, color=MLGREEN, linewidth=2.5, label='Supply (MC)', zorder=3)
ax2.plot(Q, P_supply_heavy, color=MLRED, linewidth=2.5, linestyle='--',
         label=f'Supply + τ = ${tau_heavy}', zorder=3)

# Fill consumer surplus (heavy regulation)
Q_fill_cs_h = Q[Q <= Q_heavy]
P_fill_cs_demand_h = a - b * Q_fill_cs_h
P_fill_cs_supply_h = c + tau_heavy + s * Q_fill_cs_h
ax2.fill_between(Q_fill_cs_h, P_heavy, P_fill_cs_demand_h,
                 alpha=0.35, color=MLBLUE, label=f'CS = ${CS_heavy:.0f}')

# Fill producer surplus (heavy regulation)
ax2.fill_between(Q_fill_cs_h, c + tau_heavy, P_fill_cs_supply_h,
                 alpha=0.35, color=MLGREEN, label=f'PS = ${PS_heavy:.0f}')

# Fill deadweight loss (heavy regulation)
Q_fill_dwl_h = Q[(Q >= Q_heavy) & (Q <= Q_star)]
P_fill_dwl_demand_h = a - b * Q_fill_dwl_h
P_fill_dwl_supply_h = c + tau_heavy + s * Q_fill_dwl_h
ax2.fill_between(Q_fill_dwl_h, P_fill_dwl_supply_h, P_fill_dwl_demand_h,
                 alpha=0.5, color=MLRED, label=f'DWL = ${DWL_heavy:.0f}')

# Equilibrium markers
ax2.plot(Q_star, P_star, 'ko', markersize=8, zorder=5)
ax2.plot(Q_heavy, P_heavy, 'ro', markersize=8, zorder=5)

# Vertical lines
ax2.axvline(Q_star, color=MLGRAY, linestyle=':', linewidth=1.5, alpha=0.6)
ax2.axvline(Q_heavy, color=MLRED, linestyle=':', linewidth=1.5, alpha=0.6)

# Annotations
ax2.annotate(f'Free Market\nQ* = {Q_star:.1f}\nP* = ${P_star:.1f}',
            xy=(Q_star, P_star), xytext=(Q_star - 15, P_star + 15),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.2))

ax2.annotate(f'With Regulation\nQ = {Q_heavy:.1f}\nP = ${P_heavy:.1f}',
            xy=(Q_heavy, P_heavy), xytext=(Q_heavy + 15, P_heavy - 15),
            fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color=MLRED, lw=1.2))

ax2.set_xlabel('Quantity (Q)')
ax2.set_ylabel('Price (P)')
ax2.set_title('Heavy Financial Regulation Compliance Cost Analysis', fontsize=14)
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 100)
ax2.set_ylim(0, 110)

# Add educational annotation
ax2.text(0.02, 0.98, 'Cost-Benefit: Regulate if\nSocial Benefit > DWL + τ',
        transform=ax2.transAxes, fontsize=9,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()

# Add overall title with citation
fig.suptitle('Deadweight Loss from Financial Regulation (Harberger, 1954)',
             fontsize=15, y=1.00, fontweight='bold')

plt.savefig(Path(__file__).parent / 'chart.pdf', dpi=300, bbox_inches='tight')
plt.savefig(Path(__file__).parent / 'chart.png', dpi=150, bbox_inches='tight')
plt.close()
print("Chart saved to chart.pdf and chart.png")
print(f"\n=== Welfare Analysis Summary ===")
print(f"Free Market: CS=${CS_free:.0f}, PS=${PS_free:.0f}, Total=${Total_free:.0f}")
print(f"\nLight Regulation (tau=${tau_light}):")
print(f"  CS=${CS_light:.0f}, PS=${PS_light:.0f}, DWL=${DWL_light:.0f}, Total=${Total_light:.0f}")
print(f"  Welfare Loss: ${Total_free - Total_light:.0f} ({100*(Total_free - Total_light)/Total_free:.1f}%)")
print(f"\nHeavy Regulation (tau=${tau_heavy}):")
print(f"  CS=${CS_heavy:.0f}, PS=${PS_heavy:.0f}, DWL=${DWL_heavy:.0f}, Total=${Total_heavy:.0f}")
print(f"  Welfare Loss: ${Total_free - Total_heavy:.0f} ({100*(Total_free - Total_heavy)/Total_free:.1f}%)")
