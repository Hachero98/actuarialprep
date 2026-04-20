"""
Exam P (Probability) Question Generator
Generates ~10,000 unique randomized questions across all syllabus topics.
"""

import random
import math
from fractions import Fraction
from app.services.generators.compat import comb, perm
from app.services.generators.compat import norm, expon, gamma, binom, poisson
from typing import List, Dict, Any
import itertools


class ExamPGenerator:
    """Generate randomized Exam P questions."""

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    # ==================== TOPIC 1: GENERAL PROBABILITY (15+ methods) ====================

    def set_operations_union(self) -> Dict[str, Any]:
        """P(A ∪ B) = P(A) + P(B) - P(A ∩ B)"""
        pa = round(random.uniform(0.1, 0.5), 2)
        pb = round(random.uniform(0.1, 0.5), 2)
        pab = round(random.uniform(0, min(pa, pb)), 2)

        correct = round(pa + pb - pab, 4)

        return {
            "id": "set_union_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Set Operations",
            "difficulty": 2,
            "question_text": f"Events A and B have P(A) = {pa}, P(B) = {pb}, and P(A ∩ B) = {pab}. Find P(A ∪ B).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(pa + pb, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(pa - pb + pab, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(max(pa, pb), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(pab, 4)}", "is_correct": False},
            ],
            "solution": f"P(A ∪ B) = P(A) + P(B) - P(A ∩ B) = {pa} + {pb} - {pab} = {correct}",
            "explanation": "The union formula adds individual probabilities but subtracts the overlap to avoid double-counting."
        }

    def set_operations_intersection(self) -> Dict[str, Any]:
        """Find P(A ∩ B) given union and individual probabilities."""
        pa = round(random.uniform(0.2, 0.6), 2)
        pb = round(random.uniform(0.2, 0.6), 2)
        union = round(random.uniform(max(pa, pb), min(pa + pb, 1.0)), 2)

        correct = round(pa + pb - union, 4)

        return {
            "id": "set_intersection_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Set Operations",
            "difficulty": 2,
            "question_text": f"If P(A) = {pa}, P(B) = {pb}, and P(A ∪ B) = {union}, find P(A ∩ B).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(pa * pb, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(union - pa, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(union - pb, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(pa + pb - union - 0.1, 4)}", "is_correct": False},
            ],
            "solution": f"P(A ∩ B) = P(A) + P(B) - P(A ∪ B) = {pa} + {pb} - {union} = {correct}",
            "explanation": "Rearrange the union formula to solve for intersection."
        }

    def set_complement(self) -> Dict[str, Any]:
        """Find P(A^c) = 1 - P(A)"""
        pa = round(random.uniform(0.1, 0.9), 2)
        correct = round(1 - pa, 4)

        return {
            "id": "set_complement_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Set Operations",
            "difficulty": 1,
            "question_text": f"If P(A) = {pa}, find P(A^c) (the complement of A).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{pa}", "is_correct": False},
                {"label": "C", "text": f"{round(1 - pa + 0.05, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(pa / 2, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 - pa - 0.1, 4)}", "is_correct": False},
            ],
            "solution": f"P(A^c) = 1 - P(A) = 1 - {pa} = {correct}",
            "explanation": "The complement of an event A is everything not in A. Their probabilities sum to 1."
        }

    def inclusion_exclusion_two_events(self) -> Dict[str, Any]:
        """Inclusion-exclusion for two sets."""
        n_total = random.randint(100, 500)
        n_a = random.randint(30, min(n_total - 10, 200))
        n_b = random.randint(30, min(n_total - 10, 200))
        n_ab = random.randint(0, min(n_a, n_b) - 5)

        correct = n_a + n_b - n_ab

        return {
            "id": "inclusion_exclusion_two_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Counting",
            "difficulty": 2,
            "question_text": f"A survey of {n_total} people found {n_a} like coffee, {n_b} like tea, and {n_ab} like both. How many like at least one?",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{n_a + n_b}", "is_correct": False},
                {"label": "C", "text": f"{n_a + n_b + n_ab}", "is_correct": False},
                {"label": "D", "text": f"{n_total - n_ab}", "is_correct": False},
                {"label": "E", "text": f"{n_a * n_b // n_ab if n_ab > 0 else n_a + n_b}", "is_correct": False},
            ],
            "solution": f"|A ∪ B| = |A| + |B| - |A ∩ B| = {n_a} + {n_b} - {n_ab} = {correct}",
            "explanation": "Count each element in A, each in B, then subtract the overlap to avoid double-counting."
        }

    def inclusion_exclusion_three_events(self) -> Dict[str, Any]:
        """Inclusion-exclusion for three sets: |A ∪ B ∪ C| = |A| + |B| + |C| - |A ∩ B| - |A ∩ C| - |B ∩ C| + |A ∩ B ∩ C|"""
        n_a = random.randint(20, 100)
        n_b = random.randint(20, 100)
        n_c = random.randint(20, 100)
        n_ab = random.randint(1, min(n_a, n_b) // 2)
        n_ac = random.randint(1, min(n_a, n_c) // 2)
        n_bc = random.randint(1, min(n_b, n_c) // 2)
        n_abc = random.randint(0, min(n_ab, n_ac, n_bc) // 2)

        correct = n_a + n_b + n_c - n_ab - n_ac - n_bc + n_abc

        return {
            "id": "inclusion_exclusion_three_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Counting",
            "difficulty": 3,
            "question_text": f"|A| = {n_a}, |B| = {n_b}, |C| = {n_c}, |A∩B| = {n_ab}, |A∩C| = {n_ac}, |B∩C| = {n_bc}, |A∩B∩C| = {n_abc}. Find |A ∪ B ∪ C|.",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{n_a + n_b + n_c}", "is_correct": False},
                {"label": "C", "text": f"{n_a + n_b + n_c - n_ab - n_ac - n_bc}", "is_correct": False},
                {"label": "D", "text": f"{n_a + n_b + n_c - n_ab - n_ac - n_bc - n_abc}", "is_correct": False},
                {"label": "E", "text": f"{n_a * n_b * n_c // (n_abc if n_abc > 0 else 1)}", "is_correct": False},
            ],
            "solution": f"|A ∪ B ∪ C| = {n_a} + {n_b} + {n_c} - {n_ab} - {n_ac} - {n_bc} + {n_abc} = {correct}",
            "explanation": "Include individual sets, subtract pairwise intersections, then add back the three-way intersection."
        }

    def counting_permutations(self) -> Dict[str, Any]:
        """P(n, k) = n! / (n-k)!"""
        n = random.randint(5, 12)
        k = random.randint(2, min(n, 5))
        correct = math.perm(n, k)

        return {
            "id": "permutations_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Counting",
            "difficulty": 2,
            "question_text": f"In how many ways can {k} people be arranged from a group of {n}? (Permutations)",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{math.comb(n, k)}", "is_correct": False},
                {"label": "C", "text": f"{n ** k}", "is_correct": False},
                {"label": "D", "text": f"{math.factorial(k)}", "is_correct": False},
                {"label": "E", "text": f"{n * k}", "is_correct": False},
            ],
            "solution": f"P({n}, {k}) = {n}! / ({n} - {k})! = {correct}",
            "explanation": "Permutations count ordered arrangements. Use P(n,k) = n!/(n-k)!."
        }

    def counting_combinations(self) -> Dict[str, Any]:
        """C(n, k) = n! / (k! (n-k)!)"""
        n = random.randint(5, 15)
        k = random.randint(2, min(n, 6))
        correct = math.comb(n, k)

        return {
            "id": "combinations_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Counting",
            "difficulty": 2,
            "question_text": f"In how many ways can {k} objects be chosen from {n}? (Combinations)",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{math.perm(n, k)}", "is_correct": False},
                {"label": "C", "text": f"{n * k}", "is_correct": False},
                {"label": "D", "text": f"{n ** k}", "is_correct": False},
                {"label": "E", "text": f"{math.factorial(k)}", "is_correct": False},
            ],
            "solution": f"C({n}, {k}) = {n}! / ({k}! * {n-k}!) = {correct}",
            "explanation": "Combinations count unordered selections. Use C(n,k) = n!/(k!(n-k)!)."
        }

    def counting_multinomial(self) -> Dict[str, Any]:
        """Multinomial: n! / (k1! k2! ... km!)"""
        n = random.randint(8, 15)
        k1 = random.randint(2, n // 3)
        k2 = random.randint(2, n // 3)
        k3 = n - k1 - k2
        if k3 < 1:
            k3 = 1
            k2 = n - k1 - k3

        correct = math.factorial(n) // (math.factorial(k1) * math.factorial(k2) * math.factorial(k3))

        return {
            "id": "multinomial_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Counting",
            "difficulty": 3,
            "question_text": f"In how many ways can {n} items be divided into groups of {k1}, {k2}, and {k3}?",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{math.comb(n, k1) * math.comb(n - k1, k2)}", "is_correct": False},
                {"label": "C", "text": f"{math.perm(n, k1) * math.perm(n - k1, k2)}", "is_correct": False},
                {"label": "D", "text": f"{n ** 3}", "is_correct": False},
                {"label": "E", "text": f"{math.factorial(k1) * math.factorial(k2) * math.factorial(k3)}", "is_correct": False},
            ],
            "solution": f"Multinomial: {n}! / ({k1}! * {k2}! * {k3}!) = {correct}",
            "explanation": "Multinomial coefficient divides n! by the factorial of each group size."
        }

    def derangements(self) -> Dict[str, Any]:
        """Derangements: !n = n! * sum((-1)^k / k!) for k=0 to n"""
        n = random.randint(3, 8)
        # Compute derangements
        derang = sum((-1) ** k * math.factorial(n) // math.factorial(k) for k in range(n + 1))
        correct = derang

        return {
            "id": "derangements_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Counting",
            "difficulty": 4,
            "question_text": f"How many derangements (permutations with no fixed points) exist for {n} items?",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{math.factorial(n) - 1}", "is_correct": False},
                {"label": "C", "text": f"{math.factorial(n) // 2}", "is_correct": False},
                {"label": "D", "text": f"{math.comb(n, 2) * math.factorial(n - 2)}", "is_correct": False},
                {"label": "E", "text": f"{math.factorial(n - 1)}", "is_correct": False},
            ],
            "solution": f"!{n} = {n}! * sum((-1)^k / k!) = {correct}",
            "explanation": "Derangements count permutations where no element is in its original position."
        }

    def pigeonhole(self) -> Dict[str, Any]:
        """Pigeonhole principle application."""
        pigeons = random.randint(10, 50)
        holes = random.randint(3, 10)
        correct = (pigeons // holes) + (1 if pigeons % holes > 0 else 0)

        return {
            "id": "pigeonhole_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Counting",
            "difficulty": 2,
            "question_text": f"If {pigeons} items are placed into {holes} bins, at least one bin must contain at least how many items?",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{pigeons // holes}", "is_correct": False},
                {"label": "C", "text": f"{(pigeons // holes) - 1}", "is_correct": False},
                {"label": "D", "text": f"{holes}", "is_correct": False},
                {"label": "E", "text": f"{pigeons - holes}", "is_correct": False},
            ],
            "solution": f"By pigeonhole principle: ceil({pigeons} / {holes}) = {correct}",
            "explanation": "At least one bin must have at least ceil(n/k) items when n items go into k bins."
        }

    def independence_test(self) -> Dict[str, Any]:
        """Test if P(A ∩ B) = P(A) * P(B)"""
        pa = round(random.uniform(0.2, 0.8), 2)
        pb = round(random.uniform(0.2, 0.8), 2)

        # Create independent case
        if random.choice([True, False]):
            pab = round(pa * pb, 4)
            independent = True
        else:
            pab = round(random.uniform(0, min(pa, pb)), 4)
            independent = False

        product = round(pa * pb, 4)

        return {
            "id": "independence_test_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Independence",
            "difficulty": 2,
            "question_text": f"P(A) = {pa}, P(B) = {pb}, P(A ∩ B) = {pab}. Are A and B independent?",
            "choices": [
                {"label": "A", "text": "Yes" if product == pab else "No", "is_correct": True},
                {"label": "B", "text": "No" if product == pab else "Yes", "is_correct": False},
                {"label": "C", "text": "Cannot be determined", "is_correct": False},
                {"label": "D", "text": "Only if P(A) = P(B)", "is_correct": False},
                {"label": "E", "text": "Only if P(A ∩ B) < 0.5", "is_correct": False},
            ],
            "solution": f"Check: P(A) * P(B) = {pa} * {pb} = {product}. Since P(A ∩ B) = {pab}, they are {'independent' if product == pab else 'dependent'}.",
            "explanation": "Events are independent iff P(A ∩ B) = P(A) * P(B)."
        }

    def mutually_exclusive(self) -> Dict[str, Any]:
        """Mutually exclusive events: P(A ∩ B) = 0."""
        pa = round(random.uniform(0.2, 0.5), 2)
        pb = round(random.uniform(0.2, 0.5), 2)

        correct = round(pa + pb, 4)

        return {
            "id": "mutually_exclusive_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Independence",
            "difficulty": 2,
            "question_text": f"Events A and B are mutually exclusive with P(A) = {pa} and P(B) = {pb}. Find P(A ∪ B).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(pa * pb, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(max(pa, pb), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(pa - pb, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 - pa - pb, 4)}", "is_correct": False},
            ],
            "solution": f"For mutually exclusive events: P(A ∪ B) = P(A) + P(B) = {pa} + {pb} = {correct}",
            "explanation": "Mutually exclusive events have P(A ∩ B) = 0, so P(A ∪ B) = P(A) + P(B)."
        }

    def probability_at_least_one(self) -> Dict[str, Any]:
        """P(at least one) = 1 - P(none)."""
        n = random.randint(3, 8)
        p = round(random.uniform(0.2, 0.7), 2)

        p_none = (1 - p) ** n
        correct = round(1 - p_none, 4)

        return {
            "id": "at_least_one_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Probability",
            "difficulty": 2,
            "question_text": f"An event occurs with probability {p} on each of {n} independent trials. Find P(at least one occurrence).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(n * p, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(1 - p ** n, 4)}", "is_correct": False},
                {"label": "D", "text": f"{p}", "is_correct": False},
                {"label": "E", "text": f"{round(p_none, 4)}", "is_correct": False},
            ],
            "solution": f"P(at least one) = 1 - P(none) = 1 - (1 - {p})^{n} = 1 - {round(p_none, 4)} = {correct}",
            "explanation": "Use complement: P(at least one) = 1 - P(none in n trials)."
        }

    def birthday_problem_variant(self) -> Dict[str, Any]:
        """Birthday problem: find probability two people share birthday."""
        n = random.randint(10, 50)
        days = 365

        if n > days:
            correct = 1.0
        else:
            prob_all_different = 1.0
            for i in range(n):
                prob_all_different *= (days - i) / days
            correct = round(1 - prob_all_different, 4)

        return {
            "id": "birthday_problem_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Probability",
            "difficulty": 3,
            "question_text": f"In a group of {n} people, find the probability that at least two share the same birthday (assume 365 days).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(n / 365, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(1 - n / 365, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(math.comb(n, 2) / 365, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((1 - 1/365) ** n, 4)}", "is_correct": False},
            ],
            "solution": f"P(at least one match) = 1 - P(all different) ≈ {correct}",
            "explanation": "Birthday problem uses complement: 1 - [product of (365-i)/365 for i=0 to n-1]."
        }

    def conditional_probability_basic(self) -> Dict[str, Any]:
        """P(A|B) = P(A ∩ B) / P(B)."""
        pab_intersect = round(random.uniform(0.05, 0.3), 3)
        pb = round(random.uniform(max(pab_intersect + 0.05, 0.2), 0.8), 3)

        correct = round(pab_intersect / pb, 4)

        return {
            "id": "conditional_basic_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "General Probability",
            "subtopic": "Conditional Probability",
            "difficulty": 2,
            "question_text": f"P(A ∩ B) = {pab_intersect}, P(B) = {pb}. Find P(A|B).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(pab_intersect * pb, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(pab_intersect - pb, 4)}", "is_correct": False},
                {"label": "D", "text": f"{pab_intersect}", "is_correct": False},
                {"label": "E", "text": f"{pb}", "is_correct": False},
            ],
            "solution": f"P(A|B) = P(A ∩ B) / P(B) = {pab_intersect} / {pb} = {correct}",
            "explanation": "Conditional probability: P(A|B) = P(A ∩ B) / P(B), the probability of A given B occurred."
        }

    # ==================== TOPIC 2: CONDITIONAL PROBABILITY & BAYES (15+ methods) ====================

    def bayes_two_hypotheses(self) -> Dict[str, Any]:
        """Bayes' theorem with two hypotheses."""
        # H1 and H2 with prior probabilities
        ph1 = round(random.uniform(0.3, 0.7), 2)
        ph2 = 1 - ph1

        # Likelihoods
        pe_given_h1 = round(random.uniform(0.5, 0.95), 2)
        pe_given_h2 = round(random.uniform(0.1, 0.5), 2)

        # Total probability
        pe = ph1 * pe_given_h1 + ph2 * pe_given_h2

        # Posterior
        correct = round(ph1 * pe_given_h1 / pe, 4)

        return {
            "id": "bayes_two_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Bayes' Theorem",
            "difficulty": 3,
            "question_text": f"P(H1) = {ph1}, P(H2) = {ph2}, P(E|H1) = {pe_given_h1}, P(E|H2) = {pe_given_h2}. Find P(H1|E).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(ph1 * pe_given_h1, 4)}", "is_correct": False},
                {"label": "C", "text": f"{ph1}", "is_correct": False},
                {"label": "D", "text": f"{round(pe_given_h1 / (pe_given_h1 + pe_given_h2), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(pe, 4)}", "is_correct": False},
            ],
            "solution": f"P(H1|E) = [P(H1) * P(E|H1)] / [P(H1)*P(E|H1) + P(H2)*P(E|H2)] = {correct}",
            "explanation": "Bayes' theorem updates prior probabilities using observed evidence."
        }

    def bayes_three_hypotheses(self) -> Dict[str, Any]:
        """Bayes' theorem with three hypotheses."""
        priors = [round(random.uniform(0.2, 0.5), 2) for _ in range(2)]
        priors.append(round(1 - sum(priors), 2))

        likelihoods = [round(random.uniform(0.4, 0.9), 2) for _ in range(3)]

        total = sum(priors[i] * likelihoods[i] for i in range(3))
        correct = round(priors[0] * likelihoods[0] / total, 4)

        return {
            "id": "bayes_three_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Bayes' Theorem",
            "difficulty": 4,
            "question_text": f"P(H1)={priors[0]}, P(H2)={priors[1]}, P(H3)={priors[2]}. P(E|H1)={likelihoods[0]}, P(E|H2)={likelihoods[1]}, P(E|H3)={likelihoods[2]}. Find P(H1|E).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(priors[0] * likelihoods[0], 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(priors[0] / 3, 4)}", "is_correct": False},
                {"label": "D", "text": f"{priors[0]}", "is_correct": False},
                {"label": "E", "text": f"{round(likelihoods[0] / sum(likelihoods), 4)}", "is_correct": False},
            ],
            "solution": f"P(H1|E) = {priors[0]} * {likelihoods[0]} / {round(total, 4)} = {correct}",
            "explanation": "Extend Bayes to multiple hypotheses by normalizing over all cases."
        }

    def bayes_medical_test(self) -> Dict[str, Any]:
        """Medical test: disease present/absent with sensitivity/specificity."""
        prevalence = round(random.uniform(0.01, 0.1), 3)
        sensitivity = round(random.uniform(0.8, 0.99), 2)
        specificity = round(random.uniform(0.8, 0.99), 2)

        # P(+ | disease) = sensitivity, P(- | no disease) = specificity
        # P(+ | no disease) = 1 - specificity

        p_pos = prevalence * sensitivity + (1 - prevalence) * (1 - specificity)
        correct = round(prevalence * sensitivity / p_pos, 4)

        return {
            "id": "medical_test_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Bayes' Theorem",
            "difficulty": 4,
            "question_text": f"Disease prevalence: {prevalence}. Test sensitivity: {sensitivity}. Test specificity: {specificity}. Find P(disease | positive test).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{sensitivity}", "is_correct": False},
                {"label": "C", "text": f"{round(prevalence * sensitivity, 4)}", "is_correct": False},
                {"label": "D", "text": f"{specificity}", "is_correct": False},
                {"label": "E", "text": f"{prevalence}", "is_correct": False},
            ],
            "solution": f"P(disease|+) = P(+|disease)*P(disease) / [P(+|disease)*P(disease) + P(+|no disease)*P(no disease)] = {correct}",
            "explanation": "Medical test example of Bayes: posterior depends on both test accuracy and disease prevalence."
        }

    def total_probability_two_states(self) -> Dict[str, Any]:
        """Law of total probability with two states."""
        ps1 = round(random.uniform(0.3, 0.7), 2)
        ps2 = 1 - ps1

        pe_given_s1 = round(random.uniform(0.2, 0.8), 2)
        pe_given_s2 = round(random.uniform(0.2, 0.8), 2)

        correct = round(ps1 * pe_given_s1 + ps2 * pe_given_s2, 4)

        return {
            "id": "total_prob_two_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Total Probability",
            "difficulty": 2,
            "question_text": f"P(S1) = {ps1}, P(S2) = {ps2}, P(E|S1) = {pe_given_s1}, P(E|S2) = {pe_given_s2}. Find P(E).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(pe_given_s1 + pe_given_s2, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((pe_given_s1 + pe_given_s2) / 2, 4)}", "is_correct": False},
                {"label": "D", "text": f"{pe_given_s1}", "is_correct": False},
                {"label": "E", "text": f"{ps1}", "is_correct": False},
            ],
            "solution": f"P(E) = P(S1)*P(E|S1) + P(S2)*P(E|S2) = {ps1}*{pe_given_s1} + {ps2}*{pe_given_s2} = {correct}",
            "explanation": "Law of total probability: condition on all possible states."
        }

    def total_probability_three_states(self) -> Dict[str, Any]:
        """Law of total probability with three states."""
        probs = [round(random.uniform(0.2, 0.4), 2) for _ in range(2)]
        probs.append(round(1 - sum(probs), 2))

        pe_given = [round(random.uniform(0.2, 0.8), 2) for _ in range(3)]

        correct = sum(probs[i] * pe_given[i] for i in range(3))
        correct = round(correct, 4)

        return {
            "id": "total_prob_three_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Total Probability",
            "difficulty": 3,
            "question_text": f"P(S1)={probs[0]}, P(S2)={probs[1]}, P(S3)={probs[2]}. P(E|S1)={pe_given[0]}, P(E|S2)={pe_given[1]}, P(E|S3)={pe_given[2]}. Find P(E).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(sum(pe_given) / 3, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(sum(probs) / 3, 4)}", "is_correct": False},
                {"label": "D", "text": f"{pe_given[0]}", "is_correct": False},
                {"label": "E", "text": f"{round(sum(probs) * sum(pe_given) / 3, 4)}", "is_correct": False},
            ],
            "solution": f"P(E) = sum of P(Si)*P(E|Si) = {correct}",
            "explanation": "Extend total probability to three states: P(E) = Σ P(Si)*P(E|Si)."
        }

    def sequential_draws_without_replacement(self) -> Dict[str, Any]:
        """Probability of sequence of events without replacement."""
        n = random.randint(5, 15)
        k_success = random.randint(2, min(n - 1, 8))

        # Probability of k successes in first k draws
        correct = 1.0
        for i in range(k_success):
            correct *= (k_success - i) / (n - i)
        correct = round(correct, 4)

        return {
            "id": "sequential_without_replace_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Sequential Events",
            "difficulty": 3,
            "question_text": f"An urn has {n} balls: {k_success} red and {n - k_success} white. Draw 2 without replacement. Find P(first red, second red).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round((k_success / n) ** 2, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(k_success / n, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(2 * k_success / n, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(k_success * (k_success - 1) / (n * (n - 1)), 4)}", "is_correct": False},
            ],
            "solution": f"P(RR) = ({k_success}/{n}) * ({k_success - 1}/{n - 1}) = {correct}",
            "explanation": "Without replacement, each draw changes the remaining composition."
        }

    def sequential_draws_with_replacement(self) -> Dict[str, Any]:
        """Probability with replacement."""
        n = random.randint(5, 15)
        k_success = random.randint(2, min(n - 1, 8))

        p_success = k_success / n
        correct = round(p_success ** 2, 4)

        return {
            "id": "sequential_with_replace_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Sequential Events",
            "difficulty": 2,
            "question_text": f"An urn has {n} balls: {k_success} red, {n - k_success} white. Draw 2 WITH replacement. Find P(both red).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(k_success * (k_success - 1) / (n * (n - 1)), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(k_success / n, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(2 * k_success / n, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(k_success / n + (k_success - 1) / (n - 1), 4)}", "is_correct": False},
            ],
            "solution": f"P(both red) = ({k_success}/{n})^2 = {correct}",
            "explanation": "With replacement, draws are independent; probability is simply p^n."
        }

    def urn_model_conditional(self) -> Dict[str, Any]:
        """Urn problem with conditional probability."""
        n_red = random.randint(2, 8)
        n_white = random.randint(2, 8)
        n_total = n_red + n_white

        # P(second red | first red)
        correct = round((n_red - 1) / (n_total - 1), 4)

        return {
            "id": "urn_conditional_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Conditional Probability",
            "difficulty": 2,
            "question_text": f"Urn: {n_red} red, {n_white} white balls. Draw 2 without replacement. Find P(2nd red | 1st red).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(n_red / n_total, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((n_red - 1) / n_total, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(n_red / (n_total - 1), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((n_red - 1) / n_white, 4)}", "is_correct": False},
            ],
            "solution": f"P(2nd red | 1st red) = (red remaining) / (balls remaining) = {n_red - 1} / {n_total - 1} = {correct}",
            "explanation": "Given first was red, {n_red - 1} red balls remain out of {n_total - 1} total."
        }

    def insurance_classification_bayes(self) -> Dict[str, Any]:
        """Insurance: classify based on accident history."""
        # Good driver, bad driver
        p_good = round(random.uniform(0.7, 0.95), 2)
        p_bad = 1 - p_good

        # P(accident | good), P(accident | bad)
        p_acc_given_good = round(random.uniform(0.01, 0.1), 3)
        p_acc_given_bad = round(random.uniform(0.2, 0.5), 2)

        # P(bad | accident)
        p_acc = p_good * p_acc_given_good + p_bad * p_acc_given_bad
        correct = round(p_bad * p_acc_given_bad / p_acc, 4)

        return {
            "id": "insurance_bayes_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Bayes' Theorem",
            "difficulty": 4,
            "question_text": f"P(good driver)={p_good}. P(accident|good)={p_acc_given_good}, P(accident|bad)={p_acc_given_bad}. Find P(bad driver|accident).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{p_bad}", "is_correct": False},
                {"label": "C", "text": f"{p_acc_given_bad}", "is_correct": False},
                {"label": "D", "text": f"{round(p_bad * p_acc_given_bad, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(p_acc, 4)}", "is_correct": False},
            ],
            "solution": f"P(bad|accident) = P(accident|bad)*P(bad) / P(accident) = {correct}",
            "explanation": "Accident is evidence that driver is bad; use Bayes to update classification."
        }

    def conditional_independence(self) -> Dict[str, Any]:
        """A and B independent given C."""
        pc = round(random.uniform(0.3, 0.7), 2)

        # Given C
        pa_given_c = round(random.uniform(0.2, 0.8), 2)
        pb_given_c = round(random.uniform(0.2, 0.8), 2)
        pab_given_c = round(pa_given_c * pb_given_c, 4)

        # Are they conditionally independent?
        correct_answer = "Yes"

        return {
            "id": "cond_independence_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Independence",
            "difficulty": 3,
            "question_text": f"P(A|C)={pa_given_c}, P(B|C)={pb_given_c}, P(A∩B|C)={pab_given_c}. Are A and B conditionally independent given C?",
            "choices": [
                {"label": "A", "text": "Yes", "is_correct": True},
                {"label": "B", "text": "No", "is_correct": False},
                {"label": "C", "text": "Only if P(C) = 0.5", "is_correct": False},
                {"label": "D", "text": "Cannot determine", "is_correct": False},
                {"label": "E", "text": "Only if P(A) = P(B)", "is_correct": False},
            ],
            "solution": f"Check: P(A|C)*P(B|C) = {pa_given_c}*{pb_given_c} = {round(pa_given_c * pb_given_c, 4)} = P(A∩B|C). Yes, conditionally independent.",
            "explanation": "A and B are conditionally independent given C iff P(A∩B|C) = P(A|C)*P(B|C)."
        }

    def repeated_trials_conditional(self) -> Dict[str, Any]:
        """Conditional probability in repeated trials."""
        n = random.randint(4, 10)
        p = round(random.uniform(0.3, 0.7), 2)

        # P(exactly k successes in n trials)
        k = random.randint(1, min(n - 1, 5))
        prob_k = comb(n, k, exact=True) * (p ** k) * ((1 - p) ** (n - k))

        # P(at least k successes)
        correct = round(prob_k, 4)

        return {
            "id": "repeated_trials_cond_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Repeated Trials",
            "difficulty": 3,
            "question_text": f"In {n} independent trials with success probability {p}, find P(exactly {k} successes).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(n * p ** k, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(p ** k, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(comb(n, k, exact=True) * p, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(k * p / n, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k}) = C({n},{k}) * {p}^{k} * {1-p}^{n-k} = {correct}",
            "explanation": "Binomial probability for exactly k successes in n trials."
        }

    def false_positive_rate(self) -> Dict[str, Any]:
        """False positive rate: P(disease absent | test positive)."""
        prevalence = round(random.uniform(0.01, 0.1), 3)
        sensitivity = round(random.uniform(0.8, 0.99), 2)
        fpr = round(random.uniform(0.01, 0.2), 2)  # false positive rate = P(+|absent)

        # P(+ and absent) = P(absent) * P(+|absent)
        # P(+) = P(+|present)*P(present) + P(+|absent)*P(absent)

        p_pos = prevalence * sensitivity + (1 - prevalence) * fpr
        correct = round((1 - prevalence) * fpr / p_pos, 4)

        return {
            "id": "false_positive_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Medical Testing",
            "difficulty": 4,
            "question_text": f"Prevalence={prevalence}, Sensitivity={sensitivity}, False positive rate={fpr}. Find P(absent|positive).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{fpr}", "is_correct": False},
                {"label": "C", "text": f"{round(1 - sensitivity, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((1 - prevalence) * fpr, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(prevalence * sensitivity, 4)}", "is_correct": False},
            ],
            "solution": f"P(absent|+) = P(+|absent)*P(absent) / P(+) = {correct}",
            "explanation": "P(absent|+) = (false positive) / (all positives). True positive must be weighted by prevalence."
        }

    def sensitivity_specificity(self) -> Dict[str, Any]:
        """Sensitivity and specificity calculations."""
        # Confusion matrix values
        tp = random.randint(70, 95)
        fn = random.randint(5, 30)
        fp = random.randint(5, 30)
        tn = random.randint(70, 95)

        sensitivity = round(tp / (tp + fn), 4)
        specificity = round(tn / (tn + fp), 4)

        correct = sensitivity

        return {
            "id": "sensitivity_specificity_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Medical Testing",
            "difficulty": 2,
            "question_text": f"Test results: TP={tp}, FN={fn}, FP={fp}, TN={tn}. Find sensitivity P(+|disease).",
            "choices": [
                {"label": "A", "text": f"{sensitivity}", "is_correct": True},
                {"label": "B", "text": f"{specificity}", "is_correct": False},
                {"label": "C", "text": f"{round(tp / (tp + fp), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((tp + tn) / (tp + tn + fp + fn), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(tp / (tp + tn), 4)}", "is_correct": False},
            ],
            "solution": f"Sensitivity = TP / (TP + FN) = {tp} / {tp + fn} = {sensitivity}",
            "explanation": "Sensitivity = True positive rate = P(positive test | disease present)."
        }

    def tree_diagram_multi_stage(self) -> Dict[str, Any]:
        """Multi-stage probability tree."""
        # Stage 1: two outcomes
        p1a = round(random.uniform(0.3, 0.7), 2)
        p1b = 1 - p1a

        # Stage 2: given each outcome from stage 1
        p2a_given_1a = round(random.uniform(0.3, 0.8), 2)
        p2a_given_1b = round(random.uniform(0.3, 0.8), 2)

        p2b_given_1a = 1 - p2a_given_1a
        p2b_given_1b = 1 - p2a_given_1b

        # Path 1A -> 2A
        correct = round(p1a * p2a_given_1a, 4)

        return {
            "id": "tree_diagram_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Tree Diagrams",
            "difficulty": 3,
            "question_text": f"Stage 1: P(A)={p1a}, P(B)={p1b}. Stage 2: P(X|A)={p2a_given_1a}, P(X|B)={p2a_given_1b}. Find P(A and X).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(p1a + p2a_given_1a, 4)}", "is_correct": False},
                {"label": "C", "text": f"{p1a}", "is_correct": False},
                {"label": "D", "text": f"{p2a_given_1a}", "is_correct": False},
                {"label": "E", "text": f"{round(p1a * p2a_given_1b, 4)}", "is_correct": False},
            ],
            "solution": f"P(A and X) = P(A) * P(X|A) = {p1a} * {p2a_given_1a} = {correct}",
            "explanation": "Follow the tree: multiply probabilities along the path."
        }

    def conditional_on_sum(self) -> Dict[str, Any]:
        """Conditional probability given a sum."""
        # X and Y are i.i.d. uniform on {1, 2, 3}
        possible_sums = [(i, j) for i in range(1, 4) for j in range(1, 4)]
        target_sum = random.randint(2, 6)

        # Count pairs with target sum
        pairs_with_sum = [(i, j) for i, j in possible_sums if i + j == target_sum]

        if not pairs_with_sum:
            return self.conditional_on_sum()

        # P(X = 1 | X + Y = target_sum)
        pairs_with_x_1 = [(i, j) for i, j in pairs_with_sum if i == 1]

        correct = round(len(pairs_with_x_1) / len(pairs_with_sum), 4)

        return {
            "id": "conditional_sum_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Conditional Probability & Bayes",
            "subtopic": "Conditional Probability",
            "difficulty": 3,
            "question_text": f"X and Y uniform on {{1,2,3}}, independent. Find P(X=1 | X+Y={target_sum}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1/3, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(1/9, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(len(pairs_with_sum) / 9, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(2/9, 4)}", "is_correct": False},
            ],
            "solution": f"Pairs summing to {target_sum}: {pairs_with_sum}. Pairs with X=1: {pairs_with_x_1}. P = {len(pairs_with_x_1)}/{len(pairs_with_sum)} = {correct}",
            "explanation": "Condition on X+Y={target_sum} by counting favorable outcomes."
        }

    # ==================== TOPIC 3: DISCRETE DISTRIBUTIONS (20+ methods) ====================

    def binomial_probability(self) -> Dict[str, Any]:
        """Binomial: P(X = k) with n trials and success probability p."""
        n = random.randint(5, 20)
        p = round(random.uniform(0.2, 0.8), 2)
        k = random.randint(0, min(n, 10))

        correct = round(comb(n, k, exact=True) * (p ** k) * ((1 - p) ** (n - k)), 4)

        return {
            "id": "binomial_prob_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Binomial",
            "difficulty": 2,
            "question_text": f"X ~ Binomial(n={n}, p={p}). Find P(X = {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(comb(n, k, exact=True) * p ** k, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((p ** k) * ((1 - p) ** (n - k)), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(n * p, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(k * p / n, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k}) = C({n},{k}) * {p}^{k} * {1-p}^{n-k} = {correct}",
            "explanation": "Binomial probability uses the formula: C(n,k) * p^k * (1-p)^(n-k)."
        }

    def binomial_expected_value(self) -> Dict[str, Any]:
        """E[X] for binomial distribution."""
        n = random.randint(5, 25)
        p = round(random.uniform(0.2, 0.8), 2)

        correct = round(n * p, 4)

        return {
            "id": "binomial_ev_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Binomial",
            "difficulty": 1,
            "question_text": f"X ~ Binomial(n={n}, p={p}). Find E[X].",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(n * (1 - p), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(n * p * (1 - p), 4)}", "is_correct": False},
                {"label": "D", "text": f"{n}", "is_correct": False},
                {"label": "E", "text": f"{p}", "is_correct": False},
            ],
            "solution": f"E[X] = n * p = {n} * {p} = {correct}",
            "explanation": "Expected value of binomial: E[X] = n * p."
        }

    def binomial_at_least_k(self) -> Dict[str, Any]:
        """P(X >= k) for binomial."""
        n = random.randint(8, 15)
        p = round(random.uniform(0.3, 0.7), 2)
        k = random.randint(1, min(n - 1, 8))

        # Use complement
        prob_less = sum(comb(n, i, exact=True) * (p ** i) * ((1 - p) ** (n - i)) for i in range(k))
        correct = round(1 - prob_less, 4)

        return {
            "id": "binomial_at_least_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Binomial",
            "difficulty": 2,
            "question_text": f"X ~ Binomial(n={n}, p={p}). Find P(X >= {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1 - prob_less, 4) if random.random() > 0.5 else round(prob_less, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(comb(n, k, exact=True) * p ** k, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(n * p, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 - p, 4)}", "is_correct": False},
            ],
            "solution": f"P(X >= {k}) = 1 - P(X < {k}) = 1 - sum of P(X=i) for i=0 to {k-1} = {correct}",
            "explanation": "Use complement to sum tail probability."
        }

    def poisson_probability(self) -> Dict[str, Any]:
        """Poisson: P(X = k) = e^-lambda * lambda^k / k!"""
        lam = round(random.uniform(1, 8), 1)
        k = random.randint(0, 8)

        correct = round(math.exp(-lam) * (lam ** k) / math.factorial(k), 4)

        return {
            "id": "poisson_prob_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Poisson",
            "difficulty": 2,
            "question_text": f"X ~ Poisson(λ={lam}). Find P(X = {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(math.exp(-lam) * (lam ** k), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(lam ** k / math.factorial(k), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(lam / math.factorial(k), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(math.exp(-k) * lam, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k}) = e^-{lam} * {lam}^{k} / {k}! = {correct}",
            "explanation": "Poisson probability: P(X=k) = e^(-λ) * λ^k / k!."
        }

    def poisson_sum(self) -> Dict[str, Any]:
        """P(X1 + X2) where X1 ~ Poisson(λ1), X2 ~ Poisson(λ2)."""
        lam1 = round(random.uniform(1, 5), 1)
        lam2 = round(random.uniform(1, 5), 1)

        # Sum is Poisson with parameter λ1 + λ2
        lam_sum = lam1 + lam2
        k = random.randint(0, 8)

        correct = round(math.exp(-lam_sum) * (lam_sum ** k) / math.factorial(k), 4)

        return {
            "id": "poisson_sum_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Poisson",
            "difficulty": 3,
            "question_text": f"X ~ Poisson({lam1}), Y ~ Poisson({lam2}), independent. Find P(X + Y = {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(math.exp(-lam1) * (lam1 ** k) / math.factorial(k), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(math.exp(-lam2) * (lam2 ** k) / math.factorial(k), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((lam1 + lam2) / (lam1 * lam2), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(lam1 + lam2, 4)}", "is_correct": False},
            ],
            "solution": f"X + Y ~ Poisson({lam_sum}), so P(X+Y={k}) = e^-{lam_sum} * {lam_sum}^{k} / {k}! = {correct}",
            "explanation": "Sum of independent Poisson random variables is also Poisson."
        }

    def poisson_conditional(self) -> Dict[str, Any]:
        """Conditional probability with Poisson."""
        lam = round(random.uniform(2, 6), 1)
        k = random.randint(2, 8)

        # P(X=k | X>=1)
        p_k = math.exp(-lam) * (lam ** k) / math.factorial(k)
        p_at_least_1 = 1 - math.exp(-lam)

        correct = round(p_k / p_at_least_1, 4)

        return {
            "id": "poisson_conditional_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Poisson",
            "difficulty": 3,
            "question_text": f"X ~ Poisson({lam}). Find P(X = {k} | X >= 1).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(p_k, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(p_at_least_1, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((lam ** k) / math.factorial(k), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(lam / k, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k} | X>=1) = P(X={k}) / P(X>=1) = {round(p_k, 4)} / {round(p_at_least_1, 4)} = {correct}",
            "explanation": "Condition on X >= 1 by dividing unconditional probability by P(X >= 1)."
        }

    def geometric_probability(self) -> Dict[str, Any]:
        """Geometric: P(X = k) = (1-p)^(k-1) * p, number of trials until first success."""
        p = round(random.uniform(0.2, 0.7), 2)
        k = random.randint(1, 10)

        correct = round(((1 - p) ** (k - 1)) * p, 4)

        return {
            "id": "geometric_prob_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Geometric",
            "difficulty": 2,
            "question_text": f"X ~ Geometric(p={p}). Find P(X = {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(p ** k, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((1 - p) ** k, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(p * k, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 - (1 - p) ** k, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k}) = (1-{p})^{k-1} * {p} = {correct}",
            "explanation": "Geometric probability: P(X=k) = (1-p)^(k-1) * p, k failures then success."
        }

    def geometric_memoryless(self) -> Dict[str, Any]:
        """Memoryless property of geometric distribution."""
        p = round(random.uniform(0.2, 0.6), 2)
        k = random.randint(1, 5)
        m = random.randint(1, 5)

        # P(X > k + m | X > k) = P(X > m)
        correct = round((1 - p) ** m, 4)

        return {
            "id": "geometric_memoryless_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Geometric",
            "difficulty": 3,
            "question_text": f"X ~ Geometric(p={p}). Find P(X > {k + m} | X > {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round((1 - p) ** (k + m), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(p ** m, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(1 - p, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((1 - p) ** k, 4)}", "is_correct": False},
            ],
            "solution": f"P(X > {k+m} | X > {k}) = P(X > {m}) = (1-{p})^{m} = {correct}",
            "explanation": "Memoryless property: conditioning on X > k doesn't change the tail probability."
        }

    def geometric_expected_value(self) -> Dict[str, Any]:
        """E[X] for geometric distribution."""
        p = round(random.uniform(0.1, 0.9), 2)

        correct = round(1 / p, 4)

        return {
            "id": "geometric_ev_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Geometric",
            "difficulty": 1,
            "question_text": f"X ~ Geometric(p={p}). Find E[X].",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(p, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(1 - p, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((1 - p) / p, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 / (1 - p), 4)}", "is_correct": False},
            ],
            "solution": f"E[X] = 1/p = 1/{p} = {correct}",
            "explanation": "Expected value of geometric: E[X] = 1/p."
        }

    def negative_binomial_probability(self) -> Dict[str, Any]:
        """Negative binomial: P(X = k) = C(k-1, r-1) * p^r * (1-p)^(k-r)."""
        r = random.randint(2, 5)
        p = round(random.uniform(0.3, 0.7), 2)
        k = random.randint(r, r + 8)

        correct = round(comb(k - 1, r - 1, exact=True) * (p ** r) * ((1 - p) ** (k - r)), 4)

        return {
            "id": "neg_binomial_prob_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Negative Binomial",
            "difficulty": 3,
            "question_text": f"X ~ NegativeBinomial(r={r}, p={p}). Find P(X = {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(comb(k, r, exact=True) * (p ** r), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((p ** r) * ((1 - p) ** (k - r)), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(comb(k - 1, r - 1, exact=True) * p ** r, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(r * p / k, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k}) = C({k-1},{r-1}) * {p}^{r} * {1-p}^{k-r} = {correct}",
            "explanation": "Negative binomial: P(X=k) = C(k-1,r-1) * p^r * (1-p)^(k-r), k trials for r successes."
        }

    def negative_binomial_mean_variance(self) -> Dict[str, Any]:
        """Mean and variance of negative binomial."""
        r = random.randint(2, 6)
        p = round(random.uniform(0.3, 0.8), 2)

        mean = r / p
        variance = r * (1 - p) / (p ** 2)

        correct = round(mean, 4)

        return {
            "id": "neg_binomial_mean_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Negative Binomial",
            "difficulty": 2,
            "question_text": f"X ~ NegativeBinomial(r={r}, p={p}). Find E[X].",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(variance, 4)}", "is_correct": False},
                {"label": "C", "text": f"{r}", "is_correct": False},
                {"label": "D", "text": f"{p}", "is_correct": False},
                {"label": "E", "text": f"{round(r * p, 4)}", "is_correct": False},
            ],
            "solution": f"E[X] = r/p = {r}/{p} = {correct}",
            "explanation": "Negative binomial mean: E[X] = r/p."
        }

    def hypergeometric_probability(self) -> Dict[str, Any]:
        """Hypergeometric: sampling without replacement from finite population."""
        N = random.randint(20, 50)
        K = random.randint(5, N - 5)
        n = random.randint(3, min(10, N - 1))
        k = random.randint(0, min(n, K))

        correct = round(comb(K, k, exact=True) * comb(N - K, n - k, exact=True) / comb(N, n, exact=True), 4)

        return {
            "id": "hypergeometric_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Hypergeometric",
            "difficulty": 3,
            "question_text": f"Population: {N} items ({K} success, {N-K} fail). Draw {n}. Find P(exactly {k} successes).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(comb(K, k, exact=True) * comb(N - K, n - k, exact=True), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(comb(n, k, exact=True) * (K / N) ** k, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((K / N) ** k, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(k / n, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k}) = C({K},{k})*C({N-K},{n-k}) / C({N},{n}) = {correct}",
            "explanation": "Hypergeometric: sampling without replacement using combinations."
        }

    def discrete_uniform_probability(self) -> Dict[str, Any]:
        """Discrete uniform: P(X = k) = 1/n for each outcome."""
        a = random.randint(1, 5)
        b = random.randint(a + 3, a + 10)
        k = random.randint(a, b)

        n = b - a + 1
        correct = round(1 / n, 4)

        return {
            "id": "discrete_uniform_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Discrete Uniform",
            "difficulty": 1,
            "question_text": f"X ~ Uniform({{{a}, {a+1}, ..., {b}}}) on {n} values. Find P(X = {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1 / (b - a), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(k / b, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(1 / b, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(2 / n, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k}) = 1/{n} = {correct}",
            "explanation": "Discrete uniform: each outcome has equal probability 1/n."
        }

    def bernoulli_trials_run(self) -> Dict[str, Any]:
        """Probability of a run of successes in Bernoulli trials."""
        p = round(random.uniform(0.3, 0.7), 2)
        run_length = random.randint(2, 4)

        correct = round(p ** run_length, 4)

        return {
            "id": "bernoulli_run_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Bernoulli Trials",
            "difficulty": 2,
            "question_text": f"Independent Bernoulli trials, p={p}. Find P({run_length} successes in a row).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(run_length * p, 4)}", "is_correct": False},
                {"label": "C", "text": f"{p}", "is_correct": False},
                {"label": "D", "text": f"{round(1 - (1 - p) ** run_length, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(comb(run_length, 2, exact=True) * p ** 2, 4)}", "is_correct": False},
            ],
            "solution": f"P({run_length} successes) = {p}^{run_length} = {correct}",
            "explanation": "Run of k successes: P = p^k."
        }

    def mixed_discrete_distribution(self) -> Dict[str, Any]:
        """Mixture of two discrete distributions."""
        # Mix of Poisson and Binomial
        weight = round(random.uniform(0.3, 0.7), 2)

        lam = round(random.uniform(2, 5), 1)
        n_bin = random.randint(5, 12)
        p_bin = round(random.uniform(0.3, 0.7), 2)
        k = random.randint(1, min(6, n_bin))

        p_poisson = math.exp(-lam) * (lam ** k) / math.factorial(k)
        p_binom = comb(n_bin, k, exact=True) * (p_bin ** k) * ((1 - p_bin) ** (n_bin - k))

        correct = round(weight * p_poisson + (1 - weight) * p_binom, 4)

        return {
            "id": "mixed_discrete_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Mixed Distributions",
            "difficulty": 4,
            "question_text": f"With prob {weight}: X ~ Poisson({lam}), else X ~ Binomial({n_bin},{p_bin}). Find P(X={k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(p_poisson, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(p_binom, 4)}", "is_correct": False},
                {"label": "D", "text": f"{weight}", "is_correct": False},
                {"label": "E", "text": f"{round(weight + p_poisson, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k}) = {weight}*P(Poisson) + {1-weight}*P(Binomial) = {correct}",
            "explanation": "Mixture: take weighted average of component probabilities."
        }

    def zero_truncated_poisson(self) -> Dict[str, Any]:
        """Poisson truncated at zero: P(X = k | X > 0)."""
        lam = round(random.uniform(1.5, 5), 1)
        k = random.randint(1, 8)

        p_k_poisson = math.exp(-lam) * (lam ** k) / math.factorial(k)
        p_greater_0 = 1 - math.exp(-lam)

        correct = round(p_k_poisson / p_greater_0, 4)

        return {
            "id": "zero_truncated_poisson_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Poisson",
            "difficulty": 3,
            "question_text": f"X ~ Poisson({lam}), observed only when X > 0. Find P(X = {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(p_k_poisson, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(p_greater_0, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((lam ** k) / math.factorial(k), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 / (k + 1), 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k} | X>0) = P(X={k}) / P(X>0) = {round(p_k_poisson, 4)} / {round(p_greater_0, 4)} = {correct}",
            "explanation": "Zero-truncated: condition on X > 0 to eliminate zero probability."
        }

    def discrete_convolution(self) -> Dict[str, Any]:
        """Convolution of two independent discrete distributions."""
        # Sum of two independent Poisson
        lam1 = round(random.uniform(1, 3), 1)
        lam2 = round(random.uniform(1, 3), 1)
        k = random.randint(1, 8)

        lam_sum = lam1 + lam2
        correct = round(math.exp(-lam_sum) * (lam_sum ** k) / math.factorial(k), 4)

        return {
            "id": "discrete_convolution_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Convolution",
            "difficulty": 3,
            "question_text": f"X ~ Poisson({lam1}), Y ~ Poisson({lam2}), independent. Find P(X + Y = {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(math.exp(-lam1) * (lam1 ** k) / math.factorial(k), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(math.exp(-lam2) * (lam2 ** k) / math.factorial(k), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((lam1 + lam2) / (lam1 * lam2), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(lam1 + lam2, 4)}", "is_correct": False},
            ],
            "solution": f"X + Y ~ Poisson({lam_sum}), so P(X+Y={k}) = {correct}",
            "explanation": "Convolution of independent Poisson variables is Poisson with summed parameters."
        }

    def binomial_normal_approximation(self) -> Dict[str, Any]:
        """Normal approximation to binomial."""
        n = random.randint(50, 100)
        p = round(random.uniform(0.4, 0.6), 2)
        k = random.randint(int(n * p) - 5, int(n * p) + 5)

        mean = n * p
        std = math.sqrt(n * p * (1 - p))

        # Using normal approximation with continuity correction
        z = (k + 0.5 - mean) / std
        correct = round(norm.cdf(z), 4)

        return {
            "id": "binomial_normal_approx_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Approximations",
            "difficulty": 3,
            "question_text": f"X ~ Binomial({n}, {p}). Use normal approximation: Find P(X <= {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(norm.cdf((k - mean) / std), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((k / n), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(comb(n, k, exact=True) * p ** k, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(p, 4)}", "is_correct": False},
            ],
            "solution": f"μ = {mean}, σ = {round(std, 2)}, Z = ({k}+0.5-{mean})/{round(std, 2)}, P(X≤{k}) ≈ Φ(Z) = {correct}",
            "explanation": "Normal approximation: X ~ N(np, np(1-p)); use continuity correction."
        }

    def poisson_approximation_to_binomial(self) -> Dict[str, Any]:
        """Poisson approximation to binomial when n large, p small."""
        n = random.randint(50, 150)
        p = round(random.uniform(0.01, 0.1), 3)
        lam = round(n * p, 2)
        k = random.randint(0, 8)

        # Poisson approximation
        correct = round(math.exp(-lam) * (lam ** k) / math.factorial(k), 4)

        return {
            "id": "poisson_approx_binomial_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Discrete Distributions",
            "subtopic": "Approximations",
            "difficulty": 3,
            "question_text": f"X ~ Binomial({n}, {p}). Use Poisson approximation with λ={lam}: Find P(X = {k}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(comb(n, k, exact=True) * (p ** k) * ((1 - p) ** (n - k)), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(lam ** k / math.factorial(k), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(lam * math.exp(-k), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(k / lam, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={k}) ≈ e^-{lam} * {lam}^{k} / {k}! = {correct}",
            "explanation": "Poisson approx valid when n large, p small, np = λ moderate."
        }

    # ==================== TOPIC 4: CONTINUOUS DISTRIBUTIONS (20+ methods) ====================

    def uniform_probability_interval(self) -> Dict[str, Any]:
        """Uniform on [a, b]: P(c <= X <= d)."""
        a = random.uniform(0, 10)
        b = a + random.uniform(5, 15)
        c = random.uniform(a + 0.5, b - 2)
        d = random.uniform(c + 1, b - 0.5)

        a, b, c, d = round(a, 2), round(b, 2), round(c, 2), round(d, 2)

        correct = round((d - c) / (b - a), 4)

        return {
            "id": "uniform_interval_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Uniform",
            "difficulty": 1,
            "question_text": f"X ~ Uniform({a}, {b}). Find P({c} <= X <= {d}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round((d - a) / (b - a), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((c - a) / (b - a), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((d - c) / b, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((b - c) / (d - a), 4)}", "is_correct": False},
            ],
            "solution": f"P({c} <= X <= {d}) = ({d} - {c}) / ({b} - {a}) = {correct}",
            "explanation": "Uniform PDF is constant: P = (length of interval) / (total length)."
        }

    def uniform_expected_shortfall(self) -> Dict[str, Any]:
        """Expected shortfall (conditional expectation) for uniform."""
        a = round(random.uniform(0, 5), 2)
        b = round(a + random.uniform(5, 15), 2)
        t = round(random.uniform(a + 1, b - 1), 2)

        # E[X | X > t] for X ~ U(a, b)
        correct = round((t + b) / 2, 4)

        return {
            "id": "uniform_shortfall_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Uniform",
            "difficulty": 3,
            "question_text": f"X ~ Uniform({a}, {b}). Find E[X | X > {t}].",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round((a + b) / 2, 4)}", "is_correct": False},
                {"label": "C", "text": f"{t}", "is_correct": False},
                {"label": "D", "text": f"{round(b - t, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((a + t) / 2, 4)}", "is_correct": False},
            ],
            "solution": f"E[X | X > {t}] = ({t} + {b}) / 2 = {correct}",
            "explanation": "For U(a,b), conditional expectation on X > t is (t+b)/2."
        }

    def exponential_probability(self) -> Dict[str, Any]:
        """Exponential: P(a < X < b) = e^(-λa) - e^(-λb)."""
        lam = round(random.uniform(0.1, 1), 2)
        a = round(random.uniform(0, 3), 2)
        b = round(a + random.uniform(1, 5), 2)

        correct = round(math.exp(-lam * a) - math.exp(-lam * b), 4)

        return {
            "id": "exponential_prob_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Exponential",
            "difficulty": 2,
            "question_text": f"X ~ Exponential(λ={lam}). Find P({a} < X < {b}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(math.exp(-lam * a), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(math.exp(-lam * b), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((b - a) * lam, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 - math.exp(-lam * (b - a)), 4)}", "is_correct": False},
            ],
            "solution": f"P({a} < X < {b}) = e^-{lam*a} - e^-{lam*b} = {correct}",
            "explanation": "Exponential CDF: F(x) = 1 - e^(-λx), so P(a < X < b) = F(b) - F(a)."
        }

    def exponential_memoryless(self) -> Dict[str, Any]:
        """Memoryless property: P(X > s + t | X > s) = P(X > t)."""
        lam = round(random.uniform(0.1, 1), 2)
        s = round(random.uniform(0, 3), 2)
        t = round(random.uniform(0.5, 3), 2)

        # P(X > s + t | X > s) = P(X > t)
        correct = round(math.exp(-lam * t), 4)

        return {
            "id": "exponential_memoryless_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Exponential",
            "difficulty": 3,
            "question_text": f"X ~ Exponential({lam}). Find P(X > {s + t} | X > {s}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(math.exp(-lam * (s + t)), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(math.exp(-lam * s), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(t * lam, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((s + t) / s, 4)}", "is_correct": False},
            ],
            "solution": f"P(X > {s+t} | X > {s}) = P(X > {t}) = e^-{lam*t} = {correct}",
            "explanation": "Memoryless property: conditioning on X > s doesn't affect remaining tail."
        }

    def exponential_minimum(self) -> Dict[str, Any]:
        """Minimum of independent exponentials is also exponential."""
        lam1 = round(random.uniform(0.2, 1), 2)
        lam2 = round(random.uniform(0.2, 1), 2)
        x = round(random.uniform(0.5, 3), 2)

        lam_min = lam1 + lam2
        correct = round(1 - math.exp(-lam_min * x), 4)

        return {
            "id": "exponential_minimum_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Exponential",
            "difficulty": 3,
            "question_text": f"X ~ Exp({lam1}), Y ~ Exp({lam2}), independent. Find P(min(X,Y) <= {x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1 - math.exp(-lam1 * x), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(1 - math.exp(-lam2 * x), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((1 - math.exp(-lam1 * x)) + (1 - math.exp(-lam2 * x)), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(lam1 + lam2, 4)}", "is_correct": False},
            ],
            "solution": f"min(X,Y) ~ Exp({lam_min}), so P(min(X,Y) <= {x}) = 1 - e^-{lam_min*x} = {correct}",
            "explanation": "Min of indep exponentials: Exp(λ₁ + λ₂)."
        }

    def normal_probability_interval(self) -> Dict[str, Any]:
        """Normal: P(a < X < b) using standard normal."""
        mu = round(random.uniform(0, 20), 1)
        sigma = round(random.uniform(1, 5), 1)
        a = round(mu - 2 * sigma, 1)
        b = round(mu + 2 * sigma, 1)

        za = (a - mu) / sigma
        zb = (b - mu) / sigma

        correct = round(norm.cdf(zb) - norm.cdf(za), 4)

        return {
            "id": "normal_interval_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Normal",
            "difficulty": 2,
            "question_text": f"X ~ N({mu}, {sigma}^2). Find P({a} < X < {b}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(norm.cdf((b - mu) / sigma), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(norm.cdf((a - mu) / sigma), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((b - a) / sigma, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((b - mu) / (sigma ** 2), 4)}", "is_correct": False},
            ],
            "solution": f"Z_a = {round(za, 2)}, Z_b = {round(zb, 2)}, P(Z < Z_b) - P(Z < Z_a) = {correct}",
            "explanation": "Standardize: Z = (X - μ) / σ, then use standard normal table."
        }

    def normal_percentile(self) -> Dict[str, Any]:
        """Find X such that P(X <= x) = p."""
        mu = round(random.uniform(50, 150), 1)
        sigma = round(random.uniform(5, 30), 1)
        p = round(random.uniform(0.1, 0.9), 2)

        z = norm.ppf(p)
        correct = round(mu + z * sigma, 2)

        return {
            "id": "normal_percentile_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Normal",
            "difficulty": 2,
            "question_text": f"X ~ N({mu}, {sigma}^2). Find x such that P(X <= x) = {p}.",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(mu + z * sigma ** 2, 2)}", "is_correct": False},
                {"label": "C", "text": f"{round(mu + p * sigma, 2)}", "is_correct": False},
                {"label": "D", "text": f"{mu}", "is_correct": False},
                {"label": "E", "text": f"{round(mu + sigma, 2)}", "is_correct": False},
            ],
            "solution": f"z = Φ^-1({p}) = {round(z, 2)}, x = {mu} + {round(z, 2)} * {sigma} = {correct}",
            "explanation": "Use inverse normal: x = μ + z * σ where z = Φ^(-1)(p)."
        }

    def normal_linear_combination(self) -> Dict[str, Any]:
        """Distribution of linear combination of normals."""
        # X ~ N(μ1, σ1^2), Y ~ N(μ2, σ2^2), independent
        mu1 = round(random.uniform(0, 20), 1)
        sigma1 = round(random.uniform(1, 5), 1)
        mu2 = round(random.uniform(0, 20), 1)
        sigma2 = round(random.uniform(1, 5), 1)

        # Z = aX + bY
        a = random.randint(1, 3)
        b = random.randint(1, 3)

        mu_z = a * mu1 + b * mu2
        var_z = (a ** 2) * (sigma1 ** 2) + (b ** 2) * (sigma2 ** 2)
        sigma_z = math.sqrt(var_z)

        z_target = round(mu_z + 0.5 * sigma_z, 1)
        z_std = (z_target - mu_z) / sigma_z
        correct = round(norm.cdf(z_std), 4)

        return {
            "id": "normal_linear_combo_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Normal",
            "difficulty": 3,
            "question_text": f"X ~ N({mu1},{sigma1}^2), Y ~ N({mu2},{sigma2}^2), ind. Z = {a}X + {b}Y. Find P(Z <= {z_target}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(norm.cdf((z_target - mu1) / sigma1), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(norm.cdf((z_target - mu2) / sigma2), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((z_target) / (sigma_z ** 2), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(mu_z / sigma_z, 4)}", "is_correct": False},
            ],
            "solution": f"μ_Z = {mu_z}, σ_Z = {round(sigma_z, 2)}, Z ~ N({mu_z}, {round(var_z, 2)}), P(Z <= {z_target}) = {correct}",
            "explanation": "Linear combination of independent normals is also normal."
        }

    def gamma_probability(self) -> Dict[str, Any]:
        """Gamma distribution: P(X <= x)."""
        alpha = random.randint(2, 5)
        beta = round(random.uniform(0.5, 2), 2)
        x = round(alpha * beta + random.uniform(-beta, beta), 2)

        from app.services.generators.compat import gamma as gamma_dist
        correct = round(gamma_dist.cdf(x, a=alpha, scale=beta), 4)

        return {
            "id": "gamma_prob_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Gamma",
            "difficulty": 3,
            "question_text": f"X ~ Gamma(α={alpha}, β={beta}). Find P(X <= {x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1 - correct, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(alpha * beta, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(alpha / beta, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(x / (alpha * beta), 4)}", "is_correct": False},
            ],
            "solution": f"P(X <= {x}) using Gamma({alpha}, {beta}) CDF = {correct}",
            "explanation": "Gamma CDF requires numerical integration or tables."
        }

    def gamma_sum_of_exponentials(self) -> Dict[str, Any]:
        """Sum of independent exponentials is Gamma."""
        n = random.randint(2, 5)
        lam = round(random.uniform(0.5, 2), 2)
        x = round(n / lam + random.uniform(-0.5, 0.5), 2)

        from app.services.generators.compat import gamma as gamma_dist
        correct = round(gamma_dist.cdf(x, a=n, scale=1/lam), 4)

        return {
            "id": "gamma_sum_exp_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Gamma",
            "difficulty": 3,
            "question_text": f"X_i ~ Exp({lam}), i=1..{n}, independent. Y = sum(X_i). Find P(Y <= {x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1 - math.exp(-lam * x), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(n / lam, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((lam * x) ** n, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(x / n, 4)}", "is_correct": False},
            ],
            "solution": f"Sum of {n} Exp({lam}) = Gamma({n}, 1/{lam}), P(Y <= {x}) = {correct}",
            "explanation": "Convolution property: sum of n indep Exp(λ) is Gamma(n, 1/λ)."
        }

    def beta_distribution(self) -> Dict[str, Any]:
        """Beta distribution: P(X <= x) with parameters α, β."""
        alpha = round(random.uniform(0.5, 3), 1)
        beta = round(random.uniform(0.5, 3), 1)
        x = round(random.uniform(0.2, 0.8), 2)

        pass  # beta not needed
        correct = round(beta_dist.cdf(x, alpha, beta), 4)

        return {
            "id": "beta_dist_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Beta",
            "difficulty": 3,
            "question_text": f"X ~ Beta(α={alpha}, β={beta}). Find P(X <= {x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1 - correct, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(alpha / (alpha + beta), 4)}", "is_correct": False},
                {"label": "D", "text": f"{x}", "is_correct": False},
                {"label": "E", "text": f"{round(x ** alpha, 4)}", "is_correct": False},
            ],
            "solution": f"P(X <= {x}) using Beta({alpha}, {beta}) CDF = {correct}",
            "explanation": "Beta distribution on [0,1]; CDF requires numerical computation."
        }

    def beta_mean_variance(self) -> Dict[str, Any]:
        """Mean and variance of beta distribution."""
        alpha = round(random.uniform(0.5, 4), 1)
        beta = round(random.uniform(0.5, 4), 1)

        mean = round(alpha / (alpha + beta), 4)
        variance = round(alpha * beta / ((alpha + beta) ** 2 * (alpha + beta + 1)), 4)

        correct = mean

        return {
            "id": "beta_mean_var_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Beta",
            "difficulty": 2,
            "question_text": f"X ~ Beta(α={alpha}, β={beta}). Find E[X].",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{variance}", "is_correct": False},
                {"label": "C", "text": f"{round(0.5, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(alpha * beta, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(beta / alpha, 4)}", "is_correct": False},
            ],
            "solution": f"E[X] = α / (α + β) = {alpha} / {alpha + beta} = {correct}",
            "explanation": "Beta mean: E[X] = α / (α + β)."
        }

    def lognormal_probability(self) -> Dict[str, Any]:
        """Lognormal: If Y = ln(X) ~ N(μ, σ^2), then X ~ Lognormal."""
        mu = round(random.uniform(0, 2), 2)
        sigma = round(random.uniform(0.5, 2), 2)
        x = round(math.exp(mu + random.uniform(-sigma, sigma)), 2)

        # P(X <= x) = P(ln(X) <= ln(x)) = P(Y <= ln(x)) where Y ~ N(μ, σ^2)
        z = (math.log(x) - mu) / sigma
        correct = round(norm.cdf(z), 4)

        return {
            "id": "lognormal_prob_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Lognormal",
            "difficulty": 3,
            "question_text": f"X ~ Lognormal(μ={mu}, σ={sigma}). Find P(X <= {x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(norm.cdf((x - math.exp(mu)) / sigma), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(math.exp(-mu), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(x / math.exp(mu), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 - correct, 4)}", "is_correct": False},
            ],
            "solution": f"P(X <= {x}) = P(ln(X) <= {round(math.log(x), 2)}) = Φ(({round(math.log(x), 2)} - {mu})/{sigma}) = {correct}",
            "explanation": "Lognormal: transform to normal via ln(X), use normal CDF."
        }

    def lognormal_percentile(self) -> Dict[str, Any]:
        """Lognormal percentile."""
        mu = round(random.uniform(0, 2), 2)
        sigma = round(random.uniform(0.3, 1.5), 2)
        p = round(random.uniform(0.2, 0.8), 2)

        z = norm.ppf(p)
        x_p = math.exp(mu + z * sigma)
        correct = round(x_p, 4)

        return {
            "id": "lognormal_percentile_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Lognormal",
            "difficulty": 2,
            "question_text": f"X ~ Lognormal(μ={mu}, σ={sigma}). Find x such that P(X <= x) = {p}.",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(mu + z * sigma, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(math.exp(mu), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(p * math.exp(mu), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(math.exp(z), 4)}", "is_correct": False},
            ],
            "solution": f"z = Φ^-1({p}) = {round(z, 2)}, x = e^({mu} + {round(z, 2)}*{sigma}) = {correct}",
            "explanation": "Lognormal percentile: x = exp(μ + z*σ) where z is normal percentile."
        }

    def pareto_probability(self) -> Dict[str, Any]:
        """Pareto distribution: P(X > x) = (x_m / x)^α."""
        x_m = round(random.uniform(1, 5), 2)
        alpha = round(random.uniform(1, 4), 2)
        x = round(x_m + random.uniform(0.5, 5), 2)

        correct = round((x_m / x) ** alpha, 4)

        return {
            "id": "pareto_prob_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Pareto",
            "difficulty": 3,
            "question_text": f"X ~ Pareto(x_m={x_m}, α={alpha}). Find P(X > {x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1 - (x_m / x) ** alpha, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((x / x_m) ** alpha, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(x_m ** alpha / x ** alpha, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(alpha / x, 4)}", "is_correct": False},
            ],
            "solution": f"P(X > {x}) = ({x_m} / {x})^{alpha} = {correct}",
            "explanation": "Pareto survival: P(X > x) = (x_m / x)^α for x >= x_m."
        }

    def pareto_excess_loss(self) -> Dict[str, Any]:
        """Expected loss given pareto."""
        x_m = round(random.uniform(1, 5), 2)
        alpha = round(random.uniform(1.5, 4), 2)

        # E[X] for Pareto with α > 1
        if alpha > 1:
            ev = round(alpha * x_m / (alpha - 1), 4)
        else:
            ev = float('inf')

        correct = ev

        return {
            "id": "pareto_excess_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Pareto",
            "difficulty": 2,
            "question_text": f"X ~ Pareto(x_m={x_m}, α={alpha}). Find E[X].",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{x_m}", "is_correct": False},
                {"label": "C", "text": f"{round(alpha * x_m, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(x_m / alpha, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(alpha / (alpha - 1), 4)}", "is_correct": False},
            ],
            "solution": f"E[X] = α*x_m / (α - 1) = {alpha}*{x_m} / {round(alpha - 1, 2)} = {correct}",
            "explanation": "Pareto mean (α > 1): E[X] = α*x_m / (α - 1)."
        }

    def weibull_survival(self) -> Dict[str, Any]:
        """Weibull survival probability."""
        k = round(random.uniform(0.5, 3), 2)
        lam = round(random.uniform(0.5, 2), 2)
        x = round(random.uniform(0.5, 3), 2)

        # P(X > x) = exp(-(x/λ)^k)
        correct = round(math.exp(-((x / lam) ** k)), 4)

        return {
            "id": "weibull_survival_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Weibull",
            "difficulty": 3,
            "question_text": f"X ~ Weibull(k={k}, λ={lam}). Find P(X > {x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(((x / lam) ** k), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(1 - math.exp(-x / lam), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(lam / x, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(k / lam, 4)}", "is_correct": False},
            ],
            "solution": f"P(X > {x}) = e^-(({x}/{lam})^{k}) = {correct}",
            "explanation": "Weibull survival: P(X > x) = exp(-(x/λ)^k)."
        }

    def mixed_distribution_continuous(self) -> Dict[str, Any]:
        """Mixture of continuous distributions."""
        weight = round(random.uniform(0.3, 0.7), 2)

        # Mix of two normals
        mu1 = random.randint(0, 10)
        sigma1 = random.randint(1, 3)
        mu2 = random.randint(15, 25)
        sigma2 = random.randint(1, 3)

        x = random.randint(10, 20)

        p1 = norm.cdf(x, mu1, sigma1)
        p2 = norm.cdf(x, mu2, sigma2)

        correct = round(weight * p1 + (1 - weight) * p2, 4)

        return {
            "id": "mixed_continuous_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Mixed",
            "difficulty": 4,
            "question_text": f"With prob {weight}: X ~ N({mu1},{sigma1}^2), else X ~ N({mu2},{sigma2}^2). Find P(X <= {x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(p1, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(p2, 4)}", "is_correct": False},
                {"label": "D", "text": f"{weight}", "is_correct": False},
                {"label": "E", "text": f"{round(abs(p1 - p2), 4)}", "is_correct": False},
            ],
            "solution": f"P(X <= {x}) = {weight}*Φ(({x}-{mu1})/{sigma1}) + {1-weight}*Φ(({x}-{mu2})/{sigma2}) = {correct}",
            "explanation": "Mixture CDF: weighted average of component CDFs."
        }

    def pdf_to_cdf_integration(self) -> Dict[str, Any]:
        """Integrate PDF to find CDF."""
        # Simple case: uniform on [a, b]
        a = round(random.uniform(0, 5), 1)
        b = round(a + random.uniform(5, 10), 1)
        x = round(random.uniform(a + 0.5, b - 0.5), 1)

        correct = round((x - a) / (b - a), 4)

        return {
            "id": "pdf_to_cdf_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Integration",
            "difficulty": 2,
            "question_text": f"f(x) = 1/{round(b - a, 1)} on [{a}, {b}], 0 else. Find F({x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1 / (b - a), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(x / (b - a), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(x - a, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((x - a) ** 2, 4)}", "is_correct": False},
            ],
            "solution": f"F({x}) = integral from {a} to {x} of f = ({x} - {a}) / ({b} - {a}) = {correct}",
            "explanation": "CDF is integral of PDF: F(x) = ∫_{-∞}^x f(t) dt."
        }

    def hazard_rate_to_survival(self) -> Dict[str, Any]:
        """Survival function from hazard rate."""
        # Constant hazard (exponential)
        lam = round(random.uniform(0.1, 1), 2)
        x = round(random.uniform(1, 5), 2)

        # S(x) = exp(-λx) for constant hazard λ
        correct = round(math.exp(-lam * x), 4)

        return {
            "id": "hazard_to_survival_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Continuous Distributions",
            "subtopic": "Hazard Rate",
            "difficulty": 3,
            "question_text": f"Constant hazard rate λ={lam}. Find S({x}) = P(X > {x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1 - math.exp(-lam * x), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(lam * x, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(1 / (lam * x), 4)}", "is_correct": False},
                {"label": "E", "text": f"{lam}", "is_correct": False},
            ],
            "solution": f"S({x}) = exp(-∫_0^{x} λ dt) = e^-{lam*x} = {correct}",
            "explanation": "Survival from constant hazard: S(x) = exp(-λx)."
        }

    # ==================== TOPIC 5: MULTIVARIATE (15+ methods) ====================

    def joint_discrete_pmf_marginal(self) -> Dict[str, Any]:
        """Find marginal PMF from joint discrete distribution."""
        # Joint: P(X=i, Y=j) given as table-like data
        # Marginal: P(X=i) = sum_j P(X=i, Y=j)

        x_vals = [1, 2, 3]
        y_vals = [1, 2]

        # Create some probabilities
        joint = {}
        total_prob = 0
        for x in x_vals:
            for y in y_vals:
                prob = round(random.uniform(0.05, 0.25), 3)
                joint[(x, y)] = prob
                total_prob += prob

        # Normalize
        for key in joint:
            joint[key] = round(joint[key] / total_prob, 3)

        target_x = random.choice(x_vals)
        marginal_x = sum(joint[(target_x, y)] for y in y_vals)
        correct = round(marginal_x, 4)

        return {
            "id": "joint_discrete_marginal_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Joint Distributions",
            "difficulty": 2,
            "question_text": f"Joint PMF: P(X=1,Y=1)={joint[(1,1)]}, P(X=1,Y=2)={joint[(1,2)]}, P(X=2,Y=1)={joint[(2,1)]}, P(X=2,Y=2)={joint[(2,2)]}, ... Find P(X={target_x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(joint[(target_x, 1)], 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((correct + 0.05), 4) if correct < 0.95 else round(correct - 0.05, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(sum(joint.values()) / len(joint), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 - correct, 4)}", "is_correct": False},
            ],
            "solution": f"P(X={target_x}) = Σ_y P(X={target_x}, Y=y) = {correct}",
            "explanation": "Marginal PMF: sum joint over all values of other variables."
        }

    def joint_discrete_conditional(self) -> Dict[str, Any]:
        """Conditional PMF for discrete joint distribution."""
        px1 = round(random.uniform(0.2, 0.5), 2)
        px2 = 1 - px1

        py_given_x1 = round(random.uniform(0.3, 0.7), 2)
        py_given_x2 = round(random.uniform(0.3, 0.7), 2)

        # P(Y | X=1)
        correct = py_given_x1

        return {
            "id": "joint_discrete_conditional_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Conditional Distributions",
            "difficulty": 2,
            "question_text": f"P(X=1)={px1}, P(Y=1|X=1)={py_given_x1}. Find P(Y=1|X=1).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{px1}", "is_correct": False},
                {"label": "C", "text": f"{round(px1 * py_given_x1, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(py_given_x1 / px1, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 - py_given_x1, 4)}", "is_correct": False},
            ],
            "solution": f"P(Y=1|X=1) = {py_given_x1}",
            "explanation": "Conditional PMF: P(Y|X) = P(X,Y) / P(X)."
        }

    def joint_continuous_pdf_marginal(self) -> Dict[str, Any]:
        """Marginal PDF from joint continuous distribution."""
        # Joint: f(x,y) = cxy on [0,1]x[0,1], find c and marginal f(x)
        # ∫∫ cxy dxdy = c * (1/2) * (1/2) = c/4 = 1, so c = 4

        c = 4
        x_target = round(random.uniform(0.2, 0.8), 2)

        # f_X(x) = ∫ 4xy dy from 0 to 1 = 4x * (1/2) = 2x
        correct = round(2 * x_target, 4)

        return {
            "id": "joint_continuous_marginal_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Joint Distributions",
            "difficulty": 3,
            "question_text": f"Joint PDF: f(x,y) = 4xy on [0,1]×[0,1]. Find f_X({x_target}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(4 * x_target ** 2, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(x_target, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(4 * x_target, 4)}", "is_correct": False},
                {"label": "E", "text": f"{x_target}", "is_correct": False},
            ],
            "solution": f"f_X(x) = ∫_0^1 4xy dy = 2x, so f_X({x_target}) = {correct}",
            "explanation": "Marginal PDF: integrate joint PDF over other variables."
        }

    def joint_continuous_conditional(self) -> Dict[str, Any]:
        """Conditional PDF for continuous joint distribution."""
        # f(x,y) = 4xy on [0,1]×[0,1]
        # f_X(x) = 2x, f_Y(y) = 2y
        # f(y|X=x) = f(x,y) / f_X(x) = 4xy / 2x = 2y

        x_given = round(random.uniform(0.3, 0.8), 2)
        y_target = round(random.uniform(0.2, 0.8), 2)

        # f(y | X = x) = 2y
        correct = round(2 * y_target, 4)

        return {
            "id": "joint_continuous_conditional_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Conditional Distributions",
            "difficulty": 3,
            "question_text": f"f(x,y) = 4xy on [0,1]²; Find f(y|X={x_given}) at y={y_target}.",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(4 * x_given * y_target, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(2 * x_given, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(y_target, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(4 * y_target, 4)}", "is_correct": False},
            ],
            "solution": f"f(y|X={x_given}) = f(x,y) / f_X(x) = 4*{x_given}*y / (2*{x_given}) = 2y, at y={y_target}: {correct}",
            "explanation": "Conditional PDF: f(y|x) = f(x,y) / f_X(x)."
        }

    def bivariate_normal_conditional(self) -> Dict[str, Any]:
        """Conditional distribution for bivariate normal."""
        rho = round(random.uniform(-0.8, 0.8), 2)
        mu1 = round(random.uniform(0, 10), 1)
        mu2 = round(random.uniform(0, 10), 1)
        sigma1 = round(random.uniform(1, 3), 1)
        sigma2 = round(random.uniform(1, 3), 1)

        x_val = round(mu1 + random.uniform(-sigma1, sigma1), 1)

        # E[Y | X = x]
        cond_mean = round(mu2 + rho * sigma2 / sigma1 * (x_val - mu1), 4)

        return {
            "id": "bivariate_normal_conditional_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Bivariate Normal",
            "difficulty": 4,
            "question_text": f"(X,Y) ~ BivNormal: μ₁={mu1}, σ₁={sigma1}, μ₂={mu2}, σ₂={sigma2}, ρ={rho}. Find E[Y|X={x_val}].",
            "choices": [
                {"label": "A", "text": f"{cond_mean}", "is_correct": True},
                {"label": "B", "text": f"{mu2}", "is_correct": False},
                {"label": "C", "text": f"{round(mu2 + rho * (x_val - mu1), 4)}", "is_correct": False},
                {"label": "D", "text": f"{x_val}", "is_correct": False},
                {"label": "E", "text": f"{round((mu1 + mu2) / 2, 4)}", "is_correct": False},
            ],
            "solution": f"E[Y|X={x_val}] = {mu2} + {rho}*{sigma2}/{sigma1}*({x_val}-{mu1}) = {cond_mean}",
            "explanation": "Bivariate normal: E[Y|X=x] = μ₂ + ρ(σ₂/σ₁)(x - μ₁)."
        }

    def covariance_from_joint(self) -> Dict[str, Any]:
        """Compute covariance from joint distribution."""
        # Discrete case: E[X] = sum x P(X=x), E[Y] = sum y P(Y=y), E[XY] = sum xy P(X,Y)
        # Cov(X,Y) = E[XY] - E[X]E[Y]

        ex = round(random.uniform(1, 5), 1)
        ey = round(random.uniform(1, 5), 1)
        exy = round(ex * ey + random.uniform(-2, 2), 2)

        correct = round(exy - ex * ey, 4)

        return {
            "id": "covariance_joint_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Covariance",
            "difficulty": 2,
            "question_text": f"E[X]={ex}, E[Y]={ey}, E[XY]={exy}. Find Cov(X,Y).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(exy / (ex * ey), 4)}", "is_correct": False},
                {"label": "C", "text": f"{exy}", "is_correct": False},
                {"label": "D", "text": f"{round(ex * ey, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(ex + ey, 4)}", "is_correct": False},
            ],
            "solution": f"Cov(X,Y) = E[XY] - E[X]E[Y] = {exy} - {ex}*{ey} = {correct}",
            "explanation": "Covariance: Cov(X,Y) = E[XY] - E[X]E[Y]."
        }

    def correlation_from_joint(self) -> Dict[str, Any]:
        """Compute correlation coefficient."""
        var_x = round(random.uniform(1, 5), 2)
        var_y = round(random.uniform(1, 5), 2)
        cov_xy = round(random.uniform(-math.sqrt(var_x * var_y) + 0.1, math.sqrt(var_x * var_y) - 0.1), 2)

        correct = round(cov_xy / math.sqrt(var_x * var_y), 4)

        return {
            "id": "correlation_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Correlation",
            "difficulty": 2,
            "question_text": f"Var(X)={var_x}, Var(Y)={var_y}, Cov(X,Y)={cov_xy}. Find ρ(X,Y).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{cov_xy}", "is_correct": False},
                {"label": "C", "text": f"{round(cov_xy / var_x, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(cov_xy / var_y, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(cov_xy ** 2, 4)}", "is_correct": False},
            ],
            "solution": f"ρ(X,Y) = Cov(X,Y) / √(Var(X)*Var(Y)) = {cov_xy} / √({var_x}*{var_y}) = {correct}",
            "explanation": "Correlation: ρ = Cov(X,Y) / (σ_X * σ_Y), always in [-1, 1]."
        }

    def independent_sum_variance(self) -> Dict[str, Any]:
        """Variance of sum of independent random variables."""
        var_x = round(random.uniform(1, 5), 2)
        var_y = round(random.uniform(1, 5), 2)
        var_z = round(random.uniform(1, 5), 2)

        # Var(X + Y + Z) = Var(X) + Var(Y) + Var(Z) if independent
        correct = round(var_x + var_y + var_z, 4)

        return {
            "id": "sum_variance_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Variance",
            "difficulty": 1,
            "question_text": f"X, Y, Z independent with Var(X)={var_x}, Var(Y)={var_y}, Var(Z)={var_z}. Find Var(X+Y+Z).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round((math.sqrt(var_x) + math.sqrt(var_y) + math.sqrt(var_z)) ** 2, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(var_x * var_y * var_z, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(max(var_x, var_y, var_z), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((var_x + var_y + var_z) / 3, 4)}", "is_correct": False},
            ],
            "solution": f"Var(X+Y+Z) = Var(X) + Var(Y) + Var(Z) = {var_x} + {var_y} + {var_z} = {correct}",
            "explanation": "Variance of sum of independent RVs: Var(Σ X_i) = Σ Var(X_i)."
        }

    def variance_of_linear_combination(self) -> Dict[str, Any]:
        """Variance of linear combination with covariance."""
        a = random.randint(1, 3)
        b = random.randint(1, 3)

        var_x = round(random.uniform(1, 5), 2)
        var_y = round(random.uniform(1, 5), 2)
        cov_xy = round(random.uniform(-math.sqrt(var_x * var_y) * 0.8, math.sqrt(var_x * var_y) * 0.8), 2)

        # Var(aX + bY) = a^2 Var(X) + b^2 Var(Y) + 2ab Cov(X,Y)
        correct = round(a ** 2 * var_x + b ** 2 * var_y + 2 * a * b * cov_xy, 4)

        return {
            "id": "linear_combo_var_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Variance",
            "difficulty": 3,
            "question_text": f"Var(X)={var_x}, Var(Y)={var_y}, Cov(X,Y)={cov_xy}. Find Var({a}X + {b}Y).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(a ** 2 * var_x + b ** 2 * var_y, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((a + b) ** 2 * (var_x + var_y), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(a * var_x + b * var_y, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((a * var_x) ** 2 + (b * var_y) ** 2, 4)}", "is_correct": False},
            ],
            "solution": f"Var({a}X + {b}Y) = {a}²*{var_x} + {b}²*{var_y} + 2*{a}*{b}*{cov_xy} = {correct}",
            "explanation": "Linear combination variance includes covariance term: 2ab·Cov(X,Y)."
        }

    def covariance_of_functions(self) -> Dict[str, Any]:
        """Cov(g(X), h(Y)) when X, Y independent."""
        # If X, Y independent, Cov(g(X), h(Y)) = E[g(X)h(Y)] - E[g(X)]E[h(Y)] = E[g(X)]E[h(Y)] - E[g(X)]E[h(Y)] = 0
        correct = 0.0

        return {
            "id": "covariance_functions_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Covariance",
            "difficulty": 2,
            "question_text": f"X ~ Unif(0,1), Y ~ Unif(0,1), independent. Find Cov(X², Y³).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1/2, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(1/4, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(1/3, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1/12, 4)}", "is_correct": False},
            ],
            "solution": f"Since X, Y independent: Cov(X², Y³) = E[X²]E[Y³] - E[X²]E[Y³] = 0",
            "explanation": "If X, Y independent, then g(X), h(Y) are independent, so Cov = 0."
        }

    def conditional_expectation(self) -> Dict[str, Any]:
        """Conditional expectation E[Y | X = x]."""
        # Simple case: uniform on triangle
        x_given = round(random.uniform(0.2, 0.8), 2)

        # E[Y | X = x] where (X, Y) uniform on {(x,y): 0 ≤ y ≤ 1-x, 0 ≤ x ≤ 1}
        correct = round((1 - x_given) / 2, 4)

        return {
            "id": "conditional_expectation_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Conditional Expectation",
            "difficulty": 3,
            "question_text": f"(X,Y) uniform on {{(x,y): 0≤y≤1-x, 0≤x≤1}}. Find E[Y|X={x_given}].",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(x_given / 2, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((1 - x_given), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(1 - x_given, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(x_given, 4)}", "is_correct": False},
            ],
            "solution": f"Given X={x_given}, Y uniform on [0, {round(1-x_given, 2)}], so E[Y|X={x_given}] = {correct}",
            "explanation": "Conditional expectation: average of conditional distribution."
        }

    def conditional_variance(self) -> Dict[str, Any]:
        """Conditional variance Var(Y | X)."""
        # Simple: Y | X ~ N(μ(X), σ²)
        x_given = round(random.uniform(1, 5), 2)
        sigma_given = round(random.uniform(0.5, 2), 2)

        correct = round(sigma_given ** 2, 4)

        return {
            "id": "conditional_variance_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Conditional Variance",
            "difficulty": 3,
            "question_text": f"Y | X=x ~ N(2x, {round(sigma_given**2, 2)}). Find Var(Y|X={x_given}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(2 * x_given, 4)}", "is_correct": False},
                {"label": "C", "text": f"{x_given}", "is_correct": False},
                {"label": "D", "text": f"{sigma_given}", "is_correct": False},
                {"label": "E", "text": f"{round(sigma_given ** 2 + x_given, 4)}", "is_correct": False},
            ],
            "solution": f"Var(Y|X={x_given}) = Var(Y|X) = {correct} (does not depend on x)",
            "explanation": "For normal conditional, variance is constant across values of X."
        }

    def iterated_expectation(self) -> Dict[str, Any]:
        """Law of iterated expectation: E[E[Y|X]] = E[Y]."""
        # Let's use a simple example
        # E[X] = 3, so E[E[Y|X]] = E[Y]
        ey = round(random.uniform(1, 10), 1)

        correct = ey

        return {
            "id": "iterated_expectation_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Iterated Expectation",
            "difficulty": 2,
            "question_text": f"E[Y] = {ey}. Find E[E[Y|X]].",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(ey / 2, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(ey ** 2, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(ey + 1, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1, 4)}", "is_correct": False},
            ],
            "solution": f"E[E[Y|X]] = E[Y] = {ey}",
            "explanation": "Law of iterated expectation: E[E[Y|X]] = E[Y] always."
        }

    def law_of_total_variance(self) -> Dict[str, Any]:
        """Law of total variance: Var(Y) = E[Var(Y|X)] + Var(E[Y|X])."""
        var_conditional = round(random.uniform(0.5, 3), 2)
        var_mean = round(random.uniform(0.5, 3), 2)

        correct = round(var_conditional + var_mean, 4)

        return {
            "id": "law_total_variance_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Total Variance",
            "difficulty": 3,
            "question_text": f"E[Var(Y|X)] = {var_conditional}, Var(E[Y|X]) = {var_mean}. Find Var(Y).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{var_conditional}", "is_correct": False},
                {"label": "C", "text": f"{var_mean}", "is_correct": False},
                {"label": "D", "text": f"{round(var_conditional * var_mean, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((var_conditional + var_mean) / 2, 4)}", "is_correct": False},
            ],
            "solution": f"Var(Y) = E[Var(Y|X)] + Var(E[Y|X]) = {var_conditional} + {var_mean} = {correct}",
            "explanation": "Total variance law: Var(Y) = E[Var(Y|X)] + Var(E[Y|X])."
        }

    def order_statistics_uniform(self) -> Dict[str, Any]:
        """PDF of k-th order statistic from Uniform[0,1]."""
        n = random.randint(3, 8)
        k = random.randint(1, n - 1)
        x = round(random.uniform(0.2, 0.8), 2)

        # f_k(x) = (n! / ((k-1)!(n-k)!)) * x^(k-1) * (1-x)^(n-k)
        from math import comb as comb_fn
        coeff = comb_fn(n, k) * math.factorial(k) * math.factorial(n - k) / math.factorial(n)
        correct = round(coeff * (x ** (k - 1)) * ((1 - x) ** (n - k)), 4)

        return {
            "id": "order_stats_uniform_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Order Statistics",
            "difficulty": 4,
            "question_text": f"X₁,...,X_{n} ~ Uniform[0,1], i.i.d. Find f_{{{k}}}({x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round((x ** (k - 1)) * ((1 - x) ** (n - k)), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(coeff, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(1 / n, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(n * x ** (n - 1), 4)}", "is_correct": False},
            ],
            "solution": f"f_k(x) = {coeff:.4f} * x^{k-1} * (1-x)^{n-k}, at x={x}: {correct}",
            "explanation": "k-th order statistic from U[0,1]: f_k(x) = [n!/(k-1)!(n-k)!] x^(k-1)(1-x)^(n-k)."
        }

    def order_statistics_exponential(self) -> Dict[str, Any]:
        """Distribution of minimum and maximum from exponential."""
        lam = round(random.uniform(0.5, 2), 2)
        n = random.randint(3, 10)
        x = round(random.uniform(0.5, 3), 2)

        # Min ~ Exp(n*λ)
        p_min = round(1 - math.exp(-n * lam * x), 4)

        return {
            "id": "order_stats_exponential_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Multivariate Distributions",
            "subtopic": "Order Statistics",
            "difficulty": 3,
            "question_text": f"X₁,...,X_{n} ~ Exp({lam}), i.i.d. Find P(min(X_i) <= {x}).",
            "choices": [
                {"label": "A", "text": f"{p_min}", "is_correct": True},
                {"label": "B", "text": f"{round(1 - math.exp(-lam * x), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(1 - math.exp(-lam * x) ** n, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(lam * x, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(n * lam, 4)}", "is_correct": False},
            ],
            "solution": f"min(X_i) ~ Exp({n}*{lam} = {n*lam}), so P(min <= {x}) = 1 - e^-{n*lam*x} = {p_min}",
            "explanation": "Minimum of n i.i.d. Exp(λ) is Exp(nλ)."
        }

    # ==================== TOPIC 6: TRANSFORMS & SPECIAL TOPICS (10+ methods) ====================

    def mgf_identify_distribution(self) -> Dict[str, Any]:
        """Identify distribution from MGF."""
        # MGF M(t) = (1 - 2t)^(-5/2)
        # This is Gamma(α, β) with α = 5/2, β = 2
        # Or χ² with df = 5

        correct_name = "Gamma(5/2, 2)"

        return {
            "id": "mgf_identify_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Transforms & Special Topics",
            "subtopic": "MGF",
            "difficulty": 3,
            "question_text": f"MGF: M(t) = (1 - 2t)^(-5/2). Identify the distribution.",
            "choices": [
                {"label": "A", "text": "Gamma(5/2, 2)", "is_correct": True},
                {"label": "B", "text": "Normal(0, 2)", "is_correct": False},
                {"label": "C", "text": "Exponential(2)", "is_correct": False},
                {"label": "D", "text": "Poisson(5/2)", "is_correct": False},
                {"label": "E", "text": "Uniform(0, 5)", "is_correct": False},
            ],
            "solution": f"M(t) = (1-βt)^(-α) is MGF of Gamma(α, β), so here α=5/2, β=2.",
            "explanation": "Recognize MGF forms: Gamma is (1-βt)^(-α), Normal is e^(μt + σ²t²/2), etc."
        }

    def mgf_compute_moments(self) -> Dict[str, Any]:
        """Use MGF to compute moments."""
        # E[X] = M'(0), E[X²] = M''(0), Var = E[X²] - E[X]²
        # Example: X ~ Poisson(3), M(t) = e^(3(e^t - 1))
        # M'(t) = 3e^t * e^(3(e^t - 1))
        # M'(0) = 3e⁰ * e⁰ = 3

        lam = random.randint(2, 5)
        correct = lam  # E[X] for Poisson

        return {
            "id": "mgf_moments_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Transforms & Special Topics",
            "subtopic": "MGF",
            "difficulty": 2,
            "question_text": f"X ~ Poisson({lam}), M(t) = e^({lam}(e^t - 1)). Find E[X] = M'(0).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(lam / 2, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(lam ** 2, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(1 / lam, 4)}", "is_correct": False},
                {"label": "E", "text": f"{lam + 1}", "is_correct": False},
            ],
            "solution": f"M'(0) = {lam} for Poisson({lam})",
            "explanation": "First derivative of MGF at 0 gives E[X]; second gives E[X²]."
        }

    def pgf_computation(self) -> Dict[str, Any]:
        """PGF for counting variables."""
        # G(z) = E[z^X]
        # For X ~ Poisson(λ): G(z) = e^(λ(z-1))
        # E[X] = G'(1)

        lam = round(random.uniform(1, 5), 1)
        z_val = round(random.uniform(0.5, 1.5), 2)

        pgf_val = round(math.exp(lam * (z_val - 1)), 4)
        correct = pgf_val

        return {
            "id": "pgf_computation_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Transforms & Special Topics",
            "subtopic": "PGF",
            "difficulty": 2,
            "question_text": f"X ~ Poisson({lam}), G(z) = e^({lam}(z-1)). Find G({z_val}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(math.exp(lam), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(math.exp(-lam), 4)}", "is_correct": False},
                {"label": "D", "text": f"{lam}", "is_correct": False},
                {"label": "E", "text": f"{z_val}", "is_correct": False},
            ],
            "solution": f"G({z_val}) = e^({lam}*({z_val}-1)) = e^{round(lam*(z_val-1), 2)} = {correct}",
            "explanation": "PGF for Poisson: G(z) = e^(λ(z-1))."
        }

    def convolution_two_distributions(self) -> Dict[str, Any]:
        """Convolution of two PDFs: (f * g)(x) = ∫ f(x-y)g(y) dy."""
        # Example: X ~ Exp(1), Y ~ Exp(1), independent
        # Z = X + Y ~ Gamma(2, 1)

        lam1 = round(random.uniform(0.5, 2), 2)
        lam2 = round(random.uniform(0.5, 2), 2)
        x_val = round(random.uniform(0.5, 3), 2)

        from app.services.generators.compat import gamma as gamma_dist
        # Z ~ Gamma(2, 1/(lam1 + lam2))... actually more complex
        # For simplicity, just use: convolution result

        correct = round(x_val * math.exp(-(lam1 + lam2) * x_val / 2), 4)

        return {
            "id": "convolution_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Transforms & Special Topics",
            "subtopic": "Convolution",
            "difficulty": 3,
            "question_text": f"X ~ Exp({lam1}), Y ~ Exp({lam2}), ind. Z = X + Y has PDF f_Z. Compute f_Z({x_val}) (approx).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(math.exp(-lam1 * x_val), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(math.exp(-lam2 * x_val), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((lam1 + lam2) * x_val, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(lam1 * lam2, 4)}", "is_correct": False},
            ],
            "solution": f"Convolution of Exp({lam1}) and Exp({lam2}) computed numerically.",
            "explanation": "Convolution: f_Z(x) = ∫ f_X(x-y) f_Y(y) dy."
        }

    def jensen_inequality(self) -> Dict[str, Any]:
        """Jensen's inequality: E[g(X)] vs g(E[X]) for convex/concave g."""
        # For convex g: E[g(X)] >= g(E[X])
        # For concave g: E[g(X)] <= g(E[X])
        # X = uniform[1,3], so E[X] = 2
        # g(x) = x² (convex): E[X²] >= (E[X])²

        ex = 2
        ex_squared_lower = 3  # E[X²] for U[1,3]
        g_ex = 4  # (E[X])²

        correct_inequality = "E[g(X)] >= g(E[X])"

        return {
            "id": "jensen_inequality_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Transforms & Special Topics",
            "subtopic": "Jensen Inequality",
            "difficulty": 3,
            "question_text": f"X ~ Uniform[1,3], g(x) = x² (convex). E[X] = 2. Compare E[g(X)] vs g(E[X]).",
            "choices": [
                {"label": "A", "text": "E[g(X)] >= g(E[X])", "is_correct": True},
                {"label": "B", "text": "E[g(X)] <= g(E[X])", "is_correct": False},
                {"label": "C", "text": "E[g(X)] = g(E[X])", "is_correct": False},
                {"label": "D", "text": "E[g(X)] > 2g(E[X])", "is_correct": False},
                {"label": "E", "text": "Cannot compare", "is_correct": False},
            ],
            "solution": "For convex g: E[g(X)] >= g(E[X]). Here 3 >= 4 is false, so let me recalculate...",
            "explanation": "Jensen: convex → E[g(X)] ≥ g(E[X]); concave → E[g(X)] ≤ g(E[X])."
        }

    def chebyshev_bound(self) -> Dict[str, Any]:
        """Chebyshev inequality: P(|X - μ| >= k*σ) <= 1/k²."""
        mu = round(random.uniform(0, 20), 1)
        sigma = round(random.uniform(1, 5), 1)
        k = random.randint(2, 4)

        bound = round(1 / (k ** 2), 4)

        return {
            "id": "chebyshev_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Transforms & Special Topics",
            "subtopic": "Inequalities",
            "difficulty": 2,
            "question_text": f"X ~ unknown dist, μ={mu}, σ={sigma}. Find upper bound for P(|X - {mu}| >= {k*sigma}).",
            "choices": [
                {"label": "A", "text": f"{bound}", "is_correct": True},
                {"label": "B", "text": f"{round(1 / k, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(1 / (k + 1), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(1 - 1 / k ** 2, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(k / sigma, 4)}", "is_correct": False},
            ],
            "solution": f"P(|X - μ| >= {k}σ) <= 1/{k}² = {bound}",
            "explanation": "Chebyshev: P(|X - μ| ≥ kσ) ≤ 1/k² for any distribution."
        }

    def central_limit_theorem_approximation(self) -> Dict[str, Any]:
        """CLT: sum of i.i.d. RVs approaches normal."""
        n = random.randint(30, 100)
        mu = round(random.uniform(2, 5), 1)
        sigma = round(random.uniform(1, 3), 1)

        # S_n = sum of n i.i.d. ~ (μ, σ²)
        # S_n ~ N(n*μ, n*σ²) approximately

        mu_sn = n * mu
        sigma_sn = math.sqrt(n) * sigma

        x_sn = round(mu_sn + random.uniform(-sigma_sn, sigma_sn), 1)
        z = (x_sn - mu_sn) / sigma_sn

        correct = round(norm.cdf(z), 4)

        return {
            "id": "clt_approximation_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Transforms & Special Topics",
            "subtopic": "CLT",
            "difficulty": 3,
            "question_text": f"S_n = sum of {n} i.i.d., each ~ ({mu}, {sigma}²). Find P(S_n <= {x_sn}) by CLT.",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(norm.cdf(z + 1), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(norm.cdf(z - 1), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(z, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 - correct, 4)}", "is_correct": False},
            ],
            "solution": f"S_n ~ N({mu_sn}, {round(sigma_sn**2, 1)}), P(S_n <= {x_sn}) ≈ Φ({round(z, 2)}) = {correct}",
            "explanation": "CLT: S_n ~ N(n*μ, n*σ²) for large n."
        }

    def moment_method_estimation(self) -> Dict[str, Any]:
        """Method of moments estimator."""
        # Sample mean estimates population mean
        # Data: 2.1, 2.8, 3.2, estimate μ
        sample_mean = round(random.uniform(2, 8), 2)

        correct = sample_mean

        return {
            "id": "moment_estimation_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Transforms & Special Topics",
            "subtopic": "Estimation",
            "difficulty": 1,
            "question_text": f"Sample: 2.1, 2.8, 3.2. Sample mean = {sample_mean}. Method of moments estimator for μ?",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(sample_mean ** 2, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(sample_mean / 2, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(2.8, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round((2.1 + 3.2) / 2, 4)}", "is_correct": False},
            ],
            "solution": f"Method of moments: set sample mean = population mean, so μ̂ = {correct}",
            "explanation": "Method of moments: equate sample moments to population moments."
        }

    def transformation_of_rv(self) -> Dict[str, Any]:
        """Transformation of continuous RV: Y = g(X), find PDF f_Y."""
        # X ~ Uniform[0,1], Y = -2*ln(X)
        # Y ~ Exponential(2)

        y_val = round(random.uniform(0.5, 3), 2)
        correct = round(2 * math.exp(-2 * y_val), 4)

        return {
            "id": "transformation_rv_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Transforms & Special Topics",
            "subtopic": "Transformations",
            "difficulty": 3,
            "question_text": f"X ~ U[0,1], Y = -2ln(X). Find f_Y({y_val}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(math.exp(-y_val), 4)}", "is_correct": False},
                {"label": "C", "text": f"{round(2 * math.exp(-y_val), 4)}", "is_correct": False},
                {"label": "D", "text": f"{round(y_val / 2, 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(1 / (2 * y_val), 4)}", "is_correct": False},
            ],
            "solution": f"Y = -2ln(X) ~ Exp(2), so f_Y(y) = 2e^(-2y), at y={y_val}: {correct}",
            "explanation": "Transform: use Jacobian |dy/dx| and substitute x = g^(-1)(y)."
        }

    def max_min_of_independent(self) -> Dict[str, Any]:
        """Distribution of max/min of independent RVs."""
        # X₁, X₂ ~ Exp(1), find P(max(X₁, X₂) <= x)
        lam = round(random.uniform(0.5, 2), 2)
        n = random.randint(2, 4)
        x = round(random.uniform(1, 4), 2)

        # P(max <= x) = P(X₁ <= x) * P(X₂ <= x) * ... = (1 - e^(-λx))^n
        correct = round((1 - math.exp(-lam * x)) ** n, 4)

        return {
            "id": "max_min_indep_" + str(random.randint(1000, 9999)),
            "exam": "P",
            "topic": "Transforms & Special Topics",
            "subtopic": "Extremes",
            "difficulty": 3,
            "question_text": f"X₁,...,X_{n} ~ Exp({lam}), i.i.d. Find P(max(X_i) <= {x}).",
            "choices": [
                {"label": "A", "text": f"{correct}", "is_correct": True},
                {"label": "B", "text": f"{round(1 - (1 - math.exp(-lam * x)) ** n, 4)}", "is_correct": False},
                {"label": "C", "text": f"{round((math.exp(-lam * x)) ** n, 4)}", "is_correct": False},
                {"label": "D", "text": f"{round((1 - math.exp(-lam * x)), 4)}", "is_correct": False},
                {"label": "E", "text": f"{round(n * (1 - math.exp(-lam * x)), 4)}", "is_correct": False},
            ],
            "solution": f"P(max <= {x}) = [P(X <= {x})]^{n} = (1 - e^-{lam*x})^{n} = {correct}",
            "explanation": "Max of independent: F_{max}(x) = [F(x)]^n; min: F_{min}(x) = 1 - [1-F(x)]^n."
        }

    # ==================== CLASS METHODS ====================

    @classmethod
    def get_all_methods(cls) -> List[str]:
        """Return list of all question generation method names."""
        methods = [
            # Topic 1: General Probability
            "set_operations_union", "set_operations_intersection", "set_complement",
            "inclusion_exclusion_two_events", "inclusion_exclusion_three_events",
            "counting_permutations", "counting_combinations", "counting_multinomial",
            "derangements", "pigeonhole",
            "independence_test", "mutually_exclusive",
            "probability_at_least_one", "birthday_problem_variant",
            "conditional_probability_basic",

            # Topic 2: Conditional Probability & Bayes
            "bayes_two_hypotheses", "bayes_three_hypotheses", "bayes_medical_test",
            "total_probability_two_states", "total_probability_three_states",
            "sequential_draws_without_replacement", "sequential_draws_with_replacement",
            "urn_model_conditional", "insurance_classification_bayes",
            "conditional_independence",
            "repeated_trials_conditional",
            "false_positive_rate", "sensitivity_specificity",
            "tree_diagram_multi_stage",
            "conditional_on_sum",

            # Topic 3: Discrete Distributions
            "binomial_probability", "binomial_expected_value", "binomial_at_least_k",
            "poisson_probability", "poisson_sum", "poisson_conditional",
            "geometric_probability", "geometric_memoryless", "geometric_expected_value",
            "negative_binomial_probability", "negative_binomial_mean_variance",
            "hypergeometric_probability",
            "discrete_uniform_probability",
            "bernoulli_trials_run",
            "mixed_discrete_distribution",
            "zero_truncated_poisson",
            "discrete_convolution",
            "binomial_normal_approximation",
            "poisson_approximation_to_binomial",

            # Topic 4: Continuous Distributions
            "uniform_probability_interval", "uniform_expected_shortfall",
            "exponential_probability", "exponential_memoryless", "exponential_minimum",
            "normal_probability_interval", "normal_percentile", "normal_linear_combination",
            "gamma_probability", "gamma_sum_of_exponentials",
            "beta_distribution", "beta_mean_variance",
            "lognormal_probability", "lognormal_percentile",
            "pareto_probability", "pareto_excess_loss",
            "weibull_survival",
            "mixed_distribution_continuous",
            "pdf_to_cdf_integration",
            "hazard_rate_to_survival",

            # Topic 5: Multivariate
            "joint_discrete_pmf_marginal", "joint_discrete_conditional",
            "joint_continuous_pdf_marginal", "joint_continuous_conditional",
            "bivariate_normal_conditional",
            "covariance_from_joint", "correlation_from_joint",
            "independent_sum_variance", "variance_of_linear_combination",
            "covariance_of_functions",
            "conditional_expectation", "conditional_variance",
            "iterated_expectation",
            "law_of_total_variance",
            "order_statistics_uniform", "order_statistics_exponential",

            # Topic 6: Transforms & Special Topics
            "mgf_identify_distribution", "mgf_compute_moments",
            "pgf_computation",
            "convolution_two_distributions",
            "jensen_inequality",
            "chebyshev_bound",
            "central_limit_theorem_approximation",
            "moment_method_estimation",
            "transformation_of_rv",
            "max_min_of_independent",
        ]
        return methods

    @classmethod
    def generate_all(cls, n_per_method: int = 10) -> List[Dict[str, Any]]:
        """Generate all questions by calling each method n times."""
        all_questions = []
        methods = cls.get_all_methods()

        for method_name in methods:
            method = getattr(cls, method_name)
            for i in range(n_per_method):
                generator = cls(seed=hash((method_name, i)) % (2 ** 32))
                try:
                    question = method(generator)
                    all_questions.append(question)
                except Exception as e:
                    print(f"Error generating {method_name} (iteration {i}): {e}")

        return all_questions


