"""
Video Lessons API

GET  /lessons/                          — list all lessons (filterable)
GET  /lessons/{lesson_id}               — lesson detail
GET  /lessons/contextual-video          — ranked clip(s) by topic_id + difficulty
GET  /api/get-contextual-video          — ranked clip(s) by topic_id + subtopic_slug
                                          (Intelligent Content Layer contract)
"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.services.lesson_service import LessonService
from app.services.video_service import VideoService
from app.services.seed_templates import get_templates_by_subtopic

# Two routers: one under /lessons, one under /api (Intelligent Content Layer)
router = APIRouter(prefix="/lessons", tags=["lessons"])
api_router = APIRouter(prefix="/api", tags=["contextual-video"])


# ─── Pydantic response schemas ────────────────────────────────────────────────

class VideoClipOut(BaseModel):
    clip_id: int
    lesson_id: int
    topic_id: int
    title: str
    description: Optional[str] = None
    channel_name: Optional[str] = None
    youtube_video_id: Optional[str] = None
    start_seconds: int
    end_seconds: int
    duration_seconds: int
    video_url: str = Field(description="Embed URL with start/end timestamps")
    timestamp_start: int = Field(description="Alias for start_seconds — content layer contract")
    youtube_url: Optional[str] = None
    concept_tags: list[str] = []
    min_difficulty: int
    max_difficulty: int
    subtopic_slug: Optional[str] = None


class ContextualVideoResponse(BaseModel):
    topic_id: int
    subtopic_slug: Optional[str] = None
    difficulty: int
    clips: list[VideoClipOut]
    fallback: bool = False
    seed_template_ids: list[str] = Field(
        default_factory=list,
        description="IDs of matching question templates from the seed content layer",
    )


def _clip_to_out(c: dict[str, Any], subtopic_slug: Optional[str] = None) -> VideoClipOut:
    """Map a VideoService dict to the VideoClipOut schema."""
    return VideoClipOut(
        clip_id       = c["clip_id"],
        lesson_id     = c["lesson_id"],
        topic_id      = c["topic_id"],
        title         = c["title"],
        description   = c.get("description"),
        channel_name  = c.get("channel_name"),
        youtube_video_id = c.get("youtube_video_id"),
        start_seconds = c["start_seconds"],
        end_seconds   = c["end_seconds"],
        duration_seconds = c["duration_seconds"],
        video_url     = c["embed_url"],      # content-layer name
        timestamp_start = c["start_seconds"],
        youtube_url   = c.get("youtube_url"),
        concept_tags  = c.get("concept_tags", []),
        min_difficulty = c["min_difficulty"],
        max_difficulty = c["max_difficulty"],
        subtopic_slug  = subtopic_slug,
    )


# ─── /lessons/* endpoints ────────────────────────────────────────────────────

@router.get("/", response_model=list[dict[str, Any]], summary="List video lessons")
async def list_lessons(
    exam_code: Optional[str] = Query(None),
    topic_id: Optional[int] = Query(None),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[dict[str, Any]]:
    try:
        return await LessonService(db).list_lessons(exam_code=exam_code, topic_id=topic_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving lessons",
        )


@router.get(
    "/contextual-video",
    response_model=ContextualVideoResponse,
    summary="Ranked video clips for a missed question (by topic_id)",
)
async def get_contextual_video_by_topic(
    topic_id: int = Query(..., description="DB topic_id of the missed question"),
    difficulty: int = Query(5, ge=1, le=10),
    subtopic_slug: Optional[str] = Query(None, description="Optional subtopic slug for seed-template lookup"),
    limit: int = Query(3, ge=1, le=5),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ContextualVideoResponse:
    svc = VideoService(db)
    clips = await svc.get_contextual_clips(topic_id=topic_id, difficulty=difficulty, limit=limit)
    fallback = False
    if not clips:
        fallback = True
        clips = await svc.get_contextual_clips(topic_id=topic_id, difficulty=5, limit=limit)

    seed_ids = (
        [t["id"] for t in get_templates_by_subtopic(subtopic_slug)]
        if subtopic_slug else []
    )
    return ContextualVideoResponse(
        topic_id=topic_id,
        subtopic_slug=subtopic_slug,
        difficulty=difficulty,
        clips=[_clip_to_out(c, subtopic_slug) for c in clips],
        fallback=fallback,
        seed_template_ids=seed_ids,
    )


@router.get("/{lesson_id}", response_model=dict[str, Any], summary="Get lesson detail")
async def get_lesson_detail(
    lesson_id: int,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    lesson = await LessonService(db).get_lesson_detail(lesson_id=lesson_id)
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return lesson


# ─── /api/get-contextual-video  (Intelligent Content Layer contract) ──────────

@api_router.get(
    "/get-contextual-video",
    response_model=ContextualVideoResponse,
    summary="Contextual video by topic_id + subtopic_slug",
    description=(
        "Intelligent Content Layer endpoint. "
        "Accepts `topic_id` (DB FK) and `subtopic_slug` (e.g. 'redington-immunization'). "
        "Returns ranked VideoClip objects with `video_url` and `timestamp_start` fields "
        "for direct embedding in the Review modal. "
        "Also returns `seed_template_ids` listing matching expert question templates. "
        "Falls back to difficulty=5 search and sets `fallback=true` when no exact match exists."
    ),
)
async def get_contextual_video(
    topic_id: int = Query(..., description="DB FK topic_id"),
    subtopic_slug: str = Query(..., description="e.g. 'redington-immunization', 'order-statistics'"),
    difficulty: int = Query(5, ge=1, le=10, description="Question difficulty 1–10"),
    limit: int = Query(3, ge=1, le=5, description="Max clips to return"),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ContextualVideoResponse:
    svc = VideoService(db)

    clips = await svc.get_contextual_clips(topic_id=topic_id, difficulty=difficulty, limit=limit)
    fallback = False
    if not clips:
        fallback = True
        clips = await svc.get_contextual_clips(topic_id=topic_id, difficulty=5, limit=limit)

    seed_tpls = get_templates_by_subtopic(subtopic_slug)

    return ContextualVideoResponse(
        topic_id         = topic_id,
        subtopic_slug    = subtopic_slug,
        difficulty       = difficulty,
        clips            = [_clip_to_out(c, subtopic_slug) for c in clips],
        fallback         = fallback,
        seed_template_ids= [t["id"] for t in seed_tpls],
    )
