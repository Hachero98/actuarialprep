"""
Question models for the actuarial exam prep platform.
"""
from typing import Optional

from sqlalchemy import String, Integer, Text, ForeignKey, Index, Float
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IdMixin, TimestampMixin


class QuestionTemplate(Base, IdMixin, TimestampMixin):
    """QuestionTemplate model for parameterized question generation."""

    __tablename__ = "question_templates"
    __table_args__ = (
        Index("ix_question_templates_topic_id", "topic_id"),
    )

    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-10 scale
    template_text: Mapped[str] = mapped_column(Text, nullable=False)
    solution_template: Mapped[str] = mapped_column(Text, nullable=False)
    variables_config: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    distractor_config: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )
    explanation_template: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        nullable=True,
        default=None,
    )

    # Relationships
    topic: Mapped["Topic"] = relationship(
        "Topic",
        back_populates="question_templates",
        foreign_keys=[topic_id],
    )
    questions: Mapped[list["Question"]] = relationship(
        "Question",
        back_populates="template",
        cascade="all, delete-orphan",
        foreign_keys="Question.template_id",
    )

    def __repr__(self) -> str:
        return f"<QuestionTemplate(id={self.id}, topic_id={self.topic_id}, difficulty={self.difficulty})>"


class Question(Base, IdMixin, TimestampMixin):
    """Question model for rendered question instances."""

    __tablename__ = "questions"
    __table_args__ = (
        Index("ix_questions_template_id", "template_id"),
    )

    template_id: Mapped[int] = mapped_column(ForeignKey("question_templates.id", ondelete="CASCADE"), nullable=False)
    rendered_text: Mapped[str] = mapped_column(Text, nullable=False)
    choices: Mapped[list[dict]] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )
    correct_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # 0-based
    rendered_solution: Mapped[str] = mapped_column(Text, nullable=False)
    rendered_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    variables_used: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    difficulty: Mapped[float] = mapped_column(Float, nullable=False)
    irt_discrimination: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    irt_difficulty: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    irt_guessing: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Added by migration 002 — tutor/content layer fields
    template_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    solution: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    common_mistakes: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String), nullable=True)
    correct_answer_label: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    correct_answer_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    exam_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    topic_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    template: Mapped["QuestionTemplate"] = relationship(
        "QuestionTemplate",
        back_populates="questions",
        foreign_keys=[template_id],
    )
    performance_records: Mapped[list["UserPerformance"]] = relationship(
        "UserPerformance",
        back_populates="question",
        cascade="all, delete-orphan",
        foreign_keys="UserPerformance.question_id",
    )

    def __repr__(self) -> str:
        return f"<Question(id={self.id}, template_id={self.template_id}, difficulty={self.difficulty})>"
