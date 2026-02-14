# L08 In-Class Exercises: Synthesis and Future Directions

## Plan Metadata
- **Created**: 2026-02-04
- **Lesson**: L08 - Synthesis and Future Directions
- **Target Audience**: BSc students (completing the Digital Finance Economics course)
- **Time Allocation**: 30 minutes work + 5 minutes presentation per exercise
- **Instructor Choice**: Select 2-3 exercises per session based on class size and learning goals

---

## Exercise Overview

| # | Title | Category | Group Size | Materials |
|---|-------|----------|------------|-----------|
| 1 | Crypto Contagion Network Mapper | Python/Data | Individual or Pairs | Laptop with Python |
| 2 | Four Lenses Stablecoin Regulation Analysis | Synthesis/Framework | Groups of 3-4 | Worksheet |
| 3 | 2022 Crypto Contagion Chain Investigation | Case Study | Groups of 3-4 | Internet Access |
| 4 | "DeFi Will Replace TradFi" Great Debate | Debate | Two Teams (4-6 each) | None |
| 5 | Design a TradFi-DeFi Hybrid Institution | Creative/Design | Groups of 3-4 | Whiteboard/Paper |
| 6 | Digital Finance Trilemma Mapping | Framework Application | Groups of 3-4 | Worksheet + Triangle Template |
| 7 | Digital Finance 2030: Predictive Analysis | Future Prediction | Groups of 3-4 | Discussion Framework |
| 8 | The Complete Case: All Four Lenses Integration | Final Integration | Groups of 4-5 | Comprehensive Case Materials |

---

## Exercise 1: Crypto Contagion Network Mapper

**Category**: Python/Data
**Time**: 30 min work + 5 min presentation
**Group Size**: Individual or Pairs
**Materials Needed**: Laptop with Python (networkx, matplotlib, pandas), internet access

### Task

Build a network visualization of the 2022 crypto contagion, showing how failures spread from Terra/LUNA through the ecosystem. Calculate network centrality metrics to identify systemically important nodes and discuss implications for systemic risk monitoring in digital finance.

**As covered in L02 (Monetary Economics)**: Private money creation without proper backing creates run risk.
**Building on L04 concepts (Payment Systems)**: Contagion spreads through interconnected payment and settlement networks.

### Complete Code

```python
"""
Crypto Contagion Network Analysis: 2022 Crisis Visualization
L08 Exercise - Economics of Digital Finance

# Data as of February 2025

Requirements: pip install networkx matplotlib pandas numpy
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =============================================================================
# NETWORK DATA: 2022 Crypto Contagion
# Events occurred May-November 2022; facts documented as of February 2025
# =============================================================================

# Define entities and their types
entities = {
    # Collapsed entities
    'Terra/LUNA': {'type': 'protocol', 'status': 'collapsed', 'loss_bn': 40},
    'Three Arrows Capital': {'type': 'hedge_fund', 'status': 'collapsed', 'loss_bn': 10},
    'Celsius': {'type': 'lender', 'status': 'collapsed', 'loss_bn': 4.7},
    'Voyager': {'type': 'lender', 'status': 'collapsed', 'loss_bn': 1.3},
    'BlockFi': {'type': 'lender', 'status': 'collapsed', 'loss_bn': 1.0},
    'FTX': {'type': 'exchange', 'status': 'collapsed', 'loss_bn': 8},
    'Alameda Research': {'type': 'hedge_fund', 'status': 'collapsed', 'loss_bn': 8},
    'Genesis': {'type': 'lender', 'status': 'collapsed', 'loss_bn': 3},

    # Stressed but survived
    'Tether (USDT)': {'type': 'stablecoin', 'status': 'stressed', 'loss_bn': 0},
    'Crypto.com': {'type': 'exchange', 'status': 'stressed', 'loss_bn': 0.5},
    'Gemini': {'type': 'exchange', 'status': 'stressed', 'loss_bn': 0.9},

    # Healthy majors (for context)
    'Coinbase': {'type': 'exchange', 'status': 'healthy', 'loss_bn': 0},
    'Binance': {'type': 'exchange', 'status': 'healthy', 'loss_bn': 0},
    'Circle (USDC)': {'type': 'stablecoin', 'status': 'healthy', 'loss_bn': 0},
}

# Define contagion links (source, target, exposure_type)
# Edge represents: source failure affected target
contagion_links = [
    # Terra collapse cascade
    ('Terra/LUNA', 'Three Arrows Capital', 'direct_exposure'),
    ('Terra/LUNA', 'Celsius', 'direct_exposure'),
    ('Terra/LUNA', 'Voyager', 'indirect'),
    ('Terra/LUNA', 'Tether (USDT)', 'redemption_pressure'),

    # 3AC cascade
    ('Three Arrows Capital', 'Voyager', 'loan_default'),
    ('Three Arrows Capital', 'BlockFi', 'loan_default'),
    ('Three Arrows Capital', 'Genesis', 'loan_default'),
    ('Three Arrows Capital', 'Celsius', 'counterparty'),

    # Celsius cascade
    ('Celsius', 'Voyager', 'liquidity_contagion'),
    ('Celsius', 'Gemini', 'counterparty'),

    # FTX/Alameda cascade (separate but connected)
    ('FTX', 'Alameda Research', 'affiliated'),
    ('FTX', 'BlockFi', 'rescue_failed'),
    ('FTX', 'Genesis', 'counterparty'),
    ('FTX', 'Crypto.com', 'confidence'),
    ('Alameda Research', 'Genesis', 'loan_default'),

    # Broader market effects
    ('Three Arrows Capital', 'Binance', 'market_impact'),
    ('FTX', 'Binance', 'market_impact'),
    ('Terra/LUNA', 'Circle (USDC)', 'confidence'),
]

# =============================================================================
# BUILD NETWORK
# =============================================================================

G = nx.DiGraph()

# Add nodes with attributes
for entity, attrs in entities.items():
    G.add_node(entity, **attrs)

# Add edges
for source, target, exposure_type in contagion_links:
    G.add_edge(source, target, exposure_type=exposure_type)

# =============================================================================
# CALCULATE CENTRALITY METRICS
# =============================================================================

# In-degree: How many entities were affected by this node
in_degree = dict(G.in_degree())

# Out-degree: How many entities affected this node
out_degree = dict(G.out_degree())

# Betweenness centrality: How often a node lies on shortest paths (systemic importance)
betweenness = nx.betweenness_centrality(G)

# PageRank: Importance based on who links to you (influence measure)
pagerank = nx.pagerank(G)

# =============================================================================
# SUMMARY STATISTICS
# =============================================================================

print("=" * 70)
print("SYSTEMIC RISK ANALYSIS: 2022 Crypto Contagion Network")
print("=" * 70)

# Create metrics dataframe
metrics_df = pd.DataFrame({
    'Entity': list(entities.keys()),
    'Type': [entities[e]['type'] for e in entities.keys()],
    'Status': [entities[e]['status'] for e in entities.keys()],
    'Loss ($B)': [entities[e]['loss_bn'] for e in entities.keys()],
    'Out-Degree': [out_degree.get(e, 0) for e in entities.keys()],
    'In-Degree': [in_degree.get(e, 0) for e in entities.keys()],
    'Betweenness': [round(betweenness.get(e, 0), 3) for e in entities.keys()],
    'PageRank': [round(pagerank.get(e, 0), 3) for e in entities.keys()],
})

# Sort by betweenness (systemic importance)
metrics_df = metrics_df.sort_values('Betweenness', ascending=False)

print("\nSYSTEMIC IMPORTANCE RANKING (by Betweenness Centrality):")
print("-" * 70)
print(metrics_df.to_string(index=False))

# Identify most systemically important nodes
print("\n" + "=" * 70)
print("KEY FINDINGS:")
print("=" * 70)

top_systemic = metrics_df.nlargest(3, 'Betweenness')
print("\nMost Systemically Important Nodes (highest betweenness):")
for _, row in top_systemic.iterrows():
    print(f"  - {row['Entity']}: Betweenness = {row['Betweenness']:.3f}, "
          f"connects {row['Out-Degree']} downstream entities")

top_spreaders = metrics_df.nlargest(3, 'Out-Degree')
print("\nBiggest Contagion Spreaders (highest out-degree):")
for _, row in top_spreaders.iterrows():
    print(f"  - {row['Entity']}: Directly affected {row['Out-Degree']} entities")

# =============================================================================
# VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# ----- LEFT PANEL: Network Visualization -----
ax1 = axes[0]

# Layout
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

# Node colors by status
color_map = {'collapsed': '#D62728', 'stressed': '#FF7F0E', 'healthy': '#2CA02C'}
node_colors = [color_map[entities[n]['status']] for n in G.nodes()]

# Node sizes by loss magnitude (with minimum size)
node_sizes = [max(300, entities[n]['loss_bn'] * 100 + 200) for n in G.nodes()]

# Draw edges with different styles by type
edge_styles = {
    'direct_exposure': {'style': 'solid', 'color': 'red', 'alpha': 0.8},
    'loan_default': {'style': 'solid', 'color': 'darkred', 'alpha': 0.7},
    'counterparty': {'style': 'dashed', 'color': 'orange', 'alpha': 0.6},
    'liquidity_contagion': {'style': 'dotted', 'color': 'purple', 'alpha': 0.6},
    'confidence': {'style': 'dotted', 'color': 'gray', 'alpha': 0.4},
    'market_impact': {'style': 'dotted', 'color': 'blue', 'alpha': 0.3},
    'affiliated': {'style': 'solid', 'color': 'black', 'alpha': 0.9},
    'redemption_pressure': {'style': 'dashed', 'color': 'purple', 'alpha': 0.5},
    'rescue_failed': {'style': 'dashed', 'color': 'brown', 'alpha': 0.6},
    'indirect': {'style': 'dotted', 'color': 'gray', 'alpha': 0.4},
}

for (u, v, data) in G.edges(data=True):
    exp_type = data.get('exposure_type', 'indirect')
    style = edge_styles.get(exp_type, {'style': 'solid', 'color': 'gray', 'alpha': 0.5})
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], ax=ax1,
                          style=style['style'], edge_color=style['color'],
                          alpha=style['alpha'], arrows=True,
                          arrowsize=15, width=1.5,
                          connectionstyle='arc3,rad=0.1')

# Draw nodes
nx.draw_networkx_nodes(G, pos, ax=ax1, node_color=node_colors,
                       node_size=node_sizes, alpha=0.8, edgecolors='black', linewidths=2)

# Labels with smaller font for readability
labels = {n: n.replace(' ', '\n') if len(n) > 10 else n for n in G.nodes()}
nx.draw_networkx_labels(G, pos, labels, ax=ax1, font_size=7, font_weight='bold')

ax1.set_title('2022 Crypto Contagion Network\nNode size = Loss magnitude, Color = Status',
             fontsize=12, fontweight='bold')
ax1.axis('off')

# Legend for status
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#D62728', label='Collapsed'),
    Patch(facecolor='#FF7F0E', label='Stressed'),
    Patch(facecolor='#2CA02C', label='Healthy'),
]
ax1.legend(handles=legend_elements, loc='upper left', fontsize=9)

# ----- RIGHT PANEL: Centrality Bar Chart -----
ax2 = axes[1]

# Top 8 by betweenness
top_8 = metrics_df.nlargest(8, 'Betweenness')

y_pos = np.arange(len(top_8))
colors = [color_map[s] for s in top_8['Status']]

bars = ax2.barh(y_pos, top_8['Betweenness'], color=colors, alpha=0.8, edgecolor='black')
ax2.set_yticks(y_pos)
ax2.set_yticklabels(top_8['Entity'], fontsize=10)
ax2.invert_yaxis()
ax2.set_xlabel('Betweenness Centrality (systemic importance)', fontsize=11)
ax2.set_title('Systemic Importance Ranking\n(Betweenness Centrality)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='x')

# Annotate top bar
ax2.annotate('Most systemically\nimportant node',
            xy=(top_8['Betweenness'].iloc[0], 0), xytext=(0.15, 1.5),
            fontsize=9, fontweight='bold', color='darkred',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5))

plt.suptitle('Crypto Systemic Risk: 2022 Contagion Network Analysis',
            fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('crypto_contagion_network.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nChart saved as 'crypto_contagion_network.png'")

# =============================================================================
# ECONOMIC CONCLUSIONS
# =============================================================================

print("\n" + "=" * 70)
print("ECONOMIC ANALYSIS: Systemic Risk Implications")
print("=" * 70)

print("""
KEY ECONOMIC INSIGHTS:

1. NETWORK TOPOLOGY AND CONTAGION:
   - Three Arrows Capital had highest betweenness centrality
   - This means 3AC was the critical "bridge" in the contagion chain
   - Monitoring centrality metrics could have flagged systemic importance

2. CONTAGION CHANNELS:
   - Direct exposure (loans, deposits): Fastest, most severe
   - Counterparty risk: Secondary cascade effects
   - Confidence/market impact: Slower but broader reach

3. POLICY IMPLICATIONS:
   - Network-based systemic risk monitoring needed
   - Centrality thresholds could trigger enhanced scrutiny
   - Interconnection limits (like bank large exposure rules)

4. TRADFI PARALLELS:
   - Similar to 2008 Lehman Brothers cascade
   - But FASTER: 24/7 markets, instant liquidations
   - Allen & Gale (2000) contagion model applies

5. WHAT REGULATORS MISSED:
   - 3AC was unregulated hedge fund (no reporting)
   - No consolidated view of cross-platform exposures
   - Network topology was invisible until collapse
""")
```

### Model Answer / Expected Output

**Expected Chart Description:**
- Left panel: Network graph with Terra/LUNA and Three Arrows Capital as central nodes, connected to downstream failures (Celsius, Voyager, BlockFi, FTX cascade)
- Node sizes reflect loss magnitude ($40B for Terra, $10B for 3AC, etc.)
- Red nodes = collapsed, Orange = stressed, Green = healthy
- Arrows show direction of contagion flow
- Right panel: Horizontal bar chart ranking entities by betweenness centrality

**Key Finding (Model Answer):**

Three Arrows Capital (3AC) had the **highest systemic importance** despite not being the initial trigger:

1. **Betweenness centrality** measures how often a node lies on the shortest path between other nodes - 3AC connected Terra's collapse to the broader crypto lending ecosystem

2. **Contagion amplification**: 3AC borrowed from multiple lenders (Voyager, BlockFi, Genesis) and invested in Terra - when Terra collapsed, 3AC failed, creating a cascade to all its creditors simultaneously

3. **Policy implication**: Network centrality metrics could serve as an early warning system for systemically important crypto institutions (like G-SIBs in banking)

4. **Speed difference**: Unlike 2008 (which took weeks), crypto contagion occurred within days due to:
   - 24/7 markets
   - Instant smart contract liquidations
   - Social media panic acceleration
   - No circuit breakers

### Presentation Talking Points
- Network topology matters for systemic risk - highly connected nodes are systemically important even if not largest by assets
- Betweenness centrality is more important than size - 3AC was smaller than FTX but more critical for contagion transmission
- Crypto contagion is FASTER than TradFi contagion - Allen & Gale models need updating for instant settlement
- Policy implication: regulators should monitor network metrics, not just individual entity health
- Key economic insight: The entity that triggers a crisis (Terra) may not be the most systemically important node (3AC) - network position matters

---

## Exercise 2: Four Lenses Stablecoin Regulation Analysis

**Category**: Synthesis/Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Printed worksheet, course notes on four lenses

### Task

The EU has just passed MiCA (Markets in Crypto-Assets Regulation). Your group is a policy advisory team that must analyze the stablecoin provisions using ALL FOUR economic lenses from the course. For each lens, identify: (1) the key economic concern addressed, (2) the specific MiCA provision that addresses it, and (3) remaining gaps or unintended consequences.

**Cross-reference**: Apply the four lenses framework from L01 (Introduction) systematically.
**As covered in L03**: CBDCs and stablecoin competition presents monetary sovereignty challenges.
**Building on L07**: Regulatory economics requires balancing innovation with consumer protection.

**MiCA Stablecoin Provisions to Analyze:**
1. Reserve requirement: 1:1 backing with high-quality liquid assets
2. Redemption right: Holders can redeem at par at any time
3. Issuer authorization: Must be licensed credit institution or e-money institution
4. Market cap limits: Significant stablecoins face additional requirements above EUR 5B
5. Transaction volume limits: Daily transaction limits if volume exceeds thresholds

### Model Answer / Expected Output

**COMPLETED FOUR LENSES ANALYSIS:**

---

**LENS 1: MONETARY ECONOMICS**

| Concern | MiCA Provision | Gap/Consequence |
|---------|----------------|-----------------|
| **Private money creation** - Stablecoins create quasi-money outside central bank control | Reserve requirement (1:1 HQLA backing) ensures stablecoins are "narrow banks" not money creators | Gap: Doesn't address monetary policy transmission if stablecoins substitute for bank deposits |
| **Seigniorage capture** - Private issuers capture float income that would otherwise go to public | Issuer authorization requires disclosure of reserve management and income | Gap: No requirement to share seigniorage with public |
| **Currency substitution** - Euro area monetary sovereignty at risk if foreign stablecoins dominate | Transaction volume limits and significant stablecoin designation | Consequence: May push activity to non-EU stablecoins (regulatory arbitrage) |
| **Bank disintermediation** - Deposits may flow from banks to stablecoins, reducing bank lending | Implicit through reserve requirements (stablecoins can't create credit) | Gap: Doesn't address liquidity impact on banking system if deposits migrate |

**Monetary Economics Verdict**: MiCA addresses money creation risk well (narrow banking model) but is weaker on monetary policy transmission and seigniorage capture. The volume limits may be unenforceable in practice.

---

**LENS 2: PLATFORM ECONOMICS**

| Concern | MiCA Provision | Gap/Consequence |
|---------|----------------|-----------------|
| **Network effects / winner-take-all** - Dominant stablecoins may abuse market power | Significant stablecoin designation (>EUR 5B) triggers additional oversight | Gap: Thresholds may be too high - market power emerges earlier |
| **Two-sided market dynamics** - Need both holders and merchants for adoption | Redemption right ensures holders aren't locked in | Consequence: Redemption right may reduce issuer incentive to build merchant network |
| **Interoperability / lock-in** - Proprietary ecosystems may create switching costs | Not directly addressed | Gap: No interoperability requirements between stablecoins |
| **Multi-homing** - Users holding multiple stablecoins for different purposes | Facilitated by standardized authorization requirements | Positive: Common standards reduce friction |

**Platform Economics Verdict**: MiCA focuses more on consumer protection than competition policy. Network effects and market power concerns are addressed only at very large scale. Missing: interoperability mandates.

---

**LENS 3: MARKET MICROSTRUCTURE**

| Concern | MiCA Provision | Gap/Consequence |
|---------|----------------|-----------------|
| **Peg stability / price discovery** - Stablecoins should trade at $1 | Redemption at par creates arbitrage mechanism to maintain peg | Gap: Doesn't address intraday deviations or exchange pricing |
| **Liquidity provision** - Issuers must be able to meet redemptions | HQLA reserve requirement ensures liquidity | Consequence: May concentrate reserves in same assets (systemic risk) |
| **Run dynamics** - Mass redemptions can break the peg | 1:1 reserves eliminate fractional reserve run risk | Gap: Doesn't address secondary market liquidity spirals |
| **Arbitrage efficiency** - Markets need frictionless arbitrage to maintain peg | Redemption right enables arbitrage | Gap: Doesn't specify redemption speed (instant? 1 day?) |

**Market Microstructure Verdict**: Strong on primary market (issuer-holder) but weaker on secondary market dynamics. No provisions for exchange-level circuit breakers or liquidity stress testing.

---

**LENS 4: REGULATORY ECONOMICS**

| Concern | MiCA Provision | Gap/Consequence |
|---------|----------------|-----------------|
| **Consumer protection** - Information asymmetry, fraud risk | Authorization, disclosure, redemption rights | Gap: Doesn't address DeFi wrappers of stablecoins |
| **Systemic risk** - Stablecoin failure could cascade | Significant stablecoin designation, enhanced supervision | Gap: Cross-border coordination with non-EU stablecoins (USDT) |
| **Regulatory arbitrage** - Activity moves to lenient jurisdictions | Comprehensive EU-wide framework reduces intra-EU arbitrage | Consequence: May push innovation to non-EU jurisdictions (UK, Singapore) |
| **Proportionality** - Regulation should match risk | Tiered approach (small vs. significant stablecoins) | Gap: Small stablecoin threshold may burden innovation |
| **Enforcement** - Can rules actually be enforced? | National competent authority supervision | Gap: Decentralized stablecoins (DAI) don't fit issuer model |

**Regulatory Economics Verdict**: MiCA is a sophisticated regulatory response with appropriate tiering. Key gaps: (1) decentralized stablecoins, (2) cross-border enforcement, (3) DeFi integration. The fundamental question: can territorial regulation govern borderless assets?

---

**SYNTHESIS CONCLUSION:**

| Lens | Strength | Weakness |
|------|----------|----------|
| Monetary | Narrow banking model prevents money creation | Ignores monetary policy transmission effects |
| Platform | Consumer protection via redemption rights | Weak on competition/interoperability |
| Microstructure | Strong on primary market stability | Ignores secondary market/exchange dynamics |
| Regulatory | Proportionate, tiered approach | Enforcement against decentralized systems unclear |

**Key Economic Insight**: MiCA is designed for **centralized, fiat-backed stablecoins** (USDC model). It struggles with:
1. **Algorithmic stablecoins** (Terra model) - effectively banned but not explicitly
2. **Decentralized stablecoins** (DAI model) - no identifiable issuer
3. **Cross-border stablecoins** (USDT) - limited extraterritorial reach

### Presentation Talking Points
- Each lens reveals different aspects of stablecoin regulation - no single lens is sufficient
- MiCA is strongest from monetary economics perspective (prevents private money creation)
- MiCA is weakest from platform economics perspective (ignores network effects until very large scale)
- Key tension: territorial regulation vs. borderless technology
- Economic insight: Regulation follows the "centralized issuer" model from TradFi - this doesn't map well to decentralized protocols
- Prediction: MiCA will be effective for USDC/EURC, less effective for USDT (non-EU), and inapplicable to DAI

---

## Exercise 3: 2022 Crypto Contagion Chain Investigation

**Category**: Case Study
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Internet access for research

### Task

Reconstruct the complete contagion chain of the 2022 crypto crisis. For each stage, identify: (1) the triggering event, (2) the transmission channel, (3) the economic mechanism at work, and (4) why existing safeguards failed.

**The Chain to Trace (events of 2022, documented as of February 2025):**
Terra/LUNA (May 2022) --> Three Arrows Capital (June 2022) --> Celsius/Voyager (June-July 2022) --> FTX/Alameda (November 2022)

**Cross-reference**:
- **L02**: Bank run dynamics and lender of last resort concepts
- **L04**: Payment system interconnections amplify contagion
- **L06**: Market microstructure, liquidity spirals, and price impact
- **L07**: Regulatory gaps and systemic risk monitoring

### Model Answer / Expected Output

**STAGE 1: TERRA/LUNA COLLAPSE (May 7-13, 2022)**
*As covered in L02: Algorithmic stablecoins represent unbacked private money - inherently unstable.*

| Element | Analysis |
|---------|----------|
| **Triggering Event** | Large UST sell orders ($285M) triggered by Anchor yield reduction announcement; UST depegged to $0.98 |
| **Transmission Channel** | Algorithmic peg mechanism: UST redemption for $1 of LUNA forced massive LUNA minting; LUNA price crashed; more UST holders redeemed; death spiral |
| **Economic Mechanism** | **Reflexive death spiral**: UST peg backed by LUNA, but LUNA value depended on UST confidence. When confidence broke, both collapsed simultaneously. This is a bank run without deposits - pure expectations failure. |
| **Why Safeguards Failed** | (1) No actual reserves - "backing" was circular; (2) Anchor's 20% yield was unsustainable (subsidized by Terraform Labs); (3) Bitcoin reserve ($3.5B) was insufficient for $18B market cap; (4) No lender of last resort |
| **Total Loss** | ~$40 billion market cap destroyed in 5 days |

**Economic Insight**: Terra demonstrated why monetary economists distrust unbacked private money. The "algorithmic" stabilization was just a fancy bank run waiting to happen. Gresham's Law applied: when confidence dropped, everyone fled simultaneously.

---

**STAGE 2: THREE ARROWS CAPITAL COLLAPSE (June 2022)**
*Building on L06 concepts: Leverage and counterparty risk amplify market shocks.*

| Element | Analysis |
|---------|----------|
| **Triggering Event** | 3AC had massive LUNA/UST positions (reportedly $600M); also held stETH (Lido staked ETH) which traded at discount |
| **Transmission Channel** | Failed margin calls from lenders (Voyager, BlockFi, Genesis); 3AC couldn't post collateral; defaulted on $3.5B in loans |
| **Economic Mechanism** | **Leveraged counterparty cascade**: 3AC borrowed from multiple lenders to make concentrated bets. When bets failed, couldn't repay ANY lender - the leverage amplified losses beyond capital. Classic hedge fund failure pattern. |
| **Why Safeguards Failed** | (1) 3AC was unregulated hedge fund in Singapore/BVI - no capital requirements; (2) Lenders didn't know 3AC's total exposure across all counterparties; (3) No consolidated supervision of crypto hedge funds; (4) Collateral (GBTC, stETH) also declined |
| **Total Loss** | ~$10 billion in defaulted obligations |

**Economic Insight**: 3AC was the Lehman Brothers of crypto - a highly connected node whose failure cascaded to multiple counterparties simultaneously. The lack of centralized clearing or exposure reporting meant no one knew the systemic risk.

---

**STAGE 3: CELSIUS/VOYAGER COLLAPSE (June-July 2022)**
*As covered in L02: Diamond-Dybvig bank run model applies to crypto lenders.*

| Element | Analysis |
|---------|----------|
| **Triggering Event** | Both had lent heavily to 3AC; when 3AC defaulted, they faced massive write-offs and couldn't meet customer redemptions |
| **Transmission Channel** | Liquidity mismatch: borrowed short (customer deposits, redeemable anytime) and lent long (to hedge funds, in illiquid positions like stETH) |
| **Economic Mechanism** | **Classic bank run (Diamond-Dybvig)**: Celsius/Voyager were performing maturity transformation without FDIC insurance or lender of last resort. When doubts arose about solvency, rational depositors rushed to withdraw first - self-fulfilling prophecy. |
| **Why Safeguards Failed** | (1) Not regulated as banks despite performing bank-like functions; (2) No deposit insurance; (3) No reserve requirements; (4) Terms of service allowed freezing withdrawals (but users didn't read them); (5) Celsius had lent customer funds to DeFi protocols and 3AC |
| **Total Loss** | Celsius: $4.7B in customer funds frozen; Voyager: $1.3B |

**Economic Insight**: Celsius/Voyager proved that crypto "lending platforms" are banks without the regulatory safety net. Diamond-Dybvig (1983) model perfectly predicted the run dynamic - the innovation was technology, not economics.

---

**STAGE 4: FTX/ALAMEDA COLLAPSE (November 2022)**
*Building on L07 concepts: Regulatory gaps enable fraud and systemic risk concentration.*

| Element | Analysis |
|---------|----------|
| **Triggering Event** | CoinDesk article (Nov 2) revealed Alameda's balance sheet was heavily dependent on FTT (FTX's token); Binance announced selling FTT holdings; run on FTX began |
| **Transmission Channel** | Customer deposits ($8B) had been secretly lent to Alameda; when customers withdrew, FTX had no funds; FTT price collapsed, making Alameda insolvent |
| **Economic Mechanism** | **Fraud + confidence collapse**: FTX used customer deposits as Alameda's funding source (illegal). FTT as collateral was circular - FTX issued FTT, Alameda borrowed against it. When confidence broke, the entire structure collapsed. **Ponzi dynamics**: new customer deposits funded Alameda's trading losses. |
| **Why Safeguards Failed** | (1) FTX was regulated in Bahamas with minimal oversight; (2) No segregation of customer funds (fundamental broker requirement); (3) FTT collateral was worthless when FTX failed; (4) Auditor (Armanino) didn't catch fund misappropriation; (5) Venture investors did no due diligence |
| **Total Loss** | ~$8 billion in customer funds; ~$32 billion in FTX/Alameda equity value |

**Economic Insight**: FTX was fundamentally a fraud disguised as a systemic event. However, the AFTERMATH created genuine contagion - Genesis exposure to Alameda led to Gemini Earn shutdown and DCG crisis. The fraud wouldn't have been possible without regulatory gaps.

---

**SYNTHESIS: THE COMPLETE CONTAGION CHAIN**

```
Terra/LUNA                  Three Arrows Capital           Celsius/Voyager              FTX/Alameda
(Monetary failure)    -->   (Counterparty cascade)    --> (Bank run)              -->  (Fraud + cascade)
     |                            |                            |                           |
     v                            v                            v                           v
Algorithmic peg             Concentrated leverage       Maturity mismatch           Commingled funds
breaks under                amplified losses across     + no insurance              + circular collateral
selling pressure            multiple lenders            caused classic run          caused total collapse
     |                            |                            |                           |
     v                            v                            v                           v
$40B lost                   $10B in defaults            $6B frozen                  $8B+ lost
(5 days)                    (2 weeks)                   (1 month)                   (1 week)
```

**Common Economic Themes:**

1. **Leverage amplification**: Each node was highly leveraged, turning asset declines into insolvency
2. **Liquidity mismatch**: Borrowed short, lent long, with no lender of last resort
3. **Interconnection opacity**: No one knew total exposures across the system
4. **Speed**: Digital settlement meant collapses happened in days/weeks, not months
5. **Regulatory gaps**: Each entity exploited different regulatory holes

### Presentation Talking Points
- The 2022 crisis validated classic financial economics: bank runs, leverage cascades, counterparty risk all manifested
- New element: SPEED - contagion that took months in 2008 took days in crypto due to 24/7 markets and instant settlement
- Key regulatory lesson: function-based regulation needed - if it walks like a bank (maturity transformation), regulate it like a bank
- Network topology mattered: 3AC was the critical node connecting Terra to the lender ecosystem
- FTX was fraud, but it revealed genuine systemic interconnections (Genesis, DCG, Gemini)
- Economic insight: Innovation in technology doesn't eliminate fundamental economic risks - it can accelerate them

---

## Exercise 4: "DeFi Will Replace TradFi" Great Debate

**Category**: Debate
**Time**: 30 min work + 5 min final presentations
**Group Size**: Two teams of 4-6 students each
**Materials Needed**: Timer

### Task

Full-course synthesis debate using ALL FOUR economic lenses. Each team must use at least one argument from each lens.

**Motion**: "By 2040, decentralized finance will handle the majority of global financial transactions, making traditional banks and intermediaries obsolete."

**Required**: Each team must cite concepts from at least three different lessons (L02-L07) to support their position.

**Team A (Pro)**: DeFi will replace TradFi
**Team B (Con)**: TradFi will adapt and survive

**Debate Structure**:
| Phase | Time | Activity |
|-------|------|----------|
| Preparation | 15 min | Teams prepare 4 arguments (one per lens) |
| Opening | 4 min each | Each team presents main arguments |
| Cross-examination | 5 min | Teams question each other |
| Rebuttals | 3 min each | Each team responds |
| Closing | 2 min each | Final summary |

### Model Answer / Expected Output

**TEAM A: PRO (DeFi Replaces TradFi)**

---

**ARGUMENT 1: MONETARY ECONOMICS**
*"DeFi enables programmable money that central banks cannot match"*

- Stablecoins provide dollar-equivalent money without bank intermediaries
- CBDCs will likely use DeFi infrastructure (smart contracts, distributed ledgers)
- Seigniorage currently captured by banks can flow to users (yield farming)
- Monetary policy can be implemented through smart contracts (algorithmic interest rates)
- Evidence: USDC/USDT combined volume already exceeds many national payment systems

**ARGUMENT 2: PLATFORM ECONOMICS**
*"Network effects favor composable, open protocols over walled gardens"*

- DeFi is "money legos" - protocols build on each other, creating exponential value
- Open APIs vs. closed banking systems - developers prefer DeFi
- No switching costs - users own their keys, can move freely between protocols
- Two-sided market: DeFi already has more developers than TradFi fintech
- Evidence: DeFi TVL grew from $1B (2020) to $200B (2024) without bank involvement

**ARGUMENT 3: MARKET MICROSTRUCTURE**
*"AMMs and on-chain markets are more efficient than traditional exchange structure"*

- 24/7 markets vs. limited banking hours
- No intermediaries taking spread - pure price discovery
- Instant settlement (minutes) vs. T+2 in traditional markets
- Transparent order books and transaction history
- Evidence: Uniswap volume rivals Coinbase; DEX/CEX ratio increasing

**ARGUMENT 4: REGULATORY ECONOMICS**
*"Code is law provides better enforcement than expensive human regulation"*

- Smart contracts are self-enforcing - no need for courts
- Audit trails are permanent and public - better than bank records
- Global, uniform rules vs. fragmented national regulation
- Regulatory arbitrage eliminated - same rules everywhere
- Evidence: DeFi protocols have processed $2T+ with far fewer staff than banks

---

**TEAM B: CON (TradFi Adapts and Survives)**

---

**ARGUMENT 1: MONETARY ECONOMICS**
*"Central banks will never cede monetary sovereignty to private protocols"*

- Money creation is a sovereign function - governments won't allow private alternatives
- Lender of last resort requires central bank - DeFi has none (2022 proved this)
- CBDCs will be distributed through banks, not replace them (re-intermediation)
- Bank credit creation serves macroeconomic goals - DeFi is overcollateralized only
- Evidence: No major economy has banned banks; all are regulating DeFi, not replacing TradFi

**ARGUMENT 2: PLATFORM ECONOMICS**
*"Banks have insurmountable network effects and trust capital"*

- 500+ years of trust vs. 10 years of DeFi (including multiple catastrophic failures)
- Banks already have billions of users - DeFi has <10 million active wallets
- FDIC insurance creates trust that DeFi cannot replicate
- Integration with government (tax, benefits, loans) creates lock-in
- Evidence: 2022 crisis lost $2T; users flooded BACK to banks for safety

**ARGUMENT 3: MARKET MICROSTRUCTURE**
*"DeFi markets have fundamental structural problems banks don't"*

- MEV extraction is a hidden tax on users - worse than bank fees
- Impermanent loss hurts liquidity providers - unsustainable model
- No credit creation - DeFi can only do overcollateralized lending (useless for most)
- Oracle manipulation creates systemic risks that don't exist in TradFi
- Evidence: Flash loan attacks, oracle exploits, bridge hacks - billions lost to design flaws

**ARGUMENT 4: REGULATORY ECONOMICS**
*"Regulation will either tame DeFi or kill it - neither means bank replacement"*

- AML/KYC requirements apply regardless of technology - compliant DeFi = CeFi
- Liability requires identifiable entities - "decentralized" developers get sued
- Consumer protection requires someone to hold accountable
- If DeFi succeeds, it gets regulated; if regulated, it becomes TradFi 2.0
- Evidence: MiCA requires authorization; SEC enforcement actions; Tornado Cash sanctions

---

**BALANCED VERDICT (for instructor):**

The economically strongest position is **TradFi transforms but doesn't disappear**:

1. **Monetary**: Central banks will maintain control - via CBDCs distributed through banks, not DeFi replacement

2. **Platform**: DeFi technology will be absorbed by TradFi (tokenization, smart contracts) but within regulated frameworks

3. **Microstructure**: Some functions will move to DeFi-style mechanisms (AMMs, 24/7 trading) but with TradFi wrappers for compliance

4. **Regulatory**: The fundamental insight: if DeFi becomes systemically important, it will be regulated; if regulated, it converges with TradFi

**Best analogy**: The internet didn't eliminate media companies - it transformed them. Amazon is still an intermediary (like a bank); it just uses better technology. Similarly, "DeFi" infrastructure will be used by institutions that look a lot like... banks.

### Presentation Talking Points
- Both sides must use all four lenses - no single-lens arguments
- The key economic question: is "decentralization" a feature users actually value, or just an implementation detail?
- 2022 crisis is Exhibit A for both sides: proves DeFi risk (Pro TradFi) or proves DeFi survived without bailouts (Pro DeFi)
- Network effects argument is crucial - do DeFi's composability benefits outweigh TradFi's trust and integration advantages?
- Economic insight: The debate is really about re-intermediation vs. disintermediation - history suggests new intermediaries replace old ones rather than elimination

---

## Exercise 5: Design a TradFi-DeFi Hybrid Institution

**Category**: Creative/Design
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Whiteboard, paper, markers

### Task

Your group is a founding team launching a new financial institution that combines the best of TradFi and DeFi. Design the institution using insights from all four economic lenses. You must address the Digital Finance Trilemma (Decentralization, Security, Scalability - pick two and explain the trade-off for the third).

**Cross-reference**:
- **L02**: Monetary policy implications of private money creation
- **L03**: CBDC integration opportunities
- **L05**: Platform economics and network effects
- **L07**: Regulatory compliance strategy

**Design Requirements:**
1. Name and one-sentence mission
2. Core services offered (minimum 3)
3. Technology stack (what's on-chain vs. off-chain)
4. Regulatory strategy (which jurisdiction, which licenses)
5. Trilemma positioning (explicit trade-off choice)
6. Competitive moat (why will you win?)

### Model Answer / Expected Output

**EXAMPLE DESIGN: "Meridian Finance"**

---

**MISSION**: "Institutional-grade DeFi with bank-level protection"

---

**CORE SERVICES:**

| Service | TradFi Element | DeFi Element | Value Proposition |
|---------|----------------|--------------|-------------------|
| **1. Tokenized Deposits** | FDIC-insured up to $250K; bank charter | Deposits represented as on-chain tokens; earn yield from DeFi | Safety of bank + yield of DeFi |
| **2. Compliant DeFi Access** | KYC/AML on all users; whitelisted protocol access only | Direct connection to Aave, Compound, Uniswap via permissioned pool | Access DeFi without compliance risk |
| **3. Institutional Lending** | Credit underwriting; legal loan agreements | Collateral held in smart contracts; automated liquidation | Lower cost lending with DeFi efficiency |
| **4. Cross-Border Payments** | Correspondent banking relationships; FX licenses | Settlement via stablecoin rails; instant finality | Speed of crypto, compliance of bank |

---

**TECHNOLOGY STACK:**

| Layer | On-Chain | Off-Chain | Rationale |
|-------|----------|-----------|-----------|
| **Customer Identity** | Soulbound verification tokens | KYC database, biometrics | Compliance requires off-chain verification; on-chain proof for protocol access |
| **Custody** | Smart contract vaults (multisig) | Cold storage for large holdings | Smart contracts for automation; cold storage for security |
| **Lending** | Collateral custody, automated liquidation | Credit scoring, loan origination | Automate what can be automated; human judgment for credit decisions |
| **Payments** | Stablecoin settlement layer | Bank account integration, ACH/SWIFT | Use crypto for efficiency; bank rails for fiat on/off ramp |
| **Yield Generation** | Direct integration with whitelisted DeFi protocols | Risk management, rebalancing algorithms | Capture DeFi yields with institutional risk controls |

---

**REGULATORY STRATEGY:**

| Jurisdiction | License/Charter | Rationale |
|--------------|-----------------|-----------|
| **Primary**: Switzerland (FINMA) | Fintech license + banking license application | Crypto-friendly, high credibility, EU market access |
| **Secondary**: Singapore (MAS) | Payment Services Act license | Asia-Pacific access, clear crypto framework |
| **Future**: US (OCC) | Special Purpose National Bank charter | Highest-value market, most demanding but most valuable |

**Regulatory Philosophy**: Be the most regulated crypto institution. Regulation is a moat, not a burden. Compliance cost is a barrier to entry that protects market position.

---

**TRILEMMA POSITIONING:**

```
                    DECENTRALIZATION
                          /\
                         /  \
                        /    \
                       /  X   \   <-- Meridian: Sacrifice partial decentralization
                      /________\
        EFFICIENCY ───────────────── COMPLIANCE
                      (We maximize both)
```

**Choice**: Maximize Efficiency + Compliance, sacrifice Decentralization

**Trade-off Rationale**:
- **Efficiency**: Smart contracts for automation, 24/7 operations, instant settlement
- **Compliance**: Full KYC/AML, regulatory licenses, deposit insurance
- **Decentralization sacrificed**: Permissioned access, centralized custody option, off-chain credit decisions

**Why this trade-off**: Institutional customers (our target) value compliance and efficiency over decentralization. They need to answer to regulators, auditors, and shareholders. "Decentralization" has no value to a pension fund - but efficiency and compliance do.

---

**COMPETITIVE MOAT:**

| Moat Type | How We Build It |
|-----------|-----------------|
| **Regulatory moat** | Licenses take 2-3 years and millions of dollars; first-mover advantage in compliant DeFi |
| **Network effects** | More institutional assets = better DeFi yields = more institutions want access |
| **Trust capital** | Bank charter + FDIC insurance = trust that crypto-native competitors can't match |
| **Technical integration** | Deep integration with both TradFi (SWIFT, ACH) and DeFi (on-chain protocols) - hard to replicate |
| **Data moat** | Proprietary data on DeFi protocol risk from live institutional exposure |

---

**RISKS AND MITIGATIONS:**

| Risk | Impact | Mitigation |
|------|--------|------------|
| Smart contract exploit | Customer funds lost | Insurance, formal verification, whitelisted protocols only |
| DeFi yield collapse | Revenue decline | Diversified yield sources; TradFi services as base |
| Regulatory change | License revoked | Multi-jurisdiction structure; regulatory relationships |
| Bank run | Liquidity crisis | FDIC insurance; liquid reserve requirements; stress testing |
| Stablecoin depeg | Settlement failure | Multi-stablecoin strategy; USDC primary (Circle banking partner) |

### Presentation Talking Points
- The design should explicitly reference all four lenses: monetary (deposit creation, yield), platform (network effects, two-sided market), microstructure (settlement, liquidity), regulatory (licensing, compliance)
- Trilemma trade-off must be explicit - there is no "all three" option
- Most institutional-focused designs will sacrifice decentralization for compliance - this is economically rational for the target market
- Key insight: "Hybrid" institutions will likely be the winners - pure DeFi is too risky, pure TradFi is too slow
- The competitive moat analysis should identify sustainable advantages, not just features

---

## Exercise 6: Digital Finance Trilemma Mapping

**Category**: Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Printed triangle template, markers, list of 10 projects

### Task

Map 10 crypto/digital finance projects onto the Digital Finance Trilemma triangle. For each project, assign scores from 0-10 for each dimension (Decentralization, Security, Scalability), justify your scoring, and identify the trade-off each project has made.

**Projects to Map:**
1. Bitcoin
2. Ethereum
3. Solana
4. USDC (Circle)
5. Tether (USDT)
6. Uniswap
7. Aave
8. Binance (CEX)
9. Coinbase
10. Digital Euro (CBDC - hypothetical)

### Model Answer / Expected Output

**COMPLETED TRILEMMA MAP:**

| Project | Decentralization | Security | Scalability | Trade-off Made |
|---------|------------------|------------|------------|----------------|
| **Bitcoin** | 9 | 9 | 2 | Maximum decentralization and security (PoW), sacrifices scalability (7 TPS, high fees) |
| **Ethereum** | 8 | 8 | 3 | High decentralization, strong security (PoS), moderate scalability (15 TPS, improving with L2s) |
| **Solana** | 5 | 5 | 9 | Sacrifices decentralization (validator concentration) and security (multiple outages) for scalability (65K TPS) |
| **USDC (Circle)** | 2 | 8 | 7 | Centralized issuer (Circle), strong security (regulated reserves), good scalability on modern chains |
| **Tether (USDT)** | 2 | 6 | 8 | Centralized, scalable across many chains, but security concerns (reserve transparency questions) |
| **Uniswap** | 8 | 7 | 4 | Decentralized protocol with smart-contract security, limited scalability (L1 gas costs) |
| **Aave** | 7 | 7 | 4 | Decentralized governance, audited smart contracts, scalability limited by L1 throughput |
| **Binance (CEX)** | 1 | 6 | 9 | Fully centralized, maximum scalability (matching engine), security risks (single point of failure, hacks) |
| **Coinbase** | 1 | 8 | 8 | Fully centralized, strong security (US-regulated, insured), high scalability at cost of decentralization |
| **Digital Euro (CBDC)** | 1 | 9 | 8 | Central bank issued (no decentralization), maximum security (sovereign backing), designed for scalability |

---

**VISUAL REPRESENTATION:**

```
                      DECENTRALIZATION (10)
                             /\
                            /  \
                           /    \
                          / BTC  \
                         /   ETH  \
                        /    UNI   \
                       /     AAVE   \
                      /              \
                     /  SOLANA        \
                    /                  \
                   /                    \
                  /    USDT  USDC        \
                 /                        \
                /      BNB    BASE         \
               /                            \
              /________________________________\
   SECURITY (10)                         SCALABILITY (10)
              CBDC     COINBASE
```

---

**DETAILED JUSTIFICATIONS:**

**Bitcoin (D:9, E:2, C:1)**
- Decentralization: Most distributed network (10,000+ nodes), no single point of failure, UTXO model resists censorship
- Efficiency: 7 TPS, 10-minute blocks, high fees during congestion, not suitable for payments
- Compliance: No identity layer, pseudonymous by design, resistant to regulatory integration
- Trade-off: Bitcoin maximally prioritizes decentralization; everything else is secondary

**Ethereum (D:8, E:4, C:2)**
- Decentralization: Large validator set (500,000+), but more concentrated than Bitcoin; client diversity concerns
- Efficiency: 15 TPS base layer, but L2s add capacity; higher than Bitcoin but still limited
- Compliance: Account-based model slightly easier to track than UTXO; some compliance tools exist (Chainalysis)
- Trade-off: Ethereum tries to balance decentralization with programmability, but neither efficiency nor compliance

**Solana (D:5, E:9, C:2)**
- Decentralization: Fewer validators (~2,000), high hardware requirements, some centralization concerns
- Efficiency: 65,000 TPS theoretical, sub-second finality, low fees
- Compliance: No native compliance features; same pseudonymity as other L1s
- Trade-off: Explicitly sacrifices decentralization for performance; "fast Ethereum" positioning

**USDC (D:2, E:7, C:9)**
- Decentralization: Single issuer (Circle), can freeze/blacklist addresses, centralized reserve management
- Efficiency: Works on multiple chains, fast settlement, low fees on modern chains
- Compliance: US-regulated, monthly reserve attestations, can comply with sanctions, works with banks
- Trade-off: Deliberately centralized to enable compliance; target market is institutions

**Uniswap (D:8, E:6, C:2)**
- Decentralization: Permissionless protocol, governance via UNI token, no central operator
- Efficiency: Instant swaps, but gas costs vary; efficient for large trades, expensive for small
- Compliance: No KYC, no identity, frontend geo-blocking only (easily bypassed), sanctions list compliance at UI only
- Trade-off: Maximizes decentralization within DeFi; compliance is minimal (and intentionally so)

**Coinbase (D:1, E:7, C:10)**
- Decentralization: Centralized exchange, company controls all assets, can freeze accounts
- Efficiency: Fast trading, good UX, but not instant settlement; withdrawal limits
- Compliance: US public company, BitLicense, registered with SEC, full KYC/AML, SAR filing
- Trade-off: Maximum compliance for US market access; accepts full centralization

**Digital Euro CBDC (D:1, E:8, C:10)**
- Decentralization: Central bank issued and controlled; by definition not decentralized
- Efficiency: Designed for instant settlement, 24/7, low/no fees for end users
- Compliance: Full regulatory compliance built-in; programmable compliance possible
- Trade-off: Central bank explicitly chooses efficiency + compliance; decentralization is not a goal

---

**SYNTHESIS INSIGHTS:**

| Cluster | Projects | Observation |
|---------|----------|-------------|
| **Decentralization maximizers** | Bitcoin, Ethereum, Uniswap | Sacrifice efficiency and compliance for censorship resistance |
| **Efficiency maximizers** | Solana, Binance | Accept some centralization for performance |
| **Compliance maximizers** | Coinbase, USDC, CBDC | Accept full centralization for regulatory access |
| **Balanced attempts** | Aave, Tether | Try to find middle ground; often criticized by all sides |

**Key Economic Insight**: The trilemma is real - no project achieves high scores on all three dimensions. Projects make explicit or implicit trade-offs based on their target users:
- Crypto natives value decentralization
- Traders value efficiency
- Institutions value compliance

### Presentation Talking Points
- Scoring requires defending each number - what does "7 out of 10 efficiency" mean?
- Projects cluster in corners, not center - the trilemma forces choices
- No project scores 10-10-10 - this validates the trilemma framework
- Evolution over time: Ethereum moving toward efficiency (L2s), Coinbase maintaining compliance focus
- Key insight: Where a project sits on the trilemma reveals its target market and values
- Prediction: Most valuable projects long-term will be in Efficiency + Compliance corner (where institutions are)

---

## Exercise 7: Digital Finance 2030: Predictive Analysis

**Category**: Future Prediction
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Discussion framework, access to course concepts

### Task

Using ALL frameworks from the course (four lenses, trilemma, network effects, contagion models), predict the state of digital finance in 2030. Make specific, falsifiable predictions for each category.

**Context**: Predictions made as of February 2025; evaluate plausibility based on current trends and course frameworks.

**Prediction Categories:**
1. CBDCs - Which countries will have retail CBDCs? How widely used?
2. Stablecoins - Market structure: how many major stablecoins? Regulated or unregulated?
3. DeFi - TVL in 2030? What's changed about how it works?
4. TradFi Integration - Have banks tokenized deposits? Do they offer crypto custody?
5. Payment Systems - What rails do cross-border payments use?
6. Regulatory Framework - Global coordination or fragmentation?

### Model Answer / Expected Output

**DIGITAL FINANCE 2030: COURSE FRAMEWORK PREDICTIONS**

---

**1. CBDCs**

| Prediction | Confidence | Framework Justification |
|------------|------------|------------------------|
| China's digital yuan will have 500M+ active users | High (85%) | **Platform economics (L05)**: First-mover network effects + government mandate = adoption. Already at 150M+ in 2024. |
| EU Digital Euro launched (2027) with modest adoption (50M users) | Medium (65%) | **Monetary economics (L02/L03)**: ECB committed but bank lobby will impose holding limits. Slow adoption like SEPA was. |
| US Fed will NOT have retail CBDC | High (80%) | **Regulatory economics (L07)**: Political opposition (privacy concerns, bank lobby). Fed prefers FedNow + regulated stablecoins. |
| 20+ countries with retail CBDCs | High (75%) | **Monetary economics (L03)**: Emerging markets leapfrog to CBDCs for financial inclusion (Bahamas, Nigeria model). |
| Interoperable CBDC corridors exist (mBridge expanded) | Medium (60%) | **Market microstructure (L06)**: Settlement efficiency demands drive cross-border CBDC links. BIS leading this work. |

---

**2. Stablecoins**

| Prediction | Confidence | Framework Justification |
|------------|------------|------------------------|
| Three dominant stablecoins: USDC, bank-issued (JPM/Citi), and EU-regulated | High (80%) | **Platform economics**: Network effects favor consolidation + **Regulatory economics**: Only regulated issuers survive |
| Tether (USDT) either regulated or marginalized | Medium (70%) | **Regulatory economics**: Global coordination on stablecoin standards (FSB) will force transparency or exclusion |
| Total stablecoin market cap: $500B-$1T | Medium (65%) | **Monetary economics**: Growing use case for payments and DeFi, but constrained by regulation |
| Algorithmic stablecoins effectively dead | High (90%) | **Market microstructure**: Terra collapse + regulatory ban (MiCA) eliminates economic viability |
| Bank-issued stablecoins (JPM Coin successors) rival crypto-native | Medium (60%) | **Platform economics**: Banks bring existing network effects and trust capital |

---

**3. DeFi**

| Prediction | Confidence | Framework Justification |
|------------|------------|------------------------|
| DeFi TVL: $500B-$1T (5-10x current) | Medium (55%) | **Platform economics**: Composability and yield opportunities continue attracting capital, but regulatory headwinds |
| "Permissioned DeFi" (Aave Arc model) becomes major category | High (75%) | **Regulatory economics**: Institutions need KYC-compliant DeFi access; market demand proven |
| Core protocols (Uniswap, Aave, Compound) still exist | High (85%) | **Market microstructure**: First-mover liquidity advantages; Lindy effect |
| MEV largely solved by protocol-level solutions | Medium (60%) | **Market microstructure**: Economic incentive to solve MEV is strong; Flashbots, PBS evolution |
| Real-world asset tokenization reaches $10T+ | Medium (65%) | **Monetary economics**: Efficiency gains too large to ignore; BlackRock, Fidelity leading |

---

**4. TradFi Integration**

| Prediction | Confidence | Framework Justification |
|------------|------------|------------------------|
| All top 20 global banks offer crypto custody | High (90%) | **Platform economics**: Client demand + regulatory clarity = offering. Already 10+ by 2024. |
| Tokenized deposits live at 5+ major banks | High (80%) | **Market microstructure**: JPM Onyx model proven; efficiency gains drive adoption |
| ETF-like products for major crypto assets in all G20 countries | High (85%) | **Regulatory economics**: US Bitcoin ETF approval in 2024 creates precedent; others follow |
| Blockchain settlement for securities in major markets | Medium (70%) | **Market microstructure**: T+0 settlement too efficient to ignore; pilots underway |
| Traditional exchanges (NYSE, LSE) trading tokenized assets | Medium (65%) | **Platform economics**: Leverage existing network effects; extend rather than build new |

---

**5. Payment Systems**

| Prediction | Confidence | Framework Justification |
|------------|------------|------------------------|
| Stablecoin rails handle 10%+ of cross-border payments | High (75%) | **Market microstructure**: Cost and speed advantages (vs. SWIFT) drive adoption for certain corridors |
| SWIFT still dominant but uses blockchain for settlement | Medium (60%) | **Platform economics**: Network effects too strong to replace; but efficiency pressure forces upgrade |
| CBDCs used for central bank settlement (wholesale) | High (80%) | **Monetary economics**: BIS projects (mBridge, Dunbar) already proving concept |
| Retail cross-border payments: hybrid stablecoin + CBDC | Medium (55%) | **Regulatory economics**: Regulatory preferences for CBDCs + stablecoin efficiency creates hybrid |
| Visa/Mastercard settlement layer includes stablecoins | High (85%) | **Platform economics**: Already experimenting; leverage existing merchant network |

---

**6. Regulatory Framework**

| Prediction | Confidence | Framework Justification |
|------------|------------|------------------------|
| Global baseline standards for stablecoins (FSB framework) | High (80%) | **Regulatory economics**: Systemic importance demands coordination; FSB already leading |
| No global coordination on DeFi - fragmented approach | High (85%) | **Regulatory economics**: DeFi's borderless nature makes coordination hard; jurisdictional arbitrage continues |
| "Same activity, same risk, same regulation" becomes norm | High (75%) | **Regulatory economics**: Function-based regulation is the only workable approach |
| Major jurisdiction bans Bitcoin | Low (20%) | **Monetary economics**: Too economically valuable; regulation preferred over prohibition |
| SEC clarifies most crypto tokens are securities | High (80%) | **Regulatory economics**: US case law building toward clear token classification |

---

**WILDCARD PREDICTIONS:**

| Wildcard | Probability | If True, Implications |
|----------|-------------|----------------------|
| Major stablecoin run (USDT fails) | 25% | Crypto winter, accelerated regulation, CBDC adoption boost |
| CBDC used for capital controls (China) | 40% | International resistance to CBDC interoperability; fragmentation |
| DeFi protocol DAO successfully governs at scale | 30% | New model for decentralized organization; implications beyond finance |
| Central bank adopts Bitcoin as reserve asset | 10% | Legitimization wave; massive price appreciation; monetary economics disruption |
| Quantum computing breaks current crypto | 5% (by 2030) | All bets off; massive migration to quantum-resistant cryptography |

---

**FRAMEWORK-BASED META-PREDICTION:**

Using the four lenses to predict the STRUCTURE of digital finance in 2030:

| Lens | 2030 Prediction |
|------|-----------------|
| **Monetary** | CBDCs exist but are complements to, not replacements for, bank deposits. Stablecoins regulated as e-money. Monetary policy transmission adapted but not fundamentally changed. |
| **Platform** | Winner-take-all dynamics create 2-3 dominant stablecoins, 1-2 dominant chains per use case. Network effects favor incumbents who adopt crypto technology. |
| **Microstructure** | Settlement moves to T+0 on blockchain rails for securities and cross-border payments. AMMs and order books coexist for different use cases. MEV partially solved. |
| **Regulatory** | Tiered regulation: heavy for stablecoins and exchanges, lighter for pure DeFi (but access restricted). International coordination on stablecoins, fragmentation on DeFi. |

### Presentation Talking Points
- Predictions must be specific and falsifiable - "DeFi will grow" is not a prediction
- Each prediction should cite specific course framework as justification
- Confidence levels force acknowledgment of uncertainty
- Wildcard predictions test ability to think about tail risks
- Key insight: Use the trilemma to predict - projects in Efficiency + Compliance corner will thrive in institutional adoption scenario
- Meta-prediction: The dichotomy between DeFi and TradFi will blur - "hybrid" models dominate

---

## Exercise 8: The Complete Case: All Four Lenses Integration

**Category**: Final Integration
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 4-5 (one person per lens + coordinator)
**Materials Needed**: Comprehensive case materials, four-lens analysis template

### Task

This is the capstone exercise. Your group will analyze a complex, real-world case using ALL FOUR economic lenses simultaneously. Each group member takes primary responsibility for one lens, but the final analysis must be INTEGRATED - showing how the lenses interact.

**Case: The March 2023 USDC Depeg Event**
*Event occurred March 2023; analysis conducted as of February 2025 with full hindsight.*

On March 10, 2023, Circle announced $3.3B of USDC reserves were held at Silicon Valley Bank, which had just failed. USDC depegged to $0.87 before recovering when the Fed announced depositor protection.

**Apply concepts from**:
- **L02**: Money as store of value, lender of last resort
- **L05**: Platform network effects, two-sided markets
- **L06**: Market microstructure, price discovery, liquidity
- **L07**: Regulatory gaps and systemic risk

**Required Analysis:**
1. Each lens perspective (4 separate analyses)
2. CROSS-LENS INTERACTIONS (how did they connect?)
3. Policy recommendations using insights from all lenses

### Model Answer / Expected Output

**USDC DEPEG CASE: COMPLETE FOUR-LENS ANALYSIS**

---

**LENS 1: MONETARY ECONOMICS ANALYSIS**

**Key Questions:**
- How did this affect USDC's function as money?
- What does this reveal about private money stability?

**Analysis:**

| Monetary Concept | Application to USDC Depeg |
|------------------|---------------------------|
| **Store of Value** | USDC failed store of value function during crisis: $1.00 → $0.87 = 13% purchasing power loss in hours |
| **Medium of Exchange** | During depeg, USDC was rejected by some merchants and DEXs (uncertainty about value) |
| **Money Demand Shock** | Classic flight to quality: USDC → DAI → USDT → USD (bank deposits) |
| **Seigniorage** | Circle earns interest on reserves (~$1B+ annually on $30B reserves); this income is at risk if reserves aren't safe |
| **Lender of Last Resort** | USDC had NO lender of last resort; Fed backstopped banks, not stablecoins - USDC only recovered because Fed backstopped SVB depositors |

**Key Monetary Insight**: The USDC depeg demonstrated that even "fully backed" private money is only as stable as its reserve assets AND its access to central bank facilities. USDC was one small decision away from permanent collapse - if Fed hadn't protected all SVB depositors, USDC might have faced 10%+ permanent impairment.

---

**LENS 2: PLATFORM ECONOMICS ANALYSIS**

**Key Questions:**
- How did network effects behave during stress?
- What happened to USDC's two-sided market?

**Analysis:**

| Platform Concept | Application to USDC Depeg |
|------------------|---------------------------|
| **Network Effects (Negative)** | Negative spiral: USDC sell → price drops → more USDC sell → accelerating depeg. Network effects reversed. |
| **Two-Sided Market Stress** | Users (holders) fled; protocols (liquidity pools) faced forced rebalancing; the two sides stopped transacting |
| **Switching Costs (Revealed: Low)** | Users instantly swapped USDC → DAI → USDT. No lock-in. Low switching costs accelerated run. |
| **Platform Competition** | Competitors benefited: DAI briefly at $1.05 (premium); USDT market cap increased; Tether gained share |
| **Composability Cascades** | DeFi protocols with USDC collateral faced forced liquidations; $1B+ in liquidations across protocols |

**Key Platform Insight**: USDC's network effects work in reverse during stress. The same composability that made USDC valuable (integration with every DeFi protocol) made the stress instantly systemic. Interestingly, DAI (decentralized) and USDT (offshore) benefited from USDC's (regulated) distress.

---

**LENS 3: MARKET MICROSTRUCTURE ANALYSIS**

**Key Questions:**
- How did price discovery work during stress?
- What happened to liquidity?

**Analysis:**

| Microstructure Concept | Application to USDC Depeg |
|------------------------|---------------------------|
| **Price Discovery** | DEX prices led CEX prices - Curve showed depeg first; CEX USDC/USD pairs followed with delay |
| **Liquidity Evaporation** | Curve 3pool massively imbalanced (80%+ USDC vs. 10% each DAI/USDT); market makers withdrew |
| **Arbitrage Breakdown** | Classical arb (buy USDC at $0.87, redeem for $1.00) was blocked - Circle redemptions paused |
| **Bid-Ask Spread** | Spreads widened 100x on some venues; $1M+ orders moved price 5%+ |
| **Price Impact** | Large sells caused cascading liquidations; $100M sells caused 3-5% additional price drops |

**Key Microstructure Insight**: The depeg revealed that stablecoin price stability depends on arbitrage mechanisms, which fail when redemptions are unavailable. The peg mechanism is: market price < $1 → arbs buy USDC → redeem for $1 reserves → profit. When Circle paused redemptions (weekend + bank failure), this mechanism broke, and the peg was unsupported.

---

**LENS 4: REGULATORY ECONOMICS ANALYSIS**

**Key Questions:**
- What market failures were revealed?
- How should regulators respond?

**Analysis:**

| Regulatory Concept | Application to USDC Depeg |
|--------------------|---------------------------|
| **Systemic Risk** | USDC is systemically important to DeFi (largest stablecoin by TVL); its depeg cascaded across ecosystem |
| **Information Asymmetry** | Users didn't know USDC's reserve composition until crisis; SVB exposure was not disclosed |
| **Consumer Protection** | No deposit insurance for stablecoin holders; no guaranteed redemption |
| **Moral Hazard** | Fed bailout of SVB depositors indirectly bailed out USDC - creates expectation of future bailouts? |
| **Regulatory Perimeter** | USDC is "regulated" (Circle has money transmitter licenses) but NOT like a bank (no FDIC, no Fed access) |

**Key Regulatory Insight**: The USDC depeg revealed that stablecoins occupy an ambiguous regulatory space - too integrated with banking to be independent, but not regulated as banks. The recovery depended on Fed action for banks, not stablecoin regulation. This suggests stablecoin issuers should either:
1. Become banks (with Fed access, FDIC insurance)
2. Hold only T-bills (no bank exposure)
3. Accept permanent run risk

---

**CROSS-LENS INTEGRATION: HOW THE LENSES CONNECTED**

| Interaction | Lens A | Lens B | Connection |
|-------------|--------|--------|------------|
| **1** | Monetary (reserve risk) | Microstructure (peg mechanism) | Reserve uncertainty broke arbitrage, causing depeg |
| **2** | Platform (composability) | Regulatory (systemic risk) | DeFi integration amplified systemic impact |
| **3** | Microstructure (liquidity) | Platform (network effects) | Liquidity withdrawal accelerated negative network effects |
| **4** | Regulatory (no LOLR) | Monetary (run dynamics) | Absence of lender of last resort enabled bank-run dynamic |
| **5** | Monetary (money demand) | Platform (switching costs) | Low switching costs enabled instant flight to competitors |
| **6** | Regulatory (moral hazard) | Monetary (money stability) | Fed bailout restored peg but created expectation of future support |

**The Key Integrated Insight**: The USDC depeg was a BANK RUN on an entity that isn't a bank:
- **Monetary lens**: It functions like a bank (takes deposits, invests reserves)
- **Platform lens**: It has network effects like a bank (systemic importance)
- **Microstructure lens**: It lacks bank stabilization mechanisms (peg broke when arb failed)
- **Regulatory lens**: It's not regulated like a bank (no deposit insurance, no Fed access)

This mismatch - bank-like function without bank-like regulation - is the core issue.

---

**POLICY RECOMMENDATIONS (INTEGRATED):**

| Recommendation | Lens Justification |
|----------------|-------------------|
| **1. Reserve disclosure requirements** | Microstructure (price discovery needs information) + Regulatory (reduce information asymmetry) |
| **2. Reserve composition rules (T-bills only)** | Monetary (reduce reserve risk) + Microstructure (enable continuous arbitrage) |
| **3. Systemic stablecoin designation with enhanced supervision** | Platform (network effects create systemic importance) + Regulatory (proportionate regulation) |
| **4. Mandatory 24/7 redemption windows** | Microstructure (maintain arbitrage mechanism) + Monetary (prevent run dynamics) |
| **5. Consider Fed access for systemic stablecoins** | Monetary (lender of last resort) + Platform (prevent negative network effect cascades) |
| **6. Interoperability requirements** | Platform (prevent single-stablecoin concentration) + Regulatory (reduce systemic risk) |

---

**FINAL SYNTHESIS: ONE-PARAGRAPH INTEGRATED CONCLUSION**

The March 2023 USDC depeg demonstrated that stablecoins occupy a dangerous regulatory gap: they function as money (monetary lens), benefit from powerful network effects (platform lens), depend on arbitrage mechanisms that can fail (microstructure lens), but lack the regulatory protections that make traditional bank deposits stable (regulatory lens). The recovery was accidental - dependent on Fed action for banks, not stablecoin-specific intervention. Going forward, regulators must either bring systemically important stablecoins into the banking perimeter (with Fed access and deposit insurance) or require reserve compositions (100% T-bills) that eliminate bank exposure. Half-measures leave the system vulnerable to future runs that may not be rescued.

### Presentation Talking Points
- Each lens reveals a different piece of the puzzle - no single lens explains the full dynamics
- The cross-lens integration is the key skill - see how monetary + microstructure created the depeg mechanism failure
- Policy recommendations should cite multiple lenses - shows integrated thinking
- The "bank without bank regulation" insight is the core synthesis
- Key economic insight: The USDC depeg proved that regulated stablecoins are not immune to runs - reserve composition and redemption mechanisms matter more than regulatory status
- Prediction: Future stablecoin regulation will require either bank-like status or T-bill-only reserves

---

**PLAN_READY: .omc/plans/l08-in-class-exercises.md**
