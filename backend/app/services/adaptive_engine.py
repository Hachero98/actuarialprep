"""
Adaptive Learning Engine — IRT 3PL + Earned Level (Elo-hybrid) + BKT

This is the mathematical heart of the platform.  Three subsystems cooperate:

1.  **IRT 3PL**  — Item Response Theory (3-Parameter Logistic) gives the
    probability a student of ability θ answers an item correctly.
2.  **EAP estimation** — Expected A Posteriori integrates over a θ grid
    to estimate latent ability from response history.
3.  **Earned Level (EL)** — An Elo-inspired rating (0–10) that rises or
    falls after each quiz.  Beating a quiz above your EL yields a bigger
    gain; failing one below your EL yields a bigger loss.
4.  **BKT (Bayesian Knowledge Tracing)** — Per-topic mastery tracking with
    learning-transition updates after every response.

All numerical work uses only numpy (no scipy dependency).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

import numpy as np


# ---------------------------------------------------------------------------
# Data classes for clean function signatures
# ---------------------------------------------------------------------------

@dataclass
class IRTParams:
    """IRT 3PL item parameters."""
    a: float = 1.0    # discrimination  (0, 3]
    b: float = 0.0    # difficulty       θ-scale
    c: float = 0.2    # guessing         [0, 0.5]


@dataclass
class ResponseRecord:
    """One student response to one item."""
    is_correct: bool
    irt: IRTParams = field(default_factory=IRTParams)
    topic_id: Optional[str] = None
    time_spent_seconds: int = 0


@dataclass
class QuizResult:
    """Summary of an entire quiz attempt."""
    quiz_level: float          # difficulty level of the quiz (1–10)
    total_questions: int
    correct_answers: int
    responses: list[ResponseRecord] = field(default_factory=list)

    @property
    def score(self) -> float:
        """Percentage score 0–100."""
        if self.total_questions == 0:
            return 0.0
        return 100.0 * self.correct_answers / self.total_questions

    @property
    def passed(self) -> bool:
        """Pass threshold: 70 %."""
        return self.score >= 70.0


# ═══════════════════════════════════════════════════════════════════════════
# IRT 3PL CORE
# ═══════════════════════════════════════════════════════════════════════════

class IRT3PL:
    """
    Item Response Theory — 3-Parameter Logistic model.

    P(θ) = c + (1 − c) / (1 + exp(−a(θ − b)))

    where:
        θ = student ability
        a = discrimination (steepness of the curve)
        b = difficulty (θ value at inflection)
        c = pseudo-guessing (lower asymptote)
    """

    @staticmethod
    def probability(theta: float, a: float, b: float, c: float) -> float:
        """P(correct | θ, a, b, c) — clipped to avoid overflow."""
        z = np.clip(a * (theta - b), -100.0, 100.0)
        return float(c + (1.0 - c) / (1.0 + np.exp(-z)))

    @staticmethod
    def fisher_information(theta: float, a: float, b: float, c: float) -> float:
        """
        Fisher information I(θ) for a 3PL item.

        I(θ) = a² · (P − c)² · (1 − P) / [P · (1 − c)²]

        Higher information ⇒ the item is more discriminating at θ.
        """
        p = IRT3PL.probability(theta, a, b, c)
        if p <= c + 1e-12 or p >= 1.0 - 1e-12:
            return 0.0
        num = (a ** 2) * ((p - c) ** 2) * (1.0 - p)
        den = p * ((1.0 - c) ** 2)
        return float(max(0.0, num / den))

    @staticmethod
    def log_likelihood(theta: float, responses: list[ResponseRecord]) -> float:
        """Log-likelihood of the response vector at ability θ."""
        ll = 0.0
        for r in responses:
            p = IRT3PL.probability(theta, r.irt.a, r.irt.b, r.irt.c)
            p = np.clip(p, 1e-15, 1.0 - 1e-15)
            ll += math.log(p) if r.is_correct else math.log(1.0 - p)
        return ll


# ═══════════════════════════════════════════════════════════════════════════
# ABILITY ESTIMATION — Expected A Posteriori (EAP)
# ═══════════════════════════════════════════════════════════════════════════

class AbilityEstimator:
    """
    EAP ability estimation on a discrete θ grid.

    Prior: N(0, 1) — standard normal.
    Posterior ∝ prior × ∏ᵢ L(θ | responseᵢ)
    EAP = E[θ | data] = Σ θⱼ · P(θⱼ | data)
    """

    def __init__(self, grid_points: int = 61, theta_min: float = -4.0, theta_max: float = 4.0):
        self.theta_grid = np.linspace(theta_min, theta_max, grid_points)
        # Standard normal prior
        self.prior = np.exp(-0.5 * self.theta_grid ** 2) / np.sqrt(2.0 * np.pi)
        self.prior /= self.prior.sum()

    def estimate(self, responses: list[ResponseRecord]) -> float:
        """
        Return EAP estimate of θ given response history.

        With zero responses, returns prior mean (0.0).
        """
        if not responses:
            return 0.0

        log_posterior = np.log(self.prior + 1e-300)

        for r in responses:
            probs = np.array([
                IRT3PL.probability(th, r.irt.a, r.irt.b, r.irt.c)
                for th in self.theta_grid
            ])
            if r.is_correct:
                log_posterior += np.log(np.clip(probs, 1e-300, None))
            else:
                log_posterior += np.log(np.clip(1.0 - probs, 1e-300, None))

        # Stabilise before exp
        log_posterior -= log_posterior.max()
        posterior = np.exp(log_posterior)
        posterior /= posterior.sum()

        eap = float(np.dot(self.theta_grid, posterior))
        return eap

    def posterior_sd(self, responses: list[ResponseRecord]) -> float:
        """Standard deviation of the posterior — measures estimation uncertainty."""
        if not responses:
            return 1.0  # prior SD

        log_posterior = np.log(self.prior + 1e-300)
        for r in responses:
            probs = np.array([
                IRT3PL.probability(th, r.irt.a, r.irt.b, r.irt.c)
                for th in self.theta_grid
            ])
            if r.is_correct:
                log_posterior += np.log(np.clip(probs, 1e-300, None))
            else:
                log_posterior += np.log(np.clip(1.0 - probs, 1e-300, None))

        log_posterior -= log_posterior.max()
        posterior = np.exp(log_posterior)
        posterior /= posterior.sum()

        mean = float(np.dot(self.theta_grid, posterior))
        var = float(np.dot((self.theta_grid - mean) ** 2, posterior))
        return math.sqrt(max(var, 0.0))


# ═══════════════════════════════════════════════════════════════════════════
# EARNED LEVEL (EL) — Elo-inspired rating system
# ═══════════════════════════════════════════════════════════════════════════

class EarnedLevelEngine:
    """
    Earned Level system inspired by Elo / ADAPT.

    The core idea: if a student at EL 3.5 passes a Level 5.0 quiz,
    they should gain more than if they passed a Level 2.0 quiz.
    Conversely, failing a quiz below your EL costs more.

    Update formula (after a quiz):
        ΔEL = K × (S − E)
    where:
        S  = actual outcome (1 if passed, 0 if failed)
        E  = expected probability of passing (logistic of EL − quiz_level)
        K  = gain factor, tuned by quiz length and difficulty gap

    The expected probability uses the same logistic function as chess Elo:
        E = 1 / (1 + 10^((quiz_level − EL) / D))
    with D controlling sensitivity to the level gap.
    """

    # Tuning constants
    BASE_K: float = 1.6          # base gain per quiz
    K_SCALE_FACTOR: float = 0.04 # per-question contribution to K
    D: float = 2.5               # Elo spread parameter
    MIN_EL: float = 0.0
    MAX_EL: float = 10.0
    PASS_THRESHOLD: float = 0.70 # 70 % to pass

    @classmethod
    def expected_pass_probability(cls, earned_level: float, quiz_level: float) -> float:
        """
        Logistic expected probability that a student at `earned_level`
        passes a quiz at `quiz_level`.

        E = 1 / (1 + 10^((quiz_level − earned_level) / D))

        Examples:
            EL=5, quiz=5 → E≈0.50
            EL=5, quiz=3 → E≈0.86
            EL=5, quiz=7 → E≈0.14
        """
        exponent = (quiz_level - earned_level) / cls.D
        return 1.0 / (1.0 + 10.0 ** exponent)

    @classmethod
    def compute_k_factor(cls, num_questions: int, quiz_level: float, earned_level: float) -> float:
        """
        Dynamic K factor.

        Longer quizzes and larger difficulty gaps produce bigger K values,
        reflecting more information.  Capped to prevent wild swings.

        K = BASE_K + K_SCALE_FACTOR × num_questions + 0.15 × |gap|
        """
        gap = abs(quiz_level - earned_level)
        k = cls.BASE_K + cls.K_SCALE_FACTOR * num_questions + 0.15 * gap
        return min(k, 4.0)  # cap at 4.0

    @classmethod
    def update_earned_level(
        cls,
        current_el: float,
        quiz_result: QuizResult,
    ) -> dict:
        """
        Compute the new Earned Level after a quiz.

        Returns a dict with:
            new_el       : float  — updated Earned Level
            delta        : float  — change in EL
            expected     : float  — expected pass probability
            passed       : bool   — whether the quiz was passed
            score        : float  — quiz score (0–100)

        Mathematical walkthrough:
        ─────────────────────────
        Suppose current EL = 3.5, quiz at level 5.0, 10 questions, 8 correct.

        1. Score = 80 % → passed = True → S = 1
        2. E = 1 / (1 + 10^((5.0 − 3.5) / 2.5)) = 1 / (1 + 10^0.6) ≈ 0.201
           (student was unlikely to pass → big information gain)
        3. K = 1.6 + 0.04×10 + 0.15×1.5 = 2.225
        4. ΔEL = 2.225 × (1 − 0.201) = 1.778
        5. New EL = 3.5 + 1.778 = 5.278 → clamp to [0, 10]

        If the student had failed (say 5/10 = 50%):
        4. ΔEL = 2.225 × (0 − 0.201) = −0.447
        5. New EL = 3.5 − 0.447 = 3.053
        """
        passed = quiz_result.passed
        S = 1.0 if passed else 0.0

        E = cls.expected_pass_probability(current_el, quiz_result.quiz_level)
        K = cls.compute_k_factor(
            quiz_result.total_questions, quiz_result.quiz_level, current_el
        )

        delta = K * (S - E)
        new_el = np.clip(current_el + delta, cls.MIN_EL, cls.MAX_EL)

        return {
            "new_el": float(new_el),
            "delta": float(delta),
            "expected": float(E),
            "passed": passed,
            "score": quiz_result.score,
        }

    @classmethod
    def suggest_next_quiz_level(cls, earned_level: float) -> float:
        """
        Suggest the difficulty level for the student's next quiz.

        The quiz should sit slightly above their current EL so they are
        challenged but not overwhelmed (~40 % expected pass rate).

        next_level ≈ EL + 0.5
        """
        suggested = earned_level + 0.5
        return float(np.clip(suggested, 1.0, 10.0))


# ═══════════════════════════════════════════════════════════════════════════
# BAYESIAN KNOWLEDGE TRACING (BKT) — per-topic mastery
# ═══════════════════════════════════════════════════════════════════════════

class BKTEngine:
    """
    Bayesian Knowledge Tracing for topic-level mastery.

    Latent state: K ∈ {known, not-known}
    Observation:  correct / incorrect

    Parameters (per topic, or global defaults):
        p_guess   = P(correct | not-known)   — default 0.25 (5-choice MCQ)
        p_slip    = P(incorrect | known)     — default 0.10
        p_transit = P(known_t | not-known_{t-1}) — learning rate, default 0.10

    Update rule:
        After observing response:
        1. posterior = P(K | observation)  via Bayes
        2. Apply learning transition:
           P(K_new) = P(K|obs) + (1 − P(K|obs)) × p_transit
    """

    DEFAULT_P_GUESS: float = 0.25
    DEFAULT_P_SLIP: float = 0.10
    DEFAULT_P_TRANSIT: float = 0.10

    @classmethod
    def update_mastery(
        cls,
        p_know: float,
        is_correct: bool,
        p_guess: float = DEFAULT_P_GUESS,
        p_slip: float = DEFAULT_P_SLIP,
        p_transit: float = DEFAULT_P_TRANSIT,
    ) -> float:
        """
        Update mastery probability for a single topic after one response.

        Args:
            p_know:     Current P(known) for this topic, in [0, 1].
            is_correct: Whether the student answered correctly.
            p_guess:    P(correct | not known).
            p_slip:     P(incorrect | known).
            p_transit:  P(learn in one step).

        Returns:
            Updated P(known) after observation and learning transition.

        Mathematical walkthrough:
        ─────────────────────────
        Suppose p_know = 0.30, student answers correctly:

        1. L_know  = P(correct | known)     = 1 − p_slip = 0.90
           L_not   = P(correct | not known) = p_guess    = 0.25

        2. Bayes numerator   = L_know × p_know = 0.90 × 0.30 = 0.270
           Bayes denominator = 0.270 + 0.25 × 0.70            = 0.445

        3. P(known | correct) = 0.270 / 0.445 ≈ 0.607

        4. Learning transition:
           P(known_new) = 0.607 + (1 − 0.607) × 0.10 = 0.646
        """
        if is_correct:
            l_know = 1.0 - p_slip
            l_not = p_guess
        else:
            l_know = p_slip
            l_not = 1.0 - p_guess

        numerator = l_know * p_know
        denominator = numerator + l_not * (1.0 - p_know)

        if denominator < 1e-15:
            p_posterior = p_know
        else:
            p_posterior = numerator / denominator

        # Learning transition
        p_new = p_posterior + (1.0 - p_posterior) * p_transit
        return float(np.clip(p_new, 0.0, 1.0))

    @classmethod
    def update_topic_mastery_dict(
        cls,
        mastery: dict[str, float],
        topic_id: str,
        is_correct: bool,
        **bkt_params,
    ) -> dict[str, float]:
        """Update mastery dict in place for one topic, return the whole dict."""
        current = mastery.get(topic_id, 0.0)
        mastery[topic_id] = cls.update_mastery(current, is_correct, **bkt_params)
        return mastery


# ═══════════════════════════════════════════════════════════════════════════
# QUESTION SELECTION — 70/15/15 rule
# ═══════════════════════════════════════════════════════════════════════════

class QuestionSelector:
    """
    Selects the next question set for a student.

    Distribution logic for a quiz of N questions:
        70 %  at the student's current Earned Level   (±0.5 difficulty band)
        15 %  slightly above  (EL+0.5 to EL+2.0)      — stretch questions
        15 %  targeting weakest topics (low mastery)   — remediation

    Within each bucket, items are ranked by Fisher information at the
    student's current θ to maximise measurement precision.
    """

    @staticmethod
    def categorise_questions(
        questions: list[dict],
        earned_level: float,
        topic_mastery: dict[str, float],
        ability_theta: float,
    ) -> dict[str, list[dict]]:
        """
        Split available questions into three buckets.

        Each question dict must have:
            difficulty  : float (1–10)
            topic_id    : str
            a, b, c     : IRT params
        """
        at_level = []
        above_level = []
        weakness = []

        # Find the 3 weakest topics
        if topic_mastery:
            sorted_topics = sorted(topic_mastery.items(), key=lambda x: x[1])
            weak_topic_ids = {t[0] for t in sorted_topics[:3]}
        else:
            weak_topic_ids = set()

        el_low = earned_level - 0.5
        el_high = earned_level + 0.5
        stretch_high = earned_level + 2.0

        for q in questions:
            diff = q.get("difficulty", 5.0)
            tid = str(q.get("topic_id", ""))

            if el_low <= diff <= el_high:
                at_level.append(q)
            elif el_high < diff <= stretch_high:
                above_level.append(q)

            if tid in weak_topic_ids:
                weakness.append(q)

        # Rank each bucket by Fisher information descending
        def sort_key(item):
            return -IRT3PL.fisher_information(
                ability_theta,
                item.get("a", 1.0),
                item.get("b", 0.0),
                item.get("c", 0.2),
            )

        at_level.sort(key=sort_key)
        above_level.sort(key=sort_key)
        weakness.sort(key=sort_key)

        return {
            "at_level": at_level,
            "above_level": above_level,
            "weakness": weakness,
        }

    @staticmethod
    def select_quiz_set(
        questions: list[dict],
        earned_level: float,
        topic_mastery: dict[str, float],
        ability_theta: float,
        num_questions: int = 10,
    ) -> list[dict]:
        """
        Select a quiz of `num_questions` items using the 70/15/15 rule.

        Returns the selected question dicts.  If a bucket is short,
        overflow goes to the at_level bucket, then above, then weakness.
        """
        buckets = QuestionSelector.categorise_questions(
            questions, earned_level, topic_mastery, ability_theta
        )

        n_at = round(num_questions * 0.70)
        n_above = round(num_questions * 0.15)
        n_weak = num_questions - n_at - n_above  # remainder

        selected_ids: set[int] = set()
        result: list[dict] = []

        def pick(pool: list[dict], n: int) -> list[dict]:
            picked = []
            for q in pool:
                if len(picked) >= n:
                    break
                qid = q.get("id")
                if qid not in selected_ids:
                    selected_ids.add(qid)
                    picked.append(q)
            return picked

        at = pick(buckets["at_level"], n_at)
        above = pick(buckets["above_level"], n_above)
        weak = pick(buckets["weakness"], n_weak)

        result.extend(at)
        result.extend(above)
        result.extend(weak)

        # Fill shortfall from any remaining questions
        if len(result) < num_questions:
            remainder = num_questions - len(result)
            all_remaining = [
                q for q in questions if q.get("id") not in selected_ids
            ]
            # Sort by information
            all_remaining.sort(
                key=lambda q: -IRT3PL.fisher_information(
                    ability_theta,
                    q.get("a", 1.0),
                    q.get("b", 0.0),
                    q.get("c", 0.2),
                )
            )
            result.extend(all_remaining[:remainder])

        # Shuffle so the student doesn't see at-level then above then weak in order
        rng = np.random.default_rng()
        rng.shuffle(result)

        return result


# ═══════════════════════════════════════════════════════════════════════════
# READINESS SCORE — weighted topic mastery composite
# ═══════════════════════════════════════════════════════════════════════════

def calculate_readiness_score(
    topic_mastery: dict[str, float],
    topic_weights: dict[str, float],
) -> float:
    """
    Compute exam readiness score (0–100).

    readiness = 100 × Σ (masteryᵢ × wᵢ) / Σ wᵢ

    where wᵢ is the syllabus weight for topic i.
    """
    if not topic_weights:
        if not topic_mastery:
            return 0.0
        return float(100.0 * np.mean(list(topic_mastery.values())))

    total_w = sum(topic_weights.values())
    if total_w < 1e-15:
        return 0.0

    score = sum(
        topic_mastery.get(tid, 0.0) * w
        for tid, w in topic_weights.items()
    )
    return float(np.clip(100.0 * score / total_w, 0.0, 100.0))


# ═══════════════════════════════════════════════════════════════════════════
# CONVENIENCE FAÇADE  (used by API routes)
# ═══════════════════════════════════════════════════════════════════════════

class AdaptiveEngine:
    """
    High-level façade that orchestrates IRT + EL + BKT + selection.

    Typically instantiated once per request with a DB session.
    """

    def __init__(self, db_session=None):
        self.db = db_session
        self.irt = IRT3PL()
        self.estimator = AbilityEstimator()
        self.el_engine = EarnedLevelEngine()
        self.bkt = BKTEngine()
        self.selector = QuestionSelector()

    # --- Ability estimation -------------------------------------------

    def estimate_ability(self, responses: list[ResponseRecord]) -> float:
        """EAP ability estimate from response history."""
        return self.estimator.estimate(responses)

    # --- Earned Level -------------------------------------------------

    def update_earned_level(
        self, current_el: float, quiz_result: QuizResult
    ) -> dict:
        """Update EL after a quiz.  Returns dict with new_el, delta, etc."""
        return self.el_engine.update_earned_level(current_el, quiz_result)

    def suggest_quiz_level(self, earned_level: float) -> float:
        """Suggest the next quiz's difficulty level."""
        return self.el_engine.suggest_next_quiz_level(earned_level)

    # --- Topic mastery (BKT) ------------------------------------------

    def update_topic_mastery(
        self,
        mastery: dict[str, float],
        topic_id: str,
        is_correct: bool,
    ) -> dict[str, float]:
        """BKT update for one topic."""
        return self.bkt.update_topic_mastery_dict(mastery, topic_id, is_correct)

    # --- Question selection -------------------------------------------

    def select_next_set(
        self,
        questions: list[dict],
        earned_level: float,
        topic_mastery: dict[str, float],
        ability_theta: float,
        num_questions: int = 10,
    ) -> list[dict]:
        """70/15/15 question selection."""
        return self.selector.select_quiz_set(
            questions, earned_level, topic_mastery, ability_theta, num_questions
        )

    # --- Readiness score ----------------------------------------------

    def readiness_score(
        self,
        topic_mastery: dict[str, float],
        topic_weights: dict[str, float],
    ) -> float:
        """Weighted readiness score 0–100."""
        return calculate_readiness_score(topic_mastery, topic_weights)
