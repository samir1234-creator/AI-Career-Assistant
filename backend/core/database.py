import sqlite3
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Database path setup: in the backend directory
DB_PATH = Path(__file__).resolve().parent.parent / "career_assistant.db"

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys support
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes the SQLite tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT,
        picture TEXT,
        google_id TEXT UNIQUE,
        last_login TEXT,
        created_at TEXT
    );
    """)
    
    # 2. Resume history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT,
        file_size INTEGER,
        text_content TEXT,
        parsed_data TEXT, -- JSON string
        ats_score INTEGER,
        recommendations TEXT, -- JSON string
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # 3. Roadmaps table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        career TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        total_weeks INTEGER NOT NULL,
        total_months INTEGER NOT NULL,
        expected_readiness INTEGER NOT NULL,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # 4. Roadmap Months table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmap_months (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roadmap_id INTEGER NOT NULL,
        month_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        completion_pct REAL DEFAULT 0.0,
        skills TEXT, -- JSON array
        goals TEXT, -- JSON array
        projects TEXT, -- JSON array
        FOREIGN KEY(roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
    );
    """)
    
    # 5. Roadmap Weeks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmap_weeks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roadmap_id INTEGER NOT NULL,
        month_number INTEGER NOT NULL,
        week_number INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        completion_pct REAL DEFAULT 0.0,
        topics TEXT, -- JSON array
        resources TEXT, -- JSON array
        quiz TEXT,
        expected_outcome TEXT,
        estimated_hours INTEGER,
        FOREIGN KEY(roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
    );
    """)
    
    # 6. Roadmap Tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmap_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roadmap_id INTEGER NOT NULL,
        week_number INTEGER NOT NULL,
        task_id TEXT NOT NULL,
        title TEXT NOT NULL,
        status TEXT NOT NULL, -- Pending, In Progress, Completed, Skipped, Locked
        type TEXT NOT NULL, -- Practice, Assignment, Quiz, Learn
        description TEXT,
        estimated_hours INTEGER,
        FOREIGN KEY(roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
    );
    """)
    
    # 7. Milestones table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS milestones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roadmap_id INTEGER NOT NULL,
        milestone_index INTEGER NOT NULL,
        title TEXT NOT NULL,
        skills TEXT, -- JSON array
        complete INTEGER DEFAULT 0, -- 0/1 boolean
        resources TEXT, -- JSON array
        projects TEXT, -- JSON array
        FOREIGN KEY(roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
    );
    """)
    
    # 8. Badges table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS badges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        badge_id TEXT NOT NULL,
        name TEXT NOT NULL,
        emoji TEXT NOT NULL,
        color TEXT NOT NULL,
        description TEXT NOT NULL,
        unlock_condition TEXT NOT NULL,
        unlocked_date TEXT,
        progress TEXT NOT NULL, -- "0/1" style progress
        requirements TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(user_id, badge_id)
    );
    """)
    
    # 9. Achievements table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        achievement_id TEXT NOT NULL,
        name TEXT NOT NULL,
        unlocked_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(user_id, achievement_id)
    );
    """)
    
    # 10. Analytics table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analytics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roadmap_id INTEGER NOT NULL,
        current_readiness INTEGER NOT NULL,
        projected_readiness INTEGER NOT NULL,
        roadmap_completion REAL NOT NULL,
        success_probability INTEGER NOT NULL,
        skills_acquired TEXT, -- JSON array
        career_growth TEXT, -- JSON array
        FOREIGN KEY(roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
    );
    """)
    
    # 11. Roadmap Progress table (for resume feature)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmap_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roadmap_id INTEGER NOT NULL,
        current_month INTEGER DEFAULT 1,
        current_week INTEGER DEFAULT 1,
        current_task_id TEXT,
        completed_milestones TEXT, -- JSON array
        unlocked_badges TEXT, -- JSON array
        last_activity TEXT,
        FOREIGN KEY(roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    conn.close()

# Auto-initialize on import
init_db()

# ==============================================================================
# DATABASE OPERATION WRAPPERS
# ==============================================================================

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?;", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?;", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_google_id(google_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM users WHERE google_id = ?;", (google_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def create_user(email: str, name: str, picture: str, google_id: str) -> int:
    conn = get_db_connection()
    now_str = datetime.utcnow().isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (email, name, picture, google_id, last_login, created_at)
        VALUES (?, ?, ?, ?, ?, ?);
    """, (email, name, picture, google_id, now_str, now_str))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id

def update_last_login(user_id: int):
    conn = get_db_connection()
    now_str = datetime.utcnow().isoformat()
    conn.execute("UPDATE users SET last_login = ? WHERE id = ?;", (now_str, user_id))
    conn.commit()
    conn.close()

# Resume history operations
def get_resume_history(user_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM resume_history WHERE user_id = ? ORDER BY id DESC;", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_resume_history(user_id: int, filename: str, file_size: int, text_content: str, parsed_data: Dict[str, Any], ats_score: int, recommendations: List[Dict[str, Any]]) -> int:
    conn = get_db_connection()
    now_str = datetime.utcnow().isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resume_history (user_id, filename, file_size, text_content, parsed_data, ats_score, recommendations, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, (user_id, filename, file_size, text_content, json.dumps(parsed_data), ats_score, json.dumps(recommendations), now_str))
    history_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return history_id

# Roadmap operations
def get_active_roadmap(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM roadmaps WHERE user_id = ? ORDER BY id DESC LIMIT 1;", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def delete_user_roadmaps(user_id: int):
    conn = get_db_connection()
    conn.execute("DELETE FROM roadmaps WHERE user_id = ?;", (user_id,))
    conn.commit()
    conn.close()

def create_roadmap_entry(user_id: int, career: str, difficulty: str, total_weeks: int, total_months: int, expected_readiness: int) -> int:
    conn = get_db_connection()
    now_str = datetime.utcnow().isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO roadmaps (user_id, career, difficulty, total_weeks, total_months, expected_readiness, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (user_id, career, difficulty, total_weeks, total_months, expected_readiness, now_str))
    roadmap_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return roadmap_id

# Badges and Achievements operations
def get_user_badges(user_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM badges WHERE user_id = ?;", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_user_achievements(user_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM achievements WHERE user_id = ?;", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_or_update_badge(user_id: int, badge_id: str, name: str, emoji: str, color: str, description: str, unlock_condition: str, unlocked_date: Optional[str], progress: str, requirements: Optional[str] = None):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO badges (user_id, badge_id, name, emoji, color, description, unlock_condition, unlocked_date, progress, requirements)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, badge_id) DO UPDATE SET
            unlocked_date=excluded.unlocked_date,
            progress=excluded.progress;
    """, (user_id, badge_id, name, emoji, color, description, unlock_condition, unlocked_date, progress, requirements))
    conn.commit()
    conn.close()

def add_achievement(user_id: int, achievement_id: str, name: str):
    conn = get_db_connection()
    now_str = datetime.utcnow().isoformat()
    try:
        conn.execute("""
            INSERT INTO achievements (user_id, achievement_id, name, unlocked_date)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, achievement_id) DO NOTHING;
        """, (user_id, achievement_id, name, now_str))
        conn.commit()
    except Exception:
        pass
    conn.close()

# Roadmap sub-component read queries
def get_roadmap_months(roadmap_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM roadmap_months WHERE roadmap_id = ? ORDER BY month_number ASC;", (roadmap_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_roadmap_weeks(roadmap_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM roadmap_weeks WHERE roadmap_id = ? ORDER BY week_number ASC;", (roadmap_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_roadmap_tasks(roadmap_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM roadmap_tasks WHERE roadmap_id = ? ORDER BY id ASC;", (roadmap_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_milestones(roadmap_id: int) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM milestones WHERE roadmap_id = ? ORDER BY milestone_index ASC;", (roadmap_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_roadmap_progress(roadmap_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM roadmap_progress WHERE roadmap_id = ? ORDER BY id DESC LIMIT 1;", (roadmap_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_analytics(roadmap_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM analytics WHERE roadmap_id = ? ORDER BY id DESC LIMIT 1;", (roadmap_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

# Roadmap sub-component write/update queries
def save_roadmap_progress(roadmap_id: int, current_month: int, current_week: int, current_task_id: Optional[str], completed_milestones: List[str], unlocked_badges: List[str]):
    conn = get_db_connection()
    now_str = datetime.utcnow().isoformat()
    conn.execute("""
        INSERT INTO roadmap_progress (roadmap_id, current_month, current_week, current_task_id, completed_milestones, unlocked_badges, last_activity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            current_month=excluded.current_month,
            current_week=excluded.current_week,
            current_task_id=excluded.current_task_id,
            completed_milestones=excluded.completed_milestones,
            unlocked_badges=excluded.unlocked_badges,
            last_activity=excluded.last_activity;
    """, (roadmap_id, current_month, current_week, current_task_id, json.dumps(completed_milestones), json.dumps(unlocked_badges), now_str))
    conn.commit()
    conn.close()

def save_analytics(roadmap_id: int, current_readiness: int, projected_readiness: int, roadmap_completion: float, success_probability: int, skills_acquired: List[str], career_growth: List[Dict[str, Any]]):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if exists
    row = cursor.execute("SELECT id FROM analytics WHERE roadmap_id = ?;", (roadmap_id,)).fetchone()
    if row:
        cursor.execute("""
            UPDATE analytics
            SET current_readiness = ?, projected_readiness = ?, roadmap_completion = ?, success_probability = ?, skills_acquired = ?, career_growth = ?
            WHERE roadmap_id = ?;
        """, (current_readiness, projected_readiness, roadmap_completion, success_probability, json.dumps(skills_acquired), json.dumps(career_growth), roadmap_id))
    else:
        cursor.execute("""
            INSERT INTO analytics (roadmap_id, current_readiness, projected_readiness, roadmap_completion, success_probability, skills_acquired, career_growth)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (roadmap_id, current_readiness, projected_readiness, roadmap_completion, success_probability, json.dumps(skills_acquired), json.dumps(career_growth)))
    conn.commit()
    conn.close()

def update_task_status_db(roadmap_id: int, task_id: str, status: str):
    conn = get_db_connection()
    conn.execute("UPDATE roadmap_tasks SET status = ? WHERE roadmap_id = ? AND task_id = ?;", (status, roadmap_id, task_id))
    conn.commit()
    conn.close()

def update_week_completion_db(roadmap_id: int, week_number: int, completion_pct: float):
    conn = get_db_connection()
    conn.execute("UPDATE roadmap_weeks SET completion_pct = ? WHERE roadmap_id = ? AND week_number = ?;", (completion_pct, roadmap_id, week_number))
    conn.commit()
    conn.close()

def update_month_completion_db(roadmap_id: int, month_number: int, completion_pct: float):
    conn = get_db_connection()
    conn.execute("UPDATE roadmap_months SET completion_pct = ? WHERE roadmap_id = ? AND month_number = ?;", (completion_pct, roadmap_id, month_number))
    conn.commit()
    conn.close()

def update_milestone_completion_db(roadmap_id: int, milestone_index: int, complete: int):
    conn = get_db_connection()
    conn.execute("UPDATE milestones SET complete = ? WHERE roadmap_id = ? AND milestone_index = ?;", (complete, roadmap_id, milestone_index))
    conn.commit()
    conn.close()

