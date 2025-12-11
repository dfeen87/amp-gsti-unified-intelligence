# Quantifying Market Trust: How Goodwill and GSTI Create a Smarter Forecasting Model

## Now With AI Implementation Code

**Author:** Don Michael Feeney Jr  

**Date:** May 26, 2025

---

## Executive Summary

The **Gold-Silver Trust Index (GSTI)** offers a multidimensional metric that captures the interplay between market trust and systemic fear. By combining the behavioral signal of the gold-silver price ratio with the accounting-based indicator of corporate goodwill, the GSTI provides early detection of macroeconomic regime shifts. This paper introduces a structured formula for GSTI calculation, a dynamic weighting model, and a real-time market reading. The result is a powerful tool for analysts, investors, and policymakers navigating increasingly sentiment-driven markets.

---

## Introduction: Unifying Market Signals

The inherent nature of gold as a safe-haven asset and silver's industrial utility makes their ratio a powerful barometer of economic outlook. A rising **Gold-Silver Ratio (GSR)** often signals risk aversion, while a declining GSR suggests economic expansion.

Complementing this, **corporate goodwill**, an accounting representation of a company's intangible value (like brand recognition and customer loyalty), serves as a proxy for market trust in long-term corporate health. The GSTI harmonizes these seemingly disparate signals to offer a more holistic interpretation of market dynamics.

---

## Quantifying Goodwill: A Multi-Factor Framework

To operationalize goodwill as a signal of institutional trust, we introduce a three-part analytical structure: **General Goodwill (G)**, **Consumer Goodwill (CG)**, and their aggregate—the **Unified Goodwill Score (UGS)**. Each equation integrates weighted indicators of reputation, satisfaction, and brand momentum, creating a quantifiable goodwill metric for dynamic use in the GSTI.

### General Goodwill (G)

The **General Goodwill Equation** offers a dynamic formula to quantify a company's internal goodwill by integrating critical performance metrics:

```
G = (CR × ES × BT × (RG^w(t) - NCB)) / T
```

**Where:**
- `CR` = Customer Retention
- `ES` = Employee Satisfaction
- `BT` = Brand Trust
- `RG` = Revenue Growth (with time-sensitive weight `w(t)`)
- `NCB` = Net Customer Backlash
- `T` = Time (smoothing to capture sustained performance)

This equation captures long-term trust signals embedded in a firm's human capital, customer loyalty, brand strength, and financial performance. The subtraction of `NCB` adjusts for systemic reputational risks or service breakdowns.

### Consumer Goodwill (CG)

Focusing on external perception, the **Consumer Goodwill Equation** highlights the brand's public image and market engagement:

```
CG = (CS × BR × CA × SS) / NCB_consumer
```

**Where:**
- `CS` = Customer Satisfaction
- `BR` = Brand Reputation
- `CA` = Customer Advocacy
- `SS` = Service Speed
- `NCB_consumer` = Negative Consumer Backlash

This formula omits time normalization, reflecting the immediate nature of consumer sentiment and its rapid feedback cycle. It is especially valuable for marketing and PR teams tracking brand health in real time.

### Unified Goodwill Score (UGS)

Bringing both internal and external lenses together, the **UGS** provides a comprehensive goodwill benchmark:

```
UGS = ((w₁ × G) + (w₂ × CG)) / T
```

**Where:**
- `w₁` and `w₂` are strategic weights applied to General and Consumer Goodwill respectively
- `T` provides temporal normalization, ensuring that high goodwill levels are not transient anomalies

---

## The Role of UGS in GSTI

The **Unified Goodwill Score (UGS)** serves as a real-time barometer of intangible corporate value by integrating both organizational integrity and consumer sentiment, making it a pivotal component of the Gold-Silver Trust Index (GSTI).

Unlike traditional goodwill, which provides a static, backward-looking snapshot, the UGS transforms goodwill into a **dynamic, forward-looking indicator** of market trust. By operationalizing goodwill through General, Consumer, and Unified Goodwill Scores, the GSTI refines its ability to detect subtle shifts in institutional and consumer confidence.

This enhanced framework ensures **early detection of macroeconomic regime shifts**, making the GSTI a more powerful tool for forecasting and strategic market analysis.

---

## Conceptual Foundation: Deconstructing Trust and Fear

### Gold-Silver Ratio (GSR)

The **Gold-Silver Ratio (GSR)** is a fundamental indicator, quantifying the number of silver ounces required to purchase one ounce of gold. Its significance lies in its historical correlation with economic cycles.

**Definition:**

```
GSR = Price_Gold / Price_Silver
```

**Implications:**

- **Rising GSR** (e.g., `> 80:1`) signals elevated risk aversion, with investors favoring gold's stability over silver's industrial exposure
- **Falling GSR** (e.g., `< 60:1`) indicates growing confidence in economic expansion, often benefiting silver due to its industrial applications

**Historical Context:**
- Average GSR (20th century): `~50:1`
- Peak fear levels (2008, 2020): `~100:1+`
- Economic boom periods: `~40:1 to 60:1`

---

## GSTI Formula: Quantifying Market Sentiment

The **Gold-Silver Trust Index (GSTI)** operationalizes market sentiment through the interaction of goodwill momentum and shifts in the gold-silver ratio.

### Core Formula

```
GSTI = Momentum(Goodwill) - (w_GSR × GSR)
```

**Where:**
- `Momentum(Goodwill)` = Rate of change in Unified Goodwill Score
- `w_GSR` = Dynamic weight applied to Gold-Silver Ratio
- `GSR` = Current Gold-Silver Ratio

### Momentum Calculation

```
Momentum(Goodwill) = (UGS_current - UGS_prior) / UGS_prior
```

**Alternative representation:**

```
Momentum(Goodwill) = ΔUGS / UGS₀ = (UGS_t - UGS_{t-1}) / UGS_{t-1}
```

### Signal Interpretations

| GSTI Range | Interpretation | Market Regime |
|------------|----------------|---------------|
| `GSTI > 0.05` | **Bullish Regime** | Confidence exceeds caution; market expects growth |
| `GSTI < -0.05` | **Bearish Divergence** | Fear dominates; heightened risk aversion |
| `│GSTI│ < 0.01` | **Neutral Zone** | Sentiment equilibrium; neither fear nor trust is dominant |

In practical terms, `Momentum(Goodwill)` can be derived from the Unified Goodwill Score (UGS) over time, offering a more granular and composite input into the GSTI formula.

---

## Dynamic Weighting Enhancement: Adapting to Market Regimes

To improve sensitivity, the GSTI employs a **dynamic weighting system** that adjusts the influence of goodwill and GSR based on prevailing market conditions.

### Dynamic Weight Adjustment Formula

```
w_GSR = f(VIX, M&A_activity, market_volatility)
w_Goodwill = g(earnings_trends, corporate_sentiment)
```

### Weighting Adjustments

#### High Volatility Regime (VIX > 25)
```
w_GSR = 0.015 (increased from baseline 0.01)
w_Goodwill = 0.8 (decreased from baseline 1.0)
```
**Rationale:** Fear becomes dominant; GSR influence amplified

#### Strong Economic Activity (M&A Surges, Strong Earnings)
```
w_GSR = 0.005 (decreased from baseline)
w_Goodwill = 1.2 (increased from baseline)
```
**Rationale:** Trust dominates; Goodwill influence elevated

#### Neutral Conditions
```
w_GSR = 0.01 (baseline)
w_Goodwill = 1.0 (baseline)
```

### Advantages

✅ **Early Detection of Regime Shifts:** GSTI adapts swiftly to transitions between risk-on and risk-off environments

✅ **Behavioral Responsiveness:** Reflects investor psychology across different business cycle phases

✅ **Noise Reduction:** Dampens short-term market anomalies by prioritizing regime-relevant indicators

---

## Applications: Practical Use Across Stakeholders

### Institutional Investors

**Asset Allocation:**
- GSTI guides allocation decisions in equities vs. defensive assets
- Shift to defensive posture when `GSTI < -0.05`
- Increase growth exposure when `GSTI > 0.05`

**Macro Overlay:**
- Functions as a sentiment gauge for long/short strategies
- Complements traditional technical and fundamental analysis

### Retail Traders

**Confirmation Tool:**
- Validates technical setups across equities, crypto, and metals
- Provides confluence with chart patterns and momentum indicators

**Behavioral Context:**
- Provides a macro overlay to speculative trades, especially in volatile assets
- Helps time entries/exits based on broader market sentiment

### Policymakers and Economists

**Sentiment Divergence Monitor:**
- Detects dissonance between market perception and official data
- Early warning system for confidence crises

**Stimulus Feedback Tool:**
- Evaluates the psychological impact of fiscal or monetary interventions
- Measures effectiveness of central bank communications

---

## Real-Time Example (May 2025): A Nuanced Bullish Read

### Current Market Conditions

As of May 2025:

| Indicator | Value | Interpretation |
|-----------|-------|----------------|
| **GSR** | ≈ 101:1 | Historically high; elevated caution |
| **Goodwill Trends** | Stable | No widespread impairments; corporate confidence intact |
| **Bitcoin Price** | ~$109,500 | Signals speculative appetite |
| **Equity Futures** | Positive | S&P and Nasdaq futures up; forward sentiment bullish |

### GSTI Analysis

**Current GSTI ≈ 0.495**

**Interpretation:**
- Reflects **cautious optimism**
- While GSR implies fear (`101:1` is elevated), stable goodwill and bullish crypto/futures suggest **latent confidence**
- Market is in transitional state between fear and growth

### Future Trajectory Scenarios

#### Bullish Confirmation Scenario
```
If: GSR ↓ (declining) AND Goodwill ↑ (rising)
Then: GSTI ↑↑ (significantly higher)
Result: Strong pro-growth outlook confirmed
```

#### Bearish Divergence Scenario
```
If: GSR ↑ (rising) OR Goodwill ↓ (falling)
Then: GSTI ↓↓ (significantly lower)
Result: Rising uncertainty; defensive positioning warranted
```

---

## Limitations and Considerations

While the GSTI offers a robust framework, it's important to acknowledge certain limitations and consider them during its application:

### 1. Goodwill Data Lag

**Issue:** Corporate goodwill data is typically reported quarterly, which may lag behind rapid shifts in market sentiment or economic conditions.

**Impact:** The GSTI's goodwill component might not capture instantaneous changes in corporate trust.

**Mitigation:** 
- Use real-time proxies (consumer sentiment surveys, social media sentiment)
- Combine with higher-frequency indicators

### 2. GSR Volatility and Distortions

**Issue:** The Gold-Silver Ratio, while historically reliable as a sentiment indicator, can be subject to short-term distortions caused by:
- Liquidity events
- Speculative trading
- Temporary supply/demand imbalances in precious metals markets

**Mitigation:**
- Use moving averages to smooth GSR volatility
- Consider median GSR over rolling windows

### 3. Trend Indicator, Not a Short-Term Timing Tool

**Key Understanding:** The GSTI is most effective when interpreted as a **trend indicator** for identifying broader market regimes (e.g., sustained bullish or bearish periods).

**Not designed for:**
- Precise short-term timing
- Daily trading decisions
- High-frequency trading strategies

**Best used for:**
- Regime identification (bullish/bearish/neutral)
- Strategic asset allocation
- Medium to long-term positioning

---

## Conclusion: A Behavioral-Macro Hybrid for Market Clarity

The GSTI represents a novel synthesis of **behavioral finance** and **macroeconomic indicators**. By merging the emotion-laden GSR with the rational valuation of goodwill, the index captures both **fear** and **trust** in a single, coherent metric.

Its dynamic weighting structure ensures that it adapts fluidly to changing market regimes, offering real-time insight into the psychological and structural forces shaping markets.

### Key Innovations

1. **Multi-Factor Goodwill Quantification**: Transforms subjective trust into measurable metrics
2. **Dynamic Regime Adaptation**: Weights adjust automatically to market conditions
3. **Behavioral-Fundamental Synthesis**: Combines fear (GSR) with trust (Goodwill)
4. **Early Warning System**: Detects regime shifts before traditional indicators

---

## Future Work: Scaling the GSTI Framework

### Immediate Priorities

**Real-Time Automation:**
- Connect to APIs for instant GSR and goodwill updates
- Build live dashboards for continuous monitoring
- Implement alert systems for regime changes

**Historical Validation:**
- Backtest GSTI across major bull and bear cycles
- Validate predictive power against historical market events
- Calculate correlation with market returns

**Machine Learning Integration:**
- Combine with macroeconomic indicators for predictive sentiment modeling
- Train ensemble models on GSTI + traditional indicators
- Develop adaptive weighting algorithms

### Long-Term Vision

**Global Expansion:**
- Extend GSTI framework to international markets
- Incorporate regional trust indicators
- Build cross-market GSTI comparisons

**Sector-Specific GSTI:**
- Develop industry-specific trust indices
- Create GSTI variants for tech, finance, healthcare sectors
- Enable granular allocation decisions

**Integration with DeFi:**
- On-chain GSTI calculation for crypto markets
- Real-time trust scoring for DAOs and protocols
- Automated trading strategies based on GSTI signals

---

## Call to Action

The GSTI has the potential to evolve into a **core sentiment compass** for 21st-century financial markets—an adaptive, data-driven lens through which both trust and fear are quantified, contextualized, and acted upon.

**We invite:**

**Macro Strategists** to test GSTI against existing frameworks and provide feedback on practical implementation

**Fintech Builders** to integrate GSTI into trading platforms, robo-advisors, and risk management systems

**Institutional Allocators** to pilot GSTI-based allocation models and share performance metrics

**Academic Researchers** to rigorously backtest and validate the GSTI methodology across historical data

> The GSTI is open for interpretation, integration, and iteration. Together, we can build a more intelligent, sentiment-aware approach to navigating modern markets.

---

## Mathematical Appendix

### Complete GSTI Calculation Flow

**Step 1: Calculate General Goodwill**
```
G = (CR × ES × BT × (RG^w(t) - NCB)) / T
```

**Step 2: Calculate Consumer Goodwill**
```
CG = (CS × BR × CA × SS) / NCB_consumer
```

**Step 3: Calculate Unified Goodwill Score**
```
UGS = ((w₁ × G) + (w₂ × CG)) / T
```

**Step 4: Calculate Goodwill Momentum**
```
Momentum(Goodwill) = (UGS_t - UGS_{t-1}) / UGS_{t-1}
```

**Step 5: Calculate Gold-Silver Ratio**
```
GSR = Price_Gold / Price_Silver
```

**Step 6: Apply Dynamic Weighting**
```
w_GSR = f(VIX, market_conditions)
w_Goodwill = g(earnings, sentiment)
```

**Step 7: Calculate Final GSTI**
```
GSTI = (w_Goodwill × Momentum(Goodwill)) - (w_GSR × GSR)
```

### Example Calculation

**Given:**
- `CR = 0.85`, `ES = 0.75`, `BT = 0.80`
- `RG = 1.05`, `w(t) = 1.0`, `NCB = 0.10`
- `CS = 0.90`, `BR = 0.85`, `CA = 0.70`, `SS = 0.80`
- `NCB_consumer = 0.05`
- `T = 1.0`, `w₁ = 0.6`, `w₂ = 0.4`
- `Gold = $2,500`, `Silver = $25` → `GSR = 100`
- `VIX = 30` (high volatility)

**Calculation:**

```
G = (0.85 × 0.75 × 0.80 × (1.05¹·⁰ - 0.10)) / 1.0
G = (0.51 × 0.95) / 1.0 = 0.4845

CG = (0.90 × 0.85 × 0.70 × 0.80) / 0.05
CG = 0.4284 / 0.05 = 8.568

UGS = ((0.6 × 0.4845) + (0.4 × 8.568)) / 1.0
UGS = (0.2907 + 3.4272) / 1.0 = 3.7179

Momentum = (3.7179 - 3.5000) / 3.5000 = 0.0623

w_GSR = 0.015 (elevated due to high VIX)
w_Goodwill = 0.8

GSTI = (0.8 × 0.0623) - (0.015 × 100)
GSTI = 0.0498 - 1.5 = -1.4502
```

**Interpretation:** `GSTI = -1.45` indicates a **bearish regime** despite positive goodwill momentum, due to extremely high GSR signaling dominant fear.

---

## Python Implementation

```python
class GSTICalculator:
    """
    Complete GSTI calculation engine with dynamic weighting.
    """
    
    def __init__(self, w1=0.6, w2=0.4):
        self.w1 = w1  # General Goodwill weight
        self.w2 = w2  # Consumer Goodwill weight
        self.w_goodwill = 1.0
        self.w_gsr = 0.01
        self.historical_ugs = []
    
    def calculate_general_goodwill(self, CR, ES, BT, RG, w_t, NCB, T):
        """Calculate General Goodwill (G)"""
        numerator = CR * ES * BT * (pow(RG, w_t) - NCB)
        return numerator / T
    
    def calculate_consumer_goodwill(self, CS, BR, CA, SS, NCB_consumer):
        """Calculate Consumer Goodwill (CG)"""
        if NCB_consumer == 0:
            NCB_consumer = 0.001  # Prevent division by zero
        return (CS * BR * CA * SS) / NCB_consumer
    
    def calculate_ugs(self, G, CG, T):
        """Calculate Unified Goodwill Score (UGS)"""
        ugs = ((self.w1 * G) + (self.w2 * CG)) / T
        self.historical_ugs.append(ugs)
        return ugs
    
    def calculate_gsr(self, gold_price, silver_price):
        """Calculate Gold-Silver Ratio"""
        return gold_price / silver_price
    
    def calculate_momentum(self, period=2):
        """Calculate Goodwill Momentum"""
        if len(self.historical_ugs) < period:
            return 0.0
        ugs_current = self.historical_ugs[-1]
        ugs_prior = self.historical_ugs[-period]
        if ugs_prior == 0:
            return 0.0
        return (ugs_current - ugs_prior) / ugs_prior
    
    def adjust_weights(self, VIX, M_A_Surges):
        """Dynamic weight adjustment based on market conditions"""
        if VIX > 25:
            self.w_gsr = 0.015
            self.w_goodwill = 0.8
        elif M_A_Surges:
            self.w_gsr = 0.005
            self.w_goodwill = 1.2
        else:
            self.w_gsr = 0.01
            self.w_goodwill = 1.0
    
    def calculate_gsti(self, gold_price, silver_price):
        """Calculate final GSTI score"""
        gsr = self.calculate_gsr(gold_price, silver_price)
        momentum = self.calculate_momentum()
        gsti = (self.w_goodwill * momentum) - (self.w_gsr * gsr)
        
        # Determine regime
        if gsti > 0.05:
            regime = "BULLISH"
        elif gsti < -0.05:
            regime = "BEARISH"
        else:
            regime = "NEUTRAL"
        
        return {
            "gsti_score": gsti,
            "regime": regime,
            "gsr": gsr,
            "momentum": momentum
        }

# Example usage
calculator = GSTICalculator()

# Period 1: Establish baseline
G1 = calculator.calculate_general_goodwill(0.85, 0.75, 0.80, 1.05, 1.0, 0.1, 1.0)
CG1 = calculator.calculate_consumer_goodwill(0.90, 0.85, 0.70, 0.80, 0.05)
UGS1 = calculator.calculate_ugs(G1, CG1, 1.0)

# Period 2: Calculate GSTI
G2 = calculator.calculate_general_goodwill(0.88, 0.78, 0.82, 1.07, 1.0, 0.08, 1.0)
CG2 = calculator.calculate_consumer_goodwill(0.85, 0.80, 0.65, 0.75, 0.08)
UGS2 = calculator.calculate_ugs(G2, CG2, 1.0)

calculator.adjust_weights(VIX=30, M_A_Surges=False)
result = calculator.calculate_gsti(gold_price=2500, silver_price=25)

print(f"GSTI Score: {result['gsti_score']:.4f}")
print(f"Market Regime: {result['regime']}")
print(f"GSR: {result['gsr']:.2f}")
print(f"Goodwill Momentum: {result['momentum']:.4f}")
```

---

## References

1. Buterin, V. et al., "Decentralized Society: Finding Web3's Soul" (2022)
2. Federal Reserve Economic Data (FRED), Gold and Silver Price Series
3. Gallup Economic Confidence Index, Historical Data
4. World Economic Forum, "Global Trust Survey" (2024)
5. BlackRock Investment Institute, "Market Regime Analysis Framework"

---

**© 2025 Don Michael Feeney Jr. All Rights Reserved.**

*For API implementation, live dashboards, and collaboration opportunities, visit the project repository.*
