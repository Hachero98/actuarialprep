import random
import math
from typing import Dict, List, Any


class ExamFAMGenerator:
    """
    Generator for SOA Exam FAM (Fundamentals of Actuarial Mathematics) Long-Term questions.
    Produces questions on survival models, insurance products, annuities, premiums, and reserves.
    """

    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
        self.exam = "FAM"
        self.topic_map = {
            "survival": "Survival Models",
            "insurance": "Insurance Products",
            "annuity": "Annuities",
            "premium": "Premiums",
            "reserve": "Reserves"
        }

    def format_number(self, value: float, decimals: int = 4) -> str:
        """Format a number to a string with specified decimal places."""
        return f"{value:.{decimals}f}"

    def make_choices(self, correct: float, distractors: List[float]) -> List[Dict[str, Any]]:
        """
        Create a 5-choice multiple choice structure.

        Args:
            correct: The correct answer value
            distractors: List of 4 distractor values

        Returns:
            List of 5 choice dicts with label, text, is_correct
        """
        choices_list = [
            {"value": correct, "is_correct": True},
            {"value": distractors[0], "is_correct": False},
            {"value": distractors[1], "is_correct": False},
            {"value": distractors[2], "is_correct": False},
            {"value": distractors[3], "is_correct": False},
        ]
        random.shuffle(choices_list)

        for i, choice in enumerate(choices_list):
            choice["label"] = chr(65 + i)  # A, B, C, D, E
            choice["text"] = self.format_number(choice["value"])

        return choices_list

    # ======================== SURVIVAL MODELS (10 methods) ========================

    def constant_force_survival(self) -> Dict[str, Any]:
        """
        Constant force of mortality: Given mu and t, find t_p_x = e^(-mu*t)
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        t = random.randint(5, 25)

        answer = math.exp(-mu * t)

        d1 = math.exp(-mu * t * 0.8)
        d2 = math.exp(-mu * t * 1.2)
        d3 = 1 - (mu * t)
        d4 = math.exp(-mu * (t + 2))

        return {
            "id": "fam_001",
            "exam": self.exam,
            "topic": self.topic_map["survival"],
            "subtopic": "Constant Force of Mortality",
            "difficulty": "Easy",
            "question_text": f"Under a constant force of mortality, mu = {mu}, what is {t}p_x (the probability that (x) survives t = {t} years)?",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"{t}p_x = e^(-{mu}*{t}) = e^({-mu*t}) = {answer}",
            "explanation": "Under constant force, the survival function is S(t) = e^(-mu*t). This is a fundamental result for exponential survival times."
        }

    def force_from_survival(self) -> Dict[str, Any]:
        """
        Given S(x) = (1 - x/w)^a (uniform mortality distribution), find mu(x) = a/(w-x)
        """
        w = random.randint(80, 110)
        a = round(random.uniform(0.5, 2.0), 2)
        x = random.randint(30, 60)

        answer = a / (w - x)

        d1 = a / (w - x + 5)
        d2 = (a + 1) / (w - x)
        d3 = a / w
        d4 = math.log(a) / (w - x)

        return {
            "id": "fam_002",
            "exam": self.exam,
            "topic": self.topic_map["survival"],
            "subtopic": "Force of Mortality from Survival Function",
            "difficulty": "Medium",
            "question_text": f"Given S(x) = (1 - x/{w})^{a}, find the force of mortality mu({x}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"mu(x) = -S'(x)/S(x). With S(x) = (1-x/w)^a, we have mu(x) = {a}/({w}-{x}) = {answer}",
            "explanation": "The force of mortality is the negative derivative of the log survival function: mu(x) = -d/dx[ln S(x)]."
        }

    def de_moivre_survival(self) -> Dict[str, Any]:
        """
        De Moivre's law: S(x) = (w-x)/w, find n_p_x = (w-x-n)/(w-x)
        """
        w = random.randint(80, 110)
        x = random.randint(20, 60)
        n = random.randint(5, min(20, w - x - 1))

        answer = (w - x - n) / (w - x)

        d1 = (w - x - n) / w
        d2 = (w - x - n) / (w - x + 1)
        d3 = (w - x) / (w - x - n)
        d4 = n / (w - x)

        return {
            "id": "fam_003",
            "exam": self.exam,
            "topic": self.topic_map["survival"],
            "subtopic": "De Moivre's Law",
            "difficulty": "Easy",
            "question_text": f"Under De Moivre's law with omega = {w}, find the probability that a life aged {x} survives {n} years.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"{n}p_{x} = ({w}-{x}-{n})/({w}-{x}) = {w-x-n}/{w-x} = {answer}",
            "explanation": "De Moivre's law assumes a uniform distribution of deaths between age 0 and omega. The survival probability is simply the ratio of remaining years."
        }

    def gompertz_mortality(self) -> Dict[str, Any]:
        """
        Gompertz force: mu(x) = B*c^x
        Find t_p_x = exp(-B*c^x*(c^t - 1)/ln(c))
        """
        B = round(random.uniform(0.0001, 0.0005), 5)
        c = round(random.uniform(1.06, 1.11), 4)
        x = random.randint(30, 60)
        t = random.randint(1, 5)

        ln_c = math.log(c)
        answer = math.exp(-B * (c ** x) * ((c ** t) - 1) / ln_c)

        d1 = math.exp(-B * (c ** (x + t)))
        d2 = math.exp(-B * c ** x * t)
        d3 = (c ** (-x * t))
        d4 = math.exp(-B * (c ** x) * (c ** t) / ln_c)

        return {
            "id": "fam_004",
            "exam": self.exam,
            "topic": self.topic_map["survival"],
            "subtopic": "Gompertz Mortality",
            "difficulty": "Hard",
            "question_text": f"Under Gompertz mortality with B = {B}, c = {c}, find {t}p_{x} for age {x}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"{t}p_{x} = exp(-B*c^x*(c^t-1)/ln(c)) = exp(-{B}*{c**x:.6f}*{(c**t - 1)/ln_c:.6f}) = {answer}",
            "explanation": "Gompertz assumes force of mortality mu(x) = B*c^x. The survival probability integrates this force over time."
        }

    def curtate_lifetime_expectation(self) -> Dict[str, Any]:
        """
        Curtate lifetime expectation: E[K] = sum_{k=1}^{omega-x} k_p_x
        Given 4 survival probabilities, compute the sum.
        """
        q_values = [round(random.uniform(0.01, 0.3), 3) for _ in range(4)]
        p_values = [1 - q for q in q_values]

        expectation = 0
        cumulative_p = 1
        for i, p in enumerate(p_values):
            cumulative_p *= p
            expectation += cumulative_p

        d1 = expectation * 0.9
        d2 = expectation * 1.1
        d3 = sum(p_values)
        d4 = len(p_values) / sum(q_values)

        return {
            "id": "fam_005",
            "exam": self.exam,
            "topic": self.topic_map["survival"],
            "subtopic": "Curtate Lifetime Expectation",
            "difficulty": "Medium",
            "question_text": f"Given survival probabilities q_x = {q_values[0]}, q_{{x+1}} = {q_values[1]}, q_{{x+2}} = {q_values[2]}, q_{{x+3}} = {q_values[3]}, compute E[K_x].",
            "choices": self.make_choices(expectation, [d1, d2, d3, d4]),
            "solution": f"E[K] = sum of k_p_x values: {' + '.join([f'{p:.3f}' for p in p_values])} = {expectation}",
            "explanation": "The curtate lifetime K is the integer part of the complete lifetime T. Its expectation is the sum of all survival probabilities."
        }

    def complete_lifetime_constant(self) -> Dict[str, Any]:
        """
        Complete lifetime expectation under constant force: e_x = 1/mu
        """
        mu = round(random.uniform(0.02, 0.08), 4)

        answer = 1 / mu

        d1 = 1 / (2 * mu)
        d2 = math.log(1 / mu)
        d3 = mu
        d4 = math.sqrt(1 / mu)

        return {
            "id": "fam_006",
            "exam": self.exam,
            "topic": self.topic_map["survival"],
            "subtopic": "Complete Lifetime Expectation",
            "difficulty": "Easy",
            "question_text": f"Under constant force of mortality mu = {mu}, find the complete lifetime expectation e_x.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"e_x = integral from 0 to infinity of t_p_x dt = integral of e^(-mu*t) dt = 1/mu = 1/{mu} = {answer}",
            "explanation": "For exponential survival, the mean lifetime is the reciprocal of the force parameter."
        }

    def deferred_mortality(self) -> Dict[str, Any]:
        """
        Deferred mortality probability: s|t_q_x = probability of death between s and s+t
        = e^(-mu*s) - e^(-mu*(s+t)) under constant force
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        s = random.randint(5, 15)
        t = random.randint(1, 10)

        answer = math.exp(-mu * s) - math.exp(-mu * (s + t))

        d1 = math.exp(-mu * t)
        d2 = math.exp(-mu * (s + t))
        d3 = (1 - math.exp(-mu * t)) * math.exp(-mu * s)
        d4 = math.exp(-mu * s) / math.exp(-mu * t)

        return {
            "id": "fam_007",
            "exam": self.exam,
            "topic": self.topic_map["survival"],
            "subtopic": "Deferred Mortality",
            "difficulty": "Medium",
            "question_text": f"Under constant force mu = {mu}, find {s}|{t}q_x (probability that (x) survives {s} years but dies in the next {t} years).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"{s}|{t}q_x = e^(-mu*{s}) - e^(-mu*{s+t}) = {math.exp(-mu*s):.4f} - {math.exp(-mu*(s+t)):.4f} = {answer}",
            "explanation": "The deferred probability is the difference of two survival probabilities: the probability of surviving s years minus the probability of surviving s+t years."
        }

    def life_table_calculations(self) -> Dict[str, Any]:
        """
        Given l_x values at 3 ages, compute q_x and other life table quantities.
        """
        l_base = 100000
        l_x = l_base
        l_x1 = int(l_base * random.uniform(0.95, 0.99))
        l_x2 = int(l_x1 * random.uniform(0.95, 0.99))

        q_x = (l_x - l_x1) / l_x
        d_x = l_x - l_x1
        p_x = l_x1 / l_x

        d1 = q_x * 1.1
        d2 = d_x / l_x1
        d3 = p_x / 2
        d4 = (l_x - l_x2) / l_x

        return {
            "id": "fam_008",
            "exam": self.exam,
            "topic": self.topic_map["survival"],
            "subtopic": "Life Table Calculations",
            "difficulty": "Easy",
            "question_text": f"Given l_x = {l_x}, l_{{x+1}} = {l_x1}, l_{{x+2}} = {l_x2}, compute q_x.",
            "choices": self.make_choices(q_x, [d1, d2, d3, d4]),
            "solution": f"q_x = (l_x - l_{{x+1}}) / l_x = ({l_x} - {l_x1}) / {l_x} = {d_x}/{l_x} = {q_x}",
            "explanation": "The probability of death in the life table is the ratio of deaths (l_x - l_{x+1}) to the number at the start of the year."
        }

    def fractional_age_UDD(self) -> Dict[str, Any]:
        """
        Uniform distribution of deaths (UDD) assumption: t_q_x = t*q_x for t in (0,1)
        """
        q_x = round(random.uniform(0.01, 0.15), 4)
        t = round(random.uniform(0.1, 0.9), 2)

        answer = t * q_x

        d1 = q_x * (1 - t)
        d2 = q_x / t
        d3 = (q_x ** t)
        d4 = q_x * (1 + t)

        return {
            "id": "fam_009",
            "exam": self.exam,
            "topic": self.topic_map["survival"],
            "subtopic": "Fractional Age - UDD",
            "difficulty": "Easy",
            "question_text": f"Under UDD, with q_x = {q_x}, find {t}q_x.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"{t}q_x = {t} * q_x = {t} * {q_x} = {answer}",
            "explanation": "Under the uniform distribution of deaths assumption, the probability of death is proportional to the fraction of the year."
        }

    def makeham_force(self) -> Dict[str, Any]:
        """
        Makeham force: mu(x) = A + B*c^x
        Compute 1_p_x = exp(-(A + B*c^x))
        """
        A = round(random.uniform(0.001, 0.005), 5)
        B = round(random.uniform(0.0001, 0.0005), 5)
        c = round(random.uniform(1.06, 1.10), 4)
        x = random.randint(30, 60)

        mu_x = A + B * (c ** x)
        answer = math.exp(-mu_x)

        d1 = math.exp(-A - B * (c ** (x - 1)))
        d2 = math.exp(-A * c ** x)
        d3 = math.exp(-(A + B) * c ** x)
        d4 = 1 - mu_x

        return {
            "id": "fam_010",
            "exam": self.exam,
            "topic": self.topic_map["survival"],
            "subtopic": "Makeham Force of Mortality",
            "difficulty": "Hard",
            "question_text": f"Under Makeham mortality with A = {A}, B = {B}, c = {c}, find 1p_{x} at age {x}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"mu({x}) = {A} + {B}*{c}^{x} = {mu_x:.6f}. Thus 1p_{x} = e^(-{mu_x:.6f}) = {answer}",
            "explanation": "Makeham force adds a constant (A) to Gompertz. This is a more realistic model for human mortality."
        }

    # ======================== INSURANCE PRODUCTS (8 methods) ========================

    def whole_life_APV_constant(self) -> Dict[str, Any]:
        """
        Whole life insurance, continuous, constant force: A_x = mu/(mu + delta)
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)

        answer = mu / (mu + delta)

        d1 = delta / (mu + delta)
        d2 = mu / delta
        d3 = (mu + delta) / mu
        d4 = mu / (2 * (mu + delta))

        return {
            "id": "fam_011",
            "exam": self.exam,
            "topic": self.topic_map["insurance"],
            "subtopic": "Whole Life APV - Continuous",
            "difficulty": "Medium",
            "question_text": f"Under constant force mu = {mu} and interest rate i = {i}, find the actuarial present value of a unit whole life insurance A_x.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"A_x = mu/(mu + delta) = {mu}/({mu} + {delta:.5f}) = {answer}",
            "explanation": "For continuous whole life insurance under constant force and constant interest, the APV is the ratio of force of mortality to the sum of mortality and interest forces."
        }

    def term_insurance_APV(self) -> Dict[str, Any]:
        """
        n-year term insurance, continuous, constant force: A^1_{x:n} = mu/(mu + delta) * (1 - e^(-(mu+delta)*n))
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)
        n = random.randint(5, 20)

        answer = (mu / (mu + delta)) * (1 - math.exp(-(mu + delta) * n))

        d1 = (mu / (mu + delta)) * (1 - math.exp(-mu * n))
        d2 = (mu / (mu + delta)) * (1 - math.exp(-delta * n))
        d3 = (1 - math.exp(-(mu + delta) * n))
        d4 = (mu / (mu + delta)) * math.exp(-(mu + delta) * n)

        return {
            "id": "fam_012",
            "exam": self.exam,
            "topic": self.topic_map["insurance"],
            "subtopic": "Term Life APV - Continuous",
            "difficulty": "Medium",
            "question_text": f"Under constant force mu = {mu}, interest i = {i}, find the APV of a {n}-year term insurance A^1_{{x:{n}}}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"A^1_{{x:{n}}} = (mu/(mu+delta))*(1 - e^(-(mu+delta)*{n})) = {answer}",
            "explanation": "Term insurance provides coverage only for n years. The APV is a whole life APV multiplied by the survival-adjusted discount factor."
        }

    def endowment_APV(self) -> Dict[str, Any]:
        """
        n-year endowment: A_{x:n} = A^1_{x:n} + n_E_x = A^1_{x:n} + e^(-(mu+delta)*n)
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)
        n = random.randint(5, 20)

        term_apv = (mu / (mu + delta)) * (1 - math.exp(-(mu + delta) * n))
        pure_endowment = math.exp(-(mu + delta) * n)
        answer = term_apv + pure_endowment

        d1 = term_apv
        d2 = pure_endowment
        d3 = (mu / (mu + delta)) * math.exp(-(mu + delta) * n)
        d4 = 1 - math.exp(-(mu + delta) * n)

        return {
            "id": "fam_013",
            "exam": self.exam,
            "topic": self.topic_map["insurance"],
            "subtopic": "Endowment APV",
            "difficulty": "Medium",
            "question_text": f"Find the APV of a {n}-year endowment insurance (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"A_{{x:{n}}} = A^1_{{x:{n}}} + n_E_x = {term_apv:.4f} + {pure_endowment:.4f} = {answer}",
            "explanation": "An endowment combines term insurance (pays if death before n) with pure endowment (pays if alive at n)."
        }

    def pure_endowment(self) -> Dict[str, Any]:
        """
        Pure endowment (survival benefit): nE_x = e^(-(mu+delta)*n)
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)
        n = random.randint(5, 20)

        answer = math.exp(-(mu + delta) * n)

        d1 = math.exp(-mu * n)
        d2 = math.exp(-delta * n)
        d3 = 1 - math.exp(-(mu + delta) * n)
        d4 = math.exp(-(mu + delta) * (n / 2))

        return {
            "id": "fam_014",
            "exam": self.exam,
            "topic": self.topic_map["insurance"],
            "subtopic": "Pure Endowment",
            "difficulty": "Easy",
            "question_text": f"Find the APV of a pure endowment of 1 payable in {n} years if (x) survives (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"n_E_x = e^(-(mu+delta)*{n}) = e^({-(mu+delta)*n:.4f}) = {answer}",
            "explanation": "A pure endowment is the expected present value of a unit payment if the individual survives n years."
        }

    def whole_life_discrete(self) -> Dict[str, Any]:
        """
        Whole life insurance (discrete): Ax = sum_{k=0}^{inf} v^{k+1} * k_p_x * q_{x+k}
        Given 3-4 values of q, compute approximately.
        """
        i = round(random.uniform(0.02, 0.08), 4)
        v = 1 / (1 + i)

        q_values = [round(random.uniform(0.01, 0.25), 4) for _ in range(4)]

        ax = 0
        p_cumulative = 1
        for k, q in enumerate(q_values):
            ax += (v ** (k + 1)) * p_cumulative * q
            p_cumulative *= (1 - q)

        d1 = ax * 0.9
        d2 = ax * 1.1
        d3 = sum([(v ** (k + 1)) * q_values[k] for k in range(len(q_values))])
        d4 = v * sum(q_values) / len(q_values)

        return {
            "id": "fam_015",
            "exam": self.exam,
            "topic": self.topic_map["insurance"],
            "subtopic": "Whole Life Insurance - Discrete",
            "difficulty": "Medium",
            "question_text": f"Given i = {i} and q_x = {q_values[0]}, q_{{x+1}} = {q_values[1]}, q_{{x+2}} = {q_values[2]}, q_{{x+3}} = {q_values[3]}, find A_x.",
            "choices": self.make_choices(ax, [d1, d2, d3, d4]),
            "solution": f"A_x = sum of v^(k+1) * k_p_x * q_(x+k) = {ax}",
            "explanation": "Discrete whole life insurance sums the present values of death benefits weighted by the probability of dying in each year."
        }

    def increasing_insurance(self) -> Dict[str, Any]:
        """
        Increasing insurance (discrete): (IA)_x = sum_{k=1}^{inf} k * v^k * k-1|q_x
        Benefit k at time k (or k+1 depending on convention).
        """
        i = round(random.uniform(0.02, 0.08), 4)
        v = 1 / (1 + i)

        q_values = [round(random.uniform(0.01, 0.25), 4) for _ in range(4)]

        ia = 0
        p_cumulative = 1
        for k in range(1, len(q_values) + 1):
            ia += k * (v ** k) * p_cumulative * q_values[k - 1]
            if k < len(q_values):
                p_cumulative *= (1 - q_values[k - 1])

        d1 = ia * 0.85
        d2 = ia * 1.15
        d3 = sum([(k) * (v ** k) * q_values[k - 1] for k in range(1, len(q_values) + 1)])
        d4 = (1 / (1 - v)) * (1 - (v ** len(q_values)))

        return {
            "id": "fam_016",
            "exam": self.exam,
            "topic": self.topic_map["insurance"],
            "subtopic": "Increasing Insurance",
            "difficulty": "Hard",
            "question_text": f"Find the APV of increasing insurance (IA)_x where benefit = k at time k, given i = {i} and mortality rates {q_values}.",
            "choices": self.make_choices(ia, [d1, d2, d3, d4]),
            "solution": f"(IA)_x = sum k*v^k*k-1|q_x = {ia}",
            "explanation": "Increasing insurance pays more in later years. The APV weights each payment by its discount factor and probability of death."
        }

    def insurance_variance(self) -> Dict[str, Any]:
        """
        Variance of insurance benefit: Var(Z) = E[Z^2] - (E[Z])^2 = 2A_x - (A_x)^2
        where 2A_x uses force 2*delta instead of delta.
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)

        ax = mu / (mu + delta)
        two_ax = mu / (mu + 2 * delta)

        answer = two_ax - (ax ** 2)

        d1 = ax - (ax ** 2)
        d2 = 2 * (ax ** 2)
        d3 = two_ax * (1 - ax)
        d4 = ax * two_ax

        return {
            "id": "fam_017",
            "exam": self.exam,
            "topic": self.topic_map["insurance"],
            "subtopic": "Insurance Variance",
            "difficulty": "Hard",
            "question_text": f"Given A_x = {ax:.4f} (with mu = {mu}, i = {i}), find Var(Z) where Z is the present value of benefit.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"Var(Z) = 2A_x - (A_x)^2 = {two_ax:.4f} - {ax**2:.4f} = {answer}",
            "explanation": "Variance measures the dispersion of the insurance benefit around its mean. It uses the second moment (2A) minus the squared mean."
        }

    def insurance_recursion(self) -> Dict[str, Any]:
        """
        Insurance recursion: A_x = v*q_x + v*p_x*A_{x+1}
        Given A_{x+1}, q_x, i, solve for A_x.
        """
        i = round(random.uniform(0.02, 0.08), 4)
        v = 1 / (1 + i)

        q_x = round(random.uniform(0.01, 0.15), 4)
        a_x1 = round(random.uniform(0.1, 0.5), 4)

        answer = v * q_x + v * (1 - q_x) * a_x1

        d1 = q_x + (1 - q_x) * a_x1
        d2 = v * (q_x + a_x1)
        d3 = (q_x + a_x1) / (1 + i)
        d4 = q_x / v + a_x1

        return {
            "id": "fam_018",
            "exam": self.exam,
            "topic": self.topic_map["insurance"],
            "subtopic": "Insurance Recursion",
            "difficulty": "Medium",
            "question_text": f"Given A_{{x+1}} = {a_x1}, q_x = {q_x}, and i = {i}, find A_x using the recursion formula.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"A_x = v*q_x + v*p_x*A_{{x+1}} = {v:.4f}*{q_x} + {v:.4f}*{1-q_x}*{a_x1} = {answer}",
            "explanation": "Insurance APVs satisfy a recursion: the value today is the discounted expected value of next year's outcome."
        }

    # ======================== ANNUITIES (7 methods) ========================

    def whole_life_annuity_due(self) -> Dict[str, Any]:
        """
        Whole life annuity due (continuous): a_x = (1 - A_x) / delta
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)

        ax_insurance = mu / (mu + delta)
        answer = (1 - ax_insurance) / delta

        d1 = (1 - ax_insurance) / (mu + delta)
        d2 = ax_insurance / delta
        d3 = 1 / delta - ax_insurance
        d4 = (1 + mu) / delta

        return {
            "id": "fam_019",
            "exam": self.exam,
            "topic": self.topic_map["annuity"],
            "subtopic": "Whole Life Annuity Due",
            "difficulty": "Medium",
            "question_text": f"Find the APV of a continuous whole life annuity due (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"a_x = (1 - A_x) / delta = (1 - {ax_insurance:.4f}) / {delta:.4f} = {answer}",
            "explanation": "The annuity-insurance relation: an annuity plus its corresponding insurance equals a pure endowment of 1/delta."
        }

    def temp_life_annuity(self) -> Dict[str, Any]:
        """
        Temporary life annuity (continuous): a_{x:n} = (1 - A^1_{x:n} - n_E_x) / delta
        or equivalently: integral from 0 to n of e^(-delta*t) * t_p_x dt
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)
        n = random.randint(5, 20)

        term_insur = (mu / (mu + delta)) * (1 - math.exp(-(mu + delta) * n))
        pure_endow = math.exp(-(mu + delta) * n)
        answer = (1 - term_insur - pure_endow) / delta

        d1 = (1 - pure_endow) / delta
        d2 = (mu / (mu + delta)) / delta
        d3 = (1 - term_insur) / delta
        d4 = n / delta

        return {
            "id": "fam_020",
            "exam": self.exam,
            "topic": self.topic_map["annuity"],
            "subtopic": "Temporary Life Annuity",
            "difficulty": "Medium",
            "question_text": f"Find the APV of a {n}-year temporary life annuity (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"a_{{x:{n}}} = (1 - A^1_{{x:{n}}} - {n}_E_x) / delta = {answer}",
            "explanation": "A temporary annuity stops paying if the individual dies or after n years."
        }

    def deferred_annuity(self) -> Dict[str, Any]:
        """
        Deferred annuity: n|a_x = n_E_x * a_{x+n}
        Using constant force: a_x = 1/(mu + delta)
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)
        n = random.randint(5, 20)

        pure_endow = math.exp(-(mu + delta) * n)
        annuity_deferred = pure_endow / (mu + delta)
        answer = annuity_deferred

        d1 = pure_endow / mu
        d2 = 1 / (mu + delta)
        d3 = pure_endow * mu / (mu + delta)
        d4 = pure_endow * delta / (mu + delta)

        return {
            "id": "fam_021",
            "exam": self.exam,
            "topic": self.topic_map["annuity"],
            "subtopic": "Deferred Annuity",
            "difficulty": "Medium",
            "question_text": f"Find the APV of an annuity deferred {n} years (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"n|a_x = n_E_x * a_{{x+n}} = e^(-(mu+delta)*{n}) * 1/(mu+delta) = {answer}",
            "explanation": "A deferred annuity starts payments only if the individual survives n years."
        }

    def continuous_annuity(self) -> Dict[str, Any]:
        """
        Continuous annuity (whole life): a_x = 1 / (mu + delta)
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)

        answer = 1 / (mu + delta)

        d1 = mu / (mu + delta)
        d2 = delta / (mu + delta)
        d3 = 1 / mu
        d4 = (mu + delta)

        return {
            "id": "fam_022",
            "exam": self.exam,
            "topic": self.topic_map["annuity"],
            "subtopic": "Continuous Annuity",
            "difficulty": "Easy",
            "question_text": f"Find the APV of a continuous whole life annuity of 1 per unit time (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"a_x = 1/(mu + delta) = 1/({mu} + {delta:.4f}) = {answer}",
            "explanation": "A continuous annuity pays 1 per unit time continuously until death. It's the reciprocal of the sum of mortality and interest forces."
        }

    def annuity_insurance_relation(self) -> Dict[str, Any]:
        """
        Fundamental relation: A_x + d*a_x = 1 (continuous)
        or A_x = 1 - d*a_x
        Rearrange: a_x = (1 - A_x) / d
        """
        i = round(random.uniform(0.02, 0.08), 4)
        d = i / (1 + i)

        ax_insur = round(random.uniform(0.1, 0.5), 4)

        answer = (1 - ax_insur) / d

        d1 = (1 - ax_insur) / i
        d2 = ax_insur / d
        d3 = (ax_insur - 1) / d
        d4 = 1 / d - ax_insur

        return {
            "id": "fam_023",
            "exam": self.exam,
            "topic": self.topic_map["annuity"],
            "subtopic": "Annuity-Insurance Relation",
            "difficulty": "Easy",
            "question_text": f"Given A_x = {ax_insur} and i = {i}, find a_x using the fundamental relation.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"a_x = (1 - A_x)/d = (1 - {ax_insur})/{d:.4f} = {answer}",
            "explanation": "The annuity-insurance relation links these two products: A_x + d*a_x = 1."
        }

    def certain_and_life(self) -> Dict[str, Any]:
        """
        Certain-and-life annuity: a_{x:n|} = a_{n} + n_E_x * a_{x+n}
        where a_n is annuity certain.
        """
        i = round(random.uniform(0.02, 0.08), 4)
        v = 1 / (1 + i)
        d = i / (1 + i)

        mu = round(random.uniform(0.02, 0.08), 4)
        delta = math.log(1 + i)
        n = random.randint(5, 20)

        certain = (1 - v ** n) / d
        pure_endow = math.exp(-(mu + delta) * n)
        life_portion = pure_endow / (mu + delta)

        answer = certain + life_portion

        d1 = certain
        d2 = life_portion
        d3 = (1 - v ** n) / (mu + delta)
        d4 = certain * life_portion

        return {
            "id": "fam_024",
            "exam": self.exam,
            "topic": self.topic_map["annuity"],
            "subtopic": "Certain-and-Life Annuity",
            "difficulty": "Hard",
            "question_text": f"Find the APV of a {n}-year certain-and-life annuity (i = {i}, mu = {mu}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"a_{{x:{n}|}} = a_{n} + n_E_x * a_{{x+n}} = {certain:.4f} + {life_portion:.4f} = {answer}",
            "explanation": "A certain-and-life annuity guarantees payments for n years, then continues if alive."
        }

    def varying_annuity(self) -> Dict[str, Any]:
        """
        Increasing annuity (discrete): (Ia)_x = sum_{k=0}^{inf} k * v^k * k_p_x
        """
        i = round(random.uniform(0.02, 0.08), 4)
        v = 1 / (1 + i)

        q_values = [round(random.uniform(0.01, 0.25), 4) for _ in range(4)]

        ia = 0
        p_cumulative = 1
        for k in range(len(q_values)):
            ia += k * (v ** k) * p_cumulative
            p_cumulative *= (1 - q_values[k])

        d1 = ia * 0.85
        d2 = ia * 1.15
        d3 = sum([(v ** k) for k in range(len(q_values))])
        d4 = (1 / (1 - v)) ** 2

        return {
            "id": "fam_025",
            "exam": self.exam,
            "topic": self.topic_map["annuity"],
            "subtopic": "Varying Annuity",
            "difficulty": "Hard",
            "question_text": f"Find the APV of an increasing annuity (Ia)_x with i = {i} and mortality {q_values}.",
            "choices": self.make_choices(ia, [d1, d2, d3, d4]),
            "solution": f"(Ia)_x = sum k*v^k*k_p_x = {ia}",
            "explanation": "An increasing annuity pays 0 at time 0, 1 at time 1, 2 at time 2, etc."
        }

    # ======================== PREMIUMS (5 methods) ========================

    def net_premium_whole(self) -> Dict[str, Any]:
        """
        Net annual premium for whole life: P = A_x / a_x (whole life annuity due basis)
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)

        ax_insur = mu / (mu + delta)
        ax_annuity = 1 / (mu + delta)

        answer = ax_insur / ax_annuity

        d1 = ax_insur * ax_annuity
        d2 = mu / delta
        d3 = delta
        d4 = mu * (mu + delta)

        return {
            "id": "fam_026",
            "exam": self.exam,
            "topic": self.topic_map["premium"],
            "subtopic": "Net Premium - Whole Life",
            "difficulty": "Medium",
            "question_text": f"Find the net annual premium for a whole life insurance (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"P = A_x / a_x = {ax_insur:.4f} / {ax_annuity:.4f} = {answer}",
            "explanation": "The net premium equals the APV of benefits divided by the APV of annuity of premiums."
        }

    def net_premium_term(self) -> Dict[str, Any]:
        """
        Net annual premium for n-year term: P^1 = A^1_{x:n} / a_{x:n}
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)
        n = random.randint(5, 20)

        term_insur = (mu / (mu + delta)) * (1 - math.exp(-(mu + delta) * n))
        term_annuity = (1 - term_insur - math.exp(-(mu + delta) * n)) / delta

        answer = term_insur / term_annuity

        d1 = term_insur * term_annuity
        d2 = mu / delta
        d3 = term_insur / (mu + delta)
        d4 = (mu / (mu + delta)) * (1 - math.exp(-delta * n))

        return {
            "id": "fam_027",
            "exam": self.exam,
            "topic": self.topic_map["premium"],
            "subtopic": "Net Premium - Term Life",
            "difficulty": "Medium",
            "question_text": f"Find the net annual premium for a {n}-year term insurance (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"P^1 = A^1_{{x:{n}}} / a_{{x:{n}}} = {term_insur:.4f} / {term_annuity:.4f} = {answer}",
            "explanation": "Term insurance premium is the ratio of term APV to the temporary annuity APV."
        }

    def net_premium_endowment(self) -> Dict[str, Any]:
        """
        Net annual premium for n-year endowment: P = A_{x:n} / a_{x:n}
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)
        n = random.randint(5, 20)

        term_insur = (mu / (mu + delta)) * (1 - math.exp(-(mu + delta) * n))
        pure_endow = math.exp(-(mu + delta) * n)
        endow_insur = term_insur + pure_endow

        endow_annuity = (1 - endow_insur) / delta

        answer = endow_insur / endow_annuity

        d1 = term_insur / endow_annuity
        d2 = pure_endow / endow_annuity
        d3 = (endow_insur + delta) / (mu + delta)
        d4 = mu * pure_endow / delta

        return {
            "id": "fam_028",
            "exam": self.exam,
            "topic": self.topic_map["premium"],
            "subtopic": "Net Premium - Endowment",
            "difficulty": "Medium",
            "question_text": f"Find the net annual premium for a {n}-year endowment insurance (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"P = A_{{x:{n}}} / a_{{x:{n}}} = {endow_insur:.4f} / {endow_annuity:.4f} = {answer}",
            "explanation": "Endowment premium is higher than term due to the pure endowment component."
        }

    def gross_premium(self) -> Dict[str, Any]:
        """
        Gross premium including expenses: G = (A_x + expenses) / a_x
        where expenses = % of premium + per-policy fee
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)

        ax_insur = mu / (mu + delta)
        ax_annuity = 1 / (mu + delta)

        percent_exp_rate = round(random.uniform(0.05, 0.15), 3)
        per_policy_fee = round(random.uniform(5, 25), 2)

        answer = (ax_insur + per_policy_fee) / (ax_annuity * (1 - percent_exp_rate))

        d1 = (ax_insur + per_policy_fee) / ax_annuity
        d2 = ax_insur / (ax_annuity * (1 - percent_exp_rate))
        d3 = (ax_insur + percent_exp_rate) / ax_annuity
        d4 = (ax_insur / ax_annuity) * (1 + percent_exp_rate)

        return {
            "id": "fam_029",
            "exam": self.exam,
            "topic": self.topic_map["premium"],
            "subtopic": "Gross Premium",
            "difficulty": "Hard",
            "question_text": f"Find the gross premium including {percent_exp_rate*100}% expense and ${per_policy_fee} per policy fee (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"G = (A_x + {per_policy_fee})/(a_x*(1-{percent_exp_rate})) = {answer}",
            "explanation": "Gross premiums cover benefits, acquisition expenses, and ongoing per-policy costs."
        }

    def loss_variance(self) -> Dict[str, Any]:
        """
        Variance of loss: Var(L) = Var(Benefits - G*Annuity) = Var(Z) - G^2 * Var(Y)
        For whole life with constant force: Var(L) = 2A_x - (A_x)^2
        where 2A_x uses double discount rate.
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)

        ax_insur = mu / (mu + delta)
        two_ax = mu / (mu + 2 * delta)
        ax_annuity = 1 / (mu + delta)

        G = ax_insur / ax_annuity

        var_benefit = two_ax - (ax_insur ** 2)
        answer = var_benefit * (1 - G * ax_annuity) ** 2

        d1 = var_benefit
        d2 = var_benefit * G
        d3 = (two_ax - (ax_insur ** 2)) / ax_annuity
        d4 = two_ax * (1 - G) ** 2

        return {
            "id": "fam_030",
            "exam": self.exam,
            "topic": self.topic_map["premium"],
            "subtopic": "Loss Variance",
            "difficulty": "Hard",
            "question_text": f"Find the variance of loss for whole life insurance with net premium G (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"Var(L) = Var(Z) * (1 - P*a_x)^2 = {var_benefit:.6f} * ({1 - G * ax_annuity:.4f})^2 = {answer}",
            "explanation": "Loss variance combines the benefit variance with the reduction due to net premiums."
        }

    # ======================== RESERVES (5 methods) ========================

    def reserve_prospective(self) -> Dict[str, Any]:
        """
        Prospective reserve: t_V = A_{x+t} - P*a_{x+t}
        At duration t, compute the reserve.
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)

        ax_insur = mu / (mu + delta)
        ax_annuity = 1 / (mu + delta)
        P = ax_insur / ax_annuity

        t = random.randint(1, 10)

        ax_t = ax_insur
        ax_t_annuity = ax_annuity

        answer = ax_t - P * ax_t_annuity

        d1 = ax_insur - P * ax_annuity
        d2 = P * ax_t_annuity
        d3 = ax_t - P
        d4 = ax_insur * (1 - P * t / ax_annuity)

        return {
            "id": "fam_031",
            "exam": self.exam,
            "topic": self.topic_map["reserve"],
            "subtopic": "Prospective Reserve",
            "difficulty": "Medium",
            "question_text": f"Find the prospective reserve at duration t = {t} for a whole life insurance (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"{t}V = A_{{x+{t}}} - P*a_{{x+{t}}} = {ax_t:.4f} - {P:.4f}*{ax_t_annuity:.4f} = {answer}",
            "explanation": "The prospective reserve is the PV of future benefits minus the PV of future net premiums."
        }

    def reserve_retrospective(self) -> Dict[str, Any]:
        """
        Retrospective reserve: t_V = (P*s_dd_{x:t} - cost) / t_E_x
        For constant force, simplified to accumulation of premiums less accumulated cost.
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)
        v = 1 / (1 + i)

        ax_insur = mu / (mu + delta)
        ax_annuity = 1 / (mu + delta)
        P = ax_insur / ax_annuity

        t = random.randint(1, 5)

        s_certain = ((1 + i) ** t - 1) / i
        accumulated_cost = ax_insur * (1 - v ** t) / i
        t_e = math.exp(-(mu + delta) * t)

        answer = (P * s_certain - accumulated_cost) / t_e

        d1 = P * s_certain
        d2 = P * s_certain / t_e
        d3 = (P - accumulated_cost) * s_certain
        d4 = P * s_certain * t_e

        return {
            "id": "fam_032",
            "exam": self.exam,
            "topic": self.topic_map["reserve"],
            "subtopic": "Retrospective Reserve",
            "difficulty": "Hard",
            "question_text": f"Find the retrospective reserve at duration t = {t} (mu = {mu}, i = {i}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"{t}V = (P*s_{{:{t}}} - cost) / {t}_E_x = {answer}",
            "explanation": "The retrospective reserve accumulates past premiums less past costs, discounted back to present."
        }

    def reserve_recursion(self) -> Dict[str, Any]:
        """
        Reserve recursion: (t_V + P)(1 + i) = q_{x+t} * 1 + p_{x+t} * t+1_V
        Solve for unknown (typically t+1_V given t_V)
        """
        i = round(random.uniform(0.02, 0.08), 4)
        P = round(random.uniform(0.01, 0.05), 4)
        q = round(random.uniform(0.01, 0.15), 4)
        p = 1 - q
        t_V = round(random.uniform(0.01, 0.15), 4)

        answer = ((t_V + P) * (1 + i) - q) / p

        d1 = (t_V + P) * (1 + i) - q
        d2 = ((t_V + P) * (1 + i)) / p
        d3 = (t_V + P) / p
        d4 = (t_V + P) * (1 + i) / q

        return {
            "id": "fam_033",
            "exam": self.exam,
            "topic": self.topic_map["reserve"],
            "subtopic": "Reserve Recursion",
            "difficulty": "Medium",
            "question_text": f"Using the reserve recursion with {t}V = {t_V}, P = {P}, q_{{x+t}} = {q}, and i = {i}, find {t+1}V.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"({t}V + P)(1 + i) = q + p*{t+1}V, so {t+1}V = (({t_V} + {P})*(1+{i}) - {q})/{p} = {answer}",
            "explanation": "Reserve recursion links consecutive year reserves through the profit equation."
        }

    def terminal_reserve_first_year(self) -> Dict[str, Any]:
        """
        Terminal reserve at end of year 1: 1_V from recursion
        (0 + P)(1 + i) = q_x * 1 + p_x * 1_V
        So 1_V = (P(1+i) - q_x) / p_x
        """
        i = round(random.uniform(0.02, 0.08), 4)
        mu = round(random.uniform(0.02, 0.08), 4)
        delta = math.log(1 + i)

        ax_insur = mu / (mu + delta)
        ax_annuity = 1 / (mu + delta)
        P = ax_insur / ax_annuity

        q_x = round(random.uniform(0.01, 0.15), 4)
        p_x = 1 - q_x

        answer = (P * (1 + i) - q_x) / p_x

        d1 = P * (1 + i) - q_x
        d2 = P * (1 + i) / p_x
        d3 = (P - q_x) / (1 + i)
        d4 = P / p_x

        return {
            "id": "fam_034",
            "exam": self.exam,
            "topic": self.topic_map["reserve"],
            "subtopic": "Terminal Reserve - First Year",
            "difficulty": "Medium",
            "question_text": f"Find the terminal reserve at end of year 1 with P = {P:.4f}, q_x = {q_x}, and i = {i}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"1_V = (P(1+i) - q_x) / p_x = ({P:.4f}*{1+i:.4f} - {q_x}) / {p_x:.4f} = {answer}",
            "explanation": "The first year terminal reserve uses the recursion formula starting with 0_V = 0."
        }

    def gross_premium_reserve(self) -> Dict[str, Any]:
        """
        Gross premium reserve: t_V(G) = A_{x+t} + expenses - G*a_{x+t}
        """
        mu = round(random.uniform(0.02, 0.08), 4)
        i = round(random.uniform(0.02, 0.06), 4)
        delta = math.log(1 + i)

        ax_insur = mu / (mu + delta)
        ax_annuity = 1 / (mu + delta)

        percent_exp = round(random.uniform(0.05, 0.15), 3)
        per_policy = round(random.uniform(5, 25), 2)

        G = (ax_insur + per_policy) / (ax_annuity * (1 - percent_exp))

        t = random.randint(1, 5)

        ax_t = ax_insur
        ax_t_annuity = ax_annuity
        remaining_cost = per_policy * (1 / (ax_annuity * (1 - percent_exp)))

        answer = ax_t + remaining_cost - G * ax_t_annuity

        d1 = ax_t - G * ax_t_annuity
        d2 = ax_t + per_policy - G * ax_t_annuity
        d3 = G * ax_t_annuity - ax_t
        d4 = ax_insur + remaining_cost

        return {
            "id": "fam_035",
            "exam": self.exam,
            "topic": self.topic_map["reserve"],
            "subtopic": "Gross Premium Reserve",
            "difficulty": "Hard",
            "question_text": f"Find the gross premium reserve at duration t = {t} (mu = {mu}, i = {i}, per-policy cost = ${per_policy}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"{t}V(G) = A_{{x+{t}}} + expenses - G*a_{{x+{t}}} = {answer}",
            "explanation": "The gross premium reserve accounts for all future expenses in the reserve calculation."
        }

    # ======================== SEVERITY MODELS (8 methods) ========================

    def exponential_severity(self) -> Dict[str, Any]:
        """
        Exponential severity: E[(X-d)+] = theta*e^(-d/theta)
        """
        theta = round(random.uniform(500, 5000), 0)
        d = round(random.uniform(100, theta * 0.8), 0)

        answer = theta * math.exp(-d / theta)

        d1 = theta * (1 - math.exp(-d / theta))
        d2 = theta * math.exp(-theta / d)
        d3 = (theta - d) * math.exp(-d / theta)
        d4 = theta / math.exp(d / theta)

        return {
            "id": "fam_036",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Exponential Severity",
            "difficulty": "Medium",
            "question_text": f"For exponential severity with theta = {theta}, find E[(X-{d})+].",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[(X-d)+] = theta*e^(-d/theta) = {theta}*e^(-{d}/{theta}) = {answer}",
            "explanation": "For exponential distribution, the limited expected value above a deductible follows a simple exponential formula."
        }

    def pareto_severity(self) -> Dict[str, Any]:
        """
        Pareto severity: alpha rand [2,5], theta rand [1000,10000]
        E[X] = theta/(alpha-1), E[X^d], E[(X-d)+]
        """
        alpha = round(random.uniform(2, 5), 2)
        theta = round(random.uniform(1000, 10000), 0)
        d = round(random.uniform(theta, theta * 3), 0)

        e_x = theta / (alpha - 1)
        if alpha > 1:
            answer = (theta / (alpha - 1)) * ((theta / d) ** (alpha - 1))
        else:
            answer = theta

        d1 = theta / (alpha - 1)
        d2 = theta * (d / theta) ** (1 - alpha)
        d3 = (theta ** alpha) / (d ** (alpha - 1))
        d4 = theta * alpha / d

        return {
            "id": "fam_037",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Pareto Severity",
            "difficulty": "Hard",
            "question_text": f"For Pareto severity (alpha = {alpha}, theta = {theta}), find E[(X-{d})+].",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[(X-d)+] = (theta/(alpha-1))*((theta/d)^(alpha-1)) = {answer}",
            "explanation": "Pareto severity has a power-law tail. The limited expected value uses the tail probability formula."
        }

    def lognormal_severity(self) -> Dict[str, Any]:
        """
        Lognormal severity: mu rand [5,8], sigma rand [0.5,2]
        P(X > x) = 1 - Phi((ln(x)-mu)/sigma)
        """
        mu = round(random.uniform(5, 8), 2)
        sigma = round(random.uniform(0.5, 2), 2)
        x = round(random.uniform(math.exp(mu - 2 * sigma), math.exp(mu + 2 * sigma)), 0)

        z = (math.log(x) - mu) / sigma
        # Approximate Phi using error function
        from app.services.generators.compat import ndtr
        answer = 1 - ndtr(z)

        d1 = ndtr(z)
        d2 = 1 - ndtr(-z)
        d3 = ndtr((mu - math.log(x)) / sigma)
        d4 = math.exp(-z)

        return {
            "id": "fam_038",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Lognormal Severity",
            "difficulty": "Hard",
            "question_text": f"For lognormal severity (mu = {mu}, sigma = {sigma}), find P(X > {x}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"P(X > x) = 1 - Phi((ln({x})-{mu})/{sigma}) = 1 - Phi({z:.4f}) = {answer}",
            "explanation": "Lognormal is found by taking the natural log and using the standard normal distribution."
        }

    def gamma_mean_variance(self) -> Dict[str, Any]:
        """
        Gamma: Given mean and variance, solve alpha = mean^2/var, theta = var/mean
        """
        mean = round(random.uniform(500, 2000), 0)
        cv = round(random.uniform(0.3, 0.8), 2)
        variance = (mean * cv) ** 2

        alpha = (mean ** 2) / variance
        theta = variance / mean

        answer = alpha

        d1 = variance / mean
        d2 = mean / variance
        d3 = (mean / variance) ** 2
        d4 = math.sqrt(mean / variance)

        return {
            "id": "fam_039",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Gamma Mean-Variance",
            "difficulty": "Easy",
            "question_text": f"For gamma distribution with mean = {mean} and variance = {variance}, find alpha.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"alpha = mean^2/var = {mean}^2/{variance} = {answer}",
            "explanation": "For gamma, alpha = mean^2/variance and theta = variance/mean."
        }

    def weibull_survival(self) -> Dict[str, Any]:
        """
        Weibull survival: tau rand [0.5,3], theta rand [1000,5000]
        S(x) = exp(-(x/theta)^tau), find S(x) for random x
        """
        tau = round(random.uniform(0.5, 3), 2)
        theta = round(random.uniform(1000, 5000), 0)
        x = round(random.uniform(0, theta * 2), 0)

        answer = math.exp(-(x / theta) ** tau)

        d1 = 1 - (x / theta) ** tau
        d2 = math.exp(-x / theta)
        d3 = math.exp(-(x / theta) ** (1 / tau))
        d4 = (theta / x) ** tau

        return {
            "id": "fam_040",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Weibull Survival",
            "difficulty": "Medium",
            "question_text": f"For Weibull with tau = {tau}, theta = {theta}, find S({x}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"S(x) = exp(-(x/theta)^tau) = exp(-({x}/{theta})^{tau}) = {answer}",
            "explanation": "Weibull is a flexible distribution with shape parameter tau."
        }

    def mixture_exponentials(self) -> Dict[str, Any]:
        """
        Mixture of exponentials: p rand [0.3,0.7], theta1, theta2
        E[X] = p*theta1 + (1-p)*theta2
        """
        p = round(random.uniform(0.3, 0.7), 2)
        theta1 = round(random.uniform(500, 2000), 0)
        theta2 = round(random.uniform(2000, 8000), 0)

        answer = p * theta1 + (1 - p) * theta2

        d1 = p * theta1
        d2 = (1 - p) * theta2
        d3 = (theta1 + theta2) / 2
        d4 = (p * theta1) * ((1 - p) * theta2)

        return {
            "id": "fam_041",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Mixture of Exponentials",
            "difficulty": "Easy",
            "question_text": f"For mixture with p = {p}, theta1 = {theta1}, theta2 = {theta2}, find E[X].",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[X] = p*theta1 + (1-p)*theta2 = {p}*{theta1} + {1-p}*{theta2} = {answer}",
            "explanation": "For a mixture distribution, the overall mean is the weighted average of component means."
        }

    def spliced_distribution(self) -> Dict[str, Any]:
        """
        Spliced distribution: Two distributions joined at c
        """
        c = round(random.uniform(1000, 2000), 0)
        theta_below = round(random.uniform(500, c), 0)
        theta_above = round(random.uniform(c, 5000), 0)

        prob_below = 0.6
        prob_above = 0.4

        e_x_below = theta_below * (1 - math.exp(-c / theta_below))
        e_x_above = c + theta_above
        answer = prob_below * e_x_below + prob_above * e_x_above

        d1 = prob_below * e_x_below
        d2 = prob_above * e_x_above
        d3 = (e_x_below + e_x_above) / 2
        d4 = c * (prob_below + prob_above)

        return {
            "id": "fam_042",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Spliced Distribution",
            "difficulty": "Hard",
            "question_text": f"For spliced distribution with splice point c = {c}, find overall E[X].",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[X] = {prob_below}*E[X below] + {prob_above}*E[X above] = {answer}",
            "explanation": "A spliced distribution combines two models at a splice point."
        }

    def loss_elimination_ratio(self) -> Dict[str, Any]:
        """
        LER = E[(X-d)+]/E[X] for exponential = 1 - e^(-d/theta)
        """
        theta = round(random.uniform(500, 5000), 0)
        d = round(random.uniform(100, theta), 0)

        e_x = theta
        limited_e_x = theta * math.exp(-d / theta)
        answer = limited_e_x / e_x

        d1 = 1 - answer
        d2 = 1 - math.exp(-d / theta)
        d3 = math.exp(-d / theta) / theta
        d4 = d / theta

        return {
            "id": "fam_043",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Loss Elimination Ratio",
            "difficulty": "Medium",
            "question_text": f"For exponential severity (theta = {theta}), find LER with deductible d = {d}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"LER = E[(X-d)+]/E[X] = e^(-d/theta) = e^(-{d}/{theta}) = {answer}",
            "explanation": "The loss elimination ratio measures the proportion of losses eliminated by a deductible."
        }

    # ======================== FREQUENCY (6 methods) ========================

    def poisson_probability(self) -> Dict[str, Any]:
        """
        Poisson: lambda rand [1,10], k rand [0,5]
        P(N=k) = e^(-lambda)*lambda^k/k!
        """
        lambda_param = round(random.uniform(1, 10), 2)
        k = random.randint(0, 5)

        answer = math.exp(-lambda_param) * (lambda_param ** k) / math.factorial(k)

        d1 = (lambda_param ** k) / math.factorial(k)
        d2 = lambda_param * math.exp(-lambda_param) / math.factorial(k)
        d3 = math.exp(-lambda_param) * (lambda_param ** (k - 1)) / math.factorial(k)
        d4 = (1 - math.exp(-lambda_param)) * (lambda_param ** k) / math.factorial(k)

        return {
            "id": "fam_044",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Poisson Probability",
            "difficulty": "Easy",
            "question_text": f"For Poisson with lambda = {lambda_param}, find P(N = {k}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"P(N={k}) = e^(-{lambda_param})*{lambda_param}^{k}/{k}! = {answer}",
            "explanation": "The Poisson distribution is commonly used to model claim counts."
        }

    def neg_binomial_frequency(self) -> Dict[str, Any]:
        """
        Negative binomial: r rand [1,5], beta rand [0.5,3]
        P(N=0) = (1/(1+beta))^r, P(N=k) general form
        """
        r = random.randint(1, 5)
        beta = round(random.uniform(0.5, 3), 2)
        k = random.randint(0, 4)

        p_0 = (1 / (1 + beta)) ** r
        if k == 0:
            answer = p_0
        else:
            answer = (math.comb(r + k - 1, k) * (beta / (1 + beta)) ** k * (1 / (1 + beta)) ** r)

        d1 = (1 / (1 + beta)) ** r if k == 0 else (beta / (1 + beta)) ** k
        d2 = (beta / (1 + beta)) ** k / (1 + beta) ** r
        d3 = (r + k) * (beta / (1 + beta)) ** k / (1 + beta) ** r
        d4 = (beta ** k) / ((1 + beta) ** (r + k))

        return {
            "id": "fam_045",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Negative Binomial Frequency",
            "difficulty": "Hard",
            "question_text": f"For NB with r = {r}, beta = {beta}, find P(N = {k}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"P(N={k}) = C(r+k-1,k)*(beta/(1+beta))^k*(1/(1+beta))^r = {answer}",
            "explanation": "The negative binomial is a conjugate prior for Poisson in Bayesian analysis."
        }

    def binomial_frequency(self) -> Dict[str, Any]:
        """
        Binomial: m rand [5,20], q rand [0.05,0.3]
        P(N=k) = C(m,k)*q^k*(1-q)^(m-k)
        """
        m = random.randint(5, 20)
        q = round(random.uniform(0.05, 0.3), 3)
        k = random.randint(0, m)

        answer = math.comb(m, k) * (q ** k) * ((1 - q) ** (m - k))

        d1 = (q ** k) * ((1 - q) ** (m - k))
        d2 = math.comb(m, k) * (q ** (k + 1)) * ((1 - q) ** (m - k - 1))
        d3 = (m / k) * (q ** k) * ((1 - q) ** (m - k))
        d4 = math.comb(m, m - k) * ((1 - q) ** k) * (q ** (m - k))

        return {
            "id": "fam_046",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Binomial Frequency",
            "difficulty": "Medium",
            "question_text": f"For binomial with m = {m}, q = {q}, find P(N = {k}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"P(N={k}) = C({m},{k})*{q}^{k}*{1-q}^{m-k} = {answer}",
            "explanation": "Binomial models a fixed number of independent Bernoulli trials."
        }

    def zero_truncated_poisson(self) -> Dict[str, Any]:
        """
        Zero-truncated Poisson: lambda rand
        P_T(k) = P(k)/(1-P(0)) for k > 0
        """
        lambda_param = round(random.uniform(1, 8), 2)
        k = random.randint(1, 5)

        p_k = math.exp(-lambda_param) * (lambda_param ** k) / math.factorial(k)
        p_0 = math.exp(-lambda_param)
        answer = p_k / (1 - p_0)

        d1 = p_k
        d2 = p_k / (1 - 1 / (1 + lambda_param))
        d3 = (lambda_param ** k) / (math.factorial(k) * (1 - math.exp(-lambda_param)))
        d4 = math.exp(-lambda_param) * (lambda_param ** (k - 1)) / (1 - p_0)

        return {
            "id": "fam_047",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Zero-Truncated Poisson",
            "difficulty": "Medium",
            "question_text": f"For zero-truncated Poisson (lambda = {lambda_param}), find P(N = {k}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"P_T({k}) = P({k})/(1-P(0)) = {p_k:.6f}/{1-p_0:.6f} = {answer}",
            "explanation": "Zero-truncated distributions exclude the possibility of zero."
        }

    def zero_modified_distribution(self) -> Dict[str, Any]:
        """
        Zero-modified: p_0_M rand [0.3,0.7], base Poisson
        P_M(0) = p_0_M, P_M(k) = (1-p_0_M)*P(k)/(1-P(0)) for k > 0
        """
        lambda_param = round(random.uniform(1, 8), 2)
        p_0_m = round(random.uniform(0.3, 0.7), 2)
        k = random.randint(1, 4)

        p_k = math.exp(-lambda_param) * (lambda_param ** k) / math.factorial(k)
        p_0 = math.exp(-lambda_param)
        answer = (1 - p_0_m) * p_k / (1 - p_0)

        d1 = p_0_m
        d2 = (1 - p_0_m) * p_k
        d3 = p_k / (1 - p_0)
        d4 = p_0_m * p_k / (1 - p_0)

        return {
            "id": "fam_048",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Zero-Modified Distribution",
            "difficulty": "Hard",
            "question_text": f"For zero-modified Poisson (p_0_M = {p_0_m}, lambda = {lambda_param}), find P(N = {k}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"P_M({k}) = (1-{p_0_m})*P({k})/(1-P(0)) = {answer}",
            "explanation": "Zero-modified distributions adjust the probability of zero from the base distribution."
        }

    def poisson_gamma_mixture(self) -> Dict[str, Any]:
        """
        Gamma mixing distribution for Poisson
        Resulting NB has mean alpha*theta
        """
        alpha = round(random.uniform(1, 5), 2)
        theta = round(random.uniform(0.5, 3), 2)

        answer = alpha * theta

        d1 = alpha / theta
        d2 = alpha + theta
        d3 = alpha / (alpha + theta)
        d4 = (alpha * theta) / (alpha + theta)

        return {
            "id": "fam_049",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Poisson-Gamma Mixture",
            "difficulty": "Easy",
            "question_text": f"For Poisson-Gamma mixture (alpha = {alpha}, theta = {theta}), find E[N].",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[N] = alpha*theta = {alpha}*{theta} = {answer}",
            "explanation": "Mixing Poisson with a Gamma distribution on the parameter yields a negative binomial."
        }

    # ======================== AGGREGATE LOSS (8 methods) ========================

    def compound_poisson_mean(self) -> Dict[str, Any]:
        """
        Compound Poisson: E[S] = lambda*E[X]
        """
        lambda_param = round(random.uniform(1, 10), 2)
        e_x = round(random.uniform(500, 5000), 0)

        answer = lambda_param * e_x

        d1 = lambda_param / e_x
        d2 = lambda_param + e_x
        d3 = math.sqrt(lambda_param * e_x)
        d4 = lambda_param * (e_x ** 2)

        return {
            "id": "fam_050",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Compound Poisson Mean",
            "difficulty": "Easy",
            "question_text": f"For compound Poisson (lambda = {lambda_param}, E[X] = {e_x}), find E[S].",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[S] = lambda*E[X] = {lambda_param}*{e_x} = {answer}",
            "explanation": "The mean of an aggregate loss is the product of frequency and severity means."
        }

    def compound_poisson_variance(self) -> Dict[str, Any]:
        """
        Compound Poisson Variance: Var(S) = lambda*E[X^2]
        """
        lambda_param = round(random.uniform(1, 10), 2)
        e_x = round(random.uniform(500, 5000), 0)
        cv = round(random.uniform(0.5, 1.5), 2)
        e_x2 = e_x * e_x * (1 + cv ** 2)

        answer = lambda_param * e_x2

        d1 = lambda_param * e_x
        d2 = lambda_param * (e_x ** 2)
        d3 = (lambda_param ** 2) * e_x2
        d4 = lambda_param * e_x / (1 + cv)

        return {
            "id": "fam_051",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Compound Poisson Variance",
            "difficulty": "Medium",
            "question_text": f"For compound Poisson (lambda = {lambda_param}, E[X^2] = {e_x2:.0f}), find Var(S).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"Var(S) = lambda*E[X^2] = {lambda_param}*{e_x2:.0f} = {answer}",
            "explanation": "Variance of aggregate loss depends on both frequency and severity second moments."
        }

    def stop_loss_normal_approx(self) -> Dict[str, Any]:
        """
        Stop-loss: E[(S-d)+] using normal approximation
        """
        e_s = round(random.uniform(5000, 20000), 0)
        var_s = round(random.uniform(1000000, 5000000), 0)
        sd_s = math.sqrt(var_s)
        d = round(random.uniform(e_s, e_s + 2 * sd_s), 0)

        from app.services.generators.compat import ndtr
        z = (d - e_s) / sd_s
        answer = sd_s * (z * ndtr(z) + (1 / math.sqrt(2 * math.pi)) * math.exp(-z ** 2 / 2))

        d1 = (d - e_s) * (1 - ndtr(z))
        d2 = sd_s * (1 - ndtr(z))
        d3 = e_s - d * ndtr(z)
        d4 = (d - e_s) * ndtr(z)

        return {
            "id": "fam_052",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Stop-Loss Normal Approx",
            "difficulty": "Hard",
            "question_text": f"Find E[(S-{d})+] using normal approx (E[S] = {e_s}, SD(S) = {sd_s:.0f}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[(S-d)+] ≈ {answer:.0f}",
            "explanation": "Stop-loss expected value uses the normal tail integral."
        }

    def panjer_recursion(self) -> Dict[str, Any]:
        """
        Panjer recursion for compound Poisson with discrete severity
        """
        lambda_param = round(random.uniform(1, 5), 2)
        p_1 = round(random.uniform(0.3, 0.6), 2)
        p_2 = round(random.uniform(0.2, 0.4), 2)
        p_2 = min(p_2, 1 - p_1)

        f_s_0 = math.exp(-lambda_param)
        f_s_1 = lambda_param * p_1 * f_s_0

        d1 = lambda_param * p_1
        d2 = f_s_0
        d3 = lambda_param * p_1 * math.exp(-lambda_param)
        d4 = lambda_param * (1 - p_1)

        return {
            "id": "fam_053",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Panjer Recursion",
            "difficulty": "Hard",
            "question_text": f"Using Panjer recursion (lambda = {lambda_param}, p_1 = {p_1}), find f_S(1).",
            "choices": self.make_choices(f_s_1, [d1, d2, d3, d4]),
            "solution": f"f_S(1) = lambda*p_1*exp(-lambda) = {lambda_param}*{p_1}*exp(-{lambda_param}) = {f_s_1:.6f}",
            "explanation": "Panjer recursion efficiently computes aggregate loss PMF for (a,b,0) class distributions."
        }

    def individual_risk_model(self) -> Dict[str, Any]:
        """
        Individual risk: n independent risks, prob q, severity X
        E[S] = n*q*E[X], Var(S) = n*(q*E[X^2] - q^2*E[X]^2)
        """
        n = random.randint(10, 100)
        q = round(random.uniform(0.01, 0.3), 3)
        e_x = round(random.uniform(500, 2000), 0)
        cv = round(random.uniform(0.3, 1), 2)
        e_x2 = (e_x ** 2) * (1 + cv ** 2)

        answer = n * (q * e_x2 - (q ** 2) * (e_x ** 2))

        d1 = n * q * e_x
        d2 = n * q * e_x2
        d3 = n * (q * (e_x ** 2))
        d4 = (n ** 2) * q * (e_x2 - (e_x ** 2))

        return {
            "id": "fam_054",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Individual Risk Model",
            "difficulty": "Medium",
            "question_text": f"For {n} independent risks (q = {q}, E[X^2] = {e_x2:.0f}), find Var(S).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"Var(S) = n*(q*E[X^2] - q^2*E[X]^2) = {answer:.0f}",
            "explanation": "Individual risk model applies when risks are independent."
        }

    def normal_approx_prob(self) -> Dict[str, Any]:
        """
        Normal approximation: P(S > s) = 1 - Phi((s-E[S])/sqrt(Var(S)))
        """
        e_s = round(random.uniform(5000, 20000), 0)
        var_s = round(random.uniform(1000000, 5000000), 0)
        sd_s = math.sqrt(var_s)
        s = round(random.uniform(e_s, e_s + 2 * sd_s), 0)

        from app.services.generators.compat import ndtr
        z = (s - e_s) / sd_s
        answer = 1 - ndtr(z)

        d1 = ndtr(z)
        d2 = ndtr((e_s - s) / sd_s)
        d3 = 1 - ndtr(-z)
        d4 = (s - e_s) / sd_s

        return {
            "id": "fam_055",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Normal Approx Probability",
            "difficulty": "Medium",
            "question_text": f"Find P(S > {s}) using normal approx (E[S] = {e_s}, SD = {sd_s:.0f}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"P(S > {s}) = 1 - Phi(({s}-{e_s})/{sd_s:.0f}) = 1 - Phi({z:.4f}) = {answer}",
            "explanation": "Normal approximation is useful when aggregate loss is approximately normal."
        }

    def excess_reinsurance(self) -> Dict[str, Any]:
        """
        Excess reinsurance per claim: E[S_ceded] = lambda*E[(X-M)+]
        """
        lambda_param = round(random.uniform(1, 10), 2)
        theta = round(random.uniform(500, 5000), 0)
        m = round(random.uniform(500, theta * 2), 0)

        e_x_excess = theta * math.exp(-m / theta)
        answer = lambda_param * e_x_excess

        d1 = lambda_param * m
        d2 = lambda_param * (theta - m)
        d3 = lambda_param * theta
        d4 = (lambda_param / theta) * m

        return {
            "id": "fam_056",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Excess Reinsurance",
            "difficulty": "Medium",
            "question_text": f"For compound Poisson (lambda = {lambda_param}, exp severity, theta = {theta}), find E[S_ceded] with per-claim limit M = {m}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[S_ceded] = lambda*E[(X-M)+] = {lambda_param}*{e_x_excess:.0f} = {answer:.0f}",
            "explanation": "Excess reinsurance transfers losses above a per-claim limit."
        }

    def aggregate_deductible(self) -> Dict[str, Any]:
        """
        Aggregate deductible: E[(S-D)+] using normal approximation
        """
        e_s = round(random.uniform(5000, 20000), 0)
        var_s = round(random.uniform(1000000, 5000000), 0)
        sd_s = math.sqrt(var_s)
        d_agg = round(random.uniform(e_s * 0.5, e_s), 0)

        from app.services.generators.compat import ndtr
        z = (d_agg - e_s) / sd_s
        answer = sd_s * (-z * ndtr(z) + (1 / math.sqrt(2 * math.pi)) * math.exp(-z ** 2 / 2))

        d1 = (e_s - d_agg) * (1 - ndtr(z))
        d2 = sd_s * (1 - ndtr(z))
        d3 = (e_s - d_agg) * ndtr(-z)
        d4 = e_s * (1 - d_agg / e_s)

        return {
            "id": "fam_057",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Aggregate Deductible",
            "difficulty": "Hard",
            "question_text": f"Find E[(S-{d_agg})+] using normal approx (E[S] = {e_s}, SD = {sd_s:.0f}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[(S-D)+] ≈ {answer:.0f}",
            "explanation": "Aggregate deductible applies to total losses across all claims."
        }

    # ======================== COVERAGE MODIFICATIONS (8 methods) ========================

    def ordinary_deductible(self) -> Dict[str, Any]:
        """
        Ordinary deductible: E[(X-d)+] = E[X] - E[X^d]
        For exponential: theta*e^(-d/theta)
        """
        theta = round(random.uniform(500, 5000), 0)
        d = round(random.uniform(100, theta), 0)

        e_x = theta
        e_xd = theta * (1 - math.exp(-d / theta))
        answer = e_x - e_xd

        d1 = e_xd
        d2 = theta - d
        d3 = e_x * (1 - d / theta)
        d4 = theta / (1 + d / theta)

        return {
            "id": "fam_058",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Ordinary Deductible",
            "difficulty": "Easy",
            "question_text": f"For exponential (theta = {theta}), find E[(X-{d})+].",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[(X-d)+] = E[X] - E[X^d] = {e_x} - {e_xd:.0f} = {answer:.0f}",
            "explanation": "An ordinary deductible eliminates the first d of losses."
        }

    def franchise_deductible(self) -> Dict[str, Any]:
        """
        Franchise deductible: E[(X-d)+] + d*(1-F(d))
        For exponential: theta*e^(-d/theta) + d*e^(-d/theta)
        """
        theta = round(random.uniform(500, 5000), 0)
        d = round(random.uniform(100, theta), 0)

        limited_ex = theta * math.exp(-d / theta)
        survival = math.exp(-d / theta)
        answer = limited_ex + d * survival

        d1 = limited_ex
        d2 = d * survival
        d3 = theta * (1 - survival)
        d4 = (limited_ex + d) / 2

        return {
            "id": "fam_059",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Franchise Deductible",
            "difficulty": "Medium",
            "question_text": f"For exponential (theta = {theta}), find expected payout with franchise deductible d = {d}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"Payout = E[(X-d)+] + d*P(X>d) = {limited_ex:.0f} + {d*survival:.0f} = {answer:.0f}",
            "explanation": "A franchise deductible is waived entirely if the loss exceeds it."
        }

    def policy_limit(self) -> Dict[str, Any]:
        """
        Policy limit: E[X^u] = integral 0 to u of S(x)dx
        For exponential: theta*(1 - e^(-u/theta))
        """
        theta = round(random.uniform(500, 5000), 0)
        u = round(random.uniform(500, theta * 3), 0)

        answer = theta * (1 - math.exp(-u / theta))

        d1 = u * (1 - math.exp(-u / theta))
        d2 = theta * (1 - u / (theta + u))
        d3 = theta - u
        d4 = theta * math.exp(-u / theta)

        return {
            "id": "fam_060",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Policy Limit",
            "difficulty": "Easy",
            "question_text": f"For exponential (theta = {theta}), find E[min(X, {u})].",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[X^u] = theta*(1 - e^(-u/theta)) = {theta}*(1 - e^(-{u}/{theta})) = {answer:.0f}",
            "explanation": "A policy limit caps the maximum payout."
        }

    def deductible_and_limit(self) -> Dict[str, Any]:
        """
        Deductible and limit: E[min(max(X-d,0), u-d)]
        = E[X^u] - E[X^d] for exponential
        """
        theta = round(random.uniform(500, 5000), 0)
        d = round(random.uniform(100, theta), 0)
        u = round(random.uniform(d + 500, theta * 3), 0)

        e_xu = theta * (1 - math.exp(-u / theta))
        e_xd = theta * (1 - math.exp(-d / theta))
        answer = e_xu - e_xd

        d1 = e_xd
        d2 = e_xu
        d3 = (e_xu + e_xd) / 2
        d4 = theta * (math.exp(-d / theta) - math.exp(-u / theta))

        return {
            "id": "fam_061",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Deductible and Limit",
            "difficulty": "Medium",
            "question_text": f"For exponential (theta = {theta}), deductible d = {d}, limit u = {u}, find expected payout.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"Payout = E[X^u] - E[X^d] = {e_xu:.0f} - {e_xd:.0f} = {answer:.0f}",
            "explanation": "A deductible and limit together define the coverage range."
        }

    def coinsurance_calc(self) -> Dict[str, Any]:
        """
        Coinsurance: alpha*(E[(X-d)+])
        """
        theta = round(random.uniform(500, 5000), 0)
        d = round(random.uniform(100, theta), 0)
        alpha = round(random.uniform(0.7, 0.95), 2)

        limited_ex = theta * math.exp(-d / theta)
        answer = alpha * limited_ex

        d1 = limited_ex
        d2 = (1 - alpha) * limited_ex
        d3 = alpha * theta
        d4 = alpha * (theta - d)

        return {
            "id": "fam_062",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Coinsurance",
            "difficulty": "Easy",
            "question_text": f"With {alpha*100:.0f}% coinsurance and deductible d = {d} (theta = {theta}), find expected insurer payout.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"Payout = {alpha}*E[(X-{d})+] = {alpha}*{limited_ex:.0f} = {answer:.0f}",
            "explanation": "Coinsurance means the insured bears a percentage of losses above the deductible."
        }

    def inflation_with_deductible(self) -> Dict[str, Any]:
        """
        Inflation with deductible: E[((1+r)X - d)+]
        Adjust parameters with inflation rate
        """
        theta = round(random.uniform(500, 5000), 0)
        d = round(random.uniform(100, theta), 0)
        r = round(random.uniform(0.02, 0.08), 3)

        inflated_theta = theta * (1 + r)
        inflated_d = d
        answer = inflated_theta * math.exp(-inflated_d / inflated_theta)

        d1 = theta * math.exp(-d / theta)
        d2 = (1 + r) * theta * math.exp(-d / (theta * (1 + r)))
        d3 = inflated_theta * math.exp(-d / theta)
        d4 = theta * math.exp(-(inflated_d / theta) * (1 + r))

        return {
            "id": "fam_063",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Inflation with Deductible",
            "difficulty": "Hard",
            "question_text": f"With inflation r = {r}, theta = {theta}, deductible d = {d}, find expected payout.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"Payout = {inflated_theta:.0f}*e^(-{d}/{inflated_theta:.0f}) = {answer:.0f}",
            "explanation": "Inflation adjusts both severity and deductible values."
        }

    def per_payment_deductible(self) -> Dict[str, Any]:
        """
        Per-payment deductible: E[X-d | X>d] = E[(X-d)+] / (1-F(d))
        For exponential: theta
        """
        theta = round(random.uniform(500, 5000), 0)
        d = round(random.uniform(100, theta), 0)

        answer = theta

        d1 = theta - d
        d2 = theta * (1 - math.exp(-d / theta))
        d3 = theta * math.exp(-d / theta)
        d4 = d

        return {
            "id": "fam_064",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Per-Payment Deductible",
            "difficulty": "Medium",
            "question_text": f"For exponential (theta = {theta}) conditional on X > {d}, find E[X - {d} | X > {d}].",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"E[X-d|X>d] = theta = {answer}",
            "explanation": "For exponential, the conditional mean above a threshold equals the original parameter."
        }

    def increased_limit_factor(self) -> Dict[str, Any]:
        """
        ILF: E[X^u] / E[X^b] for Pareto
        """
        alpha = round(random.uniform(2, 5), 2)
        theta = round(random.uniform(1000, 5000), 0)
        b = round(random.uniform(theta, theta * 2), 0)
        u = round(random.uniform(b, b * 3), 0)

        e_xb = theta * (1 - (theta / b) ** (alpha - 1)) / (alpha - 1) if alpha > 1 else theta
        e_xu = theta * (1 - (theta / u) ** (alpha - 1)) / (alpha - 1) if alpha > 1 else theta

        answer = e_xu / e_xb if e_xb > 0 else 1

        d1 = e_xb / e_xu
        d2 = (u / b) ** (1 - alpha)
        d3 = ((theta + u) / (theta + b)) ** (alpha - 1)
        d4 = (alpha * u) / (alpha * b)

        return {
            "id": "fam_065",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Increased Limit Factor",
            "difficulty": "Hard",
            "question_text": f"For Pareto (alpha = {alpha}, theta = {theta}), find ILF({u}/{b}).",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"ILF = E[X^{u}]/E[X^{b}] = {e_xu:.0f}/{e_xb:.0f} = {answer:.4f}",
            "explanation": "The increased limit factor shows how coverage cost increases with higher limits."
        }

    # ======================== CRITICAL - ESTIMATION (5 methods) ========================

    def method_of_moments_exponential(self) -> Dict[str, Any]:
        """
        Method of moments: theta_hat = sample mean
        """
        true_theta = round(random.uniform(500, 5000), 0)
        n = random.randint(10, 100)
        sample_mean = round(random.uniform(true_theta * 0.8, true_theta * 1.2), 0)

        answer = sample_mean

        d1 = true_theta
        d2 = sample_mean * 0.9
        d3 = sample_mean / math.sqrt(n)
        d4 = sample_mean * math.sqrt(n)

        return {
            "id": "fam_066",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Method of Moments",
            "difficulty": "Easy",
            "question_text": f"Using method of moments with sample mean = {sample_mean}, estimate theta for exponential.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"theta_hat = sample mean = {answer}",
            "explanation": "For exponential, the method of moments estimator equals the sample mean."
        }

    def mle_exponential(self) -> Dict[str, Any]:
        """
        MLE for exponential: theta_hat = sample mean
        """
        true_theta = round(random.uniform(500, 5000), 0)
        n = random.randint(10, 100)
        sample_mean = round(random.uniform(true_theta * 0.8, true_theta * 1.2), 0)

        answer = sample_mean

        d1 = sample_mean * math.sqrt(n)
        d2 = sample_mean / math.sqrt(n)
        d3 = true_theta
        d4 = sample_mean * n

        return {
            "id": "fam_067",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "MLE - Exponential",
            "difficulty": "Easy",
            "question_text": f"Find the MLE of theta for exponential given sample mean = {sample_mean}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"theta_MLE = sample mean = {answer}",
            "explanation": "The MLE of exponential parameter equals the sample mean."
        }

    def chi_squared_goodness_of_fit(self) -> Dict[str, Any]:
        """
        Chi-squared: chi^2 = sum((O - E)^2 / E)
        """
        o_values = [random.randint(5, 30) for _ in range(4)]
        e_values = [round(v * random.uniform(0.8, 1.2), 1) for v in o_values]

        chi_sq = sum(((o_values[i] - e_values[i]) ** 2) / e_values[i] for i in range(len(o_values)))
        answer = chi_sq

        d1 = sum([o_values[i] - e_values[i] for i in range(len(o_values))])
        d2 = sum([(o_values[i] - e_values[i]) ** 2 for i in range(len(o_values))])
        d3 = sum([o_values[i] / e_values[i] for i in range(len(o_values))])
        d4 = chi_sq * 0.5

        return {
            "id": "fam_068",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Chi-Squared GOF",
            "difficulty": "Medium",
            "question_text": f"Compute chi-squared with observed {o_values} and expected {e_values}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"chi^2 = sum((O-E)^2/E) = {answer:.4f}",
            "explanation": "Chi-squared goodness-of-fit tests distributional fit."
        }

    def kolmogorov_smirnov_statistic(self) -> Dict[str, Any]:
        """
        KS statistic: D = max|F_empirical - F_theoretical|
        """
        cdf_empir = [round(random.uniform(0, 1), 3) for _ in range(5)]
        cdf_empir.sort()
        cdf_theory = [round(random.uniform(0, 1), 3) for _ in range(5)]

        ks_stat = max([abs(cdf_empir[i] - cdf_theory[i]) for i in range(len(cdf_empir))])
        answer = ks_stat

        d1 = sum([abs(cdf_empir[i] - cdf_theory[i]) for i in range(len(cdf_empir))]) / len(cdf_empir)
        d2 = max([abs(cdf_theory[i] - cdf_empir[i]) for i in range(len(cdf_theory))])
        d3 = sum([cdf_empir[i] - cdf_theory[i] for i in range(len(cdf_empir))])
        d4 = math.sqrt(sum([(cdf_empir[i] - cdf_theory[i]) ** 2 for i in range(len(cdf_empir))]))

        return {
            "id": "fam_069",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Kolmogorov-Smirnov",
            "difficulty": "Medium",
            "question_text": f"Find KS statistic D with empirical CDF {cdf_empir} and theoretical {cdf_theory}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"D = max|F_e - F_t| = {answer:.4f}",
            "explanation": "The KS statistic measures the maximum vertical distance between CDFs."
        }

    def likelihood_ratio_test(self) -> Dict[str, Any]:
        """
        LRT: -2*ln(L0/L1) = -2*(ln(L0) - ln(L1))
        """
        ln_l0 = round(random.uniform(-100, -50), 2)
        ln_l1 = round(random.uniform(-50, -10), 2)

        answer = -2 * (ln_l0 - ln_l1)

        d1 = ln_l0 - ln_l1
        d2 = 2 * (ln_l1 - ln_l0)
        d3 = (ln_l0 ** 2) - (ln_l1 ** 2)
        d4 = -2 * ln_l0 / ln_l1

        return {
            "id": "fam_070",
            "exam": self.exam,
            "topic": "FAM Short-Term",
            "subtopic": "Likelihood Ratio Test",
            "difficulty": "Easy",
            "question_text": f"Compute -2*ln(L0/L1) with ln(L0) = {ln_l0}, ln(L1) = {ln_l1}.",
            "choices": self.make_choices(answer, [d1, d2, d3, d4]),
            "solution": f"-2*ln(L0/L1) = -2*({ln_l0} - {ln_l1}) = {answer:.2f}",
            "explanation": "The likelihood ratio test compares two competing models."
        }

    # ======================== Class Methods ========================

    @classmethod
    def get_all_methods(cls):
        """Return list of all question-generating methods."""
        exclude = {'get_all_methods', 'generate_all', 'format_number', 'make_choices'}
        return [m for m in dir(cls) if not m.startswith('_') and callable(getattr(cls, m)) and m not in exclude]

    @classmethod
    def generate_all(cls, n_per_method: int = 100):
        """
        Generate all questions from all methods.

        Args:
            n_per_method: Number of questions per method (default 100)

        Returns:
            List of all generated question dicts
        """
        questions = []
        methods = cls.get_all_methods()
        for i, method_name in enumerate(methods):
            for j in range(n_per_method):
                try:
                    gen = cls(seed=i * 10000 + j)
                    q = getattr(gen, method_name)()
                    questions.append(q)
                except Exception:
                    pass
        return questions
