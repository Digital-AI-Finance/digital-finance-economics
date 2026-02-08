# Assignment A3: Will CBDCs Kill Commercial Banks?

## Introduction

A **CBDC** (Central Bank Digital Currency — digital money issued directly by a country's central bank, like a digital version of cash) could cause **bank disintermediation** (when people move their money from commercial banks to the central bank's digital currency). This model simulates how bank deposits D change over time using a **differential equation** (a formula describing how something changes from one moment to the next):

**dD/dt = -α(r_CBDC - r_D)D + β·confidence(t)**

Where:
- **α (alpha)** = rate sensitivity — how strongly the interest rate gap drives deposit outflow
- **r_CBDC** = interest rate on CBDC
- **r_D** = interest rate on bank deposits
- **β (beta)** = confidence sensitivity — how much public confidence affects deposits
- **ODE** = Ordinary Differential Equation — a math formula that describes continuous change over time

## Variations to Explore

### Variation 1: Increase Rate Sensitivity
**Task:** Change α from 0.8 to 2.0

**Question:** How much faster do deposits flee when people are more sensitive to interest rate differences?

### Variation 2: Zero CBDC Interest Rate
**Task:** Set CBDC rate to 0% in all scenarios (instead of 0%, 1%, 2%)

**Question:** Do banks still lose deposits even if CBDC pays nothing? Why or why not?

### Variation 3: Early Crisis
**Task:** Move crisis start from quarter 8 to quarter 2

**Question:** How does an early crisis change the outcomes? Why does timing matter?

## Open Extension

**Task:** Add a "tiered CBDC" scenario where:
- CBDC pays 2% interest on the first EUR 3,000
- CBDC pays 0% interest above EUR 3,000

**Question:** How does this tiered structure protect banks compared to a flat 2% CBDC rate? Who benefits most from this policy design?

## How to Run

1. **Google Colab** (recommended): Upload the chart.py file to Google Colab
2. **Install dependencies**: Run `!pip install scipy` in a Colab cell (needed for solving the differential equation)
3. **Run the code**: Execute the chart.py file
4. **Create variations**: Modify parameters and observe changes

## Time Allocation

- **45 minutes**: Run variations 1-3, analyze results, prepare slides
- **10 minutes**: Present findings to class

## Deliverables

1. **Presentation slides** (5-7 slides) showing:
   - The baseline model and what it means
   - Results from all three variations with charts
   - Your interpretation of what changes
   - (Optional) Extension results for tiered CBDC

2. **Key insight**: What is the most important policy lever for protecting banks from CBDC competition?

## References

- Brunnermeier, M. K., & Niepelt, D. (2019). On the Equivalence of Private and Public Money. *Journal of Monetary Economics*, 106, 27-41.
- Bindseil, U. (2020). Tiered CBDC and the financial system. *ECB Working Paper Series*, No. 2351.
