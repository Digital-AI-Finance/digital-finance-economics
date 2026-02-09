# Assignment A7: The Regulatory Race to the Bottom

## Introduction

When countries compete for crypto businesses, they face a **prisoner's dilemma** (a situation where two players each have an incentive to act selfishly, even though cooperating would make both better off). This model uses **game theory** (the mathematical study of strategic decision-making) with a 3×3 **payoff matrix** (a table showing the outcome for every possible combination of strategies). Two countries simultaneously choose between Strict, Medium, or Lax regulation. A **Nash equilibrium** (a combination of strategies where neither player wants to change their choice, given what the other is doing) reveals the stable outcome.

## The Baseline Payoff Matrix

Each cell shows the payoff for the row player (Country A). Country B receives symmetric payoffs (same matrix, but using columns as their strategy and rows as opponent strategy).

```
           Strict  Medium  Lax
Strict      7       4       2
Medium      8       6       3
Lax         9       7       4
```

**Analysis:**
- Lax is **dominant** (the best response regardless of opponent's choice):
  - vs Strict: 9 > 8 > 7
  - vs Medium: 7 > 6 > 4
  - vs Lax: 4 > 3 > 2
- **Nash equilibrium**: (Lax, Lax) = 4 for each country
- **Cooperative outcome**: (Strict, Strict) = 7 for each country (unstable)

The race to the bottom produces lower payoffs than cooperation, but no country can unilaterally improve by choosing stricter regulation.

## Variations

### Variation 1: Lax Penalty (-5)

Suppose international organizations impose a penalty of -5 on any country choosing Lax regulation. Subtract 5 from all Lax row payoffs AND all Lax column payoffs.

**New Lax row**: [9-5, 7-5, 4-5] = [4, 2, -1]
**New Lax column** (for row player): [2-5, 3-5, 4-5] = [-3, -2, -1]

**Question**: Where is the new Nash equilibrium? Is Lax still dominant?

### Variation 2: Strict Subsidy (+3)

Suppose a global climate fund subsidizes strict regulators by +3. Add 3 to all Strict row payoffs.

**New Strict row**: [7+3, 4+3, 2+3] = [10, 7, 5]

**Question**: Is Strict now dominant? What is the Nash equilibrium?

### Variation 3: Extended Game (200 Rounds)

Change the repeated game from 50 rounds to 200 rounds. Keep the same defection pattern (defection rounds at 10, 25, 40, each lasting 2 rounds).

**Questions**:
- How much does **tit-for-tat** (a strategy of copying the opponent's previous move) gain over always-Lax in 50 rounds?
- How much does tit-for-tat gain over always-Lax in 200 rounds?
- What does this tell you about the importance of long-term relationships?

## Open Extension

Design a payoff matrix where **(Medium, Medium) is the unique Nash equilibrium**. Your matrix must satisfy:
1. Medium is the best response to Medium
2. Medium is the best response to Strict
3. Medium is the best response to Lax

Provide your matrix and verify it mathematically.

## How to Run

Use Google Colab to modify the provided Python code. The baseline chart shows the payoff matrix and repeated game dynamics. Your task is to create variations that demonstrate how penalties, subsidies, and repeated interaction affect equilibrium outcomes.

## Time Allocation

- **45 minutes**: Analysis and calculations
- **10 minutes**: Presentation preparation

## Learning Outcomes

After completing this assignment, you should be able to:
1. Identify dominant strategies and Nash equilibria in normal-form games
2. Explain how external incentives (penalties/subsidies) can shift equilibria
3. Understand the role of repeated interaction in sustaining cooperation
4. Apply game theory to real-world regulatory competition scenarios

## Reference

Kanbur, R., & Keen, M. (1993). Jeux Sans Frontières: Tax Competition and Tax Coordination When Countries Differ in Size. *American Economic Review*, 83(4), 877-892.
