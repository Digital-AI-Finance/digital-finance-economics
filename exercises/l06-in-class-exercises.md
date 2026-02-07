# L06 In-Class Exercises: Market Microstructure in Digital Finance

## Plan Metadata
- **Created**: 2026-02-04
- **Lesson**: L06 - Market Microstructure in Digital Finance (AMMs, Order Books, Price Discovery)
- **Target Audience**: BSc students (just completed L06)
- **Time Allocation**: 30 minutes work + 5 minutes presentation per exercise
- **Instructor Choice**: Select 1-2 exercises per session based on class size and learning goals

---

## Exercise Overview

| # | Title | Category | Group Size | Materials |
|---|-------|----------|------------|-----------|
| 1 | AMM Price Impact Simulator | Python/Data | Individual or Pairs | Laptop with Python |
| 2 | Impermanent Loss Calculator | Python/Data | Individual or Pairs | Laptop with Python |
| 3 | CEX vs DEX Battle Matrix | Framework Application | Groups of 3-4 | Worksheet |
| 4 | Sandwich Attack Anatomy | Case Study | Groups of 3-4 | Case Data |
| 5 | MEV Ethics Debate | Debate/Discussion | Two Teams (4-6 each) | None |
| 6 | Design an MEV-Resistant AMM | Creative/Design | Groups of 3-4 | Whiteboard/Paper |
| 7 | LP Profitability Analysis | Quantitative Analysis | Pairs | Calculator/Spreadsheet |
| 8 | Order Book vs AMM Trade Execution | Comparative Analysis | Groups of 3-4 | Worksheet |

### Exercise Pairing Recommendations

Choose exercise pairs based on your pedagogical goals:

| Focus | Pair | Rationale |
|-------|------|-----------|
| Quantitative | 1 + 7 | AMM mechanics + LP profitability analysis |
| Conceptual | 3 + 5 | CEX vs DEX comparison + MEV ethics |
| Creative | 6 + 8 | MEV-resistant design + trade execution comparison |
| Mixed | 2 + 4 | IL calculations + sandwich attack case study |

---

## Exercise 1: AMM Price Impact Simulator

**Category**: Python/Data
**Time**: 30 min work + 5 min presentation
**Group Size**: Individual or Pairs
**Materials Needed**: Laptop with Python (numpy, matplotlib), internet access

> **Key Terms**
>
> - **Constant product formula (x*y=k)**: The invariant maintained by Uniswap v2-style AMMs. The product of the two token reserves must remain constant after every trade (ignoring fees).
> - **Spot price (P=y/x)**: The instantaneous price of token X in terms of token Y, calculated as the ratio of reserves. Changes with every trade.
> - **Slippage**: The difference between the expected price before a trade and the actual execution price. Caused by the trade itself moving along the x*y=k curve.
> - **Price impact**: How much your trade moves the market price. Larger trades have greater price impact because they consume more of the pool's reserves.
> - **Liquidity pool**: A smart contract holding reserves of two tokens. Anyone can trade against it using the constant product formula, and anyone can deposit tokens to earn trading fees.

### Task

Build a constant product AMM simulator that demonstrates how trade size affects price impact and slippage. Use the x*y=k formula to show why large trades are expensive on AMMs.

**Specific Requirements:**
1. Implement the constant product formula x*y=k
2. Calculate price impact for trades of varying sizes (10, 50, 100, 500, 1000 tokens)
3. Compare effective price vs. spot price
4. Visualize the relationship between trade size and slippage
5. Answer: At what trade size does slippage exceed 5%? 10%?

### Setup Verification

Before starting, verify your environment:

```python
# Run this cell first to check your setup
import sys
print(f"Python version: {sys.version}")

try:
    import numpy as np
    print(f"numpy: {np.__version__}")
except ImportError:
    print("ERROR: numpy not installed. Run: pip install numpy")

try:
    import matplotlib
    print(f"matplotlib: {matplotlib.__version__}")
except ImportError:
    print("ERROR: matplotlib not installed. Run: pip install matplotlib")

print("\nAll dependencies OK!" if all(
    __import__(m) for m in ['numpy', 'matplotlib']
) else "Fix missing dependencies above.")
```

### Student Task

Complete the skeleton code below. Fill in each `# YOUR CODE HERE` section.

**Step-by-step instructions:**

1. Implement the `execute_buy_eth()` function using the constant product formula
2. Analyze trades of different sizes and record results
3. Implement the slippage threshold search to find where slippage exceeds 5% and 10%
4. The visualization code is provided for you

```python
"""
AMM Price Impact Simulator
L06 Exercise - Market Microstructure in Digital Finance

Demonstrates: Constant product formula (x*y=k), price impact, slippage
Requirements: pip install numpy matplotlib
# Data as of February 2025
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# AMM POOL SETUP
# =============================================================================

# Initial pool reserves (ETH/USDC pool)
x_initial = 1000  # ETH in pool
y_initial = 1_800_000  # USDC in pool (implies ETH price = $1800)
k = x_initial * y_initial  # Constant product invariant

spot_price = y_initial / x_initial
print(f"Initial Pool State:")
print(f"  ETH Reserve: {x_initial:,} ETH")
print(f"  USDC Reserve: {y_initial:,} USDC")
print(f"  Constant k: {k:,}")
print(f"  Spot Price: ${spot_price:,.2f} per ETH")
print()

# =============================================================================
# TRADE EXECUTION FUNCTION
# =============================================================================

def execute_buy_eth(eth_to_buy, x_pool, y_pool, k_constant):
    """
    Buy ETH from the pool by paying USDC.

    The constant product formula says: x * y = k (always).
    After removing eth_to_buy from the pool:
      new_x = x_pool - eth_to_buy
      new_y = k_constant / new_x   (to maintain k)
      usdc_cost = new_y - y_pool    (USDC added to pool)

    Then calculate:
      effective_price = usdc_cost / eth_to_buy
      slippage_pct = (effective_price - spot_price) / spot_price * 100

    Returns: (usdc_cost, effective_price, slippage_pct, new_x, new_y)
    """
    # YOUR CODE HERE
    # 1. Calculate new_x after removing eth_to_buy from the pool
    # 2. Calculate new_y using k_constant / new_x
    # 3. Calculate usdc_cost = new_y - y_pool
    # 4. Calculate effective_price = usdc_cost / eth_to_buy
    # 5. Calculate slippage_pct using current spot price (y_pool / x_pool)
    # 6. Return (usdc_cost, effective_price, slippage_pct, new_x, new_y)
    pass

# =============================================================================
# ANALYZE TRADES OF DIFFERENT SIZES
# =============================================================================

print("="*70)
print("TRADE ANALYSIS: Buying ETH from the Pool")
print("="*70)
print(f"{'Trade Size':>12} | {'USDC Cost':>14} | {'Eff. Price':>12} | {'Slippage':>10} | {'Pool Impact':>12}")
print("-"*70)

trade_sizes = [1, 10, 50, 100, 200, 500, 1000]
results = []

for eth_amount in trade_sizes:
    if eth_amount >= x_initial:
        print(f"{eth_amount:>12} ETH | {'IMPOSSIBLE - exceeds pool':>50}")
        continue

    cost, eff_price, slip, new_x, new_y = execute_buy_eth(
        eth_amount, x_initial, y_initial, k
    )

    pool_impact = (x_initial - new_x) / x_initial * 100

    results.append({
        'size': eth_amount,
        'cost': cost,
        'eff_price': eff_price,
        'slippage': slip,
        'pool_impact': pool_impact
    })

    print(f"{eth_amount:>12} ETH | ${cost:>13,.2f} | ${eff_price:>11,.2f} | {slip:>9.2f}% | {pool_impact:>11.1f}%")

# =============================================================================
# FIND CRITICAL SLIPPAGE THRESHOLDS
# =============================================================================

print()
print("="*70)
print("SLIPPAGE THRESHOLD ANALYSIS")
print("="*70)

# YOUR CODE HERE
# 1. Create an array of test_sizes from 1 to 500 (use np.linspace with 1000 points)
# 2. For each size, call execute_buy_eth() and collect the slippage values
# 3. Convert to numpy array
# 4. Use np.argmax(slippages >= 5) to find where slippage first hits 5%
# 5. Use np.argmax(slippages >= 10) to find where slippage first hits 10%
# 6. Print the threshold sizes and their notional values (size * spot_price)
# 7. Print each threshold as a percentage of pool reserves

# =============================================================================
# VISUALIZATION (provided - no changes needed)
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Constant Product Curve
ax1 = axes[0, 0]
x_curve = np.linspace(100, 2000, 500)
y_curve = k / x_curve

ax1.plot(x_curve, y_curve, 'b-', linewidth=2, label=r'$x \cdot y = k$')
ax1.plot(x_initial, y_initial, 'go', markersize=12, label='Initial State', zorder=5)

# Show a trade
trade_example = 100
_, _, _, new_x_ex, new_y_ex = execute_buy_eth(trade_example, x_initial, y_initial, k)
ax1.plot(new_x_ex, new_y_ex, 'ro', markersize=10, label=f'After {trade_example} ETH buy', zorder=5)
ax1.annotate('', xy=(new_x_ex, new_y_ex), xytext=(x_initial, y_initial),
            arrowprops=dict(arrowstyle='->', color='red', lw=2))

ax1.set_xlabel('ETH Reserve (x)')
ax1.set_ylabel('USDC Reserve (y)')
ax1.set_title('Constant Product Curve (x*y=k)')
ax1.legend()
ax1.grid(alpha=0.3)
ax1.set_xlim(0, 2000)

# Plot 2: Slippage vs Trade Size
ax2 = axes[0, 1]
ax2.plot(test_sizes, slippages, 'b-', linewidth=2)
ax2.axhline(y=5, color='orange', linestyle='--', label='5% threshold')
ax2.axhline(y=10, color='red', linestyle='--', label='10% threshold')
if size_5pct:
    ax2.axvline(x=size_5pct, color='orange', linestyle=':', alpha=0.5)
if size_10pct:
    ax2.axvline(x=size_10pct, color='red', linestyle=':', alpha=0.5)

ax2.set_xlabel('Trade Size (ETH)')
ax2.set_ylabel('Slippage (%)')
ax2.set_title('Price Slippage vs. Trade Size')
ax2.legend()
ax2.grid(alpha=0.3)

# Plot 3: Effective Price vs Trade Size
ax3 = axes[1, 0]
sizes_plot = [r['size'] for r in results]
eff_prices = [r['eff_price'] for r in results]

ax3.bar(range(len(sizes_plot)), eff_prices, color='steelblue', alpha=0.7)
ax3.axhline(y=spot_price, color='green', linestyle='--', linewidth=2, label=f'Spot: ${spot_price:,.0f}')
ax3.set_xticks(range(len(sizes_plot)))
ax3.set_xticklabels([f'{s} ETH' for s in sizes_plot], rotation=45)
ax3.set_ylabel('Effective Price ($/ETH)')
ax3.set_title('Effective Price by Trade Size')
ax3.legend()
ax3.grid(axis='y', alpha=0.3)

# Add price labels on bars
for i, (size, price) in enumerate(zip(sizes_plot, eff_prices)):
    ax3.text(i, price + 20, f'${price:,.0f}', ha='center', fontsize=9)

# Plot 4: Pool Depletion
ax4 = axes[1, 1]
pool_impacts = [r['pool_impact'] for r in results]

ax4.bar(range(len(sizes_plot)), pool_impacts, color='coral', alpha=0.7)
ax4.set_xticks(range(len(sizes_plot)))
ax4.set_xticklabels([f'{s} ETH' for s in sizes_plot], rotation=45)
ax4.set_ylabel('Pool Depletion (%)')
ax4.set_title('Pool Reserve Impact by Trade Size')
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('amm_price_impact_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nChart saved as 'amm_price_impact_analysis.png'")
```

### Discussion Questions

After running your simulator, discuss with your partner or group:

1. **Nonlinear price impact**: Why does slippage grow nonlinearly with trade size? What mathematical property of x*y=k causes this?
2. **Constant product mechanics**: Explain in your own words why removing X from the pool requires adding progressively more Y.
3. **Practical implications**: If you needed to buy $500,000 worth of ETH, would you use an AMM with this pool size? What alternatives exist?
4. **Pool size matters**: How would slippage change if this pool were 10x larger (10,000 ETH / 18,000,000 USDC)? Why do protocols compete for TVL?
5. **AMM vs order book**: AMM slippage is guaranteed by the formula. Order book slippage depends on available depth. When is guaranteed liquidity (with slippage) preferable to uncertain depth (with potentially less slippage)?

### Model Answer / Expected Output

**Expected Console Output (approximate):**
```
Initial Pool State:
  ETH Reserve: 1,000 ETH
  USDC Reserve: 1,800,000 USDC
  Constant k: 1,800,000,000
  Spot Price: $1,800.00 per ETH

TRADE ANALYSIS: Buying ETH from the Pool
   Trade Size |      USDC Cost |   Eff. Price |   Slippage | Pool Impact
----------------------------------------------------------------------
        1 ETH |      $1,801.80 |    $1,801.80 |      0.10% |        0.1%
       10 ETH |     $18,181.82 |    $1,818.18 |      1.01% |        1.0%
       50 ETH |     $94,736.84 |    $1,894.74 |      5.26% |        5.0%
      100 ETH |    $200,000.00 |    $2,000.00 |     11.11% |       10.0%
      200 ETH |    $450,000.00 |    $2,250.00 |     25.00% |       20.0%
      500 ETH |  $1,800,000.00 |    $3,600.00 |    100.00% |       50.0%

5% slippage threshold:  47.2 ETH ($84,960 notional)
10% slippage threshold: 91.3 ETH ($164,340 notional)

5% slippage at 4.7% of pool reserves
10% slippage at 9.1% of pool reserves
```

**Key Quantitative Insights:**
1. **5% slippage** occurs at approximately 4.7% of pool reserves
2. **10% slippage** occurs at approximately 9.1% of pool reserves
3. The relationship is approximately: slippage % = trade_size / (pool_size - trade_size)
4. A $90,000 trade in a $3.6M pool already incurs 5% slippage

### Presentation Talking Points
- The constant product formula (x*y=k) creates GUARANTEED slippage - this is not a bug, it's how AMMs work
- Slippage is the "price" of guaranteed liquidity - you can always trade, but large trades are expensive
- Pool depth (TVL) is the key metric: a 10x larger pool has ~10x less slippage for the same trade
- This explains why professional traders prefer order books for large trades, but retail prefers AMMs for convenience
- Economic insight: AMM slippage is predictable and transparent (formula-based) vs. order book slippage which depends on hidden depth

---

## Exercise 2: Impermanent Loss Calculator

**Category**: Python/Data
**Time**: 30 min work + 5 min presentation
**Group Size**: Individual or Pairs
**Materials Needed**: Laptop with Python (numpy, matplotlib), calculator

> **Key Terms**
>
> - **Impermanent loss (IL)**: The opportunity cost of providing liquidity to an AMM pool compared to simply holding the tokens. Called "impermanent" because it reverses if prices return to the original ratio -- but it becomes permanent if you withdraw at a different ratio.
> - **Price ratio (r)**: The ratio of the token's final price to its initial price. If ETH goes from $1,800 to $3,600, r = 2.0.
> - **Liquidity provider (LP)**: Someone who deposits tokens into an AMM pool to earn trading fees. LPs take on impermanent loss risk in exchange for fee income.
> - **Fee APY (annual percentage yield)**: The annualized return from trading fees earned by LPs. Must exceed IL for LP to be profitable vs. holding.

### Task

Build an impermanent loss calculator that shows when providing liquidity is profitable vs. simply holding assets. Determine the breakeven fee APY needed to compensate for IL at different price movements.

**Specific Requirements:**
1. Implement the IL formula: IL = 2*sqrt(r)/(1+r) - 1, where r = price_ratio
2. Calculate IL for price changes: 0.5x, 0.75x, 1.25x, 1.5x, 2x, 3x, 5x
3. Determine the fee APY needed to break even at each price ratio
4. Create a "should I LP?" decision framework

### Setup Verification

Before starting, verify your environment:

```python
# Run this cell first to check your setup
import sys
print(f"Python version: {sys.version}")

try:
    import numpy as np
    print(f"numpy: {np.__version__}")
except ImportError:
    print("ERROR: numpy not installed. Run: pip install numpy")

try:
    import matplotlib
    print(f"matplotlib: {matplotlib.__version__}")
except ImportError:
    print("ERROR: matplotlib not installed. Run: pip install matplotlib")

print("\nAll dependencies OK!" if all(
    __import__(m) for m in ['numpy', 'matplotlib']
) else "Fix missing dependencies above.")
```

### Student Task

Complete the skeleton code below. Fill in each `# YOUR CODE HERE` section.

**Step-by-step instructions:**

1. Implement the `impermanent_loss()` function using the IL formula
2. Implement the `portfolio_values()` function to compare LP vs hold strategies
3. Analyze price scenarios and record results
4. Implement the breakeven fee calculation
5. The visualization and decision framework code is provided for you

```python
"""
Impermanent Loss Calculator
L06 Exercise - Market Microstructure in Digital Finance

Demonstrates: Impermanent loss formula, LP profitability analysis
Requirements: pip install numpy matplotlib
# Data as of February 2025
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# IMPERMANENT LOSS FORMULA
# =============================================================================

def impermanent_loss(price_ratio):
    """
    Calculate impermanent loss given price ratio (final/initial).

    Formula: IL = 2*sqrt(r)/(1+r) - 1

    Returns: IL as a decimal (negative = loss relative to holding)
    """
    # YOUR CODE HERE
    # 1. Let r = price_ratio
    # 2. Return 2 * sqrt(r) / (1 + r) - 1
    pass

def portfolio_values(initial_value, price_ratio):
    """
    Calculate LP position value vs. hold value.

    Assumes 50/50 initial split (standard for most AMM pools).

    Hold strategy: half in volatile token (appreciates by price_ratio),
                   half in stablecoin (unchanged).
    Formula: hold_value = initial_value * (1 + price_ratio) / 2

    LP strategy: value scales with sqrt(price_ratio) due to constant
                 product rebalancing.
    Formula: lp_value = initial_value * sqrt(price_ratio)

    Returns: (lp_value, hold_value)
    """
    # YOUR CODE HERE
    # 1. Calculate hold_value = initial_value * (1 + price_ratio) / 2
    # 2. Calculate lp_value = initial_value * sqrt(price_ratio)
    # 3. Return (lp_value, hold_value)
    pass

# =============================================================================
# ANALYZE SPECIFIC PRICE SCENARIOS
# =============================================================================

print("="*80)
print("IMPERMANENT LOSS ANALYSIS")
print("="*80)
print()

# Initial investment
initial_investment = 10000  # $10,000 total ($5k ETH + $5k USDC)

price_ratios = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 5.0]

print(f"Initial Investment: ${initial_investment:,} (50% ETH, 50% USDC)")
print(f"Initial ETH Price: $1,800 (assumed)")
print()
print(f"{'Price Change':>14} | {'LP Value':>12} | {'Hold Value':>12} | {'IL':>10} | {'$ Lost to IL':>12}")
print("-"*80)

results = []

for ratio in price_ratios:
    lp_val, hold_val = portfolio_values(initial_investment, ratio)
    il = impermanent_loss(ratio)
    dollar_loss = hold_val - lp_val  # Positive means LP lost money vs holding

    results.append({
        'ratio': ratio,
        'lp_value': lp_val,
        'hold_value': hold_val,
        'il': il,
        'dollar_loss': dollar_loss
    })

    # Format price change
    if ratio < 1:
        change_str = f"{ratio:.0%} ({1/ratio:.1f}x down)"
    elif ratio > 1:
        change_str = f"{ratio:.0%} ({ratio:.1f}x up)"
    else:
        change_str = "100% (no change)"

    print(f"{change_str:>14} | ${lp_val:>10,.2f} | ${hold_val:>10,.2f} | {il:>9.2%} | ${dollar_loss:>10,.2f}")

# =============================================================================
# BREAKEVEN FEE ANALYSIS
# =============================================================================

print()
print("="*80)
print("BREAKEVEN FEE APY ANALYSIS")
print("="*80)
print()
print("Question: What fee APY do you need to BREAK EVEN with IL?")
print()

# Assume 1-year holding period
holding_period_days = 365

print(f"{'Price Change':>14} | {'IL Loss':>10} | {'Daily Fee Needed':>16} | {'Annual APY Needed':>18}")
print("-"*80)

# YOUR CODE HERE
# For each result in results (skip ratio == 1.0):
#   1. Calculate il_pct = abs(il) * 100
#   2. Calculate daily_fee_needed = il_pct / holding_period_days
#   3. Calculate annual_apy_needed = il_pct (simple approximation)
#   4. Print the row with formatted values

# =============================================================================
# VISUALIZATION (provided - no changes needed)
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: IL vs Price Ratio
ax1 = axes[0, 0]
ratios = np.linspace(0.1, 5, 500)
ils = [impermanent_loss(r) * 100 for r in ratios]

ax1.plot(ratios, ils, 'b-', linewidth=2.5)
ax1.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax1.axvline(x=1, color='green', linestyle='--', linewidth=1, label='No price change')

# Mark specific points
markers = [(0.5, 'r'), (2.0, 'r'), (0.75, 'orange'), (1.5, 'orange')]
for ratio, color in markers:
    il = impermanent_loss(ratio) * 100
    ax1.plot(ratio, il, 'o', color=color, markersize=10)
    ax1.annotate(f'{ratio}x: {il:.1f}%', xy=(ratio, il),
                xytext=(10, 10), textcoords='offset points', fontsize=9)

ax1.set_xlabel('Price Ratio (Final / Initial)')
ax1.set_ylabel('Impermanent Loss (%)')
ax1.set_title('Impermanent Loss vs. Price Movement')
ax1.legend()
ax1.grid(alpha=0.3)
ax1.set_xscale('log')
ax1.set_xticks([0.25, 0.5, 1, 2, 4])
ax1.set_xticklabels(['0.25x', '0.5x', '1x', '2x', '4x'])

# Plot 2: LP vs Hold Value
ax2 = axes[0, 1]
ratios_lin = np.linspace(0.2, 3, 200)
lp_vals = [portfolio_values(10000, r)[0] for r in ratios_lin]
hold_vals = [portfolio_values(10000, r)[1] for r in ratios_lin]

ax2.plot(ratios_lin, lp_vals, 'b-', linewidth=2, label='LP Position')
ax2.plot(ratios_lin, hold_vals, 'g--', linewidth=2, label='Hold Strategy')
ax2.fill_between(ratios_lin, lp_vals, hold_vals,
                 where=[l < h for l, h in zip(lp_vals, hold_vals)],
                 alpha=0.3, color='red', label='IL Zone')

ax2.axvline(x=1, color='black', linestyle=':', alpha=0.5)
ax2.set_xlabel('Price Ratio (Final / Initial)')
ax2.set_ylabel('Portfolio Value ($)')
ax2.set_title('LP Position vs. Hold Strategy')
ax2.legend()
ax2.grid(alpha=0.3)

# Plot 3: Breakeven Fee APY
ax3 = axes[1, 0]
price_moves = [abs(1 - r['ratio']) * 100 for r in results if r['ratio'] != 1.0]
ils_needed = [abs(r['il']) * 100 for r in results if r['ratio'] != 1.0]

ax3.bar(range(len(ils_needed)), ils_needed, color='coral', alpha=0.7)
ax3.axhline(y=5, color='blue', linestyle='--', linewidth=2, label='Typical 0.3% pool APY (~5%)')
ax3.axhline(y=2, color='green', linestyle='--', linewidth=2, label='Typical 0.05% pool APY (~2%)')

labels = ['0.5x', '0.75x', '1.25x', '1.5x', '2x', '3x', '5x']
ax3.set_xticks(range(len(labels)))
ax3.set_xticklabels(labels)
ax3.set_xlabel('Price Movement')
ax3.set_ylabel('Fee APY Needed to Break Even (%)')
ax3.set_title('Required Fee APY to Offset Impermanent Loss')
ax3.legend()
ax3.grid(axis='y', alpha=0.3)

# Plot 4: Decision Heatmap
ax4 = axes[1, 1]

# Create decision matrix
fee_apys = [1, 2, 5, 10, 20]
price_movements = [1.1, 1.25, 1.5, 2.0, 3.0]

decision_matrix = np.zeros((len(fee_apys), len(price_movements)))

for i, fee in enumerate(fee_apys):
    for j, price in enumerate(price_movements):
        il = abs(impermanent_loss(price)) * 100
        # Net profit = fee APY - IL
        decision_matrix[i, j] = fee - il

im = ax4.imshow(decision_matrix, cmap='RdYlGn', aspect='auto', vmin=-20, vmax=20)

ax4.set_xticks(range(len(price_movements)))
ax4.set_xticklabels([f'{p}x' for p in price_movements])
ax4.set_yticks(range(len(fee_apys)))
ax4.set_yticklabels([f'{f}%' for f in fee_apys])
ax4.set_xlabel('Price Movement')
ax4.set_ylabel('Fee APY')
ax4.set_title('LP Profit/Loss Matrix (Fee APY - IL)')

# Add value annotations
for i in range(len(fee_apys)):
    for j in range(len(price_movements)):
        val = decision_matrix[i, j]
        color = 'white' if abs(val) > 10 else 'black'
        ax4.text(j, i, f'{val:+.1f}%', ha='center', va='center', color=color, fontsize=9)

plt.colorbar(im, ax=ax4, label='Net Profit (%)')

plt.tight_layout()
plt.savefig('impermanent_loss_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nChart saved as 'impermanent_loss_analysis.png'")
```

### Model Answer / Expected Output

**Key Numerical Results:**

| Price Change | IL | LP Value | Hold Value | Dollar Loss on $10k |
|--------------|-----|----------|------------|---------------------|
| 0.5x (50% down) | -5.72% | $7,071.07 | $7,500.00 | $428.93 |
| 0.75x (25% down) | -1.03% | $8,660.25 | $8,750.00 | $89.75 |
| 1.25x (25% up) | -0.62% | $11,180.34 | $11,250.00 | $69.66 |
| 1.5x (50% up) | -2.02% | $12,247.45 | $12,500.00 | $252.55 |
| 2x (100% up) | -5.72% | $14,142.14 | $15,000.00 | $857.86 |
| 3x (200% up) | -13.40% | $17,320.51 | $20,000.00 | $2,679.49 |
| 5x (400% up) | -25.46% | $22,360.68 | $30,000.00 | $7,639.32 |

**Calculation method:**
- hold_value = 10000 * (1 + r) / 2
- lp_value = 10000 * sqrt(r)
- dollar_loss = hold_value - lp_value

**Decision Framework:**
- If expected price movement < 25%: LP is usually profitable with standard 0.3% fee pools
- If expected price movement 25-50%: Need higher fee tier or liquidity mining rewards
- If expected price movement > 50%: LP is likely unprofitable - just hold

### Presentation Talking Points
- Impermanent loss is "impermanent" only if prices return to initial ratio - otherwise it's very permanent
- IL is symmetric: 2x up and 0.5x down have identical IL because the AMM rebalances the same way
- The key economic insight: LPs are selling options on price divergence - IL is the option premium they pay
- Most retail LPs lose money because they underestimate IL and overestimate fee income
- Professional LPs use concentrated liquidity (Uniswap v3) and active management to mitigate IL

---

## Exercise 3: CEX vs DEX Battle Matrix

**Category**: Framework Application
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Printed worksheet, pens

> **Key Terms**
>
> - **Centralized exchange (CEX)**: A traditional exchange (e.g., Binance, Coinbase) that uses an order book, holds custody of user assets, and requires KYC. Offers fast execution and deep liquidity.
> - **Decentralized exchange (DEX)**: A blockchain-based exchange (e.g., Uniswap, Curve) that uses smart contracts for trading. Non-custodial, permissionless, and transparent but subject to gas fees and MEV.
> - **Custody risk**: The risk that a centralized entity holding your assets becomes insolvent, is hacked, or freezes your account (e.g., FTX collapse in 2022).
> - **Capital efficiency**: How effectively capital is deployed to provide liquidity. Order books concentrate capital at active price levels; AMM v2 spreads capital across all prices.
> - **Composability**: The ability of DeFi protocols to interact with each other programmatically (e.g., flash loans, yield aggregators).

### Task

Create a comprehensive comparison matrix evaluating Centralized Exchanges (CEXs) vs. Decentralized Exchanges (DEXs) across six key dimensions. Reach group consensus on ratings and identify the optimal exchange type for different user profiles.

**Dimensions to Compare:**
1. Speed (execution, settlement)
2. Cost (fees, slippage)
3. Custody (who holds assets)
4. Transparency (order flow, pricing)
5. Accessibility (KYC, geography)
6. Capital Efficiency (for liquidity providers)

**Rating Scale:** 1-5 (5 = excellent, 1 = poor)

### Model Answer / Expected Output

**Completed Comparison Matrix:**

| Dimension | CEX (e.g., Binance) | DEX (e.g., Uniswap) | Winner | Justification |
|-----------|---------------------|---------------------|--------|---------------|
| **Speed** | **5** | **3** | CEX | CEX: millisecond execution, instant settlement to exchange wallet. DEX: 12-second block times (Ethereum), potential mempool delays, MEV extraction slows effective execution |
| **Cost** | **4** | **3** | CEX | CEX: 0.1% maker/taker, no gas fees. DEX: 0.3% swap fee + $5-50 gas (Ethereum), MEV extraction can add 1-5% implicit cost. DEX wins on very small trades with L2s |
| **Custody** | **2** | **5** | DEX | CEX: Exchange holds your assets (counterparty risk - see FTX). DEX: Non-custodial, you control keys, smart contract risk only |
| **Transparency** | **2** | **5** | DEX | CEX: Order flow opaque, potential front-running, wash trading concerns. DEX: All trades on-chain, verifiable, open-source smart contracts |
| **Accessibility** | **2** | **5** | DEX | CEX: KYC required, geographic restrictions, account bans possible. DEX: Permissionless, no KYC, anyone with wallet can trade |
| **Capital Efficiency** | **5** | **2** | CEX | CEX: Professional market makers use leverage, concentrated positions. DEX: Constant product requires 2x capital vs. actual trading range (v3 improves this) |

**Overall Scores:**
- CEX: 20/30
- DEX: 23/30

**User Profile Recommendations:**

| User Profile | Recommended | Reasoning |
|--------------|-------------|-----------|
| Day trader, large volume | **CEX** | Speed and cost matter most; can tolerate custody risk with good security practices |
| Long-term holder, privacy-conscious | **DEX** | Custody and accessibility matter most; doesn't need speed |
| Institutional investor | **CEX** | Needs capital efficiency, regulatory compliance, customer support |
| Resident of sanctioned country | **DEX** | Only option - CEXs won't serve them |
| DeFi yield farmer | **DEX** | Composability with other DeFi protocols, no withdrawal delays |
| New crypto user | **CEX** | Better UX, fiat on-ramps, customer support |

**Key Trade-off Insight:**

The CEX vs. DEX choice fundamentally trades off **efficiency** (speed, cost, capital efficiency) against **decentralization** (custody, transparency, accessibility). There is no universally superior option - it depends on what the user values most.

### Presentation Talking Points
- CEXs excel at efficiency metrics (speed, cost, capital efficiency) because centralization enables optimization
- DEXs excel at decentralization metrics (custody, transparency, accessibility) because that's their design goal
- The FTX collapse (2022) dramatically shifted sentiment toward DEX custody benefits
- Capital efficiency is DEXs' biggest weakness - Uniswap v3's concentrated liquidity is an attempt to close this gap
- Economic insight: This mirrors the classic centralization vs. decentralization trade-off seen throughout economics (planned economies vs. markets, big firms vs. small firms)

---

## Exercise 4: Sandwich Attack Anatomy

**Category**: Case Study
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Case data handout, calculators

> **Key Terms**
>
> - **Sandwich attack**: An MEV strategy where an attacker places a buy order before (front-run) and a sell order after (back-run) a victim's trade, profiting from the price movement caused by the victim's trade.
> - **Front-running**: Submitting a transaction ahead of a known pending transaction to profit from the anticipated price movement.
> - **Slippage tolerance**: The maximum price deviation a trader is willing to accept. Setting 1% slippage means accepting any price up to 1% worse than the quoted price.
> - **Mempool**: The queue of pending transactions waiting to be included in a block. On public blockchains, anyone can observe the mempool and see pending trades.
> - **MEV (Maximal Extractable Value)**: The profit that block producers or searchers can extract by reordering, inserting, or censoring transactions within blocks.

### Task

Analyze a real sandwich attack transaction and calculate the exact profit extraction. Identify who wins, who loses, and whether this is "theft" or "market efficiency."

**Case Data: Actual Sandwich Attack (Simplified)**

**Initial Pool State (ETH/USDC on Uniswap v2):**
- ETH Reserve: 10,000 ETH
- USDC Reserve: 18,000,000 USDC
- k = 180,000,000,000
- Spot Price: $1,800/ETH

**Victim Transaction:**
- Victim wants to buy 50 ETH
- Victim's slippage tolerance: 1%
- Victim's maximum acceptable price: $1,818/ETH

**Attacker's Strategy:**
- Front-run: Buy ETH before victim
- Back-run: Sell ETH after victim
- Gas cost per transaction: $20

**Questions to Answer:**
1. Calculate the optimal front-run size
2. What price does the victim actually pay?
3. What is the attacker's profit?
4. What is the victim's loss vs. a non-attacked scenario?
5. Is this "theft" or "market efficiency"?

### Model Answer / Expected Output

**Step 1: Feasible Front-Run Calculation**

The attacker must keep the victim's effective price within slippage tolerance ($1,818/ETH). A front-run of f = 24 ETH satisfies this constraint (the slippage math yields a maximum near 24 ETH before the victim's execution price exceeds $1,818).

**Front-run size: 24 ETH**

**Step 2: Transaction Sequence Calculations (all using x*y = k = 180,000,000,000)**

**Initial State:**
- x0 = 10,000 ETH, y0 = 18,000,000 USDC
- Price = y0/x0 = $1,800.00/ETH

**After Front-Run (Attacker buys 24 ETH):**
The attacker adds USDC to the pool and removes 24 ETH.
```
x1 = 10,000 - 24 = 9,976 ETH
y1 = k / x1 = 180,000,000,000 / 9,976 = 18,043,305.93 USDC
USDC paid by attacker = y1 - y0 = 18,043,305.93 - 18,000,000 = $43,305.93
New price = y1 / x1 = 18,043,305.93 / 9,976 = $1,808.66/ETH
```

**After Victim Trade (Victim buys 50 ETH):**
```
x2 = 9,976 - 50 = 9,926 ETH
y2 = k / x2 = 180,000,000,000 / 9,926 = 18,134,224.96 USDC
USDC paid by victim = y2 - y1 = 18,134,224.96 - 18,043,305.93 = $90,919.03
Victim's effective price = $90,919.03 / 50 = $1,818.38/ETH
New price = y2 / x2 = 18,134,224.96 / 9,926 = $1,827.02/ETH
```

The victim's effective price ($1,818.38) is within the 1% slippage tolerance ($1,818).

**After Back-Run (Attacker sells 24 ETH):**
```
x3 = 9,926 + 24 = 9,950 ETH
y3 = k / x3 = 180,000,000,000 / 9,950 = 18,090,452.26 USDC
USDC received by attacker = y2 - y3 = 18,134,224.96 - 18,090,452.26 = $43,772.70
```

**Step 3: Profit/Loss Calculation**

**Attacker:**
- USDC spent (front-run): $43,305.93
- USDC received (back-run): $43,772.70
- Gross profit: $43,772.70 - $43,305.93 = **$466.77**
- Gas costs: $50 (2 transactions)
- **Net profit: $416.77**

**Victim:**
- Price paid: $1,818.38/ETH (effective, for 50 ETH)
- Price without attack: $1,809.05/ETH (50 ETH from initial pool: k/(10000-50) = 18,090,452.26; cost = 90,452.26; eff = 90,452.26/50)
- Overpayment per ETH: $1,818.38 - $1,809.05 = $9.33
- Total overpayment: $9.33 x 50 = **$466.77 loss**

**Verification:** Attacker gross profit ($466.77) = Victim overpayment ($466.77). This is exactly zero-sum before gas. After gas ($50), the attacker nets $416.77 and $50 goes to validators.

**Step 4: Is This "Theft" or "Market Efficiency"?**

| Argument: "This is Theft" | Argument: "This is Market Efficiency" |
|---------------------------|---------------------------------------|
| Victim did not consent to worse price | Victim set 1% slippage tolerance - they consented to any price up to $1,818 |
| Attacker adds no value, pure extraction | Arbitrageurs provide price discovery by linking mempool info to prices faster |
| Uses information asymmetry (sees pending tx) | All traders should monitor mempool - it's public information |
| Analogous to front-running in TradFi (illegal) | DeFi has different rules - code is law |
| Transfers wealth from uninformed to informed | Markets have always rewarded informed participants |

**Consensus View:**
- **Economically**: It's a wealth transfer from those who don't optimize (set tight slippage, use MEV protection) to those who do
- **Ethically**: Most would consider it unfair, but it's not "illegal" in a permissionless system
- **Practically**: It creates an arms race that wastes resources (gas wars) and degrades user experience

### Presentation Talking Points
- Sandwich attacks are possible because the mempool is PUBLIC - everyone can see pending transactions
- The attack is precisely calibrated to the victim's slippage tolerance (this is why tight slippage matters)
- Total value extracted: ~$467 on a ~$91k trade = ~0.5% implicit cost on top of the 0.3% AMM fee
- MEV is estimated at $600M+ extracted from Ethereum users since 2020
- Solutions being developed: private mempools (Flashbots Protect), MEV auctions, encrypted transactions
- Economic insight: MEV is an "invisible tax" on DeFi users that flows to searchers and validators

---

## Exercise 5: MEV Ethics Debate

**Category**: Debate/Discussion
**Time**: 30 min work + 5 min presentation
**Group Size**: Two teams of 4-6 students each
**Materials Needed**: None (timer helpful)

> **Key Terms**
>
> - **MEV (Maximal Extractable Value)**: Profit extracted by reordering, inserting, or censoring transactions within blocks. Includes sandwich attacks, arbitrage, and liquidations.
> - **Adverse selection**: The risk that a market maker trades against a better-informed counterparty. In DeFi, MEV searchers are the "informed" traders who exploit less-informed users.
> - **Deadweight loss**: Economic value destroyed (not transferred) in a transaction. Gas wars between competing MEV searchers are a deadweight loss.
> - **MEV supply chain**: The chain of actors involved in MEV extraction: searchers (find opportunities), builders (construct blocks), and validators (propose blocks). Value flows from users through this supply chain.
> - **Information asymmetry**: When one party in a transaction has more or better information than the other. MEV searchers have superior mempool monitoring and compute power.

### Task

Structured debate on the motion: **"MEV extraction is economically equivalent to theft and should be eliminated through protocol design."**

**Team A (Pro)**: MEV is theft and should be eliminated
**Team B (Con)**: MEV improves market efficiency and is a feature, not a bug

**Debate Structure:**
| Phase | Time | Activity |
|-------|------|----------|
| Preparation | 15 min | Teams prepare 3 main arguments using L06 concepts |
| Opening | 3 min each | Each team presents main arguments |
| Rebuttal Prep | 5 min | Teams prepare responses |
| Rebuttals | 2 min each | Each team responds to opponent |
| Closing | 1 min each | Final summary |

**Required L06 Concepts**: Use at least 2 per team from:
- Price discovery
- MEV supply chain
- Adverse selection
- Transaction costs
- Welfare economics (Pareto efficiency)
- Information asymmetry

### Model Answer / Expected Output

**Team A (Pro - MEV is Theft):**

**Argument 1: Information Asymmetry Creates Unfair Advantage**
- L06 Concept: *Information asymmetry and adverse selection*
- MEV extractors have privileged access to pending transaction information (mempool visibility + compute power)
- This is exactly the "adverse selection" problem from Glosten-Milgrom (1985) - informed traders profit at expense of uninformed
- Traditional finance BANS front-running for this reason (it's illegal under SEC Rule 10b-5)
- Analogy: It's like a casino employee who can see other players' cards - the game is rigged

**Argument 2: MEV is a Deadweight Loss, Not Value Creation**
- L06 Concept: *Welfare economics and Pareto efficiency*
- MEV extraction is NOT Pareto-improving - victims are strictly worse off
- Resources wasted: Gas wars between competing searchers burn billions in fees
- Zero-sum (or negative-sum): Total value extracted = victim losses + wasted gas
- Compare to productive trading: Arbitrage that MOVES prices toward efficiency creates value; sandwiching does not

**Argument 3: MEV Undermines Trust and Adoption**
- L06 Concept: *Transaction costs*
- MEV adds hidden transaction costs (5-10% on some trades per L06 slides)
- Users don't understand they're being exploited - this undermines informed consent
- Long-term: Rational users will avoid DeFi, reducing liquidity and welfare
- Comparison: Would you shop at a store where employees can legally pickpocket you?

**Rebuttal Points Against Con:**
- "Arbitrage provides price discovery" - Sandwich attacks don't move prices toward fundamental value
- "Mempool is public" - Just because something is visible doesn't mean exploiting it is ethical
- "Users can protect themselves" - This is victim-blaming; most users don't have technical knowledge

---

**Team B (Con - MEV is Market Efficiency):**

**Argument 1: MEV is Information-Based Trading (Legal and Normal)**
- L06 Concept: *MEV supply chain and price discovery*
- Efficient markets incorporate ALL available information quickly
- Mempool information is PUBLIC - anyone can read it (not insider info)
- MEV searchers are performing a service: rapidly incorporating order flow information into prices
- Kyle (1985) model shows informed trading is essential for price discovery

**Argument 2: MEV Extracts Only the "Slack" Users Voluntarily Provided**
- L06 Concept: *Transaction costs and slippage tolerance*
- Users set their own slippage tolerance - they CONSENT to any price within that range
- If victim sets 5% slippage, they're saying "I'm willing to pay up to 5% more"
- MEV extracts exactly this declared willingness to pay - it's revealed preference
- Solution is user education, not protocol-level bans

**Argument 3: Eliminating MEV Centralizes Power**
- L06 Concept: *Information asymmetry and market microstructure*
- Encrypted mempools and private order flow = CENTRALIZATION
- Someone still sees the orders (the encryptor, the sequencer) - just hidden from public
- Current system is transparent: all MEV is visible on-chain
- "Elimination" really means "capture by privileged parties" (validators, sequencers)

**Rebuttal Points Against Pro:**
- "Front-running is illegal in TradFi" - DeFi operates under different rules; code is law
- "Deadweight loss" - Gas costs fund network security; not purely wasted
- "Users don't understand" - That's an education problem, not a protocol problem

---

**Balanced Verdict (for instructor):**

The strongest economic position is nuanced:

1. **Arbitrage MEV** (e.g., DEX-CEX arb) is genuinely efficiency-enhancing - it aligns prices across venues
2. **Sandwich MEV** is pure extraction - it adds no information and transfers wealth from uninformed to informed
3. **Liquidation MEV** is necessary for DeFi to function - someone must liquidate underwater positions

The debate should conclude that **not all MEV is equal** - some is valuable, some is extractive. The protocol design challenge is enabling good MEV while minimizing bad MEV.

### Presentation Talking Points
- Both teams should distinguish between types of MEV (arbitrage vs. sandwich vs. liquidation)
- The core tension: transparency (public mempool) vs. fairness (first-come-first-served)
- Historical parallel: This debate echoes the HFT controversy in traditional markets
- No blockchain has "solved" MEV - Ethereum's Flashbots is mitigation, not elimination
- Key economic insight: MEV is the "cost of decentralization" - centralized systems can prevent it but sacrifice trustlessness

---

## Exercise 6: Design an MEV-Resistant AMM

**Category**: Creative/Design
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Whiteboard, flip chart, or paper; colored markers

> **Key Terms**
>
> - **Commit-reveal scheme**: A two-phase protocol where users first submit an encrypted commitment (hash of their order), then reveal the actual order in a later phase. Prevents front-running because orders are hidden during the commit phase.
> - **Batch auction**: A trading mechanism where multiple orders are collected over a time window and executed simultaneously at a single clearing price. Eliminates ordering advantages.
> - **JIT (just-in-time) liquidity**: A strategy where LPs add liquidity just before a large trade and remove it immediately after, capturing fees without long-term IL exposure. Considered a form of MEV.
> - **Incentive compatibility**: A mechanism is incentive-compatible if participants maximize their payoff by acting honestly. Good MEV-resistant designs make manipulation unprofitable.
> - **Encrypted mempool**: A mempool where pending transactions are encrypted so that no one (including validators) can see order details until they are committed to a block.

### Task

Your team is designing the next generation AMM that minimizes MEV extraction while maintaining liquidity and usability. Create a detailed mechanism design that addresses sandwich attacks, front-running, and arbitrage extraction.

**Design Requirements:**
1. Must maintain constant liquidity (can't just "pause trading during attacks")
2. Must be economically sustainable (LPs need to earn fees)
3. Must be implementable on a blockchain (can't require trusted third parties)
4. Must clearly explain the trade-offs

**Evaluation Criteria:**
- Creativity of mechanism
- Economic soundness (incentive compatibility)
- Practical implementability
- Honest assessment of trade-offs

### Model Answer / Expected Output

**Model Design Brief: "TimeShield AMM"**

---

**MECHANISM NAME:** TimeShield AMM

**CORE INNOVATION:** Time-Weighted Batch Auctions with Commit-Reveal

---

**HOW IT WORKS:**

**Phase 1: COMMIT (Block N)**
- Traders submit encrypted order commitments: `commit = hash(order_details + secret)`
- No one (including validators) can see order details
- Commit fee: small fixed fee to prevent spam

**Phase 2: REVEAL (Block N+1)**
- Traders reveal their orders by submitting `order_details + secret`
- Orders that don't match their commit are rejected
- All orders in the batch are now visible

**Phase 3: EXECUTE (Block N+2)**
- All orders execute at a SINGLE clearing price
- Price determined by: weighted average of where supply = demand
- No ordering advantage - all trades in batch treated equally

---

**MATHEMATICAL FORMULATION:**

**Single Clearing Price:**
```
P* = argmin[ |sum(buy_orders at P) - sum(sell_orders at P)| ]
```

All buys execute at P*, all sells execute at P*.

**Batch Interval:** 3 blocks (~36 seconds on Ethereum)

---

**WHY THIS DEFEATS MEV:**

| Attack Type | How TimeShield Blocks It |
|-------------|--------------------------|
| **Front-running** | Attacker can't see orders during commit phase; by reveal phase, attacker's commit deadline has passed |
| **Sandwich** | No ordering within batch - everyone gets same price; can't buy before and sell after victim |
| **JIT Liquidity** | Liquidity commits must also be batched; can't add/remove liquidity between seeing order and execution |

---

**TRADE-OFFS (HONEST ASSESSMENT):**

| Benefit | Cost |
|---------|------|
| No sandwich attacks | 36-second execution delay (vs. 12 seconds on Uniswap) |
| Fair pricing | More complex UX (commit + reveal) |
| LP protection | Lower capital efficiency (price uncertainty during batch) |
| MEV goes to traders | Arbitrage now batch-delayed (prices can drift from CEX) |

---

**INCENTIVE ANALYSIS:**

**For Traders:**
- Benefit: No MEV extraction (save 1-5% on large trades)
- Cost: Slower execution, price uncertainty during batch
- Net: Positive for large traders, negative for time-sensitive traders

**For LPs:**
- Benefit: No JIT liquidity stealing their fees, no IL from MEV
- Cost: Less fee income per trade (no MEV premium)
- Net: Probably positive - more sustainable, less adversarial

**For Arbitrageurs:**
- Can still arbitrage, but batched - must predict clearing price
- Reduces pure speed advantage, increases prediction skill advantage
- Some arbitrage still happens (good for price discovery)

---

**IMPLEMENTABILITY:**

| Component | Implementation |
|-----------|----------------|
| Commit-reveal | Standard cryptographic scheme (already used in ENS) |
| Batch auctions | Implemented by CoW Protocol (Gnosis), CrocSwap |
| Clearing price | Requires on-chain computation (expensive but feasible) |
| Smart contract | ~500 lines of Solidity, auditable |

**Existing Protocols Using Similar Ideas:**
- CowSwap: Batch auctions with off-chain solvers
- Chainlink Fair Sequencing Services: Encrypted mempools
- Flashbots Protect: Private transaction submission

---

**EXPECTED RESULTS:**

| Metric | Uniswap v2 | TimeShield (Projected) |
|--------|------------|------------------------|
| MEV extracted | 1-5% of large trades | ~0% |
| Execution time | 12 seconds | 36 seconds |
| Gas per trade | ~150k | ~200k (extra commit tx) |
| LP profitability | Often negative (IL + MEV) | More sustainable |

---

### Presentation Talking Points
- There is no perfect MEV solution - all designs involve trade-offs
- The core insight: MEV exists because of ORDERING - remove ordering, remove MEV
- Batch auctions are the economist's favorite solution (used in stock market opens/closes)
- Challenge: DeFi users want instant execution, not 36-second delays
- Practical implementations exist (CowSwap, Flashbots Protect) - this isn't just theory
- Key economic insight: The "price" of MEV protection is execution delay and complexity

---

## Exercise 7: LP Profitability Analysis

**Category**: Quantitative Analysis
**Time**: 30 min work + 5 min presentation
**Group Size**: Pairs
**Materials Needed**: Calculator or spreadsheet

> **Key Terms**
>
> - **TVL (Total Value Locked)**: The total dollar value of assets deposited in a DeFi protocol or liquidity pool. Higher TVL generally means lower slippage for traders.
> - **Fee tier**: The percentage fee charged on each swap. Uniswap v3 offers 0.01%, 0.05%, 0.3%, and 1% tiers. Higher tiers compensate LPs for greater IL risk.
> - **Pool share**: Your proportion of the total pool. Determines what fraction of trading fees you earn. Pool share = your_deposit / pool_TVL.
> - **Impermanent loss (IL)**: See Exercise 2. The opportunity cost of LP vs. holding. Must be offset by fee income for LP to be profitable.
> - **Annualized APY**: The annual return rate. Calculated as (daily_return * 365) for simple annualization. Actual returns may vary significantly from this projection.

### Task

Analyze whether being a liquidity provider in a specific pool is profitable, comparing LP returns against simply holding the assets ("hodling"). Use real fee and volume data to make a recommendation.

**Pool Data (ETH/USDC on Uniswap v3):**
- Pool TVL: $100,000,000
- Daily volume: $50,000,000
- Fee tier: 0.3%
- Your position: $10,000 (50% ETH at $1,800, 50% USDC)
- Time horizon: 30 days
- Expected ETH price scenarios: -20%, 0%, +20%, +50%

**Calculate for each scenario:**
1. Fee income earned (assume your share of pool is proportional)
2. Impermanent loss (if any)
3. Net profit/loss vs. holding
4. Equivalent APY

### Model Answer / Expected Output

**Step 1: Fee Income Calculation**

```
Daily fees generated by pool = $50,000,000 * 0.003 = $150,000
Your pool share = $10,000 / $100,000,000 = 0.01%
Your daily fee income = $150,000 * 0.0001 = $15
Your 30-day fee income = $15 * 30 = $450
Fee APY = ($15 * 365) / $10,000 = 54.75%
```

> **Important caveat on fee APY:** The 54.75% fee APY in this example reflects an exceptionally high-volume pool (daily volume = 50% of TVL). In practice, most Uniswap v3 pools earn **5-15% APY** from fees. The ETH/USDC 0.3% pool on mainnet typically has a volume/TVL ratio of 10-20%, not 50%. This exercise uses a high ratio for pedagogical clarity, but students should not expect these returns in real pools. Always check the actual volume/TVL ratio before providing liquidity.

**Step 2: Impermanent Loss for Each Scenario**

| ETH Price Change | Price Ratio | IL Formula | IL % | IL $ |
|------------------|-------------|------------|------|------|
| -20% ($1,440) | 0.80 | 2*sqrt(0.8)/(1+0.8)-1 | -0.62% | -$62 |
| 0% ($1,800) | 1.00 | 0 | 0% | $0 |
| +20% ($2,160) | 1.20 | 2*sqrt(1.2)/(1+1.2)-1 | -0.46% | -$46 |
| +50% ($2,700) | 1.50 | 2*sqrt(1.5)/(1+1.5)-1 | -2.02% | -$202 |

**Step 3: Net Profit/Loss vs. Holding**

| Scenario | Fee Income | IL | Net vs Hold | Verdict |
|----------|------------|-----|-------------|---------|
| -20% | +$450 | -$62 | **+$388** | LP WINS |
| 0% | +$450 | $0 | **+$450** | LP WINS |
| +20% | +$450 | -$46 | **+$404** | LP WINS |
| +50% | +$450 | -$202 | **+$248** | LP WINS |

**Step 4: Equivalent APY Comparison**

| Scenario | LP 30-Day Return | LP Annualized APY | Hold 30-Day Return | Hold Annualized |
|----------|------------------|-------------------|--------------------| --------------- |
| -20% | +$388 (3.88%) | 47.3% APY | -$1,000 (-10%) | -120% |
| 0% | +$450 (4.50%) | 54.8% APY | $0 (0%) | 0% |
| +20% | +$404 (4.04%) | 49.2% APY | +$1,000 (+10%) | +122% |
| +50% | +$248 (2.48%) | 30.2% APY | +$2,500 (+25%) | +304% |

**Step 5: Recommendation**

**RECOMMENDATION: LP is profitable in all scenarios due to high fee APY (54.75%)**

However, important caveats:
1. In the +50% scenario, HOLDING outperforms LP ($2,500 vs $248) in absolute terms
2. The fee APY assumes consistent volume - volume can drop significantly
3. This analysis ignores gas costs for entering/exiting (~$50-100)
4. This analysis ignores smart contract risk
5. **Most real pools earn 5-15% APY, not 54.75%** - this example uses an unusually high-volume pool

**When LP beats Hold:**
- Sideways markets (low IL, full fee capture)
- High volume pools (high fee APY)
- Low volatility assets (stablecoin pairs)

**When Hold beats LP:**
- Strong directional moves (high IL erodes gains)
- Low volume periods (fee income drops)
- Very volatile assets (IL can exceed fees)

### Presentation Talking Points
- The key metric is: Fee APY vs. Expected IL - in this pool, 54.75% fee APY easily covers IL up to ~50% price moves
- Most LP analysis ignores that fee income is NOT guaranteed - volume fluctuates
- This pool has unusually high volume/TVL ratio (50%) - most pools have 10-20%, yielding 5-15% APY
- Real LPs also face: gas costs, smart contract risk, opportunity cost
- The comparison baseline matters: LP vs. Hold vs. stable yield (e.g., 5% on USDC)
- Key economic insight: LP profitability is pool-specific - high volume pools can be very profitable, low volume pools are often not

---

## Exercise 8: Order Book vs AMM Trade Execution

**Category**: Comparative Analysis
**Time**: 30 min work + 5 min presentation
**Group Size**: Groups of 3-4
**Materials Needed**: Worksheet with order book data, calculators

> **Key Terms**
>
> - **Order book**: A list of buy (bid) and sell (ask) orders at different price levels. Trades execute by matching the best available bid with the best available ask. Used by CEXs like Binance.
> - **Market order**: An order to buy or sell immediately at the best available price. Guarantees execution but not price.
> - **Price impact**: The difference between the expected price and the actual execution price caused by consuming liquidity from the order book or moving along the AMM curve.
> - **Maker/taker fees**: Order book exchanges charge fees for providing liquidity (maker, typically lower) and consuming liquidity (taker, typically higher). Common rates: 0.1% for both.
> - **Depth**: The total quantity of orders available at each price level. Deeper order books have more liquidity and lower price impact for large trades.

### Task

Compare trade execution quality between an order book (Binance) and an AMM (Uniswap) for different trade sizes. Determine which venue is better for retail vs. institutional traders.

**Order Book Data (Binance ETH/USDC):**
| Price Level | Bid Quantity | Ask Quantity |
|-------------|--------------|--------------|
| $1,799 | 100 ETH | - |
| $1,800 | 200 ETH | - |
| $1,801 | - | 150 ETH |
| $1,802 | - | 200 ETH |
| $1,805 | - | 500 ETH |

Mid price: $1,800.50, Spread: $1 (0.056%)

**AMM Data (Uniswap ETH/USDC):**
- ETH Reserve: 50,000 ETH
- USDC Reserve: 90,000,000 USDC
- k = 4,500,000,000,000
- Spot price: $1,800
- Fee: 0.3%

**Calculate for trade sizes: 1 ETH, 10 ETH, 100 ETH, 500 ETH:**
1. Execution price on each venue
2. Total cost (including fees/spread)
3. Which venue is better?

**Note:** For a fair comparison, this exercise focuses on **price impact and AMM fees** but excludes order book trading fees. If you want to include order book fees (typically 0.1% taker), add them to the order book totals for a complete comparison.

### Model Answer / Expected Output

**Order Book Execution Analysis:**

**Buy 1 ETH:**
- Fills at best ask: $1,801
- Total cost: $1,801
- Slippage: 0%

**Buy 10 ETH:**
- Fills at best ask: $1,801 (10 ETH available at this level)
- Total cost: $18,010
- Effective price: $1,801
- Slippage: 0%

**Buy 100 ETH:**
- 150 ETH at $1,801, fills 100 at $1,801
- Total cost: $180,100
- Effective price: $1,801
- Slippage: 0%

**Buy 500 ETH:**
- 150 at $1,801 = $270,150
- 200 at $1,802 = $360,400
- 150 at $1,805 = $270,750
- Total: $901,300
- Effective price: $1,802.60
- Slippage: 0.14%

---

**AMM Execution Analysis:**

For a buy of `dx` ETH:
- New ETH reserve: x - dx
- New USDC reserve: k / (x - dx)
- USDC cost: new_USDC - old_USDC
- Plus 0.3% fee

**Buy 1 ETH:**
- Raw USDC cost = k/(50000-1) - 90,000,000 = $1,800.04
- Price impact (slippage): (1,800.04 - 1,800) / 1,800 = 0.002%
- Fee: $1,800.04 * 0.003 = $5.40
- Total: $1,805.44

**Buy 10 ETH:**
- Raw USDC cost = k/(50000-10) - 90,000,000 = $18,003.60
- Price impact (slippage): effective raw price $1,800.36 vs spot $1,800 = 0.02%
- Fee: $18,003.60 * 0.003 = $54.01
- Total: $18,057.61
- Effective price: $1,805.76

**Buy 100 ETH:**
- Raw USDC cost = k/(50000-100) - 90,000,000 = $180,360.72
- Price impact (slippage): effective raw price $1,803.61 vs spot $1,800 = 0.20%
- Fee: $180,360.72 * 0.003 = $541.08
- Total: $180,901.80
- Effective price: $1,809.02

**Buy 500 ETH:**
- Raw USDC cost = k/(50000-500) - 90,000,000 = $909,090.91
- Price impact (slippage): effective raw price $1,818.18 vs spot $1,800 = 1.01%
- Fee: $909,090.91 * 0.003 = $2,727.27
- Total: $911,818.18
- Effective price: $1,823.64

---

**Comparison Summary:**

| Trade Size | Order Book Total | AMM Total | Better Venue | Savings |
|------------|------------------|-----------|--------------|---------|
| 1 ETH | $1,801 | $1,805.44 | **Order Book** | $4.44 (0.25%) |
| 10 ETH | $18,010 | $18,057.61 | **Order Book** | $47.61 (0.26%) |
| 100 ETH | $180,100 | $180,901.80 | **Order Book** | $801.80 (0.44%) |
| 500 ETH | $901,300 | $911,818.18 | **Order Book** | $10,518 (1.17%) |

**Winner: Order Book (Binance) for ALL trade sizes**

---

**Why Order Book Wins:**

1. **Spread is tighter**: Order book spread of $1 (0.056%) beats AMM's 0.3% fee
2. **Depth at specific prices**: Order book has concentrated liquidity at best prices
3. **Slippage scales better**: Order book slippage is step-function (hits price levels), AMM is continuous curve

**When AMM Might Win:**

| Scenario | Why AMM Could Be Better |
|----------|-------------------------|
| Exotic pairs | Order book may have no depth for obscure tokens |
| Non-custodial | Don't want to trust Binance with funds |
| 24/7 liquidity | Order book depth thin overnight/weekends |
| Composability | Need on-chain execution for DeFi strategies |
| Censorship resistance | Binance can freeze accounts |

---

**User Profile Recommendations:**

| User Type | Best Venue | Reasoning |
|-----------|------------|-----------|
| Retail (<$10k trades) | Either | Difference is small; CEX has better UX |
| Active trader | Order Book | Speed and cost matter; can manage custody risk |
| Whale (>$100k) | Order Book | Significant cost savings from depth |
| DeFi native | AMM | Composability with other protocols |
| Privacy-conscious | AMM | No KYC, no tracking |

### Presentation Talking Points
- Order books beat AMMs on execution quality for liquid pairs - this is the "cost of decentralization"
- The 0.3% AMM fee is substantial - order books often charge 0.1% or less
- But this comparison ignores non-monetary factors: custody risk, censorship resistance, composability
- Real traders use BOTH: CEX for large trades, DEX for DeFi composability
- Key economic insight: The efficient market would use each venue for what it's best at - order books for execution, AMMs for permissionless access
- Uniswap v3's concentrated liquidity was designed to close this gap - and it partially succeeds

---

**PLAN_READY: .omc/plans/l06-in-class-exercises.md**
