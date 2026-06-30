-- Migration Script: Phase 7.6 - Resume History Optimization & Roadmap Task Tracking

-- 1. Drop existing resume_history table (CASCADE drops referencing FK constraints)
DROP TABLE IF EXISTS public.resume_history CASCADE;

-- 2. Create the new current_resume table
CREATE TABLE IF NOT EXISTS public.current_resume (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    resume_file_url TEXT NOT NULL,
    resume_text TEXT NOT NULL,
    ats_score INTEGER,
    career_goal TEXT,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3. Restore Foreign Key constraints on dependent tables
ALTER TABLE public.ats_reports 
    ADD CONSTRAINT ats_reports_resume_id_fkey 
    FOREIGN KEY (resume_id) REFERENCES public.current_resume(id) ON DELETE CASCADE;

ALTER TABLE public.career_recommendations 
    ADD CONSTRAINT career_recommendations_resume_id_fkey 
    FOREIGN KEY (resume_id) REFERENCES public.current_resume(id) ON DELETE CASCADE;

ALTER TABLE public.skill_gap_reports 
    ADD CONSTRAINT skill_gap_reports_resume_id_fkey 
    FOREIGN KEY (resume_id) REFERENCES public.current_resume(id) ON DELETE CASCADE;

ALTER TABLE public.learning_roadmaps 
    ADD CONSTRAINT learning_roadmaps_resume_id_fkey 
    FOREIGN KEY (resume_id) REFERENCES public.current_resume(id) ON DELETE SET NULL;

-- 4. Create roadmap_task_progress table
CREATE TABLE IF NOT EXISTS public.roadmap_task_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    roadmap_id UUID NOT NULL REFERENCES public.learning_roadmaps(id) ON DELETE CASCADE,
    milestone_id TEXT,
    task_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Not Started',
    completed_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(user_id, roadmap_id, task_id)
);

-- 5. Row Level Security Policies
ALTER TABLE public.current_resume ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own resume" ON public.current_resume FOR ALL USING (auth.uid() = user_id);

ALTER TABLE public.roadmap_task_progress ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can manage own roadmap progress" ON public.roadmap_task_progress FOR ALL USING (auth.uid() = user_id);

-- 6. Trigger for updated_at on current_resume
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = now(); 
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_current_resume_modtime
BEFORE UPDATE ON public.current_resume
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

CREATE TRIGGER update_roadmap_task_progress_modtime
BEFORE UPDATE ON public.roadmap_task_progress
FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
