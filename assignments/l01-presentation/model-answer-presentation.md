---
marp: true
theme: default
paginate: true
---

# How Fast Do Payment Technologies Spread?
## Rogers (1962) Diffusion of Innovations
*In-Class Presentation Assignment — L01 Introduction*

**Student Name**: Model Answer
**Date**: February 2026

---

## The Model: S-Curve (Logistic Growth)

**Equation**: S(t) = K / (1 + exp(-r * (t - t0)))

**Parameters**:
- **K** (carrying capacity) = maximum adoption percentage the technology will ever reach
- **r** (growth rate) = how fast adoption accelerates during the steep middle phase
- **t0** (inflection point) = the year when adoption reaches exactly half of K

**Why S-shaped?** Early adopters are easy to convince (slow start), then word-of-mouth creates exponential growth (steep middle), then the market saturates as remaining holdouts resist (flat top).

**Source**: Rogers, E.M. (1962). *Diffusion of Innovations*. Free Press.

---

## Baseline: Six Payment Technologies

![Baseline](../../L01_Introduction/01_payment_evolution/chart.png)

**Key Observations**:
- Credit cards: slowest growth (r=0.08) but highest ceiling (K=75%)
- Mobile payments: fastest growth (r=0.15) but medium ceiling (K=65%)
- Cryptocurrencies: slow growth (r=0.10) and low ceiling (K=30%)
- Growth rate r determines steepness through inflection, carrying capacity K determines finish line

---

## Variation 1: Adding Buy Now Pay Later (BNPL)

![Variations](chart_varied.png)

**Parameters**: K=40%, r=0.20, t0=2022

**Analysis**:
- BNPL has the *fastest* growth rate (r=0.20) of all technologies shown
- But lowest ceiling among traditional payments (K=40%)
- Interpretation: BNPL spreads quickly among young consumers (high r) but faces regulatory limits and consumer skepticism that cap long-term adoption (low K)
- By 2035, BNPL reaches ~38% (near its ceiling), while credit cards continue growing toward 75%

---

## Variation 2: Faster Crypto Adoption (r doubled)

**Both curves**: reach 15% (half of K=30%) at the inflection point t0=2022

**Analysis**:
- Doubling r changes HOW STEEPLY the curve rises through 15%, not WHEN it crosses 15%
- With r=0.10: goes from 5% to 25% (17% to 83% of K) over ~28 years
- With r=0.20: goes from 5% to 25% in ~14 years (twice as steep)
- But ceiling K=30% remains unchanged — crypto still plateaus at 30% regardless of r
- **Key Insight**: Growth rate r controls the *steepness* of adoption during the transition phase, while carrying capacity K controls your *ultimate* market share

**Real-world question**: What would it take to increase crypto's K from 30% to 60%? (Hint: regulatory clarity, stability mechanisms, user-friendly interfaces)

---

## Variation 3: CBDC with Higher Ceiling (K=90%)

**Original**: K=50%, reaches ~45% by 2050
**Increased**: K=90%, reaches ~80% by 2050

**Analysis**:
- By 2040, K=90% CBDC (at ~70%) overtakes mobile payments (plateauing at 65%)
- By 2050, K=90% CBDC dominates all technologies
- **Interpretation**: If governments mandate CBDC for tax payments or social benefits, carrying capacity K could approach 90% (nearly universal adoption)

**Counterargument**: Privacy concerns and distrust of government surveillance might keep actual K closer to 50-60%, not 90%

---

## Key Insight: Two Parameters, Two Questions

Every technology adoption story answers two questions:

1. **How fast?** (controlled by growth rate r)
   - Mobile payments: r=0.15 (fastest)
   - Credit cards: r=0.08 (slowest)

2. **How far?** (controlled by carrying capacity K)
   - ATMs/debit: K=85% (highest)
   - Cryptocurrencies: K=30% (lowest)

**Winning strategy**: High r gets you market share quickly (first-mover advantage), but high K determines whether you're still relevant in 20 years.

**Testable prediction**: By 2030, CBDCs will reach 25-30% adoption in countries that launch pilots before 2025 (China, Sweden, Nigeria). Countries without pilots will stay below 5%.

---

## References & Data Sources

- Rogers, E.M. (1962). *Diffusion of Innovations*. Free Press.
- Chart code: Python implementation using logistic growth function
- Technology parameters: Estimated from industry reports (World Payments Report 2023, McKinsey FinTech surveys)
- Model limitations: Assumes single homogeneous population (reality: different adoption curves for age groups, countries, income levels)

**Code availability**: Full Python code in `chart_varied.py`
