"""
GET-NEXT-SET endpoint — the primary question selection API.

POST /api/get-next-set

Pulls questions from the database using the 70/15/15 rule:
    70 % at the student's current Earned Level
    15 % slightly above (stretch)
    15 % targeting weak topics (remediation)

All text fields are returned with LaTeX notation intact so the frontend
can render them with KaTeX or MathJax.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.exam import Exam, Topic
from app.models.question import Question, QuestionTemplate
from app.models.performance import AdaptiveState
from app.models.earned_level import UserEarnedLevel
from app.services.adaptive_engine import AdaptiveEngine


router = APIRouter(tags=["question-set"])


# ---------------------------------------------------------------------------
# REQUEST / RESPONSE SCHEMAS
# ---------------------------------------------------------------------------

class NextSetRequest(BaseModel):
    """Request body for /api/get-next-set."""
    exam_code: str = Field(..., description="Exam code, e.g. 'FM'")
    num_questions: int = Field(10, ge=1, le=50, description="Number of questions (1–50)")
    session_id: Optional[int] = Field(None, description="Active session ID (optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "exam_code": "FM",
                "num_questions": 10,
            }
        }


class ChoiceOut(BaseModel):
    """One answer choice, LaTeX-capable."""
    label: str = Field(..., description="Choice label (A, B, C, D, E)")
    text: str = Field(..., description="Choice text — may contain LaTeX like $\\frac{1}{2}$")


class QuestionOut(BaseModel):
    """
    A single question ready for frontend rendering.

    All text fields may contain LaTeX delimited by $ ... $ (inline)
    or $$ ... $$ (display).  The frontend should pass them through
    KaTeX.renderToString() or MathJax.
    """
    id: int
    text: str = Field(..., description="Question body with LaTeX")
    choices: list[ChoiceOut]
    difficulty: float
    topic_id: int
    topic_name: str
    exam_code: str
    # IRT params (the frontend doesn't need these, but they're useful for debugging)
    irt_a: Optional[float] = None
    irt_b: Optional[float] = None
    irt_c: Optional[float] = None


class NextSetResponse(BaseModel):
    """Response from /api/get-next-set."""
    exam_code: str
    earned_level: float = Field(..., description="Student's current EL for this exam")
    quiz_level: float = Field(..., description="Difficulty level of this question set")
    num_questions: int
    questions: list[QuestionOut]
    topic_mastery: dict[str, float] = Field(
        default_factory=dict,
        description="Current topic mastery for the exam"
    )


# ---------------------------------------------------------------------------
# ENDPOINT
# ---------------------------------------------------------------------------

@router.post(
    "/api/get-next-set",
    response_model=NextSetResponse,
    summary="Get next question set (70/15/15 adaptive selection)",
)
async def get_next_set(
    request: NextSetRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NextSetResponse:
    """
    Select the next set of questions using the adaptive 70/15/15 rule.

    The algorithm:
    1. Fetch the student's Earned Level and topic mastery for the exam.
    2. Load all active questions for the exam.
    3. Run QuestionSelector.select_quiz_set() which distributes:
       - 70% at the student's current EL (±0.5 difficulty band)
       - 15% slightly above EL (stretch questions)
       - 15% targeting weak topics
    4. Within each bucket, rank by Fisher information at the student's θ.
    5. Return questions with LaTeX-formatted text for KaTeX rendering.
    """
    user_id = int(current_user.get("sub"))
    engine = AdaptiveEngine()

    # --- 1. Resolve exam ------------------------------------------------
    exam_result = await db.execute(
        select(Exam).where(Exam.code == request.exam_code)
    )
    exam = exam_result.scalar_one_or_none()
    if exam is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown exam code: {request.exam_code}",
        )

    # --- 2. Student state -----------------------------------------------
    # Earned Level
    el_result = await db.execute(
        select(UserEarnedLevel).where(
            UserEarnedLevel.user_id == user_id,
            UserEarnedLevel.exam_id == exam.id,
        )
    )
    uel = el_result.scalar_one_or_none()
    earned_level = uel.earned_level if uel else 0.0

    # Adaptive state (topic mastery + ability)
    as_result = await db.execute(
        select(AdaptiveState).where(
            AdaptiveState.user_id == user_id,
            AdaptiveState.exam_id == exam.id,
        )
    )
    adaptive_state = as_result.scalar_one_or_none()
    topic_mastery = dict(adaptive_state.topic_mastery) if adaptive_state and adaptive_state.topic_mastery else {}
    ability_theta = adaptive_state.overall_ability if adaptive_state else 0.0

    # --- 3. Load candidate questions ------------------------------------
    # Join questions → templates → topics  to get everything in one query
    stmt = (
        select(
            Question.id,
            Question.rendered_text,
            Question.choices,
            Question.correct_index,
            Question.difficulty,
            Question.irt_discrimination,
            Question.irt_difficulty,
            Question.irt_guessing,
            QuestionTemplate.topic_id,
            Topic.name.label("topic_name"),
        )
        .join(QuestionTemplate, Question.template_id == QuestionTemplate.id)
        .join(Topic, QuestionTemplate.topic_id == Topic.id)
        .where(Topic.exam_id == exam.id)
    )
    rows = (await db.execute(stmt)).all()

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No questions found for exam {request.exam_code}",
        )

    # Build flat dicts for the selector
    candidates = []
    topic_name_map: dict[int, str] = {}
    for row in rows:
        topic_name_map[row.topic_id] = row.topic_name
        candidates.append({
            "id": row.id,
            "text": row.rendered_text,
            "choices": row.choices,
            "correct_index": row.correct_index,
            "difficulty": float(row.difficulty or 5.0),
            "topic_id": str(row.topic_id),
            "topic_name": row.topic_name,
            "a": float(row.irt_discrimination or 1.0),
            "b": float(row.irt_difficulty or 0.0),
            "c": float(row.irt_guessing or 0.2),
        })

    # --- 4. Run 70/15/15 selection --------------------------------------
    quiz_level = engine.suggest_quiz_level(earned_level)

    selected = engine.select_next_set(
        questions=candidates,
        earned_level=earned_level,
        topic_mastery=topic_mastery,
        ability_theta=ability_theta,
        num_questions=request.num_questions,
    )

    # --- 5. Format response ---------------------------------------------
    question_out = []
    for q in selected:
        # Parse choices from JSONB
        raw_choices = q.get("choices", [])
        choices_out = []
        for i, ch in enumerate(raw_choices):
            if isinstance(ch, dict):
                choices_out.append(ChoiceOut(
                    label=ch.get("label", chr(65 + i)),
                    text=ch.get("text", ""),
                ))
            elif isinstance(ch, str):
                choices_out.append(ChoiceOut(
                    label=chr(65 + i),
                    text=ch,
                ))

        question_out.append(QuestionOut(
            id=q["id"],
            text=q["text"],
            choices=choices_out,
            difficulty=q["difficulty"],
            topic_id=int(q["topic_id"]),
            topic_name=q["topic_name"],
            exam_code=request.exam_code,
            irt_a=q["a"],
            irt_b=q["b"],
            irt_c=q["c"],
        ))

    return NextSetResponse(
        exam_code=request.exam_code,
        earned_level=earned_level,
        quiz_level=quiz_level,
        num_questions=len(question_out),
        questions=question_out,
        topic_mastery=topic_mastery,
    )
