# Assignment A5: Does Random Growth Create Monopolies?

**Course**: Digital Finance & Economics
**Lecture**: L05 Platform & Token Economics
**Time**: 45 minutes work + 10 minutes presentation
**Delivery**: Google Colab + 7-slide Marp presentation

---

## Introduction

**Gibrat's Law** is a theory from 1931 stating that firm growth rates are random and independent of firm size. It predicts that even without any unfair advantages, pure randomness can create extreme **market concentration** (when a small number of firms control most of the market).

This simulation starts 100 equal firms and lets each grow by a random percentage each period. We track three key metrics:

- **HHI (Herfindahl-Hirschman Index)**: A measure of market concentration calculated by summing the squared market shares of all firms. Ranges from 0 to 10,000 where higher means more concentrated.
- **Gini coefficient**: A measure of inequality from 0 to 1 where 0 means perfect equality and 1 means one firm has everything.
- **CR4**: The combined market share of the top 4 firms.

**Research Question**: Does pure randomness in growth rates lead to monopoly?

---

## Your Task

### Part 1: Run the Baseline Model (15 minutes)

1. Copy the baseline simulation code (provided below) into Google Colab
2. Run it and observe the charts
3. Record the final HHI, Gini, and CR4 values after 100 periods
4. Screenshot or save the output chart

### Part 2: Test Three Variations (20 minutes)

Modify the baseline model to test each variation below. Run each separately and record results.

#### Variation 1: Reduce Growth Volatility
**Change**: Set `sigma=0.05` (instead of 0.25)
**Question**: Does concentration still emerge when growth is less volatile?

#### Variation 2: Increase Average Growth
**Change**: Set `mu=0.10` (instead of 0.02)
**Question**: What happens to Gini when all firms grow faster on average?

#### Variation 3: Fewer Initial Firms
**Change**: Set `n_firms=10` (instead of 100)
**Question**: How does initial market structure affect concentration?

### Part 3: Open Extension (10 minutes)

Add **increasing returns to scale**: Firms with more than 10% market share get a growth bonus.

**Implementation hint**: After calculating shares each period, add this:
```python
for i in range(n_firms):
    if shares[i] > 0.10:
        sizes[i] *= (1 + 0.05)  # 5% bonus growth
```

**Question**: Does this accelerate winner-take-all dynamics?

---

## How to Run

1. Go to [Google Colab](https://colab.research.google.com/)
2. Create a new notebook
3. Copy the baseline code (from lecture materials or below)
4. Run cells to generate charts
5. Modify parameters for each variation
6. Save/screenshot results

---

## Deliverable: 7-Slide Marp Presentation

Create a Marp markdown presentation with:

1. **Title slide**: Your name, assignment title, date
2. **The Model**: Explain Gibrat's Law equation and the three metrics (HHI, Gini, CR4)
3. **Baseline Results**: Show baseline chart + final metrics
4. **Variation 1**: Show results + interpretation
5. **Variation 2**: Show results + interpretation
6. **Variation 3**: Show results + interpretation
7. **Key Insight**: Answer the research question with evidence from your results

**Marp template starter**:
```markdown
---
marp: true
theme: default
paginate: true
---

# Does Random Growth Create Monopolies?

Your Name
Assignment A5 | L05 Platform & Token Economics

---

## The Model: Gibrat's Law (1931)

...
```

---

## Grading Criteria

| Criterion | Points |
|-----------|--------|
| Baseline model runs correctly | 20 |
| All 3 variations implemented and results recorded | 30 |
| Open extension attempted | 10 |
| Presentation clarity and structure | 20 |
| Interpretation and economic insight | 20 |
| **Total** | **100** |

---

## Academic Integrity

- You may discuss the model with classmates
- Your code variations and presentation must be your own work
- Cite any external sources (beyond lecture materials)

---

## Baseline Code Reference

The baseline model is available in:
- Lecture slides: L05 Platform & Token Economics
- Chart source: `L05_Platform_Token_Economics/05_winner_take_all_market_share/chart.py`

Key parameters:
```python
n_firms = 100
n_periods = 100
mu = 0.02      # Average growth rate
sigma = 0.25   # Growth volatility
```

The simulation uses:
```python
S_{i,t} = S_{i,t-1} * (1 + epsilon)
```
where `epsilon ~ N(mu, sigma^2)` is drawn randomly each period for each firm.

---

## Tips for Success

1. **Start early** - debugging simulation code takes time
2. **Label your charts** - include titles, axis labels, and legends
3. **Explain, don't just describe** - interpret WHY concentration emerges
4. **Compare across variations** - what's the key driver of concentration?
5. **Be concise** - 7 slides means each slide must count

Good luck!
