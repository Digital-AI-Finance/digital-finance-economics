# Assignment A4: Network Effects in Payment Systems

## Network Effects: When Does a Payment System Take Off?

### Introduction

Network effects (the phenomenon where a product becomes more valuable as more people use it) determine when a payment system reaches critical mass (the point where enough people use it that growth becomes self-sustaining). Three theories model network value V as a function of n users:

- **Metcalfe's Law**: V = n²/1000 (every pair can connect)
- **Odlyzko-Tilly**: V = n·ln(n)/10 (only close contacts matter)
- **Linear**: V = n (no network effects)

The divisors (1000 and 10) normalize raw connection counts to comparable value units.

**Key Concepts:**
- **Switching cost**: the time, effort, and money needed to change from one payment system to another
- **Critical mass**: the number of users at which network value exceeds switching costs, making adoption self-sustaining

### Your Task

You will explore how different network value models predict when payment systems reach critical mass under various switching cost scenarios.

### Variations to Implement

1. **VARIATION 1 - Lower switching cost threshold from 500 to 100**
   - How does critical mass change for each model?
   - Which model reaches critical mass fastest?

2. **VARIATION 2 - Raise switching cost to 2,000**
   - How does critical mass change?
   - Which model never reaches critical mass within 1000 users?

3. **VARIATION 3 - Add Reed's Law**
   - Implement Reed's Law: V = 2^(n/10)
   - Where does it cross the switching cost threshold (500)?
   - How does it compare to the other models?

### Open Extension (Advanced)

Remove the scaling divisors and use raw formulas:
- Metcalfe: V = n²
- Odlyzko-Tilly: V = n·ln(n)
- Linear: V = n

**Questions:**
- How do critical mass points change?
- What do the divisors represent economically?
- Why are they needed for realistic modeling?

### How to Run

Use Google Colab or your local Python environment with matplotlib and numpy installed.

### Time Allocation

- 45 minutes: Implementation and analysis
- 10 minutes: Presentation preparation

### Deliverables

1. Modified Python code implementing all three variations
2. 7-slide presentation (use Marp or PowerPoint) summarizing your findings
3. Brief written analysis of what the scaling factors mean economically

### References

- Metcalfe, B. (2013). "Metcalfe's Law after 40 Years of Ethernet"
- Odlyzko, A., & Tilly, B. (2005). "A refutation of Metcalfe's Law and a better estimate for the value of networks and network interconnections"

### Grading Criteria

- **Correctness** (40%): All three variations implemented correctly
- **Analysis** (30%): Clear explanation of critical mass changes
- **Presentation** (20%): Clear visualization and communication
- **Extension** (10%): Insight into scaling factors (bonus)
