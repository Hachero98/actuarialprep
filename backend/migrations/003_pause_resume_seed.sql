-- Migration 003: Pause/Resume persistence + seed content columns
-- Adds random_seed, variable_values, template_id to user_performance.
-- Run after 002_content_layer.sql

BEGIN;

ALTER TABLE user_performance
    ADD COLUMN IF NOT EXISTS random_seed     VARCHAR(64),
    ADD COLUMN IF NOT EXISTS variable_values JSONB,
    ADD COLUMN IF NOT EXISTS template_id     INT
        REFERENCES question_templates(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS ix_user_performance_template
    ON user_performance (template_id);

CREATE INDEX IF NOT EXISTS ix_user_performance_session_question
    ON user_performance (session_id, question_id);

COMMENT ON COLUMN user_performance.random_seed IS
    'Hex token used to seed variable generation; stored so the same numbers '
    'are shown when a paused session is resumed.';

COMMENT ON COLUMN user_performance.variable_values IS
    'Resolved numeric values {var: value} for this attempt, rounded to 4 d.p. '
    'Guarantees question text is byte-for-byte identical on resume.';

COMMIT;
