# Plan: Economics of Digital Finance - 8-Lesson BSc Course

## Overview

**Course**: Economics of Digital Finance
**Level**: BSc (Economics/Finance students with strong theory background)
**Format**: 8 lessons x 45 minutes
**Template**: Madrid theme Beamer (from `../template_beamer_final.tex`)
**Location**: `D:\Joerg\Research\slides\Digital-Finance-Economics\`

## Course Philosophy

This course examines digital finance through four economic lenses:
1. **Monetary Economics**: CBDCs, money theory, payment systems, financial stability
2. **Platform/Network Economics**: Network effects, two-sided markets, token economics
3. **Market Microstructure**: Price discovery, liquidity, trading mechanisms
4. **Regulatory Economics**: Financial regulation, competition policy, consumer protection

Unlike the technical courses (Digital-Finance-Course, Digital-Finance), this course focuses on **economic theory and analysis** rather than implementation.

---

## Proposed 8-Lesson Structure

### L01: Introduction to the Economics of Digital Finance
**Theme**: Setting the economic framework

**Content**:
- What is digital finance? (Economic definition vs. technical)
- Historical evolution: from commodity money to digital currencies
- The four economic lenses framework
- Why economists should care about digital finance
- Economic questions vs. technical questions

**Key Concepts**: Money functions, payment systems, financial intermediation, digital transformation

**Chart Ideas**:
- Evolution of payment methods timeline
- Digital finance taxonomy (economic perspective)
- Global digital payments growth

---

### L02: Monetary Economics of Digital Currencies
**Theme**: Money theory meets cryptocurrency

**Content**:
- Functions of money: unit of account, medium of exchange, store of value
- Monetary theory: quantity theory, velocity, money demand
- Cryptocurrencies as money: economic assessment
- Stablecoins: economic design and stability
- Dollarization vs. crypto-ization

**Key Concepts**: Money demand, velocity, Gresham's Law, currency substitution, seigniorage

**Chart Ideas**:
- Bitcoin volatility vs. traditional currencies
- Stablecoin market share evolution
- Money functions assessment matrix

---

### L03: Central Bank Digital Currencies (CBDCs)
**Theme**: The economics of public digital money

**Content**:
- CBDC design choices: retail vs. wholesale, account vs. token
- Monetary policy transmission with CBDCs
- Bank disintermediation risk
- Financial inclusion potential
- International dimension: currency competition

**Key Concepts**: Monetary policy transmission, financial intermediation, deposit flight, currency competition

**Chart Ideas**:
- CBDC project status worldwide (map)
- CBDC design space (2x2 matrix)
- Bank balance sheet impact scenarios

---

### L04: Payment Systems Economics
**Theme**: Economics of value transfer

**Content**:
- Economics of payment systems: network effects, interchange fees
- Cross-border payment inefficiencies and solutions
- Real-time gross settlement vs. deferred net settlement
- Financial inclusion: the unbanked problem
- Remittances and correspondent banking costs

**Key Concepts**: Two-sided markets, interchange, correspondent banking, financial inclusion

**Chart Ideas**:
- Global remittance costs by corridor
- Payment system adoption curves
- Correspondent banking network visualization

---

### L05: Platform Economics and Token Economics
**Theme**: Network effects and digital assets

**Content**:
- Platform economics: two-sided markets, winner-take-all dynamics
- Network effects in blockchain: Metcalfe's Law and beyond
- Token economics: utility tokens, governance tokens, security tokens
- Tokenomics design: supply schedules, staking, burning
- Adoption dynamics and critical mass

**Key Concepts**: Network effects, platform competition, token utility, mechanism design

**Chart Ideas**:
- Network effect value curves
- Token supply schedules comparison
- Platform adoption S-curves

---

### L06: Market Microstructure in Digital Finance
**Theme**: How digital markets work

**Content**:
- Market microstructure fundamentals: order books, bid-ask spreads
- Automated Market Makers (AMMs): economic analysis
- Liquidity provision: traditional vs. DeFi
- Price discovery in fragmented markets
- Manipulation and market quality

**Key Concepts**: Liquidity, price discovery, bid-ask spread, impermanent loss, MEV

**Chart Ideas**:
- Order book vs. AMM comparison
- Liquidity depth comparison
- Price discovery efficiency metrics

---

### L07: Regulatory Economics of Digital Finance
**Theme**: Economics of financial regulation

**Content**:
- Rationale for financial regulation: market failures, externalities
- Regulatory approaches: principles-based vs. rules-based
- Competition policy in digital finance
- Consumer protection economics
- Regulatory arbitrage and jurisdictional competition

**Key Concepts**: Market failure, asymmetric information, regulatory capture, competition policy

**Chart Ideas**:
- Regulatory framework comparison (US, EU, Asia)
- Regulatory intensity spectrum
- Regulatory sandbox outcomes

---

### L08: Synthesis - The Future of Digital Finance
**Theme**: Integration and forward-looking analysis

**Content**:
- Systemic risk in digital finance
- Traditional finance vs. DeFi: convergence or competition?
- Open research questions in economics of digital finance
- Policy recommendations synthesis
- Course integration: applying all four lenses

**Key Concepts**: Systemic risk, financial stability, regulatory coordination, future scenarios

**Chart Ideas**:
- TradFi-DeFi integration scenarios
- Systemic risk transmission channels
- Four lenses synthesis diagram

---

## Implementation Plan

### Phase 1: Course Infrastructure Setup
1. Create folder structure in `Digital-Finance-Economics/`
2. Copy template from `../template_beamer_final.tex`
3. Create lesson folders (L01-L08)

### Phase 2: Per-Lesson Development (for each L01-L08)
1. Create `LXX_Topic/` folder
2. Create chart subfolders with `chart.py` scripts
3. Generate chart PDFs
4. Write `.tex` slides using template
5. Compile and verify zero overflow

### Phase 3: Quality Assurance
1. Compile all lessons
2. Review for consistency
3. Verify all charts render correctly
4. Check for overflow warnings

---

## Folder Structure

```
Digital-Finance-Economics/
|-- README.md
|-- SYLLABUS.md
|-- template_beamer.tex          # Copied from parent
|
|-- L01_Introduction/
|   |-- L01_Introduction.tex
|   |-- 01_payment_evolution/
|   |   |-- chart.py
|   |   `-- chart.pdf
|   |-- 02_digital_finance_taxonomy/
|   |   |-- chart.py
|   |   `-- chart.pdf
|   `-- temp/
|
|-- L02_Monetary_Economics/
|-- L03_CBDCs/
|-- L04_Payment_Systems/
|-- L05_Platform_Economics/
|-- L06_Market_Microstructure/
|-- L07_Regulatory_Economics/
|-- L08_Synthesis/
```

---

## Key Differentiators from Existing Courses

| Aspect | Digital-Finance (Technical) | Economics of Digital Finance |
|--------|----------------------------|------------------------------|
| Focus | Implementation, code, protocols | Economic theory, analysis |
| Audience | Technical practitioners | Economics students |
| Assessment | Practical coding exercises | Economic analysis |
| Depth | How it works | Why it works economically |
| Examples | Solidity, DeFi protocols | Economic models, policy cases |

---

## Files to Create

1. **README.md** - Course overview
2. **SYLLABUS.md** - Detailed syllabus
3. **template_beamer.tex** - Slide template (copy from parent)
4. **8 lesson folders** with:
   - Main `.tex` file
   - 2-3 chart folders each
   - `temp/` for LaTeX auxiliary files

---

## Verification

After implementation:
- [ ] All 8 lessons compile without overflow warnings
- [ ] All charts generate correctly
- [ ] Consistent styling across all lessons
- [ ] Economic rigor maintained throughout
- [ ] Template properly applied
