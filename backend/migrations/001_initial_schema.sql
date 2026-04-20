-- ============================================================================
-- ActuarialPrep Platform — PostgreSQL Schema
-- Migration 001: Initial Schema with Earned Level System
-- ============================================================================
-- Run: psql -U actuarialprep -d actuarialprep -f 001_initial_schema.sql
-- ============================================================================

BEGIN;

-- ---------------------------------------------------------------------------
-- 1. EXTENSIONS
-- ---------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ---------------------------------------------------------------------------
-- 2. ENUM TYPES
-- ---------------------------------------------------------------------------
CREATE TYPE user_role AS ENUM ('student', 'admin', 'content_creator');
CREATE TYPE exam_code AS ENUM ('P', 'FM', 'FAM', 'ALTAM', 'ASTAM', 'SRM', 'PA');
CREATE TYPE session_type AS ENUM ('adaptive', 'topic_quiz', 'timed_exam');

-- ---------------------------------------------------------------------------
-- 3. USERS
-- ---------------------------------------------------------------------------
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255)  NOT NULL UNIQUE,
    hashed_password VARCHAR(255)  NOT NULL,
    full_name       VARCHAR(255),
    role            user_role     NOT NULL DEFAULT 'student',
    is_active       BOOLEAN       NOT NULL DEFAULT TRUE,
    is_verified     BOOLEAN       NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_users_email ON users (email);
CREATE INDEX ix_users_role  ON users (role);

-- ---------------------------------------------------------------------------
-- 4. EXAMS
-- ---------------------------------------------------------------------------
CREATE TABLE exams (
    id                  SERIAL PRIMARY KEY,
    code                VARCHAR(10)   NOT NULL UNIQUE,
    name                VARCHAR(255)  NOT NULL,
    description         TEXT,
    total_questions     INT           NOT NULL DEFAULT 30,
    time_limit_minutes  INT           NOT NULL DEFAULT 180,
    passing_score       FLOAT         NOT NULL DEFAULT 70.0,
    is_active           BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_exams_code ON exams (code);

-- Seed the 7 SOA exams
INSERT INTO exams (code, name, description, total_questions, time_limit_minutes, passing_score) VALUES
('P',     'Probability',                          'Probability and statistics fundamentals',                       30, 180, 70.0),
('FM',    'Financial Mathematics',                 'Time value of money, annuities, bonds, yield curves',           35, 180, 70.0),
('FAM',   'Fundamentals of Actuarial Mathematics', 'Long-term and short-term actuarial models',                     40, 210, 70.0),
('ALTAM', 'Advanced Long-Term Actuarial Math',     'Multi-state, multiple life, pension, profit testing',           30, 210, 70.0),
('ASTAM', 'Advanced Short-Term Actuarial Math',    'Severity, frequency, aggregate, credibility, ruin theory',      30, 210, 70.0),
('SRM',   'Statistics for Risk Modeling',          'Regression, GLMs, time series, machine learning, PCA',          35, 210, 70.0),
('PA',    'Predictive Analytics',                  'EDA, feature engineering, model building, communication',       30, 315, 70.0);

-- ---------------------------------------------------------------------------
-- 5. TOPICS  (exam subsections with syllabus weights)
-- ---------------------------------------------------------------------------
CREATE TABLE topics (
    id                  SERIAL PRIMARY KEY,
    exam_id             INT           NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    name                VARCHAR(255)  NOT NULL,
    description         TEXT,
    weight              FLOAT         NOT NULL DEFAULT 0.0,   -- syllabus weight (0–1)
    learning_objectives JSONB,
    sort_order          INT           NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_topics_exam_id ON topics (exam_id);
CREATE UNIQUE INDEX ix_topics_exam_name ON topics (exam_id, name);

-- ---------------------------------------------------------------------------
-- 6. QUESTION TEMPLATES  (parameterised, LaTeX-ready)
--    variables_config stores ranges for random parameters.
--    template_text and solution_template use LaTeX notation:
--      e.g.  "Find $\\ddot{a}_{\\anmark{n}{i}}$ where $n = {{n}}$ and $i = {{i}}$."
-- ---------------------------------------------------------------------------
CREATE TABLE question_templates (
    id                    SERIAL PRIMARY KEY,
    topic_id              INT           NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    difficulty_level      FLOAT         NOT NULL DEFAULT 5.0   -- continuous 1.0–10.0 (IRT b)
        CHECK (difficulty_level >= 1.0 AND difficulty_level <= 10.0),
    irt_discrimination    FLOAT         NOT NULL DEFAULT 1.0   -- IRT a ∈ (0, 3]
        CHECK (irt_discrimination > 0 AND irt_discrimination <= 3.0),
    irt_guessing          FLOAT         NOT NULL DEFAULT 0.2   -- IRT c ∈ [0, 0.5]
        CHECK (irt_guessing >= 0 AND irt_guessing <= 0.5),

    -- LaTeX-capable templates with {{variable}} placeholders
    template_text         TEXT          NOT NULL,               -- question body (LaTeX)
    solution_template     TEXT          NOT NULL,               -- step-by-step solution (LaTeX)
    explanation_template  TEXT,                                  -- short conceptual note

    -- JSONB config for random variable generation
    -- Example: {"n": {"type": "int", "min": 5, "max": 30},
    --           "i": {"type": "float", "min": 0.02, "max": 0.12, "decimals": 4}}
    variables_config      JSONB         NOT NULL DEFAULT '{}',

    -- How to build wrong answers
    -- Example: {"method": "perturbation", "offsets": [-0.05, 0.03, 0.08, -0.02]}
    distractor_config     JSONB         NOT NULL DEFAULT '{}',

    tags                  TEXT[]        DEFAULT '{}',
    is_active             BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at            TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_qt_topic_id    ON question_templates (topic_id);
CREATE INDEX ix_qt_difficulty   ON question_templates (difficulty_level);
CREATE INDEX ix_qt_tags         ON question_templates USING gin (tags);

-- ---------------------------------------------------------------------------
-- 7. QUESTIONS  (rendered instances of templates)
-- ---------------------------------------------------------------------------
CREATE TABLE questions (
    id                    SERIAL PRIMARY KEY,
    template_id           INT           NOT NULL REFERENCES question_templates(id) ON DELETE CASCADE,
    rendered_text         TEXT          NOT NULL,     -- final text with variables substituted (LaTeX)
    choices               JSONB         NOT NULL,     -- [{"label":"A","text":"$1{,}234$","is_correct":false}, ...]
    correct_index         SMALLINT      NOT NULL,     -- 0-based index of correct choice
    rendered_solution     TEXT          NOT NULL,     -- final step-by-step (LaTeX)
    rendered_explanation  TEXT,
    variables_used        JSONB,                       -- {"n": 10, "i": 0.05} snapshot
    difficulty            FLOAT         NOT NULL,
    irt_discrimination    FLOAT,
    irt_difficulty        FLOAT,                       -- calibrated b on θ-scale (−4…+4)
    irt_guessing          FLOAT,
    created_at            TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_q_template_id  ON questions (template_id);
CREATE INDEX ix_q_difficulty    ON questions (difficulty);

-- ---------------------------------------------------------------------------
-- 8. USER EARNED LEVEL  (the core "ADAPT-style" EL tracker)
--    One row per (user, exam).  earned_level is a continuous value (0.0–10.0)
--    that rises/falls with quiz results, analogous to an Elo rating.
-- ---------------------------------------------------------------------------
CREATE TABLE user_earned_levels (
    id              SERIAL PRIMARY KEY,
    user_id         INT           NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exam_id         INT           NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    earned_level    FLOAT         NOT NULL DEFAULT 0.0
        CHECK (earned_level >= 0.0 AND earned_level <= 10.0),
    peak_level      FLOAT         NOT NULL DEFAULT 0.0,
    total_quizzes   INT           NOT NULL DEFAULT 0,
    total_correct   INT           NOT NULL DEFAULT 0,
    total_attempted INT           NOT NULL DEFAULT 0,
    streak          INT           NOT NULL DEFAULT 0,    -- consecutive quizzes passed
    last_quiz_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, exam_id)
);

CREATE INDEX ix_uel_user_id  ON user_earned_levels (user_id);
CREATE INDEX ix_uel_exam_id  ON user_earned_levels (exam_id);

-- ---------------------------------------------------------------------------
-- 9. ADAPTIVE STATE  (topic-level mastery via BKT)
-- ---------------------------------------------------------------------------
CREATE TABLE adaptive_states (
    id              SERIAL PRIMARY KEY,
    user_id         INT           NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exam_id         INT           NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    topic_mastery   JSONB         NOT NULL DEFAULT '{}',   -- {topic_id: mastery_float}
    overall_ability FLOAT         NOT NULL DEFAULT 0.0,    -- EAP θ estimate (−4…+4)
    readiness_score FLOAT         NOT NULL DEFAULT 0.0,    -- 0–100
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, exam_id)
);

CREATE INDEX ix_as_user_exam ON adaptive_states (user_id, exam_id);

-- ---------------------------------------------------------------------------
-- 10. PRACTICE SESSIONS
-- ---------------------------------------------------------------------------
CREATE TABLE practice_sessions (
    id                SERIAL PRIMARY KEY,
    user_id           INT            NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    exam_id           INT            NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
    session_type      session_type   NOT NULL DEFAULT 'adaptive',
    quiz_level        FLOAT,                               -- difficulty level of this quiz
    started_at        TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    ended_at          TIMESTAMPTZ,
    total_questions   INT            NOT NULL DEFAULT 0,
    correct_answers   INT            NOT NULL DEFAULT 0,
    score             FLOAT,                               -- percent
    el_before         FLOAT,                               -- EL snapshot before quiz
    el_after          FLOAT,                               -- EL snapshot after quiz
    created_at        TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ    NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_ps_user_exam ON practice_sessions (user_id, exam_id);
CREATE INDEX ix_ps_started   ON practice_sessions (started_at DESC);

-- ---------------------------------------------------------------------------
-- 11. USER PERFORMANCE  (per-question attempt log)
-- ---------------------------------------------------------------------------
CREATE TABLE user_performance (
    id                 SERIAL PRIMARY KEY,
    user_id            INT           NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id        INT           NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    session_id         INT           NOT NULL REFERENCES practice_sessions(id) ON DELETE CASCADE,
    is_correct         BOOLEAN       NOT NULL,
    selected_choice    SMALLINT      NOT NULL,
    time_spent_seconds INT           NOT NULL DEFAULT 0,
    answered_at        TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_up_user_id     ON user_performance (user_id);
CREATE INDEX ix_up_session_id  ON user_performance (session_id);
CREATE INDEX ix_up_question_id ON user_performance (question_id);

-- ---------------------------------------------------------------------------
-- 12. TOPIC MASTERY HISTORY  (for time-series analytics)
-- ---------------------------------------------------------------------------
CREATE TABLE topic_mastery_history (
    id          SERIAL PRIMARY KEY,
    user_id     INT           NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id    INT           NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    mastery     FLOAT         NOT NULL,
    recorded_at TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_tmh_user_topic ON topic_mastery_history (user_id, topic_id, recorded_at DESC);

-- ---------------------------------------------------------------------------
-- 13. VIDEO LESSONS
-- ---------------------------------------------------------------------------
CREATE TABLE video_lessons (
    id          SERIAL PRIMARY KEY,
    topic_id    INT           NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    title       VARCHAR(255)  NOT NULL,
    description TEXT,
    video_url   VARCHAR(512),
    duration    INT           NOT NULL DEFAULT 0,  -- seconds
    sort_order  INT           NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_vl_topic_id ON video_lessons (topic_id);

-- ---------------------------------------------------------------------------
-- 14. HELPER: auto-update updated_at
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to all mutable tables
DO $$
DECLARE
    tbl TEXT;
BEGIN
    FOREACH tbl IN ARRAY ARRAY[
        'users', 'exams', 'topics', 'question_templates',
        'user_earned_levels', 'adaptive_states', 'practice_sessions'
    ]
    LOOP
        EXECUTE format(
            'CREATE TRIGGER set_timestamp BEFORE UPDATE ON %I
             FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp()',
            tbl
        );
    END LOOP;
END;
$$;

COMMIT;
