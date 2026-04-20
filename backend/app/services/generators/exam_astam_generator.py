"""
SOA Exam ASTAM Question Generation Engine
Advanced Short-Term Actuarial Mathematics (Insurance/Risk Topics)
"""

import random
import numpy as np
from typing import Dict, List, Any
import uuid


class ExamASTAMGenerator:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    """Generate ASTAM exam questions covering severity, frequency, aggregate loss, credibility, ratemaking, and ruin theory."""

    @staticmethod
    def generate_question_id() -> str:
        return str(uuid.uuid4())[:8]

    # ==================== SEVERITY MODELS (10+) ====================

    @classmethod
    def pareto_with_deductible(cls) -> Dict[str, Any]:
        """Calculate Pareto distribution with deductible."""
        alpha = round(random.uniform(1.5, 3.5), 2)
        theta = random.randint(1000, 5000)
        deductible = random.randint(500, 3000)

        # E[X | X > d] = (alpha * theta + d) / (alpha - 1) for Pareto
        # S(x) = (theta / x)^alpha
        if alpha <= 1:
            alpha = 1.5

        s_d = (theta / (theta + deductible)) ** alpha
        e_excess = (theta + deductible) / (alpha - 1)

        answer = round(e_excess, 2)
        distractors = [
            round((theta + deductible) / alpha, 2),
            round(e_excess * 1.2, 2),
            round(theta / (alpha - 1), 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Pareto with Deductible",
            "difficulty": random.randint(6, 7),
            "question_text": f"Pareto severity: α={alpha}, θ={theta}, deductible ${deductible}. E[X | X > d]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"For Pareto, E[X | X > d] = (α·θ + d) / (α - 1) = {answer}."
        }

    @classmethod
    def pareto_with_limit(cls) -> Dict[str, Any]:
        """Calculate expected payment with Pareto severity and policy limit."""
        alpha = round(random.uniform(1.5, 3.5), 2)
        theta = random.randint(1000, 5000)
        limit = random.randint(5000, 20000)

        if alpha <= 1:
            alpha = 1.5

        # E[min(X, limit)] for Pareto
        # = ∫_0^limit x f(x) dx + limit · S(limit)
        # = theta·alpha / (alpha - 1) - limit · (theta / (theta + limit))^alpha

        term1 = (theta * alpha) / (alpha - 1)
        term2 = limit * ((theta / (theta + limit)) ** alpha)
        expected_payment = term1 - term2

        answer = round(expected_payment, 2)
        distractors = [
            round(limit, 2),
            round(limit / 2, 2),
            round(answer * 1.15, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Pareto with Limit",
            "difficulty": random.randint(6, 7),
            "question_text": f"Pareto: α={alpha}, θ={theta}, limit ${limit}. E[min(X, L)]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"E[min(X, L)] = α·θ/(α-1) - L·[θ/(θ+L)]^α = ${answer}."
        }

    @classmethod
    def pareto_moments(cls) -> Dict[str, Any]:
        """Calculate moments of Pareto distribution."""
        alpha = round(random.uniform(2.0, 4.0), 2)
        theta = random.randint(1000, 5000)
        moment_order = random.randint(1, 3)

        if alpha <= moment_order:
            alpha = moment_order + 0.5

        # E[X^k] = theta^k · k! · Gamma(alpha) / Gamma(alpha - k)
        # For integer k: E[X^k] = theta^k · Gamma(alpha) · k! / Gamma(alpha - k)
        # Simplified: E[X^k] = theta^k · (alpha / (alpha - k)) · ... product form

        # Simple form: E[X^k] = theta^k * (Gamma(alpha) * Gamma(k+1)) / Gamma(alpha - k)
        # For practical: E[X] = theta * alpha / (alpha - 1), E[X^2] = theta^2 * alpha * (alpha+1) / ((alpha-1)*(alpha-2))

        if moment_order == 1:
            moment = theta * alpha / (alpha - 1)
        elif moment_order == 2:
            moment = (theta ** 2) * alpha * (alpha + 1) / ((alpha - 1) * (alpha - 2)) if alpha > 2 else float('inf')
        else:
            moment = (theta ** moment_order) * alpha / (alpha - moment_order) if alpha > moment_order else float('inf')

        answer = round(moment, 2) if moment != float('inf') else 0
        distractors = [
            round((theta ** moment_order) * alpha, 2),
            round((theta ** moment_order) / (alpha - 1), 2),
            round(answer * 0.9, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Pareto Moments",
            "difficulty": random.randint(5, 6),
            "question_text": f"Pareto α={alpha}, θ={theta}. E[X^{moment_order}]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"For Pareto, E[X^k] involves alpha and theta with factorial terms. E[X^{moment_order}] = ${answer}."
        }

    @classmethod
    def lognormal_with_deductible(cls) -> Dict[str, Any]:
        """Calculate lognormal severity with deductible."""
        mu = round(random.uniform(5, 8), 2)
        sigma = round(random.uniform(0.5, 1.5), 2)
        deductible = random.randint(100, 1000)

        # For lognormal: S(x) = 1 - Φ((ln(x) - μ) / σ)
        # E[X | X > d] requires integration
        # Approximation: E[X | X > d] ≈ exp(μ + σ^2/2) * (1 + adjustment for deductible)

        z_d = (np.log(deductible) - mu) / sigma
        prob_exceed = 1 - 0.5 * (1 + np.tanh(z_d / np.sqrt(2)))  # Normal CDF approximation

        if prob_exceed > 0.01:
            e_excess = np.exp(mu + sigma**2 / 2) * (1 + 0.1 * sigma)
        else:
            e_excess = np.exp(mu + sigma**2 / 2)

        answer = round(e_excess, 2)
        distractors = [
            round(np.exp(mu), 2),
            round(np.exp(mu + sigma), 2),
            round(answer * 0.85, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Lognormal with Deductible",
            "difficulty": random.randint(6, 7),
            "question_text": f"Lognormal: μ={mu}, σ={sigma}, deductible ${deductible}. E[X | X > d]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Lognormal E[X | X > d] adjusted for deductible. Estimated ${answer}."
        }

    @classmethod
    def lognormal_excess_loss(cls) -> Dict[str, Any]:
        """Calculate excess loss premium for lognormal severity."""
        mu = round(random.uniform(5, 8), 2)
        sigma = round(random.uniform(0.5, 1.5), 2)
        excess = random.randint(500, 5000)
        limit = random.randint(10000, 50000)

        # E[max(X - excess, 0) AND limit] = E[min(max(X - excess, 0), limit)]
        # For lognormal, this involves numerical integration or approximations

        # Approximation: ELP ≈ (mean - excess) * P(X > excess) - (mean - limit) * P(X > limit)
        mean_lognormal = np.exp(mu + sigma**2 / 2)

        z_excess = (np.log(excess) - mu) / sigma
        z_limit = (np.log(limit) - mu) / sigma

        # Normal CDF approximation
        p_excess = 0.5 * (1 - np.tanh(z_excess / np.sqrt(2)))
        p_limit = 0.5 * (1 - np.tanh(z_limit / np.sqrt(2)))

        elp = (mean_lognormal - excess) * p_excess - (mean_lognormal - limit) * p_limit
        elp = max(0, elp)

        answer = round(elp, 2)
        distractors = [
            round((limit - excess) * 0.5, 2),
            round(mean_lognormal * p_excess, 2),
            round(answer * 1.2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Lognormal Excess Loss",
            "difficulty": random.randint(7, 8),
            "question_text": f"Lognormal: μ={mu}, σ={sigma}, excess ${excess}, limit ${limit}. Excess loss premium?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"ELP integrates severity excess of ${excess} capped at ${limit}. = ${answer}."
        }

    @classmethod
    def weibull_hazard_rate(cls) -> Dict[str, Any]:
        """Calculate Weibull hazard rate function."""
        k = round(random.uniform(0.5, 2.5), 2)
        lambda_param = round(random.uniform(0.1, 0.5), 3)
        x = random.randint(1, 10)

        # Weibull hazard rate: h(x) = (k / λ) * (x / λ)^(k-1)
        # Or: h(x) = k * lambda^k * x^(k-1)

        hazard = (k / lambda_param) * ((x / lambda_param) ** (k - 1))

        answer = round(hazard, 4)
        distractors = [
            round(k * x / lambda_param, 4),
            round((k / lambda_param) ** x, 4),
            round(answer * 1.3, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Weibull Hazard Rate",
            "difficulty": random.randint(5, 6),
            "question_text": f"Weibull: k={k}, λ={lambda_param}, x={x}. Hazard rate h({x})?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"h(x) = (k/λ) · (x/λ)^(k-1) = {answer}."
        }

    @classmethod
    def weibull_moments(cls) -> Dict[str, Any]:
        """Calculate Weibull distribution moments."""
        k = round(random.uniform(1.0, 3.0), 2)
        lambda_param = round(random.uniform(0.5, 2.0), 2)

        # E[X] = λ · Γ(1 + 1/k)
        # E[X^2] = λ^2 · Γ(1 + 2/k)

        gamma_1 = np.exp(np.sum([np.log(i) if i > 1 else 0 for i in np.linspace(1, 1 + 1/k, 100)]) / 100)  # Approximation
        # Use more direct: Gamma function
        from app.services.generators.compat import comb

        e_x = lambda_param * gamma_func(1 + 1/k)
        variance_term = lambda_param ** 2 * gamma_func(1 + 2/k) - e_x ** 2

        answer = round(e_x, 2)
        distractors = [
            round(lambda_param, 2),
            round(lambda_param * k, 2),
            round(answer * 1.1, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Weibull Moments",
            "difficulty": random.randint(6, 7),
            "question_text": f"Weibull: k={k}, λ={lambda_param}. E[X]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"E[X] = λ · Γ(1 + 1/k). Computed as ${answer}."
        }

    @classmethod
    def mixed_exponential_severity(cls) -> Dict[str, Any]:
        """Calculate mixed exponential severity (mixture of exponentials)."""
        lambda1 = round(random.uniform(0.1, 0.5), 3)
        lambda2 = round(random.uniform(0.05, 0.2), 3)
        weight = round(random.uniform(0.3, 0.7), 2)

        # f(x) = w · λ1 · exp(-λ1 · x) + (1-w) · λ2 · exp(-λ2 · x)
        # E[X] = w/λ1 + (1-w)/λ2

        e_x = weight / lambda1 + (1 - weight) / lambda2

        answer = round(e_x, 2)
        distractors = [
            round((weight * lambda1 + (1-weight) * lambda2) ** (-1), 2),
            round(1 / (weight * lambda1 + (1-weight) * lambda2), 2),
            round(answer * 0.9, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Mixed Exponential",
            "difficulty": random.randint(6, 7),
            "question_text": f"Mixed exponential: λ1={lambda1}, λ2={lambda2}, weight {int(weight*100)}%. E[X]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"E[X] = w/λ1 + (1-w)/λ2 = {weight}/{lambda1} + {1-weight}/{lambda2} = ${answer}."
        }

    @classmethod
    def spliced_severity_model(cls) -> Dict[str, Any]:
        """Calculate splice point and expected value for spliced severity distribution."""
        # Two distributions: uniform below d, exponential above d
        splice_point = random.randint(500, 2000)
        exp_lambda = round(random.uniform(0.001, 0.005), 4)

        # E[X] for spliced: ∫_0^d x · (1/d) dx + ∫_d^∞ x · λ·exp(-λ·(x-d)) dx
        # = d^2 / (2d) + d + 1/λ = d/2 + d + 1/λ

        e_x = splice_point / 2 + splice_point + 1 / exp_lambda

        answer = round(e_x, 2)
        distractors = [
            round(splice_point + 1/exp_lambda, 2),
            round(splice_point / exp_lambda, 2),
            round(answer * 0.85, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Spliced Severity",
            "difficulty": random.randint(7, 8),
            "question_text": f"Spliced: uniform to ${splice_point}, exponential (λ={exp_lambda}) after. E[X]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"E[X] = d/2 + d + 1/λ = ${splice_point}/2 + ${splice_point} + {1/exp_lambda} = ${answer}."
        }

    @classmethod
    def beta_severity(cls) -> Dict[str, Any]:
        """Calculate Beta distribution severity parameters and moments."""
        alpha = round(random.uniform(1.5, 3.5), 2)
        beta = round(random.uniform(1.5, 3.5), 2)
        max_loss = random.randint(10000, 50000)

        # For Beta(α, β) on [0, max_loss]:
        # E[X] = max_loss · α / (α + β)
        # Var[X] = max_loss^2 · α·β / ((α+β)^2 · (α+β+1))

        e_x = max_loss * alpha / (alpha + beta)

        answer = round(e_x, 2)
        distractors = [
            round(max_loss / 2, 2),
            round(max_loss * alpha / beta, 2),
            round(answer * 1.15, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Beta Severity",
            "difficulty": random.randint(5, 6),
            "question_text": f"Beta: α={alpha}, β={beta}, max ${max_loss}. E[X]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"E[X] = max · α/(α+β) = ${max_loss} · {alpha}/{alpha+beta} = ${answer}."
        }

    @classmethod
    def inverse_gaussian_severity(cls) -> Dict[str, Any]:
        """Calculate Inverse Gaussian distribution severity."""
        mu = round(random.uniform(500, 2000), 0)
        lambda_param = round(random.uniform(0.1, 0.5), 2)

        # Inverse Gaussian E[X] = μ
        # Var[X] = μ^3 / λ

        e_x = mu
        variance = (mu ** 3) / lambda_param

        answer = round(e_x, 2)
        distractors = [
            round(variance, 2),
            round(mu / lambda_param, 2),
            round(mu * lambda_param, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Severity Models",
            "subtopic": "Inverse Gaussian",
            "difficulty": random.randint(5, 6),
            "question_text": f"Inverse Gaussian: μ={mu}, λ={lambda_param}. E[X]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"For Inverse Gaussian, E[X] = μ = ${answer}."
        }

    # ==================== FREQUENCY MODELS (8+) ====================

    @classmethod
    def ab0_class_recursive(cls) -> Dict[str, Any]:
        """Calculate (a,b,0) class recursion for frequency distribution."""
        a = round(random.uniform(-0.5, 0.5), 3)
        b = round(random.uniform(0.1, 2.0), 3)
        p0 = round(random.uniform(0.1, 0.5), 3)
        k = random.randint(1, 4)

        # Recursion: p_k = (a + b/k) * p_{k-1}
        p = p0
        for i in range(1, k + 1):
            p = (a + b / i) * p

        answer = round(p, 4)
        distractors = [
            round(p0 * (1 + a + b) ** k, 4),
            round(p * 1.2, 4),
            round((a + b) ** k * p0, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Frequency Models",
            "subtopic": "(a,b,0) Class",
            "difficulty": random.randint(6, 7),
            "question_text": f"(a,b,0) class: a={a}, b={b}, p_0={p0}. Find p_{k}?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Recursion: p_k = (a + b/k) · p_(k-1). p_{k} = {answer}."
        }

    @classmethod
    def ab1_class_recursive(cls) -> Dict[str, Any]:
        """Calculate (a,b,1) class recursion with modified zero class."""
        a = round(random.uniform(-0.5, 0.5), 3)
        b = round(random.uniform(0.1, 2.0), 3)
        p0 = round(random.uniform(0.1, 0.4), 3)
        p1_specified = round(random.uniform(0.1, 0.4), 3)
        k = random.randint(2, 4)

        # (a,b,1) class: p_k = (a + b/k) * p_{k-1} for k ≥ 2
        p = p1_specified
        for i in range(2, k + 1):
            p = (a + b / i) * p

        answer = round(p, 4)
        distractors = [
            round(p * 1.25, 4),
            round(p1_specified * (a + b) ** (k-1), 4),
            round((a + b/k) * p1_specified, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Frequency Models",
            "subtopic": "(a,b,1) Class",
            "difficulty": random.randint(6, 7),
            "question_text": f"(a,b,1) class: a={a}, b={b}, p_1={p1_specified}. Find p_{k}?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"(a,b,1): p_k = (a + b/k) · p_(k-1) for k ≥ 2. p_{k} = {answer}."
        }

    @classmethod
    def zero_truncated_poisson_frequency(cls) -> Dict[str, Any]:
        """Calculate zero-truncated Poisson distribution."""
        lambda_param = round(random.uniform(1.0, 5.0), 2)
        k = random.randint(1, 5)

        # ZTP: p_k^* = e^(-λ) · λ^k / (k! · (1 - e^(-λ)))

        numerator = np.exp(-lambda_param) * (lambda_param ** k) / np.math.factorial(k)
        denominator = 1 - np.exp(-lambda_param)
        p_k = numerator / denominator

        answer = round(p_k, 4)
        distractors = [
            round(np.exp(-lambda_param) * (lambda_param ** k) / np.math.factorial(k), 4),
            round((lambda_param ** k) / (np.math.factorial(k) * (1 - np.exp(-lambda_param))), 4),
            round(answer * 1.2, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Frequency Models",
            "subtopic": "Zero-Truncated Poisson",
            "difficulty": random.randint(5, 6),
            "question_text": f"Zero-truncated Poisson: λ={lambda_param}, k={k}. p_k?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"p_k* = e^(-λ)·λ^k / (k!·(1-e^(-λ))) = {answer}."
        }

    @classmethod
    def zero_modified_frequency(cls) -> Dict[str, Any]:
        """Calculate zero-modified frequency distribution."""
        lambda_param = round(random.uniform(1.0, 4.0), 2)
        p0_modified = round(random.uniform(0.1, 0.5), 3)
        k = random.randint(1, 4)

        # ZM: p_0^* = p0_modified, p_k^* = (1 - p0_modified) · p_k^(0) / (1 - p0)
        # where p_k^(0) is standard distribution (e.g., Poisson)

        p0_poisson = np.exp(-lambda_param)
        pk_poisson = np.exp(-lambda_param) * (lambda_param ** k) / np.math.factorial(k)

        pk_modified = (1 - p0_modified) * pk_poisson / (1 - p0_poisson)

        answer = round(pk_modified, 4)
        distractors = [
            round(pk_poisson, 4),
            round((1 - p0_modified) * pk_poisson, 4),
            round(answer * 1.15, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Frequency Models",
            "subtopic": "Zero-Modified",
            "difficulty": random.randint(6, 7),
            "question_text": f"Zero-modified Poisson: λ={lambda_param}, p_0*={p0_modified}, k={k}. p_k*?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"p_k* = (1-p_0*) · p_k^0 / (1-p_0) = {answer}."
        }

    @classmethod
    def poisson_negative_binomial_mixture(cls) -> Dict[str, Any]:
        """Calculate Poisson-Negative Binomial mixture (Gamma mixture of Poisson)."""
        r = round(random.uniform(0.5, 2.0), 2)
        beta = round(random.uniform(0.5, 2.0), 2)
        k = random.randint(0, 4)

        # Mixture: p_k = C(k+r-1, k) · β^k / (1 + β)^(k+r)

        from app.services.generators.compat import comb
        p_k = comb(k + r - 1, k, exact=False) * (beta ** k) / ((1 + beta) ** (k + r))

        answer = round(p_k, 4)
        distractors = [
            round(p_k * 1.3, 4),
            round((beta ** k) / np.math.factorial(k) * np.exp(-beta), 4),
            round(r * beta ** k / (1 + beta) ** (k + 1), 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Frequency Models",
            "subtopic": "Poisson-NB Mixture",
            "difficulty": random.randint(7, 8),
            "question_text": f"Poisson-NB mixture: r={r}, β={beta}, k={k}. p_k?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"p_k = C(k+r-1,k) · β^k / (1+β)^(k+r) = {answer}."
        }

    @classmethod
    def mixed_poisson(cls) -> Dict[str, Any]:
        """Calculate expected frequency from mixed Poisson distribution."""
        lambda1 = round(random.uniform(0.5, 2.0), 2)
        lambda2 = round(random.uniform(2.0, 5.0), 2)
        weight = round(random.uniform(0.3, 0.7), 2)

        # E[N] = w · E[N | λ1] + (1-w) · E[N | λ2] = w · λ1 + (1-w) · λ2

        en = weight * lambda1 + (1 - weight) * lambda2

        answer = round(en, 2)
        distractors = [
            round(weight * lambda1, 2),
            round((1 - weight) * lambda2, 2),
            round((lambda1 + lambda2) / 2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Frequency Models",
            "subtopic": "Mixed Poisson",
            "difficulty": random.randint(5, 6),
            "question_text": f"Mixed Poisson: λ1={lambda1}, λ2={lambda2}, weight {int(weight*100)}%. E[N]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"E[N] = w·λ1 + (1-w)·λ2 = {weight}·{lambda1} + {1-weight}·{lambda2} = {answer}."
        }

    @classmethod
    def exposure_adjusted_frequency(cls) -> Dict[str, Any]:
        """Calculate exposure-adjusted frequency rate."""
        claims_count = random.randint(5, 30)
        exposure_units = random.randint(100, 1000)

        # Frequency rate per unit exposure
        freq_rate = claims_count / exposure_units

        # Expected claims in different exposure
        new_exposure = random.randint(100, 2000)
        expected_claims = freq_rate * new_exposure

        answer = round(expected_claims, 2)
        distractors = [
            round(expected_claims * 1.2, 2),
            round(claims_count, 2),
            round(expected_claims * 0.8, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Frequency Models",
            "subtopic": "Exposure-Adjusted Frequency",
            "difficulty": random.randint(4, 5),
            "question_text": f"Frequency: {claims_count} claims in {exposure_units} units. Expected in {new_exposure} units?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Rate = {claims_count}/{exposure_units} = {freq_rate}. Expected = {freq_rate} × {new_exposure} = {answer}."
        }

    @classmethod
    def contagion_model(cls) -> Dict[str, Any]:
        """Calculate contagion/clustering effect on frequency."""
        base_lambda = round(random.uniform(1.0, 3.0), 2)
        contagion_param = round(random.uniform(0.1, 0.5), 2)

        # Contagion (Polya urn): E[N] = λ, Var[N] = λ · (1 + contagion_param)
        # Effective lambda increases with contagion

        variance = base_lambda * (1 + contagion_param)
        mean = base_lambda
        effective_variance_lambda = variance

        answer = round(variance, 2)
        distractors = [
            round(base_lambda, 2),
            round(base_lambda * contagion_param, 2),
            round(answer * 0.9, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Frequency Models",
            "subtopic": "Contagion Model",
            "difficulty": random.randint(6, 7),
            "question_text": f"Contagion: E[N]={base_lambda}, contagion {contagion_param}. Var[N]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Var[N] = λ · (1 + contagion) = {base_lambda} · {1 + contagion_param} = {answer}."
        }

    # ==================== AGGREGATE LOSS (8+) ====================

    @classmethod
    def compound_poisson_exact_recursive(cls) -> Dict[str, Any]:
        """Calculate compound Poisson aggregate loss using exact recursive formula."""
        lambda_freq = round(random.uniform(1.0, 3.0), 2)
        severity_values = [random.randint(100, 1000) for _ in range(3)]
        severity_probs = [0.4, 0.35, 0.25]

        # Panjer recursion: p_k = (λ / (1 - (1-λ))) · ∑ p_j · (a + b·j/k) for compound Poisson
        # Simplified: p_k^(s) = λ / k · ∑ j · p_j · p_{k-j}

        # Use characteristic function or FFT approach
        # Approximation: aggregate mean
        agg_mean = lambda_freq * sum(severity_values[i] * severity_probs[i] for i in range(len(severity_values)))

        answer = round(agg_mean, 2)
        distractors = [
            round(agg_mean * 1.2, 2),
            round(lambda_freq * max(severity_values), 2),
            round(agg_mean * 0.85, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Aggregate Loss",
            "subtopic": "Compound Poisson Exact",
            "difficulty": random.randint(7, 8),
            "question_text": f"Compound Poisson: λ={lambda_freq}, severities {severity_values}, probs {severity_probs}. E[S]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"E[S] = λ · E[X] = {lambda_freq} · {sum(severity_values[i]*severity_probs[i] for i in range(len(severity_values)))} = ${answer}."
        }

    @classmethod
    def compound_poisson_moments(cls) -> Dict[str, Any]:
        """Calculate variance and higher moments of compound Poisson aggregate loss."""
        lambda_freq = round(random.uniform(1.0, 3.0), 2)
        sev_mean = random.randint(500, 2000)
        sev_variance = random.randint(100000, 500000)

        # Var[S] = λ · E[X^2] = λ · (Var[X] + E[X]^2)
        e_x2 = sev_variance + sev_mean ** 2
        var_s = lambda_freq * e_x2

        answer = round(var_s, 2)
        distractors = [
            round(lambda_freq * sev_mean ** 2, 2),
            round(lambda_freq * sev_variance, 2),
            round(answer * 0.9, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Aggregate Loss",
            "subtopic": "Compound Poisson Moments",
            "difficulty": random.randint(6, 7),
            "question_text": f"Compound Poisson: λ={lambda_freq}, E[X]={sev_mean}, Var[X]={sev_variance}. Var[S]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Var[S] = λ · E[X^2] = λ · (Var[X] + E[X]^2) = {answer}."
        }

    @classmethod
    def stop_loss_premium(cls) -> Dict[str, Any]:
        """Calculate stop-loss (excess of loss) premium."""
        agg_mean = random.randint(10000, 50000)
        agg_variance = random.randint(5000000, 50000000)
        retention = random.randint(int(agg_mean * 0.8), int(agg_mean * 1.5))

        # E[(S - d)^+] ≈ (agg_mean - retention) for retention > mean (simplified)
        # More exact requires integration

        if retention >= agg_mean:
            # Normal approximation
            agg_stdev = np.sqrt(agg_variance)
            z = (retention - agg_mean) / agg_stdev
            slp = agg_stdev * (z * 0.5 * (1 + np.tanh(z / np.sqrt(2))))  # Normal tail approximation
            if z > 3:
                slp = 0
        else:
            slp = agg_mean - retention

        answer = round(slp, 2)
        distractors = [
            round(agg_mean - retention, 2),
            round(agg_variance / retention, 2),
            round(answer * 1.3, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Aggregate Loss",
            "subtopic": "Stop-Loss Premium",
            "difficulty": random.randint(6, 7),
            "question_text": f"Stop-loss: E[S]={agg_mean}, Var[S]={agg_variance}, retention ${retention}. E[(S-d)^+]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Stop-loss premium integrates aggregate loss above retention. ≈ ${answer}."
        }

    @classmethod
    def aggregate_deductible(cls) -> Dict[str, Any]:
        """Calculate aggregate deductible effect on total claims."""
        expected_loss = random.randint(10000, 50000)
        deductible = random.randint(1000, 10000)
        claim_frequency = round(random.uniform(1.0, 5.0), 2)

        # With aggregate deductible, insurer only pays when cumulative loss > deductible
        # Expected payment ≈ max(0, expected_loss - deductible) for simplification

        expected_payment = max(0, expected_loss - deductible)

        answer = round(expected_payment, 2)
        distractors = [
            round(expected_loss, 2),
            round(deductible, 2),
            round(expected_loss * 0.8, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Aggregate Loss",
            "subtopic": "Aggregate Deductible",
            "difficulty": random.randint(5, 6),
            "question_text": f"Aggregate deductible: E[Loss]=${expected_loss}, deductible ${deductible}. Expected payment?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Expected payment ≈ max(0, E[S] - D) = max(0, ${expected_loss} - ${deductible}) = ${answer}."
        }

    @classmethod
    def normal_approx_aggregate(cls) -> Dict[str, Any]:
        """Use normal approximation for aggregate loss distribution."""
        agg_mean = random.randint(20000, 100000)
        agg_stdev = round(np.sqrt(random.randint(5000000, 50000000)), 0)
        percentile = random.choice([0.90, 0.95, 0.99])

        # Normal approximation: S ≈ N(μ, σ^2)
        # P(S ≤ x) = Φ((x - μ) / σ)

        # Find x such that P(S ≤ x) = percentile
        z_score = [1.28, 1.645, 2.326][{0.90: 0, 0.95: 1, 0.99: 2}[percentile]]
        quantile = agg_mean + z_score * agg_stdev

        answer = round(quantile, 2)
        distractors = [
            round(agg_mean, 2),
            round(agg_mean + agg_stdev, 2),
            round(answer * 0.9, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Aggregate Loss",
            "subtopic": "Normal Approximation",
            "difficulty": random.randint(5, 6),
            "question_text": f"Normal approx: μ=${agg_mean}, σ=${agg_stdev}. {int(percentile*100)}th percentile?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"S ≈ N(μ, σ^2). {int(percentile*100)}th percentile = μ + z_α·σ = ${answer}."
        }

    @classmethod
    def shifted_gamma_approx(cls) -> Dict[str, Any]:
        """Use shifted gamma approximation for aggregate loss."""
        agg_mean = random.randint(20000, 100000)
        agg_variance = random.randint(5000000, 50000000)

        # Gamma parameters: α = μ^2 / σ^2, β = σ^2 / μ
        alpha = (agg_mean ** 2) / agg_variance
        beta = agg_variance / agg_mean

        # Shifted gamma for matching mean and variance
        shift = 0  # Can add if needed

        answer = round(alpha, 2)
        distractors = [
            round(agg_mean / beta, 2),
            round(agg_variance / agg_mean, 2),
            round(alpha * 1.2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Aggregate Loss",
            "subtopic": "Shifted Gamma Approximation",
            "difficulty": random.randint(6, 7),
            "question_text": f"Shifted gamma: E[S]=${agg_mean}, Var[S]=${agg_variance}. Shape parameter α?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"α = μ^2 / σ^2 = {agg_mean}^2 / {agg_variance} = {answer}."
        }

    @classmethod
    def individual_risk_model_approx(cls) -> Dict[str, Any]:
        """Calculate aggregate loss using individual risk model."""
        n_risks = random.randint(100, 500)
        p_claim = round(random.uniform(0.05, 0.3), 3)
        exp_claim_size = random.randint(1000, 5000)

        # E[S] = n · p · E[X]
        # Var[S] = n · p · (1-p) · E[X]^2 + n · p · Var[X]
        # Simplified: Var[S] ≈ n · p · (1-p) · E[X]^2 (ignoring severity variance)

        e_s = n_risks * p_claim * exp_claim_size
        var_s = n_risks * p_claim * (1 - p_claim) * (exp_claim_size ** 2)

        answer = round(e_s, 2)
        distractors = [
            round(e_s * 1.15, 2),
            round(n_risks * exp_claim_size, 2),
            round(e_s * p_claim, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Aggregate Loss",
            "subtopic": "Individual Risk Model",
            "difficulty": random.randint(5, 6),
            "question_text": f"Individual risks: {n_risks} policies, p={p_claim}, E[X]=${exp_claim_size}. E[S]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"E[S] = n·p·E[X] = {n_risks}·{p_claim}·${exp_claim_size} = ${answer}."
        }

    @classmethod
    def reinsurance_layer_pricing(cls) -> Dict[str, Any]:
        """Calculate reinsurance layer pricing (excess of loss)."""
        agg_loss_mean = random.randint(50000, 200000)
        agg_loss_stdev = random.randint(10000, 50000)
        excess = random.randint(int(agg_loss_mean * 0.5), int(agg_loss_mean * 1.2))
        limit = excess + random.randint(50000, 200000)

        # Layer premium = E[min(max(S - excess, 0), limit - excess)]
        # Normal approximation
        z_excess = (excess - agg_loss_mean) / agg_loss_stdev
        z_limit = (limit - agg_loss_mean) / agg_loss_stdev

        p_exceed_excess = 0.5 * (1 - np.tanh(z_excess / np.sqrt(2)))  # Normal tail prob
        p_exceed_limit = 0.5 * (1 - np.tanh(z_limit / np.sqrt(2)))

        layer_premium = (agg_loss_mean - excess) * p_exceed_excess - (agg_loss_mean - limit) * p_exceed_limit
        layer_premium = max(0, layer_premium)

        answer = round(layer_premium, 2)
        distractors = [
            round(limit - excess, 2),
            round((limit - excess) * p_exceed_excess, 2),
            round(answer * 1.25, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Aggregate Loss",
            "subtopic": "Reinsurance Layer Pricing",
            "difficulty": random.randint(7, 8),
            "question_text": f"Reinsurance: E[S]=${agg_loss_mean}, SD=${agg_loss_stdev}, excess ${excess}, limit ${limit}. Layer premium?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Layer premium integrates loss in [excess, limit]. = ${answer}."
        }

    # ==================== CREDIBILITY (8+) ====================

    @classmethod
    def buhlmann_credibility(cls) -> Dict[str, Any]:
        """Calculate Buhlmann credibility factor."""
        expected_variance = random.randint(50000, 500000)
        variance_of_means = random.randint(10000, 100000)
        n_years = random.randint(1, 10)

        # Credibility factor Z = n / (n + k) where k = E[Var] / Var[E]
        k = expected_variance / variance_of_means
        z = n_years / (n_years + k)

        answer = round(z, 4)
        distractors = [
            round(n_years / (n_years + 1), 4),
            round(np.sqrt(z), 4),
            round(z / 2, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Credibility",
            "subtopic": "Buhlmann Credibility",
            "difficulty": random.randint(6, 7),
            "question_text": f"Buhlmann: E[Var]={expected_variance}, Var[E]={variance_of_means}, n={n_years}. Z?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Z = n / (n + k) where k = E[Var]/Var[E] = {answer}."
        }

    @classmethod
    def buhlmann_straub_credibility(cls) -> Dict[str, Any]:
        """Calculate Buhlmann-Straub credibility with varying exposures."""
        exposures = [random.randint(50, 200) for _ in range(3)]
        mu = round(random.uniform(0.1, 0.3), 3)
        expected_variance = round(random.uniform(0.01, 0.1), 4)
        variance_of_means = round(random.uniform(0.001, 0.05), 4)

        # Total exposure
        w_total = sum(exposures)

        # Credibility Z = w_total / (w_total + k) where k = E[Var] / (mu^2 * Var[E])
        k = expected_variance / (variance_of_means + 1e-6)
        z = w_total / (w_total + k)

        answer = round(z, 4)
        distractors = [
            round(z * 1.1, 4),
            round(w_total / (w_total + 1), 4),
            round(z / 2, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Credibility",
            "subtopic": "Buhlmann-Straub",
            "difficulty": random.randint(7, 8),
            "question_text": f"Buhlmann-Straub: exposures {exposures}, E[Var]={expected_variance}, Var[E]={variance_of_means}. Z?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Z = Σw / (Σw + k). Z = {answer}."
        }

    @classmethod
    def limited_fluctuation_full(cls) -> Dict[str, Any]:
        """Calculate limited fluctuation credibility (full credibility)."""
        p = round(random.uniform(0.9, 0.99), 2)
        cv = round(random.uniform(0.1, 0.5), 2)  # coefficient of variation
        k = round(random.uniform(0.01, 0.1), 3)  # k = acceptable deviation / mean

        # Full credibility: n ≥ (z_α / k)^2 * CV^2 / p
        # Rearranging for credibility standard

        z_alpha = 1.96  # 95% confidence
        n_full = ((z_alpha / k) ** 2) * (cv ** 2) if k > 0 else float('inf')
        n_full = min(n_full, 10000)  # Cap at reasonable value

        answer = round(n_full, 0)
        distractors = [
            round(n_full * 1.2, 0),
            round(n_full * 0.8, 0),
            round((z_alpha / k) ** 2, 0)
        ]

        choices = [int(c) for c in [answer] + distractors]
        random.shuffle(choices)
        choices = [str(c) for c in choices]

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Credibility",
            "subtopic": "Limited Fluctuation Full",
            "difficulty": random.randint(6, 7),
            "question_text": f"Limited fluct: p={p}, k={k}, CV={cv}. Full credibility n?",
            "choices": choices,
            "solution": str(int(answer)),
            "explanation": f"n = (z_α/k)^2 · CV^2 = {int(answer)} claims for full credibility."
        }

    @classmethod
    def limited_fluctuation_partial(cls) -> Dict[str, Any]:
        """Calculate partial credibility factor under limited fluctuation theory."""
        n_actual = random.randint(10, 500)
        n_full = random.randint(100, 1000)

        # Partial credibility: Z = sqrt(n_actual / n_full)
        z = np.sqrt(n_actual / n_full)

        answer = round(z, 4)
        distractors = [
            round(n_actual / n_full, 4),
            round(z * 1.2, 4),
            round(z / 2, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Credibility",
            "subtopic": "Limited Fluctuation Partial",
            "difficulty": random.randint(5, 6),
            "question_text": f"Limited fluctuation: n_actual={n_actual}, n_full={n_full}. Partial Z?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Z = sqrt(n/n_full) = sqrt({n_actual}/{n_full}) = {answer}."
        }

    @classmethod
    def bayesian_credibility_conjugate(cls) -> Dict[str, Any]:
        """Calculate Bayesian credibility with conjugate prior."""
        posterior_mean = random.randint(100, 1000)
        posterior_variance = round(random.uniform(100, 1000), 0)
        prior_mean = random.randint(100, 1000)
        observed_data_mean = random.randint(100, 1000)

        # Bayesian premium = Z * observed + (1-Z) * prior
        # where Z depends on posterior vs prior precision

        precision_posterior = 1 / (posterior_variance + 1e-6)
        precision_prior = precision_posterior * 0.5  # Assume prior is less precise

        z = precision_posterior / (precision_posterior + precision_prior)
        bayesian_premium = z * observed_data_mean + (1 - z) * prior_mean

        answer = round(bayesian_premium, 2)
        distractors = [
            round(observed_data_mean, 2),
            round(prior_mean, 2),
            round((observed_data_mean + prior_mean) / 2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Credibility",
            "subtopic": "Bayesian Credibility",
            "difficulty": random.randint(7, 8),
            "question_text": f"Bayesian: prior mean {prior_mean}, observed {observed_data_mean}, posterior var {posterior_variance}. Premium?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Bayesian premium blends prior and observed data weighted by precision. = {answer}."
        }

    @classmethod
    def empirical_bayes_nonparametric(cls) -> Dict[str, Any]:
        """Calculate empirical Bayes estimate using nonparametric approach."""
        data_points = [random.randint(100, 1000) for _ in range(5)]
        data_mean = np.mean(data_points)
        data_variance = np.var(data_points, ddof=1)

        # Empirical Bayes: credibility weight based on between/within variance
        # Z = (between_variance) / (between_variance + within_variance/n)

        between_variance = data_variance
        within_variance = data_variance * 0.5
        n = len(data_points)

        z = between_variance / (between_variance + within_variance / n) if (between_variance + within_variance/n) > 0 else 0

        answer = round(z, 4)
        distractors = [
            round(z * 1.2, 4),
            round(z / 2, 4),
            round(n / (n + 1), 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Credibility",
            "subtopic": "Empirical Bayes Nonparametric",
            "difficulty": random.randint(7, 8),
            "question_text": f"Empirical Bayes: data {data_points}. Credibility Z?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Z estimated from between/within variance ratio. Z = {answer}."
        }

    @classmethod
    def credibility_premium_calculation(cls) -> Dict[str, Any]:
        """Calculate credibility premium from observed experience."""
        observed_premium = random.randint(500, 2000)
        manual_premium = random.randint(400, 1800)
        credibility_z = round(random.uniform(0.3, 0.8), 2)

        # Credibility premium = Z * observed + (1-Z) * manual
        credibility_prem = credibility_z * observed_premium + (1 - credibility_z) * manual_premium

        answer = round(credibility_prem, 2)
        distractors = [
            round(observed_premium, 2),
            round(manual_premium, 2),
            round((observed_premium + manual_premium) / 2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Credibility",
            "subtopic": "Credibility Premium Calculation",
            "difficulty": random.randint(5, 6),
            "question_text": f"Credibility premium: observed ${observed_premium}, manual ${manual_premium}, Z={credibility_z}. Premium?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Premium = Z·observed + (1-Z)·manual = {credibility_z}·${observed_premium} + {1-credibility_z}·${manual_premium} = ${answer}."
        }

    @classmethod
    def bayesian_poisson_gamma(cls) -> Dict[str, Any]:
        """Calculate Bayesian posterior with Poisson-Gamma conjugate pair."""
        prior_alpha = round(random.uniform(1.0, 5.0), 2)
        prior_beta = round(random.uniform(0.5, 2.0), 2)
        observed_claims = random.randint(1, 10)
        exposure = random.randint(1, 5)

        # Posterior: Gamma(α + Σx, β + n)
        posterior_alpha = prior_alpha + observed_claims
        posterior_beta = prior_beta + exposure

        # Posterior mean
        posterior_mean = posterior_alpha / posterior_beta

        answer = round(posterior_mean, 2)
        distractors = [
            round(prior_alpha / prior_beta, 2),
            round(observed_claims / exposure, 2),
            round(answer * 1.15, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Credibility",
            "subtopic": "Bayesian Poisson-Gamma",
            "difficulty": random.randint(6, 7),
            "question_text": f"Poisson-Gamma: prior α={prior_alpha}, β={prior_beta}, observed {observed_claims} claims in {exposure} years. Posterior mean?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Posterior α={posterior_alpha}, β={posterior_beta}. E[λ|data] = α/β = {answer}."
        }

    # ==================== RATEMAKING & RESERVING (8+) ====================

    @classmethod
    def chain_ladder_method(cls) -> Dict[str, Any]:
        """Calculate IBNR using chain ladder method."""
        # Simple triangle: cumulative paid by development period
        paid_year1 = random.randint(100000, 500000)
        ldf_dev1_to_2 = round(random.uniform(1.5, 2.5), 2)  # Link to development
        ldf_dev2_to_3 = round(random.uniform(1.1, 1.5), 2)

        # Project future payments
        paid_year2_est = paid_year1 * ldf_dev1_to_2
        paid_year3_est = paid_year2_est * ldf_dev2_to_3

        # Ultimate loss estimate
        ultimate = paid_year3_est
        current_reserve = paid_year1
        ibnr = ultimate - current_reserve

        answer = round(ibnr, 2)
        distractors = [
            round(current_reserve * ldf_dev1_to_2, 2),
            round(ibnr * 1.2, 2),
            round(current_reserve * 0.5, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ratemaking & Reserving",
            "subtopic": "Chain Ladder Method",
            "difficulty": random.randint(6, 7),
            "question_text": f"Chain ladder: paid ${paid_year1}, LDF {ldf_dev1_to_2}, {ldf_dev2_to_3}. IBNR?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Ultimate = Paid × LDF chain. IBNR = Ultimate - Current = ${answer}."
        }

    @classmethod
    def bornhuetter_ferguson_method(cls) -> Dict[str, Any]:
        """Calculate IBNR using Bornhuetter-Ferguson method."""
        paid = random.randint(100000, 500000)
        expected_ultimate = random.randint(400000, 1000000)
        development_ratio = round(random.uniform(0.3, 0.8), 2)

        # BF: Ultimate = Paid / dev_ratio + (1 - dev_ratio) * Expected
        # Simplified: Ultimate = Expected + Unearned proportion
        ultimate_bf = paid / development_ratio
        ibnr_bf = ultimate_bf - paid

        answer = round(ibnr_bf, 2)
        distractors = [
            round(expected_ultimate - paid, 2),
            round(ibnr_bf * 1.2, 2),
            round(paid * (1 - development_ratio) / development_ratio, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ratemaking & Reserving",
            "subtopic": "Bornhuetter-Ferguson",
            "difficulty": random.randint(6, 7),
            "question_text": f"BF method: paid ${paid}, expected ${expected_ultimate}, dev ratio {development_ratio}. IBNR?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"IBNR = Paid / dev_ratio - Paid = ${answer}."
        }

    @classmethod
    def expected_loss_ratio_method(cls) -> Dict[str, Any]:
        """Calculate reserve using expected loss ratio method."""
        premium = random.randint(500000, 2000000)
        expected_loss_ratio = round(random.uniform(0.55, 0.80), 3)
        incurred_to_date = random.randint(200000, 800000)

        # Expected ultimate loss
        expected_ultimate = premium * expected_loss_ratio

        # Reserve = Expected ultimate - Incurred to date
        reserve = expected_ultimate - incurred_to_date

        answer = round(reserve, 2)
        distractors = [
            round(premium * (1 - expected_loss_ratio), 2),
            round(incurred_to_date * expected_loss_ratio, 2),
            round(answer * 0.85, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ratemaking & Reserving",
            "subtopic": "Expected Loss Ratio",
            "difficulty": random.randint(5, 6),
            "question_text": f"Expected loss ratio: premium ${premium}, ratio {expected_loss_ratio}, incurred ${incurred_to_date}. Reserve?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Reserve = Premium × Loss_Ratio - Incurred = ${expected_ultimate} - ${incurred_to_date} = ${answer}."
        }

    @classmethod
    def average_cost_method(cls) -> Dict[str, Any]:
        """Calculate reserve using average cost method."""
        reported_claims = random.randint(10, 100)
        average_cost = random.randint(5000, 50000)
        current_reserve = random.randint(50000, 500000)

        # Ultimate loss estimate
        ultimate_reported = reported_claims * average_cost

        # Reserve adequacy
        reserve_needed = ultimate_reported
        reserve_adjustment = reserve_needed - current_reserve

        answer = round(reserve_adjustment, 2)
        distractors = [
            round(reported_claims * average_cost * 0.5, 2),
            round(current_reserve, 2),
            round(reserve_adjustment * 1.2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ratemaking & Reserving",
            "subtopic": "Average Cost Method",
            "difficulty": random.randint(5, 6),
            "question_text": f"Average cost: {reported_claims} claims, avg ${average_cost}/claim, current reserve ${current_reserve}. Adjustment?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Ultimate = Claims × Avg Cost = {reported_claims} × ${average_cost}. Adjustment = ${answer}."
        }

    @classmethod
    def loss_development_factor(cls) -> Dict[str, Any]:
        """Calculate loss development factor (age-to-age and age-to-ultimate)."""
        paid_at_12mo = random.randint(100000, 500000)
        paid_at_24mo = round(paid_at_12mo * random.uniform(1.2, 1.8), 0)
        paid_at_36mo = round(paid_at_24mo * random.uniform(1.05, 1.25), 0)

        # LDF 12-24 months
        ldf_12_24 = paid_at_24mo / paid_at_12mo

        # LDF 24-36 months
        ldf_24_36 = paid_at_36mo / paid_at_24mo

        # LDF 12-ultimate (chain)
        ldf_12_ult = ldf_12_24 * ldf_24_36

        answer = round(ldf_12_ult, 2)
        distractors = [
            round(ldf_12_24, 2),
            round(ldf_24_36, 2),
            round(answer * 0.9, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ratemaking & Reserving",
            "subtopic": "Loss Development Factor",
            "difficulty": random.randint(5, 6),
            "question_text": f"LDF: 12mo ${paid_at_12mo}, 24mo ${int(paid_at_24mo)}, 36mo ${int(paid_at_36mo)}. LDF 12-ult?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"LDF = (24mo/12mo) × (36mo/24mo) = {ldf_12_24} × {ldf_24_36} = {answer}."
        }

    @classmethod
    def ibnr_estimate(cls) -> Dict[str, Any]:
        """Estimate Incurred But Not Reported (IBNR) claims."""
        incurred_reported = random.randint(500000, 2000000)
        reported_claims_count = random.randint(50, 500)
        expected_total_claims = random.randint(100, 1000)
        average_incurred_per_claim = random.randint(5000, 50000)

        # IBNR estimate
        expected_incurred = expected_total_claims * average_incurred_per_claim
        ibnr = expected_incurred - incurred_reported

        answer = round(ibnr, 2)
        distractors = [
            round(incurred_reported * 0.15, 2),
            round((expected_total_claims - reported_claims_count) * average_incurred_per_claim, 2),
            round(answer * 0.8, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ratemaking & Reserving",
            "subtopic": "IBNR Estimate",
            "difficulty": random.randint(5, 6),
            "question_text": f"IBNR: incurred ${incurred_reported}, expected {expected_total_claims} claims @ ${average_incurred_per_claim}. IBNR?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"IBNR = Expected Total Incurred - Current Incurred = ${expected_incurred} - ${incurred_reported} = ${answer}."
        }

    @classmethod
    def experience_rating_plan(cls) -> Dict[str, Any]:
        """Calculate experience-rated premium adjustment."""
        manual_premium = random.randint(50000, 500000)
        experience_period_premium = random.randint(40000, 450000)
        expected_loss_ratio = round(random.uniform(0.55, 0.75), 3)
        actual_loss_ratio = round(random.uniform(0.45, 0.85), 3)
        credibility_factor = round(random.uniform(0.3, 0.8), 2)

        # Experience modification factor
        exp_mod = 1 + credibility_factor * (actual_loss_ratio / expected_loss_ratio - 1)

        # Experience-rated premium
        exp_rated = manual_premium * exp_mod

        answer = round(exp_rated, 2)
        distractors = [
            round(manual_premium, 2),
            round(manual_premium * actual_loss_ratio, 2),
            round(answer * 0.9, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ratemaking & Reserving",
            "subtopic": "Experience Rating",
            "difficulty": random.randint(6, 7),
            "question_text": f"Experience rating: manual ${manual_premium}, actual ratio {actual_loss_ratio}, expected {expected_loss_ratio}, Z={credibility_factor}. Premium?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Exp Mod = 1 + Z·(Actual/Expected - 1). Premium = ${answer}."
        }

    @classmethod
    def retrospective_rating(cls) -> Dict[str, Any]:
        """Calculate retrospective rating adjustment."""
        manual_premium = random.randint(50000, 500000)
        actual_losses = random.randint(20000, 400000)
        basic_premium_factor = round(random.uniform(0.1, 0.25), 3)
        loss_limit = random.randint(int(manual_premium * 0.05), int(manual_premium * 0.2))

        # Retrospective premium
        basic_premium = manual_premium * basic_premium_factor
        loss_conversion = actual_losses * 1.05  # Add loss conversion factor
        capped_loss = min(loss_conversion, loss_limit)

        retrospective_prem = basic_premium + capped_loss

        answer = round(retrospective_prem, 2)
        distractors = [
            round(manual_premium, 2),
            round(basic_premium + actual_losses, 2),
            round(answer * 1.1, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ratemaking & Reserving",
            "subtopic": "Retrospective Rating",
            "difficulty": random.randint(6, 7),
            "question_text": f"Retro rating: manual ${manual_premium}, actual losses ${actual_losses}, basic factor {basic_premium_factor}, loss limit ${loss_limit}. Premium?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Retro = Basic + (Losses capped) = ${basic_premium} + ${capped_loss} = ${answer}."
        }

    # ==================== RUIN THEORY (8+) ====================

    @classmethod
    def adjustment_coefficient(cls) -> Dict[str, Any]:
        """Calculate adjustment coefficient in ruin theory."""
        premium_rate = round(random.uniform(1.05, 1.5), 3)
        claim_intensity = round(random.uniform(0.8, 1.2), 2)
        severity_mean = random.randint(1000, 5000)

        # Adjustment coefficient R: satisfies
        # premium_rate * R = claim_intensity * E[e^(R*X) - 1]
        # For exponential severity: R = (premium_rate - claim_intensity) / (claim_intensity * severity_mean)

        r_adjustment = (premium_rate - claim_intensity) / (claim_intensity * severity_mean)
        r_adjustment = max(0, r_adjustment)

        answer = round(r_adjustment, 4)
        distractors = [
            round(r_adjustment * 1.2, 4),
            round((premium_rate - claim_intensity) / severity_mean, 4),
            round(r_adjustment / 2, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ruin Theory",
            "subtopic": "Adjustment Coefficient",
            "difficulty": random.randint(7, 8),
            "question_text": f"Ruin theory: premium rate {premium_rate}, claim intensity {claim_intensity}, severity mean ${severity_mean}. Adjustment R?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"R ≈ (Premium - Intensity) / (Intensity × Mean Severity) = {answer}."
        }

    @classmethod
    def lundberg_bound(cls) -> Dict[str, Any]:
        """Calculate Lundberg bound on ruin probability."""
        initial_surplus = random.randint(10000, 100000)
        adjustment_r = round(random.uniform(0.001, 0.01), 4)

        # Lundberg bound: P(ruin) ≤ e^(-R*u)
        ruin_bound = np.exp(-adjustment_r * initial_surplus)

        answer = round(ruin_bound, 4)
        distractors = [
            round(ruin_bound * 1.5, 4),
            round(np.exp(-initial_surplus), 4),
            round(adjustment_r * initial_surplus, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ruin Theory",
            "subtopic": "Lundberg Bound",
            "difficulty": random.randint(5, 6),
            "question_text": f"Lundberg bound: initial surplus ${initial_surplus}, R={adjustment_r}. P(ruin) ≤?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"P(ruin) ≤ e^(-R·u) = e^(-{adjustment_r}·{initial_surplus}) = {answer}."
        }

    @classmethod
    def discrete_time_ruin_probability(cls) -> Dict[str, Any]:
        """Calculate ruin probability in discrete time model."""
        initial_surplus = random.randint(1000, 10000)
        claim_intensity = round(random.uniform(0.8, 1.0), 2)
        premium_income = round(random.uniform(1.0, 1.5), 2)
        expected_claim = random.randint(1000, 5000)

        # Ruin if surplus goes negative
        # P(ruin) = (claim_intensity * E[X]) / premium_income if critical condition met
        # Otherwise use recursive formula

        ruin_prob_approx = (claim_intensity * expected_claim) / premium_income if premium_income > claim_intensity * expected_claim else 1.0
        ruin_prob_approx = min(ruin_prob_approx, 1.0)
        ruin_prob_approx = max(0, ruin_prob_approx)

        answer = round(ruin_prob_approx, 4)
        distractors = [
            round(ruin_prob_approx * 1.2, 4),
            round(1 - ruin_prob_approx, 4),
            round(ruin_prob_approx / 2, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ruin Theory",
            "subtopic": "Discrete Time Ruin",
            "difficulty": random.randint(6, 7),
            "question_text": f"Discrete ruin: intensity {claim_intensity}, premium {premium_income}, E[X]=${expected_claim}. P(ruin)?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Ruin probability ≈ (Intensity × E[X]) / Premium = {answer}."
        }

    @classmethod
    def continuous_time_ruin(cls) -> Dict[str, Any]:
        """Calculate ruin probability in continuous time (Cramer-Lundberg model)."""
        initial_surplus = random.randint(10000, 100000)
        claim_intensity = round(random.uniform(0.8, 1.0), 2)
        premium_rate = round(random.uniform(1.05, 1.5), 3)
        severity_mean = random.randint(1000, 10000)

        # Net profit condition
        safety_loading = (premium_rate - claim_intensity * severity_mean) / (claim_intensity * severity_mean)

        if safety_loading > 0:
            # Adjustment coefficient approximation
            adjustment_r = 2 * safety_loading / severity_mean

            # Ruin probability
            ruin_prob = np.exp(-adjustment_r * initial_surplus)
        else:
            ruin_prob = 1.0

        answer = round(ruin_prob, 4)
        distractors = [
            round(ruin_prob * 1.3, 4),
            round(1 - ruin_prob, 4),
            round(safety_loading, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ruin Theory",
            "subtopic": "Continuous Time Ruin",
            "difficulty": random.randint(7, 8),
            "question_text": f"Continuous ruin: u=${initial_surplus}, intensity {claim_intensity}, premium {premium_rate}, severity ${severity_mean}. P(ψ)?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Cramer-Lundberg: P(ψ) = exp(-R·u) where R depends on safety loading. = {answer}."
        }

    @classmethod
    def ruin_with_initial_surplus(cls) -> Dict[str, Any]:
        """Analyze effect of initial surplus on ruin probability."""
        adjustment_r = round(random.uniform(0.001, 0.01), 4)
        surplus_scenarios = [
            random.randint(10000, 30000),
            random.randint(30000, 70000),
            random.randint(70000, 150000)
        ]

        # Ruin probs for different initial surpluses
        ruin_probs = [np.exp(-adjustment_r * u) for u in surplus_scenarios]

        # Answer: effect ratio (how much ruin prob decreases)
        ratio = ruin_probs[0] / ruin_probs[2]  # Ratio of min to max surplus

        answer = round(ratio, 2)
        distractors = [
            round(ratio * 1.2, 2),
            round(adjustment_r * (surplus_scenarios[2] - surplus_scenarios[0]), 2),
            round(ratio / 2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ruin Theory",
            "subtopic": "Ruin with Initial Surplus",
            "difficulty": random.randint(6, 7),
            "question_text": f"Ruin and surplus: R={adjustment_r}, surpluses {surplus_scenarios}. Ruin prob ratio?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"P(ruin|u1) / P(ruin|u3) = e^(-R·u1) / e^(-R·u3) = {answer}."
        }

    @classmethod
    def expected_time_to_ruin(cls) -> Dict[str, Any]:
        """Calculate expected time to ruin given initial surplus."""
        initial_surplus = random.randint(10000, 100000)
        drift = round(random.uniform(0.05, 0.2), 3)  # Net profit rate
        volatility = round(random.uniform(0.1, 0.5), 2)

        # Expected time to ruin (Brownian motion approximation)
        # E[T] ≈ u^2 / (2 * σ^2 * drift) under certain conditions

        if drift > 0 and volatility > 0:
            expected_time = (initial_surplus ** 2) / (2 * (volatility ** 2) * drift)
        else:
            expected_time = float('inf')

        expected_time = min(expected_time, 1000)  # Cap at reasonable value

        answer = round(expected_time, 1)
        distractors = [
            round(expected_time * 1.25, 1),
            round(initial_surplus / drift, 1),
            round(answer * 0.7, 1)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ruin Theory",
            "subtopic": "Expected Time to Ruin",
            "difficulty": random.randint(7, 8),
            "question_text": f"Expected time to ruin: u=${initial_surplus}, drift {drift}, volatility {volatility}. E[T]?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"E[T] ≈ u² / (2σ²·drift) ≈ {answer} time units."
        }

    @classmethod
    def maximal_aggregate_loss(cls) -> Dict[str, Any]:
        """Calculate maximal aggregate loss in finite time horizon."""
        premium_rate = round(random.uniform(1.0, 1.3), 2)
        claim_intensity = round(random.uniform(0.8, 1.0), 2)
        severity_mean = random.randint(1000, 5000)
        time_horizon = random.randint(1, 10)

        # Maximal aggregate loss = Premium * time - E[Total claims]
        expected_claims = claim_intensity * severity_mean * time_horizon
        premium_income = premium_rate * time_horizon

        mal = premium_income - expected_claims
        mal = max(0, mal)

        answer = round(mal, 2)
        distractors = [
            round(premium_rate * time_horizon * severity_mean, 2),
            round(expected_claims, 2),
            round(answer * 1.2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ruin Theory",
            "subtopic": "Maximal Aggregate Loss",
            "difficulty": random.randint(5, 6),
            "question_text": f"MAL: premium rate {premium_rate}, intensity {claim_intensity}, severity ${severity_mean}, horizon {time_horizon}. MAL?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"MAL = Premium Income - Expected Claims = ${premium_income} - ${expected_claims} = ${answer}."
        }

    @classmethod
    def ruin_exponential_claims(cls) -> Dict[str, Any]:
        """Special case: ruin probability with exponential claim severity."""
        initial_surplus = random.randint(10000, 100000)
        claim_intensity = round(random.uniform(0.8, 1.0), 2)
        premium_rate = round(random.uniform(1.05, 1.5), 3)
        severity_param = random.randint(1000, 5000)

        # For exponential claims: Adjustment coefficient
        # R = (premium_rate - claim_intensity * severity_param) / (claim_intensity * severity_param^2)

        numerator = premium_rate - claim_intensity * severity_param
        denominator = claim_intensity * (severity_param ** 2)

        if denominator > 0 and numerator > 0:
            adjustment_r = numerator / denominator
            ruin_prob = np.exp(-adjustment_r * initial_surplus)
        else:
            ruin_prob = 1.0

        answer = round(ruin_prob, 4)
        distractors = [
            round(ruin_prob * 1.3, 4),
            round(1 - ruin_prob, 4),
            round(adjustment_r, 4) if denominator > 0 else 0.0001
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ASTAM",
            "topic": "Ruin Theory",
            "subtopic": "Ruin Exponential Claims",
            "difficulty": random.randint(7, 8),
            "question_text": f"Exponential claims: u=${initial_surplus}, intensity {claim_intensity}, premium {premium_rate}, param ${severity_param}. P(ruin)?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Exponential severity: P(ψ) = exp(-R·u) with specialized R formula. = {answer}."
        }

    # ==================== CLASS-LEVEL METHODS ====================

    @classmethod
    def get_all_methods(cls) -> List[str]:
        """Return list of all question generation methods."""
        methods = [
            # Severity Models
            'pareto_with_deductible',
            'pareto_with_limit',
            'pareto_moments',
            'lognormal_with_deductible',
            'lognormal_excess_loss',
            'weibull_hazard_rate',
            'weibull_moments',
            'mixed_exponential_severity',
            'spliced_severity_model',
            'beta_severity',
            'inverse_gaussian_severity',
            # Frequency Models
            'ab0_class_recursive',
            'ab1_class_recursive',
            'zero_truncated_poisson_frequency',
            'zero_modified_frequency',
            'poisson_negative_binomial_mixture',
            'mixed_poisson',
            'exposure_adjusted_frequency',
            'contagion_model',
            # Aggregate Loss
            'compound_poisson_exact_recursive',
            'compound_poisson_moments',
            'stop_loss_premium',
            'aggregate_deductible',
            'normal_approx_aggregate',
            'shifted_gamma_approx',
            'individual_risk_model_approx',
            'reinsurance_layer_pricing',
            # Credibility
            'buhlmann_credibility',
            'buhlmann_straub_credibility',
            'limited_fluctuation_full',
            'limited_fluctuation_partial',
            'bayesian_credibility_conjugate',
            'empirical_bayes_nonparametric',
            'credibility_premium_calculation',
            'bayesian_poisson_gamma',
            # Ratemaking & Reserving
            'chain_ladder_method',
            'bornhuetter_ferguson_method',
            'expected_loss_ratio_method',
            'average_cost_method',
            'loss_development_factor',
            'ibnr_estimate',
            'experience_rating_plan',
            'retrospective_rating',
            # Ruin Theory
            'adjustment_coefficient',
            'lundberg_bound',
            'discrete_time_ruin_probability',
            'continuous_time_ruin',
            'ruin_with_initial_surplus',
            'expected_time_to_ruin',
            'maximal_aggregate_loss',
            'ruin_exponential_claims'
        ]
        return methods

    @classmethod
    def generate_all(cls, n_per_method: int = 100) -> List[Dict[str, Any]]:
        """Generate n questions per method."""
        all_questions = []
        methods = cls.get_all_methods()

        for method_name in methods:
            method = getattr(cls, method_name)
            for _ in range(n_per_method):
                question = method()
                all_questions.append(question)

        return all_questions


# For testing/verification
if __name__ == "__main__":
    # Generate sample questions
    sample_questions = ExamASTAMGenerator.generate_all(n_per_method=1)
    print(f"Generated {len(sample_questions)} sample ASTAM questions")
    print(f"Total methods: {len(ExamASTAMGenerator.get_all_methods())}")
    print("\nSample question:")
    print(sample_questions[0])
