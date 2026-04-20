"""
Answer Evaluator — grades a single question response and updates mastery.

Responsibilities:
    1. Look up the question and its correct answer.
    2. Record UserPerformance.
    3. Run BKT update for the relevant topic.
    4. Update AdaptiveState.
    5. Return feedback (correct/incorrect, explanation, new mastery).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.question import Question, QuestionTemplate
from app.models.exam import Topic
from app.models.performance import UserPerformance, AdaptiveState
from app.services.adaptive_engine import BKTEngine


class AnswerEvaluator:
    """Evaluates a submitted answer and updates mastery state."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.bkt = BKTEngine()

    async def evaluate_answer(
        self,
        user_id: int,
        question_id: int,
        session_id: int,
        selected_choice: int,
        time_spent_seconds: int = 0,
    ) -> dict[str, Any]:
        """
        Grade one answer and update topic mastery.

        Returns:
            dict with keys:
                is_correct      : bool
                correct_answer  : int    (0-based index)
                explanation     : str    (LaTeX-compatible)
                new_mastery     : float  (updated P(known) for the topic)
                topic_id        : int
                topic_name      : str
        """
        # 1. Load the question
        q_result = await self.db.execute(
            select(Question).where(Question.id == question_id)
        )
        question = q_result.scalar_one_or_none()
        if question is None:
            raise ValueError(f"Question {question_id} not found")

        # Get correct index
        correct_idx = question.correct_index if hasattr(question, "correct_index") else self._find_correct(question)
        is_correct = selected_choice == correct_idx

        # 2. Record performance
        perf = UserPerformance(
            user_id=user_id,
            question_id=question_id,
            session_id=session_id,
            is_correct=is_correct,
            time_spent_seconds=time_spent_seconds,
            answered_at=datetime.now(timezone.utc),
        )
        if hasattr(perf, "selected_choice"):
            perf.selected_choice = selected_choice
        self.db.add(perf)

        # 3. Load template → topic for BKT
        tmpl_result = await self.db.execute(
            select(QuestionTemplate).where(QuestionTemplate.id == question.template_id)
        )
        template = tmpl_result.scalar_one_or_none()

        topic_id_str = "unknown"
        topic_name = "Unknown"
        if template:
            topic_result = await self.db.execute(
                select(Topic).where(Topic.id == template.topic_id)
            )
            topic = topic_result.scalar_one_or_none()
            if topic:
                topic_id_str = str(topic.id)
                topic_name = topic.name

        # 4. BKT mastery update
        # Load or create AdaptiveState
        exam_id = None
        if template:
            topic_res = await self.db.execute(
                select(Topic).where(Topic.id == template.topic_id)
            )
            t = topic_res.scalar_one_or_none()
            if t:
                exam_id = t.exam_id

        new_mastery = 0.0
        if exam_id is not None:
            state = await self._get_or_create_state(user_id, exam_id)
            mastery_dict = dict(state.topic_mastery) if state.topic_mastery else {}

            mastery_dict = self.bkt.update_topic_mastery_dict(
                mastery_dict, topic_id_str, is_correct
            )
            state.topic_mastery = mastery_dict
            new_mastery = mastery_dict.get(topic_id_str, 0.0)

        await self.db.flush()

        # 5. Build explanation text
        explanation = ""
        if question.rendered_explanation:
            explanation = question.rendered_explanation
        elif question.rendered_solution:
            explanation = question.rendered_solution

        return {
            "is_correct": is_correct,
            "correct_answer": correct_idx,
            "explanation": explanation,
            "new_mastery": new_mastery,
            "topic_id": topic_id_str,
            "topic_name": topic_name,
        }

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------

    def _find_correct(self, question: Question) -> int:
        """Derive correct index from choices JSONB if correct_index column is absent."""
        choices = question.choices or []
        for i, ch in enumerate(choices):
            if isinstance(ch, dict) and ch.get("is_correct"):
                return i
        return 0  # fallback

    async def _get_or_create_state(self, user_id: int, exam_id: int) -> AdaptiveState:
        """Fetch or create AdaptiveState for (user, exam)."""
        result = await self.db.execute(
            select(AdaptiveState).where(
                AdaptiveState.user_id == user_id,
                AdaptiveState.exam_id == exam_id,
            )
        )
        state = result.scalar_one_or_none()
        if state is None:
            state = AdaptiveState(
                user_id=user_id,
                exam_id=exam_id,
                topic_mastery={},
                overall_ability=0.0,
                readiness_score=0.0,
            )
            self.db.add(state)
            await self.db.flush()
        return state
