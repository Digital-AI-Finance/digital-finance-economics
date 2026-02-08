---
marp: true
theme: default
paginate: true
---

# CBDC and Bank Disintermediation

**Will Central Bank Digital Currencies Kill Commercial Banks?**

*Reference: Brunnermeier & Niepelt (2019) - On the Equivalence of Private and Public Money*

---

# The Model: How Deposits Change Over Time

**Differential Equation:**
dD/dt = -α(r_CBDC - r_D)D + β·confidence(t)

**In Plain Language:**
The rate of deposit outflow from banks depends on two forces:

1. **Interest Rate Gap** (-α term): If CBDC pays more than bank deposits, people move money to CBDC. The bigger the gap, the faster the outflow. Parameter α (rate sensitivity) = 0.8 means deposits are moderately responsive to rate differences.

2. **Confidence Shocks** (β term): During a crisis, people lose confidence and withdraw deposits even if rates are equal. Parameter β (confidence sensitivity) = 1.2 amplifies panic effects.

---

# Baseline Results: Four Scenarios

![Baseline](../../L03_CBDCs/03_bank_disintermediation/chart.png)

**Key Findings:**
- **0% CBDC rate (green):** Deposits barely change (<5% loss over 5 years)
- **1% CBDC rate (blue):** Deposits fall to ~85% after 5 years
- **2% CBDC rate (orange):** Deposits crash to ~65% (35% loss)
- **Crisis + 1% CBDC (red):** Combined shock drives deposits to ~70%, nearing tipping point

---

# Variation 1: High Rate Sensitivity (α = 2.0)

![Variations](chart_varied.png)

**Panel 2 (top-right):** When α = 2.0 instead of 0.8, deposit outflow accelerates dramatically.

**Result:** With 2% CBDC rate, deposits collapse to ~40% (60% loss) — bank failure territory.

**Interpretation:** If people are highly sensitive to interest rates, even small CBDC rate advantages trigger massive disintermediation.

---

# Variation 2: Zero CBDC Rate Always

**Panel 3 (bottom-left):** All scenarios have CBDC rate set to 0%.

**Result:** Deposits fall by less than 5% in all cases. Even the crisis scenario (red dashed) shows minimal outflow.

**Key Insight:** **CBDC interest rate is the critical policy variable.** Without an interest rate advantage, CBDC adoption remains low regardless of other factors.

**Policy Implication:** Central banks can protect commercial banks by keeping CBDC rates at or below deposit rates.

---

# Variation 3: Early Crisis (Quarter 2 Instead of 8)

**Panel 4 (bottom-right):** Crisis starts at quarter 2 instead of quarter 8.

**Result:** Deposits fall further (to ~60% instead of ~70%) because the confidence shock has more time to compound with interest rate effects.

**Interpretation:** Timing matters. An early crisis combined with CBDC competition gives less time for stabilization policies to work.

**Real-world parallel:** If CBDC launches during economic turbulence, disintermediation risks multiply.

---

# Key Insight: CBDC Interest Rate is the Policy Lever

**What We Learned:**
1. **0% CBDC rate = Safe:** Banks keep deposits even during crises
2. **Rate above deposit rate = Dangerous:** Disintermediation accelerates, especially if people are rate-sensitive (high α)
3. **Crisis timing matters:** Early shocks compound over more quarters

**Policy Tools:**
- **Rate ceiling:** Cap CBDC interest at 1% → deposits stabilize at 75-80%
- **Quantity limits:** Restrict CBDC holdings → reduces α (rate sensitivity) by limiting arbitrage
- **Tiered rates:** Pay 2% on first EUR 3,000 only → protects small savers while limiting bank run risk

**Bottom line:** Central banks face a trade-off. Higher CBDC rates attract users but destabilize banks. The baseline chart shows intervention at quarter 12 can stabilize deposits if policy acts quickly.
