# L01 In-Class Exercises: Introduction to Digital Finance & Economics

## Plan Metadata
- **Created**: 2026-02-04
- **Lesson**: L01 - Introduction to the Economics of Digital Finance
- **Target Audience**: BSc students (just completed L01)
- **Time Allocation**: 30 minutes work + 5 minutes presentation per exercise
- **Instructor Choice**: Select 1-2 exercises per session based on class size and learning goals

---

## Exercise Overview

| # | Title | Category | Group Size | Materials |
|---|-------|----------|------------|-----------|
| 1 | Bitcoin Volatility Explorer | Python/Data | Individual or Pairs | Laptop with Python |
| 2 | Money Functions Scorecard | Framework Application | Groups of 3-4 | Worksheet + Discussion |
| 3 | Traditional vs Digital Finance Battle | Debate/Discussion | Two Teams (4-6 each) | None |
| 4 | Four Lenses Case Analysis | Framework Application | Groups of 3-4 | Case Handout |
| 5 | Design Your Digital Currency | Creative/Design | Groups of 3-4 | Whiteboard/Paper |
| 6 | Payment Evolution Timeline | Research Mini-Task | Pairs | Internet Access |
| 7 | Network Effects Deep Dive | Comparative Analysis | Groups of 3-4 | Worksheet |
| 8 | Economic vs Technical Questions | Framework Application | Individual then Share | Worksheet |

---

## Exercise 1: Bitcoin Volatility Explorer

**Category**: Python/Data
**Time**: 30 min work + 5 min presentation
**Group Size**: Individual or Pairs
**Materials Needed**: Laptop with Python (yfinance, pandas, matplotlib), internet access

### Task

Analyze Bitcoin's ability to serve as a "store of value" by comparing its volatility to traditional currencies and gold. Create a publication-ready chart and answer: Does Bitcoin fulfill the store of value function?

### Complete Code

```python
"""
Bitcoin Volatility Analysis: Store of Value Assessment
L01 Exercise - Economics of Digital Finance

Requirements: pip install yfinance pandas matplotlib numpy
Data as of February 2025
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# =============================================================================
# DATA COLLECTION
# =============================================================================

# Define date range (last 3 years for meaningful volatility analysis)
end_date = datetime.now()
start_date = end_date - timedelta(days=3*365)

print("Fetching data from Yahoo Finance...")

# Fetch Bitcoin data
btc = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)
btc['return'] = btc['Adj Close'].pct_change()

# Fetch Gold ETF (GLD) as gold proxy
gold = yf.download('GLD', start=start_date, end=end_date, progress=False)
gold['return'] = gold['Adj Close'].pct_change()

# Fetch EUR/USD exchange rate
eurusd = yf.download('EURUSD=X', start=start_date, end=end_date, progress=False)
eurusd['return'] = eurusd['Adj Close'].pct_change()

# Fetch S&P 500 for additional context
sp500 = yf.download('^GSPC', start=start_date, end=end_date, progress=False)
sp500['return'] = sp500['Adj Close'].pct_change()

print("Data fetched successfully!")

# =============================================================================
# VOLATILITY CALCULATION
# =============================================================================

# Calculate 30-day rolling volatility (annualized)
# Formula: std(daily returns) * sqrt(trading days per year)
# Crypto trades 365 days, traditional markets ~252 days

btc['volatility'] = btc['return'].rolling(window=30).std() * np.sqrt(365) * 100
gold['volatility'] = gold['return'].rolling(window=30).std() * np.sqrt(252) * 100
eurusd['volatility'] = eurusd['return'].rolling(window=30).std() * np.sqrt(252) * 100
sp500['volatility'] = sp500['return'].rolling(window=30).std() * np.sqrt(252) * 100

# =============================================================================
# SUMMARY STATISTICS
# =============================================================================

print("\n" + "="*60)
print("SUMMARY STATISTICS: Annualized Volatility")
print("="*60)

stats = pd.DataFrame({
    'Asset': ['Bitcoin (BTC)', 'Gold (GLD)', 'EUR/USD', 'S&P 500'],
    'Mean Volatility (%)': [
        btc['volatility'].mean(),
        gold['volatility'].mean(),
        eurusd['volatility'].mean(),
        sp500['volatility'].mean()
    ],
    'Max Volatility (%)': [
        btc['volatility'].max(),
        gold['volatility'].max(),
        eurusd['volatility'].max(),
        sp500['volatility'].max()
    ],
    'Min Volatility (%)': [
        btc['volatility'].min(),
        gold['volatility'].min(),
        eurusd['volatility'].min(),
        sp500['volatility'].min()
    ]
})

print(stats.to_string(index=False))

# Calculate volatility ratios
btc_gold_ratio = btc['volatility'].mean() / gold['volatility'].mean()
btc_eurusd_ratio = btc['volatility'].mean() / eurusd['volatility'].mean()

print(f"\nBitcoin is {btc_gold_ratio:.1f}x more volatile than Gold")
print(f"Bitcoin is {btc_eurusd_ratio:.1f}x more volatile than EUR/USD")

# =============================================================================
# PUBLICATION-READY CHART
# =============================================================================

# Set style for publication quality
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots(figsize=(12, 7), dpi=100)

# Plot volatility series
ax.plot(btc.index, btc['volatility'],
        label='Bitcoin', color='#F7931A', linewidth=2, alpha=0.9)
ax.plot(gold.index, gold['volatility'],
        label='Gold', color='#FFD700', linewidth=1.5, alpha=0.8)
ax.plot(eurusd.index, eurusd['volatility'],
        label='EUR/USD', color='#0066CC', linewidth=1.5, alpha=0.8)
ax.plot(sp500.index, sp500['volatility'],
        label='S&P 500', color='#228B22', linewidth=1.5, alpha=0.8)

# Add benchmark reference lines
ax.axhline(y=15, color='gray', linestyle='--', alpha=0.5,
           label='Typical Gold Volatility (~15%)')
ax.axhline(y=8, color='gray', linestyle=':', alpha=0.5,
           label='Typical FX Volatility (~8%)')

# Formatting
ax.set_title('Bitcoin Volatility vs. Traditional Assets\n30-Day Rolling Annualized Volatility',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Annualized Volatility (%)', fontsize=11)
ax.legend(loc='upper right', fontsize=9)
ax.set_ylim(0, min(200, btc['volatility'].max() * 1.1))  # Cap at 200% for readability

# Add annotation for key insight
max_vol_date = btc['volatility'].idxmax()
max_vol = btc['volatility'].max()
ax.annotate(f'Peak: {max_vol:.0f}%',
            xy=(max_vol_date, max_vol),
            xytext=(max_vol_date, max_vol + 15),
            fontsize=9, ha='center',
            arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5))

# Add source note
fig.text(0.99, 0.01, 'Data: Yahoo Finance | Analysis: L01 Exercise',
         fontsize=8, ha='right', alpha=0.7)

plt.tight_layout()
plt.savefig('bitcoin_volatility_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nChart saved as 'bitcoin_volatility_analysis.png'")

# =============================================================================
# ECONOMIC CONCLUSION
# =============================================================================

print("\n" + "="*60)
print("ECONOMIC ANALYSIS: Store of Value Assessment")
print("="*60)

print("""
KEY FINDINGS:

1. VOLATILITY COMPARISON:
   - Bitcoin average volatility: ~{:.0f}% annually
   - Gold average volatility: ~{:.0f}% annually
   - EUR/USD average volatility: ~{:.0f}% annually
   - Bitcoin is {:.0f}x more volatile than gold

2. STORE OF VALUE ASSESSMENT:
   - Bitcoin FAILS the store of value test
   - Purchasing power can swing 20-80% in months
   - Traditional stores of value (gold) are 3-5x more stable

3. ECONOMIC INTERPRETATION:
   - High volatility = high risk of purchasing power loss
   - Volatility clustering during market stress
   - Not suitable for short/medium-term value preservation
   - Speculative asset, not monetary asset

4. WHAT WOULD NEED TO CHANGE:
   - Volatility would need to drop to ~15-20% (gold-like)
   - Requires: larger market cap, broader adoption,
     institutional involvement, regulatory clarity
""".format(
    btc['volatility'].mean(),
    gold['volatility'].mean(),
    eurusd['volatility'].mean(),
    btc_gold_ratio
))
```

### Model Answer / Expected Output

**Expected Chart Description:**
- Time series plot showing Bitcoin's 30-day rolling volatility (bright orange line) consistently between 40-100%, with spikes up to 150-200% during market stress
- Gold volatility (gold line) hovering around 10-20%
- EUR/USD volatility (blue line) flat around 5-10%
- S&P 500 volatility (green line) around 10-25%
- Two horizontal reference lines at 8% (FX benchmark) and 15% (Gold benchmark)
- Bitcoin line is ALWAYS above all other assets, often 3-5x higher

**Key Finding (Model Answer):**

Bitcoin **fails** the store of value function because:

1. **Volatility is 4-5x higher than gold** - With average annualized volatility of 50-70% vs. gold's 12-15%, Bitcoin cannot reliably preserve purchasing power

2. **Extreme drawdowns** - Bitcoin has experienced 50-80% price drops within months, making it unsuitable for value preservation

3. **Economic interpretation**: A good store of value should have:
   - Low volatility (predictable purchasing power)
   - No correlation with risk assets during stress
   - Bitcoin exhibits the opposite characteristics

4. **What would need to change**:
   - Market capitalization needs to grow 10-20x (reduce manipulation)
   - Institutional adoption needs to mature
   - Regulatory clarity would reduce uncertainty premium
   - Volatility would need to decline to ~15-20% annually

### Presentation Talking Points
- Bitcoin volatility is consistently 3-5x higher than gold and 5-10x higher than major currencies
- This makes it a **speculative asset**, not a monetary store of value
- The three functions of money are not independent - failure as store of value undermines unit of account function (who prices goods in something that swings 20% weekly?)
- Economic insight: Volatility is not a bug but a feature of a nascent, speculative market with inelastic supply

---

## Exercise 2: Money Functions Scorecard

**Category**: Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Printed worksheet, pens

### Task

Evaluate three types of digital money against the three classical functions of money. Create a scorecard rating each on a scale of 1-5, reach group consensus, and identify key trade-offs.

**Digital Money Types to Evaluate**:
1. Bitcoin (BTC)
2. A major Stablecoin (USDT or USDC)
3. A hypothetical CBDC (e.g., Digital Euro)

**Scoring Scale**:
- 5 = Excellent (comparable to best traditional money)
- 4 = Good (minor limitations)
- 3 = Adequate (noticeable limitations)
- 2 = Poor (significant limitations)
- 1 = Fails (cannot fulfill function)

### Model Answer / Expected Output

**Completed Scorecard (Consensus Answer):**

| Function | Key Question | Bitcoin | Stablecoin (USDC) | CBDC (Digital Euro) |
|----------|--------------|---------|-------------------|---------------------|
| **Medium of Exchange** | How widely accepted? How fast? How cheap? | **2** | **4** | **5** |
| **Unit of Account** | Are prices quoted in this? Is it stable enough? | **1** | **4** | **5** |
| **Store of Value** | Does it preserve purchasing power? | **2** | **3** | **4** |
| **TOTAL** | | **5** | **11** | **14** |

**Justifications:**

**Bitcoin:**
- Medium of Exchange (2): Limited merchant acceptance (~15,000 businesses globally), 10-60 min confirmation times, fees volatile ($1-$50), not practical for daily payments
- Unit of Account (1): Almost no prices quoted in BTC, too volatile - a coffee would cost 0.00005 BTC one day, 0.00007 BTC the next
- Store of Value (2): High volatility (50-70% annually), but has appreciated long-term; speculative, not reliable store

**Stablecoin (USDC):**
- Medium of Exchange (4): Widely accepted in crypto ecosystem, near-instant on modern chains, low fees ($0.01-$1), but limited outside crypto/DeFi
- Unit of Account (4): Stable at $1, but not used for pricing outside crypto; regulatory uncertainty
- Store of Value (3): Maintains $1 peg well, but counterparty risk (issuer could freeze/seize), not insured like bank deposits

**CBDC (Digital Euro):**
- Medium of Exchange (5): Would have legal tender status, instant settlement, zero/minimal fees, universal acceptance in Eurozone
- Unit of Account (5): Prices already in Euros, 1:1 with existing Euro, full legal recognition
- Store of Value (4): Central bank backing (no counterparty risk), but subject to inflation like any fiat currency; potential holding limits

**Key Insight:**
Different digital money designs excel at different functions because of inherent trade-offs:
- **Decentralization (Bitcoin)** sacrifices stability and acceptance for censorship resistance
- **Private stability (Stablecoins)** achieves medium of exchange but introduces counterparty risk
- **Public issuance (CBDCs)** maximizes all functions but requires trust in government

### Presentation Talking Points
- No digital money currently scores 5/5/5 - there are always trade-offs
- CBDCs are designed to replicate existing money's functions digitally (preserves monetary architecture)
- Stablecoins are a "bridge" technology - stable but not sovereign
- Bitcoin is not trying to be money - it's competing to be "digital gold" (store of value focus)
- Key economic insight: The three functions are interdependent - failure in one undermines the others

---

## Exercise 3: Traditional vs Digital Finance Battle

**Category**: Debate/Discussion
**Time**: 30 min work + 5 min presentation (final debate)
**Group Size**: Two teams of 4-6 students each
**Materials Needed**: None (timer helpful)

### Task

Structured debate on the motion: **"Digital finance will make traditional banks obsolete within 20 years."**

**Team A (Pro)**: Banks will become obsolete
**Team B (Con)**: Banks will adapt and survive

**Debate Structure**:
| Phase | Time | Activity |
|-------|------|----------|
| Preparation | 15 min | Teams prepare 3 main arguments using L01 concepts |
| Opening | 3 min each | Each team presents main arguments |
| Rebuttal Prep | 5 min | Teams prepare responses |
| Rebuttals | 2 min each | Each team responds to opponent |
| Closing | 2 min each | Final summary |

**Required L01 Concepts**: Use at least 2 per team from:
- Disintermediation / Re-intermediation
- Network effects
- Transaction costs
- Two-sided markets
- Market failure and regulation
- Three functions of money

### Model Answer / Expected Output

**Team A (Pro - Banks Become Obsolete):**

**Argument 1: Disintermediation is Inevitable**
- L01 Concept: *Disintermediation*
- Banks exist because they reduce transaction costs (screening, monitoring, liquidity transformation)
- DeFi protocols automate these functions: smart contracts for lending, AMMs for liquidity, algorithmic credit scoring
- Just as the internet disintermediated travel agents, record stores, and newspapers, it will disintermediate banks
- Evidence: DeFi TVL grew from $1B (2020) to $200B+ (2024) without any banks [Note: Data as of 2025]

**Argument 2: Network Effects Favor Digital Platforms**
- L01 Concept: *Network effects*
- Payment networks exhibit strong positive network effects - more users = more valuable
- Digital-native platforms (PayPal, Stripe, stablecoins) are winning the network effects battle
- Banks have legacy infrastructure (SWIFT, RTGS) that cannot compete on speed/cost
- Example: Visa/Mastercard already processing more value than many banking networks combined

**Argument 3: Transaction Costs Collapse in Digital Systems**
- L01 Concept: *Transaction costs*
- International wire transfers: $25-50 fees, 3-5 days, 3% FX spread
- Stablecoin transfer: $0.01-1 fee, instant, minimal spread
- When transaction costs approach zero, the raison d'etre of banks disappears
- Younger generations already prefer digital-first financial services

**Rebuttal Points Against Con:**
- "Regulation will protect banks" - Regulation follows innovation, not the other way around
- "Trust requires human institutions" - Smart contracts are more trustworthy than conflicted humans
- "Banks have customer relationships" - So did Kodak with photographers

---

**Team B (Con - Banks Adapt and Survive):**

**Argument 1: Re-intermediation Creates New Roles**
- L01 Concept: *Re-intermediation*
- Disintermediation is rarely complete - new intermediaries emerge (Amazon is an intermediary, not direct)
- Banks will become crypto custodians, DeFi on-ramps, regulatory compliance bridges
- Evidence: JPMorgan has blockchain division, Goldman has crypto trading desk, all major banks exploring stablecoins
- Banks have licenses, trust, and capital that startups lack

**Argument 2: Two-Sided Markets Need Trusted Intermediaries**
- L01 Concept: *Two-sided markets*
- Banks connect depositors (one side) with borrowers (other side)
- This requires credit assessment, risk management, maturity transformation
- DeFi lending is overcollateralized (150%+) because it CAN'T do credit assessment
- Real economy needs undercollateralized lending - requires human judgment and legal recourse

**Argument 3: Market Failures Require Regulated Entities**
- L01 Concept: *Market failure and regulation*
- Finance has information asymmetry, systemic risk, consumer protection needs
- 2022 crypto winter: FTX, Terra/LUNA, Celsius - $2 trillion lost [Note: Historical data as of 2025]
- Public will demand regulated, insured institutions
- CBDCs will be distributed through banks, not replace them

**Rebuttal Points Against Pro:**
- "DeFi grew fast" - From zero, and crashed 75% in 2022; still <1% of global finance [Note: Historical data as of 2025]
- "Transaction costs collapse" - But compliance costs, KYC/AML, fraud prevention don't
- "Young people prefer digital" - They also prefer deposit insurance and someone to call when hacked

---

**Balanced Verdict (for instructor):**
The economically strongest position is that banks will **transform, not disappear**. The re-intermediation argument is historically accurate (travel agents became Booking.com, record stores became Spotify - intermediaries, not disintermediation). Banks' regulatory moats (deposit insurance, payment system access, central bank facilities) are genuine barriers. However, bank profit margins will compress significantly.

### Presentation Talking Points
- Both sides should use L01 concepts explicitly and correctly
- The debate illuminates that "disintermediation" in digital finance often means "re-intermediation" by new players
- Network effects cut both ways - banks have existing networks worth trillions
- Key economic insight: The question isn't "banks or DeFi" but "what functions remain valuable and who performs them?"
- Historical parallel: Newspapers didn't disappear - they transformed (and most lost 80% of value)

---

## Exercise 4: Four Lenses Case Analysis

**Category**: Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Case handout (one of the options below)

### Task

Apply the "Four Economic Lenses" framework from L01 to analyze a real digital finance case.

**Case Options** (instructor assigns one per group):
- **Case A**: Stablecoin Collapse (Terra/LUNA 2022) [Historical case as of 2025]
- **Case B**: El Salvador Bitcoin Adoption (2021) [Historical case as of 2025]
- **Case C**: PayPal's Crypto Integration (2020-2024) [Historical case as of 2025]
- **Case D**: European Digital Euro Proposal

### Model Answer / Expected Output

**CASE A: Terra/LUNA Collapse - Completed Analysis**

| Lens | Key Question | Analysis |
|------|--------------|----------|
| **Monetary Economics** | How does this affect money supply, monetary policy? | Terra (UST) was an algorithmic stablecoin - attempted to maintain $1 peg through arbitrage with LUNA token. This was essentially **private money creation** without reserves. When confidence collapsed, the "money supply" (UST) expanded hyperinflation-style from 18B to worthless. Demonstrated why monetary economists distrust unbacked private money - no lender of last resort, no reserve requirement, pure confidence game. [Data as of 2025] |
| **Platform Economics** | What network effects are at play? Who benefits? | Terra had strong **network effects** in DeFi - 20% yield on Anchor protocol attracted $14B TVL. But network effects work in reverse too: as users withdrew, yield collapsed, more withdrew (death spiral). Two-sided market failure: when one side (depositors) fled, the other (borrowers/protocols) had no counterparty. **Winner:** Those who exited early. **Loser:** Retail investors, protocols built on Terra. [Data as of 2025] |
| **Market Microstructure** | How does trading/pricing work? What frictions exist? | The peg mechanism relied on **arbitrage**: if UST < $1, burn UST for $1 of LUNA, sell LUNA. But during stress, LUNA price crashed faster than arbitrage could work - market microstructure broke down. **Liquidity spirals**: selling LUNA lowered its price, requiring more LUNA to be minted, further lowering price. Classic microstructure failure - market makers (arbitrageurs) withdrew when needed most. |
| **Regulatory Economics** | What market failures exist? How should regulators respond? | Multiple market failures: (1) **Information asymmetry** - retail didn't understand algorithmic stablecoin risks; (2) **Systemic risk** - $40B collapse rippled through crypto; (3) **Consumer protection** - no deposit insurance, no recourse. Regulatory response: SEC now classifies algorithmic stablecoins as securities; EU MiCA bans unbacked algorithmic stablecoins; calls for reserve requirements on all stablecoins. [Regulatory data as of 2025] |

**Most Important Lens for This Case:** **Monetary Economics** - At its core, Terra was an attempt at private money creation without backing. All other failures (network effects reversal, liquidity spirals, regulatory gaps) flow from this fundamental monetary design flaw.

---

**CASE B: El Salvador Bitcoin Adoption - Completed Analysis**

| Lens | Key Question | Analysis |
|------|--------------|----------|
| **Monetary Economics** | How does this affect money supply, monetary policy? | El Salvador was already dollarized (no monetary policy). Bitcoin as legal tender means: (1) Currency substitution dynamics - Gresham's Law predicts bad money (volatile BTC) won't circulate, people hold USD; (2) Fiscal risk - government bought BTC, now underwater; (3) Seigniorage attempt - hoped to capture value from BTC appreciation instead of paying for USD. Result: BTC is <5% of transactions, failed to become medium of exchange. [Data as of 2025] |
| **Platform Economics** | What network effects are at play? Who benefits? | Government mandated merchant acceptance (forced network effect). But network effects must be organic to be valuable. **Chivo wallet** launched with $30 bonus - 70% of users withdrew bonus and abandoned wallet. Two-sided market failure: merchants forced to accept, consumers didn't want to pay. Real beneficiary: Crypto exchanges, remittance companies charging lower fees. Loser: Government credibility, taxpayers funding losses. [Data as of 2025] |
| **Market Microstructure** | How does trading/pricing work? What frictions exist? | Lightning Network deployed for fast BTC payments. But: (1) Liquidity constraints - merchants need BTC liquidity channels; (2) Pricing friction - prices still in USD, converted to BTC at volatile rate; (3) Settlement uncertainty - BTC price can move during transaction. Tourists occasionally use BTC, locals overwhelmingly prefer USD. Market microstructure not designed for daily payments. |
| **Regulatory Economics** | What market failures exist? How should regulators respond? | Reversed regulatory story - government MANDATED adoption (market "success" by decree). IMF opposed due to: fiscal risk, financial stability concerns, AML/CFT gaps. Creates regulatory arbitrage opportunity - money launderers have legal tender BTC country. Consumer protection concerns: Chivo wallet had fraud, security issues. Lesson: Mandates can't force adoption of economically inferior money. |

**Most Important Lens for This Case:** **Platform Economics** - The failure demonstrates that network effects cannot be mandated. Despite legal tender status and subsidies, Bitcoin failed to achieve critical mass for payments because users didn't want it for that purpose.

### Presentation Talking Points
- Different cases have different "dominant lenses" - the framework helps identify which perspective is most insightful
- All four lenses are always relevant, but one usually explains the core dynamic
- Terra collapse: fundamentally a monetary economics failure (money without backing)
- El Salvador: fundamentally a platform economics failure (can't mandate network effects)
- Key economic insight: The four lenses are complementary, not competing - use all, then identify which is most explanatory

---

## Exercise 5: Design Your Digital Currency

**Category**: Creative/Design
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Whiteboard, flip chart, or paper; colored markers

### Task

Your group is the economic advisory team for a small European country (population 5 million) that wants to launch its own digital currency. Design the currency using economic principles from L01.

**Design Decisions Required**:
1. **Type**: CBDC, private stablecoin, or cryptocurrency?
2. **Money Functions Priority**: Which function is most important?
3. **Seigniorage**: Who captures the value from issuing?
4. **Network Effects Strategy**: How will you achieve critical mass?
5. **Regulatory Approach**: What risks will you regulate against?

**Constraints**:
- Must maintain monetary policy effectiveness
- Must interoperate with Euro
- Budget: limited (can't compete with Big Tech marketing)

### Model Answer / Expected Output

**Model Digital Currency Design Brief: "DigiKrona" (hypothetical small EU country)**

---

**CURRENCY NAME:** DigiKrona (DKR)

**TYPE:** Retail CBDC (Central Bank Digital Currency)

**Justification:**
- CBDC chosen over private stablecoin (no counterparty risk, maintains sovereign money)
- CBDC chosen over cryptocurrency (maintains monetary policy, stable value)
- Retail (not wholesale) to directly serve citizens and enable financial inclusion

---

**MONEY FUNCTIONS PRIORITY:**

1. **Primary: Medium of Exchange**
   - Justification: Small country needs efficient domestic payments, reduce cash handling costs
   - Design implication: Near-instant settlement, zero fees for P2P, minimal fees for merchant

2. **Secondary: Unit of Account**
   - Fixed 1:1 with Euro (maintains familiar pricing)
   - No independent monetary policy (too small, already Euro-pegged)

3. **Tertiary: Store of Value**
   - Small holding limits (EUR 3,000 personal) to prevent bank disintermediation
   - No interest paid (prevents run from bank deposits)

---

**SEIGNIORAGE MODEL:**

| Stakeholder | Share | Mechanism |
|-------------|-------|-----------|
| Central Bank | 70% | Float income on reserves backing DKR |
| Commercial Banks | 20% | Distribution fee for onboarding users |
| Treasury | 10% | Direct fiscal transfer |

**Justification:** Shared model incentivizes bank participation (reduces opposition), captures public value while ensuring distribution network.

---

**NETWORK EFFECTS STRATEGY:**

**Phase 1 (Year 1): Government Anchor**
- All government payments (wages, pensions, benefits) available in DKR
- Tax payments accepted in DKR (5% discount)
- Public transport and government services: DKR only or priority queues

**Phase 2 (Year 2): Merchant Expansion**
- Zero merchant fees (subsidized for 2 years)
- Integration with existing POS terminals (partnership with local banks)
- "DKR Accepted Here" certification program

**Phase 3 (Year 3+): Private Adoption**
- P2P payments with instant settlement
- Integration with Euro payment rails (SEPA instant)
- Cross-border remittance corridors with neighboring countries

**Justification:** Government is largest economic actor - bootstraps network effect. Can't compete with Visa/PayPal on marketing, so compete on friction reduction (zero fees, instant, government priority).

---

**REGULATORY FRAMEWORK:**

| Risk | Regulation | Justification |
|------|------------|---------------|
| **Bank Disintermediation** | EUR 3,000 personal holding limit, no interest | Prevents run on deposits |
| **Money Laundering** | Full KYC, transaction limits without ID (EUR 150/day) | Tiered approach balances inclusion with compliance |
| **Privacy** | Central bank sees transactions, but data minimization, no sharing with tax authority without court order | Balance privacy with law enforcement needs |
| **Operational Risk** | Offline capability required, dual infrastructure (no single point of failure) | Resilience for critical payment infrastructure |
| **Financial Stability** | Cannot be used as collateral, not for large corporate transactions (wholesale stays in EUR) | Prevents systemic concentration |

---

**EXPECTED CHALLENGES AND MITIGATIONS:**

| Challenge | Mitigation |
|-----------|------------|
| Low initial adoption | Government payments bootstrap; patience - took Swish 5 years in Sweden |
| Bank opposition | Revenue sharing; position as complement not substitute |
| Technical failures | Offline fallback; phased rollout; extensive testing |
| Privacy concerns | Data minimization; legal protections; transparency reports |
| Euro interoperability | Build on SEPA instant rails; automatic conversion at 1:1 |

---

### Presentation Talking Points
- Every design choice has trade-offs - there is no "perfect" digital currency
- CBDC is the economically sound choice for a small country (preserves monetary sovereignty, no counterparty risk)
- Network effects cannot be bought - must be earned through genuine friction reduction
- Holding limits are the key tool to prevent bank disintermediation (L03 will cover this in depth)
- Key economic insight: The hardest problem isn't technology - it's the network effects chicken-and-egg problem

---

## Exercise 6: Payment Evolution Timeline

**Category**: Research Mini-Task
**Time**: 30 min work + 5 min presentation
**Group Size**: Pairs
**Materials Needed**: Internet access, shared document/slides

### Task

Create a detailed timeline for ONE specific region showing the evolution of payment methods, identifying the economic drivers of each transition.

**Region Options**:
- China (from traditional to WeChat/Alipay dominance)
- Kenya (from cash to M-Pesa mobile money)
- Sweden (from cash to near-cashless society)
- India (demonetization and UPI transformation)

### Model Answer / Expected Output

**KENYA / M-PESA TIMELINE - Complete Example**

---

**TRANSITION 1: Cash Economy (Pre-2007)**

| Element | Details |
|---------|---------|
| **What changed** | Predominantly cash-based economy |
| **When** | Pre-2007 |
| **Economic driver** | High transaction costs for formal banking (branches expensive, minimum balances, ID requirements). Only 19% of population had bank accounts. |
| **Who benefited** | Cash-based businesses, informal economy |
| **Who lost** | Rural poor (no access to savings/credit), women (less control over household finances) |

---

**TRANSITION 2: M-Pesa Launch (2007)**

| Element | Details |
|---------|---------|
| **What changed** | Safaricom launches M-Pesa mobile money service |
| **When** | March 2007 |
| **Economic driver** | **Transaction cost collapse**: No bank branch needed, no minimum balance, no formal ID required. Send money via SMS on basic phone. Agent network substituted for branches. |
| **Who benefited** | Rural households (could receive remittances from urban workers), small traders (reduced cash handling risk), Safaricom (transaction fees), agent network (commissions) |
| **Who lost** | Traditional banks (initially - missed the opportunity), bus drivers (previously carried cash remittances), Western Union (expensive remittances) |

---

**TRANSITION 3: Rapid Adoption / Network Effects Takeoff (2008-2012)**

| Element | Details |
|---------|---------|
| **What changed** | M-Pesa reaches critical mass: 15 million users by 2011 (40% of adult population) [Historical data as of 2025] |
| **When** | 2008-2012 |
| **Economic driver** | **Network effects**: Value of M-Pesa increased exponentially as more people joined. "Everyone has M-Pesa" became self-fulfilling. Agent network reached 40,000 points (more than all bank branches + ATMs combined). |
| **Who benefited** | Safaricom (near-monopoly), users (universal acceptance), merchants (reduced cash risk) |
| **Who lost** | Competing mobile operators (couldn't achieve network effects), traditional remittance services |

---

**TRANSITION 4: Ecosystem Expansion (2012-2017)**

| Element | Details |
|---------|---------|
| **What changed** | M-Pesa expands beyond P2P: bill payments, merchant payments, savings (M-Shwari), credit (M-Shwari loans), international remittances |
| **When** | 2012-2017 |
| **Economic driver** | **Platform economics / two-sided markets**: M-Pesa became a platform connecting users with services. Each new service increased platform value, attracted more users, enabled more services (flywheel). |
| **Who benefited** | Safaricom (multiple revenue streams), banks (partnered for M-Shwari), users (access to credit previously impossible), small businesses (working capital loans) |
| **Who lost** | Standalone microfinance institutions, informal lenders (loan sharks) |

---

**TRANSITION 5: Interoperability and Competition (2018-Present)**

| Element | Details |
|---------|---------|
| **What changed** | Regulatory intervention for interoperability (mobile money services must interoperate), new entrants (Airtel Money, T-Kash), fintech integration |
| **When** | 2018-Present [Data as of 2025] |
| **Economic driver** | **Regulatory economics**: Central Bank of Kenya mandated interoperability to prevent monopoly abuse. Competition policy to reduce fees. But M-Pesa retains ~99% market share due to **incumbent network effects**. [Market share data as of 2025] |
| **Who benefited** | Consumers (lower fees due to competition threat), fintechs (can build on M-Pesa rails), regulatory goal achieved (more competition) |
| **Who lost** | Safaricom (some margin compression), competitors (still can't break network effects) |

---

**KEY ECONOMIC INSIGHT:**

M-Pesa succeeded because:
1. **Transaction costs**: Eliminated need for bank branches (agent model)
2. **Network effects**: Early critical mass created self-reinforcing adoption
3. **Two-sided market**: Became a platform, not just a payment service
4. **Regulatory timing**: Launched before heavy regulation - "permissionless innovation"

The 2% of GDP flowing through M-Pesa annually demonstrates how payment innovation can transform an entire economy. But also shows winner-take-all dynamics - even with regulation, M-Pesa maintains near-monopoly due to network effects.

### Presentation Talking Points
- Each transition should identify specific economic forces (transaction costs, network effects, regulatory changes)
- Note winners AND losers - digital finance always has distributional consequences
- M-Pesa's success wasn't just technology - it was agent network (reduced transaction costs) + first-mover (network effects)
- The "surprising finding" might be: despite regulation, M-Pesa still has 99% share - network effects are extremely sticky [Market share data as of 2025]
- Key economic insight: Payment innovation follows the pattern - new technology reduces transaction costs, early mover captures network effects, regulation follows to address market failures

---

## Exercise 7: Network Effects Deep Dive

**Category**: Comparative Analysis
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Worksheet, calculator optional

### Task

Compare how network effects work differently across three digital finance platforms: Bitcoin, Visa, and Uniswap.

### Model Answer / Expected Output

**Completed Comparison Matrix:**

| Dimension | Bitcoin | Visa | Uniswap |
|-----------|---------|------|---------|
| **Type of Network Effect** | **Direct + Indirect** | **Two-sided (Indirect)** | **Direct (Liquidity)** |
| | Direct: More users = more nodes = more secure network | Merchants need cardholders; cardholders need merchant acceptance | More liquidity = less slippage = more traders = more liquidity |
| | Indirect: More users = more services (exchanges, wallets, ATMs) | Classic two-sided market | Also indirect: more tokens listed = more useful |
| **Critical Mass** | **~1,000 nodes minimum** | **~10% merchant coverage** | **~$10M TVL per pool** |
| | For security, needs distributed mining/validation | Cardholders won't carry card nobody accepts | Below this, slippage too high for meaningful trades |
| | Market cap critical mass ~$10B for institutional interest | For Visa, achieved decades ago | Uniswap V2 achieved this in 2020 [Historical milestone as of 2025] |
| **Switching Costs** | **Low for users, High for miners** | **Low for users, Medium for merchants** | **Very Low** |
| | Users can hold BTC anywhere | Users can easily get new card | No lock-in, can move tokens instantly |
| | Miners have sunk hardware costs | Merchants have POS terminal integration | Liquidity providers can withdraw anytime |
| | Developers have protocol knowledge | | No long-term commitment |
| **Winner-Take-All?** | **No - Multiple cryptocurrencies coexist** | **Partial - Visa/Mastercard duopoly** | **Partial - Multiple DEXs coexist** |
| | Different chains serve different purposes | Strong network effects but regulated to allow competition | Uniswap dominant but Curve, Sushiswap viable |
| | Bitcoin, Ethereum, stablecoins all survive | Regional networks (UnionPay, JCB) survive in home markets | Different DEXs specialize (Curve = stablecoins) |
| **Value Capture** | **Miners > Exchanges > Holders** | **Visa > Banks > Merchants > Consumers** | **LPs > Token Holders > Traders** |
| | Miners capture fees + block rewards | Visa captures ~0.15% of transaction | Liquidity providers earn 0.3% fees |
| | Exchanges profit from spread/fees | Issuing banks capture ~1.5% interchange | UNI token holders capture governance value |
| | Holders capture appreciation (if any) | Merchants pay, pass to consumers | Traders pay fees but gain access to liquidity |

---

**Detailed Analysis by Question:**

**1. Direct vs Indirect Network Effects:**

| Platform | Direct | Indirect |
|----------|--------|----------|
| **Bitcoin** | Yes - more nodes = more security, more holders = more liquid market | Yes - more users = more ATMs, exchanges, payment processors |
| **Visa** | No direct | Yes - classic two-sided market (merchants ↔ cardholders) |
| **Uniswap** | Yes - liquidity network effect (more LP = better execution) | Yes - more tokens listed = more useful platform |

**2. Two-Sided Market Analysis:**

| Platform | Side A | Side B | Harder to Attract |
|----------|--------|--------|-------------------|
| **Bitcoin** | Holders/Users | Miners/Validators | **Miners** (capital intensive, must be economically viable) |
| **Visa** | Cardholders | Merchants | **Merchants** (must integrate, pay fees) - solved by subsidizing through rewards |
| **Uniswap** | Traders | Liquidity Providers | **Liquidity Providers** (capital risk, impermanent loss) - solved by fee sharing |

**3. 10-Year Growth Prediction:**

**Prediction: Visa will grow most (in absolute terms), Uniswap will grow most (in percentage terms)**

**Justification:**

| Platform | Growth Trajectory | Reasoning |
|----------|-------------------|-----------|
| **Bitcoin** | Moderate (3-5x) | Network effects already mature; growth depends on institutional adoption; competition from other L1s |
| **Visa** | Steady (2-3x) | Strongest existing network effects; benefits from global digitization; protected by regulation; low-risk steady growth |
| **Uniswap** | High (10-50x) | Starting from smaller base; DeFi growing as asset class; network effects still building; but existential regulatory risk |

**Most Confident Prediction:** Visa - because its network effects are mature, sticky, and protected by regulatory moat. Payment network effects are among the strongest in economics.

**Wildcard:** If CBDC adoption is high and open, could disintermediate card networks. But likely 20+ year timeframe.

### Presentation Talking Points
- Bitcoin has network effects but they're different from traditional financial networks (security-based, not acceptance-based)
- Visa's network effects are the "gold standard" - two-sided, entrenched, protected by regulation
- Uniswap demonstrates that DeFi can achieve network effects, but they're more fragile (no switching costs)
- Key economic insight: Network effects are not binary - different types (direct/indirect/two-sided) have different dynamics and durability
- Winner-take-all is rare in practice - usually see oligopolies with 2-3 major players

---

## Exercise 8: Economic vs Technical Questions

**Category**: Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Individual (15 min) then pair discussion (10 min) then class share (5 min)
**Materials Needed**: Worksheet with questions below

### Task

L01 emphasized distinguishing economic from technical questions. Classify each question as Economic (E) or Technical (T), then provide economic answers for the E questions.

### Model Answer / Expected Output

**Classification and Explanations:**

| # | Question | Answer | Explanation |
|---|----------|--------|-------------|
| 1 | How does Bitcoin mining use electricity? | **T** | Describes a mechanism - how proof-of-work algorithm requires computational effort that consumes energy |
| 2 | Why do people mine Bitcoin despite the electricity cost? | **E** | About incentives - miners rationally calculate: if (block reward + fees) > (electricity + hardware cost), mining is profitable. Profit motive explains behavior. |
| 3 | What programming language are smart contracts written in? | **T** | Implementation detail - Solidity for Ethereum, Rust for Solana, etc. |
| 4 | How do smart contracts reduce contracting costs? | **E** | About efficiency - smart contracts eliminate: (1) legal drafting costs, (2) enforcement costs (self-executing), (3) intermediary costs (no escrow needed), (4) dispute resolution costs (deterministic) |
| 5 | What is the block size limit on Bitcoin? | **T** | Technical parameter - 1MB base block, ~4MB with SegWit |
| 6 | Why do users pay higher fees when the network is congested? | **E** | Price mechanism / scarcity - block space is scarce; users bid (via fees) for limited slots; basic supply and demand determines fee market clearing price |
| 7 | How does a hash function work? | **T** | Algorithm description - takes input, produces fixed-length output, one-way (can't reverse) |
| 8 | Why is proof-of-work considered secure? | **E** | About incentives for attack - attacking requires 51% of hash power; cost of attack (~$10B+) exceeds potential gain; rational actors won't attack. Economic security, not just technical. [Cost estimates as of 2025] |
| 9 | What consensus mechanism does Ethereum use? | **T** | Mechanism identification - proof-of-stake (since Sept 2022) [Historical transition date as of 2025] |
| 10 | Why did Ethereum switch from proof-of-work to proof-of-stake? | **E** | Complex economic reasoning: (1) Environmental externalities - PoW energy use created negative externalities and PR problems; (2) Security economics - PoS can achieve similar security at lower cost; (3) Scalability economics - enables sharding for higher throughput; (4) Governance/politics - community valued sustainability |

---

**Economic Answers for Questions 2, 4, 6, 8, 10:**

**Q2: Why do people mine Bitcoin despite the electricity cost?**
> Mining is economically rational when expected revenue (block reward ~3.125 BTC + transaction fees) exceeds costs (electricity + hardware depreciation + opportunity cost of capital). Miners locate where electricity is cheapest (often stranded energy), use most efficient hardware, and shut down when unprofitable. The difficulty adjustment ensures mining remains marginally profitable for the most efficient miners.

**Q4: How do smart contracts reduce contracting costs?**
> Smart contracts reduce transaction costs in four ways: (1) Search and information costs reduced by standardized templates; (2) Bargaining costs reduced by take-it-or-leave-it code; (3) Enforcement costs eliminated by automatic execution; (4) Counterparty risk reduced by trustless escrow. Total contracting cost reduction can be 90%+ for simple agreements.

**Q6: Why do users pay higher fees when the network is congested?**
> Bitcoin block space is a scarce resource (~4MB every 10 minutes). Users bid for inclusion via transaction fees - a price mechanism allocates scarce block space to highest-value transactions. During congestion, the market-clearing price rises as demand exceeds supply. This is efficient: high-value transfers (institutional, large) outbid low-value (coffee purchase), ensuring scarce capacity goes to highest-value uses.

**Q8: Why is proof-of-work considered secure?**
> Security is economic, not just technical. A 51% attack requires controlling majority hash power - currently costing ~$10B+ in hardware alone, plus ongoing electricity costs of ~$40M/day. The expected gain from attacking (double-spending) is less than the cost for any plausible attacker. Additionally, attacking devalues the attacker's own Bitcoin holdings and hardware. Incentives align against attack. [Cost estimates as of February 2025]

**Q10: Why did Ethereum switch from proof-of-work to proof-of-stake?**
> Four economic reasons: (1) **Externalities**: PoW consumed ~80 TWh/year (Belgium's electricity consumption), creating negative environmental externalities and regulatory pressure; (2) **Cost efficiency**: PoS achieves similar economic security at ~99.9% lower energy cost - security doesn't require physical work; (3) **Monetary policy**: PoS enables lower issuance (ETH became deflationary) - reduced "tax" on holders; (4) **Scalability**: Enables sharding, increasing throughput from ~15 TPS to potentially thousands - economic necessity for DeFi growth. [Energy and performance data as of February 2025]

### Presentation Talking Points
- Economic questions ask "why" (incentives, trade-offs, welfare); technical questions ask "how" (mechanism, implementation)
- This course focuses on economic questions - we care about behavior, not code
- Even "technical" things like consensus mechanisms have economic foundations - PoW security is economic (attack cost > gain)
- Key insight: The same phenomenon can be analyzed technically or economically - this course chooses the economic lens because that's what predicts behavior and informs policy
- Example: "Why are gas fees high?" Economic answer (scarcity, bidding) is more useful than technical answer (EVM computation metering) for understanding user behavior

---

**PLAN_READY: .omc/plans/l01-in-class-exercises.md**
