"""
Session State Schemas — Work-in-Progress Persistence
=====================================================
Pydantic v2 schemas for storing and restoring a student's exact question state
so that browser refresh does not change interest rates, time periods, or any
other randomly-generated variable.

Design principle
────────────────
A single `WorkInProgressState` row is written to PostgreSQL the moment a
question is rendered.  On refresh:
  1. Frontend sends session_id + question_id.
  2. Backend loads the row and returns `seed_value` + `active_variable_map`.
  3. Frontend re-renders with the IDENTICAL variable values.

The `seed_value` is the integer used to initialise Python's `random.seed()` or
`numpy.random.default_rng()`.  Combined with the deterministic generation
function it guarantees byte-for-byte identical question text.

Usage
─────
    state = WorkInProgressState(
        session_id=42,
        question_id=17,
        template_id="FM-TPL-001",
        seed_value=839271,
        active_variable_map={"i": 0.0450, "n": 20, "P": 1000.0, "F": 1000.0},
        question_index=3,
    )
    db_row = state.to_json_column()   # store in JSONB column
    restored = WorkInProgressState.from_json_column(db_row)
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ─── Variable value schema ────────────────────────────────────────────────────

class VariableValue(BaseModel):
    """
    Single resolved variable with metadata.
    All floats are rounded to 4 decimal places at validation time.
    """
    model_config = {"frozen": True}

    name: str = Field(description="Variable name, e.g. 'i', 'n', 'lambda'")
    value: float | int | str = Field(description="Resolved value")
    display: str = Field(default="", description="Human-readable display string, e.g. '4.50%'")
    unit: Optional[str] = Field(default=None, description="Optional unit, e.g. 'years', '%'")

    @field_validator("value", mode="before")
    @classmethod
    def round_floats(cls, v: Any) -> Any:
        if isinstance(v, float):
            return round(v, 4)
        return v


# ─── Core WIP state schema ────────────────────────────────────────────────────

class WorkInProgressState(BaseModel):
    """
    Complete state required to reconstruct a question identically on resume.

    Storage contract
    ────────────────
    This object is stored as a JSONB value in the `user_performance.variable_values`
    column (added by migration 003) OR in `practice_sessions.paused_state`.

    seed_value          : integer seed used with random.seed() / numpy rng
    active_variable_map : flat dict {var_name: resolved_value} for quick frontend use
    variable_details    : richer per-variable metadata (optional, for UI display)
    """
    model_config = {"populate_by_name": True}

    session_id: int = Field(description="FK to practice_sessions.id")
    question_id: int = Field(description="FK to questions.id")
    template_id: str = Field(description="Template identifier e.g. 'FM-TPL-001'")
    question_index: int = Field(ge=0, description="0-based index within the session")

    # ── Reproducibility fields ──────────────────────────────────────────────
    seed_value: int = Field(
        description=(
            "Integer random seed.  Pass to random.seed(seed_value) or "
            "numpy.random.default_rng(seed_value) before calling the "
            "variable-generation function to reproduce identical values."
        )
    )
    active_variable_map: dict[str, float | int | str] = Field(
        description=(
            "Flat dict of resolved variable values, e.g. {'i': 0.05, 'n': 20}. "
            "All floats are rounded to 4 d.p.  "
            "Frontend renders the question template with these values directly."
        )
    )
    variable_details: list[VariableValue] = Field(
        default_factory=list,
        description="Rich metadata per variable — used for display and validation.",
    )

    # ── Timestamps ──────────────────────────────────────────────────────────
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When this state was first persisted (UTC).",
    )
    last_seen_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Updated each time the student loads this question (UTC).",
    )

    # ── Optional enrichment ─────────────────────────────────────────────────
    exam_code: Optional[str] = Field(default=None, description="'P', 'FM', etc.")
    rendered_stem: Optional[str] = Field(
        default=None,
        description="The full rendered question text (template + variables substituted).",
    )

    # ── Validators ──────────────────────────────────────────────────────────

    @field_validator("active_variable_map", mode="before")
    @classmethod
    def round_map_floats(cls, v: dict) -> dict:
        """Round all float values in the map to 4 decimal places."""
        return {
            k: round(val, 4) if isinstance(val, float) else val
            for k, val in v.items()
        }

    @model_validator(mode="after")
    def sync_variable_details(self) -> "WorkInProgressState":
        """
        If variable_details is empty but active_variable_map is populated,
        auto-generate minimal VariableValue entries for each map entry.
        """
        if not self.variable_details and self.active_variable_map:
            details = []
            for name, value in self.active_variable_map.items():
                display = (
                    f"{value:.2%}" if name in ("i", "rate", "delta", "d")
                    else str(value)
                )
                details.append(VariableValue(name=name, value=value, display=display))
            object.__setattr__(self, "variable_details", details)
        return self

    # ── Helpers ─────────────────────────────────────────────────────────────

    def to_json_column(self) -> dict[str, Any]:
        """Serialise for storage in a PostgreSQL JSONB column."""
        return json.loads(self.model_dump_json())

    @classmethod
    def from_json_column(cls, data: dict[str, Any]) -> "WorkInProgressState":
        """Deserialise from a PostgreSQL JSONB column."""
        return cls.model_validate(data)

    def get(self, var_name: str, default: Any = None) -> Any:
        """Convenience accessor — mirrors dict.get() on active_variable_map."""
        return self.active_variable_map.get(var_name, default)

    def with_updated_timestamp(self) -> "WorkInProgressState":
        """Return a copy with last_seen_at refreshed to now."""
        return self.model_copy(update={"last_seen_at": datetime.now(timezone.utc)})


# ─── Batch state (one session, many questions) ───────────────────────────────

class SessionVariableSnapshot(BaseModel):
    """
    Full snapshot of all question states in a paused session.
    Stored in practice_sessions.paused_state (JSONB).
    """
    model_config = {"populate_by_name": True}

    session_id: int
    exam_code: str
    question_index: int = Field(ge=0, description="Which question the student was on when pausing")
    question_ids: list[int] = Field(description="Ordered list of question IDs for this session")

    # Map from str(question_id) → WorkInProgressState
    # Keyed as strings because JSON object keys must be strings.
    states: dict[str, WorkInProgressState] = Field(
        default_factory=dict,
        description="Per-question WIP states, keyed by str(question_id).",
    )

    paused_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def get_state(self, question_id: int) -> Optional[WorkInProgressState]:
        return self.states.get(str(question_id))

    def set_state(self, question_id: int, state: WorkInProgressState) -> None:
        self.states[str(question_id)] = state

    @property
    def current_question_id(self) -> Optional[int]:
        if self.question_index < len(self.question_ids):
            return self.question_ids[self.question_index]
        return None

    @property
    def current_state(self) -> Optional[WorkInProgressState]:
        qid = self.current_question_id
        return self.get_state(qid) if qid is not None else None

    def to_json_column(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())

    @classmethod
    def from_json_column(cls, data: dict[str, Any]) -> "SessionVariableSnapshot":
        return cls.model_validate(data)
