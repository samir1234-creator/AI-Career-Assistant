-- ============================================================
-- Phase 8: AI Interview Preparation Platform
-- Migration: Create interview-related tables
-- ============================================================

-- Interview Sessions: one row per interview attempt
CREATE TABLE IF NOT EXISTS public.interview_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    interview_type  VARCHAR(50) NOT NULL,   -- mock | resume | technical | hr | behavioral | coding | company
    role            VARCHAR(100),
    difficulty      VARCHAR(20),            -- Beginner | Intermediate | Advanced | Expert
    company         VARCHAR(100),
    topics          JSONB DEFAULT '[]',     -- list of topics selected
    status          VARCHAR(20) DEFAULT 'in_progress',  -- in_progress | completed | abandoned
    overall_score   FLOAT DEFAULT 0,
    total_questions INTEGER DEFAULT 0,
    answered_count  INTEGER DEFAULT 0,
    started_at      TIMESTAMPTZ DEFAULT now(),
    completed_at    TIMESTAMPTZ,
    duration_seconds INTEGER,
    metadata        JSONB DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_interview_sessions_user_id ON public.interview_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_interview_sessions_type ON public.interview_sessions(interview_type);
CREATE INDEX IF NOT EXISTS idx_interview_sessions_started_at ON public.interview_sessions(started_at DESC);

-- Interview Answers: one row per Q&A pair within a session
CREATE TABLE IF NOT EXISTS public.interview_answers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES public.interview_sessions(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    question_index  INTEGER NOT NULL,
    question_text   TEXT NOT NULL,
    question_type   VARCHAR(50),            -- technical | hr | behavioral | coding
    answer_text     TEXT DEFAULT '',
    time_taken_secs INTEGER DEFAULT 0,
    scores          JSONB DEFAULT '{}',     -- { technical_accuracy, communication, grammar, confidence, completeness, professionalism, overall }
    feedback        JSONB DEFAULT '{}',     -- { strengths, improvements, suggestions, missing_topics }
    evaluated       BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_interview_answers_session_id ON public.interview_answers(session_id);
CREATE INDEX IF NOT EXISTS idx_interview_answers_user_id ON public.interview_answers(user_id);

-- Career Coach Messages: conversation history
CREATE TABLE IF NOT EXISTS public.career_coach_messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    message         TEXT NOT NULL,
    response        TEXT NOT NULL,
    context_used    JSONB DEFAULT '{}',     -- snapshot of context (resume, ats_score, etc.)
    tokens_used     INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_career_coach_user_id ON public.career_coach_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_career_coach_created_at ON public.career_coach_messages(created_at DESC);

-- Interview Badges: gamification awards
CREATE TABLE IF NOT EXISTS public.interview_badges (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    badge_id        VARCHAR(100) NOT NULL,
    name            VARCHAR(200) NOT NULL,
    emoji           VARCHAR(10),
    color           VARCHAR(20),
    description     TEXT,
    awarded_at      TIMESTAMPTZ DEFAULT now(),
    UNIQUE(user_id, badge_id)
);

CREATE INDEX IF NOT EXISTS idx_interview_badges_user_id ON public.interview_badges(user_id);

-- ============================================================
-- Helper view: interview stats per user
-- ============================================================
CREATE OR REPLACE VIEW public.user_interview_stats AS
SELECT
    user_id,
    COUNT(*) FILTER (WHERE status = 'completed')                       AS total_completed,
    ROUND(AVG(overall_score) FILTER (WHERE status = 'completed')::numeric, 1) AS avg_score,
    MAX(overall_score) FILTER (WHERE status = 'completed')             AS best_score,
    COUNT(*) FILTER (WHERE interview_type = 'technical' AND status = 'completed') AS technical_count,
    COUNT(*) FILTER (WHERE interview_type = 'hr' AND status = 'completed')        AS hr_count,
    COUNT(*) FILTER (WHERE interview_type = 'coding' AND status = 'completed')    AS coding_count,
    COUNT(*) FILTER (WHERE interview_type = 'behavioral' AND status = 'completed') AS behavioral_count,
    MAX(started_at)                                                     AS last_interview_at
FROM public.interview_sessions
GROUP BY user_id;

