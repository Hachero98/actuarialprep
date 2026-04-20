"""
Tutor API — Socratic explanation endpoint.

POST /api/tutor/explain
    Body: TutorRequestSchema
    Returns: TutorResponseSchema (KaTeX-ready LaTeX)
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.question import Question
from app.services.tutor_service import TutorRequest, TutorService

router = APIRouter(prefix="/tutor", tags=["tutor"])

_service = TutorService()


# ─── Schemas ──────────────────────────────────────────────────────────────────

class ExplainRequest(BaseModel):
    question_id: int
    user_answer_label: str = Field("—", description="Label the student selected (A-E or — for skipped)")
    user_variables: dict[str, Any] = Field(
        default_factory=dict,
        description="Resolved variable values used when the question was rendered.",
    )


class StepSchema(BaseModel):
    index: int
    text: str


class WrongChoiceSchema(BaseModel):
    label: str
    explanation: str


class ExplainResponse(BaseModel):
    question_id: int
    socratic_hook: str
    why_this_method: str
    step_by_step: list[StepSchema]
    key_formula: str
    why_other_choices_wrong: list[WrongChoiceSchema]
    memory_anchor: str
    follow_up_question: str
    latex_safe: bool


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@router.post(
    "/explain",
    response_model=ExplainResponse,
    summary="Generate a Socratic explanation for a question",
    description=(
        "Takes the question ID, the variables used to render it, and the student's "
        "answer. Returns a structured, KaTeX-ready explanation focusing on the "
        "mathematical *why* behind the correct approach."
    ),
)
async def explain(
    body: ExplainRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ExplainResponse:
    # Load question from DB
    result = await db.execute(select(Question).where(Question.id == body.question_id))
    q = result.scalar_one_or_none()
    if q is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    # Build TutorRequest — pull fields from the Question model
    # The question schema stores solution as JSONB {calculation, concept} or plain text
    solution = q.solution if isinstance(q.solution, dict) else {"calculation": str(q.solution), "concept": ""}
    common_mistakes = q.common_mistakes if hasattr(q, "common_mistakes") and q.common_mistakes else []

    # Render the stem with the provided variables
    stem = _service.render_template(q.template_text or q.stem or "", body.user_variables)

    req = TutorRequest(
        question_template=q.template_text or q.stem or "",
        user_variables=body.user_variables,
        rendered_stem=stem,
        topic_id=str(q.topic_id),
        topic_name=getattr(q, "topic_name", ""),
        exam_code=getattr(q, "exam_code", ""),
        correct_answer_label=q.correct_answer_label if hasattr(q, "correct_answer_label") else "",
        correct_answer_text=q.correct_answer_text if hasattr(q, "correct_answer_text") else "",
        user_answer_label=body.user_answer_label,
        solution_calculation=solution.get("calculation", ""),
        solution_concept=solution.get("concept", ""),
        difficulty=q.difficulty or 5,
        common_mistakes=common_mistakes,
    )

    resp = await _service.explain(req)

    return ExplainResponse(
        question_id=body.question_id,
        socratic_hook=resp.socratic_hook,
        why_this_method=resp.why_this_method,
        step_by_step=[
            StepSchema(index=i + 1, text=s) for i, s in enumerate(resp.step_by_step)
        ],
        key_formula=resp.key_formula,
        why_other_choices_wrong=[
            WrongChoiceSchema(label=w["label"], explanation=w["explanation"])
            for w in resp.why_other_choices_wrong
        ],
        memory_anchor=resp.memory_anchor,
        follow_up_question=resp.follow_up_question,
        latex_safe=resp.latex_safe,
    )
