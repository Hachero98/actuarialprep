"""
Exam SRM (Statistics for Risk Modeling) Question Generator

Generates computational and numerical questions on:
- Linear Regression
- Generalized Linear Models
- Time Series Analysis
- Principal Component Analysis
- Decision Trees
- Clustering
- Model Selection
"""

import random
import math
from typing import List, Dict, Any
from datetime import datetime
import uuid


class ExamSRMGenerator:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    """Generates SRM exam questions with numerical/computational scenarios."""

    @staticmethod
    def _generate_id() -> str:
        """Generate unique question ID."""
        return f"SRM_{uuid.uuid4().hex[:8].upper()}"

    @staticmethod
    def _round_to(value: float, decimals: int = 3) -> float:
        """Round value to specified decimals."""
        return round(value, decimals)

    # ==================== LINEAR REGRESSION (13 methods) ====================

    @classmethod
    def simple_linear_regression_coefficient(cls) -> Dict[str, Any]:
        """Calculate slope and intercept from summary statistics."""
        n = random.randint(20, 50)
        mean_x = round(random.uniform(10, 100), 2)
        mean_y = round(random.uniform(10, 100), 2)
        sxy = round(random.uniform(50, 500), 2)
        sxx = round(random.uniform(100, 1000), 2)

        slope = cls._round_to(sxy / sxx, 3)
        intercept = cls._round_to(mean_y - slope * mean_x, 3)

        choices = [
            f"Slope = {slope}, Intercept = {intercept}",
            f"Slope = {cls._round_to(slope * 1.1, 3)}, Intercept = {intercept}",
            f"Slope = {slope}, Intercept = {cls._round_to(intercept * 1.1, 3)}",
            f"Slope = {cls._round_to(slope * 0.9, 3)}, Intercept = {cls._round_to(intercept * 0.9, 3)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Simple Linear Regression",
            "difficulty": 1,
            "question_text": f"For a simple linear regression with n={n}, mean(X)={mean_x}, mean(Y)={mean_y}, "
            f"S_xy={sxy}, and S_xx={sxx}, calculate the slope and intercept coefficients.",
            "choices": choices,
            "solution": f"Slope = {slope}, Intercept = {intercept}",
            "explanation": f"Using formulas: β₁ = S_xy/S_xx = {sxy}/{sxx} = {slope}. "
            f"β₀ = mean(Y) - β₁*mean(X) = {mean_y} - {slope}*{mean_x} = {intercept}."
        }

    @classmethod
    def interpret_slope(cls) -> Dict[str, Any]:
        """Interpret slope coefficient in context."""
        slope = round(random.uniform(0.5, 5), 2)
        x_unit = random.choice(["dollar", "year", "unit", "percentage point"])
        y_variable = random.choice(["claims frequency", "premium", "loss ratio", "claim severity"])

        choices = [
            f"For each additional {x_unit}, {y_variable} increases by {slope}",
            f"For each additional {x_unit}, {y_variable} decreases by {slope}",
            f"For each additional {x_unit}, {y_variable} increases by {slope}%",
            f"{y_variable} equals {slope} when {x_unit} is zero",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Slope Interpretation",
            "difficulty": 1,
            "question_text": f"A regression model has slope coefficient β₁ = {slope}. The predictor is measured in {x_unit}s "
            f"and response is {y_variable}. Interpret this slope.",
            "choices": choices,
            "solution": f"For each additional {x_unit}, {y_variable} increases by {slope}",
            "explanation": f"The slope represents the change in the response variable for a unit increase in the predictor. "
            f"A slope of {slope} means {y_variable} increases by {slope} units per additional {x_unit}."
        }

    @classmethod
    def multiple_regression_prediction(cls) -> Dict[str, Any]:
        """Predict response using multiple regression model."""
        intercept = round(random.uniform(10, 100), 2)
        beta1 = round(random.uniform(0.5, 5), 2)
        beta2 = round(random.uniform(-3, 3), 2)
        beta3 = round(random.uniform(0.1, 2), 2)

        x1 = round(random.uniform(10, 50), 1)
        x2 = round(random.uniform(0, 100), 1)
        x3 = round(random.uniform(1, 10), 1)

        prediction = cls._round_to(intercept + beta1 * x1 + beta2 * x2 + beta3 * x3, 2)

        choices = [
            str(prediction),
            str(cls._round_to(prediction * 1.1, 2)),
            str(cls._round_to(prediction * 0.9, 2)),
            str(cls._round_to(intercept + beta1 * x1 + beta2 * x2, 2)),
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Multiple Regression",
            "difficulty": 1,
            "question_text": f"Given model: Y = {intercept} + {beta1}*X₁ + {beta2}*X₂ + {beta3}*X₃. "
            f"Predict Y for X₁={x1}, X₂={x2}, X₃={x3}.",
            "choices": choices,
            "solution": str(prediction),
            "explanation": f"Y = {intercept} + {beta1}*{x1} + {beta2}*{x2} + {beta3}*{x3} = {prediction}"
        }

    @classmethod
    def r_squared_interpretation(cls) -> Dict[str, Any]:
        """Interpret R-squared value."""
        r_squared = round(random.uniform(0.4, 0.95), 3)
        pct = r_squared * 100

        choices = [
            f"{pct}% of variation in response is explained by the model",
            f"The correlation between X and Y is {math.sqrt(r_squared):.3f}",
            f"The model explains {r_squared}% of the sum of squares",
            f"The prediction error is {1 - r_squared} units",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Model Fit",
            "difficulty": 2,
            "question_text": f"A linear regression model has R² = {r_squared}. What does this mean?",
            "choices": choices,
            "solution": f"{pct}% of variation in response is explained by the model",
            "explanation": f"R² represents the proportion of variance in the response explained by the predictors. "
            f"An R² of {r_squared} means {pct}% of the variation in Y is explained by the model."
        }

    @classmethod
    def adjusted_r_squared(cls) -> Dict[str, Any]:
        """Calculate adjusted R-squared."""
        n = random.randint(30, 100)
        p = random.randint(2, 8)
        r_squared = round(random.uniform(0.5, 0.95), 3)

        adj_r_squared = cls._round_to(1 - ((1 - r_squared) * (n - 1) / (n - p - 1)), 3)

        choices = [
            str(adj_r_squared),
            str(cls._round_to(r_squared, 3)),
            str(cls._round_to(adj_r_squared - 0.05, 3)),
            str(cls._round_to(1 - ((1 - r_squared) * (n - 1) / (n - p)), 3)),
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Model Fit",
            "difficulty": 2,
            "question_text": f"Calculate adjusted R² for: n={n}, p={p} (predictors), R²={r_squared}",
            "choices": choices,
            "solution": str(adj_r_squared),
            "explanation": f"Adj R² = 1 - [(1-R²)*(n-1)/(n-p-1)] = 1 - [(1-{r_squared})*{n-1}/{n-p-1}] = {adj_r_squared}. "
            f"Adjusted R² penalizes for model complexity."
        }

    @classmethod
    def f_test_significance(cls) -> Dict[str, Any]:
        """Calculate F-statistic for overall model significance."""
        r_squared = round(random.uniform(0.3, 0.85), 3)
        n = random.randint(30, 100)
        p = random.randint(2, 10)

        f_stat = cls._round_to((r_squared / p) / ((1 - r_squared) / (n - p - 1)), 2)

        choices = [
            f"F = {f_stat}",
            f"F = {cls._round_to(f_stat * 1.2, 2)}",
            f"F = {cls._round_to(f_stat * 0.8, 2)}",
            f"F = {cls._round_to((1 - r_squared) / r_squared, 2)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Hypothesis Testing",
            "difficulty": 2,
            "question_text": f"Calculate F-statistic: R²={r_squared}, n={n}, p={p}. "
            f"F = (R²/p) / ((1-R²)/(n-p-1))",
            "choices": choices,
            "solution": f"F = {f_stat}",
            "explanation": f"F = ({r_squared}/{p}) / ((1-{r_squared})/({n}-{p}-1)) = {f_stat}. "
            f"Large F values indicate the model is significant overall."
        }

    @classmethod
    def residual_analysis(cls) -> Dict[str, Any]:
        """Analyze residual patterns."""
        residuals = [round(random.gauss(0, 5), 2) for _ in range(30)]
        mean_residual = cls._round_to(sum(residuals) / len(residuals), 3)
        std_residual = cls._round_to(math.sqrt(sum((r - mean_residual) ** 2 for r in residuals) / (len(residuals) - 1)), 3)

        choices = [
            f"Mean = {mean_residual}, StDev = {std_residual}",
            f"Mean = {mean_residual}, StDev = {cls._round_to(std_residual * 1.1, 3)}",
            f"Mean = {cls._round_to(mean_residual * 1.5, 3)}, StDev = {std_residual}",
            f"Mean = 1.0, StDev = {std_residual}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Diagnostics",
            "difficulty": 2,
            "question_text": f"A regression residual analysis shows: {residuals[:5]}... (30 residuals). "
            f"Calculate mean and standard deviation of residuals.",
            "choices": choices,
            "solution": f"Mean = {mean_residual}, StDev = {std_residual}",
            "explanation": f"Good residuals should have mean near 0 and constant variance. "
            f"Mean = {mean_residual}, StDev = {std_residual}."
        }

    @classmethod
    def heteroscedasticity_detection(cls) -> Dict[str, Any]:
        """Identify heteroscedasticity pattern."""
        patterns = [
            ("Residuals increase with fitted values", "Heteroscedasticity present"),
            ("Residuals randomly scattered around zero", "No heteroscedasticity"),
            ("Residuals show increasing trend", "Heteroscedasticity present"),
            ("All residuals equal to zero", "Perfect fit"),
        ]
        true_pattern, correct_answer = patterns[random.randint(0, 2)]

        choices = [correct_answer]
        alternatives = [
            "Homoscedasticity assumed",
            "Model is misspecified",
            "Multicollinearity present",
            "Heteroscedasticity detected",
        ]
        for alt in alternatives:
            if alt != correct_answer:
                choices.append(alt)
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Diagnostics",
            "difficulty": 2,
            "question_text": f"A residual plot shows: {true_pattern}. What does this indicate?",
            "choices": choices,
            "solution": correct_answer,
            "explanation": f"When residual variance increases with fitted values, this indicates heteroscedasticity. "
            f"The pattern '{true_pattern}' suggests {correct_answer}."
        }

    @classmethod
    def multicollinearity_vif(cls) -> Dict[str, Any]:
        """Calculate and interpret VIF."""
        r_squared_with_other = round(random.uniform(0.5, 0.95), 3)
        vif = cls._round_to(1 / (1 - r_squared_with_other), 2)

        choices = [
            f"VIF = {vif}",
            f"VIF = {cls._round_to(1 - r_squared_with_other, 2)}",
            f"VIF = {cls._round_to(vif * 1.5, 2)}",
            f"VIF = {cls._round_to(1 / r_squared_with_other, 2)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Multicollinearity",
            "difficulty": 2,
            "question_text": f"When a predictor is regressed on others, R² = {r_squared_with_other}. "
            f"Calculate VIF = 1/(1-R²).",
            "choices": choices,
            "solution": f"VIF = {vif}",
            "explanation": f"VIF = 1/(1-{r_squared_with_other}) = {vif}. "
            f"VIF > 5-10 suggests multicollinearity concerns."
        }

    @classmethod
    def partial_f_test(cls) -> Dict[str, Any]:
        """Calculate partial F-test for subset of coefficients."""
        ssr_full = round(random.uniform(500, 2000), 1)
        ssr_reduced = round(random.uniform(300, ssr_full - 100), 1)
        n = random.randint(50, 150)
        p_full = random.randint(3, 10)
        p_reduced = p_full - random.randint(1, 3)

        f_stat = cls._round_to(((ssr_full - ssr_reduced) / (p_full - p_reduced)) / (ssr_reduced / (n - p_full - 1)), 2)

        choices = [
            f"F = {f_stat}",
            f"F = {cls._round_to(f_stat * 1.2, 2)}",
            f"F = {cls._round_to((ssr_full - ssr_reduced) / (p_full - p_reduced), 2)}",
            f"F = {cls._round_to((ssr_full - ssr_reduced) / ssr_reduced, 2)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Hypothesis Testing",
            "difficulty": 3,
            "question_text": f"Partial F-test: SSR_full={ssr_full}, SSR_reduced={ssr_reduced}, "
            f"p_full={p_full}, p_reduced={p_reduced}, n={n}. "
            f"Calculate F = ((SSR_full-SSR_reduced)/(p_full-p_reduced)) / (SSR_reduced/(n-p_full-1))",
            "choices": choices,
            "solution": f"F = {f_stat}",
            "explanation": f"F = (({ssr_full}-{ssr_reduced})/({p_full}-{p_reduced})) / ({ssr_reduced}/({n}-{p_full}-1)) = {f_stat}"
        }

    @classmethod
    def confidence_interval_prediction(cls) -> Dict[str, Any]:
        """Calculate confidence interval for prediction."""
        predicted_value = round(random.uniform(50, 200), 2)
        se = round(random.uniform(5, 20), 2)
        t_crit = round(random.uniform(1.96, 2.5), 2)

        margin = cls._round_to(t_crit * se, 2)
        lower = cls._round_to(predicted_value - margin, 2)
        upper = cls._round_to(predicted_value + margin, 2)

        choices = [
            f"({lower}, {upper})",
            f"({cls._round_to(predicted_value - se, 2)}, {cls._round_to(predicted_value + se, 2)})",
            f"({cls._round_to(lower - 5, 2)}, {cls._round_to(upper + 5, 2)})",
            f"({lower}, {cls._round_to(upper * 1.1, 2)})",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Inference",
            "difficulty": 2,
            "question_text": f"Predicted value = {predicted_value}, SE = {se}, t-critical = {t_crit}. "
            f"Calculate 95% CI: predicted ± t*SE.",
            "choices": choices,
            "solution": f"({lower}, {upper})",
            "explanation": f"CI = {predicted_value} ± {t_crit}*{se} = {predicted_value} ± {margin} = ({lower}, {upper})"
        }

    @classmethod
    def leverage_influence(cls) -> Dict[str, Any]:
        """Identify leverage and influence points."""
        n = random.randint(30, 80)
        p = random.randint(2, 6)
        h_threshold = cls._round_to(3 * p / n, 3)
        h_value = round(random.uniform(0.02, 0.5), 3)

        if h_value > h_threshold:
            status = "High leverage point"
        else:
            status = "Normal leverage point"

        choices = [status]
        alternatives = [
            "High leverage point",
            "Normal leverage point",
            "Outlier in Y-direction",
            "Influential point",
        ]
        for alt in alternatives:
            if alt != status:
                choices.append(alt)
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Diagnostics",
            "difficulty": 2,
            "question_text": f"A point has leverage h = {h_value}. Threshold = 3p/n = 3*{p}/{n} = {h_threshold}. "
            f"Is this a high leverage point?",
            "choices": choices,
            "solution": status,
            "explanation": f"Threshold for high leverage is 3p/n = {h_threshold}. "
            f"Since {h_value} {'>' if h_value > h_threshold else '<'} {h_threshold}, this is a {status}."
        }

    @classmethod
    def dummy_variable_regression(cls) -> Dict[str, Any]:
        """Handle categorical variables with dummy coding."""
        categories = random.randint(3, 5)
        base_coef = round(random.uniform(50, 150), 2)
        dummy_coefs = [round(random.uniform(-30, 50), 2) for _ in range(categories - 1)]

        choices = [
            f"{categories - 1} dummy variables needed",
            f"{categories} dummy variables needed",
            f"{categories - 2} dummy variables needed",
            f"No dummy variables needed",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Linear Regression",
            "subtopic": "Categorical Variables",
            "difficulty": 2,
            "question_text": f"A categorical variable has {categories} categories. "
            f"How many dummy variables are needed to avoid multicollinearity?",
            "choices": choices,
            "solution": f"{categories - 1} dummy variables needed",
            "explanation": f"To represent {categories} categories without multicollinearity, use {categories - 1} dummy variables. "
            f"One category is the reference level."
        }

    # ==================== GENERALIZED LINEAR MODELS (10 methods) ====================

    @classmethod
    def poisson_regression_predict(cls) -> Dict[str, Any]:
        """Predict using Poisson regression."""
        intercept = round(random.uniform(-2, 2), 2)
        beta = round(random.uniform(0.1, 0.5), 2)
        x = round(random.uniform(1, 20), 1)

        linear_pred = intercept + beta * x
        lambda_param = cls._round_to(math.exp(linear_pred), 3)

        choices = [
            f"λ = {lambda_param}",
            f"λ = {cls._round_to(math.exp(intercept), 3)}",
            f"λ = {cls._round_to(linear_pred, 3)}",
            f"λ = {cls._round_to(lambda_param * 1.2, 3)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Generalized Linear Models",
            "subtopic": "Poisson Regression",
            "difficulty": 2,
            "question_text": f"Poisson regression: intercept={intercept}, β={beta}, x={x}. "
            f"Calculate λ = exp(η) where η = intercept + β*x.",
            "choices": choices,
            "solution": f"λ = {lambda_param}",
            "explanation": f"η = {intercept} + {beta}*{x} = {linear_pred}. λ = e^{linear_pred} = {lambda_param}"
        }

    @classmethod
    def logistic_regression_odds_ratio(cls) -> Dict[str, Any]:
        """Calculate odds ratio from logistic coefficient."""
        beta = round(random.uniform(-1, 2), 2)
        odds_ratio = cls._round_to(math.exp(beta), 3)

        choices = [
            f"OR = {odds_ratio}",
            f"OR = {cls._round_to(math.exp(beta * 2), 3)}",
            f"OR = {beta}",
            f"OR = {cls._round_to(1 / odds_ratio, 3)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Generalized Linear Models",
            "subtopic": "Logistic Regression",
            "difficulty": 2,
            "question_text": f"Logistic regression coefficient β = {beta}. "
            f"Calculate odds ratio (OR = e^β).",
            "choices": choices,
            "solution": f"OR = {odds_ratio}",
            "explanation": f"OR = e^{beta} = {odds_ratio}. "
            f"A one-unit increase in X multiplies odds by {odds_ratio}."
        }

    @classmethod
    def logistic_regression_probability(cls) -> Dict[str, Any]:
        """Calculate probability from logistic regression."""
        intercept = round(random.uniform(-3, 3), 2)
        beta = round(random.uniform(-1, 2), 2)
        x = round(random.uniform(1, 10), 1)

        eta = intercept + beta * x
        probability = cls._round_to(1 / (1 + math.exp(-eta)), 3)

        choices = [
            f"P = {probability}",
            f"P = {cls._round_to(1 / (1 + math.exp(eta)), 3)}",
            f"P = {cls._round_to(eta / (1 + eta), 3)}",
            f"P = {cls._round_to(probability * 1.1, 3)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Generalized Linear Models",
            "subtopic": "Logistic Regression",
            "difficulty": 2,
            "question_text": f"Logistic model: intercept={intercept}, β={beta}, x={x}. "
            f"Calculate P = 1/(1+e^(-η)) where η = intercept + β*x.",
            "choices": choices,
            "solution": f"P = {probability}",
            "explanation": f"η = {intercept} + {beta}*{x} = {eta}. P = 1/(1+e^(-{eta})) = {probability}"
        }

    @classmethod
    def log_link_interpretation(cls) -> Dict[str, Any]:
        """Interpret log-link coefficient."""
        beta = round(random.uniform(0.05, 0.3), 2)
        pct_change = cls._round_to((math.exp(beta) - 1) * 100, 1)

        choices = [
            f"Mean increases by {pct_change}%",
            f"Mean increases by {beta}%",
            f"Mean increases by {cls._round_to((math.exp(beta) - 1), 3)}",
            f"Mean increases by {pct_change}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Generalized Linear Models",
            "subtopic": "Link Functions",
            "difficulty": 2,
            "question_text": f"A GLM with log link has coefficient β = {beta}. "
            f"What is the percent change in mean for unit increase in X?",
            "choices": choices,
            "solution": f"Mean increases by {pct_change}%",
            "explanation": f"With log link, e^β - 1 = e^{beta} - 1 = {math.exp(beta) - 1:.3f} = {pct_change}% change."
        }

    @classmethod
    def deviance_comparison(cls) -> Dict[str, Any]:
        """Calculate deviance and compare models."""
        deviance_full = round(random.uniform(100, 300), 1)
        deviance_reduced = round(random.uniform(deviance_full, deviance_full + 100), 1)
        df_diff = random.randint(1, 4)

        chi_square = cls._round_to(deviance_reduced - deviance_full, 2)

        choices = [
            f"χ² = {chi_square}, df = {df_diff}",
            f"χ² = {cls._round_to(chi_square / df_diff, 2)}, df = {df_diff}",
            f"χ² = {cls._round_to(deviance_full, 2)}, df = {df_diff}",
            f"χ² = {cls._round_to(deviance_reduced - deviance_full - 10, 2)}, df = {df_diff}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Generalized Linear Models",
            "subtopic": "Model Comparison",
            "difficulty": 2,
            "question_text": f"Full model deviance = {deviance_full}, Reduced model deviance = {deviance_reduced}. "
            f"Calculate likelihood ratio test statistic (df = {df_diff}).",
            "choices": choices,
            "solution": f"χ² = {chi_square}, df = {df_diff}",
            "explanation": f"χ² = Deviance_reduced - Deviance_full = {deviance_reduced} - {deviance_full} = {chi_square}"
        }

    @classmethod
    def aic_model_selection(cls) -> Dict[str, Any]:
        """Compare models using AIC."""
        ll_model1 = round(random.uniform(-150, -50), 1)
        ll_model2 = round(random.uniform(ll_model1 - 30, ll_model1 + 10), 1)
        p1 = random.randint(3, 8)
        p2 = p1 + random.randint(1, 3)

        aic1 = cls._round_to(-2 * ll_model1 + 2 * p1, 1)
        aic2 = cls._round_to(-2 * ll_model2 + 2 * p2, 1)

        better = "Model 1" if aic1 < aic2 else "Model 2"

        choices = [
            better,
            "Model 1" if better != "Model 1" else "Model 2",
            "Cannot determine",
            "Same fit",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Generalized Linear Models",
            "subtopic": "Model Selection",
            "difficulty": 2,
            "question_text": f"Model 1: LL={ll_model1}, p={p1}. Model 2: LL={ll_model2}, p={p2}. "
            f"AIC = -2*LL + 2*p. Which is better?",
            "choices": choices,
            "solution": better,
            "explanation": f"AIC₁ = {aic1}, AIC₂ = {aic2}. Lower AIC is better, so {better} is preferred."
        }

    @classmethod
    def offset_variable_usage(cls) -> Dict[str, Any]:
        """Calculate prediction with offset variable."""
        intercept = round(random.uniform(-1, 1), 2)
        beta = round(random.uniform(0.1, 0.5), 2)
        x = round(random.uniform(5, 20), 1)
        offset = round(random.uniform(2, 10), 1)

        eta = intercept + beta * x + offset
        mu = cls._round_to(math.exp(eta), 2)

        choices = [
            f"μ = {mu}",
            f"μ = {cls._round_to(math.exp(intercept + beta * x), 2)}",
            f"μ = {cls._round_to(eta, 2)}",
            f"μ = {cls._round_to(mu / math.exp(offset), 2)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Generalized Linear Models",
            "subtopic": "Offset Variables",
            "difficulty": 2,
            "question_text": f"GLM with offset: intercept={intercept}, β={beta}, x={x}, offset={offset}. "
            f"Calculate μ = exp(η) with offset included.",
            "choices": choices,
            "solution": f"μ = {mu}",
            "explanation": f"η = {intercept} + {beta}*{x} + {offset} = {eta}. μ = e^{eta} = {mu}"
        }

    @classmethod
    def dispersion_parameter(cls) -> Dict[str, Any]:
        """Calculate dispersion parameter."""
        deviance = round(random.uniform(50, 200), 1)
        df_residual = random.randint(20, 80)
        phi = cls._round_to(deviance / df_residual, 3)

        choices = [
            f"φ = {phi}",
            f"φ = {cls._round_to(deviance / (df_residual - 1), 3)}",
            f"φ = {cls._round_to(df_residual / deviance, 3)}",
            f"φ = {cls._round_to(phi * 1.2, 3)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Generalized Linear Models",
            "subtopic": "Overdispersion",
            "difficulty": 2,
            "question_text": f"Deviance = {deviance}, df_residual = {df_residual}. "
            f"Calculate dispersion parameter φ = Deviance/df.",
            "choices": choices,
            "solution": f"φ = {phi}",
            "explanation": f"φ = {deviance}/{df_residual} = {phi}. "
            f"If φ > 1, overdispersion is present."
        }

    @classmethod
    def glm_link_function_identify(cls) -> Dict[str, Any]:
        """Identify appropriate link function."""
        response_types = [
            ("Binary outcome", "logit"),
            ("Count data", "log"),
            ("Positive continuous", "log"),
            ("Proportions 0-1", "logit"),
        ]
        response_type, correct_link = response_types[random.randint(0, len(response_types) - 1)]

        choices = [correct_link]
        alternatives = ["log", "logit", "identity", "inverse"]
        for alt in alternatives:
            if alt != correct_link:
                choices.append(alt)
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Generalized Linear Models",
            "subtopic": "Link Functions",
            "difficulty": 2,
            "question_text": f"Which link function is appropriate for: {response_type}?",
            "choices": choices,
            "solution": correct_link,
            "explanation": f"For {response_type}, the {correct_link} link function constrains predictions appropriately."
        }

    @classmethod
    def glm_residual_analysis(cls) -> Dict[str, Any]:
        """Analyze GLM residuals."""
        n = 50
        residuals = [round(random.gauss(0, 0.8), 2) for _ in range(n)]
        mean_resid = cls._round_to(sum(residuals) / n, 3)
        pearson_chisq = cls._round_to(sum(r ** 2 for r in residuals), 2)

        choices = [
            f"Pearson χ² ≈ {pearson_chisq}",
            f"Pearson χ² ≈ {cls._round_to(pearson_chisq * 1.1, 2)}",
            f"Pearson χ² ≈ {cls._round_to(sum(abs(r) for r in residuals), 2)}",
            f"Pearson χ² ≈ {n}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Generalized Linear Models",
            "subtopic": "Diagnostics",
            "difficulty": 2,
            "question_text": f"GLM has {n} standardized residuals: {residuals[:5]}... "
            f"Calculate Pearson χ² = Σ(r²).",
            "choices": choices,
            "solution": f"Pearson χ² ≈ {pearson_chisq}",
            "explanation": f"Pearson χ² = sum of squared standardized residuals = {pearson_chisq}. "
            f"Divided by df, this tests goodness of fit."
        }

    # ==================== TIME SERIES (10 methods) ====================

    @classmethod
    def ar1_identify_parameters(cls) -> Dict[str, Any]:
        """Identify AR(1) model parameters."""
        phi = round(random.uniform(-0.9, 0.9), 2)
        sigma_sq = round(random.uniform(0.5, 5), 2)
        y0 = round(random.uniform(10, 50), 1)

        y1 = cls._round_to(phi * y0 + round(random.gauss(0, math.sqrt(sigma_sq)), 2), 2)

        choices = [
            f"AR(1): φ = {phi}, σ² = {sigma_sq}",
            f"AR(1): φ = {cls._round_to(phi * 1.1, 2)}, σ² = {sigma_sq}",
            f"AR(2): φ₁ = {phi}, φ₂ = {cls._round_to(phi / 2, 2)}",
            f"MA(1): θ = {phi}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Time Series",
            "subtopic": "AR Models",
            "difficulty": 2,
            "question_text": f"Time series follows AR(1): Yₜ = φYₜ₋₁ + εₜ. "
            f"Observed: Y₀={y0}, Y₁={y1}, σ²={sigma_sq}. "
            f"Estimate φ ≈ Y₁/Y₀ = {cls._round_to(y1/y0, 2)}. What is model?",
            "choices": choices,
            "solution": f"AR(1): φ = {phi}, σ² = {sigma_sq}",
            "explanation": f"AR(1) model with autocorrelation φ and error variance σ²."
        }

    @classmethod
    def ma1_identify_parameters(cls) -> Dict[str, Any]:
        """Identify MA(1) model parameters."""
        theta = round(random.uniform(-0.95, 0.95), 2)
        sigma_sq = round(random.uniform(0.5, 5), 2)

        # MA(1) ACF at lag 1
        acf_lag1 = cls._round_to(-theta / (1 + theta ** 2), 3)

        choices = [
            f"MA(1): θ = {theta}, ACF(1) = {acf_lag1}",
            f"MA(1): θ = {cls._round_to(theta * 1.1, 2)}, ACF(1) = {acf_lag1}",
            f"AR(1): φ = {theta}",
            f"ARMA(1,1): φ = {theta}, θ = {cls._round_to(theta / 2, 2)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Time Series",
            "subtopic": "MA Models",
            "difficulty": 2,
            "question_text": f"MA(1) model with θ = {theta}. "
            f"Calculate autocorrelation at lag 1: ρ₁ = -θ/(1+θ²).",
            "choices": choices,
            "solution": f"MA(1): θ = {theta}, ACF(1) = {acf_lag1}",
            "explanation": f"For MA(1), ρ₁ = -θ/(1+θ²) = -{theta}/(1+{theta}²) = {acf_lag1}"
        }

    @classmethod
    def arma_forecast(cls) -> Dict[str, Any]:
        """ARMA model forecasting."""
        phi = round(random.uniform(0.3, 0.8), 2)
        theta = round(random.uniform(-0.5, 0.5), 2)
        last_y = round(random.uniform(10, 50), 1)
        last_epsilon = round(random.uniform(-3, 3), 1)

        forecast_1 = cls._round_to(phi * last_y + theta * last_epsilon, 2)
        forecast_2 = cls._round_to(phi * forecast_1, 2)

        choices = [
            f"F₁ = {forecast_1}, F₂ = {forecast_2}",
            f"F₁ = {cls._round_to(phi * last_y, 2)}, F₂ = {forecast_2}",
            f"F₁ = {cls._round_to(forecast_1 * 1.1, 2)}, F₂ = {cls._round_to(forecast_2 * 1.1, 2)}",
            f"F₁ = {last_y}, F₂ = {forecast_2}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Time Series",
            "subtopic": "ARMA Forecasting",
            "difficulty": 2,
            "question_text": f"ARMA(1,1): φ={phi}, θ={theta}. Last observed: Y={last_y}, ε={last_epsilon}. "
            f"Forecast Y_{'{t+1}'} and Y_{'{t+2}'}.",
            "choices": choices,
            "solution": f"F₁ = {forecast_1}, F₂ = {forecast_2}",
            "explanation": f"F₁ = {phi}*{last_y} + {theta}*{last_epsilon} = {forecast_1}. "
            f"F₂ = {phi}*{forecast_1} + 0 = {forecast_2} (MA term drops out)"
        }

    @classmethod
    def stationarity_check(cls) -> Dict[str, Any]:
        """Check stationarity conditions."""
        phi1 = round(random.uniform(-1, 1), 2)
        phi2 = round(random.uniform(-1, 1), 2) if random.random() > 0.5 else 0

        # AR(2) stationarity: phi1 + phi2 < 1, phi2 - phi1 < 1, |phi2| < 1
        conditions_met = (phi1 + phi2 < 1) and (phi2 - phi1 < 1) and (abs(phi2) < 1)
        status = "Stationary" if conditions_met else "Non-stationary"

        choices = [status]
        alternatives = ["Stationary", "Non-stationary", "Trend-stationary", "Cannot determine"]
        for alt in alternatives:
            if alt != status:
                choices.append(alt)
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Time Series",
            "subtopic": "Stationarity",
            "difficulty": 2,
            "question_text": f"AR(2) with φ₁={phi1}, φ₂={phi2}. "
            f"Check stationarity: φ₁+φ₂<1, |φ₂|<1, φ₂-φ₁<1.",
            "choices": choices,
            "solution": status,
            "explanation": f"Conditions: {phi1}+{phi2}={phi1+phi2}<1? {phi1+phi2<1}. "
            f"|{phi2}|<1? {abs(phi2)<1}. Series is {status}."
        }

    @classmethod
    def acf_pacf_model_identification(cls) -> Dict[str, Any]:
        """Identify model type from ACF/PACF."""
        patterns = [
            ("ACF cuts off at lag 1, PACF decays", "MA(1)"),
            ("ACF decays, PACF cuts off at lag 1", "AR(1)"),
            ("Both ACF and PACF decay", "ARMA(1,1)"),
            ("ACF cuts off at lag 2, PACF decays", "MA(2)"),
        ]
        pattern, correct_model = patterns[random.randint(0, len(patterns) - 1)]

        choices = [correct_model]
        alternatives = ["AR(1)", "MA(1)", "ARMA(1,1)", "ARIMA(1,1,1)", "MA(2)"]
        for alt in alternatives:
            if alt != correct_model:
                choices.append(alt)
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Time Series",
            "subtopic": "Model Identification",
            "difficulty": 2,
            "question_text": f"ACF/PACF pattern: {pattern}. What is the appropriate model?",
            "choices": choices,
            "solution": correct_model,
            "explanation": f"Pattern '{pattern}' indicates {correct_model}."
        }

    @classmethod
    def differencing_for_stationarity(cls) -> Dict[str, Any]:
        """Determine differencing order."""
        trend = random.choice([True, False])
        seasonal = random.choice([True, False])

        if trend and seasonal:
            d = 1
            s = 1
            explanation_text = "one regular difference and one seasonal difference"
        elif trend:
            d = 1
            s = 0
            explanation_text = "one regular difference"
        elif seasonal:
            d = 0
            s = 1
            explanation_text = "one seasonal difference"
        else:
            d = 0
            s = 0
            explanation_text = "no differencing needed"

        choices = [
            f"d={d}, D={s}",
            f"d={1-d if d > 0 else 1}, D={s}",
            f"d={d}, D={1-s if s > 0 else 1}",
            f"d=2, D=1",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Time Series",
            "subtopic": "Differencing",
            "difficulty": 2,
            "question_text": f"Series has trend: {trend}, Seasonality: {seasonal}. "
            f"How many differences (d) and seasonal differences (D) needed?",
            "choices": choices,
            "solution": f"d={d}, D={s}",
            "explanation": f"Need {explanation_text} for stationarity."
        }

    @classmethod
    def random_walk_properties(cls) -> Dict[str, Any]:
        """Analyze random walk properties."""
        y0 = round(random.uniform(10, 50), 1)
        shocks = [round(random.gauss(0, 1), 1) for _ in range(5)]
        trajectory = [y0]
        for shock in shocks:
            trajectory.append(cls._round_to(trajectory[-1] + shock, 1))

        variance = cls._round_to(sum((y - trajectory[0]) ** 2 for y in trajectory) / len(trajectory), 2)

        choices = [
            f"Variance increases with time: {variance}",
            f"Non-stationary process",
            f"Follows AR(1) with φ=1",
            "All of the above",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Time Series",
            "subtopic": "Random Walk",
            "difficulty": 2,
            "question_text": f"Random walk starts at {y0}, then {trajectory[1:]}. "
            f"What property characterizes a random walk?",
            "choices": choices,
            "solution": "All of the above",
            "explanation": "Random walk is AR(1) with φ=1, making it non-stationary with variance increasing over time."
        }

    @classmethod
    def exponential_smoothing(cls) -> Dict[str, Any]:
        """Simple exponential smoothing forecast."""
        alpha = round(random.uniform(0.1, 0.5), 2)
        last_level = round(random.uniform(20, 100), 1)
        last_obs = round(random.uniform(20, 100), 1)

        next_level = cls._round_to(alpha * last_obs + (1 - alpha) * last_level, 2)
        forecast = next_level

        choices = [
            f"Forecast = {forecast}",
            f"Forecast = {cls._round_to(alpha * last_obs, 2)}",
            f"Forecast = {last_obs}",
            f"Forecast = {cls._round_to(forecast * 1.1, 2)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Time Series",
            "subtopic": "Exponential Smoothing",
            "difficulty": 2,
            "question_text": f"Simple exponential smoothing: α={alpha}, last observation={last_obs}, "
            f"last level={last_level}. Forecast next period.",
            "choices": choices,
            "solution": f"Forecast = {forecast}",
            "explanation": f"Level = {alpha}*{last_obs} + (1-{alpha})*{last_level} = {next_level}. "
            f"Forecast equals current level."
        }

    @classmethod
    def seasonal_decomposition(cls) -> Dict[str, Any]:
        """Decompose series into components."""
        trend_val = round(random.uniform(10, 50), 1)
        seasonal_val = round(random.uniform(-5, 5), 1)
        noise = round(random.uniform(-2, 2), 1)

        observed = cls._round_to(trend_val + seasonal_val + noise, 1)

        choices = [
            f"Trend={trend_val}, Seasonal={seasonal_val}, Noise={noise}",
            f"Trend={cls._round_to(trend_val * 1.1, 1)}, Seasonal={seasonal_val}, Noise={noise}",
            f"Observed={observed}",
            "Cannot decompose",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Time Series",
            "subtopic": "Decomposition",
            "difficulty": 2,
            "question_text": f"Observed value = {observed}. Components: Trend={trend_val}, "
            f"Seasonal={seasonal_val}, Noise={noise}. Verify decomposition.",
            "choices": choices,
            "solution": f"Trend={trend_val}, Seasonal={seasonal_val}, Noise={noise}",
            "explanation": f"Decomposition: Trend + Seasonal + Noise = {trend_val} + {seasonal_val} + {noise} = {observed}"
        }

    @classmethod
    def arima_model_selection(cls) -> Dict[str, Any]:
        """Select appropriate ARIMA model."""
        d = random.randint(0, 1)
        p = random.randint(1, 2)
        q = random.randint(0, 2)

        model_str = f"ARIMA({p},{d},{q})"

        choices = [
            model_str,
            f"ARIMA({p},{d},{q+1})" if q < 2 else f"ARIMA({p},{d},{q-1})",
            f"ARIMA({p+1},{d},{q})" if p < 2 else f"ARIMA({p-1},{d},{q})",
            "Cannot determine",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Time Series",
            "subtopic": "ARIMA Selection",
            "difficulty": 3,
            "question_text": f"ACF shows cutoff at lag 1, PACF decays, first difference is stationary. "
            f"Series requires d={d} differences. Select model with p={p}, q={q}.",
            "choices": choices,
            "solution": model_str,
            "explanation": f"{model_str} fits: d={d} differencing, AR order p={p}, MA order q={q}."
        }

    # ==================== PCA (6 methods) ====================

    @classmethod
    def eigenvalue_variance_explained(cls) -> Dict[str, Any]:
        """Calculate variance explained by PC."""
        eigenvalues = [round(random.uniform(5, 50), 1) for _ in range(4)]
        eigenvalues.sort(reverse=True)
        total_var = sum(eigenvalues)
        pc1_var = cls._round_to(eigenvalues[0] / total_var * 100, 1)

        choices = [
            f"{pc1_var}%",
            f"{cls._round_to(eigenvalues[0], 1)}%",
            f"{cls._round_to((eigenvalues[0] + eigenvalues[1]) / total_var * 100, 1)}%",
            f"{cls._round_to(100 / len(eigenvalues), 1)}%",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Principal Component Analysis",
            "subtopic": "Variance Explained",
            "difficulty": 2,
            "question_text": f"Eigenvalues: {eigenvalues}. What % of total variance does PC1 explain?",
            "choices": choices,
            "solution": f"{pc1_var}%",
            "explanation": f"PC1 variance = {eigenvalues[0]} / {total_var} * 100 = {pc1_var}%"
        }

    @classmethod
    def scree_plot_interpretation(cls) -> Dict[str, Any]:
        """Interpret scree plot for component selection."""
        variances = [round(random.uniform(20, 60), 1)]
        variances.append(round(random.uniform(10, variances[0] - 5), 1))
        variances.append(round(random.uniform(5, variances[1] - 2), 1))
        variances.append(round(random.uniform(1, variances[2] - 1), 1))

        elbow_pc = random.randint(2, 3)

        choices = [
            f"Retain {elbow_pc} components",
            f"Retain {elbow_pc + 1} components",
            f"Retain 4 components",
            f"Retain 1 component",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Principal Component Analysis",
            "subtopic": "Component Selection",
            "difficulty": 2,
            "question_text": f"Scree plot shows variance: PC1={variances[0]}%, PC2={variances[1]}%, "
            f"PC3={variances[2]}%, PC4={variances[3]}%. Elbow appears at PC{elbow_pc}. "
            f"How many components to retain?",
            "choices": choices,
            "solution": f"Retain {elbow_pc} components",
            "explanation": f"Elbow criterion suggests retaining {elbow_pc} components based on variance drop."
        }

    @classmethod
    def principal_component_loading(cls) -> Dict[str, Any]:
        """Interpret principal component loadings."""
        var1_loading = round(random.uniform(0.6, 0.95), 3)
        var2_loading = round(random.uniform(0.6, 0.95), 3)
        var3_loading = round(random.uniform(-0.95, -0.6), 3)

        choices = [
            f"PC1 is contrast between (var1,var2) and var3",
            f"PC1 weights all variables equally",
            f"PC1 is primarily driven by var1",
            "PC1 has no interpretable structure",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Principal Component Analysis",
            "subtopic": "Loadings Interpretation",
            "difficulty": 2,
            "question_text": f"PC1 loadings: var1={var1_loading}, var2={var2_loading}, var3={var3_loading}. "
            f"Interpret the component.",
            "choices": choices,
            "solution": f"PC1 is contrast between (var1,var2) and var3",
            "explanation": f"Positive loadings on var1, var2 and negative on var3 suggest PC1 contrasts these groups."
        }

    @classmethod
    def biplot_interpretation(cls) -> Dict[str, Any]:
        """Interpret PCA biplot."""
        choices = [
            "Vectors close together indicate correlated variables",
            "Angles between vectors show correlation structure",
            "Point position reflects component scores",
            "All of the above",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Principal Component Analysis",
            "subtopic": "Biplot",
            "difficulty": 2,
            "question_text": "What information does a PCA biplot convey?",
            "choices": choices,
            "solution": "All of the above",
            "explanation": "A biplot shows variable loadings (vectors), correlations (angles), and observation scores (points)."
        }

    @classmethod
    def dimensionality_reduction_choice(cls) -> Dict[str, Any]:
        """Choose reduction dimension based on requirement."""
        retain_variance = random.randint(80, 95)
        eigenvalues = sorted([round(random.uniform(1, 50), 1) for _ in range(6)], reverse=True)

        cumulative = []
        total = sum(eigenvalues)
        cum_sum = 0
        for ev in eigenvalues:
            cum_sum += ev
            cumulative.append(cls._round_to(cum_sum / total * 100, 1))

        # Find dimension that meets requirement
        selected_dim = next(i + 1 for i, cv in enumerate(cumulative) if cv >= retain_variance)

        choices = [
            f"{selected_dim} dimensions",
            f"{selected_dim + 1} dimensions",
            f"{selected_dim - 1} dimensions" if selected_dim > 1 else "6 dimensions",
            "All 6 dimensions",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Principal Component Analysis",
            "subtopic": "Dimensionality Reduction",
            "difficulty": 2,
            "question_text": f"Eigenvalues: {eigenvalues}. Need {retain_variance}% variance retained. "
            f"How many dimensions?",
            "choices": choices,
            "solution": f"{selected_dim} dimensions",
            "explanation": f"Cumulative variance: {cumulative}. Need {selected_dim} dimensions to reach {retain_variance}%."
        }

    @classmethod
    def pca_correlation_vs_covariance(cls) -> Dict[str, Any]:
        """Choose between correlation and covariance matrix."""
        choices = [
            "Use correlation if variables have different scales",
            "Use covariance if variables are in same units",
            "Use correlation for standardized data",
            "All of the above",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Principal Component Analysis",
            "subtopic": "Standardization",
            "difficulty": 2,
            "question_text": "When should PCA use correlation matrix vs covariance matrix?",
            "choices": choices,
            "solution": "All of the above",
            "explanation": "Use correlation for different scales/units; use covariance for same scale. "
            "Correlation is equivalent to PCA on standardized data."
        }

    # ==================== DECISION TREES (7 methods) ====================

    @classmethod
    def gini_impurity_calculation(cls) -> Dict[str, Any]:
        """Calculate Gini impurity."""
        class_a = random.randint(10, 80)
        class_b = random.randint(10, 80)
        total = class_a + class_b

        pa = class_a / total
        pb = class_b / total
        gini = cls._round_to(1 - (pa ** 2 + pb ** 2), 3)

        choices = [
            f"Gini = {gini}",
            f"Gini = {cls._round_to(pa * pb, 3)}",
            f"Gini = {cls._round_to(1 - pa, 3)}",
            f"Gini = {cls._round_to((pa + pb) / 2, 3)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Decision Trees",
            "subtopic": "Splitting Criteria",
            "difficulty": 2,
            "question_text": f"Node has {class_a} of class A, {class_b} of class B. "
            f"Calculate Gini impurity = 1 - (p_A² + p_B²).",
            "choices": choices,
            "solution": f"Gini = {gini}",
            "explanation": f"Gini = 1 - ({pa:.3f}² + {pb:.3f}²) = {gini}"
        }

    @classmethod
    def entropy_calculation(cls) -> Dict[str, Any]:
        """Calculate information entropy."""
        class_a = random.randint(10, 80)
        class_b = random.randint(10, 80)
        total = class_a + class_b

        pa = class_a / total
        pb = class_b / total
        entropy = cls._round_to(-(pa * math.log2(pa) + pb * math.log2(pb)) if pa > 0 and pb > 0 else 0, 3)

        choices = [
            f"Entropy = {entropy}",
            f"Entropy = {cls._round_to(-(pa * math.log(pa) + pb * math.log(pb)), 3)}",
            f"Entropy = {cls._round_to(pa * pb, 3)}",
            f"Entropy = {cls._round_to(1 - entropy, 3)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Decision Trees",
            "subtopic": "Splitting Criteria",
            "difficulty": 2,
            "question_text": f"Node has {class_a} of class A, {class_b} of class B. "
            f"Calculate entropy = -Σ(pᵢ*log₂(pᵢ)).",
            "choices": choices,
            "solution": f"Entropy = {entropy}",
            "explanation": f"Entropy = -({pa:.3f}*log₂({pa:.3f}) + {pb:.3f}*log₂({pb:.3f})) = {entropy}"
        }

    @classmethod
    def information_gain_split(cls) -> Dict[str, Any]:
        """Calculate information gain from split."""
        parent_entropy = round(random.uniform(0.5, 1), 3)
        left_entropy = round(random.uniform(0.1, parent_entropy - 0.2), 3)
        right_entropy = round(random.uniform(0.1, parent_entropy - 0.2), 3)
        left_pct = round(random.uniform(0.3, 0.7), 2)
        right_pct = 1 - left_pct

        ig = cls._round_to(parent_entropy - (left_pct * left_entropy + right_pct * right_entropy), 3)

        choices = [
            f"IG = {ig}",
            f"IG = {cls._round_to(parent_entropy - left_entropy, 3)}",
            f"IG = {cls._round_to(left_entropy + right_entropy, 3)}",
            f"IG = {cls._round_to((left_entropy + right_entropy) / 2, 3)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Decision Trees",
            "subtopic": "Splitting Criteria",
            "difficulty": 2,
            "question_text": f"Parent entropy = {parent_entropy}. Split creates left node (entropy={left_entropy}, {left_pct*100}%) "
            f"and right node (entropy={right_entropy}, {right_pct*100}%). Calculate information gain.",
            "choices": choices,
            "solution": f"IG = {ig}",
            "explanation": f"IG = {parent_entropy} - ({left_pct}*{left_entropy} + {right_pct}*{right_entropy}) = {ig}"
        }

    @classmethod
    def tree_prediction(cls) -> Dict[str, Any]:
        """Predict using decision tree rules."""
        x1_threshold = round(random.uniform(10, 50), 1)
        x2_threshold = round(random.uniform(10, 50), 1)
        x1_val = round(random.uniform(5, 60), 1)

        if x1_val > x1_threshold:
            prediction = "Class A"
            leaf = "Right"
        else:
            prediction = "Class B"
            leaf = "Left"

        choices = [prediction]
        alternatives = ["Class A", "Class B", "Cannot predict", "Class C"]
        for alt in alternatives:
            if alt != prediction:
                choices.append(alt)
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Decision Trees",
            "subtopic": "Predictions",
            "difficulty": 1,
            "question_text": f"Tree rule: if X1 > {x1_threshold} go Right (Class A), else go Left (Class B). "
            f"For new observation X1 = {x1_val}, predict class.",
            "choices": choices,
            "solution": prediction,
            "explanation": f"Since X1 = {x1_val} {'>' if x1_val > x1_threshold else '<'} {x1_threshold}, "
            f"go {leaf} and predict {prediction}."
        }

    @classmethod
    def pruning_cost_complexity(cls) -> Dict[str, Any]:
        """Select tree depth via pruning."""
        depth_options = [3, 4, 5]
        train_errors = [0.15, 0.12, 0.10]
        test_errors = [0.22, 0.20, 0.25]

        best_depth = depth_options[test_errors.index(min(test_errors))]

        choices = [
            f"Depth = {best_depth}",
            f"Depth = 5 (lowest training error)",
            f"Depth = 3 (most parsimonious)",
            "Cannot determine",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Decision Trees",
            "subtopic": "Pruning",
            "difficulty": 2,
            "question_text": f"Tree performance: Depth 3 (train={train_errors[0]}, test={test_errors[0]}), "
            f"Depth 4 (train={train_errors[1]}, test={test_errors[1]}), "
            f"Depth 5 (train={train_errors[2]}, test={test_errors[2]}). "
            f"Select optimal depth based on test error.",
            "choices": choices,
            "solution": f"Depth = {best_depth}",
            "explanation": f"Test error is minimized at depth {best_depth} ({min(test_errors)}). "
            f"Depth 5 shows overfitting (test error increases)."
        }

    @classmethod
    def overfitting_diagnosis(cls) -> Dict[str, Any]:
        """Diagnose overfitting from error metrics."""
        train_error = round(random.uniform(0.05, 0.15), 3)
        test_error = round(random.uniform(train_error + 0.05, train_error + 0.20), 3)
        gap = cls._round_to(test_error - train_error, 3)

        choices = [
            "Model is overfitting (large train-test gap)",
            "Model is underfitting (high training error)",
            "Model fits well",
            "Cannot determine from these metrics",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Decision Trees",
            "subtopic": "Model Diagnostics",
            "difficulty": 2,
            "question_text": f"Model performance: Training error = {train_error}, Test error = {test_error}. "
            f"Gap = {gap}. Diagnose the issue.",
            "choices": choices,
            "solution": "Model is overfitting (large train-test gap)",
            "explanation": f"Large gap ({gap}) between training and test error indicates overfitting. "
            f"Model memorizes training data."
        }

    @classmethod
    def random_forest_vs_single_tree(cls) -> Dict[str, Any]:
        """Compare random forest to single tree."""
        choices = [
            "Random forest reduces variance by averaging",
            "Random forest uses bootstrap and feature sampling",
            "Random forest is robust to overfitting",
            "All of the above",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Decision Trees",
            "subtopic": "Ensemble Methods",
            "difficulty": 2,
            "question_text": "What are advantages of random forests over single decision trees?",
            "choices": choices,
            "solution": "All of the above",
            "explanation": "Random forests reduce variance through averaging, use randomness in bootstrap samples "
            "and feature selection, and are more robust to overfitting than single trees."
        }

    # ==================== CLUSTERING (5 methods) ====================

    @classmethod
    def kmeans_assignment_step(cls) -> Dict[str, Any]:
        """K-means cluster assignment."""
        x = round(random.uniform(0, 10), 1)
        y = round(random.uniform(0, 10), 1)

        c1 = (round(random.uniform(0, 5), 1), round(random.uniform(0, 5), 1))
        c2 = (round(random.uniform(5, 10), 1), round(random.uniform(5, 10), 1))

        dist1 = cls._round_to(math.sqrt((x - c1[0]) ** 2 + (y - c1[1]) ** 2), 2)
        dist2 = cls._round_to(math.sqrt((x - c2[0]) ** 2 + (y - c2[1]) ** 2), 2)

        cluster = "1" if dist1 < dist2 else "2"

        choices = [
            f"Cluster {cluster}",
            f"Cluster {'2' if cluster == '1' else '1'}",
            "Cannot assign",
            "Between clusters",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Clustering",
            "subtopic": "K-Means",
            "difficulty": 2,
            "question_text": f"Point ({x}, {y}). Centers: C1={c1}, C2={c2}. "
            f"Distances: d1={dist1}, d2={dist2}. Assign to cluster.",
            "choices": choices,
            "solution": f"Cluster {cluster}",
            "explanation": f"Point is closest to C{cluster} (distance={min(dist1, dist2)})."
        }

    @classmethod
    def kmeans_centroid_update(cls) -> Dict[str, Any]:
        """K-means centroid update."""
        points_cluster = [(round(random.uniform(0, 5), 1), round(random.uniform(0, 5), 1)) for _ in range(3)]

        new_x = cls._round_to(sum(p[0] for p in points_cluster) / len(points_cluster), 1)
        new_y = cls._round_to(sum(p[1] for p in points_cluster) / len(points_cluster), 1)

        choices = [
            f"New center = ({new_x}, {new_y})",
            f"New center = ({cls._round_to(new_x * 1.1, 1)}, {new_y})",
            f"New center = ({new_x}, {points_cluster[0][1]})",
            "Center doesn't change",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Clustering",
            "subtopic": "K-Means",
            "difficulty": 2,
            "question_text": f"Cluster has points: {points_cluster}. Update centroid.",
            "choices": choices,
            "solution": f"New center = ({new_x}, {new_y})",
            "explanation": f"New center = mean of all points = ({new_x}, {new_y})"
        }

    @classmethod
    def hierarchical_linkage_distance(cls) -> Dict[str, Any]:
        """Calculate distance for hierarchical clustering."""
        d_ab = round(random.uniform(2, 10), 1)
        d_ac = round(random.uniform(2, 10), 1)

        single_link = cls._round_to(min(d_ab, d_ac), 1)
        complete_link = cls._round_to(max(d_ab, d_ac), 1)
        average_link = cls._round_to((d_ab + d_ac) / 2, 1)

        linkage_type = random.choice(["single", "complete", "average"])
        if linkage_type == "single":
            answer = f"Distance = {single_link}"
        elif linkage_type == "complete":
            answer = f"Distance = {complete_link}"
        else:
            answer = f"Distance = {average_link}"

        choices = [
            answer,
            f"Distance = {single_link}",
            f"Distance = {complete_link}",
            f"Distance = {average_link}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Clustering",
            "subtopic": "Hierarchical Clustering",
            "difficulty": 2,
            "question_text": f"Distance d(A,B)={d_ab}, d(A,C)={d_ac}. "
            f"Using {linkage_type} linkage to merge B and C clusters, calculate distance to A.",
            "choices": choices,
            "solution": answer,
            "explanation": f"With {linkage_type} linkage: distance = {answer.split('=')[1]}."
        }

    @classmethod
    def silhouette_score_calculation(cls) -> Dict[str, Any]:
        """Calculate silhouette coefficient."""
        a_i = round(random.uniform(1, 5), 2)  # avg distance to same cluster
        b_i = round(random.uniform(a_i + 1, a_i + 5), 2)  # avg distance to nearest other cluster

        s_i = cls._round_to((b_i - a_i) / max(a_i, b_i), 3)

        choices = [
            f"s_i = {s_i}",
            f"s_i = {cls._round_to((b_i - a_i) / (b_i + a_i), 3)}",
            f"s_i = {cls._round_to((a_i - b_i) / max(a_i, b_i), 3)}",
            f"s_i = {cls._round_to(a_i / b_i, 3)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Clustering",
            "subtopic": "Silhouette",
            "difficulty": 2,
            "question_text": f"Point i: avg distance within cluster a_i={a_i}, "
            f"avg distance to nearest cluster b_i={b_i}. "
            f"Calculate silhouette coefficient s_i = (b_i - a_i) / max(a_i, b_i).",
            "choices": choices,
            "solution": f"s_i = {s_i}",
            "explanation": f"s_i = ({b_i} - {a_i}) / max({a_i}, {b_i}) = {s_i}. "
            f"Range [-1, 1]: positive indicates good clustering."
        }

    @classmethod
    def optimal_k_selection(cls) -> Dict[str, Any]:
        """Choose optimal number of clusters."""
        inertias = [round(random.uniform(500 - i*60, 500 - (i-1)*60), 0) for i in range(1, 6)]
        k_values = list(range(2, 7))

        # Find elbow (largest drop)
        drops = [inertias[i] - inertias[i+1] for i in range(len(inertias)-1)]
        elbow_k = k_values[drops.index(max(drops))]

        choices = [
            f"k = {elbow_k}",
            f"k = {elbow_k + 1}",
            f"k = 6",
            f"k = 2",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Clustering",
            "subtopic": "Cluster Selection",
            "difficulty": 2,
            "question_text": f"Inertias: k=2: {inertias[0]}, k=3: {inertias[1]}, k=4: {inertias[2]}, "
            f"k=5: {inertias[3]}, k=6: {inertias[4]}. Elbow method suggests?",
            "choices": choices,
            "solution": f"k = {elbow_k}",
            "explanation": f"Largest drop in inertia occurs at k={elbow_k}, suggesting optimal clusters."
        }

    # ==================== MODEL SELECTION (5 methods) ====================

    @classmethod
    def bias_variance_tradeoff(cls) -> Dict[str, Any]:
        """Understand bias-variance tradeoff."""
        choices = [
            "Simple models have high bias, low variance",
            "Complex models have low bias, high variance",
            "Low total error balances bias and variance",
            "All of the above",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Model Selection",
            "subtopic": "Bias-Variance",
            "difficulty": 2,
            "question_text": "What is the bias-variance tradeoff?",
            "choices": choices,
            "solution": "All of the above",
            "explanation": "Simple models underfit (high bias, low variance). Complex models overfit (low bias, high variance). "
            "Optimal model balances both."
        }

    @classmethod
    def cross_validation_estimate(cls) -> Dict[str, Any]:
        """Estimate model performance via cross-validation."""
        fold_errors = [round(random.uniform(0.15, 0.35), 3) for _ in range(5)]
        cv_error = cls._round_to(sum(fold_errors) / len(fold_errors), 3)
        std_error = cls._round_to(math.sqrt(sum((e - cv_error) ** 2 for e in fold_errors) / (len(fold_errors) - 1)), 3)

        choices = [
            f"CV error = {cv_error} ± {std_error}",
            f"CV error = {fold_errors[0]}",
            f"CV error = {cls._round_to(max(fold_errors), 3)}",
            f"CV error = {cls._round_to(sum(fold_errors), 3)}",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Model Selection",
            "subtopic": "Cross-Validation",
            "difficulty": 2,
            "question_text": f"5-fold CV errors: {fold_errors}. "
            f"Calculate mean CV error and standard error.",
            "choices": choices,
            "solution": f"CV error = {cv_error} ± {std_error}",
            "explanation": f"Mean error = {cv_error}. SE = sqrt(sum((e-mean)²)/(k-1)) = {std_error}."
        }

    @classmethod
    def aic_bic_comparison(cls) -> Dict[str, Any]:
        """Compare models using AIC vs BIC."""
        aic_model1 = round(random.uniform(100, 200), 1)
        aic_model2 = round(random.uniform(100, 200), 1)
        n = random.randint(50, 200)
        k = random.randint(2, 10)

        bic1 = cls._round_to(aic_model1 - 2 * k + k * math.log(n), 1)
        bic2 = cls._round_to(aic_model2 - 2 * k + k * math.log(n), 1)

        choices = [
            f"AIC prefers simpler, BIC stronger penalty",
            f"BIC prefers simpler, AIC stronger penalty",
            "AIC and BIC always select same model",
            "Cannot compare AIC and BIC",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Model Selection",
            "subtopic": "Information Criteria",
            "difficulty": 2,
            "question_text": f"When choosing between AIC and BIC with n={n}, which has stronger penalty for model complexity?",
            "choices": choices,
            "solution": f"BIC prefers simpler, AIC stronger penalty",
            "explanation": f"BIC = AIC + (k*log(n) - 2k). For n>{exp(2)}, BIC penalizes complexity more."
        }

    @classmethod
    def train_test_split_evaluation(cls) -> Dict[str, Any]:
        """Evaluate train-test split performance."""
        train_error = round(random.uniform(0.10, 0.20), 3)
        test_error = round(random.uniform(train_error - 0.05, train_error + 0.15), 3)

        if abs(train_error - test_error) < 0.05:
            assessment = "Good generalization"
        elif test_error > train_error + 0.10:
            assessment = "Overfitting likely"
        else:
            assessment = "Possible underfitting"

        choices = [assessment]
        alternatives = ["Good generalization", "Overfitting likely", "Possible underfitting", "Cannot assess"]
        for alt in alternatives:
            if alt != assessment:
                choices.append(alt)
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Model Selection",
            "subtopic": "Train-Test Evaluation",
            "difficulty": 2,
            "question_text": f"Train error = {train_error}, Test error = {test_error}. Assess model.",
            "choices": choices,
            "solution": assessment,
            "explanation": f"Gap = {test_error - train_error:.3f}. {assessment}."
        }

    @classmethod
    def regularization_effect(cls) -> Dict[str, Any]:
        """Effect of regularization parameter."""
        choices = [
            "Larger λ increases bias, decreases variance",
            "Smaller λ increases variance, decreases bias",
            "λ controls bias-variance tradeoff",
            "All of the above",
        ]
        random.shuffle(choices)

        return {
            "id": cls._generate_id(),
            "exam": "SRM",
            "topic": "Model Selection",
            "subtopic": "Regularization",
            "difficulty": 2,
            "question_text": "How does regularization parameter λ affect model fitting?",
            "choices": choices,
            "solution": "All of the above",
            "explanation": "Larger λ shrinks coefficients (more bias, less variance). Smaller λ allows larger coefficients "
            "(less bias, more variance). λ balances the tradeoff."
        }

    # ==================== UTILITY METHODS ====================

    @classmethod
    def get_all_methods(cls) -> List[str]:
        """Get list of all question generation methods."""
        methods = [
            # Linear Regression
            'simple_linear_regression_coefficient', 'interpret_slope', 'multiple_regression_prediction',
            'r_squared_interpretation', 'adjusted_r_squared', 'f_test_significance',
            'residual_analysis', 'heteroscedasticity_detection', 'multicollinearity_vif',
            'partial_f_test', 'confidence_interval_prediction', 'leverage_influence',
            'dummy_variable_regression',
            # Generalized Linear Models
            'poisson_regression_predict', 'logistic_regression_odds_ratio',
            'logistic_regression_probability', 'log_link_interpretation', 'deviance_comparison',
            'aic_model_selection', 'offset_variable_usage', 'dispersion_parameter',
            'glm_link_function_identify', 'glm_residual_analysis',
            # Time Series
            'ar1_identify_parameters', 'ma1_identify_parameters', 'arma_forecast',
            'stationarity_check', 'acf_pacf_model_identification', 'differencing_for_stationarity',
            'random_walk_properties', 'exponential_smoothing', 'seasonal_decomposition',
            'arima_model_selection',
            # PCA
            'eigenvalue_variance_explained', 'scree_plot_interpretation',
            'principal_component_loading', 'biplot_interpretation',
            'dimensionality_reduction_choice', 'pca_correlation_vs_covariance',
            # Decision Trees
            'gini_impurity_calculation', 'entropy_calculation', 'information_gain_split',
            'tree_prediction', 'pruning_cost_complexity', 'overfitting_diagnosis',
            'random_forest_vs_single_tree',
            # Clustering
            'kmeans_assignment_step', 'kmeans_centroid_update',
            'hierarchical_linkage_distance', 'silhouette_score_calculation',
            'optimal_k_selection',
            # Model Selection
            'bias_variance_tradeoff', 'cross_validation_estimate',
            'aic_bic_comparison', 'train_test_split_evaluation',
            'regularization_effect',
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
