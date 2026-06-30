-- Migration Phase 8: AI Interview Preparation & Career Coach Tables

CREATE TABLE IF NOT EXISTS public.interview_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    type TEXT NOT NULL, -- "Mock", "Resume-Based", "Technical", "HR", "Behavioral STAR", "Coding", "Company-Specific"
    company TEXT, -- Google, Microsoft, Amazon, etc. (optional)
    status TEXT NOT NULL DEFAULT 'In Progress', -- In Progress, Completed
    overall_score NUMERIC(5,2),
    strengths JSONB DEFAULT '[]'::jsonb,
    weaknesses JSONB DEFAULT '[]'::jsonb,
    missing_topics JSONB DEFAULT '[]'::jsonb,
    revision_concepts JSONB DEFAULT '[]'::jsonb,
    recommended_resources JSONB DEFAULT '[]'::jsonb,
    practice_problems JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS public.interview_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES public.interview_sessions(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    type TEXT NOT NULL, -- "Technical", "HR", "STAR", "Resume", "Coding"
    difficulty TEXT NOT NULL,
    code_template TEXT, -- for coding tasks
    solution_code TEXT, -- for coding tasks
    test_cases JSONB, -- list of inputs/outputs for coding tasks
    user_answer TEXT,
    is_evaluated BOOLEAN NOT NULL DEFAULT FALSE,
    score INTEGER,
    feedback_technical_accuracy TEXT,
    feedback_communication TEXT,
    feedback_grammar TEXT,
    feedback_confidence TEXT,
    feedback_completeness TEXT,
    feedback_professionalism TEXT,
    overall_rating TEXT,
    improvement_suggestions TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.interview_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.interview_questions ENABLE ROW LEVEL SECURITY;

-- Create Policies (Select, Insert, Update, Delete)
DROP POLICY IF EXISTS "Users can manage own interview sessions" ON public.interview_sessions;
CREATE POLICY "Users can manage own interview sessions" ON public.interview_sessions FOR ALL USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can manage own interview questions" ON public.interview_questions;
CREATE POLICY "Users can manage own interview questions" ON public.interview_questions FOR ALL USING (
    EXISTS (
        SELECT 1 FROM public.interview_sessions s 
        WHERE s.id = interview_questions.session_id 
        AND s.user_id = auth.uid()
    )
);
