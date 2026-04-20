-- Migration 002: Intelligent Content Layer
-- Adds pause/resume state, VideoClip sub-table, tutor fields, and session status.
-- Run after 001_initial_schema.sql

BEGIN;

-- ─── 1. Session pause / resume ───────────────────────────────────────────────

ALTER TABLE practice_sessions
    ADD COLUMN IF NOT EXISTS status          VARCHAR(20)  NOT NULL DEFAULT 'active'
        CHECK (status IN ('active','paused','completed')),
    ADD COLUMN IF NOT EXISTS paused_at       TIMESTAMPTZ,
    ADD COLUMN IF NOT EXISTS paused_state    JSONB;

-- paused_state shape:
-- {
--   "question_index": 3,
--   "question_ids": [42, 17, 88, 5, ...],
--   "variables_by_question": {
--       "42": {"n": 10, "i": 0.06, "P": 500.0},
--       "17": {"lambda": 2.3}
--   }
-- }

CREATE INDEX IF NOT EXISTS ix_practice_sessions_status
    ON practice_sessions (status);
CREATE INDEX IF NOT EXISTS ix_practice_sessions_paused
    ON practice_sessions (user_id, status)
    WHERE status = 'paused';

-- Back-fill existing rows
UPDATE practice_sessions
SET status = CASE
    WHEN ended_at IS NOT NULL THEN 'completed'
    ELSE 'active'
END
WHERE status = 'active';


-- ─── 2. Store randomised variables per attempt ───────────────────────────────

ALTER TABLE user_performance
    ADD COLUMN IF NOT EXISTS randomised_variables JSONB,
    ADD COLUMN IF NOT EXISTS template_id           INT
        REFERENCES question_templates(id) ON DELETE SET NULL;

-- question_templates table (if not yet created by migration 001)
CREATE TABLE IF NOT EXISTS question_templates (
    id               SERIAL PRIMARY KEY,
    exam_code        VARCHAR(10) NOT NULL,
    topic_id         INT REFERENCES topics(id) ON DELETE CASCADE,
    template_text    TEXT NOT NULL,
    variables_config JSONB NOT NULL DEFAULT '{}',
    solution_steps   JSONB NOT NULL DEFAULT '[]',
    difficulty_min   SMALLINT NOT NULL DEFAULT 1 CHECK (difficulty_min BETWEEN 1 AND 10),
    difficulty_max   SMALLINT NOT NULL DEFAULT 10 CHECK (difficulty_max BETWEEN 1 AND 10),
    tags             TEXT[],
    is_active        BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_question_templates_exam
    ON question_templates (exam_code);
CREATE INDEX IF NOT EXISTS ix_question_templates_topic
    ON question_templates (topic_id);


-- ─── 3. VideoClip sub-table ───────────────────────────────────────────────────

-- Add YouTube ID columns to the parent VideoLesson table
ALTER TABLE video_lessons
    ADD COLUMN IF NOT EXISTS youtube_video_id VARCHAR(20),
    ADD COLUMN IF NOT EXISTS channel_name     VARCHAR(120);

CREATE TABLE IF NOT EXISTS video_clips (
    id               SERIAL PRIMARY KEY,
    lesson_id        INT NOT NULL REFERENCES video_lessons(id) ON DELETE CASCADE,
    topic_id         INT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    title            VARCHAR(255) NOT NULL,
    description      TEXT,
    start_seconds    INT NOT NULL DEFAULT 0,
    end_seconds      INT NOT NULL,
    min_difficulty   SMALLINT NOT NULL DEFAULT 1,
    max_difficulty   SMALLINT NOT NULL DEFAULT 10,
    concept_tags     TEXT[],
    relevance_score  NUMERIC(4,3) NOT NULL DEFAULT 1.0,
    is_published     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT ck_clip_timestamps CHECK (end_seconds > start_seconds)
);

CREATE INDEX IF NOT EXISTS ix_video_clips_lesson_id  ON video_clips (lesson_id);
CREATE INDEX IF NOT EXISTS ix_video_clips_topic_id   ON video_clips (topic_id);
CREATE INDEX IF NOT EXISTS ix_video_clips_difficulty ON video_clips (min_difficulty, max_difficulty);
CREATE INDEX IF NOT EXISTS ix_video_clips_published  ON video_clips (is_published) WHERE is_published;


-- ─── 4. Questions: add tutor/template fields ─────────────────────────────────

ALTER TABLE questions
    ADD COLUMN IF NOT EXISTS template_text       TEXT,
    ADD COLUMN IF NOT EXISTS solution            JSONB,   -- {calculation, concept}
    ADD COLUMN IF NOT EXISTS common_mistakes     TEXT[],
    ADD COLUMN IF NOT EXISTS correct_answer_label VARCHAR(2),
    ADD COLUMN IF NOT EXISTS correct_answer_text  TEXT,
    ADD COLUMN IF NOT EXISTS exam_code           VARCHAR(10),
    ADD COLUMN IF NOT EXISTS topic_name          TEXT;


-- ─── 5. Auto-update updated_at ───────────────────────────────────────────────

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

DO $$
DECLARE tbl TEXT;
BEGIN
    FOREACH tbl IN ARRAY ARRAY['question_templates','video_clips'] LOOP
        IF NOT EXISTS (
            SELECT 1 FROM pg_trigger
            WHERE tgname = 'trg_' || tbl || '_updated_at'
        ) THEN
            EXECUTE format(
                'CREATE TRIGGER trg_%I_updated_at
                 BEFORE UPDATE ON %I
                 FOR EACH ROW EXECUTE FUNCTION set_updated_at()',
                tbl, tbl
            );
        END IF;
    END LOOP;
END;
$$;

COMMIT;
