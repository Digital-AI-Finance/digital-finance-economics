---
marp: true
theme: default
paginate: true
---

# How Financial Crises Spread Through Networks

**Assignment A8: Financial Contagion Simulation**

Reference: Acemoglu, D., Ozdaglar, A., & Tahbaz-Salehi, A. (2015). Systemic Risk and Stability in Financial Networks. *American Economic Review*, 105(2), 564-608.

---

## The Model: Network Contagion Mechanics

**Setup:**
- 20 financial institutions arranged in a random network
- Each node has a **capital buffer** $B_i$ (randomly drawn from [0.05, 0.20])
- Connections represent financial exposures (loans, derivatives, interbank lending)

**Cascade Dynamics:**
When institution $i$ fails, it spreads losses to all connected neighbors:

$$\text{Loss}_j = \sum_{i \in \text{failed neighbors}} \frac{B_i}{\text{degree}_i}$$

- If $\text{Loss}_j > B_j$, then institution $j$ also fails
- Process repeats until no new failures occur

---

## Baseline Results: Single Shock Cascade

![bg right:60% 95%](../../L08_Synthesis/01_systemic_risk_contagion/chart.png)

**Observations:**
- Initial shock to node 0 (marked "Shock")
- Cascade spreads through network connections
- Multiple rounds of failures (shown in bar chart)
- Some nodes become **stressed** (orange) but don't fail
- Total failures depend on network structure and buffer distribution

---

## Variation 1: Doubled Capital Buffers

![bg right:50% 95%](chart_varied.png)

**Change:** Buffers increased from [0.05, 0.20] to [0.10, 0.40]

**Result:** Significantly **fewer failures**

**Policy Implication:**
Capital requirements are the most effective defense against systemic risk. Even modest increases in buffers can prevent cascades.

**Trade-off:** Higher capital requirements reduce bank profitability and may restrict lending.

---

## Variation 2: Dense Network (p=0.7)

**Change:** Connection probability increased from 0.3 to 0.7

**Result:** **MORE failures** than baseline (counterintuitive!)

**The "Robust-Yet-Fragile" Paradox:**
- **Low density:** Isolated failures (few connections to spread losses)
- **Medium density:** Network absorbs shocks well (diversified exposures)
- **High density:** Every failure hits many institutions simultaneously

**Real-world example:** 2008 financial crisis — highly interconnected institutions (AIG, Lehman Brothers) spread losses globally through credit default swaps and interbank markets.

---

## Variation 3: Multiple Initial Shocks

**Change:** 3 simultaneous failures instead of 1

**Result:** Devastating cascade with **rapid propagation**

**Why it matters:**
- Correlated failures (e.g., exposure to same asset class) trigger simultaneous shocks
- 2008 crisis: many banks held mortgage-backed securities, all failed together
- 2020 COVID shock: entire travel/hospitality sectors affected at once

**Regulatory response:** Stress tests now simulate multiple simultaneous shocks to ensure banks can survive correlated failures.

---

## Key Insights: Network Structure Determines Systemic Risk

1. **Buffers protect individuals; network structure determines systemic risk**
   - Individual bank strength (high capital) is necessary but not sufficient
   - Network topology (who is connected to whom) matters more than you'd expect

2. **Dense networks are "robust-yet-fragile"** (Acemoglu et al., 2015)
   - Small shocks: absorbed by many counterparties (robust)
   - Large shocks: hit everyone simultaneously (fragile)

3. **Policy implications:**
   - Monitor interconnectedness, not just individual bank health
   - Central clearing counterparties (CCPs) reduce network complexity
   - Circuit breakers and emergency liquidity can stop cascades

4. **Trade-offs are unavoidable:**
   - Isolation reduces contagion but prevents risk-sharing
   - Interconnection enables diversification but creates fragility
