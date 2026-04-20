"""
Models package — import all models so Alembic / create_all() discovers them.
"""
from .base import Base, IdMixin, TimestampMixin
from .user import User, UserRole
from .exam import Exam, ExamCode, Topic
from .question import QuestionTemplate, Question
from .performance import UserPerformance, AdaptiveState, PracticeSession, SessionType
from .earned_level import UserEarnedLevel
from .video import VideoLesson

__all__ = [
    "Base",
    "IdMixin",
    "TimestampMixin",
    "User",
    "UserRole",
    "Exam",
    "ExamCode",
    "Topic",
    "QuestionTemplate",
    "Question",
    "UserPerformance",
    "AdaptiveState",
    "PracticeSession",
    "SessionType",
    "UserEarnedLevel",
    "VideoLesson",
]
