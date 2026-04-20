from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.study_plan import (
    StudyPlanRequest,
    StudyPlanResponse,
)

# Import services (will be created in parallel)
from app.services.study_plan_generator import StudyPlanGenerator

router = APIRouter(
    prefix="/study-plan",
    tags=["study_plan"],
)


@router.get(
    "/plan/{exam_code}",
    response_model=StudyPlanResponse,
    summary="Get user's study plan",
)
async def get_study_plan(
    exam_code: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudyPlanResponse:
    """
    Get the user's current study plan for an exam.

    Args:
        exam_code: Exam code (e.g., 'FM', 'P')
        current_user: Current authenticated user
        db: Database session

    Returns:
        StudyPlanResponse: Current study plan with daily tasks

    Raises:
        HTTPException: If exam code is invalid or no plan exists
    """
    generator = StudyPlanGenerator(db)

    try:
        user_id = int(current_user.get("sub"))
        plan = await generator.get_plan(
            user_id=user_id,
            exam_code=exam_code,
        )

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No study plan found. Create one first.",
            )

        return StudyPlanResponse.from_orm(plan)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/plan/generate",
    response_model=StudyPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate new study plan",
)
async def generate_study_plan(
    request: StudyPlanRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StudyPlanResponse:
    """
    Generate a new personalized study plan.

    Creates a customized study schedule based on available time,
    days until exam, and adaptive learning state.

    Args:
        request: Study plan parameters
        current_user: Current authenticated user
        db: Database session

    Returns:
        StudyPlanResponse: Generated study plan

    Raises:
        HTTPException: If exam code is invalid
    """
    generator = StudyPlanGenerator(db)

    try:
        user_id = int(current_user.get("sub"))
        plan = await generator.generate_plan(
            user_id=user_id,
            exam_code=request.exam_code,
            days_until_exam=request.days_until_exam,
            hours_per_day=request.hours_per_day,
        )

        return StudyPlanResponse.from_orm(plan)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
