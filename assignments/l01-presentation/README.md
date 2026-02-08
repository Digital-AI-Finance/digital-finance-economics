# L01 Presentation Assignment - Files Overview

## Assignment Structure

This directory contains a complete in-class presentation assignment for L01 Introduction on payment technology adoption using the Rogers (1962) S-curve model.

### Files

1. **assignment-brief.md** - Student-facing instructions
   - Explains the Rogers (1962) diffusion model with all terms defined
   - Lists three required variations students must complete
   - Includes optional Gompertz curve extension for extra credit
   - Provides Google Colab setup instructions
   - Specifies deliverable: 5-7 slide presentation

2. **model-answer-presentation.md** - Complete model answer
   - 7-slide Marp presentation (ready to render)
   - Shows baseline chart + all three variations
   - Includes analysis of parameter sensitivity
   - Provides testable predictions and references
   - Can be used as grading rubric or student reference after assignment

3. **chart_varied.py** - Python code for generating variation charts
   - Creates 2x2 subplot figure with 4 panels
   - Panel 1: Baseline (6 technologies)
   - Panel 2: VARIATION 1 (add BNPL)
   - Panel 3: VARIATION 2 (double crypto growth rate)
   - Panel 4: VARIATION 3 (increase CBDC ceiling)
   - Outputs chart_varied.pdf and chart_varied.png
   - Students can modify parameters and re-run

### How to Use

**For Instructors:**
1. Share `assignment-brief.md` with students at start of class
2. Give students 45 minutes to explore code and generate charts
3. Students present for 10 minutes using their generated charts
4. Use `model-answer-presentation.md` as grading rubric
5. Share model answer after presentations for learning

**For Students:**
1. Read `assignment-brief.md` for instructions
2. Open Google Colab and paste code from `chart_varied.py`
3. Run code to generate baseline chart
4. Modify parameters for three required variations
5. Create 5-7 slide presentation using your charts
6. Present findings and insights

### Learning Objectives

- Understand S-curve (logistic growth) model parameters
- Recognize how K (ceiling) and r (growth rate) affect adoption trajectories
- Practice parameter sensitivity analysis
- Develop intuition for technology adoption dynamics
- Communicate technical findings visually

### Assessment Criteria

- Correct replication of baseline chart (20%)
- All three required variations completed (30%)
- Clear explanation of parameter effects (30%)
- Presentation clarity and visual design (20%)

### Extension Ideas

Beyond the required variations, students can explore:
- Compare S-curve vs Gompertz curve for different technology types
- Add uncertainty bands using Monte Carlo simulation
- Estimate parameters from real adoption data (credit card usage statistics)
- Model network effects (metcalfe's law) on growth rate r
- Incorporate Bass model components (innovators vs imitators)

### Technical Notes

- Code uses matplotlib for plotting
- Requires numpy for numerical calculations
- Outputs both PDF (high-res) and PNG (web-friendly) formats
- Uses consistent color scheme from L01 lecture materials
- Follows course style guide (MLPURPLE, MLBLUE, etc.)
- All charts include annotations at key inflection points

### Time Estimate

- Setup (5 min): Open Colab, paste code
- Exploration (15 min): Run baseline, understand parameters
- Variations (20 min): Modify code, generate new charts
- Analysis (10 min): Interpret results, draft insights
- Presentation prep (10 min): Create slides, rehearse
- **Total: 60 minutes** (45 work + 10 presentation + 5 buffer)

### Common Student Questions

**Q: Why does BNPL have higher r but lower K than credit cards?**
A: BNPL spreads quickly among young consumers (high r) but faces regulatory limits and consumer skepticism that cap long-term adoption (low K).

**Q: What does "inflection point" mean?**
A: The year when adoption reaches exactly half of its maximum (K/2). This is when the S-curve transitions from accelerating to decelerating growth.

**Q: Can r be greater than 1.0?**
A: Theoretically yes, but in practice payment technologies have r between 0.05-0.20. Higher r would mean adoption goes from 1% to 99% in just a few years.

**Q: Why doesn't crypto reach 100% adoption?**
A: Carrying capacity K reflects structural barriers: regulatory uncertainty, volatility, lack of merchant acceptance, privacy concerns. These factors limit K to ~30%.

### Data Sources

Technology parameters estimated from:
- World Payments Report 2023 (Capgemini)
- McKinsey FinTech surveys
- Federal Reserve payments studies
- Historical credit card penetration data (1960-2020)
- Mobile payment adoption rates (2010-2025)

### References

- Rogers, E.M. (1962). *Diffusion of Innovations*. Free Press.
- Bass, F.M. (1969). "A New Product Growth Model for Consumer Durables". *Management Science* 15(5): 215-227.
- Meade, N. & Islam, T. (2006). "Modelling and forecasting the diffusion of innovation". *International Journal of Forecasting* 22(3): 519-545.
