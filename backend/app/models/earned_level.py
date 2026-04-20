"""
UserEarnedLevel model — the core ADAPT-style Earned Level tracker.

Each row tracks one user's progress on one exam.  `earned_level` is a
continuous 0.0–10.0 value that moves up or down after every quiz, using
an Elo-inspired update rule weighted by quiz difficulty.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Float, Integer, ForeignKey, Index, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base, IdMixin, TimestampMixin


class UserEarnedLevel(Base, IdMixin, TimestampMixin):
    """Earned Level (EL) per user per exam — the headline proficiency metric."""

    __tablename__ = "user_earned_levels"
    __table_args__ = (
        UniqueConstraint("user_id", "exam_id", name="uq_uel_user_exam"),
        Index("ix_uel_user_id", "user_id"),
        Index("ix_uel_exam_id", "exam_id"),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    exam_id: Mapped[int] = mapped_column(
        ForeignKey("exams.id", ondelete="CASCADE"), nullable=False
    )

    # The headline number students see (0.0 → 10.0)
    earned_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Highest EL ever reached (for badges / motivation)
    peak_level: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Aggregate counters
    total_quizzes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_correct: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_attempted: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Consecutive quizzes passed at or above current EL (for streak bonuses)
    streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    last_quiz_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    exam: Mapped["Exam"] = relationship("Exam", foreign_keys=[exam_id])

    def __repr__(self) -> str:
        return (
            f"<UserEarnedLevel(user={self.user_id}, exam={self.exam_id}, "
            f"EL={self.earned_level:.2f}, peak={self.peak_level:.2f})>"
        )
