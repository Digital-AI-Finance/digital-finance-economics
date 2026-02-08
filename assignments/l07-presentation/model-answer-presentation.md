---
marp: true
theme: default
paginate: true
math: katex
---

# Assignment A7: The Regulatory Race to the Bottom

**Model Answer Presentation**

Reference: Kanbur & Keen (1993) - Jeux Sans Frontières: Tax Competition and Tax Coordination

---

## The Model: Game Theory Concepts

**Payoff Matrix**: Shows outcome for every strategy combination

**Dominant Strategy**: Best response regardless of opponent's choice

**Nash Equilibrium**: Strategy pair where neither player wants to deviate
- Each player's strategy is the best response to the other's strategy
- Self-enforcing: no unilateral incentive to change

**Prisoner's Dilemma**: Individual incentives lead to collectively worse outcome than cooperation

---

## Baseline: Race to the Bottom

```
           Strict  Medium  Lax
Strict      7       4       2
Medium      8       6       3
Lax         9       7       4
```

**Lax is dominant:**
- vs Strict: 9 > 8 > 7
- vs Medium: 7 > 6 > 4
- vs Lax: 4 > 3 > 2

**Nash equilibrium**: (Lax, Lax) = 4
**Cooperative outcome**: (Strict, Strict) = 7 (unstable)

![Baseline](../../L07_Regulatory_Economics/04_regulatory_arbitrage_game/chart.png)

---

## Variation 1: Lax Penalty (-5)

**Modified Matrix** (Lax penalty -5 applied to row AND column):
```
           Strict  Medium  Lax
Strict      7       4      -3
Medium      8       6      -2
Lax         4       2      -1
```

**Best responses:**
- vs Strict → Medium (8 > 7 > 4)
- vs Medium → Medium (6 > 4 > 2)
- vs Lax → Lax (-1 > -2 > -3)

**Nash equilibrium shifts to (Medium, Medium) = 6**

✅ Sanctions work! Punishment makes extreme arbitrage too costly.

![Variations](chart_varied.png)

---

## Variation 2: Strict Subsidy (+3)

**Modified Matrix** (Strict subsidy +3):
```
           Strict  Medium  Lax
Strict     10       7       5
Medium      8       6       3
Lax         9       7       4
```

**Best responses:**
- vs Strict → Strict (10 > 9 > 8)
- vs Medium → Strict = Lax (7 = 7 > 6)
- vs Lax → Strict (5 > 4 > 3)

**Strict is weakly dominant. Nash equilibrium: (Strict, Strict) = 10**

✅ Subsidy makes cooperation self-enforcing!

![Variations](chart_varied.png)

---

## Variation 3: 200 Rounds (Repeated Interaction)

**50 rounds:**
- Always-Lax: 50 × 4 = **200**
- Tit-for-tat: (44 × 7) + (6 × 2) = 308 + 12 = **320**
- **Advantage: 120**

**200 rounds:**
- Always-Lax: 200 × 4 = **800**
- Tit-for-tat: (194 × 7) + (6 × 2) = 1358 + 12 = **1370**
- **Advantage: 570**

📈 Cooperation gains scale with relationship length. The "shadow of the future" (the expectation of future interactions) makes cooperation more attractive.

![Variations](chart_varied.png)

---

## Key Insights

**The Prisoner's Dilemma:**
- Individual rationality (choosing Lax) leads to collective irrationality (payoff 4 vs 7)
- Without intervention, race to bottom is inevitable

**Three Cures:**
1. **Punishment** (sanctions): Make defection too costly → shift Nash to Medium
2. **Rewards** (subsidies): Make cooperation profitable → shift Nash to Strict
3. **Repeated interaction**: Long-term relationships create incentive to cooperate

**Policy Implication:**
International coordination requires either:
- Credible penalties for regulatory arbitrage
- Financial incentives for strict regulation
- Stable long-term relationships (e.g., trade agreements with regulatory clauses)

---

