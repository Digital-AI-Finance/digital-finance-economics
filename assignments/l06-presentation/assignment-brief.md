# Assignment A6: How AMMs Set Prices — The Constant Product Formula

## Introduction

An **AMM (Automated Market Maker)** is a piece of software that lets people trade one cryptocurrency for another without needing a human broker or traditional exchange. AMMs use the **constant product formula** x * y = k where:
- **x** and **y** are the quantities of two tokens in a **liquidity pool** (a shared pot of funds that anyone can trade against)
- **k** is a constant that never changes

When you buy token A, you add token B to the pool and remove token A. This changes the ratio y/x, which automatically changes the price. **Slippage** (the difference between the expected price and the actual price you pay) increases with trade size because larger trades move the ratio more.

## Your Task

You will explore how different pool parameters affect slippage by modifying the baseline constant product AMM model. Create a 7-slide Marp presentation analyzing three variations and one open extension.

### Baseline Model
- **Pool depth**: k = 1,000,000
- **Initial reserves**: x₀ = 1000, y₀ = 1000 (balanced pool, price = 1.0)
- **Spot price formula**: P = y/x
- **Trade formula**: When you buy Δx of token X, you pay Δy = k/(x - Δx) - y tokens of Y

### Variations to Analyze

**Variation 1: Increase pool depth**
- Set k = 10,000,000 (10x larger pool, meaning √(10M) ≈ 3162 of each token initially)
- How does slippage for a 100-token trade change compared to baseline?
- Why does deeper liquidity improve prices?

**Variation 2: Imbalanced pool**
- Set initial reserves: x₀ = 500, y₀ = 2000 (initial price = y/x = 4.0 instead of 1.0)
- Keep k = 1,000,000 (so x₀ * y₀ = k still holds)
- How does the curve shape differ?
- What happens to slippage when buying X vs buying Y?

**Variation 3: Add 0.3% swap fee**
- Apply fee to output: effective output = amount_out * 0.997
- Compute effective slippage for trades of [10, 50, 100, 200, 500] tokens
- Compare to baseline (no fee)
- How much does the fee add to total slippage?

**Open Extension: Pool Depth Comparison**
- Create a chart comparing slippage between k = 1M and k = 10M on the same axes
- Show slippage curves for trade sizes from 10 to 500 tokens
- What is the percentage reduction in slippage at different trade sizes?

## Deliverables

1. **7-slide Marp presentation** (`model-answer-presentation.md`):
   - Slide 1: Title + citation (Adams et al. 2021 — Uniswap v3 Core)
   - Slide 2: The Model — formula explanation
   - Slide 3: Baseline results with baseline chart
   - Slide 4: Variation 1 results with variation chart
   - Slide 5: Variation 2 results
   - Slide 6: Variation 3 results with fee comparison
   - Slide 7: Key insights — why pool depth matters

2. **Python chart** (`chart_varied.py`):
   - 2×2 subplot grid (16×12 inches)
   - Panel 1: Baseline — constant product curve with trade arrows for 100 and 500 token trades
   - Panel 2: Variation 1 — k = 10M, same trades, show reduced slippage
   - Panel 3: Variation 2 — x₀ = 500, y₀ = 2000, show asymmetric curve
   - Panel 4: Variation 3 — bar chart comparing slippage with and without 0.3% fee for trade sizes [10, 50, 100, 200, 500]
   - Use `np.random.seed(42)` for reproducibility
   - Save to `chart_varied.pdf` and `chart_varied.png`

## How to Run

Use **Google Colab** (free, no installation required):
1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Upload `chart_varied.py`
3. Run the script (Runtime → Run all)
4. Download generated PNG/PDF from the Files panel (left sidebar)

For the Marp presentation:
1. Install the Marp extension in VS Code, or
2. Use the online Marp editor at [marp.app](https://marp.app)

## Time Allocation

- **Analysis and coding**: 45 minutes
- **Presentation preparation**: 10 minutes
- **Total**: 55 minutes

## Learning Objectives

By completing this assignment, you will:
- Understand how the constant product formula x * y = k automatically sets prices
- See why larger trades suffer worse slippage (convex, not linear)
- Appreciate why liquidity mining exists (deep pools = better prices)
- Recognize the importance of pool balance and fee structure
- Practice presenting quantitative financial analysis visually

## Grading Rubric (100 points)

| Component | Points | Criteria |
|-----------|--------|----------|
| Variation 1 analysis | 20 | Correct k = 10M calculation, slippage comparison |
| Variation 2 analysis | 20 | Correct imbalanced pool, asymmetric curve explanation |
| Variation 3 analysis | 20 | Fee calculation correct, slippage comparison table |
| Chart quality | 20 | All 4 panels correct, annotations clear, professional |
| Presentation clarity | 15 | Logic flow, key insights highlighted, visuals support text |
| Open extension | 5 | Thoughtful comparison, actionable insight |

## References

Adams, H., Zinsmeister, N., Salem, M., Keefer, R., & Robinson, D. (2021). *Uniswap v3 Core*. Retrieved from https://uniswap.org/whitepaper-v3.pdf
