"""
Exam PA (Predictive Analytics) Question Generator

Generates scenario-based analytical reasoning questions on:
- Exploratory Data Analysis
- Feature Engineering
- GLM Application
- Model Evaluation
- Overfitting & Regularization
- Communication & Ethics
"""

import random
import uuid
from typing import List, Dict, Any


class ExamPAGenerator:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    """Generates PA exam questions with scenario-based analytical reasoning."""

    @staticmethod
    def _generate_id() -> str:
        """Generate unique question ID."""
        return f"PA_{uuid.uuid4().hex[:8].upper()}"

    # ==================== EDA (8 methods) ====================

    @classmethod
    def missing_data_strategy(cls) -> Dict[str, Any]:
        """Decide strategy for handling missing data."""
        scenarios = [
            {
                "context": "A marketing dataset with 500k records and age missing in 2% of cases",
                "correct": "Impute with median age, then create missing indicator",
                "wrong": [
                    "Delete all rows with missing age",
                    "Use mean imputation without indicating missingness",
                    "Leave missing as zero",
                ]
            },
            {
                "context": "Historical claim data where claim amount is missing for denied claims (15% missing)",
                "correct": "Create two models: probability of non-zero claim, then claim amount given non-zero",
                "wrong": [
                    "Impute with zero",
                    "Delete claims with missing amounts",
                    "Impute with global mean",
                ]
            },
            {
                "context": "Insurance dataset with policyholder income missing for 5% (data acquisition issue)",
                "correct": "Impute using income proxy variables, document missingness pattern",
                "wrong": [
                    "Delete policyholder records",
                    "Use median income for all",
                    "Assume missing means zero income",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Exploratory Data Analysis",
            "subtopic": "Missing Data",
            "difficulty": 2,
            "question_text": f"You are analyzing {scenario['context']}. How should you handle the missing data?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Consider the missingness mechanism (MCAR/MAR/MNAR), whether to use simple imputation or "
            "model separate processes, and always document decisions for model transparency."
        }

    @classmethod
    def outlier_detection_approach(cls) -> Dict[str, Any]:
        """Choose appropriate outlier detection method."""
        scenarios = [
            {
                "context": "Claim amounts in auto insurance data show right-skewed distribution with extreme values",
                "correct": "Use percentile-based rules (95th, 99th) or robust statistics (IQR), verify with domain expert",
                "wrong": [
                    "Delete any value > 3 standard deviations",
                    "Use z-score cutoff of 2",
                    "Assume all extreme values are errors",
                ]
            },
            {
                "context": "Customer acquisition cost data with occasional $0 values (free referrals) and very high values",
                "correct": "Separate valid $0 from missing; investigate high values; consider log transformation",
                "wrong": [
                    "Delete $0 and $100k+ values",
                    "Cap all values at mean",
                    "Treat $0 as missing data",
                ]
            },
            {
                "context": "Predictive model on policyholder age, 20-80 years, but 5 records show age > 110",
                "correct": "Investigate records; likely data entry errors; correct or remove with documentation",
                "wrong": [
                    "Include them; they represent rare cases",
                    "Ignore them; they don't affect the model",
                    "Impute with median age",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Exploratory Data Analysis",
            "subtopic": "Outlier Detection",
            "difficulty": 3,
            "question_text": f"In your analysis, you find: {scenario['context']}. What is your approach?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Outliers warrant investigation before deletion. Consider distribution shape, business context, "
            "and whether outliers represent valid rare events or genuine errors."
        }

    @classmethod
    def variable_distribution_assessment(cls) -> Dict[str, Any]:
        """Assess variable distribution and implications."""
        scenarios = [
            {
                "context": "Response variable (claim incidence) shows 2% positives, 98% negatives",
                "correct": "Severely imbalanced; use stratified cross-validation, consider class weight adjustment, report sensitivity/specificity",
                "wrong": [
                    "Use default logistic regression; ROC-AUC will show good fit",
                    "Balance by oversampling minority class without CV stratification",
                    "Focus on accuracy as main metric",
                ]
            },
            {
                "context": "Predictor variable (log of policy value) shows roughly normal distribution after transformation",
                "correct": "Use transformed variable in model; verify transformation improves linearity",
                "wrong": [
                    "Use raw policy value; linear relationship better",
                    "Standardize but don't transform",
                    "Use both raw and transformed as separate predictors",
                ]
            },
            {
                "context": "Policyholder income shows heavy right skew with median $50k, mean $75k, max $2M",
                "correct": "Transform (log/sqrt) or use robust regression; report both raw and transformed analysis",
                "wrong": [
                    "Use income directly; skewness won't affect linear regression",
                    "Trim all values above 95th percentile",
                    "Use median income for all high earners",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Exploratory Data Analysis",
            "subtopic": "Distribution Assessment",
            "difficulty": 2,
            "question_text": f"During EDA: {scenario['context']}. What should you do?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Understanding variable distributions informs transformation decisions, model selection, "
            "and appropriate evaluation metrics. Imbalanced targets require special handling."
        }

    @classmethod
    def correlation_interpretation(cls) -> Dict[str, Any]:
        """Interpret correlation structure and implications."""
        scenarios = [
            {
                "context": "Two predictors correlate 0.92; both improve model fit individually but one becomes non-significant when both included",
                "correct": "Indicates multicollinearity; choose one predictor or use regularization; check VIF",
                "wrong": [
                    "Use both; correlation < 1 means they're independent",
                    "Transform one variable to reduce correlation",
                    "This is expected behavior; proceed as normal",
                ]
            },
            {
                "context": "Response variable shows weak correlation (0.15) with each individual predictor",
                "correct": "Weak marginal relationships; may still have good joint prediction; interaction/non-linearity possible",
                "wrong": [
                    "Model will have poor predictive power; abandon",
                    "Predictors are useless; remove all",
                    "Strong joint relationship guaranteed",
                ]
            },
            {
                "context": "Age and tenure correlate 0.45; both are significant in model with interactions included",
                "correct": "Acceptable correlation; interaction term explains joint effect; verify stability across folds",
                "wrong": [
                    "Remove one predictor due to correlation",
                    "Correlation too high; problematic",
                    "Interaction term redundant with correlation",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Exploratory Data Analysis",
            "subtopic": "Correlation",
            "difficulty": 3,
            "question_text": f"During correlation analysis: {scenario['context']}. What's your interpretation?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Correlation structure informs variable selection, identifies multicollinearity, and suggests "
            "interaction terms. Weak marginal correlations don't preclude predictive power."
        }

    @classmethod
    def categorical_variable_handling(cls) -> Dict[str, Any]:
        """Choose categorical encoding strategy."""
        scenarios = [
            {
                "context": "Categorical variable 'state' has 50 categories with wide frequency variation; small sample size relative to categories",
                "correct": "Group rare categories; use target encoding or regularized one-hot; report shrinkage method",
                "wrong": [
                    "One-hot encode all 50; model will handle sparsity",
                    "Delete categorical variable",
                    "Use dummy variables for all without grouping",
                ]
            },
            {
                "context": "Ordinal variable 'credit rating' (AAA, AA, A, BBB, BB, B, C)",
                "correct": "Encode as numeric (7, 6, 5, 4, 3, 2, 1) or one-hot; verify linear assumption for numeric",
                "wrong": [
                    "Use alphabetical dummy variables",
                    "Treat as nominal category",
                    "One-hot and numeric simultaneously",
                ]
            },
            {
                "context": "Nominal variable 'profession' has 25 categories; sample size allows modeling all",
                "correct": "One-hot encode with regularization; reference category chosen arbitrarily; verify no multi-collinearity",
                "wrong": [
                    "Use target encoding without cross-validation",
                    "Combine categories by frequency",
                    "Use dummy variables without reference category",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Exploratory Data Analysis",
            "subtopic": "Categorical Variables",
            "difficulty": 3,
            "question_text": f"In your dataset: {scenario['context']}. How should you encode this variable?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Categorical encoding depends on cardinality, frequency distribution, and sample size. "
            "Rare categories should be grouped; ordinal structure should be respected."
        }

    @classmethod
    def data_quality_issue(cls) -> Dict[str, Any]:
        """Identify and address data quality issues."""
        scenarios = [
            {
                "context": "100k records collected over 3 years; data governance changed midway (new fields, definitions); 20k records lack new fields",
                "correct": "Analyze by time period; model separately or use indicator for data source; document assumptions",
                "wrong": [
                    "Delete older records; newer data is cleaner",
                    "Impute missing new fields across all records",
                    "Combine periods assuming consistency",
                ]
            },
            {
                "context": "Premium variable shows $0 for 0.5% of records; business indicates these are legitimate (promotional policies)",
                "correct": "Keep $0 values; create indicator for promotional; model separately if impacts predictions",
                "wrong": [
                    "Delete $0 records",
                    "Replace with minimum non-zero premium",
                    "Flag as missing data",
                ]
            },
            {
                "context": "Claim amount has 15k vs 850k for large vs small claims; heavy class imbalance with different characteristics",
                "correct": "Model separately or stratified; use claim-size-specific features; evaluate on each segment",
                "wrong": [
                    "Oversample small claims to balance",
                    "Use single model for both segments",
                    "Weight by frequency",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Exploratory Data Analysis",
            "subtopic": "Data Quality",
            "difficulty": 3,
            "question_text": f"During data exploration, you discover: {scenario['context']}. How do you proceed?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Data quality issues often require segment-specific models, documentation of assumptions, "
            "and sensitivity analysis across handling approaches."
        }

    @classmethod
    def sample_size_adequacy(cls) -> Dict[str, Any]:
        """Evaluate if sample size is adequate."""
        scenarios = [
            {
                "context": "Dataset has 5k records, 40 candidate predictors; response event rate 5%",
                "correct": "Marginal; fewer than 100 events per predictor (200 total events); reduce features or use regularization",
                "wrong": [
                    "Excellent sample size for 40 predictors",
                    "Use all predictors; no constraint",
                    "Sample size determined by total n, not event count",
                ]
            },
            {
                "context": "500k records with 8 predictors; want to build 20 separate models by business segment",
                "correct": "Verify minimum 100-200 events per segment; may need pooling or hierarchical approach for small segments",
                "wrong": [
                    "500k is huge; segment models will all be well-powered",
                    "Build separate models without checking segment sizes",
                    "Combine segments due to sample size concerns",
                ]
            },
            {
                "context": "100k records, 3 key predictors, 1% event rate (1000 events)",
                "correct": "Adequate for 3 predictors; 1000 events >> 100-300 minimum; can explore interactions",
                "wrong": [
                    "1% is too rare; cannot model",
                    "Limited to 3 predictors only",
                    "Need to oversample to 10%+",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Exploratory Data Analysis",
            "subtopic": "Sample Size",
            "difficulty": 2,
            "question_text": f"Evaluating adequacy of your dataset: {scenario['context']}. What should you conclude?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Adequacy depends on event count (not total n), number of predictors, and model complexity. "
            "Guidelines: ~100-300 events per predictor for reliable estimation."
        }

    @classmethod
    def target_variable_analysis(cls) -> Dict[str, Any]:
        """Analyze target variable characteristics."""
        scenarios = [
            {
                "context": "Target variable (1-year renewal) is binary; 88% retention rate; past models showed AUC 0.72 on test set",
                "correct": "High baseline retention; model must identify churners precisely; optimize sensitivity/specificity tradeoff; use cost-weighted loss",
                "wrong": [
                    "Random baseline 0.5, so 0.72 is great performance",
                    "Class imbalance doesn't matter for logistic regression",
                    "Maximize accuracy; 88% implies good fit",
                ]
            },
            {
                "context": "Target is continuous claim amount; distribution highly skewed; median $500, mean $1200, max $150k",
                "correct": "Use quantile regression or GLM with log link; evaluate RMSE on log scale; consider separate models for amount given claim",
                "wrong": [
                    "Linear regression on raw amount",
                    "Log-transform then use OLS; predict on log scale",
                    "Cap amounts at 99th percentile before modeling",
                ]
            },
            {
                "context": "Target is time-to-event (days until claim); right-censored (20% still open); baseline hazard increases with time",
                "correct": "Use survival analysis (Cox, AFT); account for censoring explicitly; partial likelihood estimation",
                "wrong": [
                    "Treat open claims as non-events",
                    "Logistic regression on event indicator",
                    "Standard linear regression with time as outcome",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Exploratory Data Analysis",
            "subtopic": "Target Analysis",
            "difficulty": 3,
            "question_text": f"Analyzing your target variable: {scenario['context']}. What's the implication?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Target variable structure (binary/continuous/censored) and distribution inform model family, "
            "appropriate transformations, and evaluation metrics."
        }

    # ==================== FEATURE ENGINEERING (8 methods) ====================

    @classmethod
    def variable_transformation_choice(cls) -> Dict[str, Any]:
        """Choose appropriate variable transformation."""
        scenarios = [
            {
                "context": "Predictor (annual income) shows right skew; range $20k-$500k; strong relationship with log(target)",
                "correct": "Use log(income); improves linearity and normality; more interpretable coefficients per % income change",
                "wrong": [
                    "Use sqrt(income)",
                    "Use income directly; skewness irrelevant for GLM",
                    "Standardize to mean 0, sd 1",
                ]
            },
            {
                "context": "Categorical ordinal variable (credit score bands: Poor, Fair, Good, Excellent); clear separation in response",
                "correct": "Encode as numeric (1,2,3,4) or one-hot; verify ordinal assumption with diagnostic plots",
                "wrong": [
                    "Use one-hot without testing ordinality",
                    "Random numeric codes for each category",
                    "Treat as nominal without ordering",
                ]
            },
            {
                "context": "Ratio of two noisy measurements; high variance, but theoretically important; 5% of records have zero denominator",
                "correct": "Create derived ratio with missing for division by zero; handle separately; consider log transformation",
                "wrong": [
                    "Drop records with zero denominator",
                    "Set ratio to one where denominator near zero",
                    "Use unmeasured original variables instead",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Feature Engineering",
            "subtopic": "Variable Transformation",
            "difficulty": 2,
            "question_text": f"For your modeling, you have: {scenario['context']}. What transformation is most appropriate?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Transformations improve linearity, normality, and interpretability. Choice depends on variable type, "
            "distribution, and theoretical relationship with target."
        }

    @classmethod
    def interaction_term_need(cls) -> Dict[str, Any]:
        """Determine if interaction terms are warranted."""
        scenarios = [
            {
                "context": "Age and vehicle type both significant; residual plots show patterns by age within vehicle type; domain suggests interaction",
                "correct": "Add age × vehicle_type interaction; test significance and model fit improvement; regularize if overfitting",
                "wrong": [
                    "Don't add interaction; VIF will increase",
                    "Add but don't test significance",
                    "Always add interactions for all pairs",
                ]
            },
            {
                "context": "10 predictors; preliminary model fits well; residuals show no pattern; model stable across folds",
                "correct": "Don't add interactions; risk overfitting; seek marginal gains; add only if domain/residuals suggest",
                "wrong": [
                    "Systematically test all 45 pairs",
                    "Add interactions for top 3 predictors",
                    "Interactions always improve generalization",
                ]
            },
            {
                "context": "Geographic region and income both predictive; business knows poor urban areas differ from poor rural; test suggests p=0.01",
                "correct": "Region × income interaction justified; domain and statistics align; interpret coefficient",
                "wrong": [
                    "p=0.01 might be false positive; exclude interaction",
                    "Add without testing significance",
                    "Create separate models per region instead",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Feature Engineering",
            "subtopic": "Interactions",
            "difficulty": 3,
            "question_text": f"When building your model: {scenario['context']}. Should you include an interaction term?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Interaction terms improve fit when effects combine non-additively. Include based on theory, "
            "residual patterns, and statistical significance; avoid overfitting with many interactions."
        }

    @classmethod
    def binning_strategy(cls) -> Dict[str, Any]:
        """Choose binning strategy for continuous variables."""
        scenarios = [
            {
                "context": "Age predictor: business wants risk tables by age band; 50k observations; strong non-linear relationship with risk",
                "correct": "Use quantile-based bins (quartiles) or equal-width bins; test for equal slope assumption within bins; alternatively use splines",
                "wrong": [
                    "Single cutoff (e.g., age < 50)",
                    "Too many bins (100+); overfitting risk",
                    "Keep continuous; binning loses information",
                ]
            },
            {
                "context": "Balance amount: heavily skewed; sparse in high range; linear model assumption violated",
                "correct": "Log-transform or use square root; specify a spline; or bin based on natural gaps in data",
                "wrong": [
                    "Equal-width bins; skewness ignored",
                    "Many small bins for rare high values",
                    "Bin all continuous variables uniformly",
                ]
            },
            {
                "context": "Tenure (months with company): 1-360 months; business requires annual targets; nonlinear effect",
                "correct": "Domain-driven bins (annual): 0-12, 13-24, etc.; test linearity; or use natural spline on log(tenure)",
                "wrong": [
                    "Equal-width bins (e.g., 0-36, 36-72, ...)",
                    "Quantile bins; doesn't respect business logic",
                    "Don't bin; use continuous tenure",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Feature Engineering",
            "subtopic": "Binning",
            "difficulty": 2,
            "question_text": f"When deciding to bin a continuous variable: {scenario['context']}. What's your approach?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Binning may be justified for interpretability and non-linearity, but causes information loss. "
            "Quantile-based, equal-width, or domain-driven approaches have different merits."
        }

    @classmethod
    def one_hot_encoding_scenario(cls) -> Dict[str, Any]:
        """Handle one-hot encoding in specific context."""
        scenarios = [
            {
                "context": "Categorical variable 'insurance type' has 5 categories; using linear regression with no regularization",
                "correct": "Use 4 dummies (drop reference category); ensures no multicollinearity; coefficient interpretation relative to reference",
                "wrong": [
                    "Use all 5 dummies; include intercept",
                    "Use 3 dummies; arbitrary choice",
                    "Use target encoding instead",
                ]
            },
            {
                "context": "Using regularized GLM (ridge regression); 200 candidate categorical variables (high-dimensional)",
                "correct": "Use all one-hot dummies (no reference category needed); regularization handles multicollinearity",
                "wrong": [
                    "Drop reference category to avoid multicollinearity",
                    "Select only top 50 variables first",
                    "Use ordinal encoding for all",
                ]
            },
            {
                "context": "Predictor 'promotion code' has 50k unique codes; want to incorporate code effects",
                "correct": "Target encode or use embeddings; use hierarchical approach; or collapse rare codes into 'other'",
                "wrong": [
                    "One-hot encode all 50k codes",
                    "Drop variable as too sparse",
                    "Ordinal encode by frequency",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Feature Engineering",
            "subtopic": "Encoding",
            "difficulty": 2,
            "question_text": f"In your modeling setup: {scenario['context']}. How should you encode?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "One-hot encoding requires reference category for unregularized models but not for regularized methods. "
            "High-cardinality variables need alternative strategies."
        }

    @classmethod
    def feature_selection_method(cls) -> Dict[str, Any]:
        """Choose feature selection approach."""
        scenarios = [
            {
                "context": "Candidate features: 500 variables from automated data mining; interpretability needed for business model",
                "correct": "Use regularization (elastic net) with cross-validation; examine coefficients; verify stability; combine with domain knowledge",
                "wrong": [
                    "Univariate p-value cutoff (e.g., p < 0.05)",
                    "Stepwise selection (forward/backward/both)",
                    "Use all variables; let cross-validation handle",
                ]
            },
            {
                "context": "50 predictors; clear business features + some derived; want parsimonious model; sample size adequate",
                "correct": "Start with business features; test derived variables for significance; use regularization; compare simple vs complex",
                "wrong": [
                    "Use all 50; justify with R²",
                    "Univariate filter then model selection",
                    "Principal components on all features",
                ]
            },
            {
                "context": "Very high-dimensional (10k+ features); small effective sample size; sparse target",
                "correct": "Use strong regularization (lasso/elastic net); select features with non-zero coefficients; or dimensionality reduction (PCA/embedding)",
                "wrong": [
                    "Standard stepwise selection",
                    "Univariate filter with loose threshold",
                    "Random forest variable importance",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Feature Engineering",
            "subtopic": "Feature Selection",
            "difficulty": 3,
            "question_text": f"Selecting features for your model: {scenario['context']}. What's your strategy?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Feature selection balances model simplicity with predictive power. Regularization combined with "
            "domain knowledge typically outperforms automated univariate filters or stepwise approaches."
        }

    @classmethod
    def multicollinearity_resolution(cls) -> Dict[str, Any]:
        """Address multicollinearity issues."""
        scenarios = [
            {
                "context": "Two similar predictors (r=0.88) both significant; domain suggests using both; standard errors inflated",
                "correct": "Use regularization (ridge); or combine into single feature; verify VIF < 5; interpret joint effect",
                "wrong": [
                    "Remove one predictor",
                    "Standardize both variables",
                    "Accept high standard errors; t-stats still valid",
                ]
            },
            {
                "context": "Multiple operational metrics highly correlated; all contain overlapping information; want interpretability",
                "correct": "PCA or factor analysis to extract common signal; or select representative variable; or combine score",
                "wrong": [
                    "Include all metrics; multicollinearity ignorable",
                    "Randomized feature selection to pick subset",
                    "Linear combinations for manual dimensionality reduction",
                ]
            },
            {
                "context": "20 predictors; VIF > 10 for half; lasso selected all; model unstable across CV folds",
                "correct": "Use ridge or elastic net; reduce regularization parameter; combine correlated features; re-examine feature engineering",
                "wrong": [
                    "Ignore multicollinearity; lasso handles it",
                    "Delete all high-VIF predictors",
                    "Increase regularization further",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Feature Engineering",
            "subtopic": "Multicollinearity",
            "difficulty": 3,
            "question_text": f"Addressing multicollinearity: {{scenario['context']}}. What's your approach?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Multicollinearity inflates standard errors and destabilizes models. Solutions include regularization, "
            "feature combination, dimensionality reduction, or informed variable selection."
        }

    @classmethod
    def derived_variable_creation(cls) -> Dict[str, Any]:
        """Decide on creating derived variables."""
        scenarios = [
            {
                "context": "Original data: purchase amount and purchase frequency; business domain suggests interaction; correlation 0.3",
                "correct": "Create derived: lifetime value (amount × frequency); test in model; remove if adds little after regularization",
                "wrong": [
                    "Add both raw and interaction term",
                    "Domain suggests interaction; automatically include",
                    "Derived variables always redundant with originals",
                ]
            },
            {
                "context": "Date fields (month-of-issue, days-since-issue); temporal patterns evident in EDA; calendar effects possible",
                "correct": "Extract features: day-of-week, season, time-to-event; test for significance; balance with sample size",
                "wrong": [
                    "Use raw date; model extracts patterns",
                    "Too many derived features; causes overfitting",
                    "Only year as temporal feature",
                ]
            },
            {
                "context": "Three balance fields; relationships complex; business wants single risk score; high collinearity",
                "correct": "Create weighted score using PCA/factor analysis; or logistic regression score; validate interpretation",
                "wrong": [
                    "Simple average of three fields",
                    "Don't combine; use all three separately",
                    "Arbitrary weights for combination",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Feature Engineering",
            "subtopic": "Derived Features",
            "difficulty": 2,
            "question_text": f"In feature engineering: {scenario['context']}. Should you create derived variables?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Derived variables capture domain knowledge and interactions but risk overfitting. Create only if "
            "justified by theory/EDA; test in model; remove if redundant after regularization."
        }

    @classmethod
    def text_feature_extraction(cls) -> Dict[str, Any]:
        """Extract features from text data."""
        scenarios = [
            {
                "context": "Customer complaint descriptions (100-500 words); hundreds of unique terms; want to predict complaint severity",
                "correct": "Bag-of-words TF-IDF or word embeddings; dimensionality reduction; test key terms identified by domain experts",
                "wrong": [
                    "Raw word count as single feature",
                    "One-hot encode all unique words",
                    "Ignore text; use structured features only",
                ]
            },
            {
                "context": "Policy document text; regulatory/domain-specific terminology; moderate volume (10k documents); English only",
                "correct": "TF-IDF with domain-aware preprocessing; remove boilerplate; extract key phrase frequencies; use selected terms",
                "wrong": [
                    "Word embeddings (overkill for structured data)",
                    "All terms equally weighted",
                    "Topic modeling for classification task",
                ]
            },
            {
                "context": "Short categorical labels (insurance product name, abbreviated descriptions); very limited vocabulary (50 unique)",
                "correct": "One-hot encoding or ordinal if hierarchical; supplementary to structured features",
                "wrong": [
                    "Full NLP pipeline for short labels",
                    "Treat as free-form text",
                    "Combine with word embeddings",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Feature Engineering",
            "subtopic": "Text Features",
            "difficulty": 3,
            "question_text": f"Handling text data: {scenario['context']}. How should you extract features?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Text feature extraction depends on document length, vocabulary size, and domain specificity. "
            "Balance between capturing signal and avoiding high-dimensional sparsity."
        }

    # ==================== GLM APPLICATION (10 methods) ====================

    @classmethod
    def distribution_family_selection(cls) -> Dict[str, Any]:
        """Select appropriate GLM distribution family."""
        scenarios = [
            {
                "context": "Response: claim frequency (counts); mean 1.5, variance 3.2; test dispersion via pearson χ²",
                "correct": "Poisson family; test for overdispersion; if variance >> mean, use negative binomial instead",
                "wrong": [
                    "Normal family; ignore count nature",
                    "Binomial family for proportions",
                    "Gamma family for positive data",
                ]
            },
            {
                "context": "Response: claim status (yes/no, binary); insurance prediction; class imbalance 10-90%",
                "correct": "Binomial family with logit link; weight classes; evaluate AUC/sensitivity separately",
                "wrong": [
                    "Normal family with identity link",
                    "Poisson family for binary outcomes",
                    "Gaussian family with log link",
                ]
            },
            {
                "context": "Response: positive continuous (severity | claim occurred); range $100-$500k; right-skewed",
                "correct": "Gamma family with log link (common in insurance); or Tweedie for excess data; test fit",
                "wrong": [
                    "Normal family with identity link",
                    "Binomial family for continuous",
                    "Poisson family for individual amounts",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "GLM Application",
            "subtopic": "Distribution Family",
            "difficulty": 2,
            "question_text": f"Selecting a GLM family: {scenario['context']}. What's appropriate?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Distribution family chosen based on response variable nature (counts, binary, continuous, skew). "
            "Poisson for counts, binomial for binary, gamma for positive continuous, normal for unrestricted continuous."
        }

    @classmethod
    def link_function_choice(cls) -> Dict[str, Any]:
        """Choose appropriate link function."""
        scenarios = [
            {
                "context": "Poisson regression for claim count; intercept-only model predicts mean 1.8; want proportional interpretation",
                "correct": "Log link (standard for Poisson); easy interpretation: exp(coefficient) = multiplicative effect on mean count",
                "wrong": [
                    "Identity link; predictions unbounded below zero",
                    "Logit link; doesn't apply to counts",
                    "Reciprocal link; uncommon for this purpose",
                ]
            },
            {
                "context": "Logistic regression for claim probability; business needs odds ratios; data shows natural threshold in risk",
                "correct": "Logit link (standard for binomial); interpret exp(coefficient) as odds ratio; flexible risk modeling",
                "wrong": [
                    "Probit link; harder to interpret",
                    "Log link; predictions unbounded above 1",
                    "Identity link; negative probabilities",
                ]
            },
            {
                "context": "Gamma GLM for claim severity; conditional on claim occurring; right-skewed; proportional effects expected",
                "correct": "Log link with gamma; exponential mean structure; percent change interpretation; common in insurance",
                "wrong": [
                    "Identity link; doesn't handle skew well",
                    "Inverse link; uncommon and less interpretable",
                    "Sqrt link; arbitrary transformation",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "GLM Application",
            "subtopic": "Link Function",
            "difficulty": 2,
            "question_text": f"Selecting a link function: {{scenario['context']}}. What's most appropriate?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Link function maps linear predictor to response scale. Log link for counts/positive continuous; "
            "logit for probabilities. Choice affects interpretation and constraints on predictions."
        }

    @classmethod
    def offset_vs_weight(cls) -> Dict[str, Any]:
        """Distinguish offset vs exposure weight."""
        scenarios = [
            {
                "context": "Modeling claim frequency; data: policies with different exposure (months active in year); want rate per exposure",
                "correct": "Use offset=log(exposure) in Poisson; models rate per unit exposure; coefficient interpreted as rate multiplier",
                "wrong": [
                    "Use weight=1/exposure; incorrect probability weighting",
                    "Divide response by exposure; loses count nature",
                    "Ignore exposure; biased towards long-exposure policies",
                ]
            },
            {
                "context": "Logistic regression with survey data; unequal sampling; weights reflect inverse sampling probability",
                "correct": "Use weight parameter; accounts for design; sandwich estimator for SE; results representative of population",
                "wrong": [
                    "Use offset; not applicable to logistic model",
                    "Rescale outcome by weight",
                    "Ignore weights; valid only for unweighted sample",
                ]
            },
            {
                "context": "Modeling annual loss; policies have different coverage limits (limits vary); want loss per $100 limit",
                "correct": "Use offset=log(limit) in GLM; models loss per unit limit; handles different exposures correctly",
                "wrong": [
                    "Divide loss by limit first; loses variance structure",
                    "Use weight=limit",
                    "Dummy code limit categories",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "GLM Application",
            "subtopic": "Offset vs Weight",
            "difficulty": 3,
            "question_text": f"In your GLM setup: {{scenario['context']}}. Should you use offset or weight?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Offset models exposure/denominator in rate/proportion; weight adjusts for design/survey probability. "
            "Offset has fixed coefficient 1 in log scale; weight is a multiplier on likelihood."
        }

    @classmethod
    def overdispersion_handling(cls) -> Dict[str, Any]:
        """Handle overdispersion in GLM."""
        scenarios = [
            {
                "context": "Poisson model for claim counts; Pearson χ² = 250, df = 100; suggest overdispersion; clusters in data",
                "correct": "Fit negative binomial (quasi-Poisson); tests show significant; re-evaluate model fit; check for omitted variables",
                "wrong": [
                    "Ignore; Poisson estimate consistent despite overdispersion",
                    "Scale standard errors by sqrt(dispersion); doesn't change estimates",
                    "Divide response by variance",
                ]
            },
            {
                "context": "Logistic regression; model fits well; Hosmer-Lemeshow test p=0.15 (no evidence of lack of fit)",
                "correct": "Overdispersion not indicated; standard binomial appropriate; proceed with normal inference",
                "wrong": [
                    "Assume overdispersion in logistic models",
                    "Use quasibinomial unnecessarily",
                    "Inflate standard errors",
                ]
            },
            {
                "context": "Gamma GLM for claim severity; deviance = 450, df = 200; dispersion φ = 2.25; heterogeneity expected",
                "correct": "Phi = 2.25 moderate; acceptable; scale SEs; consider additional predictors or quasi-likelihood; test interaction",
                "wrong": [
                    "Phi > 1 implies model failure; abandon",
                    "Remove outliers to reduce phi",
                    "Ignore dispersion; estimate unchanged",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "GLM Application",
            "subtopic": "Overdispersion",
            "difficulty": 3,
            "question_text": f"Diagnosing model fit: {{scenario['context']}}. How should you address?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Overdispersion (variance > mean for count data) inflates standard errors. Detect via dispersion parameter; "
            "fix with negative binomial, quasi-likelihood, or additional predictors."
        }

    @classmethod
    def model_output_interpretation(cls) -> Dict[str, Any]:
        """Interpret GLM model output."""
        scenarios = [
            {
                "context": "Poisson GLM: coefficient age = 0.03 (SE=0.005); exp(0.03) = 1.0305; claim count ~ 2/policy/year",
                "correct": "Per year age increase, expected claim count multiplies by 1.0305; ~3% increase per year",
                "wrong": [
                    "Claim count increases by 0.03 per year",
                    "Coefficient 0.03 means 3% risk",
                    "Standard error indicates unreliability",
                ]
            },
            {
                "context": "Logistic GLM: coefficient income = -0.001 (SE=0.0002); exp(-0.001) = 0.999; intercept = -1.5",
                "correct": "Per $1000 income increase, odds of claim multiply by 0.999; ~0.1% decrease per $1k; intercept sets scale",
                "wrong": [
                    "Probability decreases by 0.1%",
                    "Income effect is -0.1%",
                    "Intercept has no interpretation",
                ]
            },
            {
                "context": "Gamma GLM: coefficient log(limit) = 1.2 (SE=0.15); severity model; intercept = 3.8",
                "correct": "Doubling coverage limit multiplies expected severity by 2^1.2 = 2.3 (log coeff = elasticity); offset scaled by limit",
                "wrong": [
                    "Severity increases by 1.2 dollars",
                    "Log transformation doesn't affect interpretation",
                    "Coefficient is marginal effect",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "GLM Application",
            "subtopic": "Model Output",
            "difficulty": 2,
            "question_text": f"Interpreting your GLM output: {{scenario['context']}}. What does the coefficient mean?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "In GLM, coefficients apply to linear predictor (log scale for log-link). Exponentiate for multiplicative effects "
            "on scale of link function (e.g., exp(coef) for log-link)."
        }

    @classmethod
    def coefficient_significance(cls) -> Dict[str, Any]:
        """Evaluate coefficient significance."""
        scenarios = [
            {
                "context": "Logistic model: variable age, coefficient = 0.05 (SE = 0.025); z = 2.0; p = 0.046; 95% CI: (0.001, 0.099)",
                "correct": "Marginally significant (p=0.046); practical significance questionable (1% per 20 years); verify stability",
                "wrong": [
                    "Highly significant; definitely include",
                    "Not significant; p > 0.05",
                    "Include regardless of p-value",
                ]
            },
            {
                "context": "Large model, 50 predictors; after Bonferroni (α = 0.001), variable region has p = 0.0008; coefficient stable",
                "correct": "Highly significant after correction; include; region effect substantial; interpret coefficient",
                "wrong": [
                    "p < 0.05 suffices; Bonferroni too strict",
                    "Ignore multiple testing; use α = 0.05",
                    "Too many variables; reduce before testing",
                ]
            },
            {
                "context": "Poisson model: variable marketing_spend, coefficient = 0.0001 (SE = 0.00005); CI: (0, 0.00025); p = 0.001",
                "correct": "Significant but small effect; elastic claim count to spend increase; practical significance small",
                "wrong": [
                    "Significant = important; always include",
                    "Small coefficient = insignificant",
                    "p = 0.001 implies large effect size",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "GLM Application",
            "subtopic": "Significance",
            "difficulty": 2,
            "question_text": f"Assessing coefficient significance: {{scenario['context']}}. What's your conclusion?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Statistical significance (p-value) differs from practical significance (effect size). "
            "Multiple testing requires adjustment. Low p-value with small coefficient still requires judgment on inclusion."
        }

    @classmethod
    def rate_relativities(cls) -> Dict[str, Any]:
        """Calculate and interpret rate relativities."""
        scenarios = [
            {
                "context": "Rating variable: vehicle type (sedan, SUV, truck); base rate $800 (sedan); SUV coefficient = 0.15, truck = 0.25",
                "correct": "Sedan $800 (reference); SUV $800 * exp(0.15) = $920 (+15%); Truck $800 * exp(0.25) = $1004 (+25%)",
                "wrong": [
                    "Add coefficients to base: SUV $800 + 0.15 = $800.15",
                    "Coefficients are direct rate adjustments",
                    "Truck is cheapest since 0.25 < sedan implicitly",
                ]
            },
            {
                "context": "GLM for pure premium; territory interaction with vehicle; base urban sedan $900; rural uplift +20%; truck uplift +30%",
                "correct": "Rural sedan: $900 * 1.2 = $1080; rural truck: $900 * 1.2 * 1.3 = $1404 (multiplicative)",
                "wrong": [
                    "Rural truck: $900 + $216 + $270 = $1386 (additive)",
                    "Uplift applied sequentially not multiplicatively",
                    "Interact separately; cannot combine effects",
                ]
            },
            {
                "context": "Base rate $1200; competitor offers equivalent vehicle at $1050; your GLM estimates elasticity of -1.5 vs price",
                "correct": "Gap: $150/$1200 = 12.5%; demand loss: 1.5 * 12.5% = 18.75% volume drop expected; risk tier adjustment needed",
                "wrong": [
                    "Match competitor price; maintain volume",
                    "Elasticity -1.5 means 1% price increase = 1.5% rate increase",
                    "Statistical relationship applies directly to profitability",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "GLM Application",
            "subtopic": "Rate Relativities",
            "difficulty": 3,
            "question_text": f"Calculating rate relativities: {{scenario['context']}}. What's the correct pricing?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Relativities in log-link GLMs are multiplicative. Effects combine via exponentiation. "
            "Base rate × exp(coefficient₁) × exp(coefficient₂) for additive predictors on log scale."
        }

    @classmethod
    def base_level_impact(cls) -> Dict[str, Any]:
        """Evaluate choice of reference/base category."""
        scenarios = [
            {
                "context": "Logistic model: region (north=ref, south, east, west); south coef=0.2, east=0.1, west=-0.1",
                "correct": "North is baseline; south odds 1.22x north; east 1.1x; west 0.9x; relative comparisons valid regardless of reference",
                "wrong": [
                    "South is highest risk; always use south as reference",
                    "Reference category choice affects conclusions",
                    "Coefficients absolute, not relative to reference",
                ]
            },
            {
                "context": "Change reference from 'no prior claims' to 'one or more claims'; coefficient flips sign; interpretation impacts business",
                "correct": "Interpretation flips (sign inverts); meaning preserved; choose reference for clearest business communication",
                "wrong": [
                    "Reference choice irrelevant; underlying effect unchanged",
                    "Always use alphabetical order for reference",
                    "Negative coefficients inferior to positive",
                ]
            },
            {
                "context": "Rating rule: 'Non-smoker' baseline $500; 'Smoker' coefficient = 0.40; report wants premium for smoker vs non-smoker",
                "correct": "Smoker: $500 * exp(0.40) = $745; non-smoker: $500; difference $245; clearly communicates impact",
                "wrong": [
                    "Smoker premium is 40% above non-smoker",
                    "Coefficient 0.40 equals 40% surcharge directly",
                    "Reference category has zero premium",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "GLM Application",
            "subtopic": "Base Level",
            "difficulty": 2,
            "question_text": f"Understanding base categories: {{scenario['context']}}. What's the correct interpretation?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Choice of reference category affects coefficient signs/values but not relative relationships. "
            "Choose reference for clearest business interpretation; relative comparisons remain valid."
        }

    @classmethod
    def glm_prediction_scenario(cls) -> Dict[str, Any]:
        """Make predictions from GLM."""
        scenarios = [
            {
                "context": "Logistic model P(claim) = 1/(1+exp(-(η))), η = -2.5 + 0.02*age + 0.1*has_prior_claim (1=yes, 0=no); predict for age=45, no prior",
                "correct": "η = -2.5 + 0.02*45 + 0.1*0 = -1.6; P = 1/(1+exp(1.6)) = 0.168 or 16.8% probability",
                "wrong": [
                    "η = -2.5 + 0.9 + 0 = -1.6; probability = -1.6 = invalid",
                    "Probability = 0.02*45 = 0.9 = 90%",
                    "Cannot predict without confidence interval",
                ]
            },
            {
                "context": "Poisson model E[claims] = exp(η), η = 0.5 + 0.03*years_tenure - 0.2*good_driver (1=yes); age 35, tenure 5, good",
                "correct": "η = 0.5 + 0.03*5 - 0.2*1 = 0.35; E[claims] = exp(0.35) ≈ 1.42 claims/year",
                "wrong": [
                    "E[claims] = 0.5 + 0.15 - 0.2 = 0.45",
                    "Expected = exp(η) / n for n=number of variables",
                    "Cannot exponentiate; use linear prediction",
                ]
            },
            {
                "context": "Gamma GLM (log link) for severity: E[loss] = exp(η), η = 4.0 + 0.05*log(limit) + 0.02*age; limit=$100k, age=50",
                "correct": "η = 4.0 + 0.05*ln(100000) + 0.02*50 = 4.0 + 0.345 + 1.0 = 5.345; E[loss] = exp(5.345) ≈ $211k",
                "wrong": [
                    "E[loss] = 4.0 + 5.345 = $9.345k",
                    "Log(limit) = 100000; η = 4.0 + 0.05*100000 + 1 = 5001.0",
                    "Prediction = η = 5.345 (log scale)",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "GLM Application",
            "subtopic": "Predictions",
            "difficulty": 2,
            "question_text": f"Making GLM predictions: {{scenario['context']}}. What's your prediction?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Prediction: compute linear predictor η, then apply inverse link (e.g., 1/(1+exp(-η)) for logit, "
            "exp(η) for log). Never predict on link scale directly."
        }

    @classmethod
    def residual_pattern_interpretation(cls) -> Dict[str, Any]:
        """Interpret GLM residual patterns."""
        scenarios = [
            {
                "context": "Pearson residual plot vs fitted: increasing variance fan pattern; suggests heteroscedasticity",
                "correct": "Variance not constant; check for outliers; consider robust GLM or weighted regression; log transform",
                "wrong": [
                    "Pattern irrelevant in GLM; residuals uncorrelated",
                    "Transform response to stabilize variance",
                    "Add polynomial terms to predictor",
                ]
            },
            {
                "context": "Deviance residual qqplot: heavy tails; some standardized residuals > 3; remainder fit normal",
                "correct": "Few extreme observations; check for outliers; consider robust methods; may be valid rare events",
                "wrong": [
                    "Entire model invalid; residuals must be perfectly normal",
                    "Delete outliers; refits will fix tails",
                    "Log transform to normalize",
                ]
            },
            {
                "context": "Residuals vs predictor X: clear U-shaped pattern; suggests nonlinear relationship or omitted variable",
                "correct": "Add nonlinear term (spline, polynomial); or interaction; or check for omitted variable confounding",
                "wrong": [
                    "Pattern in residuals acceptable; orthogonal to fit",
                    "Indicates overdispersion; use quasi-likelihood",
                    "X already linear in model; cannot improve",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "GLM Application",
            "subtopic": "Residuals",
            "difficulty": 3,
            "question_text": f"Analyzing residual patterns: {{scenario['context']}}. What does it indicate?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Residual patterns reveal violations of model assumptions: non-constant variance, nonlinearity, "
            "omitted variables, or outliers. Address systematically via transformation, additional terms, or robust methods."
        }

    # ==================== MODEL EVALUATION (8 methods) ====================

    @classmethod
    def confusion_matrix_metrics(cls) -> Dict[str, Any]:
        """Interpret confusion matrix and derived metrics."""
        scenarios = [
            {
                "context": "Binary classifier: TP=80, FP=20, TN=400, FN=100. Business: false positives expensive; false negatives tolerable",
                "correct": "Sensitivity=44%, Specificity=95%, Precision=80%. High specificity good; low sensitivity problematic for business",
                "wrong": [
                    "Accuracy = (80+400)/600 = 80% is excellent",
                    "Precision insufficient; model useless",
                    "All metrics equally important",
                ]
            },
            {
                "context": "Claims prediction model: TP=50, FP=1000, TN=8000, FN=50. Want to identify claims efficiently",
                "correct": "Sensitivity=50%, Specificity=89%, Precision=5%. Model has poor precision; too many false positives; recalibrate threshold",
                "wrong": [
                    "High specificity sufficient; proceed",
                    "Accuracy = 80%; good model",
                    "Sensitivity = 50%; acceptable for screening",
                ]
            },
            {
                "context": "Medical screening test: TP=1, FP=9, TN=990, FN=0. Disease rare; want zero false negatives",
                "correct": "Sensitivity=100%, Specificity=99%, Precision=10%. Achieves zero FN; acceptable despite low precision in rare disease",
                "wrong": [
                    "Low precision = poor model",
                    "High FP rate means model fails",
                    "Accuracy 99.1%; excellent",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Model Evaluation",
            "subtopic": "Confusion Matrix",
            "difficulty": 2,
            "question_text": f"Evaluating classification: {{scenario['context']}}. What's your assessment?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Confusion matrix yields multiple metrics: sensitivity (TPR), specificity (TNR), precision (PPV). "
            "Choice of metric depends on business cost of false positives vs false negatives."
        }

    @classmethod
    def auc_roc_interpretation(cls) -> Dict[str, Any]:
        """Interpret AUC-ROC curve."""
        scenarios = [
            {
                "context": "Claim probability model: ROC-AUC = 0.72 (95% CI: 0.68-0.76); random classifier AUC = 0.50",
                "correct": "Model better than random; moderate discrimination; 72% chance model ranks random claim > non-claim",
                "wrong": [
                    "72% accuracy of predictions",
                    "Threshold probability 0.72",
                    "Model performance poor; AUC < 0.8",
                ]
            },
            {
                "context": "Two models: M1 AUC=0.85, M2 AUC=0.82 on same test set; M1 complexity much higher; validation set AUC M1=0.79, M2=0.81",
                "correct": "M2 better generalization; M1 likely overfitting; prefer M2 (simpler, better validation)",
                "wrong": [
                    "M1 always better; higher test AUC",
                    "Use M1 for simplicity despite lower test AUC",
                    "AUC difference 0.03 statistically insignificant; flip coin",
                ]
            },
            {
                "context": "Insurance model AUC=0.56; client questions if better than random. Baseline (underwriting rules) AUC=0.52",
                "correct": "Model marginally better than baseline; improvement modest; explore feature engineering; consider regulatory risk",
                "wrong": [
                    "AUC > 0.5 means model works; deploy",
                    "Only 56% accuracy; model unusable",
                    "Compare to 0.50 only; ignore baseline",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Model Evaluation",
            "subtopic": "AUC-ROC",
            "difficulty": 2,
            "question_text": f"Interpreting AUC-ROC: {{scenario['context']}}. What's your conclusion?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "AUC (area under ROC curve) measures rank ordering of predictions. AUC=0.5 is random; 1.0 is perfect. "
            "AUC>0.7 typically considered useful. Compare models on test/validation set, not training."
        }

    @classmethod
    def lift_chart_analysis(cls) -> Dict[str, Any]:
        """Analyze lift chart."""
        scenarios = [
            {
                "context": "Lift chart for churn model: at 20% of population (sorted by prediction descending), lift = 3.2",
                "correct": "Top 20% has 3.2x baseline churn rate; effective targeting; 3.2x 80% baseline = 256% capture",
                "wrong": [
                    "20% of churners correctly identified",
                    "Model identifies 32% of churners",
                    "Lift of 3.2 means 3.2% churn rate",
                ]
            },
            {
                "context": "Comparing models: M1 lift curve steeper initially, flattens at 40%; M2 lift more gradual but sustained to 100%",
                "correct": "M1 concentrates signal early (better for top-N targeting); M2 more balanced; choose M1 for concentrated campaigns",
                "wrong": [
                    "M1 superior in all applications",
                    "Flattening at 40% means model fails",
                    "Gradual lift indicates underfitting",
                ]
            },
            {
                "context": "Cross-validation folds: M1 lift varies wildly (2.5 to 4.5); M2 consistent (2.8 to 3.1); AUC similar",
                "correct": "M2 more stable; M1 overfitting or unstable; prefer M2 for deployment; monitor lift in production",
                "wrong": [
                    "High variance lift shows M1 effective",
                    "Consistency irrelevant if average same",
                    "M1 averages higher; use M1",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Model Evaluation",
            "subtopic": "Lift Chart",
            "difficulty": 2,
            "question_text": f"Analyzing lift charts: {{scenario['context']}}. What should you conclude?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Lift = (response rate in segment) / (baseline response rate). Lift at decile D indicates how much better "
            "than random for top D% of sorted scores. Used for targeting strategies."
        }

    @classmethod
    def gains_table_reading(cls) -> Dict[str, Any]:
        """Read and interpret gains table."""
        scenarios = [
            {
                "context": "Gains table: Decile 1 (top 10%) captures 35% of all positives; Deciles 1-2 (top 20%) capture 55%; n_pos=5000",
                "correct": "Top 10% contains 1750 positives (35% of 5000); highly concentrated; effective for targeted campaigns",
                "wrong": [
                    "35% accuracy in top decile",
                    "35% of population are positives",
                    "Decile 1 response rate is 35%",
                ]
            },
            {
                "context": "Gains: Decile 1 captures 20%, Decile 2 captures 19%, ... Decile 10 captures 5% of total positives",
                "correct": "Signal gradually distributed; model not strongly predictive; consider feature engineering or simpler baseline",
                "wrong": [
                    "Gains table shows poor fit",
                    "Even distribution indicates good model",
                    "5% in Decile 10 shows overfitting",
                ]
            },
            {
                "context": "Gains: top 30% (3 deciles) capture 80% of positives; business can target 30% population for 80% of response",
                "correct": "Excellent concentration; cost-effective to target 30%; covers 80% of opportunity; cost-benefit favorable",
                "wrong": [
                    "Must target 100% to reach all positives",
                    "Can only reach 80% of positives",
                    "30% targeting rate means 30% accuracy",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Model Evaluation",
            "subtopic": "Gains Table",
            "difficulty": 2,
            "question_text": f"Reading gains table: {{scenario['context']}}. What does this tell you?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Gains table shows cumulative % of positives captured by deciles (ordered by score). "
            "Rapid rise indicates strong concentration; flat indicates poor predictive power."
        }

    @classmethod
    def model_comparison_multiple_metrics(cls) -> Dict[str, Any]:
        """Compare models across multiple metrics."""
        scenarios = [
            {
                "context": "Model A: Accuracy 82%, Sensitivity 60%, AUC 0.75. Model B: Accuracy 78%, Sensitivity 80%, AUC 0.72. Business priority: identify claims",
                "correct": "Model B preferred; higher sensitivity captures more claims despite lower accuracy; business-aligned",
                "wrong": [
                    "Model A better; higher accuracy",
                    "AUC difference favors A; use A",
                    "Metrics contradict; cannot decide",
                ]
            },
            {
                "context": "Regression models: M1 RMSE=450, R²=0.75, MAE=320. M2 RMSE=480, R²=0.72, MAE=300. Data has outliers",
                "correct": "M2 better MAE (robust to outliers); M1 better RMSE (outliers inflate). Prefer M2 for robustness; verify outliers",
                "wrong": [
                    "M1 overall better; all metrics relevant equally",
                    "Cannot choose; metrics conflicting",
                    "Use M1; RMSE standard metric",
                ]
            },
            {
                "context": "Time series models: M1 MAE=50 (recent data), naive=120. M2 MAE=60 (recent), naive=120. M1 much more complex (ARIMA vs exp smoothing)",
                "correct": "M2 preferred; 50% error reduction over naive vs M1's 58% not worth complexity; bias-variance tradeoff",
                "wrong": [
                    "M1 always better; lower error",
                    "Complexity irrelevant if M1 more accurate",
                    "Naive baseline not meaningful comparison",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Model Evaluation",
            "subtopic": "Multi-Metric Comparison",
            "difficulty": 3,
            "question_text": f"Comparing models across metrics: {{scenario['context']}}. Which should you select?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Model selection requires balancing multiple metrics: accuracy, sensitivity, specificity, AUC, error measures. "
            "Business priority (e.g., minimize false negatives) should guide metric weighting."
        }

    @classmethod
    def gini_coefficient(cls) -> Dict[str, Any]:
        """Understand Gini coefficient for model ranking."""
        scenarios = [
            {
                "context": "Model Gini = 0.45 (where max Gini = 1.0 for perfect ranking); baseline Gini ≈ 0.0; competitor Gini = 0.38",
                "correct": "Model discriminates well (0.45 is strong); better than competitor (0.38); Gini = 2*AUC-1",
                "wrong": [
                    "Gini = 0.45 means 45% accuracy",
                    "Low Gini; model poor",
                    "Gini unrelated to AUC",
                ]
            },
            {
                "context": "Two actuarial models: each has AUC 0.70. Calculate Gini for both.",
                "correct": "Both Gini = 2*(0.70)-1 = 0.40; same AUC implies same Gini; no discriminator difference",
                "wrong": [
                    "Gini cannot be derived from AUC",
                    "Higher AUC = higher Gini always",
                    "Gini independent of discrimination",
                ]
            },
            {
                "context": "Gini = 0.02 (barely above random); cross-validation shows this stable. Simplify model or add features?",
                "correct": "Model has minimal discriminatory power; feature engineering, new data, or domain transformation needed; "
                "current features insufficient",
                "wrong": [
                    "Gini 0.02 acceptable; deploy",
                    "Add more interaction terms",
                    "Increase model complexity",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Model Evaluation",
            "subtopic": "Gini Coefficient",
            "difficulty": 2,
            "question_text": f"Evaluating with Gini coefficient: {{scenario['context']}}. What's your interpretation?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Gini coefficient measures ranking quality: Gini = 2*AUC - 1, ranging [-1, 1]. "
            "Higher Gini indicates better discrimination. Gini=0 is random; Gini=1 is perfect."
        }

    @classmethod
    def calibration_assessment(cls) -> Dict[str, Any]:
        """Assess model calibration."""
        scenarios = [
            {
                "context": "Calibration plot: predicted probability vs observed frequency; points lie near diagonal; Hosmer-Lemeshow p=0.45",
                "correct": "Well-calibrated; predicted probabilities match observed rates; no correction needed; trustworthy predictions",
                "wrong": [
                    "Uncalibrated; always incorrect predictions",
                    "Calibration irrelevant if accurate ranking (AUC high)",
                    "Hosmer-Lemeshow p=0.45 indicates miscalibration",
                ]
            },
            {
                "context": "Predicted probabilities consistently 20% too high (0.30 predicted = 0.25 observed); systematic bias",
                "correct": "Calibration adjustment needed; apply isotonic regression or Platt scaling; or document bias for users",
                "wrong": [
                    "AUC remains same; ranking preserves; ignore",
                    "Predictions useless; model fails",
                    "Retrain model entirely",
                ]
            },
            {
                "context": "High-risk group (pred prob > 0.8): observed freq = 0.70; low-risk (pred < 0.2): observed = 0.05",
                "correct": "Underestimated high-risk, overestimated low-risk; plausible (fewer extreme observations); monitor calibration",
                "wrong": [
                    "Perfect calibration requires pred=obs everywhere",
                    "Asymmetry indicates model error",
                    "Cannot assess calibration with limited groups",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Model Evaluation",
            "subtopic": "Calibration",
            "difficulty": 3,
            "question_text": f"Assessing calibration: {{scenario['context']}}. What's your assessment?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Calibration: predicted probabilities match observed frequencies. Assessed via calibration plot (diag=perfect), "
            "Hosmer-Lemeshow test, or isotonic regression. Ranking (AUC) and calibration are separate; both matter for predictions."
        }

    @classmethod
    def holdout_vs_cv(cls) -> Dict[str, Any]:
        """Compare holdout vs cross-validation evaluation."""
        scenarios = [
            {
                "context": "Dataset 1000 rows; holdout test set (100 rows) AUC 0.75; 5-fold CV mean AUC 0.72 (SD 0.04); small dataset",
                "correct": "CV more reliable (uses all data); holdout may lucky split; prefer CV mean 0.72; report SD for uncertainty",
                "wrong": [
                    "Holdout more honest estimate",
                    "CV AUC overestimated due to fold averaging",
                    "Trust single largest number (0.75)",
                ]
            },
            {
                "context": "Dataset 100k rows; holdout 10k test, train 90k. 5-fold CV would need retraining; holdout computationally efficient",
                "correct": "Holdout practical given size; sufficient test set; power trade-off acceptable; ensure stratification for class balance",
                "wrong": [
                    "CV always better; use 10 folds",
                    "Large dataset makes holdout unreliable",
                    "Holdout must match CV percentage split",
                ]
            },
            {
                "context": "5-fold CV: Fold 1 AUC 0.82, Fold 2 0.68, Fold 3 0.75, Fold 4 0.80, Fold 5 0.70; mean 0.75, SD 0.06",
                "correct": "High variance in folds suggests unstable model; investigate fold structure; try stratification; "
                "consider larger dataset or simpler model",
                "wrong": [
                    "Use mean 0.75 as final estimate; ignore variance",
                    "High SD indicates good generalization",
                    "One poor fold invalidates all results",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Model Evaluation",
            "subtopic": "Holdout vs CV",
            "difficulty": 2,
            "question_text": f"Choosing evaluation strategy: {{scenario['context']}}. What's best?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Cross-validation uses data more efficiently; holdout simpler but wastes data. Use CV for small/medium datasets; "
            "holdout acceptable for large datasets. Always report both point estimate and variance."
        }

    # ==================== OVERFITTING & REGULARIZATION (6 methods) ====================

    @classmethod
    def train_test_gap_diagnosis(cls) -> Dict[str, Any]:
        """Diagnose and address train-test gap."""
        scenarios = [
            {
                "context": "Training AUC 0.92, Test AUC 0.68, gap = 0.24; model has 50 features, sample 5000",
                "correct": "Severe overfitting; features >> signal; reduce features via regularization or selection; increase lambda",
                "wrong": [
                    "Gap acceptable; within typical variance",
                    "Test set too small; gap inflated",
                    "Retrain model on test set",
                ]
            },
            {
                "context": "Train MSE 25, Test MSE 26, gap = 1; model has 5 features, 1000 observations",
                "correct": "Minimal gap; good generalization; low overfitting risk; model reliable for deployment",
                "wrong": [
                    "Any gap indicates overfitting",
                    "Gap > 0 means model failure",
                    "Increase features to improve train",
                ]
            },
            {
                "context": "Progressive with epochs: train loss decreases to 0.05; validation loss decreases to 0.20, then increases; neural net",
                "correct": "Early signs of overfitting; validation loss increases; stop training (early stopping); use model from epoch with min val loss",
                "wrong": [
                    "Train 0.05 excellent; continue training",
                    "Validation increasing means data issue",
                    "Validation noise; ignore; keep training",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Overfitting & Regularization",
            "subtopic": "Train-Test Gap",
            "difficulty": 2,
            "question_text": f"Diagnosing overfitting: {{scenario['context']}}. What should you do?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Train-test gap indicates overfitting. Remedies: reduce features, regularization (λ), early stopping, "
            "simpler models, or more training data. Minimize test error, not training error."
        }

    @classmethod
    def regularization_parameter_effect(cls) -> Dict[str, Any]:
        """Understand regularization parameter tuning."""
        scenarios = [
            {
                "context": "Ridge regression: λ=0 (no penalty): Train R²=0.95, Test R²=0.65; λ=1: Train 0.85, Test 0.82; λ=10: Train 0.70, Test 0.71",
                "correct": "λ=1 optimal; balances bias-variance; λ=0 overfits; λ=10 underfits; choose λ via CV",
                "wrong": [
                    "λ=0 best; highest training fit",
                    "λ=10 best; both R² equal (stable)",
                    "Regularization always hurts fit",
                ]
            },
            {
                "context": "Lasso regression: coefficients selected at different λ values; λ=0.001 selects 50 features, λ=0.1 selects 5; sparsity increases",
                "correct": "Larger λ drives more coefficients to zero; balance model sparsity with predictive power; use CV for optimal λ",
                "wrong": [
                    "λ=0.001 preferred; more features fit better",
                    "λ=0.1 preferred; parsimonious",
                    "Lasso always selects same features",
                ]
            },
            {
                "context": "Elastic net (α=0.5 mix ridge/lasso); parameter λ: test error U-shaped with minimum at λ=0.05; use this λ",
                "correct": "λ=0.05 minimizes test error; use for deployment; validate on holdout set; regularization necessary",
                "wrong": [
                    "λ=0 always best; minimize penalty",
                    "U-shaped curve means model unstable",
                    "Any λ > 0 arbitrary; choose smallest",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Overfitting & Regularization",
            "subtopic": "Regularization Parameter",
            "difficulty": 2,
            "question_text": f"Tuning regularization: {{scenario['context']}}. What parameter should you select?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Regularization parameter λ controls model complexity. Too small (λ→0) causes overfitting; "
            "too large (λ→∞) causes underfitting. Optimize via cross-validation on test/validation set."
        }

    @classmethod
    def stepwise_vs_lasso(cls) -> Dict[str, Any]:
        """Compare stepwise selection vs lasso."""
        scenarios = [
            {
                "context": "100 candidate predictors; stepwise (AIC): selects 15 features; lasso (CV): selects 12 features; high correlation among variables",
                "correct": "Lasso more stable; handles multicollinearity; stepwise unstable (backwards elimination order-dependent); prefer lasso",
                "wrong": [
                    "Stepwise simpler; easier to interpret",
                    "Both methods equivalent",
                    "Stepwise selects more features; overcomplexity",
                ]
            },
            {
                "context": "Stepwise selects: {X1, X5, X10}; remove X5, get {X1, X3, X10}; order affects selection; CV RMSE increases",
                "correct": "Stepwise is greedy, order-dependent, unstable; problematic for inference; use lasso for robustness",
                "wrong": [
                    "Both selections equally valid",
                    "Stepwise adaptive; second model better",
                    "Feature order irrelevant",
                ]
            },
            {
                "context": "p=5000 features, n=200 observations; stepwise infeasible (dimension); lasso via coordinate descent scales",
                "correct": "Lasso essential for high-dimensional; stepwise computationally prohibitive; lasso practical and theoretically grounded",
                "wrong": [
                    "Stepwise still possible with patience",
                    "PCA alternative but loses interpretability",
                    "High-dim requires neural networks",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Overfitting & Regularization",
            "subtopic": "Feature Selection Methods",
            "difficulty": 3,
            "question_text": f"Comparing selection methods: {{scenario['context']}}. Which should you use?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Stepwise selection is greedy, order-dependent, unstable; lasso regularization is convex, stable, "
            "handles multicollinearity, and scales to high dimensions. Prefer lasso/elastic net."
        }

    @classmethod
    def model_complexity_tradeoff(cls) -> Dict[str, Any]:
        """Evaluate complexity vs performance tradeoff."""
        scenarios = [
            {
                "context": "Model A: 3 features, AUC 0.73, easy to explain; Model B: 50 features, AUC 0.76, hard to explain; deployment",
                "correct": "Model A preferred; interpretability valuable in insurance; 0.73 adequate; AUC gain (0.03) not worth complexity",
                "wrong": [
                    "Model B; always prefer higher AUC",
                    "Models equivalent; choose randomly",
                    "Explainability irrelevant if accurate",
                ]
            },
            {
                "context": "Polynomial degrees: degree 1 RMSE=50, degree 5 RMSE=35, degree 15 RMSE=25 (train), 95 (test)",
                "correct": "Degree 5 balanced; degree 1 underfits; degree 15 severe overfitting; choose degree 5 via CV",
                "wrong": [
                    "Degree 15; lowest training error",
                    "Degree 1; simplest model",
                    "Degree 5 arbitrary",
                ]
            },
            {
                "context": "Random forest: 100 trees test AUC 0.78; 500 trees test AUC 0.78; computational cost 5x increase for no gain",
                "correct": "Stop at 100 trees; no improvement with 500; diminishing returns; 100-tree model sufficient",
                "wrong": [
                    "Use 500 trees; typically better",
                    "500 trees more stable",
                    "More trees always safer",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Overfitting & Regularization",
            "subtopic": "Complexity Tradeoff",
            "difficulty": 2,
            "question_text": f"Balancing complexity: {{scenario['context']}}. Which model should you choose?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Prefer simpler models that achieve acceptable performance: Occam's Razor. Complexity gains must "
            "justify cost in interpretability, maintenance, and overfitting risk."
        }

    @classmethod
    def early_stopping_rationale(cls) -> Dict[str, Any]:
        """Understand early stopping technique."""
        scenarios = [
            {
                "context": "Neural network training: epoch 1-50 validation loss decreases; epoch 51-200 validation loss plateaus then increases; stop early?",
                "correct": "Stop at epoch where validation loss minimized (~50-60); prevent overfitting; use that model for deployment",
                "wrong": [
                    "Continue training; more epochs always better",
                    "Stop when training loss reaches zero",
                    "Plateau means model converged; continue",
                ]
            },
            {
                "context": "Boosting (AdaBoost): training error 0.1%, test error 5% after 100 iterations; continue boosting?",
                "correct": "Stop or limit iterations; test error increasing while training improves (overfitting); validate optimal iterations",
                "wrong": [
                    "Continue; training still improving",
                    "Stop immediately; gap too large",
                    "Gap irrelevant; boosting self-regularizing",
                ]
            },
            {
                "context": "Gradient boosting: validation AUC improves to 0.80 by iteration 200, then plateaus at 0.801-0.802 for iterations 201-500",
                "correct": "Early stop around iteration 200; no meaningful improvement after; computational savings without performance loss",
                "wrong": [
                    "Continue to 500; every iteration adds",
                    "0.001 AUC improvement insignificant; stop at 50",
                    "Plateauing means model failure",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Overfitting & Regularization",
            "subtopic": "Early Stopping",
            "difficulty": 2,
            "question_text": f"Using early stopping: {{scenario['context']}}. What should you do?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Early stopping prevents overfitting by halting training when validation metric stops improving. "
            "Monitor validation error; stop when plateau or degradation observed; use best-epoch model."
        }

    @classmethod
    def ensemble_benefit(cls) -> Dict[str, Any]:
        """Evaluate ensemble method benefits."""
        scenarios = [
            {
                "context": "5 diverse models: AUC 0.72, 0.71, 0.69, 0.73, 0.70; ensemble (majority/average) AUC 0.75; correlation low",
                "correct": "Ensemble outperforms all individual models; uncorrelated errors reduce via averaging; use ensemble",
                "wrong": [
                    "Individual model (0.73) sufficient; ensemble gains marginal",
                    "Averaging unequal models suboptimal",
                    "Ensemble requires identical models",
                ]
            },
            {
                "context": "5 highly correlated models: all AUC 0.74; ensemble AUC 0.745; same preprocessing, similar features",
                "correct": "Correlated models; ensemble gains negligible; diversity essential; use single best model or retrain diverse",
                "wrong": [
                    "Ensemble always improves",
                    "0.005 AUC gain justifies ensemble complexity",
                    "Ensemble works regardless of correlation",
                ]
            },
            {
                "context": "Stacking 3 classifiers into meta-learner: base-level models AUC 0.70, 0.72, 0.68; stacked AUC 0.76; complex",
                "correct": "Stacking effective; meta-learner learns optimal combination; complexity justified if improved AUC stable on validation",
                "wrong": [
                    "3 models in 1 always beats individual",
                    "Stacking overcomplicates; use simple average",
                    "Base-level models must have AUC > 0.75",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Overfitting & Regularization",
            "subtopic": "Ensemble Methods",
            "difficulty": 3,
            "question_text": f"Evaluating ensemble methods: {{scenario['context']}}. Should you use ensemble?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Ensemble benefits from diverse, uncorrelated base models. Gains diminish with correlated models. "
            "Bagging reduces variance; boosting reduces bias; stacking learns combinations."
        }

    # ==================== COMMUNICATION & ETHICS (10 methods) ====================

    @classmethod
    def business_recommendation_from_model(cls) -> Dict[str, Any]:
        """Translate model results into business recommendations."""
        scenarios = [
            {
                "context": "Claims severity model: gender coefficient 0.15 (p=0.002); predicts female claims ~16% higher; stakeholder asks to price by gender",
                "correct": "Gender effect significant statistically; BUT regulatory risk (disparate impact); recommend alternative factors; "
                "investigate causality before pricing",
                "wrong": [
                    "Yes, price by gender; significant and large effect",
                    "No, exclude gender; never use protected attributes",
                    "Gender effect irrelevant for pricing",
                ]
            },
            {
                "context": "Customer churn model AUC 0.72; retention rate currently 88%; model identifies top 20% churn-risk; cost to save customer $50, CLV $500",
                "correct": "Target top 20% for $50 retention offer; ROI if save 20%: 0.2*0.2*$500=$20 < $50; check if CLV calculation, "
                "retention rate differ in top-20%",
                "wrong": [
                    "High CLV; offer retention to all churners",
                    "ROI negative; don't intervene",
                    "AUC 0.72 means 72% success rate",
                ]
            },
            {
                "context": "Model predicts high-cost claimants; accuracy high; insurer asks to deny coverage to flagged individuals",
                "correct": "Cannot deny coverage based on pure prediction; regulatory/ethical issue; recommend risk-based pricing instead; "
                "fair underwriting standard",
                "wrong": [
                    "Yes, deny coverage to high-cost individuals",
                    "Model predicts accurately; legally defensible",
                    "Denial strategy maximizes profit",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Communication & Ethics",
            "subtopic": "Business Recommendation",
            "difficulty": 3,
            "question_text": f"Translating model to business decision: {{scenario['context']}}. What do you recommend?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Model results inform but don't dictate decisions. Consider regulatory constraints, ethical implications, "
            "business cost/benefit, and causality. Statistical significance ≠ business impact or actionability."
        }

    @classmethod
    def non_technical_explanation(cls) -> Dict[str, Any]:
        """Explain model to non-technical stakeholders."""
        scenarios = [
            {
                "context": "Executive asks: what does coefficient 0.02 on age mean in your claim model? How do you explain clearly?",
                "correct": "Each year older, customers expected claims increase ~2%; or specific example: 40-year-old vs 50-year-old expected claims ~22% higher",
                "wrong": [
                    "Coefficient 0.02 means 2% direct increase",
                    "The log(coefficient) is 0.02",
                    "Cannot explain without statistician present",
                ]
            },
            {
                "context": "Non-technical team: what is AUC? How do you explain in business terms?",
                "correct": "AUC tells if model correctly ranks: higher score → higher risk. AUC=0.7 means 70% chance model gives "
                "higher score to random claim than non-claim",
                "wrong": [
                    "AUC is 70% prediction accuracy",
                    "AUC measures model complexity",
                    "AUC compares to baseline only",
                ]
            },
            {
                "context": "Regulator asks: how can you prove model is fair? What evidence?",
                "correct": "Test for demographic parity/disparate impact; show performance metrics stratified by protected classes; "
                "conduct sensitivity analysis; document decisions",
                "wrong": [
                    "High accuracy guarantees fairness",
                    "Cannot test fairness; inherent to data",
                    "Fairness is subjective opinion",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Communication & Ethics",
            "subtopic": "Non-Technical Explanation",
            "difficulty": 2,
            "question_text": f"Explaining to stakeholders: {{scenario['context']}}. How do you respond?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Effective communication translates technical concepts into business language. Use analogies, concrete examples, "
            "and avoid jargon. Tailor explanation to audience expertise level."
        }

    @classmethod
    def model_limitation_identification(cls) -> Dict[str, Any]:
        """Identify and communicate model limitations."""
        scenarios = [
            {
                "context": "Churn model trained on 2018-2020 data; deployed 2024; business stability has changed, product mix evolved",
                "correct": "Model obsolescence risk; data drift; recommend retraining on recent data; monitor performance drift; "
                "document training period limitation",
                "wrong": [
                    "Model timeless; static relationships hold",
                    "Retraining unnecessary if AUC high initially",
                    "External changes irrelevant to model",
                ]
            },
            {
                "context": "Claim amount model built on historical data; future claims uncertain; tail risk in 2008-style event; model silent on extreme scenarios",
                "correct": "Model reflects historical distribution; rare/extreme events underpredicted; stress test with extreme scenarios; "
                "document limitation for risk management",
                "wrong": [
                    "Historical data sufficient for all futures",
                    "Extreme events impossible; ignore",
                    "Model captures all risk",
                ]
            },
            {
                "context": "Model predicts claim probability; actual decision affected by underwriting rules, medical history, external factors",
                "correct": "Model estimates component of risk; decision depends on multiple factors; clearly delineate model scope; "
                "recommend human review for high-stakes decisions",
                "wrong": [
                    "Model determines all underwriting decisions",
                    "Factors outside model irrelevant",
                    "Model automates decision entirely",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Communication & Ethics",
            "subtopic": "Model Limitations",
            "difficulty": 2,
            "question_text": f"Documenting limitations: {{scenario['context']}}. What should you communicate?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "All models have limitations: historical bias, data drift, extrapolation risk, incomplete information, "
            "rare event underprediction. Transparent documentation builds appropriate trust and enables correct usage."
        }

    @classmethod
    def fairness_assessment(cls) -> Dict[str, Any]:
        """Assess fairness in model predictions."""
        scenarios = [
            {
                "context": "Model AUC: overall 0.75; by gender (male/female): 0.78/0.71; accuracy similar; disparate impact analysis needed?",
                "correct": "Yes; performance gap (AUC difference) suggests potential fairness issue; test for disparate impact; investigate drivers",
                "wrong": [
                    "Similar accuracy means fair model",
                    "AUC differences acceptable if overall fit good",
                    "Fairness and accuracy independent concerns",
                ]
            },
            {
                "context": "Model uses: age, income, credit score (no protected attributes); but credit score highly correlated with race",
                "correct": "Proxy discrimination risk; credit score correlates with race; test disparate impact; consider "
                "domain knowledge; may need alternative features",
                "wrong": [
                    "No protected attributes = fair model",
                    "Correlation irrelevant if not directly used",
                    "Income/credit/age always defensible",
                ]
            },
            {
                "context": "Fair lending audit: model approval rate 80% overall; by race: 82% (white), 75% (black); adverse impact?",
                "correct": "Potential adverse impact (75% < 80% * 0.8 threshold = 64% typically requires investigation); "
                "recommend explanation/remediation",
                "wrong": [
                    "7% difference acceptable",
                    "No protected attribute in model; approved",
                    "Overall rate determines fairness",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Communication & Ethics",
            "subtopic": "Fairness",
            "difficulty": 3,
            "question_text": f"Assessing fairness: {{scenario['context']}}. What should you do?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Fairness requires testing for disparate impact across protected classes. Proxy variables can create "
            "discrimination even if protected attributes excluded. Regulatory standards apply (e.g., 80% rule)."
        }

    @classmethod
    def disparate_impact_detection(cls) -> Dict[str, Any]:
        """Detect and quantify disparate impact."""
        scenarios = [
            {
                "context": "Hiring model approves: 100/120 white applicants (83%), 40/80 black applicants (50%); statistically significantly different",
                "correct": "Disparate impact detected; 50%/83% = 60% < 80% (4/5 rule); prima facie discrimination; explain or modify model",
                "wrong": [
                    "33% difference non-significant; approve",
                    "Cannot assess discrimination with proportions",
                    "100 white hires sufficient",
                ]
            },
            {
                "context": "Insurance rating: female average premium $800, male average $850; 5% difference; price elasticity analysis complex",
                "correct": "Small difference; verify non-discriminatory drivers; if justified (claims data), acceptable; document rationale; "
                "monitor over time",
                "wrong": [
                    "Any gender difference unacceptable",
                    "Males pay more; no discrimination",
                    "5% passes all fairness tests",
                ]
            },
            {
                "context": "Loan underwriting: approved amounts same race/gender; denial rates: 10% (majority), 18% (minority); "
                "prima facie case?",
                "correct": "Yes, denial rate difference (18% vs 10%) exceeds 80% rule threshold; triggers investigation; "
                "requires non-discriminatory explanation",
                "wrong": [
                    "Approved amounts same; no discrimination",
                    "8% difference is acceptable",
                    "Cannot assess discrimination without intent evidence",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Communication & Ethics",
            "subtopic": "Disparate Impact",
            "difficulty": 3,
            "question_text": f"Detecting disparate impact: {{scenario['context']}}. What's the assessment?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Disparate impact analyzed via 80% rule: minority outcome < 80% of majority indicates discrimination. "
            "Quantify with statistical tests. Document business necessity if impact detected."
        }

    @classmethod
    def proxy_variable_concern(cls) -> Dict[str, Any]:
        """Identify proxy variable risks."""
        scenarios = [
            {
                "context": "Model uses: ZIP code (correlated with neighborhood race/SES), income, home value. Race not in model.",
                "correct": "ZIP code may act as proxy for race/SES; disparate impact risk; test model by race; consider alternative location variables",
                "wrong": [
                    "No race variable = no proxy discrimination",
                    "ZIP code is geographic, not demographic",
                    "Proxies acceptable if not direct variables",
                ]
            },
            {
                "context": "Credit score (used in model) predicts default + correlates with race (r=0.35). Cannot exclude credit score.",
                "correct": "Proxy discrimination risk; test for disparate impact by race; justify business necessity; monitor regularly; "
                "consider alternative credit metrics",
                "wrong": [
                    "Credit score independent of race; no risk",
                    "r=0.35 too low to constitute proxy",
                    "Correlation irrelevant if causation lacking",
                ]
            },
            {
                "context": "Historical underwriting decisions (biased before) used to predict future claims. Model optimizes based on historical bias.",
                "correct": "Label bias / historical bias encoded; model perpetuates prior discrimination; recommend retraining on "
                "debiased labels or alternative outcomes",
                "wrong": [
                    "Historical data most accurate; use directly",
                    "Bias in labels doesn't affect model",
                    "Past underwriting decisions objective",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Communication & Ethics",
            "subtopic": "Proxy Variables",
            "difficulty": 3,
            "question_text": f"Identifying proxy variables: {{scenario['context']}}. What's your concern?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Proxies are variables correlated with protected attributes; using proxies can indirectly discriminate. "
            "Test for disparate impact; consider business necessity; monitor outcomes by demographic group."
        }

    @classmethod
    def regulatory_compliance_consideration(cls) -> Dict[str, Any]:
        """Consider regulatory constraints in modeling."""
        scenarios = [
            {
                "context": "Insurance regulation prohibits using education level for rating. Model's best predictor is education (coefficient significant).",
                "correct": "Remove education; comply with regulation; rebuild model with allowed variables; document decision; "
                "may sacrifice accuracy for legality",
                "wrong": [
                    "Education significant; use it for predictions",
                    "Education proxy allowable",
                    "Regulatory rules are guidelines, not hard",
                ]
            },
            {
                "context": "GDPR right-to-explanation for model decisions. Model is neural network (black box). Compliant?",
                "correct": "No; GDPR requires explainability; switch to interpretable model (linear, tree-based) or develop post-hoc explanation; "
                "document trade-offs",
                "wrong": [
                    "Neural network allowed; privacy laws don't apply",
                    "Post-hoc explanation sufficient for GDPR",
                    "Model accuracy exceeds explanation requirement",
                ]
            },
            {
                "context": "Fair Housing Act prohibits discrimination in lending. Model uses: income, credit, employment history, loan-to-value ratio.",
                "correct": "All variables allowed; verify no protected attributes; test for disparate impact; document rationale; "
                "ensure fair lending monitoring post-deployment",
                "wrong": [
                    "Variables allowed = fair model automatically",
                    "Disparate impact testing unnecessary",
                    "Protected classes have no Fair Housing protection",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Communication & Ethics",
            "subtopic": "Regulatory Compliance",
            "difficulty": 3,
            "question_text": f"Ensuring regulatory compliance: {{scenario['context']}}. How should you proceed?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Regulatory frameworks (Fair Lending, GDPR, etc.) impose constraints: prohibited variables, explainability "
            "requirements, disparate impact testing. Compliance is mandatory; may limit model complexity/accuracy."
        }

    @classmethod
    def model_documentation(cls) -> Dict[str, Any]:
        """Document model for governance and compliance."""
        scenarios = [
            {
                "context": "Model in production for 2 years; recently questions on methodology, feature changes, performance drift. Documentation minimal.",
                "correct": "Create comprehensive documentation: approach, data period, features, coefficients, performance metrics, "
                "limitations, maintenance plan",
                "wrong": [
                    "Documentation unnecessary; model works",
                    "Only preserve code comments",
                    "Verbal explanation to SMEs sufficient",
                ]
            },
            {
                "context": "Regulator asks: why is variable X in your model? Cannot explain coefficient interpretation or business justification.",
                "correct": "Severe governance gap; document feature rationale, statistical significance, business impact, and "
                "regulatory defensibility before deployment",
                "wrong": [
                    "Variable selection automatic; no explanation needed",
                    "Statistical significance sufficient justification",
                    "Regulator question means model failure",
                ]
            },
            {
                "context": "Model performance degrades over 6 months; stakeholders unaware; no monitoring documentation or refresh plan.",
                "correct": "Document performance monitoring plan: metrics tracked, refresh frequency, decision rules for retraining; "
                "implement before deployment",
                "wrong": [
                    "Monitoring unnecessary; model static",
                    "Refresh only if complained",
                    "Documentation of performance plan optional",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Communication & Ethics",
            "subtopic": "Documentation",
            "difficulty": 2,
            "question_text": f"Model governance: {{scenario['context']}}. What documentation is critical?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Comprehensive documentation supports governance, compliance, and transparency. Essential: methodology, data, "
            "features, performance, limitations, maintenance plan, monitoring strategy."
        }

    @classmethod
    def stakeholder_appropriate_metric(cls) -> Dict[str, Any]:
        """Select metrics appropriate for stakeholder needs."""
        scenarios = [
            {
                "context": "Executive wants ROI on marketing campaign using churn model. Analyst proposes AUC as metric.",
                "correct": "AUC irrelevant to ROI; need: model lift at deciles, cost per contact, CLV, retention rate, actual savings. "
                "ROI = (contacts * retention_rate * CLV - cost) / cost",
                "wrong": [
                    "AUC directly indicates campaign ROI",
                    "Higher AUC guarantees ROI",
                    "Marketing metrics same as modeling metrics",
                ]
            },
            {
                "context": "Regulator asks: is model fair? Actuary proposes AUC metric; regulator expects disparate impact analysis by race.",
                "correct": "AUC insufficient; report approval/denial rates, outcomes by protected class, statistical test for disparate impact, "
                "fairness metrics (parity, odds ratio)",
                "wrong": [
                    "AUC measures fairness implicitly",
                    "Fairness is subjective; AUC objective",
                    "Regulator wrong to ask for fairness",
                ]
            },
            {
                "context": "Reserving team needs claims projection model; analytics team proposes MAE (mean absolute error) as metric.",
                "correct": "MAE useful but incomplete; also need: directional bias (systematic under/over-reserve), tail risk (percentile errors), "
                "segment-specific errors",
                "wrong": [
                    "MAE sufficient for all uses",
                    "Reservation accuracy only requires average error",
                    "Tail risk irrelevant to reserving",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Communication & Ethics",
            "subtopic": "Stakeholder Metrics",
            "difficulty": 2,
            "question_text": f"Selecting metrics: {{scenario['context']}}. What metric(s) should you report?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Metrics must align with stakeholder decisions: business uses ROI/lift/cost-benefit; regulators need fairness; "
            "operations need calibration/tail risk. Tailor reporting to audience."
        }

    @classmethod
    def model_monitoring_plan(cls) -> Dict[str, Any]:
        """Design model monitoring and refresh plan."""
        scenarios = [
            {
                "context": "Claims prediction model deployed; business conditions (economy, competitors, products) changing; no monitoring plan.",
                "correct": "Establish monitoring: track AUC monthly, compare recent vs baseline; flag if AUC drops >5%; refresh annually or triggered; "
                "document triggers",
                "wrong": [
                    "Monitor annually only",
                    "No monitoring needed; model static",
                    "Refresh only on performance degradation",
                ]
            },
            {
                "context": "Model predicts policyholder income for rating. Data source changes quarterly (new vendor). How monitor for bias?",
                "correct": "Track income distribution: mean, median, percentiles by quarter; compare to historical; assess covariate shift; "
                "test for systematic bias from new vendor",
                "wrong": [
                    "Monitoring unnecessary; vendor certified",
                    "Track only model AUC; ignore data",
                    "Annual review sufficient",
                ]
            },
            {
                "context": "Model fairness assessment: baseline disparate impact ratio 0.95 (female to male approval). What's monitoring threshold?",
                "correct": "Set threshold <0.90 (4/5 rule); monitor quarterly; if ratio drops below, investigate causes and remediate; document all tests",
                "wrong": [
                    "Fairness static; no monitoring",
                    "0.95 = acceptable; no action needed",
                    "Only monitor if complaint filed",
                ]
            },
        ]
        scenario = scenarios[random.randint(0, len(scenarios) - 1)]
        choices = [scenario["correct"]] + scenario["wrong"]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "PA",
            "topic": "Communication & Ethics",
            "subtopic": "Monitoring",
            "difficulty": 3,
            "question_text": f"Designing monitoring: {{scenario['context']}}. What plan should you establish?",
            "choices": choices,
            "solution": scenario["correct"],
            "explanation": "Proactive monitoring detects data drift, performance degradation, and fairness issues. "
            "Set specific metrics, thresholds, and refresh triggers; automate where possible."
        }

    # ==================== UTILITY METHODS ====================

    @classmethod
    def get_all_methods(cls) -> List[str]:
        """Get list of all question generation methods."""
        methods = [
            # EDA
            'missing_data_strategy', 'outlier_detection_approach', 'variable_distribution_assessment',
            'correlation_interpretation', 'categorical_variable_handling', 'data_quality_issue',
            'sample_size_adequacy', 'target_variable_analysis',
            # Feature Engineering
            'variable_transformation_choice', 'interaction_term_need', 'binning_strategy',
            'one_hot_encoding_scenario', 'feature_selection_method', 'multicollinearity_resolution',
            'derived_variable_creation', 'text_feature_extraction',
            # GLM Application
            'distribution_family_selection', 'link_function_choice', 'offset_vs_weight',
            'overdispersion_handling', 'model_output_interpretation', 'coefficient_significance',
            'rate_relativities', 'base_level_impact', 'glm_prediction_scenario',
            'residual_pattern_interpretation',
            # Model Evaluation
            'confusion_matrix_metrics', 'auc_roc_interpretation', 'lift_chart_analysis',
            'gains_table_reading', 'model_comparison_multiple_metrics', 'gini_coefficient',
            'calibration_assessment', 'holdout_vs_cv',
            # Overfitting & Regularization
            'train_test_gap_diagnosis', 'regularization_parameter_effect', 'stepwise_vs_lasso',
            'model_complexity_tradeoff', 'early_stopping_rationale', 'ensemble_benefit',
            # Communication & Ethics
            'business_recommendation_from_model', 'non_technical_explanation',
            'model_limitation_identification', 'fairness_assessment', 'disparate_impact_detection',
            'proxy_variable_concern', 'regulatory_compliance_consideration',
            'model_documentation', 'stakeholder_appropriate_metric', 'model_monitoring_plan',
        ]
        return methods

    @classmethod
    def generate_all(cls, n_per_method: int = 100) -> List[Dict[str, Any]]:
        """Generate n questions for each method."""
        questions = []
        methods = cls.get_all_methods()

        for method_name in methods:
            method = getattr(cls, method_name)
            for _ in range(n_per_method):
                try:
                    question = method()
                    questions.append(question)
                except Exception as e:
                    # Skip any problematic generations
                    pass

        return questions
