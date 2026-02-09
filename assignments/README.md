# In-Class Presentation Assignments

## Overview
8 in-class presentation assignments, one per lecture. Each asks student groups (3-4 students) to replicate an existing chart model, vary parameters, and present findings in a 5-7 slide presentation.

**Target audience**: BSc students with no prior knowledge of finance, economics, or programming.
**Time budget**: 45 min work + 10 min presentation per assignment.
**Environment**: Google Colab (no local install required).

## Assignment Table

| # | Lecture | Title | Economic Model | Source Chart |
|---|---------|-------|---------------|-------------|
| A1 | L01 Introduction | How Fast Do Payment Technologies Spread? | Rogers S-curve: S(t) = K/(1+exp(-r(t-t0))) | `L01_Introduction/01_payment_evolution/chart.py` |
| A2 | L02 Monetary Economics | Gresham's Law: When Bad Money Wins | Logit feedback agent simulation | `L02_Monetary_Economics/05_greshams_law_simulation/chart.py` |
| A3 | L03 CBDCs | Will CBDCs Kill Commercial Banks? | ODE deposit dynamics | `L03_CBDCs/03_bank_disintermediation/chart.py` |
| A4 | L04 Payment Systems | Network Effects: When Does a Payment System Take Off? | Metcalfe V=n^2 vs Odlyzko V=n*ln(n) | `L04_Payment_Systems/04_network_effects_metcalfe/chart.py` |
| A5 | L05 Platform & Token Economics | Does Random Growth Create Monopolies? | Gibrat's Law with HHI, Gini, CR4 | `L05_Platform_Token_Economics/05_winner_take_all_market_share/chart.py` |
| A6 | L06 Market Microstructure | How AMMs Set Prices: The Constant Product Formula | AMM: x*y=k with slippage | `L06_Market_Microstructure/01_amm_constant_product/chart.py` |
| A7 | L07 Regulatory Economics | The Regulatory Race to the Bottom | Nash equilibrium in 3x3 payoff matrix | `L07_Regulatory_Economics/04_regulatory_arbitrage_game/chart.py` |
| A8 | L08 Synthesis | How Financial Crises Spread Through Networks | Network cascade contagion | `L08_Synthesis/01_systemic_risk_contagion/chart.py` |

## Each Assignment Contains

| File | Description |
|------|-------------|
| `assignment-brief.md` | Student-facing instructions with 3 parameter variations + 1 open extension |
| `model-answer-presentation.md` | Complete 7-slide Marp presentation (instructor's model answer) |
| `chart_varied.py` | Modified Python code producing 2x2 subplot comparing baseline with 3 variations |

## How to Use

### For Instructors
1. Distribute `assignment-brief.md` to student groups
2. Students work in Google Colab for 45 minutes
3. Groups present their findings (10 min each)
4. Use `model-answer-presentation.md` as reference for grading

### For Students
1. Open Google Colab (colab.research.google.com)
2. Create a new notebook and paste the Python code from the source chart
3. Run it to see the baseline chart
4. Modify parameters as described in the assignment brief
5. Save your charts and build your presentation

## Requirements
- Python packages: numpy, matplotlib (pre-installed in Google Colab)
- A3 additionally requires scipy (`!pip install scipy` in Colab)
