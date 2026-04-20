# Exam PA: Predictive Analytics
## Original Case-Study Questions

---

## Question 1: Exploratory Data Analysis
**Difficulty:** 5  
**Topic:** EDA — Understanding Data, Identifying Patterns and Anomalies

**Scenario:**
An insurance company has collected 18 months of data on 50,000 auto insurance policyholders. The dataset includes: age, gender, miles driven per year, traffic violations in past 5 years, claim frequency (0, 1, 2, 3+ claims), claim severity (average claim amount in dollars), and insurance premium paid. Initial EDA reveals:
- Claim frequency is heavily right-skewed (85% have 0 claims, 10% have 1, 5% have 2+)
- Age distribution is relatively uniform from 18-80
- Miles driven per year shows a bimodal distribution with peaks at ~8,000 and ~15,000
- Premium paid ranges from $500 to $5,000 with no obvious pattern
- 3% of records have missing severity values (only for policyholders with 0 claims)

**Question:**
Given these observations, which is the most appropriate next step in EDA?

**(A)** Immediately build a linear regression model to predict claim severity using all variables. The bimodal distribution of miles driven suggests two distinct customer segments, so include an interaction term between miles and age.

**(B)** Investigate the bimodal pattern in miles driven by examining whether it corresponds to city vs. rural drivers, commuters vs. non-commuters, or data collection periods. Separately explore the relationship between claim frequency and the potential segments; determine whether missing severity values are Missing Completely At Random (MCAR) or Missing At Random (MAR).

**(C)** Exclude the 3% of missing severity values and all records with 0 claims (since they contribute little information), then model claim severity on the remaining 15% of data using only drivers with claims.

**(D)** Create a single indicator variable "High Risk" = 1 if claims ≥ 1, else 0. Use this as the response variable and ignore severity to simplify the model. The right-skewed claim frequency is problematic for standard regression.

**(E)** Aggregate the data by age group and gender to reduce noise, then build a logistic regression to predict the probability of any claim occurring. The bimodal distribution of miles should be handled by centering and scaling.

**Correct Answer:** **(B)**

**Solution:**

This question tests the candidate's approach to EDA and understanding of how exploratory findings should guide subsequent analysis decisions.

**Why (B) is Correct:**

The answer correctly prioritizes deeper investigation of key patterns:

1. **Bimodal Distribution of Miles Driven:**
   - The two peaks suggest distinct behavioral groups (e.g., urban vs. rural commuting patterns)
   - Understanding these segments is critical because claim frequency and severity likely differ by segment
   - Example: rural drivers (high annual miles) may have longer commutes but lower accident rates; city drivers may drive less but face more congestion-related accidents
   - Action: Segment the data and analyze claim patterns separately; this may inform feature engineering or model stratification

2. **Missing Severity Values (MCAR vs. MAR):**
   - The fact that severity is missing only for 0-claim policyholders is not random; it's a structural feature
   - Missing severity is Missing Not At Random (MNAR), since the absence is directly caused by the claim frequency value
   - Implications:
     - Cannot simply impute or delete these rows
     - May need to model claim severity separately for sub-populations with claims
     - Cannot directly use "overall severity" as a predictor for all policyholders
   - Action: Separate the analysis; predict claim frequency first, then severity conditional on frequency > 0

**Why Other Options Are Incorrect:**

**(A)** INCORRECT — Premature modeling:
- Suggests building a linear regression before understanding the data structure
- Assumes the bimodal pattern can be captured via an interaction term, but this is speculation without investigation
- Ignores the missing severity problem (3% of data)
- Violates the principle that EDA must precede modeling

**(C)** INCORRECT — Destructive exclusion:
- Removing 85% of the data (0-claim policyholders) eliminates the most common outcome
- Excluding missing values without understanding the mechanism leads to biased analysis
- The 0-claim group is extremely informative; claim frequency itself is a key variable to model
- Severity should be modeled separately for claimants (those with claims ≥ 1)

**(D)** INCORRECT — Oversimplification:
- Creates a binary response by losing information (converting severities to binary discards valuable data)
- Misdiagnoses the issue: right-skewness is not problematic; Poisson or gamma regression handles it well
- Claim frequency (0, 1, 2, 3+) is count data, not binary (claim vs. no-claim)
- This approach throws away actionable information

**(E)** INCORRECT — Inappropriate aggregation:
- Aggregating to the age/gender level eliminates individual-level variation and reduces sample size
- Centering and scaling addresses distributions but doesn't address the bimodal structure
- Ignores the EDA findings (missing data, potential segments, skewed outcomes)
- Loss of granularity reduces predictive power

**Key Principles for EDA Illustrated:**

1. **Investigate patterns, don't assume:** The bimodal distribution needs explanation before modeling
2. **Understand missing data mechanisms:** MCAR, MAR, and MNAR require different handling
3. **Preserve information:** Right-skewness and class imbalance are not problems to hide; they're features to model appropriately
4. **Separate concerns:** Claim frequency and severity are likely generated by different mechanisms; analyze separately
5. **Segment data when appropriate:** Distinct customer segments may require different models

**Next Steps After (B):**
- Confirm the source of bimodality (urban vs. rural, job type, etc.)
- Build separate models: (1) claim frequency for all policyholders, (2) claim severity for claimants only
- Use segments as stratification variables or predictors in subsequent models

---

## Question 2: Feature Engineering and Variable Selection
**Difficulty:** 6  
**Topic:** Feature Engineering — Creating Meaningful Predictors, Variable Selection

**Scenario:**
A health insurance company wants to predict medical cost inflation (% increase in annual medical costs year-over-year) for 8,000 individual policyholders. Raw data includes: age, gender, BMI, smoking status, zip code (5 digits), provider network (HMO, PPO, POS), number of prescriptions filled, hospital admissions count, emergency room visits, and prior year medical cost.

The modeler creates the following candidate features:
1. Age groups: (18-30, 31-45, 46-60, 60+)
2. BMI categories: (Underweight <18.5, Normal 18.5-24.9, Overweight 25-29.9, Obese ≥30)
3. Zip code as a categorical variable with 4,000 unique values
4. "Risk Score" = 2×(Smoking) + 1.5×(Hospital Admissions) + 0.5×(ER Visits) - 0.3×(Prior Cost in $10Ks)
5. Interaction: Smoking × Age (6 interaction terms)
6. Polynomial: Age², Age³ (for non-linear age effects)

**Question:**
Which feature(s) are most problematic for predictive modeling?

**(A)** Zip code as a categorical variable with 4,000 unique values will cause overfitting and multicollinearity. Remove it entirely to improve model stability.

**(B)** Age groups and BMI categories transform continuous variables into categorical form, losing information. Retain the original continuous variables and use splines or polynomials for non-linearity instead.

**(C)** The "Risk Score" feature is a domain-expert weighted combination that will reduce model flexibility and force relationships not supported by data. The model should learn feature weights directly rather than using pre-specified scores.

**(D)** Zip code and Age² are the most problematic. Zip code has excessive dimensionality (4,000 categories) and weak signal for medical costs; Age² redundantly captures information already in interaction terms. Drop both.

**(E)** The Smoking × Age and Age² interactions are excellent candidates for removal. Smoking is binary and age effects are likely captured by the continuous age variable directly. These create noise without adding signal.

**Correct Answer:** **(D)**

**Solution:**

This question tests feature engineering judgment: understanding when to create new features, when to transform, and when to exclude—balancing signal, noise, and overfitting risk.

**Analysis of Each Feature:**

| Feature | Role | Evaluation | Decision |
|---------|------|-----------|----------|
| Age groups | Binning | Loses granularity; consider only if age effects are step-function | Conditional |
| BMI categories | Binning | Simplifies interpretation; acceptable if effects are non-linear | Accept |
| Zip code (4,000) | Categorical | Extreme dimensionality; curse of dimensionality risk | **REMOVE** |
| Risk Score | Weighted combo | Domain expertise can be valuable; but may constrain learning | Caution |
| Smoking × Age | Interaction | Plausible (smoking harm varies by age); worth testing | Keep |
| Age², Age³ | Polynomial | Captures non-linear age effects; useful for U-shaped or cubic patterns | Keep |

**Problem Analysis:**

**1. Zip Code as 4,000 Categories (MAJOR PROBLEM):**

- Sample size: 8,000 policyholders, 4,000 zip codes → average 2 per zip code
- Creating 4,000 binary indicators leads to:
  - **Curse of dimensionality:** 4,000 features >> 8,000 observations
  - **Overfitting:** Rare zip codes have 1-2 samples; model will memorize them
  - **Sparsity:** Coefficient estimates are unstable when most categories are rare
  - **Validation problems:** Many zip codes may not appear in training set
- Better approaches:
  - Aggregate zip codes to regions (e.g., 50 regions)
  - Use zip-code-level summary statistics (e.g., mean cost, urbanicity) as predictors
  - Target encoding: encode zip code by mean medical cost in that zip
  - Exclude zip code if no strong a priori reason to believe location matters

**2. Age² / Age³ (EVALUATE TOGETHER, MAY KEEP):**

- Polynomials capture curvature in age-cost relationship
- Example: Medical costs may increase slowly in youth, rapidly in old age (non-linear pattern)
- Not redundant with Smoking × Age (which captures interaction, not univariate non-linearity)
- Decision: **KEEP if EDA shows non-linear age effects; REMOVE if relationship is approximately linear**

**3. Smoking × Age (LIKELY KEEP):**

- Plausible interaction: smoking's harmful effect may amplify with age
- 6 terms (one for each age category × smoking) capture this
- Not redundant with Age² (which is univariate)
- Decision: **KEEP if domain knowledge or EDA supports interaction**

**4. Risk Score (CAUTION):**

- Pre-specified weighted combination of features
- Pros: Incorporates domain expertise; interpretable; reduces dimensionality
- Cons: Constrains model; assumes specified weights are correct
- Better approach: Include component variables separately; let model learn weights
- Compromise: Use as a baseline feature but allow model to adjust the weights
- Decision: **ACCEPTABLE if validated; REMOVE if domain experts uncertain**

**Analysis of Each Option:**

**(A)** PARTIALLY CORRECT but incomplete:
- Correctly identifies zip code dimensionality as problematic ✓
- Correctly recommends removal ✓
- But claims "multicollinearity" is the issue; the main problem is overfitting, not multicollinearity
- Multicollinearity occurs when predictors are correlated; 4,000 zip code dummies are not highly correlated with each other
- Does not address Age², which is also problematic

**(B)** INCORRECT — Loses valuable domain reasoning:
- Advocates retaining continuous age, not age groups
- While continuous age preserves information, age groups may be clinically relevant (e.g., Medicare eligibility at 65)
- BMI categories are sensible; medical guidelines use BMI categories (Normal, Overweight, Obese)
- Splines are good for capturing non-linearity but may overfit with 8,000 samples
- This option prioritizes granularity over domain knowledge

**(C)** INCORRECT — Overstates the cost of domain knowledge:
- The Risk Score is a pre-specified combination; this can be problematic if wrong
- But completely excluding expert judgment creates a different risk
- Best practice: Include component variables AND the score (score becomes one feature)
- Models do learn feature weights directly; the risk score just suggests a starting relationship
- This option is too rigid in rejecting domain expertise

**(D)** CORRECT — Identifies the two most pressing problems:
- Zip code with 4,000 categories is the most egregious overfitting risk
  - Sample size (8,000) cannot support 4,000 categories
  - Average cells (2 obs/category) lead to unstable estimates
  - **Primary issue: dimensionality and sparsity**
- Age² is problematic if Age² and Smoking×Age are both included:
  - Explanation: If age effects are primarily captured via Smoking×Age interactions, Age² may be redundant
  - However, this depends on EDA; if age alone shows non-linearity, Age² is valuable
  - The option calls Age² "redundant with interactions," which is reasonable if interactions already capture the non-linearity
  - **Secondary issue: potential redundancy; consider dropping one**
- Decision: **REMOVE zip code; consider removing Age² if interactions already model the non-linearity**

**(E)** INCORRECT — Dismisses potentially valuable interactions:
- Smoking status is binary, but interactions with continuous age are NOT binary; they create 6 terms
- Claim: "age effects are likely captured by continuous age directly"
  - This assumes the effect of age is the same regardless of smoking status
  - Medical evidence suggests otherwise (smoking + age interaction is plausible)
  - Example: 30-year-old non-smoker vs. smoker have small cost difference; 70-year-old smoker has much higher costs than non-smoker
- The option throws away a plausible and testable interaction
- Age² is also dismissed without justification

**Model-Building Implications:**

Starting feature set for the model:
- **KEEP:** Age (continuous), BMI (continuous or categories), Smoking, Provider Network, Prescriptions, Admissions, ER Visits, Prior Cost
- **KEEP:** Age² for non-linearity, Smoking × Age for interaction effects
- **CONSIDER:** Risk Score as one feature (not as a replacement for components)
- **REMOVE:** Zip code in categorical form (too many categories); use only if aggregated or encoded
- **TEST:** Remove Age² if model validation shows it's not improving predictions

**Key Learning Points:**
- Dimensionality vs. sample size: As a rule, avoid creating more features than √n (here, √8000 ≈ 90)
- Domain expertise + data-driven feature selection: Use both together
- Categorical variables with many levels (>100) often need aggregation or encoding
- Interactions: Plausible interactions (e.g., smoking × age) are worth testing
- Polynomials: Non-linearity in EDA justifies polynomial terms
- Risk scores: Can simplify interpretation but may constrain learning

---

## Question 3: GLM Specification — Distribution Family and Link Function
**Difficulty:** 6  
**Topic:** GLM — Choosing Distribution, Link Function, Model Assumptions

**Scenario:**
An actuary is building a GLM to predict annual claim amounts for workers' compensation cases. The response variable is claim amount (in dollars), observed on 2,000 claims. Summary statistics:
```
Mean:           $15,000
Median:         $8,500
Standard Dev:   $28,000
Min:            $100
Max:            $425,000
Skewness:       3.2 (right-skewed)
Excess Kurtosis: 8.5 (heavy-tailed)

Histogram shows:
- 60% of claims below $10,000
- 25% between $10,000-$25,000
- 15% between $25,000-$425,000
```

The actuary must choose a GLM specification. Candidate models:

**Option 1:** Normal distribution with identity link: E[Claim] = β₀ + β₁X₁ + β₂X₂
**Option 2:** Gamma distribution with log link: log(E[Claim]) = β₀ + β₁X₁ + β₂X₂
**Option 3:** Inverse Gaussian with log link: log(E[Claim]) = β₀ + β₁X₁ + β₂X₂
**Option 4:** Lognormal (not a GLM, but shown for comparison)

**Question:**
Which GLM specification is most appropriate for workers' compensation claim amounts?

**(A)** Option 1 (Normal + Identity) because the large sample size (n=2,000) ensures the Central Limit Theorem applies; the mean ($15,000) provides a good summary of the distribution.

**(B)** Option 2 (Gamma + Log) because claim amounts are positive, right-skewed, and have variance proportional to the mean (typical of Gamma). The log link ensures predictions remain positive and is interpretable.

**(C)** Option 3 (Inverse Gaussian + Log) because it has the highest kurtosis and is best for very heavy-tailed data like workers' compensation claims.

**(D)** Option 4 (Lognormal) because it is a standard approach for insurance claim modeling and directly corresponds to the log-normal distribution inherent in claim amounts.

**(E)** Options 2 and 3 are equally appropriate; the choice between Gamma and Inverse Gaussian should be made via likelihood ratio test or information criteria (AIC/BIC). Both distributions handle positive, right-skewed data with the log link.

**Correct Answer:** **(B)**

**Solution:**

This question tests understanding of GLM distribution selection based on data characteristics and the insurance context.

**Data Characteristics Analysis:**

| Characteristic | Observation | Implication |
|---|---|---|
| Range | Positive, $100 to $425,000 | Requires positive-support distribution |
| Skewness | 3.2 (right-skewed) | Rules out Normal (symmetric) |
| Kurtosis | 8.5 (heavy-tailed) | Heavy right tail; multiple large claims |
| Mean/Median | $15,000 / $8,500 | Mean >> Median → right skew |
| Variance | Very high (SD=$28,000) | Variance ≈ mean² (multiplicative, not additive) |

**Distribution Characteristics:**

| Distribution | Support | Variance | Shape | Typical Use |
|---|---|---|---|---|
| Normal | All real | Constant (σ²) | Symmetric | Continuous, unbounded data |
| Gamma | Positive | μ²/shape | Right-skewed | Positive, skewed, positive variance-mean relationship |
| Inverse Gaussian | Positive | μ³/shape | Right-skewed, heavy-tailed | Positive, very skewed, heavy tails |
| Lognormal | Positive | e^(2μ+σ²)(e^(σ²)-1) | Right-skewed | Log-transformed data is normal |

**Analysis of Each Option:**

**(A)** INCORRECT — Normal is inappropriate:
- Normal distribution has support on all real numbers; claims cannot be negative ✗
- Normal assumes symmetric distribution; skewness = 3.2 violates this ✗
- Identity link (linear predictor) can produce negative predictions if β₀ and coefficients are not carefully constrained
- Central Limit Theorem applies to sample means, not to the data distribution itself; large sample size doesn't fix the skewness ✗
- Normal is a poor choice for insurance claims data

**(B)** CORRECT — Gamma + Log is appropriate:
- **Distribution choice:**
  - Gamma is designed for positive, right-skewed data ✓
  - Excess kurtosis of 8.5 is within Gamma's range; Gamma can have varying kurtosis depending on shape parameter
  - Variance of Gamma is μ²/shape, exhibiting the multiplicative variance structure typical of claim amounts
  - Claims exhibit heteroskedasticity (variance increases with mean); Gamma naturally captures this
- **Link function:**
  - Log link ensures predictions are positive (no need to constrain coefficients)
  - Log link is interpretable: exponentiated coefficients represent multiplicative effects
  - Example: β₁ = 0.05 means a unit increase in X₁ multiplies expected claim by e^0.05 ≈ 1.05 (5% increase)
- **Fit to data:**
  - Right-skewness (3.2) matches Gamma's flexibility ✓
  - Positive claims match Gamma support ✓
  - Multiplicative variance structure typical of claims data ✓
- **Justification:**
  - Gamma + log is the standard specification for insurance claim modeling
  - It's parsimonious and interpretable
  - It handles the data characteristics naturally

**(C)** INCORRECT — Inverse Gaussian is overly specialized:
- Inverse Gaussian is more heavy-tailed than Gamma (higher kurtosis)
- While high kurtosis (8.5) might suggest Inverse Gaussian, Gamma is sufficient
- Inverse Gaussian is more specialized; used for very extreme heavy tails or inverse-distance relationships
- Choosing Inverse Gaussian over Gamma requires stronger evidence (e.g., EDA showing Inverse Gaussian fit better)
- Without that evidence, prefer the more parsimonious Gamma model
- Caveat: If model validation shows Inverse Gaussian fits better, it would be appropriate

**(D)** INCORRECT — Lognormal is not a GLM:
- Lognormal is not part of the exponential family of distributions (which GLMs are based on)
- While lognormal can be used for insurance claim modeling, it's not a GLM specification
- Lognormal requires transformation: fit the model on log(Claim), then exponentiate predictions
- Lognormal is a valid approach, but the question asks for a GLM specification
- Gamma + log provides similar benefits with GLM framework advantages (diagnostics, inference)

**(E)** PARTIALLY CORRECT but misleading:
- True that Gamma and Inverse Gaussian are both defensible for positive, skewed data ✓
- True that likelihood ratio tests or AIC/BIC can compare them ✓
- However, without evidence that Inverse Gaussian is superior, Gamma is preferred:
  - Gamma is more parsimonious (simpler, fewer parameters to estimate)
  - Gamma is the standard for claim modeling
  - Inverse Gaussian is specialized for very heavy tails (kurtosis > 10)
  - Starting with Gamma, then testing Inverse Gaussian if needed, is the correct approach
- This option over-complicates the choice when Gamma is the clear first choice

**Practical Modeling Approach:**

1. **Start with Gamma + log link** (most appropriate for standard claim modeling)
2. **Fit the model** and examine diagnostics (residuals, Q-Q plot, etc.)
3. **If diagnostics show poor fit**, test alternatives:
   - Inverse Gaussian if heavy tails are evident
   - Tweedie distribution if there are zero claims (inflated zeros)
4. **Compare models** using AIC/BIC if alternatives are reasonable
5. **Validate** on test data to ensure generalization

**Key Concepts:**

- **Exponential family distributions:** Normal, Poisson, Gamma, Inverse Gaussian all belong; Lognormal does not
- **Link functions:** Identity (Normal), log (Gamma, Poisson), logit (Binomial), inverse (Gamma alternative)
- **Variance structure:** Gamma has variance = mean²/shape (multiplicative); Normal has constant variance
- **Interpretation:** Log link coefficients are multiplicative; identity link coefficients are additive
- **Insurance context:** Claim amounts are positive, skewed, heavy-tailed → Gamma + log is standard

**Key Learning Points:**
- Data characteristics (positive, right-skew, heavy tail) guide distribution choice
- Variance structure matters: multiplicative (claim data) vs. additive (other data)
- Log link ensures positive predictions and provides interpretability
- Gamma is the standard for insurance claims; Inverse Gaussian is more specialized
- Always examine diagnostics before accepting a model specification

---

## Question 4: Model Comparison — Evaluating Performance Metrics
**Difficulty:** 6  
**Topic:** Model Comparison — AUC, Lift, Gini, Precision-Recall Trade-offs

**Scenario:**
An insurance company built two logistic regression models to predict claim occurrence (1 = claim, 0 = no claim) on a test set of 5,000 policyholders (Base rate: 20% have claims).

```
MODEL A (Simple: 5 features)
Test AUC:          0.72
Gini:              0.44
Lift at top 20%:   1.55
Precision at 20%:  0.31 (100/320 true claims at top 20%)
Recall at 20%:     0.25 (100/400 total claims)

MODEL B (Complex: 22 features)
Test AUC:          0.76
Gini:              0.52
Lift at top 20%:   1.82
Precision at 20%:  0.38 (152/400 true claims at top 20%)
Recall at 20%:     0.38 (152/400 total claims)

Model B was overfit on training data (training AUC = 0.82 vs. test AUC = 0.76)
but outperforms Model A on test set across all metrics.
```

The company wants to deploy one model for underwriting. Which model should they choose?

**(A)** Model A because it is simpler (5 features) and more interpretable. While Model B has higher AUC, simplicity and explainability are more important than a 0.04 AUC difference in insurance.

**(B)** Model B because it outperforms Model A on all test metrics (AUC, Gini, Lift, Precision). The train-test gap (0.06) is acceptable and does not indicate problematic overfitting. The higher precision (0.38) means better identification of actual claims.

**(C)** Model B for prediction, but with caution about generalization: the 0.06 train-test gap suggests overfitting. Recommend regularization (L1/L2) or feature selection before deployment. Monitor test performance on new data closely after deployment.

**(D)** Model A because overfitting on the training set (Model B: train 0.82 vs. test 0.76) indicates Model B will perform poorly on new data. Model A's conservative predictions and wider generalization margin are preferable.

**(E)** This is context-dependent: both models have sufficient discriminative ability (AUC > 0.70). Choose Model A if interpretability and lower operational risk are priorities; choose Model B if maximizing claims identification (precision/recall) is the priority.

**Correct Answer:** **(C)**

**Solution:**

This question tests practical model selection balancing performance, overfitting, and business context.

**Performance Metrics Explanation:**

| Metric | Formula | Interpretation |
|---|---|---|
| AUC | Area under ROC curve | Probability model ranks random claim higher than non-claim |
| Gini | 2×(AUC - 0.5) | Normalized AUC; ranges 0-1 |
| Lift at 20% | (True positive rate at 20%) / Base rate | How much better than random at targeting top 20% |
| Precision | TP / (TP + FP) | Of those predicted as claim, what % actually claimed |

**Metrics Comparison:**

| Metric | Model A | Model B | Difference | Interpretation |
|---|---|---|---|---|
| AUC | 0.72 | 0.76 | +0.04 | Model B is 4% better at ranking |
| Gini | 0.44 | 0.52 | +0.08 | Model B explains 8% more variance |
| Lift at 20% | 1.55 | 1.82 | +0.27 | Model B targets 27% more effectively |
| Precision at 20% | 0.31 | 0.38 | +0.07 | Model B is 7 percentage points more precise |
| Train-Test Gap | ~0.00 (no info given) | 0.06 | Model B shows overfitting risk |

**Analysis of Each Option:**

**(A)** INCORRECT — Overstates the importance of simplicity:
- "Simpler is better" principle is too rigid without context
- In insurance underwriting, better discrimination is critical (lower claims losses)
- 0.04 AUC improvement + 0.07 precision improvement is material, not negligible
- 5 features vs. 22 features: the difference in operationalization is minimal in modern systems
- The statement ignores the overfitting concern that should be addressed
- Choosing Model A purely for simplicity abandons real predictive gains

**(B)** INCORRECT — Downplays overfitting:
- Claims "0.06 train-test gap is acceptable," but this is a 7.3% drop in AUC
- For a test AUC of 0.76, a 0.06 gap suggests moderate overfitting risk
- True that all metrics favor Model B, but overfitting indicates generalization risk on future data
- "Does not indicate problematic overfitting" is false; 0.06 gap is concerning
- The option ignores the need for remediation (regularization, feature selection)
- Deploying without addressing overfitting risks performance deterioration on new data

**(C)** CORRECT — Balanced and practical:
- Correctly identifies Model B's superior performance across all metrics ✓
- Acknowledges the 0.06 train-test gap as an overfitting signal ✓
- Proposes concrete remediation (regularization, feature selection) ✓
- Recommends caution: monitor performance after deployment ✓
- Balances performance gains against generalization risk ✓
- Suggests a pathway forward: improve Model B before deployment, not abandon it
- This is the approach used by experienced practitioners

**(D)** INCORRECT — Overstates overfitting risk:
- Train-test gap of 0.06 is concerning but not disqualifying
- Overfitting is a matter of degree: Model B shows moderate overfitting, not severe
- Claim that Model A has a "wider generalization margin" is unsupported (no train-test gap data for Model A)
- Model A's lower test performance will likely be its actual performance on new data (not better)
- Rejecting Model B solely because of overfitting is overly conservative
- The correct approach is to address overfitting, not avoid the better model

**(E)** PARTIALLY CORRECT but too non-committal:
- Correctly states this is "context-dependent" ✓
- Correctly outlines the trade-off (interpretability vs. precision) ✓
- However, the answer doesn't address the overfitting issue in Model B
- Suggesting both models as acceptable evades the decision
- In practice, if Model B's overfitting is remedied (e.g., via regularization), it should be strongly preferred
- The answer is too wishy-washy for a practical modeling scenario

**Business Context for Insurance Underwriting:**

1. **Objective:** Identify claims to set appropriate premiums or deny risky policies
2. **Cost of error:**
   - False negative (miss a future claim): Underprices risk; direct loss
   - False positive (flag non-claimant as risky): Over-priced; customer dissatisfaction
3. **Implication:** Better discrimination (higher AUC/Lift) directly reduces expected loss
4. **Example:** Model B's 7% precision improvement means fewer false accusations of risk

**Recommended Action Plan:**

1. **Investigate overfitting in Model B:**
   - Examine which features contribute most to train-test gap
   - Check if 22 features include rare interaction terms or non-linear transforms causing instability
   
2. **Apply regularization:**
   - L1 (Lasso) penalty to shrink or eliminate weak features
   - L2 (Ridge) penalty to shrink all coefficients toward zero
   - Cross-validation to select regularization strength
   
3. **Feature selection:**
   - Remove features that don't improve test performance
   - Keep only features with stable coefficients and strong signal
   - Target: 10-15 features (better balance than 22)
   
4. **Revalidate:**
   - Retrain regularized Model B
   - Confirm train-test gap improves
   - Ensure test AUC remains ≥ 0.74 (better than Model A)
   
5. **Deploy with monitoring:**
   - Track performance on new data (production)
   - Compare predicted claim rate to actual
   - Retrain quarterly or when drift is detected

**Key Learning Points:**
- Overfitting is a red flag but not a reason to reject a model; it's a reason to address it
- Better performance metrics (AUC, Lift, Precision) are meaningful; ignore at business cost
- Train-test gaps of 5-7% are moderate; > 10% is severe
- Regularization and feature selection are standard techniques to reduce overfitting
- Post-deployment monitoring is essential for model maintenance
- Context matters: balance performance, complexity, and explainability

---

## Question 5: Overfitting Diagnosis — Train vs. Test Performance
**Difficulty:** 7  
**Topic:** Overfitting — Detecting and Interpreting Performance Gaps

**Scenario:**
A machine learning engineer built a gradient boosting model to predict health insurance plan switching (1 = switch plans, 0 = stay) on a large dataset of 100,000 enrollees. The model was trained on 60,000 observations and evaluated on a separate test set of 40,000 observations.

Performance metrics:

```
TRAINING SET (60,000 obs):
Accuracy:        0.876
AUC-ROC:         0.824
Precision:       0.685
Recall:          0.718
Log Loss:        0.312

TEST SET (40,000 obs):
Accuracy:        0.852
AUC-ROC:         0.791
Precision:       0.651
Recall:          0.684
Log Loss:        0.387

Performance Gaps:
Accuracy gap:    0.024 (2.4%)
AUC gap:         0.033 (4.0%)
Log Loss gap:    0.075 (24%)
```

The model has 250 features (100 raw features + 150 engineered/interaction terms). Feature importance analysis shows the top 30 features account for 80% of predictions; features 150-250 have near-zero importance.

**Question:**
What do these performance gaps indicate, and what action is most appropriate?

**(A)** The 4% AUC gap is modest and within expected sampling variation. The model is appropriately fit; no action is required. Focus on deployment and monitoring performance in production.

**(B)** The 24% log loss gap is concerning and indicates severe overfitting, likely from the 150 weakly-important features. Feature selection (retain top 50 features only) is urgently needed before deployment.

**(C)** The consistent gaps across all metrics (accuracy, AUC, log loss) suggest moderate generalization loss. The abundance of near-zero-importance features is likely contributing. Feature selection or regularization would improve expected performance on new data. Retraining with refined feature set is recommended.

**(D)** These gaps are typical for gradient boosting models due to their complexity. The 24% log loss gap reflects the model's learning capacity; it's not a sign of overfitting. Deploy the model as-is; monitor only accuracy on production data.

**(E)** The model is overfitting because the number of features (250) exceeds the rule-of-thumb ratio of 1 feature per 100 observations. The training AUC (0.824) proves the model learned true signals despite this imbalance.

**Correct Answer:** **(C)**

**Solution:**

This question tests the ability to diagnose overfitting from performance gaps, understanding different metrics' sensitivity to overfitting, and knowing when to take remedial action.

**Performance Gap Interpretation:**

| Metric | Train | Test | Gap | Type | Sensitivity |
|---|---|---|---|---|---|
| Accuracy | 0.876 | 0.852 | 2.4% | Modest | Low; insensitive to probability calibration |
| AUC | 0.824 | 0.791 | 4.0% | Moderate | Moderate; robust to class imbalance |
| Log Loss | 0.312 | 0.387 | 24% | Large | **High; sensitive to probability calibration** |

**Key Insight: Log Loss Gap is the Diagnostic:**

Log loss measures the model's probability calibration (how close predicted probabilities are to 0/1):
- Log Loss = -1/n * Σ[y_i * log(p_i) + (1-y_i) * log(1-p_i)]
- On training data, the model has learned to output well-calibrated probabilities
- On test data, the 24% gap means the model outputs overconfident probabilities (too close to 0/1)
- This is a hallmark of overfitting: the model learned peculiarities of training data that don't generalize

**AUC vs. Log Loss:**
- AUC measures ranking (does model rank claims higher than non-claims?) → less sensitive to overconfidence
- Log Loss measures probability calibration → highly sensitive to overconfidence
- The smaller AUC gap (4%) but larger Log Loss gap (24%) indicates:
  - Model still ranks test observations reasonably well (AUC 0.791 is good)
  - But predicted probabilities are poorly calibrated on test data (Log Loss 0.387 is worse than train)
  - Typical symptom: model outputs 0.95 for a test observation that actually doesn't switch (overconfident)

**Feature Importance Analysis:**

- Top 30 features = 80% of predictions
- Features 150-250 = ~0% importance
- This suggests 100 features (31-250) are noise or near-collinear with the top 30
- These weak features can fit training-set quirks without real signal
- On test data, these spurious patterns don't appear, causing performance degradation

**Analysis of Each Option:**

**(A)** INCORRECT — Dismisses concerning log loss gap:
- Claim: "4% AUC gap is modest and within sampling variation"
  - True that 4% is acceptable for AUC alone
  - But ignores the 24% log loss gap, which is much larger ✗
- "No action is required" is premature; the large log loss gap signals overfitting
- Deploying without addressing overfitting risks poor probability calibration in production
- Example: Model says "90% likely to switch" but only 60% actually do; this mispredicts business outcomes

**(B)** INCORRECT — Overstates the severity:
- 24% log loss gap is concerning, but not "severe"
- Recommends retaining "top 50 features only," but top 30 already capture 80% of signal
- Dropping features will likely improve log loss but may slightly reduce AUC
- "Urgently needed" overstates the situation; moderate action (not urgent) is appropriate
- The gaps don't indicate model failure, just poor calibration

**(C)** CORRECT — Balanced diagnosis and action:
- "Consistent gaps across metrics suggest moderate generalization loss" ✓
  - All metrics show performance degradation from train to test
  - Magnitude varies (2.4% to 24%) but direction is consistent
  - Indicates overfitting, not model failure
- "Abundance of near-zero-importance features is contributing" ✓
  - 100+ weak features can fit noise; feature selection is appropriate
- "Feature selection or regularization" are both valid remedies ✓
  - Feature selection: keep top 30-50, discard weak ones
  - Regularization: L1/L2 penalty shrinks weak features automatically
- "Retraining with refined feature set is recommended" ✓
  - Practical next step before deployment
  - Likely outcome: improved test performance, especially log loss

**(D)** INCORRECT — Mischaracterizes the issue:
- "24% log loss gap reflects learning capacity; it's not overfitting"
  - False dichotomy; gap between train and test performance is the definition of overfitting
  - Log loss gap is the clearest sign of overfitting in this case
- "Deploy the model as-is; monitor only accuracy" is risky
  - Model's probability calibration is poor; using probabilities for scoring/ranking will be inaccurate
  - Monitoring accuracy alone misses the calibration problem
  - Production users will observe that predicted probabilities don't match actual frequencies

**(E)** INCORRECT — Rule-of-thumb misapplied:
- "250 features exceeds 1 per 100 observations" (should be 1 per 100-200)
  - Actually, 250 features for 100,000 obs = 1 per 400, which is reasonable
  - Rule of thumb is a guideline, not a hard rule
- But the actual diagnosis (100+ weak features) is correct
- "Training AUC (0.824) proves the model learned true signals"
  - High training AUC is expected; it doesn't prove learning of true signals
  - Test performance is what proves generalization; here, AUC dropped to 0.791
- The reasoning is circular (high training performance proves good fit) and misses the train-test gap

**Remediation Strategy:**

**Option 1: Feature Selection**
```
1. Identify features with feature importance < threshold (e.g., 0.001)
2. Retrain model with top N features (e.g., 30-50)
3. Evaluate train-test gaps; if improved, proceed
4. Likely outcome: Test AUC drops slightly (0.791 → 0.785), Log Loss improves (0.387 → 0.35)
```

**Option 2: Regularization**
```
1. Add L1 (Lasso) or L2 (Ridge) penalty to gradient boosting
2. Tune regularization strength via cross-validation
3. Stronger regularization shrinks weak features automatically
4. Likely outcome: More stable train-test gaps, better calibration
```

**Option 3: Both (Recommended)**
```
1. Apply feature selection (remove bottom 50% by importance)
2. Apply regularization to the refined set
3. Cross-validate to ensure robust improvements
4. Retrain on full data; validate on new hold-out set
5. Expected outcome: Balanced performance on train and test
```

**Expected Results After Remediation:**
- Log Loss gap shrinks from 24% to <10%
- AUC remains above 0.79 on test set
- Probability calibration improves; predicted probabilities align with actual frequencies
- Model is ready for production deployment

**Key Learning Points:**
- Train-test performance gaps indicate overfitting; gaps > 5-10% warrant investigation
- Log loss is highly sensitive to overfitting; AUC is more robust
- Feature importance analysis reveals which features contribute; weak features often cause overfitting
- Feature selection and regularization are complementary remedies
- Probability calibration (log loss) is as important as ranking (AUC) for many business applications
- Always inspect gaps across multiple metrics; one metric may hide problems the others reveal

---

## Question 6: Communicating Results to Business Stakeholders
**Difficulty:** 6  
**Topic:** Model Interpretation — Explaining Complex Models to Non-Technical Audience

**Scenario:**
An actuarial team built a gradient boosting model to predict health claims (binary: claim/no claim) for a large group health insurance plan. The model achieved a test AUC of 0.78 and will be used to identify high-risk employees for targeted wellness programs.

The model inputs 15 features, including age, BMI, prior claims history, prescription fill patterns, job code, tenure, and healthcare utilization metrics. The team must present findings to the plan sponsor (a non-technical executive) and the benefits committee.

A team member proposes the following explanation:

> "Our gradient boosting model with hyperparameters (n_estimators=200, max_depth=6, learning_rate=0.05) achieves an AUC of 0.78, indicating good discriminative ability. Feature importance analysis (measured by SHAP values) reveals that prior claims history (SHAP importance=0.32) and age (0.18) are the dominant predictors. The model was trained on 50,000 observations with 60-40 train-test split and validated via 5-fold cross-validation."

**Question:**
Which of the following critiques is most valid regarding this explanation for business stakeholders?

**(A)** The explanation is appropriate because it correctly defines AUC (discriminative ability) and explains the train-test-validation split. This transparency is necessary for stakeholders to understand the model's rigor.

**(B)** The explanation is too technical and fails to translate model outputs into business impact. It mentions hyperparameters and SHAP values that executives don't understand. Instead, explain what the model does, what % of high-risk employees it identifies, and why those employees should be prioritized for wellness.

**(C)** The explanation is incomplete because it doesn't include the training algorithm's computational complexity or feature names. Including a full list of all 15 features and their SHAP values would improve clarity.

**(D)** The explanation is adequate for internal stakeholders but would benefit from a visual dashboard showing model predictions across the employee population. However, the technical details (AUC, SHAP values) should be retained to demonstrate scientific rigor.

**(E)** The explanation has a critical flaw: it doesn't explain why prior claims history and age are important predictors, which are domain-knowledge facts that stakeholders likely already know. The model should identify non-obvious patterns that were unknown before.

**Correct Answer:** **(B)**

**Solution:**

This question tests understanding of how to translate technical model results into actionable business insights for non-technical stakeholders.

**The Core Problem with the Proposed Explanation:**

The explanation is written for a peer data scientist, not for the plan sponsor (an executive or benefits manager). It includes:
- Hyperparameters (n_estimators=200, max_depth=6): Not actionable for stakeholders
- SHAP values: Technical jargon unfamiliar to most executives
- AUC=0.78: Implies good performance but doesn't connect to business benefit
- Validation methodology: Important for model credibility but presented without context

**What Stakeholders Actually Need to Know:**

1. **What does the model do?** Identifies employees likely to have medical claims
2. **How accurate is it?** "Out of 100 employees we predict will have claims, about 78 actually will" (translating AUC to practical terms)
3. **Who does it identify?** "Employees with prior claims and older age are at higher risk"
4. **What should we do?** "Enroll identified employees in wellness programs; we project 15-20% reduction in claims"
5. **Any risks?** "The model works on average; some low-risk employees may be flagged; others may be missed"

**Analysis of Each Option:**

**(A)** INCORRECT — Mistakenly defends the technical explanation:
- Claim: "This transparency is necessary"
  - While transparency is good, this explanation lacks transparency about business impact
  - Executives need transparency about *what the model will do*, not hyperparameter details
  - Wrong kind of transparency
- "Executives don't understand" or don't care about AUC, train-test splits, or SHAP values
- This explanation would likely confuse, not clarify, for the intended audience

**(B)** CORRECT — Identifies the exact problem:
- "Too technical and fails to translate model outputs into business impact" ✓
  - Hyperparameters and SHAP values are implementation details, not business-relevant outcomes
- "Executives don't understand these terms" ✓
  - Most plan sponsors and benefits committees lack machine learning training
  - Explaining a 200-tree gradient boosting model is unnecessary; they only care about results
- Proposes a better approach:
  - "What the model does": Predicts who will claim
  - "% of high-risk employees identified": Concrete number, actionable
  - "Why prioritize": Links to business goal (wellness program effectiveness)
- This is exactly how experienced practitioners present to non-technical audiences

**(C)** INCORRECT — Asks for more technical content:
- Suggests adding "computational complexity" and "full list of 15 features"
  - This adds more jargon, not clarity
  - Computational complexity is irrelevant to business stakeholders
  - A list of 15 features is overwhelming; executives care about the top 2-3 drivers
- All 15 feature names with SHAP values would confuse rather than clarify
- This doubles down on the problem, not solving it

**(D)** INCORRECT — Compromises by keeping technical details:
- Suggests a dashboard is good (visual is helpful) ✓
- But insists on retaining AUC, SHAP values, hyperparameters
  - "Scientific rigor" is demonstrated through validation methodology and external testing, not by explaining SHAP to executives
  - Rigor can be mentioned briefly ("model was validated on independent data") without technical detail
- This is a compromise that still fails to translate results for business users
- Technical details belong in an appendix for interested data scientists, not in the main presentation

**(E)** INCORRECT — Misses the point:
- Claims the model "doesn't explain why prior claims history and age are important"
  - Actually, the explanation does identify these as top predictors
  - But that's besides the point; the issue is not identifying what predicts, but explaining business relevance
- "The model should identify non-obvious patterns"
  - This is a misunderstanding; predictive models don't need to be surprising
  - Age and prior claims are obvious predictors of future claims (that's why they're informative)
  - The model's job is to identify individuals at risk, not to find surprising patterns
- This critique misunderstands the modeling objective

**Recommended Presentation for Stakeholders:**

**Opening:**
> "We've developed a model that identifies employees at high risk of medical claims. This lets us prioritize wellness programs where they'll have the most impact."

**Key Findings:**
> "The model identifies three main risk factors:
> - **Prior claims history:** Employees who filed claims in the past two years are 3-4x more likely to claim again
> - **Age:** Older employees (55+) have 2.5x higher claim rates than younger employees
> - **Prescription volume:** High medication users are 2x more likely to file claims
> 
> Using these factors, the model flags about 25% of your employee population as high-risk."

**Business Impact:**
> "For the identified high-risk group, we recommend intensive wellness programs. In similar populations, these programs have reduced claims costs by 15-20%. For your group, that could mean $500K-$1M in annual savings."

**Accuracy:**
> "We tested the model on employees it hasn't seen before. Out of 100 employees we predict will claim, about 78 actually do. This is strong performance—better than you'd expect by chance."

**Limitations:**
> "No model is perfect. Some low-risk employees will still claim; some identified as high-risk won't. Plan for about 20% misidentification."

**Next Steps:**
> "We recommend starting with the top 500 high-risk employees. Monitor their wellness program participation and claims outcomes over 6-12 months. If results meet expectations, expand to the full flagged population."

**What NOT to mention:**
- Gradient boosting algorithm
- Hyperparameters (n_estimators, max_depth, learning_rate)
- SHAP values, feature importance scores
- AUC (or only translate: "78% accuracy in predicting claims")
- Train-test splits (mention only in appendix if asked)
- Cross-validation details

**Technical Appendix (for data science peers):**
> "Model Specification:
> - Algorithm: Gradient Boosting (XGBoost)
> - Hyperparameters: n_estimators=200, max_depth=6, learning_rate=0.05
> - Validation: 5-fold cross-validation on 50,000 training observations
> - Test AUC: 0.78
> - Feature importance (SHAP):
>   - Prior claims history: 0.32
>   - Age: 0.18
>   - [remaining features...]"

**Key Learning Points:**
- **Audience adaptation:** Technical details for peers, business impact for executives
- **Translation:** AUC → "78 out of 100 predictions correct" (approximate)
- **Focus:** What to do next (business decision), not how the model works (technical detail)
- **Clarity over precision:** "About 3-4x higher risk" is clearer than "coefficient = 0.847 in log-odds scale"
- **Visual communication:** Dashboards, plots of risk distribution across employees, before/after wellness participation
- **Simplicity:** Lead with the top 3 factors; don't overwhelm with all 15 features
- **Limitations:** Acknowledge uncertainty; set realistic expectations

---

## Question 7: Ethical Considerations in Predictive Modeling
**Difficulty:** 7  
**Topic:** Ethics — Fairness, Bias, Discrimination, Transparency

**Scenario:**
An insurance company has developed a predictive model to assess health insurance claim risk using age, gender, BMI, and medical history. The model will be used to set premiums for individual market policies.

During model validation, the actuarial team discovers:

1. **Disparate Impact:** The model's claim risk scores are 25% higher on average for Black applicants vs. White applicants, even after controlling for age, BMI, and claimed medical history.

2. **Feature Correlation:** Race is not explicitly included in the model, but several features (neighborhood zip code, occupation, education) are correlated with race (r = 0.35-0.45).

3. **Model Performance:** The model has identical AUC (0.78) across racial groups, suggesting it predicts equally well for all groups.

4. **Business Pressure:** The pricing strategy (using this model) is projected to increase company revenue by $12M annually. Senior leadership wants to deploy immediately.

The team faces a decision on how to proceed.

**Question:**
Which approach best balances ethical concerns with business objectives?

**(A)** Deploy the model as-is. Identical AUC across racial groups indicates the model is unbiased. Differences in claim risk scores reflect real differences in applicant risk, not discrimination. Using the best available model is the most ethical approach.

**(B)** Deploy the model but adjust premium calculations to ensure equal prices across racial groups regardless of risk score. This eliminates disparate impact but may underestimate risk for some groups, reducing company profitability and eventually harming the entire pool.

**(C)** Conduct a full audit of feature engineering and data collection for potential bias. Review whether zip code, occupation, and education are legitimate risk factors vs. proxies for race. Consider removing correlated features, retraining without them, and re-evaluating trade-offs. Only deploy after addressing or accepting bias risks with full transparency to leadership and regulators.

**(D)** Postpone deployment and commission an independent third-party audit by legal and ethics experts. Involve community groups representing affected populations. This delays revenue but ensures alignment with regulatory expectations and public reputation.

**(E)** Implement an "explainability requirement": Before granting coverage, applicants can request an explanation of why they were assigned their risk score. This transparency allows individuals to contest decisions, providing a fairness check without preventing deployment.

**Correct Answer:** **(C)**

**Solution:**

This question tests understanding of ethical issues in predictive modeling, particularly bias, fairness, and discrimination—critical topics in modern actuarial practice.

**Foundational Concepts:**

**Disparate Impact vs. Disparate Treatment:**
- **Disparate treatment:** Explicitly using race in decision-making (illegal)
- **Disparate impact:** Neutral practice (age, BMI) but has different effects across racial groups (legally risky, ethically problematic)

**Bias in ML:**
- **Allocation bias:** Model systematically over/under-estimates for certain groups
- **Measurement bias:** Features that act as proxies for race without explicit mention
- **Sample bias:** Training data underrepresents certain populations

**The Problem Identified:**

1. **Disparate impact exists:** 25% higher scores for Black applicants is substantial
2. **Proxy variables:** Zip code, occupation, education correlate with race (0.35-0.45)
3. **Equal performance masks disparate impact:** AUC=0.78 for all groups means the model predicts equally well, but applies different scores; equal accuracy doesn't imply fairness

**Analysis of Each Option:**

**(A)** INCORRECT — Ignores ethical and legal risks:
- "Identical AUC indicates model is unbiased"
  - FALSE: Equal AUC means equal discrimination ability, not equal fairness
  - A model can predict equally well for all groups while applying different scores to each
  - This is the classic conflation of accuracy with fairness
- "Differences in scores reflect real differences in risk"
  - Possibly true, but the source matters: Are they driven by real biological/behavioral differences (age, BMI) or by proxy variables correlated with race?
  - Unclear without further analysis
- "Best model is most ethical"
  - Best by accuracy ≠ best by fairness
  - Deployment carries legal risk (fair lending violations) and reputational risk
- This approach prioritizes revenue over risk management

**(B)** INCORRECT — False solution:
- "Adjust premiums to ensure equal prices across racial groups"
  - This masks the underlying bias rather than addressing it
  - Equal prices don't eliminate the fact that the model scores groups differently
  - May violate actuarial principles if risk is genuinely different
- "Underestimate risk... harming the entire pool"
  - If the 25% difference is real, ignoring it creates adverse selection and cross-subsidies
  - But if it's a measurement artifact, pretending it's real is both unethical and unprofitable
- This is a band-aid that doesn't solve the root problem

**(C)** CORRECT — Balanced, professional approach:
- **Audit features:**
  - Is zip code a proxy for race or a legitimate risk factor (e.g., healthcare access)?
  - Is occupation (correlated with race) predictive of risk independently of health status?
  - Could education differences reflect data collection bias (e.g., missing info on some groups)?
- **Legitimate questions:**
  - Does the 25% difference persist after removing proxy variables?
  - If removed, does AUC drop materially? If not, proxies weren't carrying signal
  - Can the difference be explained by unmeasured confounders (e.g., chronic stress, environmental exposure) that should be captured differently?
- **Transparent decision-making:**
  - "Accept bias" is a valid choice if: (1) proxies are legitimate factors, (2) AUC improves materially, (3) leadership and board explicitly approve with legal review
  - "Reduce bias" is appropriate if: (1) proxies are not defensible, (2) removing them doesn't harm AUC, (3) regulators expect fairness
- **Expected outcomes:**
  - Option 1: Remove zip code/education, keep occupation (if defensible) → re-evaluate disparate impact
  - Option 2: Remove all three proxies → trade-off between fairness and accuracy
  - Option 3: Keep model but implement fairness constraint (e.g., maximum 10% score difference across groups) → balance fairness and accuracy
- **Regulatory compliance:**
  - Fair lending laws require avoiding unintentional discrimination
  - Full audit demonstrates "good faith" effort to comply
  - Transparency to regulators reduces legal risk
- This is the approach used by leading financial institutions and endorsed by the Consumer Financial Protection Bureau (CFPB)

**(D)** PARTIALLY CORRECT but overly cautious:
- "Independent third-party audit" is good ✓
- "Community groups and legal review" adds transparency ✓
- However, postponing deployment indefinitely is impractical:
  - Decision can't be fully ethical without deployment data (actual claims experience)
  - Waiting for perfect agreement from all stakeholders is unrealistic
  - Some version of insurance pricing must be used; delayed deployment doesn't solve the ethics
- Better: Proceed with audited model after addressing (C), but with monitoring
- This option is correct in spirit but too rigid in execution

**(E)** INCORRECT — Explainability is not a fairness solution:
- "Explainability allows individuals to contest decisions"
  - Transparency is good, but not sufficient for fairness
  - If a decision is discriminatory, explaining it doesn't make it non-discriminatory
  - Explainability is a best-practice complement, not a substitute for bias audit
- "Explainability provides fairness check"
  - Appeals processes help but don't prevent systemic bias
  - Example: If the model systematically denies coverage to a group, individual appeals won't fix the aggregate problem
- Example of insufficient ethics: "We explain why we scored you lower; if you disagree, you can appeal"
  - Doesn't address the underlying issue that the group is systematically scored lower
- This is "ethics theater"—appearing to address fairness without doing so

**Recommended Action Plan (Following Option C):**

**Phase 1: Audit (2-3 weeks)**
1. Correlation analysis: Quantify relationship between proxy variables and protected attributes
2. Feature importance breakdown: What % of model discrimination comes from proxy variables vs. legitimate factors?
3. Fair lending test: Simulate model performance after removing proxies
4. Legal review: Consult counsel on ECOA/FHA compliance risks

**Phase 2: Decision (1 week)**
Based on audit results:
- **If proxies are non-essential:** Remove them, retrain, validate
- **If proxies are essential for accuracy:** Discuss with leadership and board whether accuracy justifies fairness risks
- **If legitimate differences exist:** Implement fairness constraint (e.g., parity constraint) and retrain

**Phase 3: Implementation**
- Deploy model with approved adjustments
- Implement monitoring dashboard: AUC and disparate impact by group, quarterly updates
- Establish appeal process for applicants to contest scores

**Phase 4: Ongoing**
- Monitor actual claims by group; compare to model predictions
- Evaluate if 25% difference predicted risk materializes in practice
- Adjust pricing annually if actual experience differs from model
- Report to regulators (if required) and board on fairness metrics

**Key Ethical Principles:**

1. **Transparency:** Clearly disclose any known biases and remediation steps
2. **Accountability:** Board and leadership must explicitly approve final model, understanding fairness trade-offs
3. **Proportionality:** Accuracy gains don't justify unfair treatment of minorities
4. **Justification:** Proxy variables must be legitimate risk factors, not just correlated with race
5. **Monitoring:** Track model performance across groups after deployment; intervene if disparities widen

**Key Learning Points:**
- Equal accuracy across groups ≠ fair treatment; need to assess disparate impact separately
- Proxy variables (zip code, education) can encode historical discrimination; audit carefully
- Transparent decision-making about bias trade-offs is essential
- Deployment doesn't end ethics work; monitoring and adjustment are ongoing
- Explainability is important but not sufficient for fairness
- Legal compliance (ECOA, FHA) is a floor, not a ceiling; ethical practice often exceeds legal minimums
- Actuarial Standard of Practice (ASOPs) require addressing fairness and bias

---

# End of Exam PA Questions

**Answer Key Summary:**
1. (B) - Exploratory Data Analysis
2. (D) - Feature Engineering and Variable Selection
3. (B) - GLM Specification
4. (C) - Model Comparison
5. (C) - Overfitting Diagnosis
6. (B) - Communicating Results
7. (C) - Ethical Considerations
