from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class QuestionGenerate(BaseModel):
    """Schema for generating a question."""

    exam_code: str = Field(..., description="Exam code (e.g., 'FM', 'P')")
    topic_id: Optional[int] = Field(None, description="Optional topic ID to filter questions")
    difficulty: Optional[str] = Field(None, description="Optional difficulty level (easy, medium, hard)")

    class Config:
        json_schema_extra = {
            "example": {
                "exam_code": "FM",
                "topic_id": 1,
                "difficulty": "medium",
            }
        }


class QuestionResponse(BaseModel):
    """Schema for question response."""

    id: int = Field(..., description="Question ID")
    text: str = Field(..., description="Question text")
    choices: List[str] = Field(..., description="Answer choices")
    difficulty: str = Field(..., description="Difficulty level")
    topic: str = Field(..., description="Topic name")
    exam: str = Field(..., description="Exam code")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "text": "What is the present value of...",
                "choices": ["A) $100", "B) $200", "C) $300", "D) $400"],
                "difficulty": "medium",
                "topic": "Interest Theory",
                "exam": "FM",
            }
        }


class AnswerSubmit(BaseModel):
    """Schema for submitting an answer."""

    question_id: int = Field(..., description="Question ID")
    session_id: int = Field(..., description="Practice session ID")
    selected_choice: int = Field(..., ge=0, description="Index of selected choice")
    time_spent_seconds: int = Field(..., ge=0, description="Time spent on this question in seconds")

    class Config:
        json_schema_extra = {
            "example": {
                "question_id": 1,
                "session_id": 1,
                "selected_choice": 2,
                "time_spent_seconds": 45,
            }
        }


class AnswerResponse(BaseModel):
    """Schema for answer feedback response."""

    is_correct: bool = Field(..., description="Whether the answer is correct")
    correct_answer: int = Field(..., description="Index of correct answer")
    explanation: str = Field(..., description="Explanation of the correct answer")
    new_mastery: float = Field(..., ge=0.0, le=1.0, description="Updated mastery level for the topic")

    class Config:
        json_schema_extra = {
            "example": {
                "is_correct": True,
                "correct_answer": 2,
                "explanation": "The present value is calculated using the formula PV = FV / (1+r)^n...",
                "new_mastery": 0.78,
            }
        }
