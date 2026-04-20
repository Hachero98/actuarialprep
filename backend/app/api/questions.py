from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.question import (
    QuestionGenerate,
    QuestionResponse,
    AnswerSubmit,
    AnswerResponse,
)

# Import services (will be created in parallel)
from app.services.question_generator import QuestionGenerator
from app.services.answer_evaluator import AnswerEvaluator

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
)


@router.post(
    "/generate",
    response_model=QuestionResponse,
    summary="Generate a question",
)
async def generate_question(
    request: QuestionGenerate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> QuestionResponse:
    """
    Generate a question based on exam and optional filters.

    Args:
        request: Question generation parameters
        current_user: Current authenticated user
        db: Database session

    Returns:
        QuestionResponse: Generated question with choices

    Raises:
        HTTPException: If exam code is invalid
    """
    question_generator = QuestionGenerator(db)

    try:
        question = await question_generator.generate(
            exam_code=request.exam_code,
            topic_id=request.topic_id,
            difficulty=request.difficulty,
        )

        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No questions available",
            )

        return QuestionResponse.from_orm(question)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/submit",
    response_model=AnswerResponse,
    summary="Submit an answer",
)
async def submit_answer(
    answer: AnswerSubmit,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AnswerResponse:
    """
    Submit an answer to a question and receive feedback.

    Records the answer, evaluates correctness, updates adaptive state,
    and returns feedback with mastery update.

    Args:
        answer: Answer submission data
        current_user: Current authenticated user
        db: Database session

    Returns:
        AnswerResponse: Feedback with correctness, explanation, and updated mastery

    Raises:
        HTTPException: If question or session not found
    """
    evaluator = AnswerEvaluator(db)

    try:
        user_id = int(current_user.get("sub"))

        result = await evaluator.evaluate_answer(
            user_id=user_id,
            question_id=answer.question_id,
            session_id=answer.session_id,
            selected_choice=answer.selected_choice,
            time_spent_seconds=answer.time_spent_seconds,
        )

        return AnswerResponse(
            is_correct=result["is_correct"],
            correct_answer=result["correct_answer"],
            explanation=result["explanation"],
            new_mastery=result["new_mastery"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing answer",
        )
