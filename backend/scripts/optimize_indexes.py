import os
import sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Load environment variables
BACKEND_DIR = Path(__file__).resolve().parent.parent
env_path = BACKEND_DIR / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

def apply_indexes():
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL not configured.")
        sys.exit(1)
        
    print("Connecting to Supabase PostgreSQL database to configure performance indexes...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        with conn.cursor() as cur:
            queries = [
                "CREATE INDEX IF NOT EXISTS idx_users_firebase_uid ON public.users(firebase_uid);",
                "CREATE INDEX IF NOT EXISTS idx_resume_history_user_id ON public.resume_history(user_id);",
                "CREATE INDEX IF NOT EXISTS idx_resume_history_created_at ON public.resume_history(created_at DESC);",
                "CREATE INDEX IF NOT EXISTS idx_ats_reports_resume_id ON public.ats_reports(resume_id);",
                "CREATE INDEX IF NOT EXISTS idx_career_recs_resume_id ON public.career_recommendations(resume_id);",
                "CREATE INDEX IF NOT EXISTS idx_roadmaps_user_id ON public.learning_roadmaps(user_id);",
                "CREATE INDEX IF NOT EXISTS idx_roadmaps_created_at ON public.learning_roadmaps(created_at DESC);",
                "CREATE INDEX IF NOT EXISTS idx_milestones_roadmap_id ON public.roadmap_milestones(roadmap_id);",
                "CREATE INDEX IF NOT EXISTS idx_tasks_roadmap_id ON public.roadmap_tasks(roadmap_id);",
                "CREATE INDEX IF NOT EXISTS idx_progress_user_roadmap ON public.user_progress(user_id, roadmap_id);",
                "CREATE INDEX IF NOT EXISTS idx_badges_user_id ON public.badges(user_id);",
                "CREATE INDEX IF NOT EXISTS idx_achievements_user_id ON public.achievements(user_id);",
                "CREATE INDEX IF NOT EXISTS idx_analytics_roadmap_id ON public.analytics(roadmap_id);"
            ]
            
            for q in queries:
                print(f"Executing: {q}")
                cur.execute(q)
                
            print("Successfully configured all performance indexes!")
        conn.close()
    except Exception as e:
        print(f"Index creation failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    apply_indexes()
