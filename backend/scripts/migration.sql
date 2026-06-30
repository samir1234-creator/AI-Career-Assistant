-- AI Career Assistant - Database Migration SQL (Supabase PostgreSQL)
-- This script sets up tables in the public schema, triggers to sync auth.users, and Row Level Security (RLS) policies.

-- Enable UUID extension if not enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -------------------------------------------------------------
-- 1. Users & Profiles
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_login TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS public.user_profiles (
    user_id UUID PRIMARY KEY REFERENCES public.users(id) ON DELETE CASCADE,
    name TEXT,
    email TEXT NOT NULL,
    picture TEXT,
    joined_date TIMESTAMPTZ NOT NULL DEFAULT now(),
    current_career_goal TEXT,
    current_readiness_score INTEGER DEFAULT 0,
    current_roadmap_id UUID
);

-- -------------------------------------------------------------
-- 2. Resume History & Reports
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.resume_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    text_content TEXT NOT NULL,
    parsed_data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.ats_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    resume_id UUID NOT NULL REFERENCES public.resume_history(id) ON DELETE CASCADE,
    ats_score INTEGER NOT NULL,
    report_data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.career_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    resume_id UUID NOT NULL REFERENCES public.resume_history(id) ON DELETE CASCADE,
    recommendations JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.skill_gap_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    resume_id UUID NOT NULL REFERENCES public.resume_history(id) ON DELETE CASCADE,
    career_goal TEXT NOT NULL,
    matched_skills JSONB NOT NULL,
    missing_skills JSONB NOT NULL,
    priority_ranking JSONB NOT NULL,
    readiness_score INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -------------------------------------------------------------
-- 3. Learning Roadmaps
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.learning_roadmaps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    resume_id UUID REFERENCES public.resume_history(id) ON DELETE SET NULL,
    career TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    total_weeks INTEGER NOT NULL,
    total_months INTEGER NOT NULL,
    expected_readiness INTEGER NOT NULL,
    job_market JSONB NOT NULL DEFAULT '{}'::jsonb,
    career_forecast JSONB NOT NULL DEFAULT '{}'::jsonb,
    matched_skills JSONB NOT NULL DEFAULT '[]'::jsonb,
    missing_skills JSONB NOT NULL DEFAULT '[]'::jsonb,
    monthly_roadmap JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Add reference in user_profiles to active roadmap
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'fk_user_profiles_current_roadmap'
    ) THEN
        ALTER TABLE public.user_profiles 
            ADD CONSTRAINT fk_user_profiles_current_roadmap 
            FOREIGN KEY (current_roadmap_id) REFERENCES public.learning_roadmaps(id) ON DELETE SET NULL;
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS public.roadmap_milestones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roadmap_id UUID NOT NULL REFERENCES public.learning_roadmaps(id) ON DELETE CASCADE,
    milestone_index INTEGER NOT NULL,
    title TEXT NOT NULL,
    skills JSONB NOT NULL DEFAULT '[]'::jsonb,
    complete BOOLEAN NOT NULL DEFAULT FALSE,
    resources JSONB NOT NULL DEFAULT '[]'::jsonb,
    projects JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.roadmap_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roadmap_id UUID NOT NULL REFERENCES public.learning_roadmaps(id) ON DELETE CASCADE,
    week_number INTEGER NOT NULL,
    month_number INTEGER NOT NULL,
    task_id TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Not Started', -- Not Started, In Progress, Completed, Skipped
    type TEXT NOT NULL DEFAULT 'Learn', -- Practice, Assignment, Quiz, Learn
    description TEXT,
    estimated_hours INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -------------------------------------------------------------
-- 4. User Progress, Badges & Achievements
-- -------------------------------------------------------------

CREATE TABLE IF NOT EXISTS public.user_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    roadmap_id UUID NOT NULL REFERENCES public.learning_roadmaps(id) ON DELETE CASCADE,
    completed_skills JSONB NOT NULL DEFAULT '[]'::jsonb,
    completed_tasks JSONB NOT NULL DEFAULT '[]'::jsonb,
    completed_weeks JSONB NOT NULL DEFAULT '[]'::jsonb,
    completed_months JSONB NOT NULL DEFAULT '[]'::jsonb,
    completed_milestones JSONB NOT NULL DEFAULT '[]'::jsonb,
    completed_projects JSONB NOT NULL DEFAULT '[]'::jsonb,
    current_readiness INTEGER DEFAULT 0,
    current_roadmap_completion NUMERIC(5,2) DEFAULT 0.00,
    last_activity TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(user_id, roadmap_id)
);

CREATE TABLE IF NOT EXISTS public.badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    badge_id TEXT NOT NULL,
    name TEXT NOT NULL,
    emoji TEXT NOT NULL,
    color TEXT NOT NULL,
    description TEXT NOT NULL,
    unlock_condition TEXT NOT NULL,
    unlocked_date TIMESTAMPTZ,
    progress TEXT NOT NULL DEFAULT '0/1',
    requirements JSONB,
    UNIQUE(user_id, badge_id)
);

CREATE TABLE IF NOT EXISTS public.achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    achievement_id TEXT NOT NULL,
    name TEXT NOT NULL,
    unlocked_date TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(user_id, achievement_id)
);

CREATE TABLE IF NOT EXISTS public.analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roadmap_id UUID NOT NULL REFERENCES public.learning_roadmaps(id) ON DELETE CASCADE,
    current_readiness INTEGER NOT NULL,
    projected_readiness INTEGER NOT NULL,
    roadmap_completion NUMERIC(5,2) NOT NULL,
    success_probability INTEGER NOT NULL,
    skills_acquired JSONB NOT NULL DEFAULT '[]'::jsonb,
    career_growth JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -------------------------------------------------------------
-- 5. Trigger to Automatically Sync Auth Users
-- -------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  -- Insert into public.users
  INSERT INTO public.users (id, email, created_at, last_login)
  VALUES (new.id, new.email, new.created_at, new.created_at)
  ON CONFLICT (id) DO NOTHING;

  -- Insert into public.user_profiles
  INSERT INTO public.user_profiles (user_id, email, name, picture, joined_date)
  VALUES (
    new.id, 
    new.email, 
    coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name', 'SaaS User'), 
    coalesce(new.raw_user_meta_data->>'avatar_url', new.raw_user_meta_data->>'picture', 'https://lh3.googleusercontent.com/a/default-user'),
    new.created_at
  )
  ON CONFLICT (user_id) DO NOTHING;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Drop trigger if exists
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Create the trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- -------------------------------------------------------------
-- 6. Enable Row Level Security (RLS) & Policies
-- -------------------------------------------------------------

-- Enable RLS on all tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.resume_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ats_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.career_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.skill_gap_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.learning_roadmaps ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.roadmap_milestones ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.roadmap_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.badges ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.analytics ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if any to avoid errors
DROP POLICY IF EXISTS "Users can read own record" ON public.users;
DROP POLICY IF EXISTS "Users can view own profile" ON public.user_profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON public.user_profiles;
DROP POLICY IF EXISTS "Users can manage own resumes" ON public.resume_history;
DROP POLICY IF EXISTS "Users can manage own ats reports" ON public.ats_reports;
DROP POLICY IF EXISTS "Users can manage own recommendations" ON public.career_recommendations;
DROP POLICY IF EXISTS "Users can manage own skill gap reports" ON public.skill_gap_reports;
DROP POLICY IF EXISTS "Users can manage own roadmaps" ON public.learning_roadmaps;
DROP POLICY IF EXISTS "Users can view milestones of own roadmaps" ON public.roadmap_milestones;
DROP POLICY IF EXISTS "Users can manage tasks of own roadmaps" ON public.roadmap_tasks;
DROP POLICY IF EXISTS "Users can manage own progress" ON public.user_progress;
DROP POLICY IF EXISTS "Users can manage own badges" ON public.badges;
DROP POLICY IF EXISTS "Users can manage own achievements" ON public.achievements;
DROP POLICY IF EXISTS "Users can view analytics of own roadmaps" ON public.analytics;

-- Define Policies
CREATE POLICY "Users can read own record" ON public.users FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can view own profile" ON public.user_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own profile" ON public.user_profiles FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own resumes" ON public.resume_history FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own ats reports" ON public.ats_reports FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own recommendations" ON public.career_recommendations FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own skill gap reports" ON public.skill_gap_reports FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own roadmaps" ON public.learning_roadmaps FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view milestones of own roadmaps" ON public.roadmap_milestones FOR ALL USING (
    EXISTS (
        SELECT 1 FROM public.learning_roadmaps r 
        WHERE r.id = roadmap_milestones.roadmap_id 
        AND r.user_id = auth.uid()
    )
);

CREATE POLICY "Users can manage tasks of own roadmaps" ON public.roadmap_tasks FOR ALL USING (
    EXISTS (
        SELECT 1 FROM public.learning_roadmaps r 
        WHERE r.id = roadmap_tasks.roadmap_id 
        AND r.user_id = auth.uid()
    )
);

CREATE POLICY "Users can manage own progress" ON public.user_progress FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own badges" ON public.badges FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own achievements" ON public.achievements FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users can view analytics of own roadmaps" ON public.analytics FOR ALL USING (
    EXISTS (
        SELECT 1 FROM public.learning_roadmaps r 
        WHERE r.id = analytics.roadmap_id 
        AND r.user_id = auth.uid()
    )
);
