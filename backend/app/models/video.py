"""
Video lesson models for the actuarial exam prep platform.

VideoLesson  — a full lecture video (owned by a topic)
VideoClip    — a 2–5 minute indexed sub-clip of a VideoLesson, with a
               YouTube start/end timestamp and relevance metadata used by
               the contextual-video endpoint.
"""
from __future__ import annotations

from typing import Optional

from sqlalchemy import String, Integer, Text, ForeignKey, Index, Boolean, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, IdMixin, TimestampMixin


class VideoLesson(Base, IdMixin, TimestampMixin):
    """Full lecture video, owned by a single topic."""

    __tablename__ = "video_lessons"
    __table_args__ = (
        Index("ix_video_lessons_topic_id", "topic_id"),
        Index("ix_video_lessons_topic_sort", "topic_id", "sort_order"),
        Index("ix_video_lessons_is_published", "is_published"),
    )

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    script_content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    youtube_video_id: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    channel_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    topic: Mapped["Topic"] = relationship(
        "Topic",
        back_populates="video_lessons",
        foreign_keys=[topic_id],
    )
    clips: Mapped[list["VideoClip"]] = relationship(
        "VideoClip",
        back_populates="lesson",
        cascade="all, delete-orphan",
        order_by="VideoClip.start_seconds",
    )

    def __repr__(self) -> str:
        return f"<VideoLesson(id={self.id}, topic_id={self.topic_id}, title={self.title!r})>"


class VideoClip(Base, IdMixin, TimestampMixin):
    """
    An indexed 2–5 minute sub-clip of a VideoLesson.

    Each clip targets a specific concept within the parent lesson's topic
    and carries enough metadata for the contextual-video selector to rank
    it against a missed question's topic_id and difficulty.

    embed_url example:
      https://www.youtube.com/embed/{youtube_video_id}?start={start_seconds}&end={end_seconds}&autoplay=1
    """

    __tablename__ = "video_clips"
    __table_args__ = (
        Index("ix_video_clips_lesson_id", "lesson_id"),
        Index("ix_video_clips_topic_id", "topic_id"),
        Index("ix_video_clips_difficulty", "min_difficulty", "max_difficulty"),
    )

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("video_lessons.id", ondelete="CASCADE"), nullable=False
    )
    # A clip may span concepts; allow direct topic association for fast lookup
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # YouTube timestamps (seconds from video start)
    start_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    end_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    # Difficulty band this clip is suited for (1–10)
    min_difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    max_difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=10)

    # Concept tags used for relevance ranking alongside topic_id
    concept_tags: Mapped[Optional[list]] = mapped_column(
        ARRAY(String), nullable=True, default=list
    )

    # Pre-computed relevance weight (0.0–1.0); can be updated offline
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    lesson: Mapped["VideoLesson"] = relationship(
        "VideoLesson",
        back_populates="clips",
        foreign_keys=[lesson_id],
    )

    @property
    def duration_seconds(self) -> int:
        return max(0, self.end_seconds - self.start_seconds)

    @property
    def embed_url(self) -> str:
        yt_id = self.lesson.youtube_video_id if self.lesson else ""
        return (
            f"https://www.youtube.com/embed/{yt_id}"
            f"?start={self.start_seconds}&end={self.end_seconds}&autoplay=1"
        )

    def __repr__(self) -> str:
        return (
            f"<VideoClip(id={self.id}, lesson_id={self.lesson_id}, "
            f"title={self.title!r}, {self.start_seconds}s–{self.end_seconds}s)>"
        )
