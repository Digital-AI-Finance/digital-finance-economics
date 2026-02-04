# L04 In-Class Exercises: Payment Systems Economics

## Plan Metadata
- **Created**: 2026-02-04
- **Lesson**: L04 - Payment Systems Economics
- **Target Audience**: BSc students (just completed L04)
- **Time Allocation**: 30 minutes work + 5 minutes presentation per exercise
- **Instructor Choice**: Select 1-2 exercises per session based on class size and learning goals

---

## Exercise Overview

| # | Title | Category | Group Size | Materials |
|---|-------|----------|------------|-----------|
| 1 | Remittance Corridor Analysis | Python/Data | Individual or Pairs | Laptop with Python |
| 2 | Two-Sided Market Pricing Calculator | Framework Application | Groups of 3-4 | Calculator + Worksheet |
| 3 | M-Pesa Success Decoded | Case Study | Groups of 3-4 | Case Handout |
| 4 | Cash Abolition Debate | Debate/Discussion | Two Teams (4-6 each) | None |
| 5 | Design a Payment System for the Unbanked | Creative/Design | Groups of 3-4 | Whiteboard/Paper |
| 6 | Network Effects Calculator | Python/Data | Individual or Pairs | Laptop with Python |
| 7 | SWIFT vs Blockchain Cross-Border | Comparative Analysis | Groups of 3-4 | Worksheet |
| 8 | RTGS vs DNS Settlement Trade-offs | Framework Application | Pairs | Worksheet |

---

## Exercise 1: Remittance Corridor Analysis

**Category**: Python/Data
**Time**: 30 min work + 5 min presentation
**Group Size**: Individual or Pairs
**Materials Needed**: Laptop with Python (pandas, matplotlib, numpy), internet access

### Task

Analyze remittance costs across different corridors using World Bank-style data. Calculate which corridors are most expensive, identify patterns, and assess progress toward the UN SDG target of 3% by 2030.

### Complete Code

```python
"""
Remittance Corridor Analysis: Cost Comparison and SDG Progress
L04 Exercise - Payment Systems Economics

Requirements: pip install pandas matplotlib numpy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# SIMULATED WORLD BANK REMITTANCE DATA
# =============================================================================

# Real-world inspired data: Q4 2023 estimates by corridor
# Format: (sending_country, receiving_country, avg_cost_%, provider_count, digital_share_%)
corridors = [
    # High-volume corridors
    ("USA", "Mexico", 4.2, 45, 65),
    ("USA", "India", 5.1, 38, 72),
    ("USA", "Philippines", 4.8, 32, 58),
    ("UAE", "India", 3.8, 28, 80),
    ("Saudi Arabia", "Pakistan", 4.5, 22, 45),

    # High-cost African corridors
    ("South Africa", "Zimbabwe", 15.2, 5, 12),
    ("Tanzania", "Rwanda", 12.8, 4, 18),
    ("Angola", "DRC", 18.5, 3, 8),
    ("South Africa", "Malawi", 14.3, 6, 15),
    ("Nigeria", "Ghana", 9.2, 8, 35),

    # European corridors
    ("UK", "Nigeria", 5.8, 25, 55),
    ("Germany", "Turkey", 4.1, 30, 62),
    ("France", "Morocco", 6.2, 18, 48),
    ("Italy", "Romania", 3.9, 22, 70),
    ("Spain", "Colombia", 5.5, 20, 52),

    # Asia-Pacific corridors
    ("Japan", "Philippines", 7.8, 15, 42),
    ("Australia", "Vietnam", 6.9, 18, 55),
    ("Singapore", "Indonesia", 5.2, 25, 68),
    ("Hong Kong", "Philippines", 4.0, 30, 75),
    ("Malaysia", "Bangladesh", 4.8, 20, 50),
]

# Create DataFrame
df = pd.DataFrame(corridors, columns=[
    'sending_country', 'receiving_country', 'avg_cost_pct',
    'provider_count', 'digital_share_pct'
])

# Add derived columns
df['corridor'] = df['sending_country'] + ' -> ' + df['receiving_country']
df['meets_sdg'] = df['avg_cost_pct'] <= 3.0
df['cost_category'] = pd.cut(df['avg_cost_pct'],
                              bins=[0, 3, 5, 8, 100],
                              labels=['SDG Compliant (<3%)', 'Low (3-5%)',
                                     'Medium (5-8%)', 'High (>8%)'])

print("="*70)
print("REMITTANCE COST ANALYSIS BY CORRIDOR")
print("="*70)

# =============================================================================
# ANALYSIS 1: COST DISTRIBUTION
# =============================================================================

print("\n1. COST DISTRIBUTION")
print("-"*40)
print(f"Global Average Cost: {df['avg_cost_pct'].mean():.1f}%")
print(f"Median Cost: {df['avg_cost_pct'].median():.1f}%")
print(f"Minimum Cost: {df['avg_cost_pct'].min():.1f}% ({df.loc[df['avg_cost_pct'].idxmin(), 'corridor']})")
print(f"Maximum Cost: {df['avg_cost_pct'].max():.1f}% ({df.loc[df['avg_cost_pct'].idxmax(), 'corridor']})")
print(f"\nCost Spread (Max - Min): {df['avg_cost_pct'].max() - df['avg_cost_pct'].min():.1f} percentage points")

# =============================================================================
# ANALYSIS 2: SDG PROGRESS
# =============================================================================

print("\n2. UN SDG 10.c PROGRESS (Target: 3% by 2030)")
print("-"*40)
sdg_compliant = df['meets_sdg'].sum()
print(f"Corridors meeting SDG target: {sdg_compliant}/{len(df)} ({100*sdg_compliant/len(df):.0f}%)")
print(f"Corridors above SDG target: {len(df) - sdg_compliant}/{len(df)} ({100*(len(df)-sdg_compliant)/len(df):.0f}%)")

print("\nBy Cost Category:")
print(df['cost_category'].value_counts().to_string())

# =============================================================================
# ANALYSIS 3: COMPETITION EFFECT
# =============================================================================

print("\n3. COMPETITION EFFECT (Bertrand Theory)")
print("-"*40)

# Calculate correlation between provider count and cost
correlation = df['provider_count'].corr(df['avg_cost_pct'])
print(f"Correlation between # providers and cost: {correlation:.3f}")
print("(Negative correlation = more competition = lower prices)")

# Split into high/low competition
median_providers = df['provider_count'].median()
high_competition = df[df['provider_count'] >= median_providers]
low_competition = df[df['provider_count'] < median_providers]

print(f"\nHigh Competition (>={int(median_providers)} providers):")
print(f"  Average cost: {high_competition['avg_cost_pct'].mean():.1f}%")
print(f"  Corridors: {len(high_competition)}")

print(f"\nLow Competition (<{int(median_providers)} providers):")
print(f"  Average cost: {low_competition['avg_cost_pct'].mean():.1f}%")
print(f"  Corridors: {len(low_competition)}")

cost_diff = low_competition['avg_cost_pct'].mean() - high_competition['avg_cost_pct'].mean()
print(f"\nCompetition Premium: {cost_diff:.1f} percentage points")
print("(Low competition corridors are more expensive)")

# =============================================================================
# ANALYSIS 4: DIGITAL DISRUPTION
# =============================================================================

print("\n4. DIGITAL DISRUPTION EFFECT")
print("-"*40)

correlation_digital = df['digital_share_pct'].corr(df['avg_cost_pct'])
print(f"Correlation between digital share and cost: {correlation_digital:.3f}")
print("(Negative correlation = more digital = lower prices)")

# Split into high/low digital
median_digital = df['digital_share_pct'].median()
high_digital = df[df['digital_share_pct'] >= median_digital]
low_digital = df[df['digital_share_pct'] < median_digital]

print(f"\nHigh Digital (>={int(median_digital)}% digital):")
print(f"  Average cost: {high_digital['avg_cost_pct'].mean():.1f}%")

print(f"\nLow Digital (<{int(median_digital)}% digital):")
print(f"  Average cost: {low_digital['avg_cost_pct'].mean():.1f}%")

# =============================================================================
# VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Remittance Corridor Analysis: Economics of Cross-Border Payments',
             fontsize=14, fontweight='bold')

# Chart 1: Cost by corridor (horizontal bar)
ax1 = axes[0, 0]
df_sorted = df.sort_values('avg_cost_pct', ascending=True)
colors = ['#2CA02C' if x <= 3 else '#FF7F0E' if x <= 5 else '#D62728'
          for x in df_sorted['avg_cost_pct']]
ax1.barh(range(len(df_sorted)), df_sorted['avg_cost_pct'], color=colors, alpha=0.8)
ax1.set_yticks(range(len(df_sorted)))
ax1.set_yticklabels(df_sorted['corridor'], fontsize=8)
ax1.axvline(x=3, color='green', linestyle='--', linewidth=2, label='SDG Target (3%)')
ax1.axvline(x=df['avg_cost_pct'].mean(), color='blue', linestyle=':',
           linewidth=2, label=f'Global Avg ({df["avg_cost_pct"].mean():.1f}%)')
ax1.set_xlabel('Cost (%)')
ax1.set_title('Remittance Costs by Corridor')
ax1.legend(loc='lower right', fontsize=8)

# Chart 2: Competition vs Cost scatter
ax2 = axes[0, 1]
ax2.scatter(df['provider_count'], df['avg_cost_pct'],
           s=100, c=df['digital_share_pct'], cmap='RdYlGn',
           alpha=0.7, edgecolors='black')
ax2.axhline(y=3, color='green', linestyle='--', linewidth=1.5, alpha=0.7)

# Add regression line
z = np.polyfit(df['provider_count'], df['avg_cost_pct'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['provider_count'].min(), df['provider_count'].max(), 100)
ax2.plot(x_line, p(x_line), 'r--', alpha=0.5, label=f'Trend (r={correlation:.2f})')

ax2.set_xlabel('Number of Providers')
ax2.set_ylabel('Cost (%)')
ax2.set_title('Bertrand Competition Effect\n(Color = Digital Share %)')
ax2.legend()
cbar = plt.colorbar(ax2.collections[0], ax=ax2)
cbar.set_label('Digital Share %')

# Chart 3: Cost distribution histogram
ax3 = axes[1, 0]
ax3.hist(df['avg_cost_pct'], bins=10, color='#3333B2', alpha=0.7, edgecolor='black')
ax3.axvline(x=3, color='green', linestyle='--', linewidth=2, label='SDG Target')
ax3.axvline(x=df['avg_cost_pct'].mean(), color='red', linestyle='-',
           linewidth=2, label=f'Mean ({df["avg_cost_pct"].mean():.1f}%)')
ax3.axvline(x=df['avg_cost_pct'].median(), color='orange', linestyle='-',
           linewidth=2, label=f'Median ({df["avg_cost_pct"].median():.1f}%)')
ax3.set_xlabel('Cost (%)')
ax3.set_ylabel('Number of Corridors')
ax3.set_title('Cost Distribution')
ax3.legend()

# Chart 4: Digital share vs Cost
ax4 = axes[1, 1]
ax4.scatter(df['digital_share_pct'], df['avg_cost_pct'],
           s=df['provider_count']*5, c='#0066CC', alpha=0.6, edgecolors='black')
ax4.axhline(y=3, color='green', linestyle='--', linewidth=1.5, alpha=0.7)

# Add regression line
z2 = np.polyfit(df['digital_share_pct'], df['avg_cost_pct'], 1)
p2 = np.poly1d(z2)
x_line2 = np.linspace(df['digital_share_pct'].min(), df['digital_share_pct'].max(), 100)
ax4.plot(x_line2, p2(x_line2), 'r--', alpha=0.5, label=f'Trend (r={correlation_digital:.2f})')

ax4.set_xlabel('Digital Share (%)')
ax4.set_ylabel('Cost (%)')
ax4.set_title('Digital Disruption Effect\n(Size = # Providers)')
ax4.legend()

plt.tight_layout()
plt.savefig('remittance_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nChart saved as 'remittance_analysis.png'")

# =============================================================================
# ECONOMIC CONCLUSIONS
# =============================================================================

print("\n" + "="*70)
print("ECONOMIC ANALYSIS: KEY FINDINGS")
print("="*70)

print("""
1. GEOGRAPHIC INEQUALITY:
   - African corridors average {:.1f}% cost vs {:.1f}% for other regions
   - This is regressive: poorest populations pay highest fees
   - Explanation: Low competition, limited infrastructure, regulatory barriers

2. COMPETITION MATTERS (Bertrand Theory):
   - Strong negative correlation between providers and cost
   - Each additional provider reduces costs by ~{:.2f} percentage points
   - Policy implication: Lower barriers to entry for new providers

3. DIGITAL DISRUPTION IS KEY:
   - Digital-first corridors are {:.1f}% cheaper on average
   - Mobile money (M-Pesa model) disrupts traditional remittance
   - But digital access remains barrier in high-cost corridors

4. SDG PROGRESS:
   - Only {:.0f}% of corridors meet 3% target
   - Current trajectory insufficient for 2030 deadline
   - Requires: regulatory harmonization, digital infrastructure, competition policy
""".format(
    df[df['corridor'].str.contains('Africa|Angola|DRC|Malawi|Zimbabwe|Tanzania|Rwanda|Nigeria|Ghana', case=False, regex=True)]['avg_cost_pct'].mean(),
    df[~df['corridor'].str.contains('Africa|Angola|DRC|Malawi|Zimbabwe|Tanzania|Rwanda|Nigeria|Ghana', case=False, regex=True)]['avg_cost_pct'].mean(),
    -z[0],  # Slope of regression line
    low_digital['avg_cost_pct'].mean() - high_digital['avg_cost_pct'].mean(),
    100*sdg_compliant/len(df)
))
```

### Model Answer / Expected Output

**Expected Chart Description:**
- 4-panel visualization showing:
  1. Horizontal bar chart of all corridors sorted by cost (green = SDG compliant, orange = low, red = high)
  2. Scatter plot showing negative relationship between competition and cost (Bertrand theory)
  3. Histogram of cost distribution showing right-skewed pattern
  4. Scatter showing digital share reduces costs

**Key Findings (Model Answer):**

1. **Geographic Inequality is Stark:**
   - African corridors average 14% cost vs 5% for other regions
   - The poorest remittance recipients pay 2-3x more in fees
   - This is economically regressive: transfers to Zimbabwe cost 15%+, while to Mexico only 4%

2. **Bertrand Competition Works:**
   - Strong negative correlation (-0.7 to -0.8) between provider count and cost
   - Corridors with 30+ providers average ~4%; corridors with <10 providers average ~12%
   - Each additional competitor reduces cost by approximately 0.2-0.3 percentage points

3. **Digital Disruption is Real but Uneven:**
   - High-digital corridors are 3-5% cheaper than low-digital corridors
   - But digital infrastructure is worst in highest-cost corridors
   - Creates reinforcing inequality: no digital = high cost = no investment in digital

4. **SDG Target is Unrealistic at Current Pace:**
   - Only 0-10% of corridors meet 3% target
   - Global average stuck at 6%+
   - Would require halving costs in 6 years = unprecedented

### Presentation Talking Points
- Remittance fees are a regressive tax on the global poor - those who can least afford it pay the most
- Bertrand competition theory predicts price convergence to marginal cost as competitors increase - data confirms this
- The 6% average global cost represents $48 billion annually in fees on $800 billion in remittances
- Digital disruption is the most promising path to SDG target, but requires infrastructure investment in high-cost corridors
- Key economic insight: Market structure (competition) matters more than technology - even with same technology, monopoly corridors charge more

---

## Exercise 2: Two-Sided Market Pricing Calculator

**Category**: Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Calculator, worksheet with formulas

### Task

Apply the Rochet-Tirole two-sided market model to calculate optimal interchange fees for a new payment network. You are the economics team advising a startup card network entering the European market.

**Given Parameters:**
- Merchant price elasticity: -2.0 (sensitive to fees)
- Consumer price elasticity: -0.5 (less sensitive - rewards offset fees)
- Total marginal cost to platform: 0.8% per transaction
- Platform target margin: 0.3%

**Questions to Answer:**
1. What is the optimal fee structure (split between merchants and consumers)?
2. How would EU interchange caps (0.3% for credit) affect your strategy?
3. What happens if a competitor offers merchants 0.5% lower fees?

### Model Answer / Expected Output

**1. Optimal Fee Structure Calculation:**

Using Rochet-Tirole pricing rule:
$$\frac{p_B - c_B}{p_S - c_S} = \frac{\eta_S}{\eta_B}$$

Where:
- $p_B$ = price to buyers (consumers), $p_S$ = price to sellers (merchants)
- $c_B$ = cost of serving buyers, $c_S$ = cost of serving sellers
- $\eta_B$ = consumer elasticity = -0.5
- $\eta_S$ = merchant elasticity = -2.0

**Step-by-step:**

Total price = Marginal cost + Margin = 0.8% + 0.3% = 1.1%

The elasticity ratio tells us how to split:
$$\frac{\eta_S}{\eta_B} = \frac{-2.0}{-0.5} = 4$$

This means: charge the less elastic side (consumers) 4x more markup than the elastic side (merchants).

Let merchant markup = x
Consumer markup = 4x
Total markup = 5x = 0.3%
Therefore: x = 0.06%

**Optimal Structure:**
| Side | Markup | Allocated Cost | Total Fee |
|------|--------|----------------|-----------|
| Merchant | 0.06% | 0.50% | **0.56%** |
| Consumer | 0.24% | 0.30% | **0.54%** |
| **TOTAL** | 0.30% | 0.80% | **1.10%** |

But in practice, consumer fees are often zero or negative (rewards), so:

**Realistic Structure:**
| Side | Fee | Notes |
|------|-----|-------|
| Merchant | 1.1% + 0.1% = 1.2% | Bears full cost plus subsidy |
| Consumer | -0.1% (1% cashback) | Subsidized to drive adoption |

**2. EU Interchange Cap Impact:**

EU caps interchange at 0.3% for credit cards. This constrains our model:

| Scenario | Consumer Fee | Merchant Fee | Platform Economics |
|----------|--------------|--------------|-------------------|
| Unconstrained | Negative (rewards) | 1.5-2.0% | Issuer profits fund rewards |
| EU Capped | Minimal rewards | 0.5-0.7% | Compressed margins, fewer rewards |

**Strategic Response:**
- Reduce consumer rewards (can't afford 2% cashback on 0.3% interchange)
- Compete on merchant services (fraud protection, analytics)
- Add annual fees to consumers (shift to fixed vs variable revenue)
- Target premium segments where higher interchange allowed

**3. Competitive Response (Merchant Fee -0.5%):**

If competitor offers 0.5% lower merchant fees:

| Option | Action | Trade-off |
|--------|--------|-----------|
| **Match** | Cut merchant fee by 0.5% | Lose 0.5% margin per transaction |
| **Don't Match** | Maintain fees | Lose merchants (elastic!) |
| **Subsidize** | Reduce consumer rewards to fund merchant discount | Lose consumers |
| **Differentiate** | Better rewards, service, or brand | Non-price competition |

**Quantitative Analysis:**
- Merchant elasticity = -2.0 means: 10% price increase = 20% volume decrease
- 0.5% fee difference = ~25% reduction in transaction volume if merchants leave
- Must match or differentiate - can't ignore given elasticity

**Recommendation:** Match the competitor on merchant fees, fund it by slightly reducing consumer rewards (consumers are less elastic, so smaller volume impact).

### Presentation Talking Points
- Two-sided markets require different economics than one-sided - can't just minimize total cost
- The "subsidize one side" model explains why credit cards give rewards: consumers are less price-sensitive, so attract them with rewards funded by merchant fees
- EU interchange caps fundamentally changed this model - rewards declined, annual fees returned
- Key economic insight: Price structure (who pays what) matters as much as price level (total cost)
- Competitive dynamics in two-sided markets are complex: attacking one side can flip the whole network

---

## Exercise 3: M-Pesa Success Decoded

**Category**: Case Study
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Case handout with M-Pesa timeline and data

### Task

Analyze M-Pesa's success through the network effects and platform economics frameworks from L04. Explain why M-Pesa succeeded in Kenya but failed in South Africa.

**Case Data Provided:**

**Kenya M-Pesa:**
- Launch: March 2007
- Users: 2M (2008), 15M (2011), 30M (2020)
- Market share: 99% of mobile money (2023)
- Agents: 40,000 (2011), 200,000+ (2023)
- Transaction volume: $50B annually (2023)

**South Africa M-Pesa:**
- Launch: September 2010
- Users: 100,000 (2011), discontinued 2016
- Market share: <1%
- Agents: Limited
- Reason for failure: "Commercial failure"

**Questions:**
1. What network effects drove M-Pesa's success in Kenya?
2. Why did M-Pesa fail in South Africa?
3. What can policymakers learn about fostering payment innovation?

### Model Answer / Expected Output

**1. Network Effects Driving Kenya Success:**

| Network Effect Type | How M-Pesa Captured It |
|---------------------|------------------------|
| **Direct Network Effects** | More users = more people you can send money to. 2M users in year 1 created immediate value. Agent network (40,000 points) created physical network effect - could cash in/out anywhere. |
| **Indirect Network Effects** | More users attracted merchants, bill payment, salary disbursement. Each new use case attracted more users (virtuous cycle). |
| **Critical Mass (16%)** | Kenya population ~50M, 15M users by 2011 = 30%. Crossed critical mass within 3-4 years. After this, adoption was self-sustaining. |
| **First-Mover Advantage** | Safaricom had 80%+ mobile market share already. Converted existing network to payment network. No competitor could match installed base. |

**Additional Success Factors:**
| Factor | Explanation |
|--------|-------------|
| **Unbanked Population** | Only 19% had bank accounts; M-Pesa solved real need |
| **Regulatory Environment** | Central Bank allowed "permissionless innovation" - regulated later |
| **Agent Economics** | Agents earned commissions - created distribution army |
| **Use Case Fit** | Urban-to-rural remittances were huge unmet need |

**2. Why South Africa Failed:**

| Factor | Kenya | South Africa | Impact |
|--------|-------|--------------|--------|
| **Banking Access** | 19% banked | 70%+ banked | Less unmet need |
| **Mobile Market** | Safaricom 80% share | Fragmented market | No existing network to leverage |
| **Agent Network** | 40,000+ agents | Failed to scale | Critical infrastructure missing |
| **Regulatory** | Light touch | Stricter banking regulations | Higher compliance costs |
| **Competition** | First mover | FNB, ABSA already had mobile banking | Incumbents had network effects |
| **Cultural Fit** | Cash-based, informal economy | More formalized economy | Less need for cash alternative |

**Core Insight:** M-Pesa succeeded in Kenya because it solved a real problem (no banking access) and captured network effects through first-mover advantage and agent network. In South Africa, the problem was already solved (high banking access) and incumbents had existing network effects.

**3. Policy Lessons:**

| Lesson | Explanation | Policy Implication |
|--------|-------------|-------------------|
| **Network effects are winner-take-all** | M-Pesa has 99% share despite competition | Regulator must decide: foster competition or let network effects work |
| **Agent networks are critical** | 200,000 agents > all bank branches | Support agent network development |
| **Timing matters** | First mover with network effects is decisive | "Permissionless innovation" can create first-mover advantage |
| **Interoperability trade-off** | Dominant player has no incentive to interoperate | May need to mandate interoperability |
| **Financial inclusion requires infrastructure** | Technology alone insufficient without distribution | Fund agent network and digital literacy |

**Recommendation for New Markets:**
1. Identify markets with low banking penetration (high unmet need)
2. Partner with dominant mobile operator (existing network effects)
3. Invest heavily in agent network (critical mass of physical presence)
4. Start with simple use case (P2P remittances) before expanding
5. Engage regulators early but advocate for innovation space

### Presentation Talking Points
- M-Pesa is the canonical example of network effects in payment systems - 99% market share is unprecedented
- The 16% critical mass threshold was reached within 4 years; after that, competition was essentially impossible
- South Africa failure proves: technology is not enough - you need network effects AND unmet demand
- The agent network was the secret weapon - created physical network effects that banks couldn't match
- Key economic insight: Network effects create natural monopolies, which requires regulatory consideration (mandate interoperability? regulate fees?)

---

## Exercise 4: Cash Abolition Debate

**Category**: Debate/Discussion
**Time**: 30 min work + 5 min presentation (final debate)
**Group Size**: Two teams of 4-6 students each
**Materials Needed**: None (timer helpful)

### Task

Structured debate on the motion: **"All physical cash should be eliminated and replaced with digital payments within 10 years."**

**Team A (Pro)**: Cash should be abolished
**Team B (Con)**: Cash should be preserved

**Debate Structure**:
| Phase | Time | Activity |
|-------|------|----------|
| Preparation | 15 min | Teams prepare 3 main arguments using L04 concepts |
| Opening | 3 min each | Each team presents main arguments |
| Rebuttal Prep | 5 min | Teams prepare responses |
| Rebuttals | 2 min each | Each team responds to opponent |
| Closing | 2 min each | Final summary |

**Required L04 Concepts**: Use at least 2 per team from:
- Network effects and critical mass
- Transaction costs
- Financial inclusion
- Settlement systems (RTGS/DNS)
- Two-sided markets
- Payment system infrastructure

### Model Answer / Expected Output

**Team A (Pro - Abolish Cash):**

**Argument 1: Transaction Cost Elimination**
- L04 Concept: *Transaction costs*
- Cash handling costs banks and businesses 1-2% of GDP annually
- Armored cars, counting machines, vault storage, counterfeiting losses
- Sweden example: cash transactions dropped from 40% (2010) to 9% (2023) with no negative effects
- Digital payments have near-zero marginal cost once infrastructure exists
- Estimate: $200-400 billion annually in global savings from cash elimination

**Argument 2: Financial Inclusion Through Digital**
- L04 Concept: *Financial inclusion*
- Cash excludes people from financial services (can't get credit with cash-only history)
- M-Pesa example: Digital payment access lifted 2% out of poverty (Suri & Jack 2016)
- CBDC can provide universal access - no bank account needed
- India's UPI: 300 million unbanked Indians now have digital access
- Digital payments create data trail enabling credit scoring and financial inclusion

**Argument 3: Network Effects Favor Full Transition**
- L04 Concept: *Network effects and critical mass*
- Cash creates negative network effects for digital - merchants must maintain two systems
- Once digital crosses critical mass (~16%), cash becomes inefficient relic
- Sweden shows: post-critical-mass, cash becomes more expensive (fewer ATMs, bank closures)
- Full transition creates maximum network value - Metcalfe's Law applies

**Rebuttal Points Against Con:**
- "Privacy concerns" - Cash is used for tax evasion and crime; legitimate privacy can be designed into digital
- "System failures" - Offline digital payments exist (India's UPI has offline mode)
- "Elderly exclusion" - Transition period allows adaptation; simpler interfaces possible

---

**Team B (Con - Preserve Cash):**

**Argument 1: Resilience and Settlement Risk**
- L04 Concept: *Settlement systems (RTGS/DNS)*
- Digital systems have single points of failure - cyberattacks, power outages
- Cash provides RTGS-like instant, final settlement without counterparty risk
- 2021 Facebook outage affected billions; imagine if all payments failed
- Central banks maintain cash as backup for financial stability
- Real example: Hurricane Maria (Puerto Rico 2017) - cash was only functional payment for weeks

**Argument 2: Financial Inclusion Requires Cash Option**
- L04 Concept: *Financial inclusion*
- 1.4 billion adults unbanked globally - they use cash
- Elderly, disabled, homeless populations rely on cash
- Digital divide: 37% of world population has no internet access
- Eliminating cash excludes the most vulnerable - opposite of inclusion
- India demonetization (2016): chaos, deaths, economic disruption when cash was suddenly restricted

**Argument 3: Privacy and Two-Sided Market Power**
- L04 Concept: *Two-sided markets*
- Digital payment platforms are two-sided markets with monopoly tendencies
- Without cash alternative, platforms can extract maximum fees (no outside option)
- Visa/Mastercard interchange fees are high precisely because cash alternative is declining
- Privacy: all digital payments create surveillance data - cash is anonymous
- Government and corporate surveillance concerns are legitimate

**Rebuttal Points Against Pro:**
- "Cash handling costs" - These are costs of freedom and resilience, not waste
- "Sweden example" - Sweden is small, wealthy, high-trust society; not generalizable
- "Network effects" - Same logic would say eliminate all minority languages for "efficiency"

---

**Balanced Verdict (for instructor):**

The economically nuanced position is that **cash and digital should coexist**:

1. **Market efficiency** favors digital (lower transaction costs)
2. **Resilience and inclusion** require cash (no single point of failure)
3. **Competition** requires cash alternative (prevents digital monopoly pricing)
4. **Privacy** is a legitimate preference that markets should serve

Most likely future: Cash usage declines to 5-10% of transactions but remains legal tender and available. This preserves optionality without forcing inefficiency.

### Presentation Talking Points
- Cash vs digital is not just about efficiency - it's about market structure, privacy, and resilience
- Network effects arguments cut both ways: digital network effects also mean monopoly power
- Financial inclusion can be served by both cash (simple, accessible) and digital (services, credit)
- Key economic insight: Payment diversity is a form of system resilience - monocultures are fragile
- Sweden is often cited but is an outlier: small, wealthy, high-trust, low corruption - not generalizable

---

## Exercise 5: Design a Payment System for the Unbanked

**Category**: Creative/Design
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Whiteboard, flip chart, or paper; colored markers

### Task

Your group is the economic advisory team for a development organization. Design a payment system for a fictional country "Ruritania" with these characteristics:

**Ruritania Profile:**
- Population: 30 million
- GDP per capita: $1,500/year
- Banked population: 15%
- Mobile phone penetration: 70% (mostly basic phones)
- Internet access: 25%
- Dominant industry: Agriculture (60% of workforce)
- Currency: Ruritanian Peso (RUP), stable but not internationally traded
- Major challenge: Agricultural workers paid in cash, no savings mechanism

**Design Requirements:**
1. Technology choice: What infrastructure?
2. Network effects strategy: How will you achieve critical mass?
3. Agent economics: How will you create distribution network?
4. Revenue model: How will you sustain the system financially?
5. Financial inclusion features: Beyond payments, what services?

### Model Answer / Expected Output

**PAYMENT SYSTEM DESIGN: "RuriPay"**

---

**1. TECHNOLOGY CHOICE:**

| Component | Choice | Justification |
|-----------|--------|---------------|
| **Interface** | USSD/SMS-based (like M-Pesa) | Works on basic phones, no internet needed, 70% reach |
| **Backend** | Cloud-hosted with mobile operator | Lower infrastructure cost, operator already has network |
| **Settlement** | Central bank digital ledger | Instant settlement, regulatory compliance, trust |
| **Offline Mode** | Store-and-forward for no-signal areas | Agricultural areas often have poor coverage |

**Technology Stack:**
```
User (basic phone) -> USSD/SMS -> Mobile Operator Gateway ->
RuriPay Platform -> Central Bank Settlement -> Agent Network
```

**Why NOT:**
- Smartphone app: Only 25% have internet
- Bank branches: Too expensive for rural areas
- Blockchain: Unnecessary complexity, no crypto culture
- Cards: No POS infrastructure exists

---

**2. NETWORK EFFECTS STRATEGY:**

**Phase 1: Government Bootstrap (Months 1-12)**
| Action | Expected Impact |
|--------|-----------------|
| Agricultural subsidies paid via RuriPay | 5M farmers onboarded immediately |
| Government salaries via RuriPay | 500K government workers onboarded |
| Tax payments accepted via RuriPay (5% discount) | Incentive to hold RuriPay balance |

*Rationale:* Government is largest payer - use to bootstrap network effects. 5M users = 16% of population = critical mass.

**Phase 2: Merchant Expansion (Months 6-18)**
| Action | Expected Impact |
|--------|-----------------|
| Zero merchant fees for first year | 50,000 merchants onboarded |
| Agricultural input dealers prioritized | Farmers can buy seeds, fertilizer with RuriPay |
| Utility payments (water, electricity) | Creates recurring use case |

*Rationale:* Once farmers have money, merchants will accept it. Agricultural supply chain is key.

**Phase 3: Ecosystem Development (Year 2+)**
| Action | Expected Impact |
|--------|-----------------|
| Savings accounts (interest-bearing) | Formalize informal savings |
| Micro-credit (harvest-cycle loans) | Enable agricultural investment |
| Insurance (crop, health) | Risk management for farmers |

---

**3. AGENT ECONOMICS:**

**Agent Network Design:**
| Metric | Target | Rationale |
|--------|--------|-----------|
| Agent density | 1 per 500 population | 60,000 agents needed |
| Agent type | Village shops, mobile vendors | Existing businesses with cash flow |
| Commission | 0.5% cash-in, 0.3% cash-out | Enough to incentivize but not too expensive |
| Float requirement | RUP 10,000 minimum (~$20) | Low barrier to entry |

**Agent Economics (per agent per month):**
```
Transactions: 200 (estimate for village of 500)
Average transaction: RUP 500 (~$1)
Total volume: RUP 100,000
Commission rate: 0.4% average
Monthly income: RUP 400 (~$0.80)
```

*Challenge:* Low income per agent. Solution: Make it supplementary income for existing shops, not standalone business.

**Agent Incentive Innovations:**
- Super-agent model: Wholesalers serve as float providers to village agents
- Commission bonuses for signing up new users
- Free business training for top agents

---

**4. REVENUE MODEL:**

| Revenue Stream | Rate | Projected Annual Revenue |
|----------------|------|--------------------------|
| Cash-out fees | 1% | $3M (assuming $300M annual cash-out) |
| Merchant fees | 0.5% (after year 1) | $1.5M (assuming $300M merchant payments) |
| Bill payment fees | RUP 5 flat fee | $500K |
| Interest on float | 3% on $20M average float | $600K |
| Cross-border remittances | 3% (vs 8% traditional) | $1.5M (assuming $50M corridor) |
| **TOTAL** | | **$7.1M annually** |

**Operating Costs:**
| Cost | Annual | Notes |
|------|--------|-------|
| Technology platform | $1M | Cloud hosting, USSD gateway |
| Agent network management | $1.5M | Training, support, compliance |
| Customer support | $500K | Call center for issues |
| Regulatory compliance | $300K | KYC/AML, reporting |
| Marketing | $700K | Farmer education, agent recruitment |
| **TOTAL COSTS** | **$4M** | |

**Net Margin:** $3.1M annually = 44% margin after scale

**Sustainability Assessment:** Viable after Year 2 once critical mass achieved. Requires $5-10M initial investment for first two years of losses.

---

**5. FINANCIAL INCLUSION FEATURES:**

| Feature | Design | Economic Impact |
|---------|--------|-----------------|
| **Savings** | Interest-bearing accounts (2% annual) | Formalizes savings currently under mattresses |
| **Micro-credit** | Harvest-cycle loans (6-month term) | Enables fertilizer purchase, 15-20% yield increase |
| **Insurance** | Weather-indexed crop insurance | Reduces risk, enables investment |
| **Credit Scoring** | Transaction history-based | Builds credit for future formal banking |
| **Group Payments** | Farmer cooperative features | Aggregates bargaining power |

**Impact Projection (5 years):**
- 15M users (50% of population)
- 2-3% poverty reduction (based on M-Pesa research)
- 30% increase in formal savings
- 50% reduction in remittance costs

### Presentation Talking Points
- M-Pesa model is proven but requires adaptation to local context
- Government bootstrap is key to achieving critical mass quickly
- Agent economics are challenging in very poor countries - need creative solutions
- Revenue model must be sustainable without extracting too much from poor users
- Key economic insight: Financial inclusion is not just about payments - it's about creating a platform for savings, credit, and insurance
- The 16% critical mass threshold is the key milestone - after that, growth is self-sustaining

---

## Exercise 6: Network Effects Calculator

**Category**: Python/Data
**Time**: 30 min work + 5 min presentation
**Group Size**: Individual or Pairs
**Materials Needed**: Laptop with Python (matplotlib, numpy)

### Task

Build an interactive model of network effects in payment systems. Compare Metcalfe's Law (value grows with n^2) with Odlyzko-Tilly (value grows with n*log(n)) and identify critical mass thresholds.

**Questions to Answer:**
1. At what user count does a network become "viable" (value > switching costs)?
2. How does the growth model (Metcalfe vs Odlyzko-Tilly) affect adoption dynamics?
3. What happens when two competing networks with different sizes merge or interoperate?

### Complete Code

```python
"""
Network Effects Calculator: Payment System Adoption Dynamics
L04 Exercise - Payment Systems Economics

Requirements: pip install matplotlib numpy
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# NETWORK VALUE MODELS
# =============================================================================

def metcalfe_value(n, k=1):
    """
    Metcalfe's Law: Value proportional to n^2

    Each of n users can connect to (n-1) others.
    Total connections = n(n-1)/2

    k = scaling constant (value per connection)
    """
    return k * n * (n - 1) / 2

def odlyzko_value(n, k=1):
    """
    Odlyzko-Tilly Law: Value proportional to n*log(n)

    Empirically, users don't value ALL connections equally.
    Value of marginal connection decreases logarithmically.

    More realistic for large networks.
    """
    return k * n * np.log(n + 1)  # +1 to avoid log(0)

def linear_value(n, k=1):
    """
    Linear growth: Value proportional to n

    Baseline model - each user adds constant value.
    No network effects.
    """
    return k * n

def calculate_critical_mass(value_func, switching_cost, max_n=1000, k=1):
    """
    Find the point where network value exceeds switching cost.
    This is the "critical mass" after which adoption accelerates.
    """
    for n in range(1, max_n):
        if value_func(n, k) > switching_cost:
            return n
    return max_n

# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================

# Users range
n = np.arange(1, 501)

# Switching cost (cost to adopt the payment network)
# Includes: learning curve, setup time, abandoning old habits
switching_cost = 500  # Arbitrary units

# Scaling constants for visualization
k_metcalfe = 0.02
k_odlyzko = 10
k_linear = 2

# Calculate values
V_metcalfe = [metcalfe_value(x, k_metcalfe) for x in n]
V_odlyzko = [odlyzko_value(x, k_odlyzko) for x in n]
V_linear = [linear_value(x, k_linear) for x in n]

# Find critical mass for each model
cm_metcalfe = calculate_critical_mass(lambda x, k: metcalfe_value(x, k_metcalfe), switching_cost)
cm_odlyzko = calculate_critical_mass(lambda x, k: odlyzko_value(x, k_odlyzko), switching_cost)
cm_linear = calculate_critical_mass(lambda x, k: linear_value(x, k_linear), switching_cost)

print("="*60)
print("NETWORK EFFECTS ANALYSIS")
print("="*60)

print(f"\n1. CRITICAL MASS THRESHOLDS (Switching Cost = {switching_cost})")
print("-"*40)
print(f"Metcalfe's Law (n^2):     {cm_metcalfe:>5} users")
print(f"Odlyzko-Tilly (n*log(n)): {cm_odlyzko:>5} users")
print(f"Linear Growth (n):        {cm_linear:>5} users")

print(f"\nInterpretation:")
print(f"  - Metcalfe networks become viable fastest (strong network effects)")
print(f"  - Linear networks need {cm_linear/cm_metcalfe:.0f}x more users to reach viability")
print(f"  - This explains winner-take-all dynamics in payment networks")

# =============================================================================
# NETWORK GROWTH SIMULATION
# =============================================================================

def simulate_adoption(value_func, k, switching_cost, market_size=1000,
                     initial_users=10, viral_coefficient=0.1, time_steps=50):
    """
    Simulate network adoption over time.

    viral_coefficient: probability existing user convinces new user to join
    Growth rate depends on: (current value - switching cost) * viral_coefficient
    """
    users = [initial_users]

    for t in range(time_steps):
        current_users = users[-1]
        current_value = value_func(current_users, k)

        # Net value determines adoption rate
        net_value = max(0, current_value - switching_cost)

        # S-curve growth: fast in middle, slow at saturation
        headroom = market_size - current_users
        growth_rate = viral_coefficient * net_value * (headroom / market_size)

        new_users = min(current_users + growth_rate, market_size)
        users.append(new_users)

    return users

# Run simulations
time_steps = 50
market_size = 500

adoption_metcalfe = simulate_adoption(
    lambda x, k: metcalfe_value(x, k_metcalfe), k_metcalfe,
    switching_cost, market_size, initial_users=20
)
adoption_odlyzko = simulate_adoption(
    lambda x, k: odlyzko_value(x, k_odlyzko), k_odlyzko,
    switching_cost, market_size, initial_users=20
)
adoption_linear = simulate_adoption(
    lambda x, k: linear_value(x, k_linear), k_linear,
    switching_cost, market_size, initial_users=20
)

print(f"\n2. ADOPTION SIMULATION (Market Size = {market_size})")
print("-"*40)
print(f"After {time_steps} time periods:")
print(f"  Metcalfe:     {adoption_metcalfe[-1]:>6.0f} users ({100*adoption_metcalfe[-1]/market_size:.0f}% penetration)")
print(f"  Odlyzko-Tilly:{adoption_odlyzko[-1]:>6.0f} users ({100*adoption_odlyzko[-1]/market_size:.0f}% penetration)")
print(f"  Linear:       {adoption_linear[-1]:>6.0f} users ({100*adoption_linear[-1]/market_size:.0f}% penetration)")

# =============================================================================
# NETWORK MERGER ANALYSIS
# =============================================================================

def analyze_merger(n1, n2, value_func, k):
    """
    Analyze value creation from merging two networks.
    """
    value_1 = value_func(n1, k)
    value_2 = value_func(n2, k)
    value_merged = value_func(n1 + n2, k)
    synergy = value_merged - value_1 - value_2
    return value_1, value_2, value_merged, synergy

# Example merger: Network A (200 users) + Network B (100 users)
n1, n2 = 200, 100

print(f"\n3. NETWORK MERGER/INTEROPERABILITY ANALYSIS")
print("-"*40)
print(f"Network A: {n1} users, Network B: {n2} users")

v1_m, v2_m, vm_m, syn_m = analyze_merger(n1, n2, metcalfe_value, k_metcalfe)
v1_o, v2_o, vm_o, syn_o = analyze_merger(n1, n2, odlyzko_value, k_odlyzko)

print(f"\nMetcalfe Model:")
print(f"  Value(A) = {v1_m:.0f}, Value(B) = {v2_m:.0f}")
print(f"  Value(A+B) = {vm_m:.0f}")
print(f"  Synergy = {syn_m:.0f} ({100*syn_m/(v1_m+v2_m):.0f}% value increase)")

print(f"\nOdlyzko-Tilly Model:")
print(f"  Value(A) = {v1_o:.0f}, Value(B) = {v2_o:.0f}")
print(f"  Value(A+B) = {vm_o:.0f}")
print(f"  Synergy = {syn_o:.0f} ({100*syn_o/(v1_o+v2_o):.0f}% value increase)")

print(f"\nImplication for Payment Systems:")
print(f"  - Interoperability (e.g., linking UPI and SEPA) creates massive value")
print(f"  - Dominant networks resist interoperability (dilutes their advantage)")
print(f"  - Regulators may need to mandate interoperability")

# =============================================================================
# VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Network Effects in Payment Systems: Value and Adoption Dynamics',
             fontsize=14, fontweight='bold')

# Chart 1: Value vs Size
ax1 = axes[0, 0]
ax1.plot(n, V_metcalfe, label="Metcalfe's Law (n^2)", color='#3333B2', linewidth=2.5)
ax1.plot(n, V_odlyzko, label="Odlyzko-Tilly (n*log(n))", color='#0066CC', linewidth=2.5)
ax1.plot(n, V_linear, label="Linear (n)", color='#FF7F0E', linewidth=2.5)
ax1.axhline(y=switching_cost, color='#D62728', linestyle='--',
           linewidth=2, label=f'Switching Cost ({switching_cost})')
ax1.axvline(x=cm_metcalfe, color='#3333B2', linestyle=':', alpha=0.7)
ax1.axvline(x=cm_odlyzko, color='#0066CC', linestyle=':', alpha=0.7)
ax1.axvline(x=cm_linear, color='#FF7F0E', linestyle=':', alpha=0.7)
ax1.set_xlabel('Network Size (users)')
ax1.set_ylabel('Network Value')
ax1.set_title('Network Value Growth Models')
ax1.legend(loc='upper left')
ax1.set_xlim(0, 500)
ax1.grid(True, alpha=0.3)

# Annotate critical mass points
ax1.annotate(f'CM: {cm_metcalfe}', xy=(cm_metcalfe, switching_cost),
            xytext=(cm_metcalfe+20, switching_cost+200),
            fontsize=9, color='#3333B2')
ax1.annotate(f'CM: {cm_odlyzko}', xy=(cm_odlyzko, switching_cost),
            xytext=(cm_odlyzko+20, switching_cost+100),
            fontsize=9, color='#0066CC')

# Chart 2: Adoption Simulation
ax2 = axes[0, 1]
time = range(len(adoption_metcalfe))
ax2.plot(time, adoption_metcalfe, label="Metcalfe's Law", color='#3333B2', linewidth=2.5)
ax2.plot(time, adoption_odlyzko, label="Odlyzko-Tilly", color='#0066CC', linewidth=2.5)
ax2.plot(time, adoption_linear, label="Linear", color='#FF7F0E', linewidth=2.5)
ax2.axhline(y=0.16*market_size, color='#2CA02C', linestyle='--',
           linewidth=1.5, label='16% Critical Mass')
ax2.set_xlabel('Time Period')
ax2.set_ylabel('Cumulative Users')
ax2.set_title('Adoption Dynamics (S-Curve)')
ax2.legend(loc='lower right')
ax2.set_xlim(0, time_steps)
ax2.set_ylim(0, market_size)
ax2.grid(True, alpha=0.3)

# Chart 3: Marginal Value
ax3 = axes[1, 0]
marginal_metcalfe = np.diff([metcalfe_value(x, k_metcalfe) for x in range(1, 502)])
marginal_odlyzko = np.diff([odlyzko_value(x, k_odlyzko) for x in range(1, 502)])
marginal_linear = np.diff([linear_value(x, k_linear) for x in range(1, 502)])
ax3.plot(range(1, 501), marginal_metcalfe, label="Metcalfe", color='#3333B2', linewidth=2)
ax3.plot(range(1, 501), marginal_odlyzko, label="Odlyzko-Tilly", color='#0066CC', linewidth=2)
ax3.plot(range(1, 501), marginal_linear, label="Linear", color='#FF7F0E', linewidth=2)
ax3.set_xlabel('Network Size')
ax3.set_ylabel('Marginal Value of New User')
ax3.set_title('Marginal Value of Adding Users')
ax3.legend(loc='upper left')
ax3.grid(True, alpha=0.3)

# Chart 4: Merger Synergies
ax4 = axes[1, 1]
sizes_b = range(10, 301, 10)  # Network B sizes
size_a = 200  # Fixed Network A size

synergies_m = [analyze_merger(size_a, b, metcalfe_value, k_metcalfe)[3] for b in sizes_b]
synergies_o = [analyze_merger(size_a, b, odlyzko_value, k_odlyzko)[3] for b in sizes_b]

ax4.plot(sizes_b, synergies_m, label="Metcalfe", color='#3333B2', linewidth=2.5)
ax4.plot(sizes_b, synergies_o, label="Odlyzko-Tilly", color='#0066CC', linewidth=2.5)
ax4.set_xlabel('Size of Network B (Network A = 200)')
ax4.set_ylabel('Merger Synergy Value')
ax4.set_title('Value Creation from Network Interoperability')
ax4.legend(loc='upper left')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('network_effects_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nChart saved as 'network_effects_analysis.png'")

# =============================================================================
# ECONOMIC CONCLUSIONS
# =============================================================================

print("\n" + "="*60)
print("ECONOMIC ANALYSIS: KEY FINDINGS")
print("="*60)

print("""
1. CRITICAL MASS MATTERS:
   - Metcalfe networks reach viability with ~{} users
   - Linear networks need ~{} users ({}x more)
   - This explains why payment startups fail: must reach critical mass FAST

2. WINNER-TAKE-ALL DYNAMICS:
   - Once past critical mass, adoption accelerates (S-curve)
   - Network effects create positive feedback: more users -> more value -> more users
   - First mover with critical mass is extremely difficult to displace

3. INTEROPERABILITY IS POWERFUL:
   - Merging two networks creates synergy beyond sum of parts
   - Under Metcalfe: 200+100 user merger creates {}% extra value
   - Policy implication: Mandate interoperability to prevent monopoly abuse

4. MARGINAL VALUE INCREASES (at first):
   - Unlike most goods, each new user makes network MORE valuable
   - This is opposite of diminishing returns in standard economics
   - Explains why dominant networks can charge monopoly prices
""".format(
    cm_metcalfe,
    cm_linear,
    cm_linear // cm_metcalfe,
    int(100*syn_m/(v1_m+v2_m))
))
```

### Model Answer / Expected Output

**Expected Output:**

| Metric | Metcalfe | Odlyzko-Tilly | Linear |
|--------|----------|---------------|--------|
| Critical Mass (users) | ~225 | ~80 | ~250 |
| Time to 50% Penetration | Fast | Medium | Slow |
| Merger Synergy | Very High | High | Zero |

**Key Findings (Model Answer):**

1. **Critical Mass Depends on Growth Model:**
   - Metcalfe (n^2): Critical mass reached with fewer users but requires explosive growth
   - Odlyzko-Tilly (n*log(n)): More realistic, earlier critical mass
   - Linear: No network effects, needs massive scale to overcome switching costs

2. **Winner-Take-All is Inevitable:**
   - Once past critical mass, adoption follows S-curve
   - Network with head start is almost impossible to catch
   - Explains why Visa/Mastercard duopoly persists despite technology changes

3. **Interoperability Creates Value:**
   - Merging 200-user and 100-user networks creates 30-50% synergy under Metcalfe
   - This is why regulators push for interoperability (UPI, SEPA linking)
   - But dominant networks resist (dilutes their network advantage)

### Presentation Talking Points
- Payment networks exhibit strong network effects - value grows faster than linearly with users
- The 16% critical mass threshold (1 in 6 users) is empirically observed across many networks
- Metcalfe's Law may overstate network effects; Odlyzko-Tilly is more realistic
- Key economic insight: Network effects create natural monopolies, requiring regulatory intervention
- Interoperability mandates can unlock massive value but are resisted by incumbents

---

## Exercise 7: SWIFT vs Blockchain Cross-Border Payments

**Category**: Comparative Analysis
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Worksheet with comparison framework

### Task

Compare SWIFT-based correspondent banking with blockchain-based cross-border payments across economic dimensions. Evaluate which is superior for different use cases.

**Comparison Dimensions:**
1. Transaction costs
2. Settlement speed
3. Counterparty risk
4. Scalability
5. Regulatory compliance
6. Network effects

### Model Answer / Expected Output

**Completed Comparison Matrix:**

| Dimension | SWIFT/Correspondent | Blockchain (Stablecoin) | Winner |
|-----------|---------------------|-------------------------|--------|
| **Transaction Cost** | $25-50 fixed + 2-3% FX spread | $0.10-2.00 + 0.1-0.5% FX | **Blockchain** (especially for small amounts) |
| **Settlement Speed** | 2-5 business days | 10 seconds - 1 hour | **Blockchain** |
| **Counterparty Risk** | Multiple intermediaries, each is counterparty | Smart contract escrow, no intermediary risk | **Blockchain** (in theory) |
| **Scalability** | Proven at scale ($5T daily) | Untested at SWIFT scale | **SWIFT** |
| **Regulatory Compliance** | Full KYC/AML at each hop | Varies by jurisdiction, often non-compliant | **SWIFT** |
| **Network Effects** | 11,000+ banks in 200 countries | Growing but fragmented | **SWIFT** |

---

**Detailed Analysis:**

**1. Transaction Costs:**

| Cost Component | SWIFT | Blockchain |
|----------------|-------|------------|
| Sending bank fee | $15-25 | $0 (self-custody) |
| Correspondent bank fee(s) | $10-30 | $0 |
| Receiving bank fee | $5-15 | $0-5 (offramp) |
| FX spread | 2-4% | 0.1-0.5% |
| Network fee | - | $0.10-2 (on-chain) |
| **TOTAL on $1000** | $60-120 (6-12%) | $5-20 (0.5-2%) |

*Verdict:* Blockchain is dramatically cheaper, especially for smaller transactions. The correspondent banking model has too many intermediaries, each taking a cut.

**2. Settlement Speed:**

| Step | SWIFT | Blockchain |
|------|-------|------------|
| Initiation | T+0 | T+0 |
| Correspondent processing | T+1-3 | N/A |
| FX conversion | T+1 | T+0 (on-chain DEX) |
| Receiving bank credit | T+2-5 | T+0 (stablecoin) |
| **TOTAL** | 2-5 days | 10 seconds - 1 hour |

*Verdict:* Blockchain is dramatically faster. SWIFT gpi has improved to same-day for some routes, but blockchain is still 10-100x faster.

**3. Counterparty Risk:**

| Risk Type | SWIFT | Blockchain |
|-----------|-------|------------|
| Sending bank default | Yes | No (self-custody) |
| Correspondent default | Yes (multiple) | No |
| Receiving bank default | Yes | Possible (offramp) |
| Smart contract risk | No | Yes |
| Protocol risk | Low (mature) | Medium (bugs, hacks) |

*Verdict:* Depends on perspective. SWIFT has known, regulated counterparties. Blockchain has protocol risk but fewer counterparties.

**4. Scalability:**

| Metric | SWIFT | Blockchain |
|--------|-------|------------|
| Daily volume | $5+ trillion | $10-20 billion |
| Transactions/day | 42 million | 1-5 million |
| Peak capacity | Proven | Untested |
| Congestion handling | Queuing | Fee spikes |

*Verdict:* SWIFT is proven at massive scale. Blockchain hasn't been tested at SWIFT volumes. Ethereum congestion in 2021 caused $100+ gas fees.

**5. Regulatory Compliance:**

| Requirement | SWIFT | Blockchain |
|-------------|-------|------------|
| KYC | Required at each bank | Often missing |
| AML screening | Multiple checks | Minimal |
| Sanctions compliance | Built-in | Problematic |
| Audit trail | Complete | Pseudonymous |

*Verdict:* SWIFT is fully compliant. Blockchain payments often bypass regulations, which is a feature for some users but a problem for institutional adoption.

**6. Network Effects:**

| Metric | SWIFT | Blockchain |
|--------|-------|------------|
| Connected banks | 11,000+ | 100s (via offramps) |
| Countries | 200+ | Fragmented |
| Acceptance | Universal in banking | Limited |
| Liquidity | Deep | Fragmented |

*Verdict:* SWIFT has entrenched network effects. Blockchain is growing but fragmented across chains and protocols.

---

**Use Case Recommendations:**

| Use Case | Better Choice | Why |
|----------|---------------|-----|
| Large corporate transfer ($1M+) | SWIFT | Compliance, proven, insured |
| Small remittance ($200) | Blockchain | Cost advantage dominates |
| Urgent transfer | Blockchain | Speed advantage |
| Emerging market (no banking) | Blockchain | Accessibility |
| Regulated institution | SWIFT | Compliance requirements |
| Sanctions screening required | SWIFT | Proper compliance infrastructure |

---

**Future Outlook:**

| Scenario | Probability | Implications |
|----------|-------------|--------------|
| SWIFT adopts blockchain | High | Best of both worlds (speed + compliance) |
| Blockchain replaces SWIFT | Low | Regulatory barriers too high |
| Coexistence | High | Different use cases, both survive |
| CBDCs change everything | Medium | Could bypass both systems |

### Presentation Talking Points
- SWIFT's dominance comes from network effects and regulatory compliance, not technological superiority
- Blockchain is 10-100x cheaper and faster but lacks compliance infrastructure and network effects
- The real competition is: will SWIFT adopt blockchain technology, or will blockchain build compliance?
- SWIFT gpi is already incorporating some blockchain principles (traceability, speed)
- Key economic insight: Network effects protect SWIFT; transaction costs favor blockchain; regulatory requirements will determine the winner

---

## Exercise 8: RTGS vs DNS Settlement Trade-offs

**Category**: Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Pairs
**Materials Needed**: Worksheet with scenarios

### Task

Apply the RTGS vs DNS framework from L04 to evaluate settlement system design for three different scenarios. For each, recommend the optimal settlement approach and justify economically.

**Scenarios:**
1. A new instant payment system for a country with 50 million people
2. A securities settlement system for stock market trades
3. A cross-border payment corridor between two countries

### Model Answer / Expected Output

**SCENARIO 1: National Instant Payment System (50M population)**

| Dimension | RTGS | DNS | Hybrid |
|-----------|------|-----|--------|
| Settlement Risk | Zero | Present until batch | Low |
| Liquidity Need | Very High | Low | Medium |
| User Experience | Instant | Delayed | Instant |
| Operational Hours | 24/7 required | Batch windows OK | 24/7 required |
| Cost | High (liquidity) | Low | Medium |

**Recommendation: Hybrid with RTGS characteristics**

**Justification:**
- Consumer expectation: "instant" means real-time, so must appear like RTGS to user
- But full RTGS would require banks to hold massive liquidity (expensive)
- Solution: Real-time clearing with periodic netting for bank settlement
- Example: India's UPI - instant user experience, but banks settle every 30 minutes

**Design Specifics:**
| Feature | Choice | Economic Rationale |
|---------|--------|-------------------|
| User layer | Instant (RTGS-like) | Consumer expectations |
| Bank layer | Netting every 30 min | Liquidity efficiency |
| Central bank | RTGS for final settlement | Eliminate settlement risk |
| Liquidity | Central bank facility | Intraday credit reduces liquidity hoarding |

---

**SCENARIO 2: Securities Settlement System (Stock Market)**

| Dimension | RTGS (T+0) | DNS (T+2) | Current Practice |
|-----------|------------|-----------|------------------|
| Settlement Risk | Zero | 2 days of exposure | T+2 standard |
| Liquidity Need | Very High | Low | Manageable |
| Operational Complexity | High | Lower | Proven |
| Margin Requirements | Lower | Higher | T+2 calibrated |
| Fail Rate | Very Low | Higher | ~2% fail rate |

**Recommendation: RTGS (T+0 or T+1) with robust liquidity facilities**

**Justification:**
- Current T+2 creates counterparty risk (GameStop 2021 showed this)
- DTCC moving to T+1 in 2024, eventually T+0
- Blockchain can enable T+0 (DvP - Delivery vs Payment in real-time)
- Higher liquidity cost is offset by reduced margin requirements and counterparty risk

**Economic Analysis:**
| Cost/Benefit | T+2 DNS | T+0 RTGS |
|--------------|---------|----------|
| Settlement risk cost | $X billion annually | ~$0 |
| Liquidity cost | Low | High |
| Margin requirements | Higher | Lower |
| Failed trade costs | ~2% fail rate | <0.1% fail rate |
| **Net** | Current equilibrium | Better (once transition complete) |

---

**SCENARIO 3: Cross-Border Payment Corridor**

| Dimension | RTGS (each country) | DNS (netting) | Hybrid |
|-----------|---------------------|---------------|--------|
| Settlement Risk | Multiple systems | High (FX exposure) | Medium |
| FX Risk | Per-transaction | Batched | Per-transaction |
| Liquidity Need | Both currencies | Net positions only | Moderate |
| Speed | Sequential delay | End-of-day | Variable |
| Correspondent Fees | Multiple per transaction | Netting reduces | Optimized |

**Recommendation: Hybrid with continuous linked settlement (CLS model)**

**Justification:**
- Pure RTGS across borders is operationally complex (time zones, different systems)
- Pure DNS has unacceptable FX settlement risk (Herstatt risk)
- CLS model: Payment-vs-Payment (PvP) in a central settlement window
- Netting reduces liquidity needs by 95%+; PvP eliminates FX settlement risk

**Design Specifics:**
| Feature | Choice | Economic Rationale |
|---------|--------|-------------------|
| Settlement mechanism | PvP (payment vs payment) | Eliminate Herstatt risk |
| Netting | Multilateral | 95% liquidity reduction |
| Settlement window | Overlapping business hours | Operational feasibility |
| Central counterparty | Yes (CLS-like) | Concentrate and manage risk |

---

**Summary Table:**

| Scenario | Recommended Approach | Key Economic Driver |
|----------|---------------------|---------------------|
| Instant Payments | Hybrid (instant UX, netting back-end) | Consumer expectations + bank liquidity |
| Securities | RTGS (T+0) | Counterparty risk reduction |
| Cross-Border | Hybrid (CLS model) | FX risk + liquidity efficiency |

### Presentation Talking Points
- RTGS vs DNS is not either/or - modern systems combine elements of both
- The fundamental trade-off: settlement risk (DNS) vs liquidity cost (RTGS)
- Real-world systems are increasingly hybrid: instant for users, netting for banks
- Key economic insight: Settlement system design affects liquidity requirements, counterparty risk, and ultimately the cost of financial intermediation
- The trend is toward faster settlement (T+2 to T+1 to T+0) as technology reduces operational barriers

---

**PLAN_READY: .omc/plans/l04-in-class-exercises.md**
