from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict, List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas.adaptive import (
    AdaptiveStateResponse,
    NextQuestionRequest,
    SessionStart,
    SessionResponse,
)


class PauseSessionRequest(BaseModel):
    question_index: int
    question_ids: List[int]
    variables_by_question: Dict[str, Dict[str, Any]] = {}

# Import services (will be created in parallel)
from app.services.adaptive_engine import AdaptiveEngine
from app.services.session_manager import SessionManager

router = APIRouter(
    prefix="/adaptive",
    tags=["adaptive"],
)


@router.get(
    "/state/{exam_code}",
    response_model=AdaptiveStateResponse,
    summary="Get user's adaptive state",
)
async def get_adaptive_state(
    exam_code: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AdaptiveStateResponse:
    """
    Get current adaptive learning state for an exam.

    Args:
        exam_code: Exam code (e.g., 'FM', 'P')
        current_user: Current authenticated user
        db: Database session

    Returns:
        AdaptiveStateResponse: Current ability estimate and topic mastery

    Raises:
        HTTPException: If exam code is invalid
    """
    engine = AdaptiveEngine(db)

    try:
        user_id = int(current_user.get("sub"))
        state = await engine.get_state(user_id=user_id, exam_code=exam_code)

        return AdaptiveStateResponse(
            exam_code=state["exam_code"],
            overall_ability=state["overall_ability"],
            readiness_score=state["readiness_score"],
            topic_mastery=state["topic_mastery"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/next",
    response_model=Dict[str, Any],
    summary="Get next adaptive question",
)
async def get_next_question(
    request: NextQuestionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Get next question adapted to user's current ability level.

    Args:
        request: Request with exam code and session ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Question with choices and metadata

    Raises:
        HTTPException: If session or exam not found
    """
    engine = AdaptiveEngine(db)

    try:
        user_id = int(current_user.get("sub"))
        question = await engine.get_next_question(
            user_id=user_id,
            exam_code=request.exam_code,
            session_id=request.session_id,
        )

        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No more questions available",
            )

        return question
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/sessions/start",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start new practice session",
)
async def start_session(
    request: SessionStart,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SessionResponse:
    """
    Start a new practice session.

    Args:
        request: Session configuration
        current_user: Current authenticated user
        db: Database session

    Returns:
        SessionResponse: Created session details

    Raises:
        HTTPException: If exam code or session type is invalid
    """
    manager = SessionManager(db)

    try:
        user_id = int(current_user.get("sub"))
        session = await manager.start_session(
            user_id=user_id,
            exam_code=request.exam_code,
            session_type=request.session_type,
            topic_id=request.topic_id,
        )

        return SessionResponse.from_orm(session)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/sessions/{session_id}/end",
    response_model=SessionResponse,
    summary="End practice session",
)
async def end_session(
    session_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SessionResponse:
    """
    End a practice session and calculate final score.

    Args:
        session_id: Session ID to end
        current_user: Current authenticated user
        db: Database session

    Returns:
        SessionResponse: Final session details with score

    Raises:
        HTTPException: If session not found or doesn't belong to user
    """
    manager = SessionManager(db)

    try:
        user_id = int(current_user.get("sub"))
        session = await manager.end_session(
            session_id=session_id,
            user_id=user_id,
        )

        return SessionResponse.from_orm(session)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to end this session",
        )


@router.post(
    "/sessions/{session_id}/pause",
    response_model=Dict[str, Any],
    summary="Pause a practice session",
)
async def pause_session(
    session_id: int,
    request: PauseSessionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Pause an active session and snapshot the exact randomised variable state
    for every unanswered question so the student resumes with identical numbers.
    """
    manager = SessionManager(db)
    try:
        user_id = int(current_user.get("sub"))
        return await manager.pause_session(
            session_id=session_id,
            user_id=user_id,
            question_index=request.question_index,
            question_ids=request.question_ids,
            variables_by_question=request.variables_by_question,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")


@router.post(
    "/sessions/{session_id}/resume",
    response_model=Dict[str, Any],
    summary="Resume a paused session",
)
async def resume_session(
    session_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    Resume a paused session. Returns the saved question state so the frontend
    can restore the exact question — and exact randomised numbers — the student
    left off on.
    """
    manager = SessionManager(db)
    try:
        user_id = int(current_user.get("sub"))
        return await manager.resume_session(session_id=session_id, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
