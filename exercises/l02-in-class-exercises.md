# L02 In-Class Exercises: Monetary Economics of Digital Currencies

## Plan Metadata
- **Created**: 2026-02-04
- **Lesson**: L02 - Monetary Economics of Digital Currencies
- **Target Audience**: BSc students (completed L01 Introduction, now in L02)
- **Time Allocation**: 30 minutes work + 5 minutes presentation per exercise
- **Instructor Choice**: Select 1-2 exercises per session based on class size and learning goals

---

## Exercise Overview

| # | Title | Category | Group Size | Materials |
|---|-------|----------|------------|-----------|
| 1 | Stablecoin Peg Deviation Analyzer | Python/Data | Individual or Pairs | Laptop with Python |
| 2 | Quantity Theory Applied: Bitcoin vs Ethereum | Framework Application | Groups of 3-4 | Worksheet + Calculator |
| 3 | Terra/LUNA Death Spiral Autopsy | Case Study | Groups of 3-4 | Case Handout |
| 4 | Algorithmic Stablecoins Can Work | Debate/Discussion | Two Teams (4-6 each) | None |
| 5 | Design a Stability Mechanism | Creative/Design | Groups of 3-4 | Whiteboard/Paper |
| 6 | Gresham's Law in Crypto Markets | Comparative Analysis | Groups of 3-4 | Worksheet |
| 7 | Seigniorage Calculator: Who Profits from Money? | Python/Data | Individual or Pairs | Laptop with Python |
| 8 | Currency Substitution Case Study | Framework Application | Groups of 3-4 | Case Handout |

---

## Exercise 1: Stablecoin Peg Deviation Analyzer

**Category**: Python/Data
**Time**: 30 min work + 5 min presentation
**Group Size**: Individual or Pairs
**Materials Needed**: Laptop with Python (yfinance, pandas, matplotlib, numpy), internet access

### Task

Analyze the stability of major stablecoins (USDT, USDC, DAI) by measuring their peg deviations over time. Create a publication-ready chart showing:
1. Historical price deviations from $1.00
2. Volatility comparison between stablecoins
3. Identification of major depeg events

Answer: Which stablecoin type (fiat-backed vs crypto-backed) is more stable, and why?

### Complete Code

```python
"""
Stablecoin Peg Deviation Analysis
L02 Exercise - Monetary Economics of Digital Currencies

Requirements: pip install yfinance pandas matplotlib numpy
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# =============================================================================
# DATA COLLECTION
# =============================================================================

# Define date range (2 years to capture recent market events)
end_date = datetime.now()
start_date = end_date - timedelta(days=2*365)

print("Fetching stablecoin price data from Yahoo Finance...")

# Fetch major stablecoins
usdt = yf.download('USDT-USD', start=start_date, end=end_date, progress=False)
usdc = yf.download('USDC-USD', start=start_date, end=end_date, progress=False)
dai = yf.download('DAI-USD', start=start_date, end=end_date, progress=False)

print("Data fetched successfully!")

# =============================================================================
# PEG DEVIATION CALCULATION
# =============================================================================

# Calculate deviation from $1.00 peg (in basis points: 1 bp = 0.01%)
usdt['deviation_bp'] = (usdt['Close'] - 1.0) * 10000
usdc['deviation_bp'] = (usdc['Close'] - 1.0) * 10000
dai['deviation_bp'] = (dai['Close'] - 1.0) * 10000

# Calculate absolute deviation for volatility metrics
usdt['abs_deviation'] = abs(usdt['Close'] - 1.0)
usdc['abs_deviation'] = abs(usdc['Close'] - 1.0)
dai['abs_deviation'] = abs(dai['Close'] - 1.0)

# =============================================================================
# SUMMARY STATISTICS
# =============================================================================

print("\n" + "="*70)
print("STABLECOIN PEG DEVIATION ANALYSIS")
print("="*70)

stats = pd.DataFrame({
    'Stablecoin': ['USDT (Fiat-backed)', 'USDC (Fiat-backed)', 'DAI (Crypto-backed)'],
    'Type': ['Fiat-backed', 'Fiat-backed', 'Crypto-backed'],
    'Mean Deviation (bp)': [
        usdt['deviation_bp'].mean(),
        usdc['deviation_bp'].mean(),
        dai['deviation_bp'].mean()
    ],
    'Std Deviation (bp)': [
        usdt['deviation_bp'].std(),
        usdc['deviation_bp'].std(),
        dai['deviation_bp'].std()
    ],
    'Max Depeg (bp)': [
        usdt['deviation_bp'].abs().max(),
        usdc['deviation_bp'].abs().max(),
        dai['deviation_bp'].abs().max()
    ],
    'Days Outside 50bp': [
        (usdt['abs_deviation'] > 0.005).sum(),
        (usdc['abs_deviation'] > 0.005).sum(),
        (dai['abs_deviation'] > 0.005).sum()
    ]
})

print(stats.to_string(index=False))

# =============================================================================
# IDENTIFY MAJOR DEPEG EVENTS
# =============================================================================

print("\n" + "="*70)
print("MAJOR DEPEG EVENTS (>100 basis points)")
print("="*70)

def find_depeg_events(df, name, threshold_bp=100):
    """Find dates where depeg exceeded threshold"""
    major_depegs = df[abs(df['deviation_bp']) > threshold_bp]
    if len(major_depegs) > 0:
        print(f"\n{name}:")
        for date, row in major_depegs.head(10).iterrows():
            print(f"  {date.strftime('%Y-%m-%d')}: ${row['Close']:.4f} ({row['deviation_bp']:+.0f} bp)")
    else:
        print(f"\n{name}: No depegs >100bp in period")

find_depeg_events(usdt, "USDT")
find_depeg_events(usdc, "USDC")
find_depeg_events(dai, "DAI")

# =============================================================================
# PUBLICATION-READY CHART
# =============================================================================

plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(2, 1, figsize=(14, 10), dpi=100)

# Panel A: Time series of deviations
ax1 = axes[0]
ax1.plot(usdt.index, usdt['deviation_bp'],
         label='USDT (Tether)', color='#26A17B', linewidth=1.2, alpha=0.8)
ax1.plot(usdc.index, usdc['deviation_bp'],
         label='USDC (Circle)', color='#2775CA', linewidth=1.2, alpha=0.8)
ax1.plot(dai.index, dai['deviation_bp'],
         label='DAI (MakerDAO)', color='#F5AC37', linewidth=1.2, alpha=0.8)

# Add reference bands
ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax1.axhline(y=50, color='red', linestyle='--', alpha=0.3, label='Warning threshold (+/-50bp)')
ax1.axhline(y=-50, color='red', linestyle='--', alpha=0.3)
ax1.axhspan(-50, 50, alpha=0.1, color='green', label='Stable zone')

ax1.set_title('Panel A: Stablecoin Peg Deviations Over Time', fontsize=12, fontweight='bold')
ax1.set_xlabel('Date', fontsize=10)
ax1.set_ylabel('Deviation from $1.00 (basis points)', fontsize=10)
ax1.legend(loc='upper right', fontsize=9)
ax1.set_ylim(-300, 300)

# Panel B: Distribution of deviations
ax2 = axes[1]
bins = np.linspace(-200, 200, 81)

ax2.hist(usdt['deviation_bp'].dropna(), bins=bins, alpha=0.5,
         label='USDT', color='#26A17B', density=True)
ax2.hist(usdc['deviation_bp'].dropna(), bins=bins, alpha=0.5,
         label='USDC', color='#2775CA', density=True)
ax2.hist(dai['deviation_bp'].dropna(), bins=bins, alpha=0.5,
         label='DAI', color='#F5AC37', density=True)

ax2.axvline(x=0, color='black', linestyle='-', linewidth=1)
ax2.axvline(x=-50, color='red', linestyle='--', alpha=0.5)
ax2.axvline(x=50, color='red', linestyle='--', alpha=0.5)

ax2.set_title('Panel B: Distribution of Peg Deviations', fontsize=12, fontweight='bold')
ax2.set_xlabel('Deviation from $1.00 (basis points)', fontsize=10)
ax2.set_ylabel('Density', fontsize=10)
ax2.legend(loc='upper right', fontsize=9)

# Add source note
fig.text(0.99, 0.01, 'Data: Yahoo Finance | Note: 1 basis point = 0.01%',
         fontsize=8, ha='right', alpha=0.7)

plt.tight_layout()
plt.savefig('stablecoin_peg_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nChart saved as 'stablecoin_peg_analysis.png'")

# =============================================================================
# ECONOMIC ANALYSIS
# =============================================================================

print("\n" + "="*70)
print("ECONOMIC ANALYSIS: Stablecoin Stability Mechanisms")
print("="*70)

print("""
KEY FINDINGS:

1. STABILITY RANKING (most to least stable):
   - USDC: Tightest peg maintenance, regulated issuer, transparent reserves
   - USDT: Generally stable but larger tail events, less transparent
   - DAI: Wider fluctuations due to crypto collateral volatility

2. MECHANISM ANALYSIS:

   FIAT-BACKED (USDT, USDC):
   + Direct arbitrage: If price < $1, buy stablecoin, redeem for $1
   + Clear economic floor and ceiling from redemption guarantee
   - Trust in issuer and reserve composition
   - Counterparty risk (issuer could freeze/fail)

   CRYPTO-BACKED (DAI):
   + Transparent, on-chain collateral
   + Decentralized governance
   - Collateral volatility propagates to stablecoin
   - Liquidation cascades during market stress
   - Over-collateralization is capital inefficient

3. WHY FIAT-BACKED IS MORE STABLE:
   - Direct link to stable asset (USD in bank)
   - Simpler arbitrage mechanism
   - Professional market makers maintain peg
   - Redemption guarantee creates hard bounds

4. WHY DAI HAS WIDER DEVIATIONS:
   - Collateral (ETH) can drop 30-50% in days
   - Liquidation auctions don't always clear at par
   - Smart contract risk adds uncertainty premium
   - Governance decisions can affect stability

5. POLICY IMPLICATIONS:
   - Fiat-backed coins trade stability for centralization
   - Crypto-backed coins trade stability for decentralization
   - Neither achieves the stability of bank deposits
   - This is why CBDCs are being developed
""")
```

### Model Answer / Expected Output

**Expected Chart Description:**
- Panel A: Time series showing all three stablecoins fluctuating around 0 basis points
- USDC (blue) tightest band, mostly within +/- 20bp
- USDT (green) slightly wider, occasional spikes to +/- 50bp
- DAI (orange) widest band, reaching +/- 100bp during stress
- Notable events: March 2023 USDC depeg (SVB collapse), periodic DAI stress during ETH volatility

**Key Quantitative Findings:**

| Stablecoin | Type | Mean Deviation | Std Dev | Max Depeg |
|------------|------|----------------|---------|-----------|
| USDC | Fiat-backed | ~0.5 bp | ~15 bp | ~300 bp (SVB event) |
| USDT | Fiat-backed | ~-2 bp | ~20 bp | ~150 bp |
| DAI | Crypto-backed | ~5 bp | ~40 bp | ~200 bp |

**Economic Conclusion:**

Fiat-backed stablecoins (USDC, USDT) are more stable than crypto-backed (DAI) because:

1. **Arbitrage clarity**: With USDC, if price = $0.99, arbitrageur buys, redeems at issuer for $1.00, profits $0.01. This creates hard price floor.

2. **Collateral stability**: USD reserves don't fluctuate in value (in USD terms). ETH collateral for DAI can crash 50%, creating liquidation cascades.

3. **Professional market makers**: Circle/Tether have institutional relationships with market makers who maintain tight spreads.

4. **Redemption guarantee**: Legal claim on reserves creates confidence; smart contracts cannot provide equivalent guarantee.

**Trade-off identified**: Stability comes at cost of centralization. DAI sacrifices stability for decentralization. This is the fundamental stablecoin trilemma.

### Presentation Talking Points
- Stablecoin stability is empirically measurable - we can quantify "how stable is stable"
- Fiat-backed stablecoins maintain tighter pegs due to clearer arbitrage and stable collateral
- DAI's crypto-backing means its stability inherits ETH's volatility
- The March 2023 USDC depeg (SVB collapse) shows even fiat-backed coins have tail risks
- Key economic insight: There's a stability-decentralization trade-off; you can't have both maximum stability AND full decentralization
- This analysis explains why central banks are skeptical of algorithmic stablecoins

---

## Exercise 2: Quantity Theory Applied: Bitcoin vs Ethereum

**Category**: Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Printed worksheet, calculator (or phone)

### Task

Apply the Quantity Theory of Money (MV = PY) to analyze Bitcoin and Ethereum. Calculate velocity, interpret what it means, and assess whether these cryptocurrencies function as money based on your findings.

**Given Data (approximate 2024/2025 figures):**

| Metric | Bitcoin | Ethereum |
|--------|---------|----------|
| Market Cap (M x P proxy) | $800 billion | $350 billion |
| Daily On-chain Volume | $15 billion | $8 billion |
| Estimated "Economic" Volume | $8 billion | $5 billion |
| Total Supply (M) | 19.5 million BTC | 120 million ETH |
| Average Price (P) | ~$41,000 | ~$2,900 |

### Model Answer / Expected Output

**Part 1: Velocity Calculation**

For traditional money, velocity is calculated as:
$$V = \frac{PY}{M} = \frac{\text{Nominal GDP}}{\text{Money Supply}}$$

For cryptocurrencies, we adapt:
$$V = \frac{\text{Annual Transaction Volume}}{\text{Market Cap}}$$

**Bitcoin Velocity Calculation:**
- Annual economic volume: $8B/day x 365 = $2,920 billion
- Market cap: $800 billion
- $V_{BTC} = \frac{2920}{800} = 3.65$

**Ethereum Velocity Calculation:**
- Annual economic volume: $5B/day x 365 = $1,825 billion
- Market cap: $350 billion
- $V_{ETH} = \frac{1825}{350} = 5.21$

**Comparison with Traditional Money:**
| Currency | Velocity |
|----------|----------|
| US Dollar (M1) | ~5.5 |
| US Dollar (M2) | ~1.3 |
| Bitcoin | ~3.7 |
| Ethereum | ~5.2 |

**Part 2: Interpretation**

**Bitcoin Velocity Analysis:**
- V = 3.7 suggests moderate circulation relative to value held
- Lower than M1 velocity indicates significant "store of value" holding (HODL behavior)
- Consistent with Gresham's Law: Bitcoin is hoarded, not spent
- If Bitcoin were truly used as medium of exchange, V would be higher

**Ethereum Velocity Analysis:**
- V = 5.2 is higher than Bitcoin, closer to M1 velocity
- Reflects Ethereum's use in DeFi, NFTs, gas payments
- Money is actually circulating (being used), not just held
- Suggests Ethereum functions more as "utility money" than store of value

**Part 3: Money Function Assessment**

| Function | Bitcoin | Ethereum |
|----------|---------|----------|
| **Medium of Exchange** | Poor (low V, HODL culture) | Moderate (higher V, DeFi usage) |
| **Unit of Account** | Poor (prices rarely in BTC) | Poor (ETH used, but prices in USD) |
| **Store of Value** | Mixed (held but volatile) | Poor (primarily utility) |

**Part 4: Quantity Theory Implications**

If MV = PY and we consider crypto as an economy:

**Bitcoin "Economy":**
- M is fixed (approaching 21M)
- V is relatively stable/low (HODL behavior)
- If Y grows (more adoption), P must rise
- Deflationary pressure: each BTC buys more over time
- Problem: Deflation discourages spending (why spend if BTC will be worth more tomorrow?)

**Ethereum "Economy":**
- M is variable (can be inflationary or deflationary post-merge)
- V is higher and more volatile
- Y includes DeFi activity, NFTs, smart contracts
- P adjusts based on demand for blockspace/utility
- More "monetary" behavior but still primarily speculation-driven

**Key Insight:**
The quantity theory reveals that Bitcoin's fixed M and moderate V make it deflationary, discouraging its use as medium of exchange (Gresham's Law). Ethereum's higher V suggests more actual usage, but both fail as unit of account due to P (price) volatility.

### Presentation Talking Points
- Velocity tells us whether crypto is being used (high V) or hoarded (low V)
- Bitcoin's moderate velocity (~3.7) confirms HODL behavior - it's held, not spent
- Ethereum's higher velocity (~5.2) reflects DeFi activity - it's actually being used
- The quantity theory shows Bitcoin is structurally deflationary (fixed M, stable V, growing Y means rising P)
- Deflationary money discourages spending - you don't want to be the Bitcoin pizza guy
- Key economic insight: Velocity measurement empirically confirms that Bitcoin behaves like gold (store of value) while Ethereum behaves more like utility money

---

## Exercise 3: Terra/LUNA Death Spiral Autopsy

**Category**: Case Study
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Case handout with timeline below

### Task

Analyze the Terra/LUNA collapse of May 2022 using the monetary economics framework from L02. Identify which specific monetary mechanisms failed and why the death spiral was inevitable once confidence broke.

**Case Timeline:**

| Date | Event | UST Price | LUNA Price |
|------|-------|-----------|------------|
| May 7, 2022 | Large UST withdrawals from Anchor | $1.00 | $80 |
| May 8, 2022 | UST loses peg, drops to $0.98 | $0.98 | $65 |
| May 9, 2022 | Panic selling begins | $0.67 | $30 |
| May 10, 2022 | LFG deploys Bitcoin reserves | $0.30 | $1.50 |
| May 11, 2022 | Chain halted, hyperinflation of LUNA | $0.10 | $0.0001 |
| May 12, 2022 | Total collapse | ~$0 | ~$0 |

**Key Mechanism:** UST was "algorithmic" - when UST < $1, users could burn UST for $1 worth of LUNA. This was supposed to reduce UST supply and restore the peg.

### Model Answer / Expected Output

**Part 1: The Mechanism (How It Was Supposed to Work)**

```
Normal Operation:
1. If UST = $0.99 (below peg)
2. Arbitrageur buys 1 UST for $0.99
3. Burns UST, receives $1.00 worth of LUNA
4. Sells LUNA for $1.00
5. Profit: $0.01
6. UST supply decreases, price rises toward $1.00
```

This is classic monetary arbitrage - the same mechanism that maintains currency pegs. The problem: it only works when LUNA has stable value.

**Part 2: The Death Spiral Mechanism**

```
Death Spiral (What Actually Happened):
1. UST = $0.99 (slightly below peg)
2. Many arbitrageurs burn UST for LUNA
3. LUNA supply increases dramatically
4. LUNA price falls due to selling pressure
5. Now need MORE LUNA minted to maintain $1 redemption value
6. LUNA falls further, confidence breaks
7. UST holders panic-sell, pushing UST lower
8. Even more LUNA minted, hyperinflation
9. LUNA price -> $0, arbitrage mechanism fails completely
10. UST has no floor, collapses to ~$0
```

**Part 3: Monetary Economics Framework Analysis**

| Concept | Application to Terra/LUNA |
|---------|---------------------------|
| **Seigniorage** | Terra ecosystem captured seigniorage from UST issuance (20% Anchor yield funded by new UST demand). This was unsustainable - paying depositors with new depositor money (Ponzi dynamics). |
| **Velocity** | When confidence broke, velocity spiked - everyone trying to exit simultaneously. High V with fixed/growing M means P must fall. |
| **Gresham's Law** | In reverse: "Good money drives out bad" when peg breaks. UST became "bad money" that nobody wanted to hold, while LUNA became worthless backing. |
| **Money Multiplier** | DeFi leverage amplified the collapse. UST was used as collateral, creating credit money on top of unbacked stablecoin - a multiplier on instability. |
| **Inflation Tax** | LUNA holders experienced hyperinflation - their holdings diluted from 350M to 6.5 trillion LUNA in days. This was the "inflation tax" concentrated in time. |

**Part 4: Why the Death Spiral Was Inevitable**

1. **Circular Backing**: UST was backed by LUNA, but LUNA's value depended on UST demand. This is circular, not backed by external value.

2. **Reflexivity**: Unlike fiat-backed stablecoins (backed by USD that doesn't depend on stablecoin), Terra's backing got weaker as the stablecoin got weaker.

3. **No Lender of Last Resort**: Central banks can print unlimited currency to defend pegs. Terra had no equivalent - the "printing" (LUNA minting) made things worse.

4. **Confidence Game**: All money is confidence, but fiat money has government enforcement, taxes payable in currency, legal tender laws. UST had only arbitrage incentives.

5. **Bank Run Dynamics**: Like a classic bank run, individual rationality (exit first) led to collective disaster. No deposit insurance equivalent.

**Part 5: Contrast with Fiat-Backed Stablecoins**

| Aspect | Algorithmic (UST) | Fiat-Backed (USDC) |
|--------|-------------------|---------------------|
| Backing | Circular (LUNA) | External (USD) |
| Arbitrage | Requires LUNA value | Independent of crypto |
| Stress response | Backing weakens | Backing unchanged |
| Floor price | None (can go to $0) | ~$1 (redemption guarantee) |
| Death spiral risk | High | Low (barring issuer failure) |

**Key Insight:**

The Terra collapse demonstrates a fundamental monetary economics principle: money must be backed by something outside of itself. LUNA backing UST, where LUNA's value derived from UST demand, violated this principle. It was a perpetual motion machine that worked until it didn't.

### Presentation Talking Points
- Terra/LUNA is a textbook example of monetary economics failure - every concept from L02 applies
- The death spiral mechanism shows why algorithmic stablecoins without external collateral are inherently fragile
- Seigniorage capture (20% Anchor yield) was the warning sign - unsustainable yields indicate unsustainable backing
- Contrast with fiat-backed: USDC's backing (USD) doesn't get weaker when USDC is stressed
- Historical parallel: Currency boards that fail when speculators test them (Asian Financial Crisis 1997)
- Key economic insight: Circular backing creates reflexive doom loops; external backing creates stability
- This is why regulators now treat algorithmic stablecoins differently (EU MiCA effectively bans them)

---

## Exercise 4: Algorithmic Stablecoins Can Work

**Category**: Debate/Discussion
**Time**: 30 min work + 5 min presentation (final debate)
**Group Size**: Two teams of 4-6 students each
**Materials Needed**: None (timer helpful)

### Task

Structured debate on the motion: **"Algorithmic stablecoins can be designed to work safely and should not be banned."**

**Team A (Pro)**: Algorithmic stablecoins can work
**Team B (Con)**: They are fundamentally flawed and should be banned

**Debate Structure:**
| Phase | Time | Activity |
|-------|------|----------|
| Preparation | 15 min | Teams prepare 3 main arguments using L02 concepts |
| Opening | 3 min each | Each team presents main arguments |
| Rebuttal Prep | 5 min | Teams prepare responses |
| Rebuttals | 2 min each | Each team responds to opponent |
| Closing | 2 min each | Final summary |

**Required L02 Concepts**: Use at least 2 per team from:
- Seigniorage
- Velocity of money
- Gresham's Law
- Quantity theory (MV=PY)
- Money functions (MoE, UoA, SoV)
- Arbitrage mechanisms
- Death spiral dynamics

### Model Answer / Expected Output

**Team A (Pro - Algorithmic Stablecoins Can Work):**

**Argument 1: Terra Was a Flawed Design, Not a Category Failure**
- L02 Concept: *Seigniorage*
- Terra's flaw: Circular backing (UST backed by LUNA whose value depended on UST)
- Better design: Partial collateralization with external assets + algorithmic component
- Example: FRAX uses fractional collateral (USDC) + algorithmic supply adjustment
- When UST failed, FRAX maintained peg because it had external backing as floor
- Analogy: Early airplanes crashed, but we improved designs, didn't ban aviation

**Argument 2: Algorithmic Mechanisms Can Reduce Capital Inefficiency**
- L02 Concept: *Quantity theory (MV=PY)*
- Problem with 100% fiat-backing: $100B in stablecoins = $100B locked in low-yield assets
- Algorithmic supply adjustment can provide same stability with less capital
- MV=PY shows: if you can control M dynamically, you can maintain stable P
- Protocol-controlled value (PCV) models hold productive assets, not just cash
- This improves capital efficiency for the entire DeFi ecosystem

**Argument 3: Decentralization Requires Non-Centralized Stability**
- L02 Concept: *Gresham's Law*
- Fiat-backed stablecoins can be frozen, blacklisted (USDC blocked Tornado Cash addresses)
- If "bad" (censorable) stablecoins drive out "good" (censorship-resistant), decentralization fails
- Algorithmic designs like RAI (reflexer) are fully decentralized - no admin keys
- Society needs censorship-resistant money for legitimate uses (human rights, dissidents)
- Banning algorithmic stablecoins forces dependence on centralized, censorable money

**Rebuttal Points Against Con:**
- "Terra proved they don't work" - One design failure doesn't condemn a category
- "Users lost $40B" - Users also lost money in regulated banks (SVB); bad actors exist everywhere
- "No external backing" - Partial collateralization models provide backing

---

**Team B (Con - Algorithmic Stablecoins Are Fundamentally Flawed):**

**Argument 1: The Arbitrage Mechanism Fails Under Stress**
- L02 Concept: *Velocity of money / Death spiral*
- Algorithmic stablecoins rely on arbitrageurs restoring peg
- Under stress, velocity spikes (everyone exits simultaneously)
- Arbitrageurs face unlimited downside if mechanism fails
- Rational arbitrageurs step back precisely when most needed
- This is procyclical - makes bad situations worse, not better
- Evidence: Every major algorithmic stablecoin has depegged under stress

**Argument 2: Circular Backing Violates Basic Monetary Economics**
- L02 Concept: *Store of value function*
- Store of value requires backing by something stable
- If backing asset's value depends on the stablecoin's success, it's circular
- "Partial collateralization" just means "partially backed" - still undercollateralized
- When you most need the backing (during crisis), it's worth least
- This is the definition of a confidence game - only works when nobody tests it

**Argument 3: Seigniorage Capture Creates Misaligned Incentives**
- L02 Concept: *Seigniorage*
- Algorithmic stablecoin creators capture seigniorage (profit from issuance)
- This creates incentive to maximize issuance, minimize collateral
- Terra offered 20% yield to attract deposits - funded by seigniorage, unsustainable
- Fiat-backed issuers have aligned incentives (reputation, regulatory compliance)
- Private seigniorage + algorithmic instability = systematic consumer harm

**Rebuttal Points Against Pro:**
- "FRAX survived" - FRAX is >90% collateralized now; barely algorithmic
- "Capital efficiency" - Efficiency that collapses to zero when needed isn't efficiency
- "Decentralization needs this" - DAI is decentralized and collateralized; false choice

---

**Balanced Verdict (for instructor):**

The economically stronger position is **Con** (algorithmic stablecoins are fundamentally flawed), but the Pro arguments have merit:

**Why Con is stronger:**
1. The arbitrage mechanism mathematically fails when both sides of a trade are falling
2. No algorithmic stablecoin has survived major market stress without substantial collateral backing
3. Empirical track record: Iron Finance, UST, TITAN, AMPL - all failed or abandoned pure algorithmic model

**Where Pro has merit:**
1. Hybrid models (partial collateral + algorithmic adjustment) might be viable
2. Banning experimentation prevents innovation
3. Censorship-resistance is a legitimate concern

**Regulatory consensus:** EU MiCA and proposed US legislation treat algorithmic stablecoins differently (higher restrictions) than fully-backed stablecoins - acknowledging the fundamental risk difference.

### Presentation Talking Points
- This debate illuminates the core tension: capital efficiency vs stability
- Terra/LUNA showed the failure mode; FRAX showed partial collateral can help
- Key monetary insight: Backing must be external and independent of the stablecoin's value
- "Algorithmic" often becomes marketing term for "undercollateralized"
- Regulatory trend is toward requiring substantial backing, effectively restricting pure algorithmic models
- The debate forces students to articulate why monetary backing matters

---

## Exercise 5: Design a Stability Mechanism

**Category**: Creative/Design
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Whiteboard, flip chart, or paper; colored markers

### Task

Your team is hired by a DeFi protocol to design a stablecoin stability mechanism. Design a novel approach that addresses the weaknesses of existing models (algorithmic, fiat-backed, crypto-backed).

**Design Requirements:**
1. **Primary stability mechanism**: How does the coin maintain its $1 peg?
2. **Stress response**: What happens when price drops to $0.95? $0.80?
3. **Collateral strategy**: What backs the coin and why?
4. **Seigniorage distribution**: Who captures the profit from issuance?
5. **Death spiral prevention**: How do you prevent reflexive collapse?

**Constraints:**
- Must be technically feasible with existing blockchain technology
- Cannot require trust in a single centralized entity
- Must explain economic incentives for all participants

### Model Answer / Expected Output

**Model Design: "TrustAnchor" - A Multi-Tier Stability Stablecoin**

---

**STABLECOIN NAME:** TrustAnchor (TAD)

**DESIGN PHILOSOPHY:** Combine the stability of fiat-backing with the decentralization of crypto-backing, using tiered collateral and dynamic stability fees.

---

**1. PRIMARY STABILITY MECHANISM:**

**Tiered Collateral Pool:**
| Tier | Composition | Purpose |
|------|-------------|---------|
| Tier 1 (60%) | Tokenized T-Bills + USDC | Hard floor - stable, external backing |
| Tier 2 (30%) | ETH + BTC | Growth potential + decentralized |
| Tier 3 (10%) | Protocol token (ANCHOR) | Absorbs volatility, captures upside |

**Arbitrage Mechanism:**
- If TAD < $1: Burn TAD, receive $1 from Tier 1 reserves (direct redemption)
- If TAD > $1: Mint TAD by depositing collateral (increases supply, reduces price)

**Key Innovation:** Tier 1 provides a HARD FLOOR - unlike Terra, the backing doesn't degrade with stablecoin stress. Tier 2 and 3 provide upside and decentralization.

---

**2. STRESS RESPONSE:**

| Price Level | Response | Mechanism |
|-------------|----------|-----------|
| $0.99 - $1.01 | Normal arbitrage | Standard mint/burn |
| $0.95 - $0.99 | Redemption priority | Tier 1 assets used first; Tier 3 token burned |
| $0.80 - $0.95 | Emergency mode | Redemption fees waived; protocol buys TAD on open market |
| Below $0.80 | Circuit breaker | Minting halted; Tier 2 liquidation begins; 1:1 redemption from remaining Tier 1 |

**Critical Design:** Circuit breaker prevents hyperinflation of protocol token (Terra's fatal flaw). Instead, protocol accepts partial redemption from Tier 2 liquidation rather than infinite token minting.

---

**3. COLLATERAL STRATEGY:**

**Why This Mix:**
| Tier | Rationale |
|------|-----------|
| Tier 1 (T-Bills + USDC) | External, stable, provides credible floor |
| Tier 2 (ETH + BTC) | Major crypto assets with deep liquidity; decentralized |
| Tier 3 (ANCHOR token) | Absorbs first losses; aligns protocol token holders with stability |

**Collateralization Ratio:** 130% total (60% + 30% + 10% at par, but Tier 2 volatile)

**Rebalancing:** Weekly rebalancing to maintain tier ratios; Tier 3 burns/mints to absorb volatility.

---

**4. SEIGNIORAGE DISTRIBUTION:**

| Recipient | Share | Mechanism |
|-----------|-------|-----------|
| Tier 1 (T-Bill yield) | 50% | Passed to TAD holders as savings rate |
| Protocol Treasury | 30% | Insurance fund + development |
| ANCHOR stakers | 20% | Compensation for absorbing downside risk |

**Key Economic Insight:** Unlike Terra (seigniorage to unsustainable yield), seigniorage here builds insurance buffer and compensates risk-takers proportionally.

---

**5. DEATH SPIRAL PREVENTION:**

| Prevention | How Implemented |
|------------|-----------------|
| External backing floor | Tier 1 provides redemption independent of protocol token |
| Non-circular collateral | T-Bills and ETH don't depend on TAD success |
| Loss absorption order | Tier 3 (protocol token) absorbs first, then Tier 2, finally Tier 1 |
| Circuit breaker | Halts minting at $0.80 to prevent hyperinflation |
| Gradual liquidation | Tier 2 sold over 72 hours to avoid market impact |

**The Key Difference from Terra:**
- Terra: UST backed by LUNA, LUNA value depends on UST demand (CIRCULAR)
- TrustAnchor: TAD backed by T-Bills and ETH, their value independent of TAD (EXTERNAL)

---

**EXPECTED WEAKNESSES TO ACKNOWLEDGE:**

1. Tier 1 reintroduces some centralization (tokenized T-Bills require trusted issuer)
2. 130% collateralization is capital inefficient
3. ANCHOR token still has reflexivity risk (though limited to 10% of backing)
4. Complex mechanism may have smart contract risk
5. Regulatory uncertainty about tokenized T-Bills

---

### Presentation Talking Points
- Every stability mechanism involves trade-offs - there's no perfect design
- The key insight is external vs circular backing - TrustAnchor's Tier 1 provides external backing
- Tiered collateral allows risk absorption in order (protocol token first, then crypto, finally stable assets)
- Circuit breakers prevent Terra-style hyperinflation of the protocol token
- Seigniorage should build reserves, not pay unsustainable yields
- Key economic insight: Stability mechanisms must break the reflexivity - backing must not depend on the stablecoin's success

---

## Exercise 6: Gresham's Law in Crypto Markets

**Category**: Comparative Analysis
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Worksheet, calculator optional

### Task

Apply Gresham's Law ("bad money drives out good") to cryptocurrency markets. Analyze which coins get spent versus hoarded, and what this reveals about their monetary properties.

**Background:** Gresham's Law states that when two currencies circulate at a fixed exchange rate, the overvalued ("bad") currency will be used for transactions while the undervalued ("good") currency will be hoarded.

**Cryptocurrencies to Analyze:**
1. Bitcoin (BTC)
2. Ethereum (ETH)
3. USDC (stablecoin)
4. Dogecoin (DOGE)

### Model Answer / Expected Output

**Part 1: Velocity as Proxy for Spending vs Hoarding**

| Crypto | Annual Volume / Market Cap | Velocity | Interpretation |
|--------|---------------------------|----------|----------------|
| Bitcoin | ~$2.9T / $800B | ~3.6 | **Hoarded** - Low velocity, HODL culture |
| Ethereum | ~$1.8T / $350B | ~5.1 | **Mixed** - Used in DeFi, but also held |
| USDC | ~$4.5T / $30B | ~150 | **Spent** - Very high turnover |
| Dogecoin | ~$200B / $12B | ~17 | **Spent** - High velocity, low hoarding |

**Part 2: Gresham's Law Analysis**

**Classical Gresham's Law Scenario:**
- Two currencies at FIXED exchange rate
- "Bad" (overvalued) currency spent
- "Good" (undervalued) currency hoarded

**Crypto Adaptation:**
- Cryptocurrencies have FLOATING exchange rates
- But perceived "store of value" quality matters
- People spend what they expect to depreciate, hoard what they expect to appreciate

**Application to Each Crypto:**

| Crypto | Perceived as... | Behavior | Gresham Classification |
|--------|-----------------|----------|------------------------|
| **Bitcoin** | "Digital gold", store of value, deflationary | Hoarded (HODL), not spent | **"Good money"** - hoarded |
| **Ethereum** | Utility + investment, mixed narrative | Used for gas, DeFi, but also held | **Mixed** |
| **USDC** | "Just dollars", stable, no appreciation | Spent freely, high velocity | **"Bad money"** - spent |
| **Dogecoin** | Meme, inflationary, no scarcity | Spent easily, tipping culture | **"Bad money"** - spent |

**Part 3: The Paradox**

Gresham's Law reveals a paradox for cryptocurrency adoption:

1. **Bitcoin's Problem:** By being perceived as "good money" (appreciating store of value), people hoard it. But money needs to circulate to function as medium of exchange. Bitcoin's success as store of value undermines its use as money.

2. **Stablecoin's Advantage:** By being perceived as "bad money" (no appreciation), stablecoins actually get used. USDC's V=150 vs Bitcoin's V=3.6 shows stablecoins function better as medium of exchange.

3. **The Inversion:** In crypto, "bad money" (stablecoins) is actually better money (for transactions), while "good money" (Bitcoin) is bad for transactions.

**Part 4: Evidence from On-Chain Data**

| Metric | Bitcoin | USDC |
|--------|---------|------|
| Daily active addresses | ~800K | ~200K |
| Daily transactions | ~300K | ~1.5M |
| Average transaction value | ~$50K | ~$3K |
| Median transaction value | ~$500 | ~$200 |
| Velocity | 3.6 | 150 |

**Interpretation:**
- Bitcoin: Fewer, larger transactions (settlement layer, investment transfers)
- USDC: More, smaller transactions (actual payments, DeFi activity)
- Bitcoin users treat it as gold (infrequent large moves)
- USDC users treat it as cash (frequent small payments)

**Part 5: Implications**

1. **For Bitcoin:** The HODL culture is rational (Gresham's Law in action) but prevents monetary function. Bitcoin will not become everyday money unless perception changes.

2. **For Stablecoins:** Their "boring" stability makes them useful as money. Being perceived as "bad money" (no appreciation) is actually good for monetary function.

3. **For Crypto Payments:** Gresham's Law predicts that crypto payments will be dominated by stablecoins, not appreciating assets. This is already happening.

4. **For Regulators:** Focus on stablecoins (they're actually used as money); Bitcoin is more like a commodity/investment.

### Presentation Talking Points
- Gresham's Law explains why Bitcoin isn't used for coffee purchases - it's too "good" (expected to appreciate)
- Stablecoins' stability makes them "bad money" in Gresham's terms - which is why they're actually used
- Velocity data empirically confirms Gresham's Law in crypto: USDC V=150 vs BTC V=3.6
- The Bitcoin Pizza story ($600M for two pizzas) is Gresham's Law in action - spending "good money" is painful
- Key economic insight: A cryptocurrency's success as store of value (Bitcoin) undermines its function as medium of exchange
- This explains the crypto ecosystem division: Bitcoin = gold, stablecoins = cash, ETH = utility

---

## Exercise 7: Seigniorage Calculator: Who Profits from Money?

**Category**: Python/Data
**Time**: 30 min work + 5 min presentation
**Group Size**: Individual or Pairs
**Materials Needed**: Laptop with Python (pandas, matplotlib), calculator

### Task

Calculate and visualize seigniorage across different money systems: the US Federal Reserve, Tether (USDT), and Bitcoin mining. Determine who captures the "profit from money creation" in each system.

**Given Data:**

| System | Key Figures |
|--------|-------------|
| **US Federal Reserve** | M2 money supply: $21 trillion; Annual growth: ~5%; Fed remits profits to Treasury |
| **Tether (USDT)** | Market cap: $95 billion; Reserve yield: ~5% (T-bills); Operating costs: ~$50 million/year |
| **Bitcoin Mining** | Block reward: 3.125 BTC/block; Blocks/day: 144; BTC price: $42,000; Mining cost: ~$30,000/BTC |

### Complete Code

```python
"""
Seigniorage Analysis Across Money Systems
L02 Exercise - Monetary Economics of Digital Currencies

Requirements: pip install pandas matplotlib numpy
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# SEIGNIORAGE CALCULATIONS
# =============================================================================

print("="*70)
print("SEIGNIORAGE ANALYSIS: Who Profits from Money Creation?")
print("="*70)

# -----------------------------------------------------------------------------
# 1. US FEDERAL RESERVE
# -----------------------------------------------------------------------------

print("\n--- US FEDERAL RESERVE ---")

# Seigniorage = revenue from money creation
# For Fed: M2 growth * velocity adjustment + interest on reserves

m2_supply = 21_000_000_000_000  # $21 trillion
m2_growth_rate = 0.05  # 5% annual growth
new_money_created = m2_supply * m2_growth_rate

# Fed earns interest on assets (Treasury securities) purchased with new money
fed_assets = 7_500_000_000_000  # $7.5 trillion balance sheet
avg_yield = 0.03  # ~3% average yield on Fed portfolio

fed_interest_income = fed_assets * avg_yield
fed_operating_costs = 5_000_000_000  # ~$5 billion operating costs
fed_remittance_to_treasury = fed_interest_income - fed_operating_costs

print(f"M2 Money Supply: ${m2_supply/1e12:.1f} trillion")
print(f"New Money Created (annual): ${new_money_created/1e12:.1f} trillion")
print(f"Fed Interest Income: ${fed_interest_income/1e9:.1f} billion")
print(f"Fed Operating Costs: ${fed_operating_costs/1e9:.1f} billion")
print(f"Fed Remittance to Treasury: ${fed_remittance_to_treasury/1e9:.1f} billion")
print(f"\nSeigniorage Beneficiary: US Treasury (public)")

# -----------------------------------------------------------------------------
# 2. TETHER (USDT)
# -----------------------------------------------------------------------------

print("\n--- TETHER (USDT) ---")

usdt_market_cap = 95_000_000_000  # $95 billion
reserve_yield = 0.05  # 5% yield on T-bill reserves
tether_gross_income = usdt_market_cap * reserve_yield
tether_operating_costs = 50_000_000  # $50 million
tether_net_profit = tether_gross_income - tether_operating_costs

# Users' opportunity cost
user_opportunity_cost = usdt_market_cap * reserve_yield  # Users could earn this themselves

print(f"USDT Market Cap: ${usdt_market_cap/1e9:.1f} billion")
print(f"Reserve Yield (T-bills): {reserve_yield*100:.1f}%")
print(f"Tether Gross Income: ${tether_gross_income/1e9:.1f} billion/year")
print(f"Tether Operating Costs: ${tether_operating_costs/1e6:.0f} million/year")
print(f"Tether Net Profit: ${tether_net_profit/1e9:.2f} billion/year")
print(f"User Opportunity Cost: ${user_opportunity_cost/1e9:.1f} billion/year")
print(f"\nSeigniorage Beneficiary: Tether Limited (private company)")

# -----------------------------------------------------------------------------
# 3. BITCOIN MINING
# -----------------------------------------------------------------------------

print("\n--- BITCOIN MINING ---")

block_reward = 3.125  # BTC per block (post-2024 halving)
blocks_per_day = 144
btc_price = 42_000
mining_cost_per_btc = 30_000

daily_btc_issued = block_reward * blocks_per_day
annual_btc_issued = daily_btc_issued * 365

gross_mining_revenue = annual_btc_issued * btc_price
total_mining_cost = annual_btc_issued * mining_cost_per_btc
net_mining_profit = gross_mining_revenue - total_mining_cost

# This is "dissipated seigniorage" - profit goes to miners but is spent on electricity/hardware
dissipation_rate = total_mining_cost / gross_mining_revenue

print(f"Block Reward: {block_reward} BTC")
print(f"Annual BTC Issued: {annual_btc_issued:,.0f} BTC")
print(f"Gross Mining Revenue: ${gross_mining_revenue/1e9:.2f} billion/year")
print(f"Total Mining Costs: ${total_mining_cost/1e9:.2f} billion/year")
print(f"Net Mining Profit: ${net_mining_profit/1e9:.2f} billion/year")
print(f"Dissipation Rate: {dissipation_rate*100:.0f}% (goes to electricity/hardware)")
print(f"\nSeigniorage Beneficiary: Miners (but mostly dissipated in costs)")

# =============================================================================
# COMPARISON SUMMARY
# =============================================================================

print("\n" + "="*70)
print("SEIGNIORAGE COMPARISON SUMMARY")
print("="*70)

comparison = pd.DataFrame({
    'System': ['US Federal Reserve', 'Tether (USDT)', 'Bitcoin Mining'],
    'Annual Seigniorage ($B)': [
        fed_remittance_to_treasury/1e9,
        tether_net_profit/1e9,
        net_mining_profit/1e9
    ],
    'Beneficiary': ['Public (Treasury)', 'Private (Tether Ltd)', 'Miners (dissipated)'],
    'Seigniorage per $1000 base': [
        (fed_remittance_to_treasury / fed_assets) * 1000,
        (tether_net_profit / usdt_market_cap) * 1000,
        (net_mining_profit / (21_000_000 * btc_price)) * 1000  # per $1000 of BTC market cap
    ]
})

print(comparison.to_string(index=False))

# =============================================================================
# VISUALIZATION
# =============================================================================

plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=100)

# Chart 1: Total Seigniorage Comparison
ax1 = axes[0]
systems = ['Fed\n(Public)', 'Tether\n(Private)', 'Bitcoin\n(Miners)']
seigniorage = [fed_remittance_to_treasury/1e9, tether_net_profit/1e9, net_mining_profit/1e9]
colors = ['#2E86AB', '#A23B72', '#F18F01']
bars = ax1.bar(systems, seigniorage, color=colors)
ax1.set_ylabel('Annual Seigniorage ($B)', fontsize=10)
ax1.set_title('Total Seigniorage by System', fontsize=12, fontweight='bold')
for bar, val in zip(bars, seigniorage):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'${val:.1f}B', ha='center', va='bottom', fontsize=9)

# Chart 2: Seigniorage Distribution Flow
ax2 = axes[1]
labels = ['Fed: Treasury', 'Tether: Shareholders', 'BTC: Miners→Electricity']
sizes = [fed_remittance_to_treasury/1e9, tether_net_profit/1e9, total_mining_cost/1e9]
ax2.pie(sizes, labels=labels, autopct='%1.0f%%', colors=colors, startangle=90)
ax2.set_title('Where Does Seigniorage Go?', fontsize=12, fontweight='bold')

# Chart 3: Seigniorage Efficiency (profit per $1000 base)
ax3 = axes[2]
efficiency = comparison['Seigniorage per $1000 base'].values
ax3.barh(systems, efficiency, color=colors)
ax3.set_xlabel('$ Seigniorage per $1000 Base', fontsize=10)
ax3.set_title('Seigniorage Efficiency', fontsize=12, fontweight='bold')
for i, val in enumerate(efficiency):
    ax3.text(val + 0.5, i, f'${val:.1f}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('seigniorage_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nChart saved as 'seigniorage_analysis.png'")

# =============================================================================
# ECONOMIC ANALYSIS
# =============================================================================

print("\n" + "="*70)
print("ECONOMIC ANALYSIS: Policy Implications")
print("="*70)

print("""
KEY FINDINGS:

1. FEDERAL RESERVE (PUBLIC SEIGNIORAGE):
   - Seigniorage flows to US Treasury (public benefit)
   - Funds ~$220B/year in government operations
   - This is the "privilege" of issuing reserve currency
   - Citizens benefit indirectly through lower taxes/more services

2. TETHER (PRIVATIZED SEIGNIORAGE):
   - $4.75B/year profit to private shareholders
   - Users provide $95B capital, earn 0%
   - Users bear all the risk (depeg, hack), capture none of yield
   - This is why regulators want stablecoins to share yield or be regulated

3. BITCOIN (DISSIPATED SEIGNIORAGE):
   - ~$4.9B/year in mining revenue, but ~$3.5B spent on electricity
   - Seigniorage is "burned" in proof-of-work
   - Only ~$1.4B net profit to miners (distributed globally)
   - Economically wasteful but provides decentralization

4. POLICY IMPLICATIONS:

   a) CBDC Argument: Why let Tether capture $4.75B that could fund public services?
      CBDCs return seigniorage to the public.

   b) Stablecoin Regulation: Should stablecoins be required to pass yield to users?
      Current model is extractive - users provide capital, issuers keep profits.

   c) Bitcoin's Design Trade-off: Dissipated seigniorage is the "cost of decentralization"
      No entity captures monetary rents, but energy is consumed.

   d) Fairness Question: Is it fair that holding USDT earns 0% while Tether earns 5%
      on those same dollars? This is hidden "tax" on stablecoin users.

5. QUANTITATIVE PERSPECTIVE:
   - If you hold $10,000 in USDT for one year, your opportunity cost is ~$500
   - Tether earns that $500 instead of you
   - This is the "seigniorage tax" on stablecoin users
""")
```

### Model Answer / Expected Output

**Expected Chart Description:**
- Three-panel visualization showing:
  - Bar chart: Fed ($220B) >> Tether ($4.75B) > Bitcoin ($1.4B net)
  - Pie chart: Distribution showing Fed to Treasury, Tether to shareholders, Bitcoin mostly to electricity
  - Efficiency chart: Tether most efficient per dollar of base ($50 per $1000), Fed lowest ($29 per $1000)

**Key Quantitative Findings:**

| System | Annual Seigniorage | Beneficiary | Efficiency |
|--------|-------------------|-------------|------------|
| Federal Reserve | ~$220 billion | US Treasury (public) | ~$29 per $1000 |
| Tether | ~$4.75 billion | Tether shareholders | ~$50 per $1000 |
| Bitcoin | ~$1.4 billion (net) | Miners (globally distributed) | Mostly dissipated |

**Economic Insight:**

The analysis reveals three fundamentally different approaches to monetary profit:

1. **Socialized seigniorage (Fed)**: Profits flow to public treasury, funding government services. This is the traditional model - the state captures monetary rents.

2. **Privatized seigniorage (Tether)**: A private company captures ~$4.75B/year by holding user deposits in yield-bearing assets while paying users 0%. Users bear counterparty risk, issuer captures all upside.

3. **Dissipated seigniorage (Bitcoin)**: Proof-of-work "burns" most of the value in electricity. No single entity captures monetary rents, but tremendous real resources consumed.

**Policy implication:** The rise of stablecoins represents a massive transfer of seigniorage from public to private hands. This is a key argument for CBDCs.

### Presentation Talking Points
- Seigniorage is the "profit from money creation" - someone always captures it
- Federal Reserve model: public captures seigniorage through Treasury remittances
- Tether model: private company captures ~$5B/year from user deposits (users get 0%)
- Bitcoin model: seigniorage is mostly "burned" in electricity (decentralization cost)
- Policy insight: Stablecoins have privatized seigniorage that historically belonged to the public
- CBDC motivation: Return seigniorage to the public sector
- Key economic insight: Every $10,000 held in USDT represents ~$500/year transferred from user to Tether

---

## Exercise 8: Currency Substitution Case Study

**Category**: Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Case handout (one of the options below)

### Task

Apply the currency substitution and dollarization framework from L02 to analyze a real-world case of cryptocurrency adoption in a high-inflation country.

**Case Options** (instructor assigns one per group):
- **Case A**: Argentina - Peso collapse and crypto adoption
- **Case B**: Venezuela - Hyperinflation and Bitcoin usage
- **Case C**: Turkey - Lira crisis and stablecoin surge
- **Case D**: Nigeria - Naira devaluation and crypto trading volume

### Model Answer / Expected Output

**CASE A: Argentina - Peso Collapse and Crypto Adoption**

---

**Background:**
- Inflation rate: ~140% (2023)
- Capital controls ("cepo") restrict USD access
- Parallel exchange rate: Official ~350 ARS/USD, Blue dollar ~1000 ARS/USD
- Crypto adoption: Top 15 globally by usage

---

**Part 1: Currency Substitution Framework**

| Concept | Application to Argentina |
|---------|--------------------------|
| **Traditional Dollarization** | Argentines have historically held USD to protect savings. Government restricts USD purchases to $200/month (cepo). This created unsatisfied demand for stable currency. |
| **"Crypto-ization"** | When USD access restricted, Argentines turned to USDT/USDC/DAI. Stablecoins became "digital dollars" accessible without capital controls. P2P trading volume surged. |
| **Gresham's Law** | Argentines receive salary in pesos (bad money), immediately convert to crypto (good money). Pesos are spent, crypto is saved. Classic Gresham's Law in action. |
| **Velocity** | Peso velocity extremely high (spent immediately). Stablecoin velocity low (saved). Money demand has shifted from peso to crypto. |
| **Seigniorage Loss** | Argentine central bank loses seigniorage as citizens hold USDT instead of pesos. Tether captures what would have been Argentine inflation tax revenue. |

---

**Part 2: Economic Analysis**

**Why Crypto Instead of Physical USD:**

| Factor | Physical USD | Stablecoins |
|--------|-------------|-------------|
| Acquisition | Requires visiting "cuevas" (illegal exchange houses), personal risk | Buy online via P2P, no physical presence |
| Storage | Risk of theft, fire, confiscation | Stored in phone/wallet, easily hidden |
| Transaction | Difficult for e-commerce, large amounts awkward | Instant, any amount, works for online payments |
| Capital controls | Enforceable at borders | Difficult to detect/enforce |

**Result:** Stablecoins provide USD-equivalent stability with crypto's accessibility.

---

**Part 3: Consequences**

| Stakeholder | Impact |
|-------------|--------|
| **Argentine Citizens** | Benefit: Protection from 140% inflation. Cost: Counterparty risk (stablecoin), tax evasion concerns |
| **Central Bank** | Lost: Seigniorage, monetary policy effectiveness. Gained: Nothing |
| **Government** | Lost: Tax revenue (crypto hard to track), monetary sovereignty. Gained: Social safety valve (prevents worse crisis) |
| **Stablecoin Issuers** | Gained: ~$1-2B of Argentine savings earning yield they capture |
| **Crypto Exchanges** | Gained: Trading volume, fees, market share |

---

**Part 4: Monetary Economics Framework**

**Using MV = PY for Argentina:**

| Variable | Peso Economy | Crypto Economy |
|----------|--------------|----------------|
| M | Expanding (printing to fund deficit) | Limited (users control) |
| V | Extremely high (hot potato) | Low (savings vehicle) |
| P | Rising rapidly (inflation) | Stable (pegged to USD) |
| Y | Struggling (economic crisis) | N/A |

**Interpretation:** The peso economy has become a "hot potato" - people receive pesos and immediately spend or convert. The crypto economy has become the "savings layer" - a parallel monetary system for value preservation.

---

**Part 5: Policy Options**

| Option | Pros | Cons |
|--------|------|------|
| **Legalize and Tax Crypto** | Capture some tax revenue, bring activity onshore | Legitimizes capital flight, technical challenges |
| **Crack Down on Crypto** | Maintain capital controls | Drives activity underground, hard to enforce |
| **Full Dollarization** | Eliminates inflation, restores savings | Loses monetary sovereignty, seigniorage |
| **CBDC (Digital Peso)** | Programmable controls, maintains sovereignty | Doesn't solve inflation, trust problem |
| **Fix Fundamentals** | Sustainable solution | Politically difficult, takes years |

**Argentina's Dilemma:** Cannot both: (1) maintain capital controls, (2) print money for fiscal deficit, and (3) prevent crypto adoption. Citizens will find ways to protect savings.

---

**Key Insight:**

Argentina demonstrates that currency substitution in the digital age is unstoppable. When governments create conditions for hyperinflation AND restrict access to stable alternatives, citizens will adopt crypto. This is dollarization 2.0 - the same economic phenomenon (flight from unstable local currency) expressed through new technology.

### Presentation Talking Points
- Argentina is a real-time case study of currency substitution via crypto
- The same forces that caused traditional dollarization (Venezuela, Ecuador, Zimbabwe) now drive crypto adoption
- Stablecoins are "digital dollarization" - same function, new technology
- Gresham's Law is observable: pesos spent immediately, stablecoins hoarded
- Key economic insight: Capital controls + inflation = crypto adoption. You cannot have both inflationary policy and prevent currency substitution.
- Seigniorage is being transferred from Argentine central bank to Tether - a geopolitical shift
- Policy implication: Countries must choose between sound money OR crypto adoption will substitute

---

**PLAN_READY: .omc/plans/l02-in-class-exercises.md**