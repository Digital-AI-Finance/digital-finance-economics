---
marp: true
theme: default
paginate: true
---

# Gresham's Law: Why People Spend Bad Money and Hoard Good Money

**Economic Principle**: "Bad money drives out good money"

**Model**: 1,000 agents decide each period whether to spend Currency A (depreciating 5%/period) or Currency B (depreciating 1%/period).

**Key Reference**: Selgin (1996) – *Salvaging Gresham's Law: The Good, the Bad, and the Illegal*

---

## The Model: Logit Feedback Rule

Probability that an agent spends Currency A at time t:

```
P(spend A)_t = 1 / (1 + exp(-z_t))
```

where the logit argument evolves as:

```
z_t = k × (s_{t-1} - 0.5) + (r_A - r_B) × 10 + b × (t/T)
```

**Variables**:
- `s_{t-1}` = share of agents who spent A in previous period
- `k` = feedback strength (how much past behavior amplifies current behavior)
- `(r_A - r_B) × 10` = depreciation differential bias (higher depreciation of A relative to B incentivizes spending A)
- `b` = small exogenous drift toward spending A (default 0.10)
- `t/T` = time progress (0 at start, 1 at end)

**Mechanism**: When Currency A depreciates faster than B, agents prefer to spend A and hoard B. This depreciation differential enters the logit directly. When more people spend A, it becomes even more rational for you to also spend A (positive feedback). Together, these forces create a tipping point.

---

## Baseline: k = 15, Tipping at ~Period 48

![width:900px](../../L02_Monetary_Economics/05_greshams_law_simulation/chart.png)

**Observations**:
- Initially 50-50 split between spending A and B
- Tipping point at period ~48: Currency A reaches 80% circulation
- By period 100: A dominates spending (~98.5%), B is hoarded

Note: The varied chart (next slides) uses an explicit depreciation differential term `(r_A - r_B) x 10` in the logit, which accelerates baseline tipping to t=27.

---

## Variation 1: Weak Feedback (k = 5)

![width:900px](chart_varied.png)

**Panel 2 (Top Right)**: Weak feedback delays tipping significantly -- tipping occurs at t=57 (vs t=27 baseline). Currency A reaches ~90% by period 100.

**Why?** Lower k means past behavior has less influence. The depreciation differential (4 pp) and small exogenous drift still push toward spending A, but the feedback loop is too weak to create a rapid cascade. The transition from 50-50 to A-dominance takes more than twice as long as baseline.

**Key Insight**: Weak feedback = delayed tipping. Even with the same depreciation difference, insufficient feedback strength stretches the transition over many more periods.

---

## Variation 2: Strong Feedback (k = 25)

![width:900px](chart_varied.png)

**Panel 3 (Bottom Left)**: Strong feedback accelerates tipping to ~period 23.

**Why?** Higher k means past behavior strongly amplifies current behavior. Combined with the depreciation differential of 0.4 pushing the logit positive, even a small deviation from 50-50 triggers a rapid cascade. The transition from 50-50 to A-dominance happens in roughly 10 periods.

**Key Insight**: Strong feedback = faster tipping, earlier tipping point. The S-curve transition is sharper. Tipping at t=23 vs baseline t=27 shows diminishing returns from increasing k when the depreciation differential already provides a strong push.

---

## Variation 3: Equal Depreciation (r_A = r_B = 3%)

![width:900px](chart_varied.png)

**Panel 4 (Bottom Right)**: Tipping is significantly delayed to ~period 48 (vs baseline t=27). The depreciation differential is zero, so only the small exogenous drift (base_bias) gradually pushes spending toward A.

**Why?** With equal depreciation (r_A = r_B = 3%), the depreciation_bias term is zero. There is no quality difference to drive Gresham's Law. The only remaining force is the small base_bias drift (0.10 * t/T), which slowly nudges the logit positive over time. This eventually triggers the feedback loop, but the transition takes nearly twice as long as baseline.

**Key Insight**: Removing the depreciation differential delays tipping by ~21 periods (from t=27 to t=48). The depreciation difference is the primary accelerant of Gresham's Law -- without it, the feedback loop lacks an initial push and must rely on weak exogenous drift to eventually trigger.

---

## Key Insight: k Controls HOW FAST, Depreciation Difference Controls WHETHER

| Parameter | Effect | Evidence |
|-----------|--------|----------|
| **k (feedback strength)** | Controls tipping SPEED | k=5: tipping delayed to t=57 (~90% by end)<br>k=15: tipping at t=27 (baseline)<br>k=25: tipping at t=23 (rapid) |
| **Depreciation difference (r_A - r_B)** | Controls tipping ACCELERATION | r_A=5%, r_B=1%: tipping at t=27 (strong depreciation push)<br>r_A=3%, r_B=3%: tipping delayed to t=48 (no depreciation push, only slow drift) |

**Economic Implication**: Gresham's Law has two drivers that interact:
- **Depreciation difference** provides the initial incentive to spend bad money. Removing it delays tipping by ~21 periods (t=27 to t=48).
- **Feedback strength** determines how quickly a small initial bias cascades into full substitution. Weak feedback (k=5) delays tipping by ~30 periods (t=27 to t=57).

The depreciation differential is the more powerful driver: it shifts the logit argument by 0.4 at every step (vs the exogenous drift which contributes at most 0.10 over the full horizon).

**Historical Example**: During hyperinflation (very large depreciation difference + strong social feedback), everyone rushes to spend depreciating currency, creating rapid collapse. During mild inflation (small depreciation difference), weak feedback allows dual-currency systems to persist for decades (e.g., dollarization in Latin America).
