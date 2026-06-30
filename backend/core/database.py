import os
import json
from datetime import datetime
from contextlib import contextmanager
from typing import Dict, Any, List, Optional, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from psycopg2.pool import ThreadedConnectionPool
from core.config import settings

# Global connection pool
_pool = None

def get_pool():
    global _pool
    if _pool is None:
        try:
            # We connect to Supabase PostgreSQL using the pooler/direct URL
            _pool = ThreadedConnectionPool(1, 10, settings.DATABASE_URL)
        except Exception as e:
            print(f"ERROR: Failed to initialize PostgreSQL connection pool: {str(e)}")
            raise e
    return _pool

@contextmanager
def get_db_connection():
    """
    Context manager that yields a database connection from the pool.
    Commits automatically on success, rolls back on error.
    """
    pool = get_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        pool.putconn(conn)

def init_db():
    """
    Dummy init function to maintain compatibility.
    Database schemas, triggers, and RLS are created via SQL migration.
    """
    print("Database manager initialized with Supabase PostgreSQL connection pool.")

# -------------------------------------------------------------
# USER & PROFILE OPERATIONS
# -------------------------------------------------------------

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT u.id, u.email, u.created_at, u.last_login, u.firebase_uid,
                       p.name, p.picture, p.joined_date, p.current_career_goal,
                       p.current_readiness_score, p.current_roadmap_id
                FROM public.users u
                LEFT JOIN public.user_profiles p ON u.id = p.user_id
                WHERE u.id = %s;
            """, (user_id,))
            row = cur.fetchone()
            return dict(row) if row else None

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT u.id, u.email, u.created_at, u.last_login, u.firebase_uid,
                       p.name, p.picture, p.joined_date, p.current_career_goal,
                       p.current_readiness_score, p.current_roadmap_id
                FROM public.users u
                LEFT JOIN public.user_profiles p ON u.id = p.user_id
                WHERE u.email = %s;
            """, (email,))
            row = cur.fetchone()
            return dict(row) if row else None

def get_user_by_firebase_uid(firebase_uid: str) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT u.id, u.email, u.created_at, u.last_login, u.firebase_uid,
                       p.name, p.picture, p.joined_date, p.current_career_goal,
                       p.current_readiness_score, p.current_roadmap_id
                FROM public.users u
                LEFT JOIN public.user_profiles p ON u.id = p.user_id
                WHERE u.firebase_uid = %s;
            """, (firebase_uid,))
            row = cur.fetchone()
            return dict(row) if row else None

def create_user(email: str, name: str, picture: str, user_id: str, firebase_uid: Optional[str] = None) -> str:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.users (id, email, created_at, last_login, firebase_uid)
                VALUES (%s, %s, now(), now(), %s)
                ON CONFLICT (id) DO UPDATE SET last_login = now(), firebase_uid = EXCLUDED.firebase_uid;
            """, (user_id, email, firebase_uid))
            
            cur.execute("""
                INSERT INTO public.user_profiles (user_id, name, email, picture, joined_date)
                VALUES (%s, %s, %s, %s, now())
                ON CONFLICT (user_id) DO UPDATE SET name = %s, picture = %s;
            """, (user_id, name, email, picture, name, picture))

            # Pre-populate default locked badges to populate the dashboard for a new user
            badge_catalog = [
                {"id": "foundations",  "name": "Foundations Master",        "emoji": "🏗️", "color": "#60a5fa", "desc": "Completed the foundational milestone", "condition": "Complete Foundations milestone"},
                {"id": "ml_explorer",  "name": "Machine Learning Explorer", "emoji": "🤖", "color": "#a78bfa", "desc": "Mastered core Machine Learning concepts", "condition": "Complete Machine Learning milestone"},
                {"id": "dl_specialist", "name": "Deep Learning Specialist",  "emoji": "🧠", "color": "#f472b6", "desc": "Conquered Deep Learning and neural networks", "condition": "Complete Deep Learning milestone"},
                {"id": "nlp_expert",   "name": "NLP Practitioner",          "emoji": "📝", "color": "#34d399", "desc": "Achieved NLP and language model proficiency", "condition": "Complete NLP milestone"},
                {"id": "llm_builder",  "name": "LLM Builder",               "emoji": "💡", "color": "#fbbf24", "desc": "Built production-ready LLM applications", "condition": "Complete LLM milestone"},
                {"id": "cloud_guru",   "name": "Cloud Practitioner",        "emoji": "☁️", "color": "#38bdf8", "desc": "Deployed and managed cloud infrastructure", "condition": "Complete AWS/Cloud milestone"},
                {"id": "security_ace", "name": "Security Specialist",       "emoji": "🔐", "color": "#ef4444", "desc": "Mastered cybersecurity and ethical hacking", "condition": "Complete Security milestone"},
                {"id": "career_ready", "name": "Career Ready",              "emoji": "🚀", "color": "#10b981", "desc": "Completed the full career roadmap!", "condition": "Complete 100% of the roadmap"}
            ]
            for badge in badge_catalog:
                cur.execute("""
                    INSERT INTO public.badges (user_id, badge_id, name, emoji, color, description, unlock_condition, unlocked_date, progress)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, '0/1')
                    ON CONFLICT (user_id, badge_id) DO NOTHING;
                """, (user_id, badge["id"], badge["name"], badge["emoji"], badge["color"], badge["desc"], badge["condition"]))
    return user_id

def ensure_user_exists(
    firebase_uid: str,
    email: str,
    name: str,
    picture: str,
    db_uuid: str
) -> str:
    """
    Canonical, atomic user-existence guarantee.

    Resolution order:
      1. Lookup by firebase_uid (fastest - indexed)
      2. Lookup by deterministic UUID (db_uuid derived from firebase UID hash)
      3. Lookup by email (handles legacy / pre-Firebase accounts)
         → if found by email, link the Firebase UID to that account
      4. If none found → create users + user_profiles + default badges atomically

    Returns the resolved user_id (UUID string) that is safe for use in
    any FK-referencing INSERT statement.
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # ── Step 1: Lookup by firebase_uid ──────────────────────────────
            cur.execute(
                "SELECT id FROM public.users WHERE firebase_uid = %s LIMIT 1;",
                (firebase_uid,)
            )
            row = cur.fetchone()
            if row:
                cur.execute(
                    "UPDATE public.users SET last_login = now() WHERE id = %s;",
                    (row["id"],)
                )
                return str(row["id"])

            # ── Step 2: Lookup by deterministic UUID ────────────────────────
            cur.execute(
                "SELECT id FROM public.users WHERE id = %s LIMIT 1;",
                (db_uuid,)
            )
            row = cur.fetchone()
            if row:
                # Patch missing firebase_uid while we're here
                cur.execute(
                    "UPDATE public.users SET firebase_uid = %s, last_login = now() WHERE id = %s;",
                    (firebase_uid, row["id"])
                )
                return str(row["id"])

            # ── Step 3: Lookup by email (legacy link) ───────────────────────
            cur.execute(
                "SELECT id FROM public.users WHERE email = %s LIMIT 1;",
                (email,)
            )
            row = cur.fetchone()
            if row:
                existing_id = str(row["id"])
                cur.execute(
                    "UPDATE public.users SET firebase_uid = %s, last_login = now() WHERE id = %s;",
                    (firebase_uid, existing_id)
                )
                print(f"[ensure_user_exists] Linked firebase_uid to existing account for: {email}")
                return existing_id

            # ── Step 4: Create brand-new user (atomic) ──────────────────────
            cur.execute("""
                INSERT INTO public.users (id, email, created_at, last_login, firebase_uid)
                VALUES (%s, %s, now(), now(), %s)
                ON CONFLICT (id) DO UPDATE SET last_login = now(), firebase_uid = EXCLUDED.firebase_uid;
            """, (db_uuid, email, firebase_uid))

            cur.execute("""
                INSERT INTO public.user_profiles (user_id, name, email, picture, joined_date)
                VALUES (%s, %s, %s, %s, now())
                ON CONFLICT (user_id) DO UPDATE SET name = EXCLUDED.name, picture = EXCLUDED.picture;
            """, (db_uuid, name, email, picture))

            # Pre-populate default locked badges
            badge_catalog = [
                ("foundations",  "Foundations Master",        "🏗️", "#60a5fa", "Completed the foundational milestone",       "Complete Foundations milestone"),
                ("ml_explorer",  "Machine Learning Explorer", "🤖", "#a78bfa", "Mastered core Machine Learning concepts",     "Complete Machine Learning milestone"),
                ("dl_specialist","Deep Learning Specialist",  "🧠", "#f472b6", "Conquered Deep Learning and neural networks", "Complete Deep Learning milestone"),
                ("nlp_expert",   "NLP Practitioner",          "📝", "#34d399", "Achieved NLP and language model proficiency", "Complete NLP milestone"),
                ("llm_builder",  "LLM Builder",               "💡", "#fbbf24", "Built production-ready LLM applications",    "Complete LLM milestone"),
                ("cloud_guru",   "Cloud Practitioner",        "☁️", "#38bdf8", "Deployed and managed cloud infrastructure",  "Complete AWS/Cloud milestone"),
                ("security_ace", "Security Specialist",       "🔐", "#ef4444", "Mastered cybersecurity and ethical hacking", "Complete Security milestone"),
                ("career_ready", "Career Ready",              "🚀", "#10b981", "Completed the full career roadmap!",         "Complete 100% of the roadmap"),
            ]
            for b_id, b_name, b_emoji, b_color, b_desc, b_cond in badge_catalog:
                cur.execute("""
                    INSERT INTO public.badges
                        (user_id, badge_id, name, emoji, color, description, unlock_condition, unlocked_date, progress)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, '0/1')
                    ON CONFLICT (user_id, badge_id) DO NOTHING;
                """, (db_uuid, b_id, b_name, b_emoji, b_color, b_desc, b_cond))

            print(f"[ensure_user_exists] Created new user: {email} → {db_uuid}")
            return db_uuid


def link_firebase_uid_to_existing_user(email: str, firebase_uid: str) -> Optional[Dict[str, Any]]:
    """
    Links a Firebase UID to an existing user record (by email) that was created 
    previously (e.g. under Supabase Auth or other methods).
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE public.users 
                SET firebase_uid = %s 
                WHERE email = %s 
                RETURNING id;
            """, (firebase_uid, email))
            row = cur.fetchone()
            if row:
                return get_user_by_id(row[0])
    return None

def update_last_login(user_id: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE public.users SET last_login = now() WHERE id = %s;", (user_id,))

def update_user_career_goal(user_id: str, career_goal: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE public.user_profiles SET current_career_goal = %s WHERE user_id = %s;", (career_goal, user_id))

def update_user_readiness_score(user_id: str, score: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE public.user_profiles SET current_readiness_score = %s WHERE user_id = %s;", (score, user_id))

def update_user_active_roadmap(user_id: str, roadmap_id: Optional[str]):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE public.user_profiles SET current_roadmap_id = %s WHERE user_id = %s;", (roadmap_id, user_id))

# -------------------------------------------------------------
# RESUME & PERSISTED ANALYSES OPERATIONS
# -------------------------------------------------------------

def save_current_resume(user_id: str, resume_file_url: str, resume_text: str, parsed_data: dict = None) -> str:
    from core.supabase_client import supabase
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # 1. Check for existing resume for the user
            cur.execute("SELECT resume_file_url FROM public.current_resume WHERE user_id = %s;", (user_id,))
            existing = cur.fetchone()
            
            # 2. If exists, delete the associated file from Supabase Storage
            if existing and existing[0]:
                old_url = existing[0]
                if old_url != "local_text_only" and supabase:
                    try:
                        filename = old_url.split("/")[-1]
                        supabase.storage.from_("resumes").remove([f"{user_id}/{filename}"])
                    except Exception as e:
                        print(f"Warning: Failed to delete old resume from storage: {e}")
            
            # 3. Delete the existing record (cascades to old reports)
            cur.execute("DELETE FROM public.current_resume WHERE user_id = %s;", (user_id,))
            
            # 4. Insert the new resume record
            cur.execute("""
                INSERT INTO public.current_resume (user_id, resume_file_url, resume_text, parsed_data, uploaded_at, updated_at)
                VALUES (%s, %s, %s, %s, now(), now())
                RETURNING id;
            """, (user_id, resume_file_url, resume_text, Json(parsed_data) if parsed_data else None))
            resume_id = cur.fetchone()[0]
    return str(resume_id)

def create_ats_report(user_id: str, resume_id: str, ats_score: int, report_data: Dict[str, Any]):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.ats_reports (user_id, resume_id, ats_score, report_data, created_at)
                VALUES (%s, %s, %s, %s, now());
            """, (user_id, resume_id, ats_score, Json(report_data)))

def create_career_recommendations(user_id: str, resume_id: str, recommendations: List[Dict[str, Any]]):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.career_recommendations (user_id, resume_id, recommendations, created_at)
                VALUES (%s, %s, %s, now());
            """, (user_id, resume_id, Json(recommendations)))

def create_skill_gap_report(user_id: str, resume_id: str, career_goal: str, matched_skills: List[str], missing_skills: List[str], priority_ranking: List[Dict[str, Any]], readiness_score: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.skill_gap_reports (user_id, resume_id, career_goal, matched_skills, missing_skills, priority_ranking, readiness_score, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, now());
            """, (user_id, resume_id, career_goal, Json(matched_skills), Json(missing_skills), Json(priority_ranking), readiness_score))

def get_user_resume_history(user_id: str) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT r.id, r.resume_file_url as filename, r.uploaded_at as created_at, 
                       a.ats_score, c.recommendations
                FROM public.current_resume r
                LEFT JOIN public.ats_reports a ON r.id = a.resume_id
                LEFT JOIN public.career_recommendations c ON r.id = c.resume_id
                WHERE r.user_id = %s;
            """, (user_id,))
            return [dict(row) for row in cur.fetchall()]

def get_resume_analysis_details(user_id: str, resume_id: str) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get resume metadata
            cur.execute("SELECT * FROM public.current_resume WHERE user_id = %s AND id = %s;", (user_id, resume_id))
            resume = cur.fetchone()
            if not resume:
                return None
                
            # Get ATS score
            cur.execute("SELECT * FROM public.ats_reports WHERE resume_id = %s;", (resume_id,))
            ats = cur.fetchone()
            
            # Get recommendations
            cur.execute("SELECT * FROM public.career_recommendations WHERE resume_id = %s;", (resume_id,))
            recs = cur.fetchone()
            
            return {
                "resume": dict(resume) if resume else None,
                "ats": dict(ats) if ats else None,
                "recommendations": dict(recs) if recs else None
            }

def get_latest_parsed_resume(user_id: str) -> Optional[Dict[str, Any]]:
    """Fetch the most recent parsed resume data for a user."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT parsed_data
                FROM public.current_resume
                WHERE user_id = %s
                ORDER BY uploaded_at DESC
                LIMIT 1;
            """, (user_id,))
            row = cur.fetchone()
            if row and row["parsed_data"]:
                data = row["parsed_data"]
                if isinstance(data, str):
                    import json
                    try:
                        return json.loads(data)
                    except Exception:
                        return None
                return dict(data)
            return None

# -------------------------------------------------------------
# LEARNING ROADMAP OPERATIONS
# -------------------------------------------------------------

def create_learning_roadmap(
    user_id: str, 
    resume_id: Optional[str], 
    career: str, 
    difficulty: str, 
    total_weeks: int, 
    total_months: int, 
    expected_readiness: int,
    job_market: Dict[str, Any],
    career_forecast: Dict[str, Any],
    matched_skills: List[str],
    missing_skills: List[str],
    monthly_roadmap: List[Dict[str, Any]]
) -> str:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.learning_roadmaps (
                    user_id, resume_id, career, difficulty, total_weeks, total_months, expected_readiness, 
                    job_market, career_forecast, matched_skills, missing_skills, monthly_roadmap, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
                RETURNING id;
            """, (
                user_id, resume_id, career, difficulty, total_weeks, total_months, expected_readiness,
                Json(job_market), Json(career_forecast), Json(matched_skills), Json(missing_skills), Json(monthly_roadmap)
            ))
            roadmap_id = cur.fetchone()[0]
    return str(roadmap_id)

from psycopg2.extras import execute_values

def create_roadmap_milestones_bulk(milestones_data: List[Tuple]):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, """
                INSERT INTO public.roadmap_milestones (roadmap_id, milestone_index, title, skills, complete, resources, projects, created_at)
                VALUES %s;
            """, milestones_data)

def create_roadmap_tasks_bulk(tasks_data: List[Tuple]):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, """
                INSERT INTO public.roadmap_tasks (roadmap_id, week_number, month_number, task_id, title, status, type, description, estimated_hours, created_at)
                VALUES %s;
            """, tasks_data)

def create_roadmap_milestone(roadmap_id: str, milestone_index: int, title: str, skills: List[str], complete: bool, resources: List[Dict[str, Any]], projects: List[Dict[str, Any]]):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.roadmap_milestones (roadmap_id, milestone_index, title, skills, complete, resources, projects, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, now());
            """, (roadmap_id, milestone_index, title, Json(skills), complete, Json(resources), Json(projects)))

def create_roadmap_task(roadmap_id: str, week_number: int, month_number: int, task_id: str, title: str, status: str, type: str, description: Optional[str], estimated_hours: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.roadmap_tasks (roadmap_id, week_number, month_number, task_id, title, status, type, description, estimated_hours, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now());
            """, (roadmap_id, week_number, month_number, task_id, title, status, type, description, estimated_hours))

def get_active_roadmap_for_user(user_id: str) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Find the active roadmap ID from profile
            cur.execute("SELECT current_roadmap_id FROM public.user_profiles WHERE user_id = %s;", (user_id,))
            profile_row = cur.fetchone()
            if not profile_row or not profile_row["current_roadmap_id"]:
                # Fallback: get latest generated roadmap
                cur.execute("SELECT * FROM public.learning_roadmaps WHERE user_id = %s ORDER BY created_at DESC LIMIT 1;", (user_id,))
                roadmap = cur.fetchone()
            else:
                cur.execute("SELECT * FROM public.learning_roadmaps WHERE id = %s;", (profile_row["current_roadmap_id"],))
                roadmap = cur.fetchone()
            
            return dict(roadmap) if roadmap else None

def get_roadmap_milestones(roadmap_id: str) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM public.roadmap_milestones WHERE roadmap_id = %s ORDER BY milestone_index ASC;", (roadmap_id,))
            return [dict(row) for row in cur.fetchall()]

def get_roadmap_tasks(roadmap_id: str) -> List[Dict[str, Any]]:
    # In a full implementation, we'd join with roadmap_task_progress.
    # Since roadmap_tasks already has a status column but roadmap_task_progress overrides it:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT t.*, COALESCE(p.status, t.status) as status
                FROM public.roadmap_tasks t
                LEFT JOIN public.roadmap_task_progress p 
                  ON t.task_id = p.task_id AND t.roadmap_id = p.roadmap_id
                WHERE t.roadmap_id = %s
                ORDER BY t.month_number ASC, t.week_number ASC, t.created_at ASC;
            """, (roadmap_id,))
            return [dict(row) for row in cur.fetchall()]

# -------------------------------------------------------------
# PROGRESS TRACKING OPERATIONS
# -------------------------------------------------------------

def get_user_progress(user_id: str, roadmap_id: str) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM public.user_progress WHERE user_id = %s AND roadmap_id = %s;", (user_id, roadmap_id))
            row = cur.fetchone()
            return dict(row) if row else None

def create_or_update_user_progress(user_id: str, roadmap_id: str, completed_skills: List[str], completed_tasks: List[str], completed_weeks: List[int], completed_months: List[int], completed_milestones: List[int], completed_projects: List[str], current_readiness: int, current_roadmap_completion: float):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.user_progress (
                    user_id, roadmap_id, completed_skills, completed_tasks, completed_weeks, 
                    completed_months, completed_milestones, completed_projects, current_readiness, 
                    current_roadmap_completion, last_activity
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
                ON CONFLICT (user_id, roadmap_id) DO UPDATE SET
                    completed_skills = EXCLUDED.completed_skills,
                    completed_tasks = EXCLUDED.completed_tasks,
                    completed_weeks = EXCLUDED.completed_weeks,
                    completed_months = EXCLUDED.completed_months,
                    completed_milestones = EXCLUDED.completed_milestones,
                    completed_projects = EXCLUDED.completed_projects,
                    current_readiness = EXCLUDED.current_readiness,
                    current_roadmap_completion = EXCLUDED.current_roadmap_completion,
                    last_activity = now();
            """, (
                user_id, roadmap_id, Json(completed_skills), Json(completed_tasks), Json(completed_weeks), 
                Json(completed_months), Json(completed_milestones), Json(completed_projects), current_readiness, 
                current_roadmap_completion
            ))

# Ensure UNIQUE constraint on (user_id, roadmap_id) for progress table exists
# We will execute this in our Python database migration wrapper safely.

def update_task_status_db(roadmap_id: str, task_id: str, status: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE public.roadmap_tasks SET status = %s WHERE roadmap_id = %s AND task_id = %s;", (status, roadmap_id, task_id))

def update_milestone_completion_db(roadmap_id: str, milestone_index: int, complete: bool):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE public.roadmap_milestones SET complete = %s WHERE roadmap_id = %s AND milestone_index = %s;", (complete, roadmap_id, milestone_index))

def upsert_task_progress(user_id: str, roadmap_id: str, milestone_id: str, task_id: str, status: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            completed_at = "now()" if status == "Completed" else "NULL"
            cur.execute(f"""
                INSERT INTO public.roadmap_task_progress (user_id, roadmap_id, milestone_id, task_id, status, completed_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, {completed_at}, now())
                ON CONFLICT (user_id, roadmap_id, task_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    completed_at = EXCLUDED.completed_at,
                    updated_at = now();
            """, (user_id, roadmap_id, milestone_id, task_id, status))

def get_user_roadmap_progress(user_id: str, roadmap_id: str) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM public.roadmap_task_progress WHERE user_id = %s AND roadmap_id = %s;", (user_id, roadmap_id))
            return [dict(row) for row in cur.fetchall()]

# -------------------------------------------------------------
# BADGES & ACHIEVEMENTS OPERATIONS
# -------------------------------------------------------------

def get_user_badges(user_id: str) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM public.badges WHERE user_id = %s;", (user_id,))
            return [dict(row) for row in cur.fetchall()]

def add_or_update_badge(user_id: str, badge_id: str, name: str, emoji: str, color: str, description: str, unlock_condition: str, unlocked_date: Optional[str], progress: str, requirements: Optional[Dict[str, Any]] = None):
    # Parse unlock date if string
    unlocked_dt = None
    if unlocked_date:
        try:
            unlocked_dt = datetime.fromisoformat(unlocked_date.replace("Z", "+00:00"))
        except Exception:
            unlocked_dt = datetime.utcnow()
            
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.badges (user_id, badge_id, name, emoji, color, description, unlock_condition, unlocked_date, progress, requirements)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT(user_id, badge_id) DO UPDATE SET
                    unlocked_date = EXCLUDED.unlocked_date,
                    progress = EXCLUDED.progress;
            """, (user_id, badge_id, name, emoji, color, description, unlock_condition, unlocked_dt, progress, Json(requirements) if requirements else None))

def get_user_achievements(user_id: str) -> List[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM public.achievements WHERE user_id = %s;", (user_id,))
            return [dict(row) for row in cur.fetchall()]

def add_achievement(user_id: str, achievement_id: str, name: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.achievements (user_id, achievement_id, name, unlocked_date)
                VALUES (%s, %s, %s, now())
                ON CONFLICT(user_id, achievement_id) DO NOTHING;
            """, (user_id, achievement_id, name))

# -------------------------------------------------------------
# ANALYTICS OPERATIONS
# -------------------------------------------------------------

def save_analytics(roadmap_id: str, current_readiness: int, projected_readiness: int, roadmap_completion: float, success_probability: int, skills_acquired: List[str], career_growth: List[Dict[str, Any]]):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM public.analytics WHERE roadmap_id = %s;", (roadmap_id,))
            row = cur.fetchone()
            if row:
                cur.execute("""
                    UPDATE public.analytics
                    SET current_readiness = %s, projected_readiness = %s, roadmap_completion = %s, 
                        success_probability = %s, skills_acquired = %s, career_growth = %s
                    WHERE roadmap_id = %s;
                """, (current_readiness, projected_readiness, roadmap_completion, success_probability, Json(skills_acquired), Json(career_growth), roadmap_id))
            else:
                cur.execute("""
                    INSERT INTO public.analytics (roadmap_id, current_readiness, projected_readiness, roadmap_completion, success_probability, skills_acquired, career_growth)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (roadmap_id, current_readiness, projected_readiness, roadmap_completion, success_probability, Json(skills_acquired), Json(career_growth)))

def get_analytics(roadmap_id: str) -> Optional[Dict[str, Any]]:
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM public.analytics WHERE roadmap_id = %s ORDER BY created_at DESC LIMIT 1;", (roadmap_id,))
            row = cur.fetchone()
            return dict(row) if row else None

def get_dashboard_summary(user_id: str) -> Dict[str, Any]:
    """
    Fetches all user profile, active roadmap, progress, analytics,
    badges, achievements, and recent resume upload history in a single,
    highly optimized database connection block using JSON aggregation
    to eliminate multiple roundtrips and dramatically speed up loading time.
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Check if badges need to be initialized first
            cur.execute("SELECT COUNT(*) as count FROM public.badges WHERE user_id = %s;", (user_id,))
            badge_count = cur.fetchone()["count"]
            if badge_count == 0:
                badge_catalog = [
                    {"id": "foundations",  "name": "Foundations Master",        "emoji": "🏗️", "color": "#60a5fa", "desc": "Completed the foundational milestone", "condition": "Complete Foundations milestone"},
                    {"id": "ml_explorer",  "name": "Machine Learning Explorer", "emoji": "🤖", "color": "#a78bfa", "desc": "Mastered core Machine Learning concepts", "condition": "Complete Machine Learning milestone"},
                    {"id": "dl_specialist", "name": "Deep Learning Specialist",  "emoji": "🧠", "color": "#f472b6", "desc": "Conquered Deep Learning and neural networks", "condition": "Complete Deep Learning milestone"},
                    {"id": "nlp_expert",   "name": "NLP Practitioner",          "emoji": "📝", "color": "#34d399", "desc": "Achieved NLP and language model proficiency", "condition": "Complete NLP milestone"},
                    {"id": "llm_builder",  "name": "LLM Builder",               "emoji": "💡", "color": "#fbbf24", "desc": "Built production-ready LLM applications", "condition": "Complete LLM milestone"},
                    {"id": "cloud_guru",   "name": "Cloud Practitioner",        "emoji": "☁️", "color": "#38bdf8", "desc": "Deployed and managed cloud infrastructure", "condition": "Complete AWS/Cloud milestone"},
                    {"id": "security_ace", "name": "Security Specialist",       "emoji": "🔐", "color": "#ef4444", "desc": "Mastered cybersecurity and ethical hacking", "condition": "Complete Security milestone"},
                    {"id": "career_ready", "name": "Career Ready",              "emoji": "🚀", "color": "#10b981", "desc": "Completed the full career roadmap!", "condition": "Complete 100% of the roadmap"}
                ]
                for b in badge_catalog:
                    cur.execute("""
                        INSERT INTO public.badges (user_id, badge_id, name, emoji, color, description, unlock_condition, unlocked_date, progress)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, '0/1')
                        ON CONFLICT (user_id, badge_id) DO NOTHING;
                    """, (user_id, b["id"], b["name"], b["emoji"], b["color"], b["desc"], b["condition"]))

            query = """
            WITH profile_data AS (
                SELECT u.id, u.email, u.created_at, u.last_login, u.firebase_uid,
                       p.name, p.picture, p.joined_date, p.current_career_goal,
                       p.current_readiness_score, p.current_roadmap_id
                FROM public.users u
                LEFT JOIN public.user_profiles p ON u.id = p.user_id
                WHERE u.id = %(user_id)s
            ),
            roadmap_data AS (
                SELECT r.*
                FROM public.learning_roadmaps r
                WHERE id = (SELECT current_roadmap_id FROM profile_data)
                UNION ALL
                SELECT r.*
                FROM public.learning_roadmaps r
                WHERE user_id = %(user_id)s AND (SELECT current_roadmap_id FROM profile_data) IS NULL
                ORDER BY created_at DESC LIMIT 1
            ),
            progress_data AS (
                SELECT * FROM public.user_progress 
                WHERE user_id = %(user_id)s AND roadmap_id = (SELECT id FROM roadmap_data)
            ),
            analytics_data AS (
                SELECT * FROM public.analytics 
                WHERE roadmap_id = (SELECT id FROM roadmap_data) 
                ORDER BY created_at DESC LIMIT 1
            ),
            badges_data AS (
                SELECT COALESCE(json_agg(b.*), '[]'::json) as data FROM public.badges b WHERE user_id = %(user_id)s
            ),
            achievements_data AS (
                SELECT COALESCE(json_agg(a.*), '[]'::json) as data FROM public.achievements a WHERE user_id = %(user_id)s
            ),
            history_data AS (
                SELECT COALESCE(json_agg(h.*), '[]'::json) as data FROM (
                    SELECT r.id, r.resume_file_url as filename, r.uploaded_at as created_at, 
                           a.ats_score, c.recommendations
                    FROM public.current_resume r
                    LEFT JOIN public.ats_reports a ON r.id = a.resume_id
                    LEFT JOIN public.career_recommendations c ON r.id = c.resume_id
                    WHERE r.user_id = %(user_id)s
                ) h
            ),
            milestones_data AS (
                SELECT COALESCE(json_agg(m.*), '[]'::json) as data FROM (
                    SELECT * FROM public.roadmap_milestones 
                    WHERE roadmap_id = (SELECT id FROM roadmap_data) 
                    ORDER BY milestone_index ASC
                ) m
            ),
            tasks_data AS (
                SELECT COALESCE(json_agg(t.*), '[]'::json) as data FROM (
                    SELECT t.*, COALESCE(p.status, t.status) as status
                    FROM public.roadmap_tasks t
                    LEFT JOIN public.roadmap_task_progress p 
                      ON t.task_id = p.task_id AND t.roadmap_id = p.roadmap_id
                    WHERE t.roadmap_id = (SELECT id FROM roadmap_data)
                    ORDER BY t.month_number ASC, t.week_number ASC, t.created_at ASC
                ) t
            )
            SELECT 
                (SELECT row_to_json(profile_data.*) FROM profile_data) as profile,
                (SELECT row_to_json(roadmap_data.*) FROM roadmap_data) as roadmap,
                (SELECT row_to_json(progress_data.*) FROM progress_data) as progress,
                (SELECT row_to_json(analytics_data.*) FROM analytics_data) as analytics,
                (SELECT data FROM badges_data) as badges,
                (SELECT data FROM achievements_data) as achievements,
                (SELECT data FROM history_data) as history,
                (SELECT data FROM milestones_data) as milestones,
                (SELECT data FROM tasks_data) as tasks
            """
            cur.execute(query, {'user_id': user_id})
            result = cur.fetchone()
            
            if not result or not result["profile"]:
                return {}

            return {
                "profile": result["profile"],
                "roadmap": result["roadmap"],
                "progress": result["progress"],
                "analytics": result["analytics"],
                "milestones": result["milestones"] if result["milestones"] else [],
                "tasks": result["tasks"] if result["tasks"] else [],
                "badges": result["badges"] if result["badges"] else [],
                "achievements": result["achievements"] if result["achievements"] else [],
                "history": result["history"] if result["history"] else []
            }


# ─────────────────────────────────────────────────────────────
# INTERVIEW SESSION OPERATIONS (Phase 8)
# ─────────────────────────────────────────────────────────────

def create_interview_session(user_id: str, interview_type: str, role: Optional[str],
                              difficulty: Optional[str], company: Optional[str],
                              topics: List[str], total_questions: int) -> str:
    """Create a new interview session and return its UUID."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO public.interview_sessions
                    (user_id, interview_type, role, difficulty, company, topics, total_questions, status, started_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'in_progress', now())
                RETURNING id;
            """, (user_id, interview_type, role, difficulty, company, Json(topics), total_questions))
            row = cur.fetchone()
            return str(row["id"])


def get_interview_sessions(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Fetch the user's interview session history, newest first."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, interview_type, role, difficulty, company, topics,
                       status, overall_score, total_questions, answered_count,
                       started_at, completed_at, duration_seconds, metadata
                FROM public.interview_sessions
                WHERE user_id = %s
                ORDER BY started_at DESC
                LIMIT %s;
            """, (user_id, limit))
            rows = cur.fetchall()
            return [dict(r) for r in rows]


def get_interview_session_by_id(session_id: str, user_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a single interview session (verifying ownership)."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, interview_type, role, difficulty, company, topics,
                       status, overall_score, total_questions, answered_count,
                       started_at, completed_at, duration_seconds, metadata
                FROM public.interview_sessions
                WHERE id = %s AND user_id = %s;
            """, (session_id, user_id))
            row = cur.fetchone()
            return dict(row) if row else None


def save_interview_answer(session_id: str, user_id: str, question_index: int,
                           question_text: str, question_type: str,
                           answer_text: str, time_taken_secs: int,
                           scores: Dict[str, Any], feedback: Dict[str, Any]) -> str:
    """Save a Q&A pair for a session and increment answered_count."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO public.interview_answers
                    (session_id, user_id, question_index, question_text, question_type,
                     answer_text, time_taken_secs, scores, feedback, evaluated)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
                RETURNING id;
            """, (session_id, user_id, question_index, question_text, question_type,
                  answer_text, time_taken_secs, Json(scores), Json(feedback)))
            row = cur.fetchone()
            answer_id = str(row["id"]) if row else ""
            cur.execute("""
                UPDATE public.interview_sessions
                SET answered_count = answered_count + 1
                WHERE id = %s;
            """, (session_id,))
            return answer_id


def get_interview_answers(session_id: str, user_id: str) -> List[Dict[str, Any]]:
    """Fetch all Q&A pairs for a session ordered by question_index."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, question_index, question_text, question_type,
                       answer_text, time_taken_secs, scores, feedback, evaluated, created_at
                FROM public.interview_answers
                WHERE session_id = %s AND user_id = %s
                ORDER BY question_index ASC;
            """, (session_id, user_id))
            rows = cur.fetchall()
            return [dict(r) for r in rows]


def complete_interview_session(session_id: str, user_id: str, overall_score: float,
                                duration_seconds: int, session_feedback: Dict[str, Any]) -> bool:
    """Mark a session as completed and store aggregate scores."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE public.interview_sessions
                SET status = 'completed',
                    overall_score = %s,
                    duration_seconds = %s,
                    completed_at = now(),
                    metadata = metadata || %s::jsonb
                WHERE id = %s AND user_id = %s;
            """, (overall_score, duration_seconds, Json({"feedback": session_feedback}), session_id, user_id))
            return cur.rowcount > 0


def get_interview_stats(user_id: str) -> Dict[str, Any]:
    """Aggregate interview statistics for the dashboard."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    COUNT(*) FILTER (WHERE status = 'completed') AS total_completed,
                    COALESCE(ROUND(AVG(overall_score) FILTER (WHERE status = 'completed')::numeric, 1), 0) AS avg_score,
                    COALESCE(MAX(overall_score) FILTER (WHERE status = 'completed'), 0) AS best_score,
                    COUNT(*) FILTER (WHERE interview_type = 'technical' AND status = 'completed') AS technical_count,
                    COUNT(*) FILTER (WHERE interview_type = 'hr' AND status = 'completed') AS hr_count,
                    COUNT(*) FILTER (WHERE interview_type = 'coding' AND status = 'completed') AS coding_count,
                    COUNT(*) FILTER (WHERE interview_type = 'behavioral' AND status = 'completed') AS behavioral_count,
                    COUNT(*) FILTER (WHERE interview_type = 'mock' AND status = 'completed') AS mock_count,
                    MAX(started_at) AS last_interview_at
                FROM public.interview_sessions
                WHERE user_id = %s;
            """, (user_id,))
            row = cur.fetchone()
            if not row:
                return {"total_completed": 0, "avg_score": 0, "best_score": 0}
            return dict(row)


# ─────────────────────────────────────────────────────────────
# CAREER COACH OPERATIONS (Phase 8)
# ─────────────────────────────────────────────────────────────

def save_career_coach_message(user_id: str, message: str, response: str,
                               context_used: Dict[str, Any]) -> str:
    """Persist a career coach conversation exchange."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO public.career_coach_messages
                    (user_id, message, response, context_used, created_at)
                VALUES (%s, %s, %s, %s, now())
                RETURNING id;
            """, (user_id, message, response, Json(context_used)))
            row = cur.fetchone()
            return str(row["id"]) if row else ""


def get_career_coach_history(user_id: str, limit: int = 30) -> List[Dict[str, Any]]:
    """Fetch career coach history (oldest first for chat display)."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, message, response, created_at
                FROM public.career_coach_messages
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s;
            """, (user_id, limit))
            rows = cur.fetchall()
            return [dict(r) for r in reversed(rows)]


# ─────────────────────────────────────────────────────────────
# INTERVIEW BADGE OPERATIONS (Phase 8)
# ─────────────────────────────────────────────────────────────

def award_interview_badge(user_id: str, badge: Dict[str, Any]) -> bool:
    """Award an interview badge (idempotent via UNIQUE constraint)."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO public.interview_badges
                    (user_id, badge_id, name, emoji, color, description, awarded_at)
                VALUES (%s, %s, %s, %s, %s, %s, now())
                ON CONFLICT (user_id, badge_id) DO NOTHING;
            """, (user_id, badge["id"], badge["name"], badge.get("emoji", "🏆"),
                  badge.get("color", "#6366f1"), badge.get("description", "")))
            return cur.rowcount > 0


def get_interview_badges(user_id: str) -> List[Dict[str, Any]]:
    """Fetch all interview badges earned by a user."""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT badge_id, name, emoji, color, description, awarded_at
                FROM public.interview_badges
                WHERE user_id = %s
                ORDER BY awarded_at DESC;
            """, (user_id,))
            rows = cur.fetchall()
            return [dict(r) for r in rows]

