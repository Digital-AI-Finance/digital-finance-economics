---
marp: true
theme: default
paginate: true
---

# Does Random Growth Create Monopolies?

**Model Answer**
Assignment A5 | L05 Platform & Token Economics
BSc Digital Finance & Economics

---

## The Model: Gibrat's Law (1931)

**Theory**: Firm growth rates are random and independent of firm size
**Equation**: $S_{i,t} = S_{i,t-1} \cdot (1 + \varepsilon_{i,t})$ where $\varepsilon \sim N(\mu, \sigma^2)$

**Baseline Parameters**:
- 100 firms start equal
- $\mu = 0.02$ (2% average growth)
- $\sigma = 0.25$ (25% growth volatility)
- 100 simulation periods

**Metrics**:
- **HHI** (Herfindahl-Hirschman Index): $\sum_i s_i^2$ — higher = more concentrated
- **Gini coefficient**: Inequality from 0 (equal) to 1 (monopoly)
- **CR4**: Combined market share of top 4 firms

**Citation**: Gibrat (1931), Arthur (1989) "Increasing Returns and Path Dependence"

---

## Baseline Results: Random Growth Creates Concentration

![width:900px](../../L05_Platform_Token_Economics/05_winner_take_all_market_share/chart.png)

**After 100 periods**:
- **HHI**: ~2,140 (below DOJ highly-concentrated threshold of 2,500 — but still moderately concentrated)
- **Gini**: ~0.75 (severe inequality)
- **CR4**: ~60% (top 4 firms control 60% of market)
- **Leader**: Single firm holds ~25% market share

**Key Observation**: Started equal, ended with winner-take-all. Pure randomness is sufficient.

---

## Variation 1: Low Volatility ($\sigma = 0.05$)

![width:800px](chart_varied.png)
*See Panel 2 (top-right) in variation chart*

**Change**: Reduced growth volatility from 25% to 5%

**Results**:
- **HHI**: Stays below 500 (competitive market)
- **Gini**: Below 0.3 (low inequality)
- **CR4**: ~25% (top 4 firms have normal competitive share)

**Interpretation**: **Volatility drives concentration**. When growth is stable, firms stay relatively equal. Random shocks must be large enough to create divergence.

---

## Variation 2: High Average Growth ($\mu = 0.10$)

![width:800px](chart_varied.png)
*See Panel 3 (bottom-left) in variation chart*

**Change**: Increased average growth rate from 2% to 10%

**Results**:
- **HHI**: Still rises to ~2,500
- **Gini**: Still ~0.70
- **CR4**: ~55%

**Interpretation**: Average growth ($\mu$) matters less than volatility ($\sigma$). All firms grow faster, but concentration still emerges because relative volatility creates winners. The **variance** of growth, not the mean, determines market structure.

---

## Variation 3: Fewer Firms ($n = 10$)

![width:800px](chart_varied.png)
*See Panel 4 (bottom-right) in variation chart*

**Change**: Started with 10 firms instead of 100

**Results**:
- **HHI**: Starts at ~1,000 (already concentrated), reaches 5,000+ rapidly
- **Gini**: Reaches 0.85+ (near-monopoly)
- **CR4**: ~85% (top 4 firms are almost entire market)

**Interpretation**: Smaller initial markets concentrate faster. With fewer firms, random shocks have larger relative impact on market shares. Oligopolistic markets are structurally unstable under random growth.

---

## Open Extension: Increasing Returns to Scale

**Modification**: Firms above 10% market share get 5% bonus growth

**Code Addition**:
```python
shares = active_sizes / np.sum(active_sizes)
for i in range(n_firms):
    if shares[i] > 0.10:
        sizes[i] *= 1.05  # 5% bonus
```

**Results** (compared to baseline):
- HHI reaches 4,500+ (vs. 2,140 baseline)
- Gini reaches 0.85+ (vs. 0.75)
- Winner emerges by period 50 (vs. period 80)

**Interpretation**: Increasing returns **accelerate** winner-take-all. Once a firm pulls ahead, it grows faster, creating a self-reinforcing cycle. This is the economic basis for platform monopolies (network effects = increasing returns).

---

## Key Insight: Volatility Creates Monopoly

**Research Question**: Does pure randomness in growth rates lead to monopoly?

**Answer**: **YES**, but only when growth volatility is high enough.

**Evidence**:
1. **Baseline**: Random growth ($\sigma = 0.25$) → moderate-to-severe concentration (HHI = 2,140)
2. **Variation 1**: Low volatility ($\sigma = 0.05$) → competitive market (HHI < 500)
3. **Variation 2**: High mean growth ($\mu = 0.10$) → still concentrates (HHI = 2,500)
4. **Variation 3**: Fewer firms → faster concentration (HHI = 5,000+)

**Economic Implication**: Markets with high growth uncertainty (e.g., tech platforms, crypto protocols) naturally tend toward monopoly **even without anticompetitive behavior**. Policy interventions (regulation, interoperability mandates) may be needed to preserve competition.

**Gibrat's Paradox**: Random growth is not neutral — it systematically favors concentration.
