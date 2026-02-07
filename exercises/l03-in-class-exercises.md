# L03 In-Class Exercises: Central Bank Digital Currencies (CBDCs)

## Plan Metadata
- **Created**: 2026-02-04
- **Lesson**: L03 - Central Bank Digital Currencies (CBDCs)
- **Target Audience**: BSc students (just completed L03)
- **Time Allocation**: 30 minutes work + 5 minutes presentation per exercise
- **Instructor Choice**: Select 1-2 exercises per session based on class size and learning goals

---

## Exercise Overview

| # | Title | Category | Group Size | Materials |
|---|-------|----------|------------|-----------|
| 1 | Global CBDC Tracker Dashboard | Python/Data | Individual or Pairs | Laptop with Python |
| 2 | CBDC Design Matrix | Framework Application | Groups of 3-4 | Printed Matrix Worksheet |
| 3 | CBDC Showdown: e-CNY vs Digital Euro vs Sand Dollar | Case Study | Groups of 3-4 | Case Materials |
| 4 | "CBDCs Will Destroy Commercial Banking" | Structured Debate | Two Teams (4-6 each) | Timer |
| 5 | Design a CBDC for a Developing Nation | Creative/Design | Groups of 3-4 | Whiteboard/Paper |
| 6 | Bank Disintermediation Risk Calculator | Python/Modeling | Pairs | Laptop with Python |
| 7 | Tiered Remuneration Design Challenge | Policy Design | Groups of 3-4 | Worksheet + Calculator |

---

## Exercise 1: Global CBDC Tracker Dashboard

**Category**: Python/Data
**Time**: 30 min work + 5 min presentation
**Group Size**: Individual or Pairs
**Materials Needed**: Laptop with Python (pandas, matplotlib, plotly optional), internet access for data verification

### Task

Create a visualization showing the current state of CBDC development worldwide. Analyze regional patterns and answer: Which regions are leading CBDC adoption, and what explains the variation?

**Note:** CBDC status data as of February 2025. Check [cbdctracker.org](https://www.cbdctracker.org) for current status.

### Complete Code

```python
"""
Global CBDC Development Tracker
L03 Exercise - Economics of Digital Finance

Requirements: pip install pandas matplotlib numpy
Optional: pip install plotly for interactive version

Data Source: Atlantic Council CBDC Tracker (2024)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# =============================================================================
# CBDC STATUS DATA (2024)
# Data as of February 2025
# Source: Atlantic Council CBDC Tracker
# =============================================================================

cbdc_data = {
    # Launched CBDCs (11 countries)
    'Launched': {
        'countries': ['Bahamas', 'Jamaica', 'Nigeria', 'Eastern Caribbean',
                      'Antigua and Barbuda', 'Dominica', 'Grenada',
                      'Saint Kitts and Nevis', 'Saint Lucia',
                      'Saint Vincent and the Grenadines', 'Montserrat'],
        'region': ['Caribbean', 'Caribbean', 'Africa', 'Caribbean',
                   'Caribbean', 'Caribbean', 'Caribbean', 'Caribbean',
                   'Caribbean', 'Caribbean', 'Caribbean'],
        'population_millions': [0.4, 2.8, 220, 0.6, 0.1, 0.07, 0.1,
                                0.05, 0.18, 0.1, 0.005],
        'year_launched': [2020, 2022, 2021, 2021, 2021, 2021, 2021,
                          2021, 2021, 2021, 2021]
    },
    # Pilot Stage (21 countries - key examples)
    'Pilot': {
        'countries': ['China', 'India', 'Russia', 'Brazil', 'South Korea',
                      'Thailand', 'UAE', 'Saudi Arabia', 'Hong Kong',
                      'Singapore', 'South Africa', 'Ghana', 'Malaysia',
                      'Kazakhstan', 'Ukraine', 'Iran', 'Turkey',
                      'Indonesia', 'Vietnam', 'Laos', 'Cambodia'],
        'region': ['Asia', 'Asia', 'Europe', 'Americas', 'Asia',
                   'Asia', 'Middle East', 'Middle East', 'Asia',
                   'Asia', 'Africa', 'Africa', 'Asia',
                   'Asia', 'Europe', 'Middle East', 'Europe',
                   'Asia', 'Asia', 'Asia', 'Asia'],
        'population_millions': [1400, 1400, 144, 215, 52,
                                70, 10, 35, 7.5,
                                6, 60, 33, 33,
                                19, 44, 87, 85,
                                275, 100, 7.4, 17],
        'pilot_start_year': [2020, 2022, 2023, 2023, 2021,
                             2022, 2023, 2022, 2022,
                             2022, 2023, 2022, 2023,
                             2021, 2021, 2022, 2023,
                             2023, 2023, 2022, 2020]
    },
    # Development Stage (33 countries - key examples)
    'Development': {
        'countries': ['Eurozone', 'United Kingdom', 'Australia', 'Canada',
                      'Sweden', 'Norway', 'Israel', 'New Zealand',
                      'Taiwan', 'Philippines', 'Bangladesh', 'Peru',
                      'Chile', 'Argentina', 'Morocco', 'Egypt'],
        'region': ['Europe', 'Europe', 'Oceania', 'Americas',
                   'Europe', 'Europe', 'Middle East', 'Oceania',
                   'Asia', 'Asia', 'Asia', 'Americas',
                   'Americas', 'Americas', 'Africa', 'Africa'],
        'population_millions': [340, 67, 26, 40,
                                10, 5.5, 9, 5,
                                24, 115, 170, 33,
                                19, 46, 37, 104]
    },
    # Research Stage (68 countries - key examples)
    'Research': {
        'countries': ['United States', 'Japan', 'Switzerland', 'Mexico',
                      'Poland', 'Czech Republic', 'Austria', 'Belgium',
                      'Iceland', 'Kenya', 'Tanzania', 'Ethiopia'],
        'region': ['Americas', 'Asia', 'Europe', 'Americas',
                   'Europe', 'Europe', 'Europe', 'Europe',
                   'Europe', 'Africa', 'Africa', 'Africa'],
        'population_millions': [335, 125, 9, 130,
                                38, 10.5, 9, 11.5,
                                0.4, 54, 65, 120]
    }
}

# Color scheme matching course style
MLPURPLE = '#3333B2'
MLBLUE = '#0066CC'
MLORANGE = '#FF7F0E'
MLGREEN = '#2CA02C'
MLRED = '#D62728'

# =============================================================================
# (a) Population-Weighted Coverage Calculation
# Task: Calculate total population (in millions) covered by each CBDC stage.
# Hint: Sum the 'population_millions' list for each stage in cbdc_data.
# =============================================================================

pop_launched = None  # YOUR CODE HERE — sum population_millions for 'Launched'
pop_pilot = None  # YOUR CODE HERE — sum population_millions for 'Pilot'
pop_development = None  # YOUR CODE HERE — sum population_millions for 'Development'
pop_research = None  # YOUR CODE HERE — sum population_millions for 'Research'

# Print your results to verify (expected: Pilot should be largest due to China + India)
print(f"Launched: {pop_launched} million")
print(f"Pilot: {pop_pilot} million")
print(f"Development: {pop_development} million")
print(f"Research: {pop_research} million")

# =============================================================================
# (b) Bar Chart: CBDC Projects by Development Stage
# Task: Create a bar chart showing the number of countries per stage.
# Given data:
stages = ['Launched', 'Pilot', 'Development', 'Research', 'Inactive']
counts = [11, 21, 33, 68, 14]
colors = [MLGREEN, MLBLUE, MLORANGE, MLPURPLE, 'gray']
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
ax1 = axes[0, 0]

# YOUR CODE HERE — create a bar chart on ax1 using stages, counts, colors
# Hint: Use ax1.bar(...), set ylabel, title, and add count labels above each bar
pass  # YOUR CODE HERE

ax1.set_ylim(0, 80)
ax1.grid(True, alpha=0.3, axis='y')

# =============================================================================
# (c) Regional Distribution: Groupby + Horizontal Bar Chart
# Task: Count how many countries are in each region across ALL stages,
#        sort by count (descending), and plot a horizontal bar chart.
# Hint: Loop over stages and regions in cbdc_data, use defaultdict(int).
# =============================================================================

ax3 = axes[1, 0]

region_counts = None  # YOUR CODE HERE — build a dict mapping region -> count
regions = None  # YOUR CODE HERE — sorted list of region names (descending by count)
region_values = None  # YOUR CODE HERE — corresponding counts

# YOUR CODE HERE — create a horizontal bar chart on ax3 using ax3.barh(...)
# Add count labels to the right of each bar
pass  # YOUR CODE HERE

ax3.set_xlabel('Number of Countries', fontweight='bold')
ax3.set_title('CBDC Projects by Region', fontweight='bold', color=MLPURPLE)
ax3.grid(True, alpha=0.3, axis='x')

# =============================================================================
# (d) Timeline Plot: Cumulative Launches and Pilots Over Time
# Task: Plot two line series on ax4 showing cumulative launched and pilot
#        countries from 2019-2024. Add annotations for key events.
# Given data:
years = [2019, 2020, 2021, 2022, 2023, 2024]
launched_cumulative = [0, 1, 9, 11, 11, 11]   # Bahamas, then Eastern Caribbean + Nigeria
pilot_cumulative = [0, 1, 3, 10, 21, 21]      # China pilot, gradual expansion
# =============================================================================

ax4 = axes[1, 1]

# YOUR CODE HERE — plot two line series on ax4 (launched and pilot cumulative)
# Add markers, legend, axis labels, title, and annotations for key events
# Hint: Use ax4.plot(...), ax4.annotate(...)
pass  # YOUR CODE HERE

# Panel 2 (pie chart) is provided for you
ax2 = axes[0, 1]
if pop_launched is not None:
    pop_by_stage = [pop_launched, pop_pilot, pop_development, pop_research]
    stage_labels = ['Launched', 'Pilot', 'Development', 'Research']
    ax2.pie(pop_by_stage, labels=stage_labels, autopct='%1.1f%%',
            colors=[MLGREEN, MLBLUE, MLORANGE, MLPURPLE],
            explode=[0.05, 0.05, 0, 0], startangle=90)
    ax2.set_title('Population Coverage by CBDC Stage\n(Sample Countries, Billions)',
                  fontweight='bold', color=MLPURPLE)
else:
    ax2.text(0.5, 0.5, 'Complete part (a) first', ha='center', va='center', fontsize=14)

plt.tight_layout()
plt.savefig('cbdc_global_tracker.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# INTERPRETATION (fill in after running your code)
# =============================================================================
print("\n" + "="*70)
print("KEY FINDINGS: Global CBDC Development Status")
print("="*70)
print("""
1. STAGE DISTRIBUTION:
   - Which stage has the most countries? Why?
   - YOUR ANSWER HERE

2. POPULATION COVERAGE:
   - Which stage covers the most people? Why?
   - YOUR ANSWER HERE

3. REGIONAL PATTERNS:
   - Which region leads? What explains this?
   - YOUR ANSWER HERE

4. KEY INSIGHT:
   - What is the relationship between country size and launch speed?
   - YOUR ANSWER HERE
""")
```

### Model Answer / Expected Output

**Expected Visualization Description:**
- Four-panel dashboard showing:
  1. Bar chart: Stage distribution showing most countries in Research (68), few Launched (11)
  2. Pie chart: Population coverage dominated by Pilot stage (China + India = 2.8B people)
  3. Horizontal bar: Regional distribution showing Asia leading, Caribbean concentrated in launches
  4. Line chart: Timeline showing acceleration since 2020

**Key Finding (Model Answer):**

The global CBDC landscape reveals a **inverse relationship between economic size and launch speed**:

1. **Small nations launch first** - Caribbean islands (Bahamas, Jamaica, Eastern Caribbean) have launched CBDCs. Why?
   - Lower systemic risk (small financial systems)
   - Stronger financial inclusion motivation (unbanked populations)
   - Testing ground for larger economies

2. **Large economies proceed cautiously** - US, Japan in research; EU, UK in development
   - Systemic risk concerns (bank disintermediation)
   - Political economy (privacy debates, bank lobbying)
   - Opportunity cost of getting it wrong

3. **China is the outlier** - Large economy with aggressive pilot
   - State control of financial system enables rapid testing
   - Strategic motivation (reduce dollar dependence)
   - Less privacy concern in political culture

4. **Regional patterns reflect development priorities**:
   - Asia: Financial inclusion + strategic autonomy
   - Europe: Payment sovereignty + declining cash
   - Americas: Privacy concerns + existing payment infrastructure

### Presentation Talking Points
- The map reveals that CBDC adoption is NOT correlated with economic development
- Caribbean nations are "laboratories" for CBDC experimentation
- China's e-CNY is by far the most consequential pilot by population
- The US "wait and see" approach may mean losing first-mover advantage
- Key economic insight: Small islands bear low risk but provide limited learning for systemic implications in large economies

---

## Exercise 2: CBDC Design Matrix

**Category**: Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Printed matrix worksheet, pens

### Task

Evaluate three CBDC design choices across key economic criteria. Score each design 1-5 on each criterion, identify the optimal design for different country contexts, and explain the trade-offs.

**Note: A "Pareto efficient" design means you cannot improve one attribute (e.g., privacy) without making another worse (e.g., AML compliance). The goal is to find designs on the Pareto frontier---the set of best possible trade-offs.**

**CBDC Designs to Evaluate**:
1. **Design A**: Retail, Account-Based, Interest-Bearing, 3000 EUR Limit
2. **Design B**: Retail, Token-Based, Non-Interest-Bearing, No Limit
3. **Design C**: Wholesale Only, Account-Based, Interest-Bearing, No Retail Access

**Scoring Criteria** (1 = Poor, 5 = Excellent):
- Financial Inclusion
- Privacy Protection
- Monetary Policy Transmission
- Banking System Stability
- Operational Simplicity
- Financial Crime Prevention (AML/CFT)

### Model Answer / Expected Output

**Completed Design Matrix (Consensus Answer):**

| Criterion | Design A (Retail Account, Limited) | Design B (Retail Token, Unlimited) | Design C (Wholesale Only) |
|-----------|-----------------------------------|-------------------------------------|---------------------------|
| **Financial Inclusion** | **4** | **5** | **1** |
| **Privacy Protection** | **2** | **4** | **3** |
| **Monetary Policy Transmission** | **5** | **2** | **4** |
| **Banking System Stability** | **4** | **1** | **5** |
| **Operational Simplicity** | **3** | **4** | **5** |
| **AML/CFT Compliance** | **5** | **2** | **5** |
| **TOTAL** | **23** | **18** | **23** |

**Justifications:**

**Design A (Digital Euro Model):**
- Financial Inclusion (4): Good access for banked population, but requires identity verification
- Privacy (2): Account-based means full transaction visibility; privacy concerns
- Monetary Policy (5): Interest-bearing enables direct rate transmission; holding limits prevent over-accumulation
- Banking Stability (4): 3000 EUR limit protects deposits; prevents large-scale flight
- Operational Simplicity (3): Requires identity infrastructure, holding limit enforcement
- AML/CFT (5): Full transaction records, identity verified

**Design B (Digital Cash Model):**
- Financial Inclusion (5): Anonymous access, no ID barriers, like physical cash
- Privacy (4): Token-based can be near-anonymous for small values
- Monetary Policy (2): Non-interest-bearing limits policy transmission; no rate channel
- Banking Stability (1): No limits = potential for rapid deposit flight; digital bank run risk
- Operational Simplicity (4): Simpler offline capability, no identity management
- AML/CFT (2): Anonymous tokens enable money laundering, hard to trace

**Design C (Wholesale Model):**
- Financial Inclusion (1): No public access - only for banks and financial institutions
- Privacy (3): Institutional transactions, less sensitive than retail privacy
- Monetary Policy (4): Improves interbank settlement, indirect transmission
- Banking Stability (5): Does not compete with deposits; enhances rather than threatens banks
- Operational Simplicity (5): Fewer participants, established institutional infrastructure
- AML/CFT (5): Institutional participants already regulated

**Optimal Design by Country Context:**

| Country Type | Recommended Design | Key Reasoning |
|--------------|-------------------|---------------|
| **Advanced Economy (EU, US)** | Design A | Balance all objectives; banking system already developed |
| **Financial Inclusion Priority (Nigeria, India)** | Design B (modified with tiered KYC) | Maximize unbanked access; accept AML trade-off |
| **Banking Hub (Singapore, Switzerland)** | Design C | Wholesale efficiency; protect banking sector |
| **Autocratic State (China)** | Design A without limits | Control + surveillance prioritized |
| **Privacy-Focused (Germany, Nordic)** | Design B with privacy tech | Zero-knowledge proofs for compliance |

**Key Insight:**
There is NO universally optimal CBDC design. The "best" design depends on:
1. Existing financial infrastructure
2. Political preferences (privacy vs. control)
3. Financial inclusion needs
4. Banking sector structure

### Presentation Talking Points
- The Digital Euro (Design A) is a compromise that scores well overall but excels at nothing
- Token-based (Design B) maximizes inclusion but creates stability and AML risks
- Wholesale (Design C) is safest but misses the retail innovation
- Key economic insight: CBDC design is fundamentally about political economy, not just technology - what trade-offs does society accept?
- Different countries will rationally choose different designs based on their constraints and priorities

---

## Exercise 3: CBDC Showdown: e-CNY vs Digital Euro vs Sand Dollar

**Category**: Case Study / Comparative Analysis
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Case handout with data below

### Task

Compare three real CBDC implementations across economic dimensions. Identify what each design reveals about the issuing country's priorities and assess the likelihood of success.

**Case Data Provided:**

**Note:** CBDC status data as of February 2025. Check [cbdctracker.org](https://www.cbdctracker.org) for current status.

| Dimension | e-CNY (China) | Digital Euro (EU) | Sand Dollar (Bahamas) |
|-----------|---------------|-------------------|----------------------|
| **Launch Status** | Pilot (2020-) | Development (expected 2027-28) | Launched (Oct 2020) |
| **Population Covered** | 1.4 billion | 340 million | 400,000 |
| **GDP per capita** | $12,720 | $38,234 | $34,732 |
| **Unbanked Rate** | 3% | 2% | 18% |
| **Technology** | Two-tier (banks distribute) | Two-tier (banks distribute) | Two-tier (authorized FIs) |
| **Privacy Model** | "Controllable anonymity" | Tiered (offline anonymous) | Tiered by transaction size |
| **Interest** | Non-interest-bearing | Non-interest-bearing initially | Non-interest-bearing |
| **Holding Limits** | Tiered (500-50,000 CNY) | ~3,000 EUR proposed | $8,000 personal |
| **Offline Capability** | Yes (NFC) | Planned | Yes |
| **Programmability** | Yes (expiring money tested) | Limited (no expiry planned) | No |
| **Cross-border** | mBridge pilot | EU scope only initially | Bilateral discussions |

### Model Answer / Expected Output

**Comparative Analysis Matrix:**

| Economic Dimension | e-CNY | Digital Euro | Sand Dollar |
|-------------------|-------|--------------|-------------|
| **Primary Motivation** | Strategic (reduce USD dependence, domestic control) | Defensive (payment sovereignty, counter Big Tech) | Inclusion (reach unbanked islands) |
| **Secondary Motivation** | Policy transmission, surveillance capacity | Declining cash replacement | Hurricane resilience, tourism efficiency |
| **Disintermediation Strategy** | Tiered limits, non-interest | Strict limits, no interest | Low limits, education campaign |
| **Privacy Approach** | State access prioritized over individual privacy | Privacy by design (EU values) | Pragmatic tiering |
| **Adoption Success Factors** | Government mandate power, WeChat/Alipay integration | Voluntary adoption, bank distribution | Small scale, high unbanked need |
| **Adoption Risk Factors** | Low demand vs WeChat/Alipay, privacy concerns | Unclear demand, bank resistance | Infrastructure gaps, low volume |

**Country-Specific Analysis:**

**e-CNY (China):**
- **What it reveals**: China prioritizes state control and strategic autonomy over individual privacy
- **Clever design features**:
  - "Controllable anonymity" = anonymous to merchants, visible to state
  - Programmable money tested (stimulus that expires in 3 months)
  - Integration with existing super-apps (WeChat, Alipay) reduces adoption friction
- **Key risk**: Chinese consumers already have excellent digital payments (WeChat/Alipay). Why switch to e-CNY? Government must create incentives (Olympics, tax discounts)
- **Success likelihood**: Medium-High (government can mandate adoption, but organic demand uncertain)

**Digital Euro (EU):**
- **What it reveals**: Europe values privacy and bank coexistence; defensive against US tech dominance
- **Clever design features**:
  - Privacy for offline/small transactions (like cash)
  - Strict holding limits protect banking system
  - Two-tier distribution keeps banks relevant
- **Key risk**: Europeans already have good payment options (cards, instant payments). Unclear consumer demand for yet another payment method
- **Success likelihood**: Medium (regulatory support strong, but adoption may be low without clear user benefit)

**Sand Dollar (Bahamas):**
- **What it reveals**: Small island nations see CBDCs as practical financial inclusion tool
- **Clever design features**:
  - Designed for geography (700 islands, many without bank branches)
  - Hurricane resilience (works offline when infrastructure fails)
  - Lower KYC for small amounts enables unbanked access
- **Key risk**: Very small scale limits network effects; merchants slow to adopt
- **Success likelihood**: Medium (genuine need exists, but scale too small to draw conclusions for larger economies)

**Cross-Cutting Insights:**

1. **Motivation determines design**: China wants control (programmable, visible); EU wants privacy (offline anonymous); Bahamas wants inclusion (low barriers)

2. **Two-tier is universal**: All three use commercial banks/FIs for distribution - direct central bank accounts deemed too disruptive

3. **Interest is avoided**: All three are non-interest-bearing initially - fear of disintermediation trumps monetary policy benefits

4. **Scale matters differently**: China can fail at retail adoption and still succeed strategically (cross-border, mBridge). Bahamas must succeed at retail or fail entirely

### Presentation Talking Points
- Each CBDC reflects its issuer's political economy, not just technical choices
- e-CNY is about power and control; Digital Euro is about sovereignty and privacy; Sand Dollar is about inclusion
- None have "succeeded" yet in the sense of displacing existing payment methods
- Key economic insight: The strategic value of CBDC (monetary sovereignty, policy tools) may matter more than whether consumers actually use it
- The Bahamas is not a model for large economies - different problems, different solutions

---

## Exercise 4: "CBDCs Will Destroy Commercial Banking"

**Category**: Structured Debate
**Time**: 30 min work + 5 min presentation (final debate)
**Group Size**: Two teams of 4-6 students each
**Materials Needed**: Timer, L03 concepts reference sheet

### Task

Structured debate on the motion: **"The introduction of retail CBDCs will lead to the collapse of the commercial banking model within 15 years."**

**Team A (Pro)**: CBDCs will destroy commercial banking
**Team B (Con)**: Banks will adapt and survive

**Debate Structure**:
| Phase | Time | Activity |
|-------|------|----------|
| Preparation | 15 min | Teams prepare 3 main arguments using L03 concepts |
| Opening | 3 min each | Each team presents main arguments |
| Rebuttal Prep | 5 min | Teams prepare responses |
| Rebuttals | 2 min each | Each team responds to opponent |
| Closing | 2 min each | Final summary |

**Required L03 Concepts**: Use at least 3 per team from:
- Bank disintermediation
- Tiered remuneration / holding limits
- Monetary policy transmission
- Flight to safety / digital bank runs
- Financial inclusion
- Two-tier distribution model
- Interest rate floor
- Wholesale vs retail CBDC

### Model Answer / Expected Output

**Team A (Pro - CBDCs Destroy Banking):**

**Argument 1: Deposit Flight is Inevitable**
- L03 Concept: *Bank disintermediation*
- Core argument: CBDC is strictly safer than bank deposits (central bank liability vs. private bank liability). Rational depositors will move funds to CBDC given any uncertainty
- Evidence: Silicon Valley Bank lost $42B in 24 hours via mobile banking in 2023. With CBDC, flight would be instant and total
- Holding limits won't work: 3000 EUR limit means every person has 3000 EUR they can immediately move - for EU, that's 340M people x 3000 = 1 trillion EUR potential flight

**Argument 2: Interest Rate Floor Destroys Bank Margins**
- L03 Concept: *Interest rate floor / monetary policy transmission*
- Core argument: If CBDC pays interest (even 0%), it sets a floor on deposit rates. Banks must match CBDC rate or lose deposits
- Economic model: Bank profit = (lending rate - deposit rate) x deposits. If deposit rate is forced up by CBDC floor, and lending rates are constrained by competition, margins collapse
- Example: If CBDC pays 0% and banks currently pay -0.5%, banks lose their negative-rate revenue source

**Argument 3: Digital Bank Runs Will Be Catastrophic**
- L03 Concept: *Flight to safety*
- Core argument: In any future crisis, depositors will flee to CBDC (risk-free) from bank deposits (risky). The speed of digital transfers means no time for central bank intervention
- Historical comparison: Traditional bank runs (1930s, 2008) took days/weeks. Digital bank runs could happen in hours
- Policy implication: Central banks will be forced to provide unlimited liquidity to banks, effectively nationalizing the banking system

**Rebuttal Points Against Con:**
- "Holding limits protect banks" - Limits only delay the inevitable; if people WANT to leave, they'll find ways (multiple accounts, corporate accounts)
- "Banks will adapt" - Banks adapted to payments disruption, but CBDCs threaten the core business (deposit-taking), not just a product line
- "Two-tier preserves banks" - Two-tier distribution is a transition, not an end state; once people have CBDC wallets, why need banks?

---

**Team B (Con - Banks Adapt and Survive):**

**Argument 1: Design Features Protect the Banking System**
- L03 Concept: *Tiered remuneration / holding limits*
- Core argument: Central banks are explicitly designing CBDCs to NOT disintermediate banks. Holding limits (3000 EUR), tiered rates (0% up to limit, negative above), non-interest features all protect deposits
- Evidence: Every major CBDC design (Digital Euro, e-CNY) includes disintermediation safeguards
- Central banks need banks: Banks perform credit allocation, maturity transformation, monitoring. Central banks don't want these responsibilities

**Argument 2: Two-Tier Distribution Ensures Bank Survival**
- L03 Concept: *Two-tier distribution model*
- Core argument: All CBDC designs use banks to distribute CBDC. This keeps banks relevant as customer interface
- Revenue model: Banks will earn distribution fees, onboarding fees, value-added services on top of CBDC
- Historical parallel: Banks survived ATMs, online banking, mobile payments - each "threat" became a service banks provide

**Argument 3: Credit Intermediation Remains Essential**
- L03 Concept: *Wholesale vs retail CBDC distinction*
- Core argument: CBDC replaces cash, not credit. Businesses still need loans, mortgages still need funding, working capital still needs financing
- Banks' core function: Maturity transformation (borrow short, lend long) and credit assessment cannot be done by a central bank. CBDC is a payment tool, not a lending tool
- Evidence: Even in China with aggressive CBDC rollout, banks remain dominant in lending

**Rebuttal Points Against Pro:**
- "Deposit flight is inevitable" - Holding limits cap flight; 3000 EUR is a convenience amount, not life savings. Large deposits stay in banks for interest
- "Interest floor destroys margins" - Banks will compete on services, not just rates. Relationship banking, advice, credit access justify premium
- "Digital bank runs" - Central banks can pause CBDC conversions during crisis; they control the system. Emergency powers exist for this reason

---

**Balanced Verdict (for instructor):**

The economically strongest position is that **banks will survive but transform significantly**:

1. **What WILL change:**
   - Deposit margins compressed (CBDC floor effect)
   - Payment revenue declines (CBDC competition)
   - Balance sheets shrink (some deposits move to CBDC)
   - More wholesale funding needed (costlier)

2. **What WON'T change:**
   - Credit intermediation remains (central banks won't do lending)
   - Maturity transformation still needed
   - Risk assessment still human/institutional

3. **The adjustment:**
   - Banks become more like narrow banks (a simplified bank that only holds safe assets and does not make risky loans) for deposits (safety)
   - Banks become more like investment banks for lending (risk)
   - The universal banking model fragments

**Historical parallel:** Newspapers didn't disappear with the internet - they lost 80% of revenue and transformed into different businesses. Banks face similar disruption: survival with dramatically reduced profitability.

### Presentation Talking Points
- Both sides should use L03 concepts explicitly and correctly
- The key tension: Central banks NEED banks (for credit) but CBDC undermines them (for deposits)
- Holding limits are the critical design feature - they determine whether disintermediation is gradual or catastrophic
- Key economic insight: The question isn't "banks or no banks" but "what will banks look like post-CBDC?"
- Winner of debate should be team that best explains the equilibrium, not extreme positions

---

## Exercise 5: Design a CBDC for a Developing Nation

**Category**: Creative/Design
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Whiteboard, flip chart, or paper; colored markers

### Task

Your group is the economic advisory team for **the Central Bank of a fictional African nation "Zawadi"**. Design a CBDC that addresses the country's specific constraints and objectives.

**Country Profile - Zawadi:**
- Population: 25 million
- GDP per capita: $2,400
- Unbanked rate: 62%
- Mobile phone penetration: 78% (mostly basic phones, not smartphones)
- Internet coverage: 45%
- Main economic activities: Agriculture (50%), remittances from diaspora (15% of GDP)
- Banking sector: 8 commercial banks, 400 branches nationwide (mostly in cities)
- Currency: Zawadi Shilling (ZWS), moderate inflation (12% annual)
- Challenges: Rural financial exclusion, expensive remittances (8% average cost), weak tax collection

**Design Decisions Required:**
1. **Retail vs Wholesale**: Who can access?
2. **Technology Platform**: Smartphone app, USSD (basic phone), card, or hybrid?
3. **Identity Requirements**: Full KYC, tiered KYC, or anonymous for small amounts?
4. **Interest Policy**: Interest-bearing, non-interest, or tiered?
5. **Holding Limits**: What amounts and why?
6. **Offline Capability**: Required or optional?
7. **Cross-border**: Remittance integration?

### Model Answer / Expected Output

**Model CBDC Design Brief: "ZawadiPay" (Digital Zawadi Shilling)**

---

**OVERVIEW:**

| Design Element | Decision | Rationale |
|----------------|----------|-----------|
| **Type** | Retail CBDC | Financial inclusion is primary goal |
| **Technology** | USSD-first with smartphone app | 78% have phones, only ~30% smartphones |
| **Identity** | Tiered KYC | Balance inclusion with AML requirements |
| **Interest** | Non-interest-bearing | Avoid bank disintermediation in weak banking system |
| **Holding Limits** | Tiered by KYC level | Higher limits for verified users |
| **Offline** | Yes, mandatory | 55% lack reliable internet |
| **Cross-border** | Remittance corridor integration | 15% of GDP from diaspora |

---

**DETAILED DESIGN:**

**1. Technology Architecture:**

| Tier | Access Method | Target Users | Cost |
|------|--------------|--------------|------|
| Basic | USSD (*123#) | Rural poor, basic phones | Free |
| Standard | Smartphone app | Urban, semi-urban | Free |
| Agent | Point-of-sale terminals | Merchants, agents | Subsidized |

**Note: USSD (Unstructured Supplementary Service Data) is a mobile phone protocol that works without internet---like texting but for interactive menus. It works on any basic phone.**

- USSD chosen because it works on any mobile phone, no data required
- Works even with spotty network (store-and-forward)
- Example: M-Pesa in Kenya succeeded with USSD, not apps

**Note: M-Pesa is a Kenyan mobile money system launched in 2007 that revolutionized financial inclusion---proof that phone-based payments can reach the unbanked without smartphones or bank accounts.**

**2. Tiered KYC Model:**

| Tier | Verification | Daily Limit | Monthly Limit | Use Case |
|------|--------------|-------------|---------------|----------|
| **Tier 0** | Phone number only | 500 ZWS (~$20) | 5,000 ZWS (~$200) | Small purchases, market traders |
| **Tier 1** | + National ID | 5,000 ZWS (~$200) | 50,000 ZWS (~$2,000) | Salary, remittances |
| **Tier 2** | + Bank-level KYC | 50,000 ZWS | Unlimited | Business, large transfers |

- Tier 0 enables unbanked to participate immediately
- Limits are set to cover typical daily transactions for informal sector
- Progression encourages formal identity uptake

**3. Financial Inclusion Features:**

| Feature | Implementation | Economic Rationale |
|---------|----------------|-------------------|
| No minimum balance | Zero | Removes barrier for poor |
| No transaction fees (P2P) | Subsidized by CB | Adoption incentive |
| Merchant fees | 0.5% (vs 2-3% cards) | Encourage merchant adoption |
| Interest | 0% (non-interest-bearing) | Protect weak banking sector |
| Agent network | 10,000 agents (vs 400 branches) | Rural reach |

**4. Remittance Integration:**

| Corridor | Partner | Target Cost | Current Cost |
|----------|---------|-------------|--------------|
| US-Zawadi | Mobile money operators | 3% | 8% |
| UK-Zawadi | Banks + fintech | 3% | 7% |
| Regional (Africa) | mCBDC platform | 1% | 5% |

- Diaspora remittances are 15% of GDP - this is critical
- Direct CBDC receipt reduces intermediary costs
- Currency conversion at central bank rates (not marked-up)

**5. Offline Capability:**

| Mode | Technology | Security |
|------|------------|----------|
| Offline P2P | Bluetooth/NFC on smartphones | Value stored in secure element |
| Offline USSD | Deferred settlement | Limits strictly enforced |
| Maximum offline | 3 days or 2,000 ZWS | Prevents large offline fraud |

- Essential for rural areas with intermittent connectivity
- Modeled on e-CNY offline capability

**6. Disintermediation Safeguards:**

| Risk | Mitigation |
|------|------------|
| Deposit flight | Non-interest-bearing, low limits |
| Bank opposition | Banks as distribution agents (earn fees) |
| Currency substitution | Only ZWS-denominated, no FX function |

---

**EXPECTED CHALLENGES AND MITIGATIONS:**

| Challenge | Mitigation |
|-----------|------------|
| Digital literacy | Agent network for assisted transactions; voice prompts in local languages |
| Feature phone limitations | USSD tested on lowest-end devices |
| Fraud risk | Transaction limits, velocity checks, agent monitoring |
| Bank resistance | Revenue sharing; banks earn agent fees |
| Infrastructure | Solar-powered agents; offline mode |

---

**SUCCESS METRICS (2-year targets):**

| Metric | Target | Baseline |
|--------|--------|----------|
| Adoption rate | 40% of adults | 0% |
| Unbanked accessing formal finance | 30% of unbanked | 0% |
| Remittance cost reduction | 3% average | 8% average |
| Government transfer efficiency | 90% digital | 20% digital |
| Merchant acceptance | 50,000 merchants | 0 |

### Presentation Talking Points
- ZawadiPay prioritizes financial inclusion over monetary policy transmission
- USSD is critical - smartphone-only solutions exclude the poorest
- Tiered KYC is the key innovation - start with phone number, grow to full KYC
- Non-interest-bearing is chosen to protect banks, but limits monetary policy benefits
- Key economic insight: CBDC design for developing nations is fundamentally different from advanced economies - inclusion trumps efficiency
- M-Pesa model proves mobile-first financial services can achieve massive scale in Africa

---

## Exercise 6: Bank Disintermediation Risk Calculator

**Category**: Python/Modeling
**Time**: 30 min work + 5 min presentation
**Group Size**: Pairs
**Materials Needed**: Laptop with Python (numpy, matplotlib, scipy), internet access

### Task

Build a simple model to simulate bank deposit flight under different CBDC design scenarios. Explore how holding limits, interest rates, and crisis events affect deposit stability.

### Complete Code

```python
"""
Bank Disintermediation Risk Calculator
L03 Exercise - Economics of Digital Finance

# Data as of February 2025

Requirements: pip install numpy matplotlib scipy

Model based on: Bindseil (2020) - Tiered CBDC and the financial system
Theory: Brunnermeier & Niepelt (2019) - On the equivalence of private and public money

Note: This exercise uses an Ordinary Differential Equation (ODE)---a mathematical formula
showing how something changes over time. The `odeint` function from scipy solves these
equations numerically.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# =============================================================================
# MODEL PARAMETERS (given)
# =============================================================================

# Baseline economy parameters
TOTAL_DEPOSITS = 100  # Normalized to 100% (e.g., 100 billion EUR)
BANK_DEPOSIT_RATE = 0.005  # 0.5% annual interest on deposits

# Depositor behavior parameters
RATE_SENSITIVITY = 0.15  # How much depositors respond to rate differential
CRISIS_SENSITIVITY = 2.0  # Amplification during crisis
CBDC_CONVENIENCE_PREMIUM = 0.002  # 0.2% equivalent value of CBDC features

# =============================================================================
# DEPOSIT DYNAMICS MODEL (given --- study this carefully!)
# =============================================================================

def deposit_flight_model(deposits, time, params):
    """
    Differential equation for deposit dynamics.

    dD/dt = -alpha * (attractiveness_CBDC - attractiveness_deposits) * D

    Where attractiveness depends on:
    - Interest rate differential
    - Convenience/safety premium of CBDC
    - Crisis conditions (confidence shock)
    """

    cbdc_rate = params['cbdc_rate']
    holding_limit = params['holding_limit']
    crisis_start = params['crisis_start']
    crisis_duration = params['crisis_duration']

    # Calculate CBDC attractiveness
    # CBDC is more attractive if: higher rate, perceived safer, more convenient
    rate_advantage = cbdc_rate - BANK_DEPOSIT_RATE  # Positive if CBDC pays more

    # Convenience premium (digital payments, instant transfers)
    convenience_advantage = CBDC_CONVENIENCE_PREMIUM

    # Crisis premium (CBDC is risk-free, deposits are not)
    if crisis_start is not None and crisis_start <= time < crisis_start + crisis_duration:
        safety_premium = 0.05  # 5% equivalent during crisis
        sensitivity = RATE_SENSITIVITY * CRISIS_SENSITIVITY
    else:
        safety_premium = 0.005  # 0.5% equivalent normally
        sensitivity = RATE_SENSITIVITY

    # Total attractiveness differential
    attractiveness_diff = rate_advantage + convenience_advantage + safety_premium

    # Holding limit effect: caps maximum flight
    # If deposits have already fallen to (100 - limit), no more can leave
    if holding_limit is not None:
        max_flight = min(holding_limit, deposits)  # Can't move more than limit or remaining
        effective_flow = -sensitivity * attractiveness_diff * max_flight
    else:
        effective_flow = -sensitivity * attractiveness_diff * deposits

    # Deposits can't go below zero or above initial
    if deposits <= 0 and effective_flow < 0:
        return 0
    if deposits >= TOTAL_DEPOSITS and effective_flow > 0:
        return 0

    return effective_flow

# =============================================================================
# (a) SCENARIO DEFINITIONS
# Task: Define 7 scenarios as a list of tuples. Each tuple contains:
#       (name, cbdc_rate, holding_limit, crisis_start)
# Scenarios to define:
#   A: No CBDC baseline (all None)
#   B: 0% CBDC rate, no holding limit, no crisis
#   C: 0% CBDC rate, 30% holding limit, no crisis
#   D: 1% CBDC rate, no holding limit, no crisis
#   E: 1% CBDC rate, 30% holding limit, no crisis
#   F: 0% CBDC rate, no holding limit, crisis at quarter 8
#   G: 0% CBDC rate, 30% holding limit, crisis at quarter 8
# =============================================================================

scenarios = None  # YOUR CODE HERE — define as a list of 7 tuples: (name, cbdc_rate, holding_limit, crisis_start)

# =============================================================================
# (b) SIMULATION FUNCTION
# Task: Complete the run_scenario function that:
#   1. Creates a params dict with keys: cbdc_rate, holding_limit, crisis_start, crisis_duration
#   2. Creates a time grid of 200 points from 0 to 20 quarters
#   3. Solves the ODE using odeint(deposit_flight_model, TOTAL_DEPOSITS, time_grid, args=(params,))
#   4. Returns (time_grid, deposits_flattened, params)
# =============================================================================

def run_scenario(name, cbdc_rate, holding_limit, crisis_start=None, crisis_duration=3):
    """Run a single scenario and return results."""
    pass  # YOUR CODE HERE

# =============================================================================
# VISUALIZATION (Panels 1 and 2 are given; Panels 3 and 4 are yours to build)
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Color scheme
colors = ['gray', '#2CA02C', '#0066CC', '#FF7F0E', '#9467BD', '#D62728', '#8C564B']
linestyles = ['-', '-', '--', '-', '--', ':', ':']

# --- Panel 1 (given): All scenarios comparison ---
ax1 = axes[0, 0]
if scenarios is not None:
    for i, (name, cbdc_rate, limit, crisis) in enumerate(scenarios):
        if name == "A: No CBDC (Baseline)":
            time_grid = np.linspace(0, 20, 200)
            deposits = np.ones(200) * TOTAL_DEPOSITS
        else:
            time_grid, deposits, _ = run_scenario(name, cbdc_rate, limit, crisis)

        ax1.plot(time_grid, deposits, label=name, color=colors[i],
                 linewidth=2 if i > 0 else 1.5, linestyle=linestyles[i])

ax1.set_xlabel('Time (Quarters)', fontweight='bold')
ax1.set_ylabel('Bank Deposits (% of Initial)', fontweight='bold')
ax1.set_title('Deposit Dynamics Under Different CBDC Designs', fontweight='bold', color='#3333B2')
ax1.legend(loc='lower left', fontsize=8)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 105)
ax1.axhline(70, color='red', linestyle=':', alpha=0.5, label='Stability Threshold')

# --- Panel 2 (given): Holding Limit Impact ---
ax2 = axes[0, 1]
limits = [0, 10, 20, 30, 40, 50, 100]  # % of deposits
final_deposits = []

for limit in limits:
    if limit == 0:
        final_deposits.append(100)
    else:
        _, deposits, _ = run_scenario("test", 0.01, limit, None)
        final_deposits.append(deposits[-1])

ax2.bar(range(len(limits)), final_deposits, color='#0066CC', alpha=0.8)
ax2.set_xticks(range(len(limits)))
ax2.set_xticklabels(['No\nCBDC', '10%', '20%', '30%', '40%', '50%', 'No\nLimit'])
ax2.set_xlabel('CBDC Holding Limit (% of Deposits)', fontweight='bold')
ax2.set_ylabel('Final Deposit Level (%)', fontweight='bold')
ax2.set_title('Impact of Holding Limits on Deposit Stability\n(1% CBDC Rate, 5 Years)', fontweight='bold', color='#3333B2')
ax2.axhline(70, color='red', linestyle='--', alpha=0.5, label='Stability Threshold')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

# =============================================================================
# (c) Panel 3: CBDC Rate Sensitivity
# Task: For each rate in [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03], run a
#        scenario with NO holding limit and collect the final deposit level.
#        Plot rates (as %) on x-axis vs final deposits on y-axis.
#        Add a horizontal line at 70% ("Stability Threshold") and a vertical
#        line at 0.5% ("Bank Deposit Rate").
# =============================================================================

ax3 = axes[1, 0]
rates = [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03]

# YOUR CODE HERE — collect final deposit levels and plot on ax3
pass  # YOUR CODE HERE

ax3.set_xlabel('CBDC Interest Rate (%)', fontweight='bold')
ax3.set_ylabel('Final Deposit Level (%)', fontweight='bold')
ax3.set_title('Deposit Sensitivity to CBDC Interest Rate\n(No Holding Limit, 5 Years)', fontweight='bold', color='#3333B2')
ax3.grid(True, alpha=0.3)
ax3.set_xlim(-0.1, 3.1)

# =============================================================================
# (c) Panel 4: Crisis Scenario Analysis
# Task: Run 3 scenarios and plot on ax4:
#   1. No crisis, 30% limit (green, solid)
#   2. Crisis at Q8, no limit (red, dashed)
#   3. Crisis at Q8, 30% limit (blue, dash-dot)
# Mark the crisis period (Q8-11) with ax4.axvspan and a text label.
# =============================================================================

ax4 = axes[1, 1]

# YOUR CODE HERE — run 3 scenarios, plot them, mark crisis period
pass  # YOUR CODE HERE

ax4.set_xlabel('Time (Quarters)', fontweight='bold')
ax4.set_ylabel('Bank Deposits (% of Initial)', fontweight='bold')
ax4.set_title('Crisis Scenario: Holding Limits as Stabilizer', fontweight='bold', color='#3333B2')
ax4.legend(loc='lower left')
ax4.grid(True, alpha=0.3)
ax4.set_ylim(0, 105)

plt.tight_layout()
plt.savefig('disintermediation_calculator.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# (d) INTERPRETATION
# Task: Fill in your findings based on the plots you generated.
# =============================================================================

print("\n" + "="*70)
print("BANK DISINTERMEDIATION RISK ANALYSIS SUMMARY")
print("="*70)

print("""
KEY FINDINGS:

1. HOLDING LIMIT EFFECT:
   - YOUR ANSWER HERE: What happens with a 30% limit vs no limit?

2. INTEREST RATE SENSITIVITY:
   - YOUR ANSWER HERE: How does each 0.5% increase in CBDC rate affect deposits?

3. CRISIS AMPLIFICATION:
   - YOUR ANSWER HERE: How do holding limits help during a crisis?

4. POLICY IMPLICATIONS:
   - YOUR ANSWER HERE: What are the key design recommendations?

MODEL LIMITATIONS:
- Simplified depositor behavior
- No bank response (raising deposit rates)
- No central bank intervention
- Homogeneous depositors (reality: heterogeneous preferences)
""")
```

### Model Answer / Expected Output

**Expected Visualization Description:**
- Four-panel analysis showing:
  1. Time series of deposits under 7 scenarios (baseline, various CBDC designs)
  2. Bar chart of final deposit levels vs. holding limit size
  3. Line chart of deposit sensitivity to CBDC interest rate
  4. Crisis comparison with and without holding limits

**Key Finding (Model Answer):**

The simulation reveals three critical design principles for CBDC stability:

1. **Holding Limits are the Primary Stabilizer**
   - A 30% holding limit preserves 75-80% of deposits even with positive CBDC rates
   - Without limits, deposits can fall below 50% in 5 years
   - Limits work by capping the maximum possible flight, regardless of incentives

2. **Interest Rate Matters Enormously**
   - Each 0.5% increase in CBDC rate above bank deposit rates costs 5-10% of deposits
   - At 2% CBDC rate (vs 0.5% deposit rate), deposit collapse is rapid
   - This is why all major CBDC designs are non-interest-bearing initially

3. **Crisis Scenarios Require Pre-Positioned Limits**
   - During a crisis, flight velocity roughly doubles
   - Without limits: 30-40% deposit loss in 3 quarters
   - With limits: crisis impact is capped, giving time for policy response

**Model Interpretation:**

The Brunnermeier-Niepelt equivalence result suggests that in a frictionless world, CBDC and deposits should be equivalent. But the model shows real-world frictions matter:

- **Safety premium**: CBDC is risk-free, deposits are not. This creates persistent flight pressure
- **Convenience premium**: Digital CBDC offers features deposits don't
- **Crisis amplification**: Safety premium spikes during uncertainty

The Digital Euro's proposed 3000 EUR limit (~30% of average deposits) appears well-calibrated based on this model.

### Presentation Talking Points
- The model is intentionally simplified - real dynamics are more complex
- Holding limits are the "circuit breaker" that prevents catastrophic flight
- The trade-off: limits cap disintermediation but also cap CBDC usefulness
- Key economic insight: CBDC design is constrained optimization - maximize benefits subject to stability constraint
- Policy recommendation: Start with strict limits, relax only if stability demonstrated

---

## Exercise 7: Tiered Remuneration Design Challenge

**Category**: Policy Design
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Worksheet with scenarios, calculator

### Task

Design a tiered remuneration scheme for a Digital Euro that balances monetary policy effectiveness, financial stability, and user adoption. Present your scheme to the "ECB Governing Council" (class).

**Context:**
The ECB is finalizing the Digital Euro design. You are the technical advisory committee tasked with designing the interest rate and holding limit structure. The current proposal is:
- 3000 EUR holding limit
- 0% interest rate

The Governing Council has asked you to evaluate alternatives and make a recommendation.

**Design Constraints:**
- Must preserve banking system stability (no more than 20% deposit flight)
- Must maintain monetary policy transmission capability
- Must be attractive enough for user adoption (at least 40% of population should want to use it)
- Must comply with EU privacy standards (tiering must be justifiable)

**Scenarios to Analyze:**

| Scenario | Tier 1 (0-3000 EUR) | Tier 2 (3000-10000 EUR) | Tier 3 (>10000 EUR) |
|----------|---------------------|-------------------------|---------------------|
| A (Baseline) | 0% | Not allowed | Not allowed |
| B (Generous) | 1% | 0% | -1% |
| C (Neutral) | 0% | -0.5% | -1% |
| D (Restrictive) | -0.5% | -1% | -2% |
| E (Your Design) | ? | ? | ? |

### Model Answer / Expected Output

**Analysis Matrix:**

| Criterion | A (Baseline) | B (Generous) | C (Neutral) | D (Restrictive) |
|-----------|--------------|--------------|-------------|-----------------|
| **Deposit Flight Risk** | Low (10-15%) | High (25-30%) | Medium (15-20%) | Very Low (5-10%) |
| **Monetary Policy Transmission** | None | Strong | Moderate | Very Strong |
| **User Adoption Likelihood** | Medium (40-50%) | High (70-80%) | Medium (50-60%) | Low (20-30%) |
| **Privacy Compliance** | High | Medium | Medium | High |
| **Operational Complexity** | Low | High | Medium | Medium |
| **OVERALL RECOMMENDATION** | Acceptable | Risky | **Preferred** | Too restrictive |

**Detailed Justifications:**

**Scenario A (Baseline: 0%, 3000 EUR limit):**
- Deposit flight: Limited by holding cap; no rate incentive to switch
- Monetary policy: Zero transmission - CBDC doesn't respond to policy rate
- Adoption: Moderate - useful for payments, but no savings incentive
- Verdict: Safe but misses monetary policy opportunity

**Scenario B (Generous: 1% / 0% / -1%):**
- Deposit flight: HIGH - 1% on first 3000 EUR beats most bank savings accounts
- Monetary policy: Strong transmission in Tier 1, but creates distortions
- Adoption: Very high - clear financial benefit to users
- Verdict: Too aggressive; bank lobby will block; stability risk

**Scenario C (Neutral: 0% / -0.5% / -1%):**
- Deposit flight: Moderate and manageable
- Monetary policy: Tier 2 and 3 rates transmit policy; Tier 1 is neutral
- Adoption: Good - convenient for payments, no penalty on small holdings
- Verdict: **RECOMMENDED** - balances all objectives

**Scenario D (Restrictive: -0.5% / -1% / -2%):**
- Deposit flight: Very low - CBDC is penalized vs. deposits
- Monetary policy: Strong transmission of negative rates
- Adoption: Very low - why hold something that costs money?
- Verdict: Defeats purpose; negative rates politically toxic

---

**Model Recommended Design (Scenario E):**

| Tier | Amount | Interest Rate | Rationale |
|------|--------|---------------|-----------|
| **Tier 1** | 0-3,000 EUR | 0% | Cash-equivalent for daily transactions; no incentive to hoard |
| **Tier 2** | 3,000-10,000 EUR | Policy Rate - 0.5% | Tracks ECB policy but below deposits; some policy transmission |
| **Tier 3** | >10,000 EUR | Policy Rate - 1.5% | Strong discouragement of large holdings; maximum policy transmission |

**Design Rationale:**

1. **Tier 1 at 0%**:
   - Acts like cash replacement
   - No incentive to move savings from banks
   - 3000 EUR covers 2-3 months of typical household spending

2. **Tier 2 tracks policy rate**:
   - Provides monetary policy transmission
   - Gap below deposit rates (assumed 0.5% above policy rate) protects banks
   - Allows those who want more CBDC to hold it, but at a cost

3. **Tier 3 heavily penalized**:
   - Discourages large-scale disintermediation
   - Crisis prevention: large holders won't accumulate CBDC speculatively
   - Ensures flight to safety is bounded

**Implementation Notes:**

- **Rate adjustment frequency**: Quarterly, following ECB policy decisions
- **Tier thresholds**: Indexed to inflation (3000 EUR in 2024 prices)
- **Privacy**: Tiers enforced at wallet level; central bank sees aggregate, not transactions
- **Transition**: Start with Scenario A (baseline), move to E after 2-year pilot

---

**Counter-Arguments to Anticipate:**

| Objection | Response |
|-----------|----------|
| "Negative rates are politically unacceptable" | Tier 1 is always non-negative; negatives only for excessive holdings |
| "Too complex for users" | Users see balance and effective rate; tiers managed automatically |
| "Banks will complain about Tier 2 competition" | Tier 2 is BELOW deposit rates by design; banks retain advantage |
| "Why allow Tier 3 at all?" | Flexibility for businesses, temporary holdings; penalty prevents abuse |

### Presentation Talking Points
- Tiered remuneration is the key innovation that makes CBDCs viable
- The 3000 EUR threshold is not arbitrary - it's roughly 2-3 months spending for average household
- Tracking policy rate in upper tiers preserves monetary policy transmission
- Key economic insight: The tier structure creates a "marginal" CBDC rate that can be used for policy, while the "average" rate (what most users experience) remains benign
- Political economy: Tier 1 at 0% is essential for public acceptance; negative rates only for "excessive" holdings
- Your design should be defensible to both a monetary economist (policy transmission) and a politician (user acceptance)

---

**PLAN_READY: .omc/plans/l03-in-class-exercises.md**
