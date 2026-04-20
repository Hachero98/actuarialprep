"""
Performance tracking models for the actuarial exam prep platform.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Integer, Boolean, ForeignKey, Index, DateTime, Float, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base, IdMixin, TimestampMixin


class SessionType(str, Enum):
    """Enum for practice session types."""
    ADAPTIVE = "adaptive"
    TOPIC_QUIZ = "topic_quiz"
    TIMED_EXAM = "timed_exam"


class UserPerformance(Base, IdMixin, TimestampMixin):
    """UserPerformance model tracking individual question attempts."""

    __tablename__ = "user_performance"
    __table_args__ = (
        Index("ix_user_performance_user_id", "user_id"),
        Index("ix_user_performance_question_id", "question_id"),
        Index("ix_user_performance_session_id", "session_id"),
        Index("ix_user_performance_user_question", "user_id", "question_id"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    session_id: Mapped[int] = mapped_column(ForeignKey("practice_sessions.id", ondelete="CASCADE"), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    selected_choice: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Pause/resume persistence — stores the exact random seed and resolved variable
    # values so the question text is byte-for-byte identical on resume.
    random_seed: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    variable_values: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # template_id back-reference for quick lookup without joining question_templates
    template_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("question_templates.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )
    question: Mapped["Question"] = relationship(
        "Question",
        back_populates="performance_records",
        foreign_keys=[question_id],
    )
    session: Mapped["PracticeSession"] = relationship(
        "PracticeSession",
        back_populates="performance_records",
        foreign_keys=[session_id],
    )

    def __repr__(self) -> str:
        return f"<UserPerformance(id={self.id}, user_id={self.user_id}, question_id={self.question_id}, correct={self.is_correct})>"


class AdaptiveState(Base, IdMixin, TimestampMixin):
    """AdaptiveState model tracking user ability and mastery across topics."""

    __tablename__ = "adaptive_states"
    __table_args__ = (
        Index("ix_adaptive_states_user_id", "user_id"),
        Index("ix_adaptive_states_exam_id", "exam_id"),
        Index("ix_adaptive_states_user_exam", "user_id", "exam_id", unique=True),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    topic_mastery: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    overall_ability: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    readiness_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )
    exam: Mapped["Exam"] = relationship(
        "Exam",
        foreign_keys=[exam_id],
    )

    def __repr__(self) -> str:
        return f"<AdaptiveState(id={self.id}, user_id={self.user_id}, exam_id={self.exam_id}, ability={self.overall_ability})>"


class PracticeSession(Base, IdMixin, TimestampMixin):
    """PracticeSession model tracking exam practice attempts."""

    __tablename__ = "practice_sessions"
    __table_args__ = (
        Index("ix_practice_sessions_user_id", "user_id"),
        Index("ix_practice_sessions_exam_id", "exam_id"),
        Index("ix_practice_sessions_user_exam", "user_id", "exam_id"),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    session_type: Mapped[SessionType] = mapped_column(nullable=False)
    quiz_level: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    el_before: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    el_after: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],
    )
    exam: Mapped["Exam"] = relationship(
        "Exam",
        foreign_keys=[exam_id],
    )
    performance_records: Mapped[list["UserPerformance"]] = relationship(
        "UserPerformance",
        back_populates="session",
        cascade="all, delete-orphan",
        foreign_keys="UserPerformance.session_id",
    )

    def __repr__(self) -> str:
        return f"<PracticeSession(id={self.id}, user_id={self.user_id}, exam_id={self.exam_id}, type={self.session_type})>"
