---
marp: true
theme: default
paginate: true
size: 16:9
---

# How AMMs Set Prices: The Constant Product Formula

**Assignment A6 — L06 Market Microstructure**

*Reference: Adams, H., Zinsmeister, N., Salem, M., Keefer, R., & Robinson, D. (2021). Uniswap v3 Core*

---

## The Model: x * y = k (Constant Product)

**Concept**: An AMM maintains a liquidity pool with two tokens (X, Y) where the product of reserves is constant:
$$x \cdot y = k \quad \text{(invariant)}$$

**Spot Price**: The marginal exchange rate is:
$$P = \frac{y}{x}$$

**Trade Mechanics**: To buy Δx of token X, you must pay Δy of token Y such that:
$$(x - \Delta x) \cdot (y + \Delta y) = k$$

Solving: $\Delta y = \frac{k}{x - \Delta x} - y$

**Slippage**: Effective price $P_{eff} = \Delta y / \Delta x$ exceeds spot price P due to convex curve (not linear).

---

## Baseline Results (k = 1M, x₀ = y₀ = 1000)

![width:900px](../../L06_Market_Microstructure/01_amm_constant_product/chart.png)

**Observations**:
- **Trade 100 X**: Costs 111 Y → effective price 1.111 Y/X → **11.1% slippage**
- **Trade 500 X**: Costs 1000 Y → effective price 2.0 Y/X → **100% slippage**
- Slippage grows **nonlinearly** (convex function)

---

## Variation 1: Deeper Pool (k = 10M)

![width:900px](chart_varied.png)
*(Panel 2: k = 10M — note reduced slippage)*

**Results**:
- Same 100 X trade now costs ~103.8 Y → **~3.8% slippage** (down from 11.1%)
- **Slippage reduction**: ~66% improvement with 10x deeper liquidity
- **Why?**: Larger k means flatter curve → smaller percentage change in y/x ratio

**Key Insight**: This is why liquidity mining exists — deeper pools attract traders with better prices.

---

## Variation 2: Imbalanced Pool (x₀ = 500, y₀ = 2000)

![width:900px](chart_varied.png)
*(Panel 3: Asymmetric curve with initial price P = 4.0)*

**Results**:
- Initial price P = y/x = 2000/500 = **4.0 Y/X** (not 1.0)
- Curve is **steeper on the X-side** (buying X is expensive)
- Curve is **flatter on the Y-side** (buying Y is cheaper)
- **Asymmetry**: Traders pay more slippage when buying the scarce asset (X)

**Implication**: Arbitrageurs will rebalance the pool toward x₀ = y₀ if external price differs.

---

## Variation 3: Adding 0.3% Swap Fee

![width:900px](chart_varied.png)
*(Panel 4: Slippage comparison with and without fee)*

**Fee Model**: Effective output = amount_out × 0.997

| Trade Size (X) | Slippage (no fee) | Slippage (with 0.3% fee) | Fee Impact |
|----------------|-------------------|-------------------------|------------|
| 10 | 1.0% | 1.3% | +0.3 pp |
| 50 | 5.3% | 5.6% | +0.3 pp |
| 100 | 11.1% | 11.4% | +0.3 pp |
| 200 | 25.0% | 25.4% | +0.4 pp |
| 500 | 100.0% | 100.6% | +0.6 pp |

**Observation**: Fee adds constant ~0.3 percentage points. For large trades, **slippage dominates fees**.

---

## Key Insights: Why Pool Depth Is Everything

1. **Nonlinear Slippage**: x * y = k creates convex curve → slippage grows faster than trade size

2. **Liquidity Is King**: 10x deeper pool (k = 10M) cuts slippage by ~70% for same trade
   - This is why protocols offer liquidity mining rewards (LP tokens, governance tokens)
   - Traders prefer deep pools → more volume → more fees for LPs → positive feedback loop

3. **Balance Matters**: Imbalanced pools punish trades in the scarce direction
   - Arbitrage naturally rebalances pools toward 50/50 split

4. **Fees Are Secondary**: For large trades, slippage (11%) >> fees (0.3%)
   - Protocol revenue comes from volume, not high fees

5. **Design Trade-off**: Constant product is simple but capital inefficient
   - Uniswap v3 uses concentrated liquidity to improve this
