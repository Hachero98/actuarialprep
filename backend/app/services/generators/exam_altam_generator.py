"""
SOA Exam ALTAM Question Generation Engine
Advanced Life Contingency Topics & Actuarial Mathematics
"""

import random
import numpy as np
from typing import Dict, List, Any
import uuid


class ExamALTAMGenerator:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    """Generate ALTAM exam questions with realistic financial scenarios."""

    @staticmethod
    def generate_question_id() -> str:
        return str(uuid.uuid4())[:8]

    # ==================== MULTI-STATE MODELS (10+) ====================

    @classmethod
    def two_state_alive_dead_transition(cls) -> Dict[str, Any]:
        """Two-state Markov model: Alive -> Dead transitions with force of mortality."""
        mu_x = round(random.uniform(0.001, 0.05), 4)
        age = random.randint(30, 75)
        t = random.randint(1, 5)

        # Exact: tpx = exp(-integral mu_x+s ds) = exp(-mu_x * t)
        survival_prob = np.exp(-mu_x * t)

        # Distractors
        distractors = [
            round(1 - mu_x * t, 4),
            round((1 - mu_x) ** t, 4),
            round(np.exp(-mu_x / t), 4)
        ]

        choices = [round(survival_prob, 4)] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multi-State Models",
            "subtopic": "Two-State Alive-Dead",
            "difficulty": random.randint(5, 6),
            "question_text": f"Age {age} individual with constant force of mortality μ = {mu_x}. Calculate {t}p{age}.",
            "choices": [str(c) for c in choices],
            "solution": str(round(survival_prob, 4)),
            "explanation": f"Under constant force of mortality, tpx = exp(-μt) = exp(-{mu_x}*{t}) = {round(survival_prob, 4)}. This is the standard survival probability in a two-state model."
        }

    @classmethod
    def three_state_healthy_sick_dead(cls) -> Dict[str, Any]:
        """Three-state model: Healthy -> Sick -> Dead transitions."""
        mu_hs = round(random.uniform(0.002, 0.01), 4)  # healthy to sick
        mu_hd = round(random.uniform(0.001, 0.008), 4)  # healthy to dead
        mu_sd = round(random.uniform(0.005, 0.03), 4)   # sick to dead
        t = 1

        # Probability of being in Healthy state: P(H->H)
        prob_healthy = np.exp(-(mu_hs + mu_hd) * t)
        prob_sick = (mu_hs / (mu_sd - mu_hs + mu_hd)) * (np.exp(-(mu_hs + mu_hd)*t) - np.exp(-mu_sd*t))
        prob_dead = 1 - prob_healthy - prob_sick

        # Focus on staying healthy
        answer = round(prob_healthy, 4)
        distractors = [
            round(prob_sick, 4),
            round(1 - mu_hs, 4),
            round(np.exp(-mu_sd), 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multi-State Models",
            "subtopic": "Three-State Healthy-Sick-Dead",
            "difficulty": random.randint(6, 7),
            "question_text": f"Three-state model: μ(H→S)={mu_hs}, μ(H→D)={mu_hd}, μ(S→D)={mu_sd}. Probability of remaining Healthy in 1 year?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"P(H→H) = exp(-(μ_HS + μ_HD)·t) = exp(-{mu_hs + mu_hd}) = {answer}. Transitions to other states cannot occur directly from remaining healthy."
        }

    @classmethod
    def kolmogorov_forward_equation(cls) -> Dict[str, Any]:
        """Solve Kolmogorov forward differential equations for multi-state model."""
        mu_01 = round(random.uniform(0.005, 0.015), 4)
        mu_10 = round(random.uniform(0.001, 0.008), 4)
        mu_02 = round(random.uniform(0.003, 0.012), 4)
        t = 1

        # For simple 3-state model, at time t the probability densities:
        lambda_01 = -(mu_01 + mu_02)
        lambda_1 = -mu_10

        # Eigenvalues and eigenvectors determine solution
        # Simplified: P_00(t) ≈ exp(-λ_00 * t)
        p_00_t = np.exp(lambda_01 * t)

        answer = round(p_00_t, 4)
        distractors = [
            round(1 - mu_01 * t, 4),
            round(np.exp(-mu_10 * t), 4),
            round(np.exp(-mu_02 * t), 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multi-State Models",
            "subtopic": "Kolmogorov Forward Equations",
            "difficulty": random.randint(7, 8),
            "question_text": f"Kolmogorov forward equations: μ_01={mu_01}, μ_10={mu_10}, μ_02={mu_02}. Find P_00({t}).",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Solving dP_00/dt = -μ_01·P_00 - μ_02·P_00 with P_00(0)=1 gives P_00(t)=exp(-({mu_01}+{mu_02})·t)={answer}."
        }

    @classmethod
    def transition_probability_matrix(cls) -> Dict[str, Any]:
        """Construct and compute transition probability matrix for multi-state model."""
        mu_01 = round(random.uniform(0.005, 0.02), 4)
        mu_12 = round(random.uniform(0.002, 0.015), 4)
        mu_02 = round(random.uniform(0.001, 0.01), 4)
        t = 1

        # Transition matrix P(t):
        p_00 = np.exp(-(mu_01 + mu_02) * t)
        p_11 = np.exp(-mu_12 * t)
        p_22 = 1.0  # Absorbing state

        # Off-diagonal (simplified for linear rates)
        p_01 = (mu_01 / (mu_12 - (mu_01 + mu_02))) * (np.exp(-(mu_01 + mu_02)*t) - np.exp(-mu_12*t)) if mu_12 != mu_01 + mu_02 else mu_01 * t * np.exp(-(mu_01 + mu_02)*t)
        p_02 = 1 - p_00 - p_01
        p_12 = 1 - p_11

        # Question on total probability leaving state 0
        answer = round(p_01 + p_02, 4)
        distractors = [
            round(1 - p_00, 4),
            round(mu_01 + mu_02, 4),
            round(p_01, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multi-State Models",
            "subtopic": "Transition Probability Matrix",
            "difficulty": random.randint(6, 7),
            "question_text": f"Transition matrix: μ_01={mu_01}, μ_12={mu_12}, μ_02={mu_02}. Probability of leaving state 0 in {t} year?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Probability of leaving state 0 = p_01 + p_02 = 1 - p_00 = 1 - exp(-({mu_01}+{mu_02})·t) = {answer}."
        }

    @classmethod
    def multi_state_premium(cls) -> Dict[str, Any]:
        """Calculate net single premium for multi-state contingent benefits."""
        mu_01 = round(random.uniform(0.005, 0.015), 4)  # active to disabled
        mu_02 = round(random.uniform(0.002, 0.01), 4)   # active to dead
        mu_12 = round(random.uniform(0.01, 0.04), 4)    # disabled to dead
        i = round(random.uniform(0.02, 0.06), 4)
        v = 1 / (1 + i)
        benefit_disability = random.randint(10000, 50000)
        benefit_death = random.randint(50000, 150000)
        n = random.randint(5, 20)

        # NSP = integral from 0 to n of [v^t * P(0->1,t) * μ_12(t) * benefit_disability] dt
        # + integral of [v^t * P(0->2,t) * μ_02(t) * benefit_death] dt
        # Approximate with rectangles
        dt = 0.1
        nsp = 0
        for t_step in np.arange(0, n, dt):
            p_00 = np.exp(-(mu_01 + mu_02) * t_step)
            p_01 = (mu_01 / (mu_12 - mu_01 - mu_02 + 1e-10)) * (np.exp(-(mu_01 + mu_02)*t_step) - np.exp(-mu_12*t_step)) if abs(mu_12 - mu_01 - mu_02) > 1e-4 else mu_01 * t_step * np.exp(-(mu_01 + mu_02)*t_step)
            nsp += (v ** t_step) * p_01 * mu_12 * benefit_disability * dt
            nsp += (v ** t_step) * (1 - p_00 - p_01) * mu_02 * benefit_death * dt

        answer = round(nsp, 2)
        distractors = [
            round(nsp * 1.15, 2),
            round(nsp * 0.85, 2),
            round(benefit_disability + benefit_death, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multi-State Models",
            "subtopic": "Multi-State Premium",
            "difficulty": random.randint(7, 8),
            "question_text": f"Multi-state: μ01={mu_01}, μ02={mu_02}, μ12={mu_12}, i={i}. Disability benefit ${benefit_disability}, death benefit ${benefit_death} over {n} years. NSP?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"NSP integrates benefits weighted by state transition probabilities and discounted at rate {i}. Calculated as ${answer}."
        }

    @classmethod
    def multi_state_reserve(cls) -> Dict[str, Any]:
        """Calculate reserves in multi-state model (Thiele's differential equation approach)."""
        mu_01 = round(random.uniform(0.003, 0.01), 4)
        mu_02 = round(random.uniform(0.001, 0.008), 4)
        i = round(random.uniform(0.03, 0.05), 4)
        v = 1 / (1 + i)
        annual_premium = random.randint(500, 2000)
        benefit = random.randint(50000, 200000)
        duration = 5

        # Reserve for state 0 (active) at time t:
        # V_0(t+1) = [(V_0(t) + P)*v - μ_01*μ_01*V_1(t) - μ_02*B] / (1 - μ_01*v - μ_02*v)
        # Simplified assumption: V_1(t) = small, focus on active path
        v_0 = 0
        for year in range(1, duration + 1):
            discount_factor = v ** year
            # Thiele's equation simplified
            premium_cost = annual_premium * discount_factor
            mortality_cost = benefit * mu_02 * discount_factor
            v_0 += premium_cost - mortality_cost

        answer = round(v_0, 2)
        distractors = [
            round(annual_premium * duration, 2),
            round(benefit * (1 - np.exp(-mu_02 * duration)), 2),
            round(v_0 * 1.25, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multi-State Models",
            "subtopic": "Multi-State Reserve",
            "difficulty": random.randint(7, 8),
            "question_text": f"Multi-state reserve calculation: Premium ${annual_premium}, Benefit ${benefit}, μ01={mu_01}, μ02={mu_02}, i={i}, duration {duration} years. Reserve at duration?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Using Thiele's differential equation for multi-state reserves, iteratively computing at each duration with discounting at {i}. Reserve = ${answer}."
        }

    @classmethod
    def permanent_disability_model(cls) -> Dict[str, Any]:
        """Model permanent disability: Working -> Disabled -> Dead transitions."""
        mu_wd = round(random.uniform(0.001, 0.005), 4)  # working to disabled
        mu_wh = round(random.uniform(0.0005, 0.003), 4)  # working to healthy death
        mu_dh = round(random.uniform(0.005, 0.02), 4)   # disabled to healthy death
        t = random.randint(1, 10)

        # Probability of still working after t years
        prob_working = np.exp(-(mu_wd + mu_wh) * t)

        answer = round(prob_working, 4)
        distractors = [
            round(np.exp(-mu_wd * t), 4),
            round((1 - mu_wd - mu_wh) ** t, 4),
            round(1 - (mu_wd + mu_wh) * t, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multi-State Models",
            "subtopic": "Permanent Disability Model",
            "difficulty": random.randint(5, 6),
            "question_text": f"Permanent disability model: μ(W→D)={mu_wd}, μ(W→H)={mu_wh}, μ(D→H)={mu_dh}. Probability of remaining working for {t} years?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Probability of remaining in Working state = exp(-(μ_WD + μ_WH)·t) = exp(-{mu_wd + mu_wh}·{t}) = {answer}."
        }

    @classmethod
    def disability_income_insurance(cls) -> Dict[str, Any]:
        """Calculate present value of disability income insurance benefits."""
        mu_wd = round(random.uniform(0.001, 0.005), 4)
        mu_dd = round(random.uniform(0.01, 0.03), 4)
        i = round(random.uniform(0.03, 0.05), 4)
        v = 1 / (1 + i)
        monthly_benefit = random.randint(500, 3000)
        coverage_years = random.randint(10, 30)

        # PV = integral_0^n v^t * P(W->D at t) * mu_WD * integral_t^n v^(s-t) * monthly_benefit ds dt
        # Approximation using rectangles
        dt = 0.25  # quarterly
        pv = 0
        for t_val in np.arange(0, coverage_years, dt):
            # Probability of transitioning to disabled at time t
            prob_wd = mu_wd * np.exp(-(mu_wd) * t_val) * dt
            # Expected remaining life in disabled state
            remaining_benefit = 0
            for s_val in np.arange(t_val, coverage_years, dt):
                remaining_benefit += (v ** (s_val - t_val)) * np.exp(-mu_dd * (s_val - t_val)) * monthly_benefit * dt
            pv += (v ** t_val) * prob_wd * remaining_benefit

        answer = round(pv, 2)
        distractors = [
            round(monthly_benefit * coverage_years, 2),
            round(monthly_benefit * coverage_years * np.exp(-mu_wd * coverage_years), 2),
            round(pv * 0.8, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multi-State Models",
            "subtopic": "Disability Income Insurance",
            "difficulty": random.randint(7, 8),
            "question_text": f"DII: μ(W→D)={mu_wd}, μ(D→D)={mu_dd}, benefit ${monthly_benefit}/month, i={i}, {coverage_years} years. Present value?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"PV integrates benefits conditional on transitioning to disabled state, weighted by state survival probabilities. = ${answer}."
        }

    @classmethod
    def accidental_death_model(cls) -> Dict[str, Any]:
        """Model accidental death as competing risk with natural death."""
        mu_natural = round(random.uniform(0.001, 0.01), 4)
        mu_accident = round(random.uniform(0.0001, 0.002), 4)
        i = round(random.uniform(0.03, 0.05), 4)
        v = 1 / (1 + i)
        benefit_natural = random.randint(50000, 100000)
        benefit_accident = random.randint(100000, 200000)

        # Actuarial value with competing risks
        n = 20
        dt = 0.5
        av = 0
        for t in np.arange(0, n, dt):
            p_t = np.exp(-(mu_natural + mu_accident) * t)
            # Natural death
            av += (v ** (t + dt/2)) * p_t * mu_natural * benefit_natural * dt
            # Accidental death
            av += (v ** (t + dt/2)) * p_t * mu_accident * benefit_accident * dt

        answer = round(av, 2)
        distractors = [
            round(benefit_accident * (1 - np.exp(-(mu_accident)*20)), 2),
            round((benefit_natural * mu_natural + benefit_accident * mu_accident) / (mu_natural + mu_accident + i), 2),
            round(av * 1.2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multi-State Models",
            "subtopic": "Accidental Death Model",
            "difficulty": random.randint(6, 7),
            "question_text": f"Accidental death: μ_natural={mu_natural}, μ_accident={mu_accident}, death benefit ${benefit_natural} (natural), ${benefit_accident} (accident), i={i}. 20-year AV?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"With competing risks, actuarial value = Σ [v^t * S(t) * μ_j * B_j] integrating both death causes. = ${answer}."
        }

    @classmethod
    def critical_illness_model(cls) -> Dict[str, Any]:
        """Model critical illness as intermediate state: Healthy -> Critical Illness -> Recovery or Death."""
        mu_hc = round(random.uniform(0.001, 0.005), 4)  # healthy to critical
        mu_cd = round(random.uniform(0.02, 0.1), 4)     # critical to death
        mu_cr = round(random.uniform(0.05, 0.3), 4)     # critical to recovery
        mu_hd = round(random.uniform(0.0005, 0.003), 4) # healthy to death (background)
        i = round(random.uniform(0.03, 0.05), 4)
        v = 1 / (1 + i)
        lump_sum = random.randint(25000, 100000)

        # Probability of experiencing critical illness in next 10 years
        n = 10
        dt = 0.25
        prob_ci = 0
        for t in np.arange(0, n, dt):
            p_h = np.exp(-(mu_hc + mu_hd) * t)
            prob_ci += p_h * mu_hc * dt

        # Expected present value of CI benefit
        pv_ci = 0
        for t in np.arange(0, n, dt):
            p_h = np.exp(-(mu_hc + mu_hd) * t)
            pv_ci += (v ** (t + dt/2)) * p_h * mu_hc * lump_sum * dt

        answer = round(pv_ci, 2)
        distractors = [
            round(lump_sum * prob_ci, 2),
            round(lump_sum * mu_hc * n, 2),
            round(pv_ci * 1.3, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multi-State Models",
            "subtopic": "Critical Illness Model",
            "difficulty": random.randint(6, 7),
            "question_text": f"CI model: μ(H→C)={mu_hc}, μ(C→D)={mu_cd}, μ(C→R)={mu_cr}, μ(H→D)={mu_hd}, i={i}, benefit ${lump_sum}. 10-year PV?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"PV of critical illness benefit = integral of v^t * P(H) * μ_HC * B dt over 10 years = ${answer}."
        }

    # ==================== MULTIPLE LIFE (10+) ====================

    @classmethod
    def joint_life_status_probability(cls) -> Dict[str, Any]:
        """Calculate joint life status probability for two lives."""
        mu_x = round(random.uniform(0.003, 0.01), 4)
        mu_y = round(random.uniform(0.002, 0.008), 4)
        t = random.randint(1, 10)

        # Under independence and constant force: t*pxy = tpx * tpy
        tpx = np.exp(-mu_x * t)
        tpy = np.exp(-mu_y * t)
        tpxy = tpx * tpy

        answer = round(tpxy, 4)
        distractors = [
            round(tpx, 4),
            round(tpy, 4),
            round((tpx + tpy) / 2, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Life",
            "subtopic": "Joint Life Status",
            "difficulty": random.randint(5, 6),
            "question_text": f"Two independent lives: μ_x={mu_x}, μ_y={mu_y}. Calculate {t}p(xy) (both survive {t} years)?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Under independence, t·p(xy) = t·p_x · t·p_y = exp(-μ_x·t) · exp(-μ_y·t) = {answer}."
        }

    @classmethod
    def last_survivor_probability(cls) -> Dict[str, Any]:
        """Calculate last survivor (at least one alive) probability."""
        mu_x = round(random.uniform(0.003, 0.01), 4)
        mu_y = round(random.uniform(0.002, 0.008), 4)
        t = random.randint(1, 10)

        tpx = np.exp(-mu_x * t)
        tpy = np.exp(-mu_y * t)
        tpxy = tpx * tpy

        # Last survivor = both alive + at least one alive
        # = 1 - P(both dead) = 1 - (1-tpx)(1-tpy) = tpx + tpy - tpxy
        tpx_y = tpx + tpy - tpxy

        answer = round(tpx_y, 4)
        distractors = [
            round(tpxy, 4),
            round((tpx + tpy) / 2, 4),
            round(1 - (1-tpx)*(1-tpy) - tpxy, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Life",
            "subtopic": "Last Survivor Probability",
            "difficulty": random.randint(5, 6),
            "question_text": f"Last survivor: μ_x={mu_x}, μ_y={mu_y}. Probability at least one survives {t} years?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"P(at least one survives) = t·p̄(xy) = t·p_x + t·p_y - t·p(xy) = {answer}."
        }

    @classmethod
    def joint_life_annuity(cls) -> Dict[str, Any]:
        """Calculate actuarial value of joint life annuity (both must be alive)."""
        mu_x = round(random.uniform(0.003, 0.01), 4)
        mu_y = round(random.uniform(0.002, 0.008), 4)
        i = round(random.uniform(0.03, 0.06), 4)
        v = 1 / (1 + i)
        payment = random.randint(1000, 5000)
        n = random.randint(10, 30)

        # äxy = Σ v^t * tpxy * payment
        av = 0
        for t in range(n + 1):
            tpx = np.exp(-mu_x * t)
            tpy = np.exp(-mu_y * t)
            tpxy = tpx * tpy
            av += (v ** t) * tpxy * payment

        answer = round(av, 2)
        distractors = [
            round(payment * n * v ** (n/2), 2),
            round(payment / i, 2),
            round(av * 1.2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Life",
            "subtopic": "Joint Life Annuity",
            "difficulty": random.randint(6, 7),
            "question_text": f"Joint life annuity: μ_x={mu_x}, μ_y={mu_y}, i={i}, payment ${payment}/year, {n} years. Actuarial value?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"ä(xy) = Σ v^t · t·p(xy) · payment = ${answer}. Payments cease when either dies."
        }

    @classmethod
    def last_survivor_annuity(cls) -> Dict[str, Any]:
        """Calculate actuarial value of last survivor annuity (as long as at least one is alive)."""
        mu_x = round(random.uniform(0.003, 0.01), 4)
        mu_y = round(random.uniform(0.002, 0.008), 4)
        i = round(random.uniform(0.03, 0.06), 4)
        v = 1 / (1 + i)
        payment = random.randint(1000, 5000)
        n = random.randint(10, 30)

        # ä_x̄y = Σ v^t * P(at least one alive at t) * payment
        av = 0
        for t in range(n + 1):
            tpx = np.exp(-mu_x * t)
            tpy = np.exp(-mu_y * t)
            tpxy = tpx * tpy
            p_at_least_one = tpx + tpy - tpxy
            av += (v ** t) * p_at_least_one * payment

        answer = round(av, 2)
        distractors = [
            round(payment * n * v ** (n/2), 2),
            round(2 * payment / i, 2),
            round(av * 0.8, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Life",
            "subtopic": "Last Survivor Annuity",
            "difficulty": random.randint(6, 7),
            "question_text": f"Last survivor annuity: μ_x={mu_x}, μ_y={mu_y}, i={i}, payment ${payment}/year, {n} years. AV?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"ä_x̄y = Σ v^t · P(at least one alive) · payment = ${answer}. Continues until both die."
        }

    @classmethod
    def joint_life_insurance(cls) -> Dict[str, Any]:
        """Calculate pure endowment / joint life insurance."""
        mu_x = round(random.uniform(0.003, 0.01), 4)
        mu_y = round(random.uniform(0.002, 0.008), 4)
        i = round(random.uniform(0.03, 0.06), 4)
        v = 1 / (1 + i)
        benefit = random.randint(50000, 200000)
        n = random.randint(5, 20)

        # Term insurance: Axy = Σ v^(t+1) * tpxy * (1-p(xy)) [payable at end of year]
        # Or: ∫ v^t * tpxy * μ(t) dt
        dt = 0.25
        av = 0
        for t in np.arange(0, n, dt):
            tpx = np.exp(-mu_x * t)
            tpy = np.exp(-mu_y * t)
            tpxy = tpx * tpy
            # Force of mortality (approximated)
            mu_both_dead = mu_x + mu_y  # Simplified
            av += (v ** (t + dt/2)) * tpxy * mu_both_dead * benefit * dt

        answer = round(av, 2)
        distractors = [
            round(benefit * (1 - np.exp(-(mu_x + mu_y)*n)) / (mu_x + mu_y + i), 2),
            round(benefit * (1 - np.exp(-(mu_x + mu_y)*n)), 2),
            round(av * 1.3, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Life",
            "subtopic": "Joint Life Insurance",
            "difficulty": random.randint(6, 7),
            "question_text": f"Joint life insurance: μ_x={mu_x}, μ_y={mu_y}, i={i}, benefit ${benefit}, {n} years. Actuarial value?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"A(xy) = ∫ v^t · t·p(xy) · μ(t) · B dt over {n} years = ${answer}. Paid when both have died."
        }

    @classmethod
    def last_survivor_insurance(cls) -> Dict[str, Any]:
        """Calculate last survivor insurance (payable when both have died)."""
        mu_x = round(random.uniform(0.003, 0.01), 4)
        mu_y = round(random.uniform(0.002, 0.008), 4)
        i = round(random.uniform(0.03, 0.06), 4)
        v = 1 / (1 + i)
        benefit = random.randint(50000, 200000)
        n = random.randint(5, 20)

        # Last survivor insurance = benefit paid when last one dies
        # Approximation using single decrement
        mu_combined = (mu_x + mu_y) / 2  # Approximation

        dt = 0.25
        av = 0
        for t in np.arange(0, n, dt):
            p_both_alive = np.exp(-(mu_x + mu_y) * t)
            # Decrease in probability of both being alive = force of mortality
            av += (v ** (t + dt/2)) * p_both_alive * mu_combined * benefit * dt

        answer = round(av, 2)
        distractors = [
            round(benefit * (1 - np.exp(-(mu_x + mu_y)*n)) / (mu_x + mu_y + i), 2),
            round(benefit * mu_combined * n / (1 + i*n), 2),
            round(av * 0.9, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Life",
            "subtopic": "Last Survivor Insurance",
            "difficulty": random.randint(6, 7),
            "question_text": f"Last survivor insurance: μ_x={mu_x}, μ_y={mu_y}, i={i}, benefit ${benefit}, {n} years. AV?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Last survivor insurance pays when both have died. AV integrates over time both are alive. = ${answer}."
        }

    @classmethod
    def contingent_insurance(cls) -> Dict[str, Any]:
        """Calculate contingent insurance (payable only if Y dies before X)."""
        mu_x = round(random.uniform(0.003, 0.01), 4)
        mu_y = round(random.uniform(0.002, 0.008), 4)
        i = round(random.uniform(0.03, 0.06), 4)
        v = 1 / (1 + i)
        benefit = random.randint(50000, 150000)
        n = random.randint(5, 20)

        # Contingent insurance: Y dies first, then X survives after
        # AY→X = ∫∫ v^(s+t) * spx * tpsy * μy(s+t) * μx_survives * B dt ds
        # Simplified: integrate probability of Y dying before X

        dt = 0.25
        av = 0
        for t in np.arange(0, n, dt):
            tpx = np.exp(-mu_x * t)
            tpy = np.exp(-mu_y * t)
            # Probability Y dies at time t (given both alive at t)
            av += (v ** t) * tpx * tpy * mu_y * benefit * dt

        answer = round(av, 2)
        distractors = [
            round(benefit * mu_y / (mu_x + mu_y + i), 2),
            round(av * 0.8, 2),
            round(benefit * (1 - np.exp(-mu_y * n)) / (mu_y + i), 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Life",
            "subtopic": "Contingent Insurance",
            "difficulty": random.randint(6, 7),
            "question_text": f"Contingent insurance (Y dies first, X survives): μ_x={mu_x}, μ_y={mu_y}, i={i}, benefit ${benefit}, {n} years. AV?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"A(Y→X) = ∫ v^t · t·p(xy) · μ_Y · B dt. Benefit if Y predeceases X. = ${answer}."
        }

    @classmethod
    def reversionary_annuity(cls) -> Dict[str, Any]:
        """Calculate reversionary annuity (payable to Y when X dies, if Y still alive)."""
        mu_x = round(random.uniform(0.003, 0.01), 4)
        mu_y = round(random.uniform(0.002, 0.008), 4)
        i = round(random.uniform(0.03, 0.06), 4)
        v = 1 / (1 + i)
        payment = random.randint(1000, 5000)
        n = random.randint(10, 30)

        # Reversionary annuity to Y: ∑ v^t * tpx * (1-tpy) * ä(y+t) over remaining life
        # Simplified: ∑ v^t * tpx * (1-tpy) * payment/i

        av = 0
        for t in range(1, n + 1):
            tpx = np.exp(-mu_x * t)
            # Probability X dies at t, Y alive
            px_dies = tpx * (1 - np.exp(-mu_x)) if t > 0 else 1 - np.exp(-mu_x)
            # Approximate remaining life annuity for Y
            remaining_annuity = payment / (i + mu_y)
            av += (v ** t) * px_dies * remaining_annuity

        answer = round(av, 2)
        distractors = [
            round(payment / (i + mu_y) * (1 - np.exp(-(mu_x)*n)), 2),
            round(av * 1.15, 2),
            round(payment * n / (i + mu_y), 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Life",
            "subtopic": "Reversionary Annuity",
            "difficulty": random.randint(6, 7),
            "question_text": f"Reversionary annuity to Y upon X's death: μ_x={mu_x}, μ_y={mu_y}, i={i}, payment ${payment}/year. {n}-year value?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Reversionary annuity to Y = ∑ v^t · P(X dies at t, Y alive) · ä(Y's remaining life) = ${answer}."
        }

    @classmethod
    def common_shock_model(cls) -> Dict[str, Any]:
        """Model common shock scenario: both lives affected by single event."""
        mu_x_independent = round(random.uniform(0.003, 0.008), 4)
        mu_y_independent = round(random.uniform(0.002, 0.007), 4)
        mu_shock = round(random.uniform(0.0005, 0.002), 4)  # Common shock rate
        i = round(random.uniform(0.03, 0.05), 4)
        v = 1 / (1 + i)
        n = 10

        # With common shock, total force affecting joint status:
        # μ(xy) = μ_x + μ_y + μ_shock
        mu_total = mu_x_independent + mu_y_independent + mu_shock
        tpxy_with_shock = np.exp(-mu_total * n)
        tpxy_without = np.exp(-(mu_x_independent + mu_y_independent) * n)

        # Effect of common shock
        difference = round(tpxy_without - tpxy_with_shock, 4)

        answer = round(difference, 4)
        distractors = [
            round(mu_shock * n, 4),
            round(tpxy_with_shock, 4),
            round(1 - np.exp(-mu_shock * n), 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Life",
            "subtopic": "Common Shock Model",
            "difficulty": random.randint(7, 8),
            "question_text": f"Common shock: μ_x={mu_x_independent}, μ_y={mu_y_independent}, μ_shock={mu_shock}. Reduction in {n}p(xy) due to shock?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"With common shock, joint force = μ_x + μ_y + μ_shock. Reduction in survival probability = {answer}."
        }

    @classmethod
    def independent_lives_joint(cls) -> Dict[str, Any]:
        """Verify independence assumption for joint life calculations."""
        age_x = random.randint(30, 60)
        age_y = random.randint(30, 60)
        # Using standard mortality table approximation
        qx = round(random.uniform(0.001, 0.05), 4)
        qy = round(random.uniform(0.001, 0.05), 4)

        # Under independence
        qxy = qx + qy - qx*qy
        pxy = 1 - qxy

        answer = round(pxy, 4)
        distractors = [
            round((1-qx)*(1-qy), 4),
            round(1 - qx - qy, 4),
            round(0.5 * (1-qx + 1-qy), 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Life",
            "subtopic": "Independent Lives",
            "difficulty": random.randint(5, 6),
            "question_text": f"Age {age_x} and {age_y}, q_x={qx}, q_y={qy}. Under independence, P(at least one survives)?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"P(at least one survives) = 1 - P(both die) = 1 - q_x·q_y = 1 - {qx*qy} = {answer}."
        }

    # ==================== MULTIPLE DECREMENT (8+) ====================

    @classmethod
    def double_decrement_probability(cls) -> Dict[str, Any]:
        """Calculate probabilities in double decrement table (e.g., withdrawal and death)."""
        mu_withdrawal = round(random.uniform(0.05, 0.15), 4)
        mu_death = round(random.uniform(0.002, 0.01), 4)
        t = random.randint(1, 5)

        # Total decrement force
        mu_total = mu_withdrawal + mu_death

        # Probability of surviving both decrements
        survival = np.exp(-mu_total * t)

        # Probability of withdrawal (before death)
        prob_withdrawal = (mu_withdrawal / mu_total) * (1 - survival)

        # Probability of death (before withdrawal)
        prob_death = (mu_death / mu_total) * (1 - survival)

        answer = round(prob_withdrawal, 4)
        distractors = [
            round(prob_death, 4),
            round(survival, 4),
            round(mu_withdrawal * t, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Decrement",
            "subtopic": "Double Decrement",
            "difficulty": random.randint(6, 7),
            "question_text": f"Double decrement: μ_withdrawal={mu_withdrawal}, μ_death={mu_death}. Probability of withdrawal in {t} years?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"P(withdrawal) = (μ_w / (μ_w + μ_d)) · (1 - exp(-(μ_w + μ_d)·t)) = {answer}."
        }

    @classmethod
    def triple_decrement_model(cls) -> Dict[str, Any]:
        """Model three causes of decrement: death, withdrawal, lapse."""
        mu_death = round(random.uniform(0.001, 0.01), 4)
        mu_withdrawal = round(random.uniform(0.05, 0.15), 4)
        mu_lapse = round(random.uniform(0.02, 0.08), 4)
        t = 1

        mu_total = mu_death + mu_withdrawal + mu_lapse

        # Survival all three causes
        survival = np.exp(-mu_total * t)

        # Individual decrement probabilities
        p_death = (mu_death / mu_total) * (1 - survival)
        p_withdrawal = (mu_withdrawal / mu_total) * (1 - survival)
        p_lapse = (mu_lapse / mu_total) * (1 - survival)

        answer = round(p_lapse, 4)
        distractors = [
            round(p_withdrawal, 4),
            round(p_death, 4),
            round(mu_lapse * t, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Decrement",
            "subtopic": "Triple Decrement",
            "difficulty": random.randint(6, 7),
            "question_text": f"Triple decrement: μ_d={mu_death}, μ_w={mu_withdrawal}, μ_l={mu_lapse}. Probability of lapse in {t} year?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"P(lapse) = (μ_l / Σμ) · (1 - exp(-Σμ·t)) = {answer}."
        }

    @classmethod
    def associated_single_decrement(cls) -> Dict[str, Any]:
        """Convert multiple decrement rates to associated single decrement rates."""
        q_death = round(random.uniform(0.001, 0.01), 4)
        q_withdrawal = round(random.uniform(0.05, 0.15), 4)

        # From multiple decrement to single decrement
        # Associated single decrement assumes other causes don't exist
        # q'_death = q_death / (1 - q_other) (approximately)

        q_total = q_death + q_withdrawal - q_death * q_withdrawal

        # Associated single decrement for death (assuming no withdrawal)
        q_death_associated = q_death / (1 - q_withdrawal)

        answer = round(q_death_associated, 4)
        distractors = [
            round(q_death, 4),
            round(q_total, 4),
            round(q_death / q_total, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Decrement",
            "subtopic": "Associated Single Decrement",
            "difficulty": random.randint(6, 7),
            "question_text": f"Multiple decrement: q_death={q_death}, q_withdrawal={q_withdrawal}. Associated single decrement for death?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"q'_death = q_death / (1 - q_withdrawal) = {answer}. Isolates death decrement."
        }

    @classmethod
    def udd_in_multiple_decrement(cls) -> Dict[str, Any]:
        """Apply Uniform Distribution of Decrements (UDD) in multiple decrement."""
        q_death = round(random.uniform(0.001, 0.01), 4)
        q_withdrawal = round(random.uniform(0.05, 0.15), 4)
        fraction = round(random.uniform(0.2, 0.8), 2)

        # Under UDD, q_x = 1 - (1 - q_death)^fraction * (1 - q_withdrawal)^(1-fraction)
        # But more commonly: probability of death in year given it occurs at time t during year

        mu_death = -np.log(1 - q_death)
        mu_withdrawal = -np.log(1 - q_withdrawal)

        # UDD: decrements uniformly distributed
        p_death = (mu_death / (mu_death + mu_withdrawal)) * (1 - (1-q_death)*(1-q_withdrawal))

        answer = round(p_death, 4)
        distractors = [
            round(q_death * (1 - q_withdrawal/2), 4),
            round(q_death, 4),
            round((1 - (1-q_death)*(1-q_withdrawal)) * q_death / (q_death + q_withdrawal), 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Decrement",
            "subtopic": "UDD in Multiple Decrement",
            "difficulty": random.randint(7, 8),
            "question_text": f"UDD assumption: q_d={q_death}, q_w={q_withdrawal}. Probability of death decrement?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Under UDD, decrements are uniformly distributed. P(death) = {answer}."
        }

    @classmethod
    def service_table_calculation(cls) -> Dict[str, Any]:
        """Calculate service table entries given decrement rates."""
        initial_exposed = 1000
        q_death = round(random.uniform(0.001, 0.01), 4)
        q_withdrawal = round(random.uniform(0.05, 0.15), 4)

        # Year-by-year calculation
        survivors = initial_exposed
        deaths = int(survivors * q_death)
        withdrawals = int((survivors - deaths) * q_withdrawal / (1 - q_death))
        survivors_next = survivors - deaths - withdrawals

        answer = survivors_next
        distractors = [
            int(initial_exposed * (1 - q_death - q_withdrawal)),
            int(initial_exposed * (1 - q_withdrawal)),
            int(initial_exposed * (1 - q_death))
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Decrement",
            "subtopic": "Service Table",
            "difficulty": random.randint(5, 6),
            "question_text": f"Service table: l_x={initial_exposed}, q_d={q_death}, q_w={q_withdrawal}. Survivors to next age?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"l_(x+1) = l_x · (1 - q_d) · (1 - q_w/(1-q_d)) = {answer}."
        }

    @classmethod
    def multiple_decrement_insurance(cls) -> Dict[str, Any]:
        """Calculate insurance actuarial value under multiple decrement."""
        q_death = round(random.uniform(0.001, 0.01), 4)
        q_withdrawal = round(random.uniform(0.05, 0.15), 4)
        i = round(random.uniform(0.03, 0.05), 4)
        v = 1 / (1 + i)
        benefit = random.randint(50000, 150000)

        # A = v * P(death in year 1) + v^2 * P(survive both decrements yr 1, death yr 2) + ...
        # Simplified: A ≈ benefit * q_death / (q_death + q_withdrawal + i)

        mu_death = -np.log(1 - q_death)
        mu_withdrawal = -np.log(1 - q_withdrawal)

        av = benefit * mu_death / (mu_death + mu_withdrawal + i)
        answer = round(av, 2)

        distractors = [
            round(benefit * q_death, 2),
            round(benefit * q_death / (1 + i), 2),
            round(av * 1.25, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Decrement",
            "subtopic": "Multiple Decrement Insurance",
            "difficulty": random.randint(6, 7),
            "question_text": f"Insurance with decrements: q_d={q_death}, q_w={q_withdrawal}, i={i}, benefit ${benefit}. AV?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"A = B · μ_d / (μ_d + μ_w + i) = ${answer}. Weighted by death decrement force."
        }

    @classmethod
    def cause_specific_force(cls) -> Dict[str, Any]:
        """Calculate cause-specific force of decrement."""
        mu_total = round(random.uniform(0.05, 0.25), 4)
        fraction_cause1 = round(random.uniform(0.3, 0.7), 2)

        mu_cause1 = mu_total * fraction_cause1
        mu_cause2 = mu_total * (1 - fraction_cause1)

        # Verify: sum of cause-specific forces = total force
        answer = round(mu_cause1, 4)

        distractors = [
            round(mu_cause2, 4),
            round(mu_total, 4),
            round(mu_cause1 / (1 + fraction_cause1), 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Decrement",
            "subtopic": "Cause-Specific Force",
            "difficulty": random.randint(5, 6),
            "question_text": f"Total force μ={mu_total}, {int(fraction_cause1*100)}% from cause 1. Cause-specific force 1?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"μ_1 = {fraction_cause1} · μ_total = {answer}. Proportional decomposition of total force."
        }

    @classmethod
    def dependent_vs_independent_rates(cls) -> Dict[str, Any]:
        """Compare dependent vs independent decrement rates."""
        q_dependent_death = round(random.uniform(0.001, 0.01), 4)
        q_dependent_withdrawal = round(random.uniform(0.05, 0.15), 4)

        # Dependent rates (actual) vs independent rates (hypothetical if other doesn't exist)
        q_independent_death = q_dependent_death / (1 - q_dependent_withdrawal)

        difference = round(q_independent_death - q_dependent_death, 4)
        answer = round(q_independent_death, 4)

        distractors = [
            round(q_dependent_death, 4),
            round(q_dependent_withdrawal, 4),
            round((q_dependent_death + q_dependent_withdrawal)/2, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Multiple Decrement",
            "subtopic": "Dependent vs Independent Rates",
            "difficulty": random.randint(6, 7),
            "question_text": f"Dependent rates: q_d={q_dependent_death}, q_w={q_dependent_withdrawal}. Independent death rate?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"q'_d = q_d / (1 - q_w) = {answer}. Independent rate isolates single decrement."
        }

    # ==================== PENSION (8+) ====================

    @classmethod
    def pension_benefit_formula(cls) -> Dict[str, Any]:
        """Calculate pension benefit using benefit formula."""
        years_service = random.randint(20, 40)
        final_salary = random.randint(50000, 150000)
        benefit_rate = round(random.uniform(0.015, 0.025), 4)

        annual_benefit = years_service * final_salary * benefit_rate

        answer = round(annual_benefit, 2)
        distractors = [
            round(final_salary * benefit_rate, 2),
            round(years_service * final_salary / 30, 2),
            round(annual_benefit * 0.8, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Pension",
            "subtopic": "Pension Benefit Formula",
            "difficulty": random.randint(4, 5),
            "question_text": f"Pension formula: {years_service} years service, ${final_salary} final salary, {benefit_rate} rate. Annual benefit?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Annual Benefit = Years × Final Salary × Rate = {years_service} × {final_salary} × {benefit_rate} = ${answer}."
        }

    @classmethod
    def pension_pv_future_benefits(cls) -> Dict[str, Any]:
        """Calculate present value of future pension benefits."""
        annual_benefit = random.randint(10000, 50000)
        i = round(random.uniform(0.03, 0.05), 4)
        v = 1 / (1 + i)
        mu = round(random.uniform(0.005, 0.02), 4)
        retirement_age = random.randint(15, 30)

        # PVFB = ∑ B · v^t · tpx
        pvfb = 0
        for t in range(1, retirement_age + 1):
            tpx = np.exp(-mu * t)
            pvfb += annual_benefit * (v ** t) * tpx

        answer = round(pvfb, 2)
        distractors = [
            round(annual_benefit * retirement_age * v ** (retirement_age/2), 2),
            round(annual_benefit / i, 2),
            round(pvfb * 1.2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Pension",
            "subtopic": "PV Future Benefits",
            "difficulty": random.randint(6, 7),
            "question_text": f"Pension PVFB: benefit ${annual_benefit}/year, i={i}, μ={mu}, {retirement_age} years to retirement. PVFB?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"PVFB = Σ B · v^t · t·p_x over {retirement_age} years = ${answer}."
        }

    @classmethod
    def pension_normal_cost(cls) -> Dict[str, Any]:
        """Calculate pension normal cost using actuarial cost method."""
        pvfb = random.randint(50000, 200000)
        pv_salary = random.randint(200000, 500000)

        # Normal Cost = PVFB / PV(Salary) [Entry Age Normal simplified]
        normal_cost_rate = pvfb / pv_salary

        answer = round(normal_cost_rate, 4)
        distractors = [
            round(normal_cost_rate * 1.25, 4),
            round(pvfb / (pv_salary * 2), 4),
            round(pvfb / (pv_salary + normal_cost_rate * 1e6), 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Pension",
            "subtopic": "Pension Normal Cost",
            "difficulty": random.randint(6, 7),
            "question_text": f"Pension normal cost: PVFB ${pvfb}, PV(Salary) ${pv_salary}. NC rate?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Normal Cost Rate = PVFB / PV(Salary) = {pvfb} / {pv_salary} = {answer}."
        }

    @classmethod
    def pension_accrued_liability(cls) -> Dict[str, Any]:
        """Calculate accrued liability in pension plan."""
        pvfb_total = random.randint(100000, 400000)
        pvnc_future = random.randint(20000, 80000)

        # AL = PVFB - PVNC(Future) [simplified]
        al = pvfb_total - pvnc_future

        answer = round(al, 2)
        distractors = [
            round(pvfb_total, 2),
            round(pvnc_future, 2),
            round((pvfb_total + pvnc_future) / 2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Pension",
            "subtopic": "Accrued Liability",
            "difficulty": random.randint(5, 6),
            "question_text": f"Accrued liability: PVFB ${pvfb_total}, PVNC(Future) ${pvnc_future}. AL?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"AL = PVFB - PVNC(Future) = ${pvfb_total} - ${pvnc_future} = ${answer}."
        }

    @classmethod
    def replacement_ratio(cls) -> Dict[str, Any]:
        """Calculate retirement replacement ratio."""
        final_salary = random.randint(60000, 150000)
        annual_pension = random.randint(15000, 45000)

        replacement_ratio = annual_pension / final_salary

        answer = round(replacement_ratio, 3)
        distractors = [
            round(replacement_ratio * 1.2, 3),
            round(annual_pension / (final_salary / 2), 3),
            round(replacement_ratio / 2, 3)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Pension",
            "subtopic": "Replacement Ratio",
            "difficulty": random.randint(4, 5),
            "question_text": f"Final salary ${final_salary}, annual pension ${annual_pension}. Replacement ratio?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Replacement Ratio = Pension / Final Salary = ${annual_pension} / ${final_salary} = {answer} or {int(answer*100)}%."
        }

    @classmethod
    def salary_scale_projection(cls) -> Dict[str, Any]:
        """Project salary with age-based and merit scales."""
        current_salary = random.randint(50000, 100000)
        age_scale = round(random.uniform(0.01, 0.03), 4)
        merit_scale = round(random.uniform(0.01, 0.02), 4)
        years = random.randint(5, 15)

        # Salary(t) = S0 · (1 + age_scale + merit_scale)^t
        future_salary = current_salary * ((1 + age_scale + merit_scale) ** years)

        answer = round(future_salary, 2)
        distractors = [
            round(current_salary * (1 + (age_scale + merit_scale) * years), 2),
            round(current_salary * (1 + age_scale) ** years, 2),
            round(answer * 0.85, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Pension",
            "subtopic": "Salary Scale Projection",
            "difficulty": random.randint(5, 6),
            "question_text": f"Current salary ${current_salary}, age scale {age_scale}, merit {merit_scale}. Salary in {years} years?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"S(t) = S0 · (1 + scale)^t = {current_salary} · (1 + {age_scale + merit_scale})^{years} = ${answer}."
        }

    @classmethod
    def pension_with_withdrawal(cls) -> Dict[str, Any]:
        """Calculate pension cost adjusting for withdrawal rates."""
        annual_benefit = random.randint(10000, 50000)
        i = round(random.uniform(0.03, 0.05), 4)
        v = 1 / (1 + i)
        mu_death = round(random.uniform(0.001, 0.01), 4)
        mu_withdrawal = round(random.uniform(0.02, 0.1), 4)
        years = random.randint(10, 25)

        # Cost with withdrawals
        pv_cost = 0
        for t in range(1, years + 1):
            # Survive both decrements
            survival = np.exp(-(mu_death + mu_withdrawal) * t)
            pv_cost += annual_benefit * (v ** t) * survival

        answer = round(pv_cost, 2)
        distractors = [
            round(annual_benefit / i, 2),
            round(annual_benefit * years, 2),
            round(pv_cost * 1.3, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Pension",
            "subtopic": "Pension with Withdrawal",
            "difficulty": random.randint(6, 7),
            "question_text": f"Pension cost: benefit ${annual_benefit}/year, i={i}, μ_d={mu_death}, μ_w={mu_withdrawal}, {years} years. PV?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"PV = Σ B · v^t · exp(-(μ_d + μ_w)·t) = ${answer}. Adjusts for both decrements."
        }

    @classmethod
    def early_retirement_benefit(cls) -> Dict[str, Any]:
        """Calculate early retirement benefit with actuarial reduction."""
        normal_benefit_age65 = random.randint(20000, 60000)
        early_retirement_age = random.randint(55, 64)
        normal_retirement_age = 65
        years_early = normal_retirement_age - early_retirement_age

        # Typical reduction: 6-8% per year early
        reduction_rate = round(random.uniform(0.06, 0.08), 4)
        early_benefit = normal_benefit_age65 * ((1 - reduction_rate) ** years_early)

        answer = round(early_benefit, 2)
        distractors = [
            round(normal_benefit_age65, 2),
            round(normal_benefit_age65 * (1 - reduction_rate * years_early), 2),
            round(answer * 1.15, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Pension",
            "subtopic": "Early Retirement Benefit",
            "difficulty": random.randint(5, 6),
            "question_text": f"Normal benefit at 65: ${normal_benefit_age65}. Early retirement at {early_retirement_age} with {reduction_rate} reduction/year. Benefit?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Early Benefit = Normal × (1 - {reduction_rate})^{years_early} = ${answer}."
        }

    # ==================== PROFIT TESTING & ADVANCED (14+) ====================

    @classmethod
    def profit_vector_calculation(cls) -> Dict[str, Any]:
        """Calculate profit vector for insurance product."""
        premium = random.randint(500, 2000)
        expense_ratio = round(random.uniform(0.15, 0.30), 3)
        mortality_assumption = round(random.uniform(0.001, 0.01), 4)
        interest_rate = round(random.uniform(0.03, 0.05), 4)
        v = 1 / (1 + interest_rate)
        benefit = random.randint(50000, 200000)
        policy_year = random.randint(1, 10)

        # Profit = Premium - Expense - Mortality Cost
        expense = premium * expense_ratio
        mortality_cost = benefit * mortality_assumption
        profit = premium - expense - mortality_cost

        # Discounted profit
        pv_profit = profit * (v ** policy_year)

        answer = round(pv_profit, 2)
        distractors = [
            round(profit, 2),
            round(premium - benefit * (v ** policy_year), 2),
            round(pv_profit * 1.25, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "Profit Vector",
            "difficulty": random.randint(7, 8),
            "question_text": f"Year {policy_year}: Premium ${premium}, expenses {int(expense_ratio*100)}%, mortality ${benefit}×{mortality_assumption}, i={interest_rate}. PV Profit?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Profit = Premium - Expense - Mortality Cost = ${premium} - ${expense} - ${mortality_cost} = ${profit}. Discounted to Year 0: ${answer}."
        }

    @classmethod
    def profit_signature(cls) -> Dict[str, Any]:
        """Analyze profit signature (cumulative profit over policy life)."""
        year_profits = [round(random.uniform(-500, 1000), 2) for _ in range(5)]
        interest_rate = round(random.uniform(0.03, 0.05), 4)
        v = 1 / (1 + interest_rate)

        # PV of all profits
        pv_total = sum(year_profits[t] * (v ** (t+1)) for t in range(len(year_profits)))

        answer = round(pv_total, 2)
        distractors = [
            round(sum(year_profits), 2),
            round(sum(year_profits) * v ** 3, 2),
            round(answer * 0.9, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "Profit Signature",
            "difficulty": random.randint(7, 8),
            "question_text": f"Yearly profits: {year_profits}, i={interest_rate}. Total PV of profits?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"PV = Σ Year_Profit_t · v^t = ${answer}. Cumulative profit analysis."
        }

    @classmethod
    def npv_of_profits(cls) -> Dict[str, Any]:
        """Calculate net present value of policy profits."""
        annual_profit = random.randint(100, 500)
        policy_duration = random.randint(10, 20)
        discount_rate = round(random.uniform(0.06, 0.12), 4)
        v = 1 / (1 + discount_rate)

        npv = sum(annual_profit * (v ** t) for t in range(1, policy_duration + 1))

        answer = round(npv, 2)
        distractors = [
            round(annual_profit * policy_duration, 2),
            round(annual_profit * policy_duration * v ** (policy_duration/2), 2),
            round(answer * 0.8, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "NPV of Profits",
            "difficulty": random.randint(6, 7),
            "question_text": f"Annual profit ${annual_profit}, duration {policy_duration} years, discount rate {discount_rate}. NPV?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"NPV = Σ Annual_Profit · v^t = ${answer}."
        }

    @classmethod
    def irr_on_profit(cls) -> Dict[str, Any]:
        """Calculate IRR (Internal Rate of Return) on policy profits."""
        initial_investment = -random.randint(10000, 50000)
        annual_profit = random.randint(500, 2000)
        duration = random.randint(10, 20)

        # IRR where NPV = 0: initial + Σ annual_profit / (1+IRR)^t = 0
        # Approximate solution
        irr_approx = (annual_profit * duration + abs(initial_investment)) / (duration * initial_investment)
        irr_approx = max(0.01, min(0.20, abs(irr_approx)))  # Bound to reasonable range

        # More accurate: Newton-Raphson or approximation
        irr_estimate = annual_profit / abs(initial_investment) * (duration / (duration + 1))
        irr_estimate = round(irr_estimate, 4)

        answer = irr_estimate
        distractors = [
            round(annual_profit / abs(initial_investment), 4),
            round(annual_profit / (abs(initial_investment) * duration), 4),
            round(answer * 1.3, 4)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "IRR on Profit",
            "difficulty": random.randint(7, 8),
            "question_text": f"Initial investment ${abs(initial_investment)}, annual profit ${annual_profit}, {duration} years. IRR?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"IRR ≈ Annual_Profit / Investment × Duration_Factor = {answer} or {int(answer*100)}%."
        }

    @classmethod
    def asset_share_recursion(cls) -> Dict[str, Any]:
        """Calculate asset share using recursive formula."""
        premium = random.randint(1000, 3000)
        expense_ratio = round(random.uniform(0.10, 0.25), 3)
        interest_rate = round(random.uniform(0.03, 0.05), 4)
        mortality_rate = round(random.uniform(0.001, 0.02), 4)
        benefit = random.randint(50000, 150000)
        year = random.randint(2, 5)

        # Asset Share: AS_t = (AS_{t-1} + Premium - Expense) × (1+i) - Mortality Cost
        as_prev = random.randint(5000, 20000)
        expense = premium * expense_ratio
        asset_share = (as_prev + premium - expense) * (1 + interest_rate) - benefit * mortality_rate

        answer = round(asset_share, 2)
        distractors = [
            round((as_prev + premium) * (1 + interest_rate), 2),
            round(as_prev + premium - expense, 2),
            round(answer * 1.1, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "Asset Share Recursion",
            "difficulty": random.randint(7, 8),
            "question_text": f"Year {year}: AS_prev ${as_prev}, premium ${premium}, expense {int(expense_ratio*100)}%, i={interest_rate}, mortality ${benefit}×{mortality_rate}. AS_t?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"AS_t = (AS_(t-1) + Prem - Exp) · (1+i) - Mortality = (${as_prev} + ${premium} - ${expense}) × {1+interest_rate} - ${benefit*mortality_rate} = ${answer}."
        }

    @classmethod
    def reserves_vs_asset_shares(cls) -> Dict[str, Any]:
        """Compare reserves versus asset shares."""
        reserve = random.randint(5000, 30000)
        asset_share = random.randint(3000, 25000)

        # Profit from difference
        profit = asset_share - reserve

        answer = round(profit, 2)
        distractors = [
            round(reserve, 2),
            round(asset_share, 2),
            round((reserve + asset_share) / 2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "Reserves vs Asset Shares",
            "difficulty": random.randint(5, 6),
            "question_text": f"Reserve ${reserve}, asset share ${asset_share}. Profit from difference?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Profit = Asset Share - Reserve = ${asset_share} - ${reserve} = ${answer}."
        }

    @classmethod
    def universal_life_account_value(cls) -> Dict[str, Any]:
        """Calculate Universal Life account value with cost of insurance charges."""
        prior_av = random.randint(10000, 50000)
        premium = random.randint(500, 2000)
        monthly_coi = round(random.uniform(0.0005, 0.002), 4)
        monthly_expenses = random.randint(5, 25)
        monthly_interest = round(random.uniform(0.002, 0.005), 4)
        months = 12

        # AV_new = (AV_old + Premium - COI - Expenses) × (1 + monthly_interest)
        av = prior_av
        for month in range(months):
            coi_charge = av * monthly_coi
            av = (av + premium/12 - coi_charge - monthly_expenses) * (1 + monthly_interest)

        answer = round(av, 2)
        distractors = [
            round(prior_av + premium, 2),
            round(prior_av * (1 + monthly_interest*12), 2),
            round(answer * 0.9, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "UL Account Value",
            "difficulty": random.randint(6, 7),
            "question_text": f"UL AV: prior ${prior_av}, annual premium ${premium}, monthly COI {monthly_coi}, monthly i={monthly_interest}. Year-end AV?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Monthly: AV = (AV + Prem/12 - COI - Exp) × (1+i_m). After 12 months: ${answer}."
        }

    @classmethod
    def ul_cost_of_insurance(cls) -> Dict[str, Any]:
        """Calculate monthly cost of insurance charge for Universal Life."""
        face_amount = random.randint(100000, 500000)
        account_value = random.randint(20000, 100000)
        monthly_coi_rate = round(random.uniform(0.0003, 0.001), 5)

        # COI = (Face - AV) × monthly_COI_rate
        coi_charge = (face_amount - account_value) * monthly_coi_rate

        answer = round(coi_charge, 2)
        distractors = [
            round(face_amount * monthly_coi_rate, 2),
            round(account_value * monthly_coi_rate, 2),
            round(answer * 1.2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "UL Cost of Insurance",
            "difficulty": random.randint(5, 6),
            "question_text": f"UL COI: face ${face_amount}, AV ${account_value}, rate {monthly_coi_rate}. Monthly charge?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"COI = (Face - AV) × Rate = (${face_amount} - ${account_value}) × {monthly_coi_rate} = ${answer}."
        }

    @classmethod
    def variable_annuity_guarantee(cls) -> Dict[str, Any]:
        """Calculate guaranteed minimum value for variable annuity."""
        purchase_payments = random.randint(100000, 500000)
        guarantee_level = round(random.uniform(0.85, 1.05), 2)
        current_account_value = random.randint(60000, 400000)

        # Guaranteed minimum = purchase_payments × guarantee_level
        gmab = purchase_payments * guarantee_level

        # Net guarantee obligation
        obligation = max(0, gmab - current_account_value)

        answer = round(obligation, 2)
        distractors = [
            round(gmab, 2),
            round(current_account_value, 2),
            round(purchase_payments, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "Variable Annuity Guarantee",
            "difficulty": random.randint(6, 7),
            "question_text": f"VA GMAB: purchases ${purchase_payments}, guarantee {int(guarantee_level*100)}%, current value ${current_account_value}. Obligation?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Obligation = max(0, Purchase × {guarantee_level} - Current Value) = ${answer}."
        }

    @classmethod
    def participating_insurance_dividend(cls) -> Dict[str, Any]:
        """Calculate dividend distribution in participating insurance."""
        mortality_surplus = random.randint(1000, 5000)
        expense_surplus = random.randint(500, 2000)
        investment_surplus = random.randint(2000, 8000)
        dividend_percentage = round(random.uniform(0.70, 0.90), 2)

        # Total surplus
        total_surplus = mortality_surplus + expense_surplus + investment_surplus

        # Dividend to policyholders
        dividend = total_surplus * dividend_percentage

        answer = round(dividend, 2)
        distractors = [
            round(total_surplus, 2),
            round(dividend * 0.8, 2),
            round(investment_surplus, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "Participating Dividend",
            "difficulty": random.randint(6, 7),
            "question_text": f"Participat. insurance: mortality surplus ${mortality_surplus}, expense ${expense_surplus}, investment ${investment_surplus}, dividend rate {int(dividend_percentage*100)}%. Dividend?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Dividend = (Mortality + Expense + Investment Surplus) × {dividend_percentage} = ${answer}."
        }

    @classmethod
    def cash_value_calculation(cls) -> Dict[str, Any]:
        """Calculate policy cash value."""
        reserve = random.randint(10000, 50000)
        surrender_charge_rate = round(random.uniform(0.05, 0.20), 3)
        policy_year = random.randint(1, 15)

        # Surrender charge decreases with duration
        surrender_charge = reserve * surrender_charge_rate * max(0, (1 - policy_year/20))

        cash_value = reserve - surrender_charge

        answer = round(cash_value, 2)
        distractors = [
            round(reserve, 2),
            round(reserve * (1 - surrender_charge_rate), 2),
            round(answer * 1.1, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "Cash Value",
            "difficulty": random.randint(5, 6),
            "question_text": f"Policy year {policy_year}: reserve ${reserve}, surrender charge rate {int(surrender_charge_rate*100)}%. Cash value?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Cash Value = Reserve - Surrender Charge = ${reserve} - ${surrender_charge} = ${answer}."
        }

    @classmethod
    def surrender_charge(cls) -> Dict[str, Any]:
        """Calculate surrender charge for policy surrendered early."""
        reserve = random.randint(15000, 60000)
        charge_rate_year1 = round(random.uniform(0.10, 0.25), 3)
        year_of_surrender = random.randint(1, 10)
        charge_declining_rate = round(random.uniform(0.02, 0.05), 3)

        # Charge declining by rate per year
        charge_rate = max(0, charge_rate_year1 - charge_declining_rate * (year_of_surrender - 1))
        surrender_charge = reserve * charge_rate

        answer = round(surrender_charge, 2)
        distractors = [
            round(reserve * charge_rate_year1, 2),
            round(reserve * charge_declining_rate * year_of_surrender, 2),
            round(answer * 1.3, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "Surrender Charge",
            "difficulty": random.randint(5, 6),
            "question_text": f"Surrender year {year_of_surrender}: reserve ${reserve}, year 1 charge {int(charge_rate_year1*100)}%, declining {int(charge_declining_rate*100)}%/year. Charge?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Surrender Charge = Reserve × [Year1_Rate - Decline_Rate × (t-1)] = ${answer}."
        }

    @classmethod
    def nonforfeiture_benefits(cls) -> Dict[str, Any]:
        """Calculate nonforfeiture benefits (extended term or reduced paid-up)."""
        death_benefit = random.randint(100000, 300000)
        reserve = random.randint(15000, 80000)
        term_insurance_rate = round(random.uniform(0.001, 0.02), 4)

        # Extended term: find t such that reserve = death_benefit × term insurance factor
        # Approximation: t ≈ reserve / (death_benefit × term_rate)
        extended_years = max(0, reserve / (death_benefit * term_insurance_rate))

        answer = round(extended_years, 1)
        distractors = [
            round(extended_years * 0.7, 1),
            round(reserve / death_benefit, 1),
            round(extended_years * 1.4, 1)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "Nonforfeiture Benefits",
            "difficulty": random.randint(6, 7),
            "question_text": f"Nonforfeiture: death benefit ${death_benefit}, reserve ${reserve}, term rate {term_insurance_rate}. Extended term years?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Extended term t ≈ Reserve / (Benefit × Term_Rate) ≈ {answer} years."
        }

    @classmethod
    def policy_alteration(cls) -> Dict[str, Any]:
        """Calculate impact of policy alteration on reserve and cost."""
        original_benefit = random.randint(100000, 200000)
        original_reserve = random.randint(10000, 50000)
        new_benefit = round(original_benefit * random.uniform(0.8, 1.2), 0)
        interest_rate = round(random.uniform(0.03, 0.05), 4)

        # Reserve scales proportionally with benefit (simplified)
        new_reserve = original_reserve * (new_benefit / original_benefit)

        # Change in reserve
        reserve_change = new_reserve - original_reserve

        answer = round(reserve_change, 2)
        distractors = [
            round(new_reserve, 2),
            round(original_reserve, 2),
            round(reserve_change * 1.2, 2)
        ]

        choices = [answer] + distractors
        random.shuffle(choices)

        return {
            "id": cls.generate_question_id(),
            "exam": "ALTAM",
            "topic": "Profit Testing & Advanced",
            "subtopic": "Policy Alteration",
            "difficulty": random.randint(5, 6),
            "question_text": f"Alteration: original benefit ${original_benefit}, reserve ${original_reserve}, new benefit ${int(new_benefit)}. Change in reserve?",
            "choices": [str(c) for c in choices],
            "solution": str(answer),
            "explanation": f"Reserve change = (New Benefit / Original) × Original Reserve - Original = ${answer}."
        }

    # ==================== CLASS-LEVEL METHODS ====================

    @classmethod
    def get_all_methods(cls) -> List[str]:
        """Return list of all question generation methods."""
        methods = [
            # Multi-State Models
            'two_state_alive_dead_transition',
            'three_state_healthy_sick_dead',
            'kolmogorov_forward_equation',
            'transition_probability_matrix',
            'multi_state_premium',
            'multi_state_reserve',
            'permanent_disability_model',
            'disability_income_insurance',
            'accidental_death_model',
            'critical_illness_model',
            # Multiple Life
            'joint_life_status_probability',
            'last_survivor_probability',
            'joint_life_annuity',
            'last_survivor_annuity',
            'joint_life_insurance',
            'last_survivor_insurance',
            'contingent_insurance',
            'reversionary_annuity',
            'common_shock_model',
            'independent_lives_joint',
            # Multiple Decrement
            'double_decrement_probability',
            'triple_decrement_model',
            'associated_single_decrement',
            'udd_in_multiple_decrement',
            'service_table_calculation',
            'multiple_decrement_insurance',
            'cause_specific_force',
            'dependent_vs_independent_rates',
            # Pension
            'pension_benefit_formula',
            'pension_pv_future_benefits',
            'pension_normal_cost',
            'pension_accrued_liability',
            'replacement_ratio',
            'salary_scale_projection',
            'pension_with_withdrawal',
            'early_retirement_benefit',
            # Profit Testing & Advanced
            'profit_vector_calculation',
            'profit_signature',
            'npv_of_profits',
            'irr_on_profit',
            'asset_share_recursion',
            'reserves_vs_asset_shares',
            'universal_life_account_value',
            'ul_cost_of_insurance',
            'variable_annuity_guarantee',
            'participating_insurance_dividend',
            'cash_value_calculation',
            'surrender_charge',
            'nonforfeiture_benefits',
            'policy_alteration'
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
    sample_questions = ExamALTAMGenerator.generate_all(n_per_method=1)
    print(f"Generated {len(sample_questions)} sample ALTAM questions")
    print(f"Total methods: {len(ExamALTAMGenerator.get_all_methods())}")
    print("\nSample question:")
    print(sample_questions[0])
