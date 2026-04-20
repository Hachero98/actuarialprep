from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime


class StudyPlanRequest(BaseModel):
    """Schema for requesting a study plan."""

    exam_code: str = Field(..., description="Exam code")
    days_until_exam: int = Field(..., ge=1, description="Number of days until the exam")
    hours_per_day: float = Field(..., gt=0.0, description="Hours per day available for study")

    class Config:
        json_schema_extra = {
            "example": {
                "exam_code": "FM",
                "days_until_exam": 60,
                "hours_per_day": 2.5,
            }
        }


class DailyTask(BaseModel):
    """Schema for a daily study task."""

    date: str = Field(..., description="Date (YYYY-MM-DD)")
    topic: str = Field(..., description="Topic to study")
    questions_target: int = Field(..., description="Target number of questions")
    focus: str = Field(..., description="Focus area or task type")


class StudyPlanResponse(BaseModel):
    """Schema for study plan response."""

    exam_code: str = Field(..., description="Exam code")
    days_until_exam: int = Field(..., description="Days until exam")
    total_questions_target: int = Field(..., description="Total questions to practice")
    daily_tasks: List[DailyTask] = Field(..., description="Daily study tasks")
    created_at: datetime = Field(..., description="Plan creation timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "exam_code": "FM",
                "days_until_exam": 60,
                "total_questions_target": 1200,
                "daily_tasks": [
                    {
                        "date": "2026-04-15",
                        "topic": "Interest Theory",
                        "questions_target": 15,
                        "focus": "fundamentals",
                    }
                ],
                "created_at": "2026-04-15T10:30:00Z",
            }
        }


class TopicBreakdown(BaseModel):
    """Schema for topic performance breakdown."""

    topic: str = Field(..., description="Topic name")
    questions_attempted: int = Field(..., description="Number of questions attempted")
    correct: int = Field(..., description="Number of correct answers")
    accuracy: float = Field(..., ge=0.0, le=100.0, description="Accuracy percentage")
    mastery: float = Field(..., ge=0.0, le=1.0, description="Mastery level")


class ProgressResponse(BaseModel):
    """Schema for progress response."""

    total_questions: int = Field(..., description="Total questions attempted")
    accuracy: float = Field(..., ge=0.0, le=100.0, description="Overall accuracy percentage")
    streak: int = Field(..., description="Current correct answer streak")
    topic_breakdown: List[TopicBreakdown] = Field(..., description="Performance by topic")

    class Config:
        json_schema_extra = {
            "example": {
                "total_questions": 125,
                "accuracy": 74.4,
                "streak": 5,
                "topic_breakdown": [
                    {
                        "topic": "Interest Theory",
                        "questions_attempted": 25,
                        "correct": 20,
                        "accuracy": 80.0,
                        "mastery": 0.82,
                    }
                ],
            }
        }
