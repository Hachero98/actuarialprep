from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime


class AdaptiveStateResponse(BaseModel):
    """Schema for adaptive learning state response."""

    exam_code: str = Field(..., description="Exam code")
    overall_ability: float = Field(..., ge=0.0, le=1.0, description="Overall ability estimate (0-1)")
    readiness_score: float = Field(..., ge=0.0, le=100.0, description="Readiness percentage (0-100)")
    topic_mastery: Dict[str, float] = Field(
        ...,
        description="Mastery level for each topic (0-1)",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "exam_code": "FM",
                "overall_ability": 0.72,
                "readiness_score": 72.0,
                "topic_mastery": {
                    "Interest Theory": 0.85,
                    "Annuities": 0.68,
                    "Bonds": 0.70,
                },
            }
        }


class NextQuestionRequest(BaseModel):
    """Schema for requesting next question."""

    exam_code: str = Field(..., description="Exam code")
    session_id: int = Field(..., description="Practice session ID")

    class Config:
        json_schema_extra = {
            "example": {
                "exam_code": "FM",
                "session_id": 1,
            }
        }


class SessionStart(BaseModel):
    """Schema for starting a new practice session."""

    exam_code: str = Field(..., description="Exam code")
    session_type: str = Field(
        ...,
        description="Session type: 'adaptive', 'topic_quiz', or 'timed_exam'",
    )
    topic_id: Optional[int] = Field(None, description="Optional topic ID for topic-specific sessions")

    class Config:
        json_schema_extra = {
            "example": {
                "exam_code": "FM",
                "session_type": "adaptive",
                "topic_id": None,
            }
        }


class SessionResponse(BaseModel):
    """Schema for session response."""

    session_id: int = Field(..., description="Session ID")
    exam: str = Field(..., description="Exam code")
    questions_answered: int = Field(..., description="Number of questions answered")
    score: float = Field(..., ge=0.0, le=100.0, description="Session score")
    duration: int = Field(..., description="Session duration in seconds")
    created_at: datetime = Field(..., description="Session start timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "session_id": 1,
                "exam": "FM",
                "questions_answered": 10,
                "score": 75.5,
                "duration": 1200,
                "created_at": "2026-04-15T10:30:00Z",
            }
        }
