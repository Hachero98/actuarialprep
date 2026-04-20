"""
Session Manager — handles practice session lifecycle.

Responsibilities
────────────────
1. Create a new PracticeSession row.
2. Look up (or create) the student's UserEarnedLevel for the exam.
3. Decide the quiz difficulty level based on current EL.
4. On session end: update EL, persist score, and return results.
5. Pause: snapshot the current question index + all pending randomised
   variable sets so the user returns to the exact same numbers.
6. Resume: reload that snapshot and continue from the saved position.

Pause/Resume contract
─────────────────────
When paused, the session row carries:
  • status          = "paused"
  • paused_at       = now()
  • paused_state    = {
        "question_index": int,         -- 0-based index into the session's question list
        "question_ids": [int, ...],    -- ordered list of question IDs for the session
        "variables_by_question": {     -- keyed by str(question_id)
            "42": {"n": 10, "i": 0.06, "P": 500.0},
            ...
        }
    }

The frontend sends the same variable dict back when submitting a resumed
question so the student sees identical numbers.
"""

from __future__ import annotations

import secrets
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exam import Exam
from app.models.performance import PracticeSession, SessionType, AdaptiveState
from app.models.earned_level import UserEarnedLevel
from app.services.adaptive_engine import (
    AdaptiveEngine,
    QuizResult,
    ResponseRecord,
    IRTParams,
)
from app.schemas.session_state import SessionVariableSnapshot, WorkInProgressState

_UTC = timezone.utc


class SessionManager:
    """Manages the full lifecycle of a practice session."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.engine = AdaptiveEngine()

    # ------------------------------------------------------------------
    # START
    # ------------------------------------------------------------------

    async def start_session(
        self,
        user_id: int,
        exam_code: str,
        session_type: str = "adaptive",
        topic_id: Optional[int] = None,
        num_questions: int = 10,
    ) -> dict[str, Any]:
        """
        Start a new practice session.

        Returns session metadata including session_id and quiz_level.
        """
        exam = await self._get_exam(exam_code)
        uel = await self._get_or_create_el(user_id, exam.id)
        quiz_level = self.engine.suggest_quiz_level(uel.earned_level)

        stype = SessionType(session_type)
        session = PracticeSession(
            user_id=user_id,
            exam_id=exam.id,
            session_type=stype,
            total_questions=num_questions,
            correct_answers=0,
            score=None,
            status="active",
        )
        if hasattr(session, "quiz_level"):
            session.quiz_level = quiz_level
        if hasattr(session, "el_before"):
            session.el_before = uel.earned_level

        self.db.add(session)
        await self.db.flush()

        return {
            "session_id": session.id,
            "exam_code": exam_code,
            "exam_name": exam.name,
            "quiz_level": quiz_level,
            "earned_level": uel.earned_level,
            "num_questions": num_questions,
            "session_type": session_type,
            "status": "active",
        }

    # ------------------------------------------------------------------
    # PAUSE
    # ------------------------------------------------------------------

    async def pause_session(
        self,
        session_id: int,
        user_id: int,
        question_index: int,
        question_ids: list[int],
        variables_by_question: dict[str, dict[str, Any]],
        exam_code: str = "P",
        template_ids: Optional[dict[str, str]] = None,
        seed_values: Optional[dict[str, int]] = None,
    ) -> dict[str, Any]:
        """
        Pause an active session and persist a typed SessionVariableSnapshot.

        Parameters
        ──────────
        question_index        : 0-based index the student was on when pausing
        question_ids          : full ordered list of question IDs for the session
        variables_by_question : {str(question_id): {var_name: value, ...}}
        template_ids          : optional {str(question_id): template_id} mapping
        seed_values           : optional {str(question_id): int_seed} mapping

        Returns the paused session summary.
        """
        session = await self._load_session(session_id, user_id)

        if session.status == "completed":
            raise ValueError("Cannot pause a completed session.")

        # Build a typed snapshot using WorkInProgressState for each question
        snapshot = SessionVariableSnapshot(
            session_id=session_id,
            exam_code=exam_code,
            question_index=question_index,
            question_ids=question_ids,
        )
        for q_id in question_ids:
            key = str(q_id)
            active_map = variables_by_question.get(key, {})
            wip = WorkInProgressState(
                session_id=session_id,
                question_id=q_id,
                template_id=(template_ids or {}).get(key, "unknown"),
                question_index=question_ids.index(q_id),
                seed_value=(seed_values or {}).get(key, 0),
                active_variable_map=active_map,
                exam_code=exam_code,
            )
            snapshot.set_state(q_id, wip)

        session.status = "paused"
        session.paused_at = datetime.now(_UTC)
        session.paused_state = snapshot.to_json_column()

        await self.db.commit()

        return {
            "session_id": session_id,
            "status": "paused",
            "paused_at": session.paused_at.isoformat(),
            "question_index": question_index,
            "questions_remaining": len(question_ids) - question_index,
        }

    # ------------------------------------------------------------------
    # RESUME
    # ------------------------------------------------------------------

    async def resume_session(
        self,
        session_id: int,
        user_id: int,
    ) -> dict[str, Any]:
        """
        Resume a paused session.

        Returns the saved state so the frontend can render the exact same
        question — with the exact same randomised numbers — that the student
        left off on.
        """
        session = await self._load_session(session_id, user_id)

        if session.status != "paused":
            raise ValueError(f"Session {session_id} is not paused (status={session.status}).")

        saved: dict[str, Any] = session.paused_state or {}

        # Reactivate
        session.status = "active"
        session.paused_at = None
        session.paused_state = None
        await self.db.commit()

        # Deserialize typed snapshot
        snapshot = SessionVariableSnapshot.from_json_column(saved) if saved else None

        question_index = snapshot.question_index if snapshot else 0
        question_ids = snapshot.question_ids if snapshot else []
        current_wip: Optional[WorkInProgressState] = (
            snapshot.current_state if snapshot else None
        )
        current_variables: dict[str, Any] = (
            current_wip.active_variable_map if current_wip else {}
        )
        current_question_id: Optional[int] = (
            snapshot.current_question_id if snapshot else None
        )

        # Full variables_by_question for frontend (flat dict of dicts)
        variables_by_question: dict[str, Any] = {}
        if snapshot:
            for qid_str, wip_state in snapshot.states.items():
                variables_by_question[qid_str] = wip_state.active_variable_map

        exam_result = await self.db.execute(
            select(Exam).where(Exam.id == session.exam_id)
        )
        exam = exam_result.scalar_one()
        uel = await self._get_or_create_el(user_id, exam.id)

        return {
            "session_id": session_id,
            "exam_code": exam.code,
            "status": "active",
            "question_index": question_index,
            "question_ids": question_ids,
            "questions_remaining": len(question_ids) - question_index,
            "current_question_id": current_question_id,
            "current_variables": current_variables,
            "current_seed_value": current_wip.seed_value if current_wip else None,
            "variables_by_question": variables_by_question,
            "earned_level": uel.earned_level,
            "quiz_level": session.quiz_level,
        }

    # ------------------------------------------------------------------
    # END
    # ------------------------------------------------------------------

    async def end_session(
        self,
        session_id: int,
        user_id: int,
    ) -> dict[str, Any]:
        """
        End a practice session, compute EL update, and persist results.
        """
        from app.models.performance import UserPerformance

        session = await self._load_session(session_id, user_id)

        perf_result = await self.db.execute(
            select(UserPerformance).where(UserPerformance.session_id == session_id)
        )
        records = perf_result.scalars().all()

        total = len(records)
        correct = sum(1 for r in records if r.is_correct)

        session.total_questions = total
        session.correct_answers = correct
        session.score = (100.0 * correct / total) if total > 0 else 0.0
        session.ended_at = datetime.now(_UTC)
        session.status = "completed"
        session.paused_at = None
        session.paused_state = None

        quiz_level = getattr(session, "quiz_level", None) or 5.0
        quiz_result = QuizResult(
            quiz_level=quiz_level,
            total_questions=total,
            correct_answers=correct,
        )

        exam_result = await self.db.execute(
            select(Exam).where(Exam.id == session.exam_id)
        )
        exam = exam_result.scalar_one()

        uel = await self._get_or_create_el(user_id, exam.id)
        el_update = self.engine.update_earned_level(uel.earned_level, quiz_result)

        uel.earned_level = el_update["new_el"]
        uel.peak_level = max(uel.peak_level, el_update["new_el"])
        uel.total_quizzes += 1
        uel.total_correct += correct
        uel.total_attempted += total
        uel.streak = (uel.streak + 1) if el_update["passed"] else 0
        uel.last_quiz_at = datetime.now(_UTC)

        if hasattr(session, "el_after"):
            session.el_after = el_update["new_el"]

        await self.db.commit()

        return {
            "session_id": session.id,
            "exam_code": exam.code,
            "total_questions": total,
            "correct_answers": correct,
            "score": session.score,
            "passed": el_update["passed"],
            "earned_level": {
                "before": el_update["new_el"] - el_update["delta"],
                "after": el_update["new_el"],
                "delta": el_update["delta"],
                "peak": uel.peak_level,
            },
            "streak": uel.streak,
        }

    # ------------------------------------------------------------------
    # RECORD ANSWER  (persist seed + variable values for pause/resume)
    # ------------------------------------------------------------------

    async def record_answer(
        self,
        session_id: int,
        user_id: int,
        question_id: int,
        selected_choice: int,
        is_correct: bool,
        time_spent_seconds: int,
        random_seed: Optional[str],
        variable_values: Optional[dict[str, Any]],
        template_id: Optional[int] = None,
    ) -> dict[str, Any]:
        """
        Persist a single question attempt, recording the exact random_seed and
        variable_values so the question text is reproducible if the session is
        paused and later resumed.

        The random_seed is a hex string (e.g. secrets.token_hex(16)) that was
        used to draw the variable values.  On resume, the frontend passes both
        the seed and the pre-resolved variable_values back so the student sees
        the identical numbers.
        """
        from app.models.performance import UserPerformance

        # Verify session ownership
        await self._load_session(session_id, user_id)

        # Round floats to 4 d.p. for clean storage
        safe_vars: Optional[dict[str, Any]] = None
        if variable_values is not None:
            safe_vars = {
                k: round(v, 4) if isinstance(v, float) else v
                for k, v in variable_values.items()
            }

        perf = UserPerformance(
            user_id=user_id,
            question_id=question_id,
            session_id=session_id,
            selected_choice=selected_choice,
            is_correct=is_correct,
            time_spent_seconds=time_spent_seconds,
            random_seed=random_seed,
            variable_values=safe_vars,
            template_id=template_id,
        )
        self.db.add(perf)
        await self.db.flush()

        return {
            "performance_id": perf.id,
            "question_id": question_id,
            "is_correct": is_correct,
            "random_seed": random_seed,
            "variable_values": safe_vars,
        }

    async def get_question_seed(
        self,
        session_id: int,
        user_id: int,
        question_id: int,
    ) -> Optional[dict[str, Any]]:
        """
        Retrieve the stored seed and variable values for a question in this session.
        Returns None if the question has not been answered yet.
        Used on resume to restore exact variable state for unanswered questions.
        """
        from app.models.performance import UserPerformance

        await self._load_session(session_id, user_id)

        result = await self.db.execute(
            select(UserPerformance)
            .where(
                UserPerformance.session_id == session_id,
                UserPerformance.question_id == question_id,
                UserPerformance.user_id == user_id,
            )
            .order_by(UserPerformance.answered_at.desc())
            .limit(1)
        )
        perf = result.scalar_one_or_none()
        if perf is None:
            return None
        return {
            "random_seed": perf.random_seed,
            "variable_values": perf.variable_values,
            "is_correct": perf.is_correct,
            "answered_at": perf.answered_at.isoformat() if perf.answered_at else None,
        }

    # ------------------------------------------------------------------
    # HELPERS
    # ------------------------------------------------------------------

    async def _get_exam(self, exam_code: str) -> Exam:
        result = await self.db.execute(select(Exam).where(Exam.code == exam_code))
        exam = result.scalar_one_or_none()
        if exam is None:
            raise ValueError(f"Unknown exam code: {exam_code}")
        return exam

    async def _load_session(self, session_id: int, user_id: int) -> PracticeSession:
        result = await self.db.execute(
            select(PracticeSession).where(PracticeSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        if session is None:
            raise ValueError(f"Session {session_id} not found")
        if session.user_id != user_id:
            raise PermissionError("Not authorised to access this session")
        return session

    async def _get_or_create_el(self, user_id: int, exam_id: int) -> UserEarnedLevel:
        result = await self.db.execute(
            select(UserEarnedLevel).where(
                UserEarnedLevel.user_id == user_id,
                UserEarnedLevel.exam_id == exam_id,
            )
        )
        uel = result.scalar_one_or_none()
        if uel is None:
            uel = UserEarnedLevel(user_id=user_id, exam_id=exam_id)
            self.db.add(uel)
            await self.db.flush()
        return uel
