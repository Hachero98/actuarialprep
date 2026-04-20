"""
Exam and Topic models for the actuarial exam prep platform.
"""
from enum import Enum
from typing import Optional

from sqlalchemy import String, Integer, Boolean, Text, ForeignKey, Index, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IdMixin, TimestampMixin


class ExamCode(str, Enum):
    """Enum for SOA exam codes."""
    P = "P"
    FM = "FM"
    FAM = "FAM"
    ALTAM = "ALTAM"
    ASTAM = "ASTAM"
    SRM = "SRM"
    PA = "PA"


class Exam(Base, IdMixin, TimestampMixin):
    """Exam model representing SOA exams."""

    __tablename__ = "exams"
    __table_args__ = (
        Index("ix_exams_code", "code", unique=True),
        Index("ix_exams_is_active", "is_active"),
    )

    code: Mapped[ExamCode] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    time_limit_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)

    # Relationships
    topics: Mapped[list["Topic"]] = relationship(
        "Topic",
        back_populates="exam",
        cascade="all, delete-orphan",
        foreign_keys="Topic.exam_id",
    )

    def __repr__(self) -> str:
        return f"<Exam(id={self.id}, code={self.code}, name={self.name})>"


class Topic(Base, IdMixin, TimestampMixin):
    """Topic model representing exam topics/sections."""

    __tablename__ = "topics"
    __table_args__ = (
        Index("ix_topics_exam_id", "exam_id"),
        Index("ix_topics_exam_id_sort_order", "exam_id", "sort_order"),
    )

    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    learning_objectives: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        default=None,
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relationships
    exam: Mapped["Exam"] = relationship(
        "Exam",
        back_populates="topics",
        foreign_keys=[exam_id],
    )
    question_templates: Mapped[list["QuestionTemplate"]] = relationship(
        "QuestionTemplate",
        back_populates="topic",
        cascade="all, delete-orphan",
        foreign_keys="QuestionTemplate.topic_id",
    )
    video_lessons: Mapped[list["VideoLesson"]] = relationship(
        "VideoLesson",
        back_populates="topic",
        cascade="all, delete-orphan",
        foreign_keys="VideoLesson.topic_id",
    )

    def __repr__(self) -> str:
        return f"<Topic(id={self.id}, exam_id={self.exam_id}, name={self.name})>"
