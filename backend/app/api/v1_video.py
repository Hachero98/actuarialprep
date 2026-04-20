"""
Video Context API — v1
======================
GET /api/v1/contextual-video

Returns ranked VideoClip metadata (video_url, start_time, end_time,
concept_summary) for embedding directly in the Review modal after a student
misses a question.

Lookup strategy
───────────────
1. Exact match on (topic_id, subtopic_slug) in MOCK_CLIPS (in-process dict).
2. If none found, relax to topic_id-only match and set fallback=True.
3. If still none, return the global FALLBACK_CLIP and set fallback=True.

In production, step 1 would query the video_clips PostgreSQL table via
VideoService.  The mock dict is a drop-in substitute for testing without DB.

All Pydantic models use v2 style (model_config instead of class Config).
"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator

from app.core.security import get_current_user

router = APIRouter(prefix="/api/v1", tags=["contextual-video-v1"])


# ─── Pydantic v2 schemas ──────────────────────────────────────────────────────

class VideoClip(BaseModel):
    """
    A timestamped sub-clip of a longer video lesson.
    Designed to be embedded directly in the Review modal iframe.
    """
    model_config = {"frozen": True}

    clip_id: str = Field(description="Unique clip identifier")
    topic_id: int = Field(description="FK to topics table")
    subtopic_slug: str = Field(description="e.g. 'redington-immunization'")
    title: str
    channel: Optional[str] = None
    video_url: str = Field(
        description="Full YouTube embed URL with start/end query params, e.g. "
                    "https://www.youtube.com/embed/{id}?start=120&end=480"
    )
    start_time: int = Field(ge=0, description="Clip start time in seconds")
    end_time: int = Field(description="Clip end time in seconds")
    duration_seconds: int = Field(ge=0)
    concept_summary: str = Field(
        description="One-paragraph summary of the concept covered in this clip. "
                    "Displayed alongside the video in the Review modal."
    )
    difficulty_min: int = Field(default=1, ge=1, le=10)
    difficulty_max: int = Field(default=10, ge=1, le=10)
    concept_tags: list[str] = Field(default_factory=list)

    @field_validator("end_time")
    @classmethod
    def end_after_start(cls, v: int, info: Any) -> int:
        start = (info.data or {}).get("start_time", 0)
        if v <= start:
            raise ValueError(f"end_time ({v}) must be greater than start_time ({start})")
        return v

    @field_validator("duration_seconds", mode="before")
    @classmethod
    def compute_duration(cls, v: int, info: Any) -> int:
        data = info.data or {}
        start = data.get("start_time", 0)
        end = data.get("end_time", v + start)
        return end - start if end > start else v


class ContextualVideoResponse(BaseModel):
    """Response envelope for GET /api/v1/contextual-video."""
    model_config = {"populate_by_name": True}

    topic_id: int
    subtopic_slug: str
    difficulty: int
    clips: list[VideoClip]
    fallback: bool = Field(
        default=False,
        description="True when no exact (topic, subtopic) match was found.",
    )
    total_clips: int = Field(default=0)

    def model_post_init(self, __context: Any) -> None:
        object.__setattr__(self, "total_clips", len(self.clips))


# ─── Mock clip database ───────────────────────────────────────────────────────
# Production: replace this dict with a VideoService.get_contextual_clips() call.
# Keys: (topic_id, subtopic_slug) — topic_id=0 means "exam-wide".

def _yt(video_id: str, start: int, end: int) -> str:
    return f"https://www.youtube.com/embed/{video_id}?start={start}&end={end}&rel=0"


MOCK_CLIPS: dict[tuple[int, str], list[dict[str, Any]]] = {

    # ── Exam FM ──────────────────────────────────────────────────────────────

    (0, "redington-immunization"): [
        dict(
            clip_id="FM-IMM-001",
            topic_id=0,
            subtopic_slug="redington-immunization",
            title="Redington Immunization: Three Conditions Explained",
            channel="Actuarial Path",
            video_url=_yt("PLACEHOLDER_IMM_01", 0, 480),
            start_time=0, end_time=480, duration_seconds=480,
            concept_summary=(
                "Redington immunization protects a surplus against small parallel "
                "interest-rate shifts by matching (i) present values, (ii) Macaulay "
                "durations, and (iii) ensuring asset convexity exceeds liability convexity. "
                "The barbell structure of maturities straddling the liability duration "
                "automatically satisfies condition (iii)."
            ),
            difficulty_min=7, difficulty_max=10,
            concept_tags=["immunization", "duration", "convexity", "surplus", "FM"],
        ),
        dict(
            clip_id="FM-IMM-002",
            topic_id=0,
            subtopic_slug="redington-immunization",
            title="Solving for Asset Allocations — Linear System",
            channel="Actuarial Path",
            video_url=_yt("PLACEHOLDER_IMM_02", 120, 540),
            start_time=120, end_time=540, duration_seconds=420,
            concept_summary=(
                "The two PV-duration equations form a 2×2 linear system in the present "
                "values of the two asset components. Solving gives unique allocations "
                "provided the bond maturities straddle the liability Macaulay duration."
            ),
            difficulty_min=8, difficulty_max=10,
            concept_tags=["linear-system", "bond-allocation", "FM"],
        ),
    ],

    (0, "convexity-increasing-annuity"): [
        dict(
            clip_id="FM-CONV-001",
            topic_id=0,
            subtopic_slug="convexity-increasing-annuity",
            title="Duration and Convexity of Non-Level Payment Streams",
            channel="FinancialExamAcademy",
            video_url=_yt("PLACEHOLDER_CONV_01", 60, 420),
            start_time=60, end_time=420, duration_seconds=360,
            concept_summary=(
                "For a non-level annuity, duration is the PV-weighted average payment "
                "time and convexity is the PV-weighted average of t². "
                "Arithmetically increasing payments use the (Ia) annuity function; "
                "the convexity correction prevents over-hedging for large rate moves."
            ),
            difficulty_min=6, difficulty_max=9,
            concept_tags=["convexity", "duration", "increasing-annuity", "FM"],
        ),
    ],

    # ── Exam P ───────────────────────────────────────────────────────────────

    (0, "jacobian-transformation"): [
        dict(
            clip_id="P-JAC-001",
            topic_id=0,
            subtopic_slug="jacobian-transformation",
            title="Jacobian Transformation for Bivariate Densities",
            channel="StatQuest with Josh Starmer",
            video_url=_yt("PLACEHOLDER_JAC_01", 0, 450),
            start_time=0, end_time=450, duration_seconds=450,
            concept_summary=(
                "The Jacobian method finds the joint density of (U,V) = g(X,Y) by "
                "computing |∂(x,y)/∂(u,v)| — the absolute determinant of the inverse "
                "transformation. For (U,V) = (X+Y, X/(X+Y)) with independent "
                "exponentials, U and V turn out to be independent: U ~ Gamma and V ~ Beta."
            ),
            difficulty_min=7, difficulty_max=10,
            concept_tags=["Jacobian", "change-of-variables", "bivariate", "P"],
        ),
    ],

    (0, "poisson-process-varying-rates"): [
        dict(
            clip_id="P-PPR-001",
            topic_id=0,
            subtopic_slug="poisson-process-varying-rates",
            title="Non-Homogeneous Poisson Process: Integrated Rate Function",
            channel="MIT OpenCourseWare",
            video_url=_yt("PLACEHOLDER_PPR_01", 0, 480),
            start_time=0, end_time=480, duration_seconds=480,
            concept_summary=(
                "When the arrival rate λ(t) varies over time, counts follow a "
                "non-homogeneous Poisson process. The expected count over (s,t] is "
                "Λ(s,t) = ∫_s^t λ(u) du, and P(N(s,t]=k) = e^{-Λ} Λ^k / k!. "
                "Independence of non-overlapping intervals still holds."
            ),
            difficulty_min=7, difficulty_max=10,
            concept_tags=["Poisson-process", "non-homogeneous", "integrated-rate", "P"],
        ),
    ],

    (0, "aggregate-loss-pgf"): [
        dict(
            clip_id="P-AGG-001",
            topic_id=0,
            subtopic_slug="aggregate-loss-pgf",
            title="Compound Distributions and PGF Composition",
            channel="Math Monkley",
            video_url=_yt("PLACEHOLDER_AGG_01", 0, 360),
            start_time=0, end_time=360, duration_seconds=360,
            concept_summary=(
                "For S = X₁ + … + X_N with N ~ Poisson(λ), the MGF satisfies "
                "M_S(t) = G_N(M_X(t)) where G_N is the PGF of N. "
                "This gives E[S] = λE[X] and Var(S) = λ(E[X²])."
            ),
            difficulty_min=6, difficulty_max=9,
            concept_tags=["compound-Poisson", "MGF", "PGF", "aggregate-loss", "P"],
        ),
    ],

    (0, "order-statistics"): [
        dict(
            clip_id="P-ORD-001",
            topic_id=0,
            subtopic_slug="order-statistics",
            title="Order Statistics: Beta Distributions and Covariance",
            channel="jbstatistics",
            video_url=_yt("PLACEHOLDER_ORD_01", 0, 420),
            start_time=0, end_time=420, duration_seconds=420,
            concept_summary=(
                "The k-th order statistic X_(k) from Uniform(0,θ) follows a scaled "
                "Beta(k, n-k+1) distribution. E[X_(k)] = kθ/(n+1) — not k/n. "
                "Adjacent order statistics are positively correlated with "
                "ρ = √[j(n-k+1) / (k(n-j+1))]."
            ),
            difficulty_min=6, difficulty_max=9,
            concept_tags=["order-statistics", "Beta", "covariance", "P"],
        ),
    ],
}

# Global fallback used when no subtopic match exists at all
_FALLBACK_CLIP = dict(
    clip_id="FALLBACK-001",
    topic_id=0,
    subtopic_slug="general",
    title="Actuarial Mathematics: Core Concepts Review",
    channel="ActuarialPrep",
    video_url=_yt("PLACEHOLDER_FALLBACK", 0, 300),
    start_time=0, end_time=300, duration_seconds=300,
    concept_summary=(
        "A review of fundamental actuarial exam concepts including probability, "
        "interest theory, and annuity valuation. Recommended when a specific "
        "topic clip is not yet available."
    ),
    difficulty_min=1, difficulty_max=10,
    concept_tags=["review", "fundamentals"],
)


def _lookup(topic_id: int, subtopic_slug: str, difficulty: int, limit: int) -> tuple[list[VideoClip], bool]:
    """
    Return (clips, is_fallback).
    Priority: (topic_id, slug) → (0, slug) → (topic_id, any) → global fallback.
    """
    # 1. Exact match
    for key in [(topic_id, subtopic_slug), (0, subtopic_slug)]:
        rows = MOCK_CLIPS.get(key, [])
        if rows:
            # Filter by difficulty band, then sort by best match
            in_band = [r for r in rows if r["difficulty_min"] <= difficulty <= r["difficulty_max"]]
            ordered = in_band or rows
            return [VideoClip(**r) for r in ordered[:limit]], False

    # 2. Relax to any clip for this topic_id
    for slug_key in MOCK_CLIPS:
        if slug_key[0] == topic_id:
            rows = MOCK_CLIPS[slug_key][:limit]
            return [VideoClip(**r) for r in rows], True

    # 3. Global fallback
    return [VideoClip(**_FALLBACK_CLIP)], True


# ─── Endpoint ─────────────────────────────────────────────────────────────────

@router.get(
    "/contextual-video",
    response_model=ContextualVideoResponse,
    summary="Get contextual video clip for a missed question",
    description=(
        "Returns 1–3 ranked VideoClip objects whose topic and difficulty best match "
        "the question the student just missed. "
        "Each clip includes `video_url` (embed URL with timestamps), `start_time`, "
        "`end_time`, and `concept_summary` for display in the Review modal. "
        "Set `fallback=true` in the response indicates no exact subtopic match was found."
    ),
)
async def get_contextual_video(
    topic_id: int = Query(..., description="DB FK topic_id of the missed question"),
    subtopic_slug: str = Query(
        ...,
        description="e.g. 'redington-immunization', 'jacobian-transformation'",
    ),
    difficulty: int = Query(5, ge=1, le=10, description="Question difficulty (1–10)"),
    limit: int = Query(3, ge=1, le=5, description="Max clips to return"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> ContextualVideoResponse:
    clips, fallback = _lookup(topic_id, subtopic_slug, difficulty, limit)
    return ContextualVideoResponse(
        topic_id=topic_id,
        subtopic_slug=subtopic_slug,
        difficulty=difficulty,
        clips=clips,
        fallback=fallback,
    )


# ─── Contextual Content endpoint (VideoManifest) ──────────────────────────────

class VideoManifest(BaseModel):
    """
    Richer content manifest returned by GET /api/v1/contextual-content.
    Includes prerequisite formulas for display above the video embed.
    """
    model_config = {"frozen": True}

    clip_id: str
    topic_id: int
    subtopic_slug: str
    title: str
    video_url: str = Field(description="Full YouTube embed URL with start/end params")
    start_timestamp: int = Field(ge=0, description="Clip start in seconds")
    duration: int = Field(ge=0, description="Clip length in seconds")
    concept_summary: str
    pre_requisite_formulas: list[str] = Field(
        default_factory=list,
        description="KaTeX-ready display formulas the student should know before watching.",
    )
    fallback: bool = False


# Prerequisite formula bank keyed by subtopic_slug
_PREREQ_FORMULAS: dict[str, list[str]] = {
    "redington-immunization": [
        "$$P_L = \\sum_t CF_t \\cdot v^t$$",
        "$$D_L = \\frac{\\sum_t t \\cdot CF_t v^t}{P_L}$$",
        "$$\\mathcal{C}_A > \\mathcal{C}_L \\iff \\text{Redington condition (iii)}$$",
    ],
    "convexity-increasing-annuity": [
        "$$a_{\\overline{n}|} = \\frac{1-v^n}{i}$$",
        "$$(Ia)_{\\overline{n}|} = \\frac{\\ddot{a}_{\\overline{n}|} - nv^n}{i}$$",
        "$$\\mathcal{C} = \\frac{1}{PV(1+i)^2}\\sum_t t^2 C_t v^t$$",
    ],
    "convexity-geometric-annuity-due": [
        "$$w = \\frac{1+g}{1+i}, \\quad PV = C\\cdot\\frac{1-w^n}{i-g}$$",
        "$$D_{\\mathrm{mac}} = \\frac{w}{1-w} - \\frac{nw^n}{1-w^n}$$",
        "$$\\Delta PV \\approx -D_{\\mathrm{mod}}\\cdot PV\\cdot\\Delta i + \\tfrac{1}{2}\\mathcal{C}\\cdot PV\\cdot(\\Delta i)^2$$",
    ],
    "jacobian-transformation": [
        "$$f_{U,V}(u,v) = f_{X,Y}(g^{-1}(u,v))\\cdot|J|$$",
        "$$|J| = \\left|\\frac{\\partial(x,y)}{\\partial(u,v)}\\right|$$",
        "$$E[V] = E\\!\\left[\\frac{X}{X+Y}\\right] = \\frac{\\lambda_2}{\\lambda_1+\\lambda_2}$$",
    ],
    "poisson-process-varying-rates": [
        "$$\\Lambda(s,t) = \\int_s^t \\lambda(u)\\,du$$",
        "$$P(N(s,t]=k) = \\frac{e^{-\\Lambda}\\Lambda^k}{k!}$$",
    ],
    "aggregate-loss-pgf": [
        "$$M_S(t) = G_N(M_X(t))$$",
        "$$E[S] = \\lambda\\theta, \\quad \\mathrm{Var}(S) = 2\\lambda\\theta^2$$",
    ],
    "order-statistics": [
        "$$E[X_{(k)}] = \\frac{k\\theta}{n+1}$$",
        "$$\\mathrm{Cov}(X_{(j)},X_{(k)}) = \\frac{j(n-k+1)\\theta^2}{(n+1)^2(n+2)}$$",
    ],
}


def _clip_to_manifest(clip: VideoClip, fallback: bool = False) -> VideoManifest:
    prereqs = _PREREQ_FORMULAS.get(clip.subtopic_slug, [])
    return VideoManifest(
        clip_id=clip.clip_id,
        topic_id=clip.topic_id,
        subtopic_slug=clip.subtopic_slug,
        title=clip.title,
        video_url=clip.video_url,
        start_timestamp=clip.start_time,
        duration=clip.duration_seconds,
        concept_summary=clip.concept_summary,
        pre_requisite_formulas=prereqs,
        fallback=fallback,
    )


@router.get(
    "/contextual-content",
    response_model=VideoManifest,
    summary="Get contextual video manifest with prerequisite formulas",
    description=(
        "Returns the best-matched VideoManifest for the given topic/subtopic. "
        "The manifest includes `video_url`, `start_timestamp`, `duration`, "
        "`concept_summary`, and a `pre_requisite_formulas` list of KaTeX strings "
        "for display above the video embed in the Review modal."
    ),
)
async def get_contextual_content(
    topic_id: int = Query(..., description="DB FK topic_id of the missed question"),
    subtopic_slug: str = Query(
        ...,
        description="e.g. 'redington-immunization', 'jacobian-transformation'",
    ),
    difficulty: int = Query(5, ge=1, le=10, description="Question difficulty (1–10)"),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> VideoManifest:
    clips, fallback = _lookup(topic_id, subtopic_slug, difficulty, limit=1)
    if not clips:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No video content found for subtopic '{subtopic_slug}'.",
        )
    return _clip_to_manifest(clips[0], fallback=fallback)
