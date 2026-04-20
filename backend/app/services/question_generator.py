"""
Question generator for dynamic question generation from templates.

Supports variable substitution, expression evaluation, and procedural distractor generation
for realistic and pedagogically valuable question variants.
"""

import random
import re
from typing import Any, Dict, List, Optional
from decimal import Decimal, ROUND_HALF_UP


class QuestionGenerator:
    """
    Generate questions from templates with variable substitution and distractor generation.
    """

    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the question generator.

        Args:
            seed: Optional random seed for reproducibility.
        """
        if seed is not None:
            random.seed(seed)

    def evaluate_expression(self, expression: str, variables: dict) -> float:
        """
        Safely evaluate mathematical expressions with variable substitution.

        Supports basic arithmetic operators and mathematical functions.
        Uses a restricted eval context to prevent code injection.

        Args:
            expression: Mathematical expression string (e.g., "P * (1 + r)**n").
            variables: Dict mapping variable names to their values.

        Returns:
            Evaluated result as float.

        Raises:
            ValueError: If expression cannot be evaluated safely.
        """
        # Remove whitespace
        expression = expression.strip()

        # Safe namespace for eval
        safe_dict = {
            '__builtins__': {
                'abs': abs,
                'round': round,
                'min': min,
                'max': max,
                'pow': pow,
            },
            'exp': __import__('math').exp,
            'log': __import__('math').log,
            'log10': __import__('math').log10,
            'sqrt': __import__('math').sqrt,
            'sin': __import__('math').sin,
            'cos': __import__('math').cos,
            'tan': __import__('math').tan,
            'pi': __import__('math').pi,
            'e': __import__('math').e,
        }

        # Add variables to safe dict
        safe_dict.update(variables)

        try:
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return float(result)
        except Exception as e:
            raise ValueError(f"Cannot evaluate expression '{expression}': {str(e)}")

    def render_template(self, template_text: str, variables: dict) -> str:
        """
        Render a template by substituting variables and computed expressions.

        Supports:
        - Simple substitution: {variable_name}
        - Computed expressions: {expression} where expression uses variables

        Args:
            template_text: Template string with {placeholders}.
            variables: Dict mapping variable names to values.

        Returns:
            Rendered template string.
        """
        result = template_text

        # Find all placeholders {xxx}
        placeholders = re.findall(r'\{([^}]+)\}', template_text)

        for placeholder in placeholders:
            if placeholder in variables:
                # Direct variable substitution
                value = variables[placeholder]
                result = result.replace(f'{{{placeholder}}}', str(value))
            else:
                # Try to evaluate as expression
                try:
                    computed_value = self.evaluate_expression(placeholder, variables)
                    result = result.replace(f'{{{placeholder}}}', str(computed_value))
                except ValueError:
                    # If evaluation fails, leave placeholder as is
                    pass

        return result

    def generate_distractors(
        self,
        correct_answer: float,
        distractor_config: dict
    ) -> List[float]:
        """
        Generate plausible wrong answers (distractors) for a multiple choice question.

        Generates distractors based on common mistakes:
        - Off-by-one errors
        - Sign errors
        - Formula confusion (e.g., using simple interest instead of compound)
        - Calculation errors (forgetting parentheses, etc.)

        Args:
            correct_answer: The correct numerical answer.
            distractor_config: Dict with keys:
                - 'method': str, method for generating distractors
                  ('common_errors', 'percentage_off', 'formula_mistakes')
                - 'count': int, number of distractors to generate (default 4)
                - 'magnitude_factor': float, scale for error magnitude (default 1.0)

        Returns:
            List of distractor values (floats).
        """
        method = distractor_config.get('method', 'common_errors')
        count = distractor_config.get('count', 4)
        magnitude_factor = distractor_config.get('magnitude_factor', 1.0)

        distractors = set()

        if method == 'percentage_off':
            # Generate answers that are N% off
            percentages = [-50, -20, -10, 10, 20, 50, 100]
            for pct in percentages:
                if len(distractors) >= count:
                    break
                distractor = correct_answer * (1 + pct / 100.0)
                distractors.add(float(distractor))

        elif method == 'formula_mistakes':
            # Simulate common formula mistakes
            distractors.add(correct_answer * 2)  # Forgot to divide
            distractors.add(correct_answer / 2)  # Forgot to multiply
            distractors.add(abs(correct_answer) * -1)  # Sign error
            distractors.add(correct_answer + 1)  # Off-by-one
            distractors.add(correct_answer - 1)  # Off-by-one

        else:  # 'common_errors' (default)
            # Magnitude-scaled errors
            error_base = abs(correct_answer) * magnitude_factor

            # Off-by-one in base unit
            distractors.add(correct_answer + error_base * 0.1)
            distractors.add(correct_answer - error_base * 0.1)

            # Sign error
            distractors.add(-correct_answer)

            # Factor of 2 error (common in finance)
            distractors.add(correct_answer * 2)
            distractors.add(correct_answer / 2)

            # Percentage errors
            distractors.add(correct_answer * 1.1)
            distractors.add(correct_answer * 0.9)

        # Remove exact duplicates and the correct answer
        distractors.discard(correct_answer)

        # Convert to list and remove very close values (within 0.01%)
        distractor_list = sorted(list(distractors))
        filtered = []
        for d in distractor_list:
            is_close = any(
                abs(d - f) < abs(correct_answer) * 0.0001
                for f in filtered
            )
            if not is_close:
                filtered.append(d)

        # Return requested count
        return filtered[:count]

    def generate_from_template(self, template: dict) -> dict:
        """
        Generate a question from a template by instantiating variables.

        Args:
            template: Template dict with keys:
                - 'id': str, unique template identifier
                - 'exam': str, exam name (P, FM, FAM, etc.)
                - 'topic': str, topic identifier
                - 'difficulty': float, difficulty (0-1)
                - 'variables_config': dict mapping var_name -> {type, range or values}
                - 'template_text': str, question text with {placeholders}
                - 'solution_template': str, expression for correct answer
                - 'distractor_config': dict, configuration for distractor generation
                - 'explanation_template': str, explanation template
                - 'tags': list, topic tags

        Returns:
            Generated question dict with keys:
                - 'id': str, unique question id
                - 'exam': str
                - 'topic': str
                - 'difficulty': float
                - 'text': str, rendered question text
                - 'correct_answer': float
                - 'options': list of floats (correct answer first, then distractors)
                - 'explanation': str
                - 'variables': dict, instantiated variables
                - 'tags': list
                - 'irt_parameters': dict with a, b, c estimates

        Raises:
            ValueError: If template is invalid or generation fails.
        """
        if not template:
            raise ValueError("Template cannot be empty")

        # Generate variable values
        variables = {}
        variables_config = template.get('variables_config', {})

        for var_name, var_spec in variables_config.items():
            var_type = var_spec.get('type', 'float')

            if var_type == 'int':
                min_val = var_spec.get('min', 0)
                max_val = var_spec.get('max', 100)
                variables[var_name] = random.randint(min_val, max_val)

            elif var_type == 'float':
                min_val = var_spec.get('min', 0.0)
                max_val = var_spec.get('max', 100.0)
                decimals = var_spec.get('decimals', 2)
                value = random.uniform(min_val, max_val)
                variables[var_name] = round(value, decimals)

            elif var_type == 'choice':
                choices = var_spec.get('choices', [])
                variables[var_name] = random.choice(choices)

            elif var_type == 'percent':
                min_pct = var_spec.get('min', 0.0)
                max_pct = var_spec.get('max', 100.0)
                decimals = var_spec.get('decimals', 1)
                value = random.uniform(min_pct, max_pct)
                variables[var_name] = round(value, decimals)

            else:
                # Default: float
                min_val = var_spec.get('min', 0.0)
                max_val = var_spec.get('max', 100.0)
                variables[var_name] = random.uniform(min_val, max_val)

        # Render question text
        template_text = template.get('template_text', '')
        question_text = self.render_template(template_text, variables)

        # Compute correct answer
        solution_template = template.get('solution_template', '')
        try:
            correct_answer = self.evaluate_expression(solution_template, variables)
        except ValueError as e:
            raise ValueError(f"Cannot compute answer for template {template.get('id')}: {str(e)}")

        # Round answer appropriately
        answer_decimals = template.get('answer_decimals', 2)
        correct_answer = round(correct_answer, answer_decimals)

        # Generate distractors
        distractor_config = template.get('distractor_config', {'method': 'common_errors', 'count': 4})
        distractors = self.generate_distractors(correct_answer, distractor_config)

        # Ensure we have exactly 4 distractors
        while len(distractors) < 4:
            offset = random.uniform(-abs(correct_answer) * 0.2, abs(correct_answer) * 0.2)
            distractor = round(correct_answer + offset, answer_decimals)
            if distractor != correct_answer and distractor not in distractors:
                distractors.append(distractor)

        distractors = distractors[:4]

        # Shuffle options (keep correct answer)
        all_options = [correct_answer] + distractors
        random.shuffle(all_options)

        # Render explanation
        explanation_template = template.get('explanation_template', '')
        explanation = self.render_template(explanation_template, variables)

        # Estimate IRT parameters based on difficulty
        difficulty = template.get('difficulty', 0.5)
        irt_a = 1.0 + difficulty  # Discrimination increases with difficulty
        irt_b = (difficulty - 0.5) * 4  # Difficulty parameter
        irt_c = 0.25  # Guessing parameter

        # Generate unique question ID
        question_id = f"{template.get('id')}_{random.randint(10000, 99999)}"

        return {
            'id': question_id,
            'template_id': template.get('id'),
            'exam': template.get('exam', 'Unknown'),
            'topic': template.get('topic', 'Unknown'),
            'difficulty': float(difficulty),
            'text': question_text,
            'correct_answer': float(correct_answer),
            'options': [float(opt) for opt in all_options],
            'explanation': explanation,
            'variables': variables,
            'tags': template.get('tags', []),
            'irt_parameters': {
                'a': irt_a,
                'b': irt_b,
                'c': irt_c,
            }
        }


# Template library with comprehensive question templates for each exam

TEMPLATE_LIBRARY = {
    # ========== EXAM P: Probability ==========

    'exam_p_basic_probability_1': {
        'id': 'exam_p_basic_probability_1',
        'exam': 'P',
        'topic': 'Basic Probability',
        'difficulty': 0.3,
        'template_text': (
            'A bag contains {red_balls} red balls and {blue_balls} blue balls. '
            'If you draw one ball at random without replacement, what is the probability '
            'of drawing a red ball?'
        ),
        'variables_config': {
            'red_balls': {'type': 'int', 'min': 2, 'max': 8},
            'blue_balls': {'type': 'int', 'min': 2, 'max': 8},
        },
        'solution_template': 'red_balls / (red_balls + blue_balls)',
        'answer_decimals': 4,
        'distractor_config': {
            'method': 'formula_mistakes',
            'count': 4,
            'magnitude_factor': 0.5,
        },
        'explanation_template': (
            'Probability = (number of favorable outcomes) / (total outcomes) = '
            '{red_balls} / {red_balls + blue_balls}'
        ),
        'tags': ['probability', 'classical_probability'],
    },

    'exam_p_conditional_probability_1': {
        'id': 'exam_p_conditional_probability_1',
        'exam': 'P',
        'topic': 'Conditional Probability',
        'difficulty': 0.5,
        'template_text': (
            'Given P(A) = {prob_a}, P(B) = {prob_b}, and P(A ∩ B) = {prob_ab}, '
            'find P(A|B), the probability of A given B.'
        ),
        'variables_config': {
            'prob_a': {'type': 'float', 'min': 0.2, 'max': 0.8, 'decimals': 2},
            'prob_b': {'type': 'float', 'min': 0.2, 'max': 0.8, 'decimals': 2},
        },
        'solution_template': 'prob_a * prob_b / prob_b',  # P(A|B) = P(A∩B)/P(B)
        'answer_decimals': 4,
        'distractor_config': {
            'method': 'common_errors',
            'count': 4,
        },
        'explanation_template': (
            'By conditional probability formula: P(A|B) = P(A∩B) / P(B) = {prob_ab} / {prob_b}'
        ),
        'tags': ['conditional_probability', 'bayes_theorem'],
    },

    'exam_p_poisson_distribution_1': {
        'id': 'exam_p_poisson_distribution_1',
        'exam': 'P',
        'topic': 'Poisson Distribution',
        'difficulty': 0.6,
        'template_text': (
            'The number of claims filed with an insurance company follows a Poisson distribution '
            'with mean λ = {lambda_param}. What is the probability of exactly {k} claims?'
        ),
        'variables_config': {
            'lambda_param': {'type': 'float', 'min': 1.0, 'max': 5.0, 'decimals': 1},
            'k': {'type': 'int', 'min': 0, 'max': 5},
        },
        'solution_template': (
            '(__import__("math").exp(-lambda_param) * (lambda_param ** k)) / '
            '__import__("math").factorial(k)'
        ),
        'answer_decimals': 4,
        'distractor_config': {
            'method': 'percentage_off',
            'count': 4,
        },
        'explanation_template': (
            'Poisson PMF: P(X=k) = (e^(-λ) * λ^k) / k! = '
            '(e^(-{lambda_param}) * {lambda_param}^{k}) / {k}!'
        ),
        'tags': ['poisson', 'distributions'],
    },

    'exam_p_normal_distribution_1': {
        'id': 'exam_p_normal_distribution_1',
        'exam': 'P',
        'topic': 'Normal Distribution',
        'difficulty': 0.55,
        'template_text': (
            'A random variable X is normally distributed with mean μ = {mean} and '
            'standard deviation σ = {stdev}. Find P(X < {value}).'
        ),
        'variables_config': {
            'mean': {'type': 'float', 'min': 0, 'max': 100, 'decimals': 0},
            'stdev': {'type': 'float', 'min': 5, 'max': 30, 'decimals': 0},
        },
        'solution_template': (
            '__import__("scipy.stats").norm.cdf({value}, loc={mean}, scale={stdev})'
        ),
        'answer_decimals': 4,
        'distractor_config': {
            'method': 'common_errors',
            'count': 4,
        },
        'explanation_template': (
            'Standardize: Z = ({value} - {mean}) / {stdev}, then use standard normal table.'
        ),
        'tags': ['normal_distribution', 'continuous_distributions'],
    },

    'exam_p_exponential_distribution_1': {
        'id': 'exam_p_exponential_distribution_1',
        'exam': 'P',
        'topic': 'Exponential Distribution',
        'difficulty': 0.5,
        'template_text': (
            'The time until failure of a device follows an exponential distribution '
            'with rate λ = {lambda_param} failures per year. What is the mean time to failure?'
        ),
        'variables_config': {
            'lambda_param': {'type': 'float', 'min': 0.1, 'max': 2.0, 'decimals': 2},
        },
        'solution_template': '1 / lambda_param',
        'answer_decimals': 3,
        'distractor_config': {
            'method': 'formula_mistakes',
            'count': 4,
        },
        'explanation_template': (
            'For exponential distribution with rate λ, mean = 1/λ = 1/{lambda_param}'
        ),
        'tags': ['exponential', 'distributions'],
    },

    'exam_p_binomial_distribution_1': {
        'id': 'exam_p_binomial_distribution_1',
        'exam': 'P',
        'topic': 'Binomial Distribution',
        'difficulty': 0.5,
        'template_text': (
            'A coin is flipped {n} times with probability of heads p = {prob}. '
            'What is the expected number of heads?'
        ),
        'variables_config': {
            'n': {'type': 'int', 'min': 5, 'max': 20},
            'prob': {'type': 'float', 'min': 0.3, 'max': 0.7, 'decimals': 2},
        },
        'solution_template': 'n * prob',
        'answer_decimals': 2,
        'distractor_config': {
            'method': 'common_errors',
            'count': 4,
        },
        'explanation_template': (
            'For binomial distribution, E[X] = n*p = {n} * {prob}'
        ),
        'tags': ['binomial', 'distributions', 'expected_value'],
    },

    # ========== EXAM FM: Financial Mathematics ==========

    'exam_fm_time_value_money_1': {
        'id': 'exam_fm_time_value_money_1',
        'exam': 'FM',
        'topic': 'Time Value of Money',
        'difficulty': 0.4,
        'template_text': (
            'An investor deposits ${principal} today at an annual interest rate of {rate}%. '
            'What is the value of this investment after {years} years (simple interest)?'
        ),
        'variables_config': {
            'principal': {'type': 'float', 'min': 1000, 'max': 10000, 'decimals': 0},
            'rate': {'type': 'float', 'min': 2, 'max': 8, 'decimals': 1},
            'years': {'type': 'int', 'min': 2, 'max': 10},
        },
        'solution_template': 'principal * (1 + rate/100 * years)',
        'answer_decimals': 2,
        'distractor_config': {
            'method': 'formula_mistakes',
            'count': 4,
        },
        'explanation_template': (
            'Simple Interest: FV = P(1 + rt) = {principal}(1 + {rate/100} * {years})'
        ),
        'tags': ['time_value', 'interest'],
    },

    'exam_fm_compound_interest_1': {
        'id': 'exam_fm_compound_interest_1',
        'exam': 'FM',
        'topic': 'Compound Interest',
        'difficulty': 0.5,
        'template_text': (
            'What is the present value of ${future_amount} to be received in {years} years, '
            'if the interest rate is {rate}% per year (compounded annually)?'
        ),
        'variables_config': {
            'future_amount': {'type': 'float', 'min': 5000, 'max': 20000, 'decimals': 0},
            'rate': {'type': 'float', 'min': 2, 'max': 8, 'decimals': 1},
            'years': {'type': 'int', 'min': 3, 'max': 10},
        },
        'solution_template': 'future_amount / ((1 + rate/100) ** years)',
        'answer_decimals': 2,
        'distractor_config': {
            'method': 'common_errors',
            'count': 4,
        },
        'explanation_template': (
            'PV = FV / (1 + i)^n = {future_amount} / (1 + {rate/100})^{years}'
        ),
        'tags': ['present_value', 'compound_interest'],
    },

    'exam_fm_annuity_ordinary_1': {
        'id': 'exam_fm_annuity_ordinary_1',
        'exam': 'FM',
        'topic': 'Annuities',
        'difficulty': 0.6,
        'template_text': (
            'An ordinary annuity pays ${payment} per year for {years} years. '
            'The discount rate is {rate}% per year. What is the present value of this annuity?'
        ),
        'variables_config': {
            'payment': {'type': 'float', 'min': 1000, 'max': 5000, 'decimals': 0},
            'rate': {'type': 'float', 'min': 3, 'max': 8, 'decimals': 1},
            'years': {'type': 'int', 'min': 5, 'max': 20},
        },
        'solution_template': (
            'payment * (1 - (1 + rate/100)**(-years)) / (rate/100)'
        ),
        'answer_decimals': 2,
        'distractor_config': {
            'method': 'percentage_off',
            'count': 4,
        },
        'explanation_template': (
            'PV of ordinary annuity: a_n = PMT * [1-(1+i)^(-n)] / i'
        ),
        'tags': ['annuity', 'present_value'],
    },

    'exam_fm_bond_pricing_1': {
        'id': 'exam_fm_bond_pricing_1',
        'exam': 'FM',
        'topic': 'Bond Pricing',
        'difficulty': 0.6,
        'template_text': (
            'A bond has a face value of ${face_value}, pays a coupon of {coupon_rate}% annually, '
            'and matures in {years} years. If the yield to maturity is {ytm}%, what is the bond price?'
        ),
        'variables_config': {
            'face_value': {'type': 'float', 'min': 1000, 'max': 1000, 'decimals': 0},
            'coupon_rate': {'type': 'float', 'min': 3, 'max': 7, 'decimals': 1},
            'ytm': {'type': 'float', 'min': 2, 'max': 8, 'decimals': 1},
            'years': {'type': 'int', 'min': 5, 'max': 20},
        },
        'solution_template': (
            'coupon_rate/100 * face_value * (1 - (1 + ytm/100)**(-years)) / (ytm/100) + '
            'face_value / ((1 + ytm/100)**years)'
        ),
        'answer_decimals': 2,
        'distractor_config': {
            'method': 'common_errors',
            'count': 4,
        },
        'explanation_template': (
            'Bond Price = PV of coupons + PV of face value'
        ),
        'tags': ['bonds', 'valuation'],
    },

    'exam_fm_loan_amortization_1': {
        'id': 'exam_fm_loan_amortization_1',
        'exam': 'FM',
        'topic': 'Loan Amortization',
        'difficulty': 0.5,
        'template_text': (
            'A loan of ${principal} is to be repaid with equal annual payments over {years} years '
            'at {rate}% annual interest. What is the annual payment amount?'
        ),
        'variables_config': {
            'principal': {'type': 'float', 'min': 50000, 'max': 200000, 'decimals': 0},
            'rate': {'type': 'float', 'min': 3, 'max': 8, 'decimals': 1},
            'years': {'type': 'int', 'min': 5, 'max': 30},
        },
        'solution_template': (
            'principal * (rate/100) / (1 - (1 + rate/100)**(-years))'
        ),
        'answer_decimals': 2,
        'distractor_config': {
            'method': 'formula_mistakes',
            'count': 4,
        },
        'explanation_template': (
            'Payment = P * i / (1 - (1+i)^(-n))'
        ),
        'tags': ['amortization', 'loans'],
    },

    # ========== EXAM FAM: Fundamentals of Actuarial Models ==========

    'exam_fam_survival_probability_1': {
        'id': 'exam_fam_survival_probability_1',
        'exam': 'FAM',
        'topic': 'Survival Models',
        'difficulty': 0.5,
        'template_text': (
            'Given that the survival probability p_x = {px}, what is the mortality probability q_x?'
        ),
        'variables_config': {
            'px': {'type': 'float', 'min': 0.85, 'max': 0.99, 'decimals': 4},
        },
        'solution_template': '1 - px',
        'answer_decimals': 4,
        'distractor_config': {
            'method': 'common_errors',
            'count': 4,
        },
        'explanation_template': (
            'q_x = 1 - p_x = 1 - {px}'
        ),
        'tags': ['survival', 'mortality'],
    },

    'exam_fam_life_table_1': {
        'id': 'exam_fam_life_table_1',
        'exam': 'FAM',
        'topic': 'Life Tables',
        'difficulty': 0.5,
        'template_text': (
            'In a life table, l_x = {lx} (number alive at age x) and l_x+1 = {lx1}. '
            'How many people died between age x and x+1 (d_x)?'
        ),
        'variables_config': {
            'lx': {'type': 'int', 'min': 90000, 'max': 99000},
            'lx1': {'type': 'int', 'min': 85000, 'max': 99000},
        },
        'solution_template': 'lx - lx1',
        'answer_decimals': 0,
        'distractor_config': {
            'method': 'formula_mistakes',
            'count': 4,
        },
        'explanation_template': (
            'd_x = l_x - l_(x+1) = {lx} - {lx1}'
        ),
        'tags': ['life_table', 'mortality'],
    },

    'exam_fam_present_value_benefits_1': {
        'id': 'exam_fam_present_value_benefits_1',
        'exam': 'FAM',
        'topic': 'Insurance Valuation',
        'difficulty': 0.6,
        'template_text': (
            'A life insurance benefit of ${benefit} is payable at the end of the year of death. '
            'The probability of death at age x is {qx}, and the discount rate is {rate}%. '
            'What is the present value of this benefit?'
        ),
        'variables_config': {
            'benefit': {'type': 'float', 'min': 100000, 'max': 500000, 'decimals': 0},
            'qx': {'type': 'float', 'min': 0.001, 'max': 0.02, 'decimals': 4},
            'rate': {'type': 'float', 'min': 2, 'max': 6, 'decimals': 1},
        },
        'solution_template': 'benefit * qx / (1 + rate/100)',
        'answer_decimals': 2,
        'distractor_config': {
            'method': 'common_errors',
            'count': 4,
        },
        'explanation_template': (
            'PV = Benefit * q_x * v = {benefit} * {qx} * 1/{1 + rate/100}'
        ),
        'tags': ['insurance_pricing', 'present_value'],
    },

    # ========== EXAM ALTAM: Advanced Life Contingencies ==========

    'exam_altam_multi_state_1': {
        'id': 'exam_altam_multi_state_1',
        'exam': 'ALTAM',
        'topic': 'Multi-State Models',
        'difficulty': 0.7,
        'template_text': (
            'In a 3-state model (Healthy, Sick, Dead), the transition probability '
            'from Healthy to Sick is {prob_hs}. What is the probability of remaining '
            'Healthy (not transitioning)?'
        ),
        'variables_config': {
            'prob_hs': {'type': 'float', 'min': 0.01, 'max': 0.1, 'decimals': 3},
        },
        'solution_template': '1 - prob_hs',
        'answer_decimals': 3,
        'distractor_config': {
            'method': 'common_errors',
            'count': 4,
        },
        'explanation_template': (
            'P(stay in Healthy) = 1 - P(Healthy→Sick) = 1 - {prob_hs}'
        ),
        'tags': ['multi_state', 'transitions'],
    },

    'exam_altam_joint_life_1': {
        'id': 'exam_altam_joint_life_1',
        'exam': 'ALTAM',
        'topic': 'Joint Life',
        'difficulty': 0.6,
        'template_text': (
            'For two independent lives, p_x = {px} and p_y = {py}. '
            'What is the joint survival probability (both alive after 1 year)?'
        ),
        'variables_config': {
            'px': {'type': 'float', 'min': 0.90, 'max': 0.99, 'decimals': 4},
            'py': {'type': 'float', 'min': 0.90, 'max': 0.99, 'decimals': 4},
        },
        'solution_template': 'px * py',
        'answer_decimals': 4,
        'distractor_config': {
            'method': 'formula_mistakes',
            'count': 4,
        },
        'explanation_template': (
            'p_(xy) = p_x * p_y = {px} * {py}'
        ),
        'tags': ['joint_life', 'multiple_lives'],
    },

    # ========== EXAM ASTAM: Advanced Short-Term Actuarial Mathematics ==========

    'exam_astam_aggregate_loss_1': {
        'id': 'exam_astam_aggregate_loss_1',
        'exam': 'ASTAM',
        'topic': 'Aggregate Loss Models',
        'difficulty': 0.7,
        'template_text': (
            'In an aggregate loss model S = X_1 + X_2 + ... + X_N, where N ~ Poisson(λ = {lambda}), '
            'and each claim X_i ~ Exp(β = {beta}), find E[S].'
        ),
        'variables_config': {
            'lambda': {'type': 'float', 'min': 10, 'max': 100, 'decimals': 1},
            'beta': {'type': 'float', 'min': 1000, 'max': 10000, 'decimals': 0},
        },
        'solution_template': 'lambda * beta',
        'answer_decimals': 0,
        'distractor_config': {
            'method': 'percentage_off',
            'count': 4,
        },
        'explanation_template': (
            'E[S] = E[N] * E[X] = {lambda} * {beta}'
        ),
        'tags': ['aggregate_loss', 'expected_value'],
    },

    'exam_astam_credibility_1': {
        'id': 'exam_astam_credibility_1',
        'exam': 'ASTAM',
        'topic': 'Credibility Theory',
        'difficulty': 0.6,
        'template_text': (
            'Using Bühlmann credibility with credibility factor Z = {z}, '
            'observed claim amount X_bar = {x_bar}, and collective mean μ = {mu}, '
            'find the credibility premium.'
        ),
        'variables_config': {
            'z': {'type': 'float', 'min': 0.3, 'max': 0.7, 'decimals': 2},
            'x_bar': {'type': 'float', 'min': 1000, 'max': 5000, 'decimals': 0},
            'mu': {'type': 'float', 'min': 1000, 'max': 5000, 'decimals': 0},
        },
        'solution_template': 'z * x_bar + (1 - z) * mu',
        'answer_decimals': 2,
        'distractor_config': {
            'method': 'common_errors',
            'count': 4,
        },
        'explanation_template': (
            'Credibility Premium = Z * X̄ + (1-Z) * μ = {z} * {x_bar} + {1-z} * {mu}'
        ),
        'tags': ['credibility', 'bayesian'],
    },

    # ========== EXAM SRM: Statistical Learning & Regression Modeling ==========

    'exam_srm_linear_regression_1': {
        'id': 'exam_srm_linear_regression_1',
        'exam': 'SRM',
        'topic': 'Linear Regression',
        'difficulty': 0.6,
        'template_text': (
            'In a simple linear regression Y = β_0 + β_1*X + ε, given that the '
            'slope β_1 = {beta_1} and intercept β_0 = {beta_0}, what is the predicted '
            'value of Y when X = {x_value}?'
        ),
        'variables_config': {
            'beta_1': {'type': 'float', 'min': 0.5, 'max': 5.0, 'decimals': 2},
            'beta_0': {'type': 'float', 'min': 10, 'max': 100, 'decimals': 0},
            'x_value': {'type': 'float', 'min': 5, 'max': 50, 'decimals': 0},
        },
        'solution_template': 'beta_0 + beta_1 * x_value',
        'answer_decimals': 2,
        'distractor_config': {
            'method': 'formula_mistakes',
            'count': 4,
        },
        'explanation_template': (
            'Ŷ = {beta_0} + {beta_1} * {x_value}'
        ),
        'tags': ['regression', 'prediction'],
    },

    'exam_srm_glm_poisson_1': {
        'id': 'exam_srm_glm_poisson_1',
        'exam': 'SRM',
        'topic': 'Generalized Linear Models',
        'difficulty': 0.7,
        'template_text': (
            'In a Poisson GLM, the linear predictor is η = {beta_0} + {beta_1}*X. '
            'Using the log link, what is E[Y] when X = {x_value}?'
        ),
        'variables_config': {
            'beta_0': {'type': 'float', 'min': -1, 'max': 2, 'decimals': 2},
            'beta_1': {'type': 'float', 'min': 0.1, 'max': 0.5, 'decimals': 2},
            'x_value': {'type': 'float', 'min': 10, 'max': 50, 'decimals': 0},
        },
        'solution_template': '__import__("math").exp(beta_0 + beta_1 * x_value)',
        'answer_decimals': 2,
        'distractor_config': {
            'method': 'percentage_off',
            'count': 4,
        },
        'explanation_template': (
            'E[Y] = exp(η) = exp({beta_0} + {beta_1} * {x_value})'
        ),
        'tags': ['glm', 'poisson'],
    },
}
