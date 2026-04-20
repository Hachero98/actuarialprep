"""
Video Service — contextual clip selection.

Given a topic_id and an optional difficulty, selects the best matching
VideoClip(s) from the database for display in the Review modal.

Ranking algorithm
─────────────────
1. Hard filter: clip.topic_id == topic_id AND is_published == True
2. Soft filter: difficulty within [min_difficulty, max_difficulty] of the clip
3. Rank by:
     score = relevance_score * difficulty_bonus * duration_bonus
   where
     difficulty_bonus = 1.2 if question difficulty is in the clip's band, else 0.8
     duration_bonus   = 1.0 if 90 ≤ duration ≤ 300 seconds (ideal 1.5–5 min), else 0.6
4. Return top N clips (default 3)
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.video import VideoClip, VideoLesson

logger = logging.getLogger(__name__)

# Ideal clip length: 90 s – 300 s  (1.5 – 5 minutes)
_MIN_IDEAL_S = 90
_MAX_IDEAL_S = 300


class VideoService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_contextual_clips(
        self,
        topic_id: int,
        difficulty: int = 5,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        """
        Return up to `limit` ranked VideoClip dicts for the Review modal.
        Each dict is safe to serialise directly to JSON.
        """
        # Load candidate clips with their parent lesson (for youtube_video_id)
        stmt = (
            select(VideoClip)
            .join(VideoLesson, VideoClip.lesson_id == VideoLesson.id)
            .where(
                and_(
                    VideoClip.topic_id == topic_id,
                    VideoClip.is_published.is_(True),
                )
            )
        )
        result = await self.db.execute(stmt)
        clips: list[VideoClip] = list(result.scalars().all())

        if not clips:
            logger.debug("No published clips found for topic_id=%s", topic_id)
            return []

        # Score and sort
        scored = sorted(
            [(_score(clip, difficulty), clip) for clip in clips],
            key=lambda x: x[0],
            reverse=True,
        )

        return [_serialize(clip) for _, clip in scored[:limit]]

    async def get_clip_by_id(self, clip_id: int) -> Optional[dict[str, Any]]:
        result = await self.db.execute(
            select(VideoClip).where(VideoClip.id == clip_id)
        )
        clip = result.scalar_one_or_none()
        return _serialize(clip) if clip else None


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _score(clip: VideoClip, difficulty: int) -> float:
    in_band = clip.min_difficulty <= difficulty <= clip.max_difficulty
    difficulty_bonus = 1.2 if in_band else 0.8

    dur = clip.duration_seconds
    duration_bonus = 1.0 if _MIN_IDEAL_S <= dur <= _MAX_IDEAL_S else 0.6

    return clip.relevance_score * difficulty_bonus * duration_bonus


def _serialize(clip: VideoClip) -> dict[str, Any]:
    yt_id = clip.lesson.youtube_video_id if clip.lesson else ""
    return {
        "clip_id": clip.id,
        "lesson_id": clip.lesson_id,
        "topic_id": clip.topic_id,
        "title": clip.title,
        "description": clip.description,
        "channel_name": clip.lesson.channel_name if clip.lesson else None,
        "youtube_video_id": yt_id,
        "start_seconds": clip.start_seconds,
        "end_seconds": clip.end_seconds,
        "duration_seconds": clip.duration_seconds,
        "embed_url": clip.embed_url,
        # Convenience direct-link for "Open on YouTube"
        "youtube_url": (
            f"https://www.youtube.com/watch?v={yt_id}&t={clip.start_seconds}"
            if yt_id else None
        ),
        "concept_tags": clip.concept_tags or [],
        "min_difficulty": clip.min_difficulty,
        "max_difficulty": clip.max_difficulty,
    }
