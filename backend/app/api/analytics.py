from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.study_plan import ProgressResponse, TopicBreakdown

# Import services (will be created in parallel)
from app.services.analytics_service import AnalyticsService

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@router.get(
    "/progress",
    response_model=ProgressResponse,
    summary="Get user's overall progress",
)
async def get_progress(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ProgressResponse:
    """
    Get user's overall progress across all exams.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        ProgressResponse: Overall stats and topic breakdown
    """
    analytics = AnalyticsService(db)

    try:
        user_id = int(current_user.get("sub"))
        progress = await analytics.get_overall_progress(user_id=user_id)

        return ProgressResponse(
            total_questions=progress["total_questions"],
            accuracy=progress["accuracy"],
            streak=progress["streak"],
            topic_breakdown=progress["topic_breakdown"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving progress",
        )


@router.get(
    "/readiness/{exam_code}",
    response_model=Dict[str, Any],
    summary="Get exam readiness score",
)
async def get_readiness(
    exam_code: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Get readiness score for a specific exam.

    Args:
        exam_code: Exam code (e.g., 'FM', 'P')
        current_user: Current authenticated user
        db: Database session

    Returns:
        Readiness score and breakdown

    Raises:
        HTTPException: If exam code is invalid
    """
    analytics = AnalyticsService(db)

    try:
        user_id = int(current_user.get("sub"))
        readiness = await analytics.get_readiness_score(
            user_id=user_id,
            exam_code=exam_code,
        )

        return readiness
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/weaknesses/{exam_code}",
    response_model=List[Dict[str, Any]],
    summary="Get weak topics for exam",
)
async def get_weaknesses(
    exam_code: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[Dict[str, Any]]:
    """
    Get list of weak topics where improvement is needed.

    Args:
        exam_code: Exam code (e.g., 'FM', 'P')
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of weak topics with details

    Raises:
        HTTPException: If exam code is invalid
    """
    analytics = AnalyticsService(db)

    try:
        user_id = int(current_user.get("sub"))
        weaknesses = await analytics.get_weak_topics(
            user_id=user_id,
            exam_code=exam_code,
        )

        return weaknesses
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
