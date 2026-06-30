from fastapi import APIRouter, Header, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from core.database import (
    get_user_by_id, create_user, update_last_login,
    get_user_resume_history, get_resume_analysis_details,
    get_roadmap_milestones, get_roadmap_tasks,
    update_task_status_db, update_milestone_completion_db,
    create_or_update_user_progress, get_user_progress,
    upsert_task_progress, get_active_roadmap_for_user,
    get_user_badges, add_or_update_badge,
    get_user_achievements, add_achievement,
    save_analytics, get_analytics,
    update_user_readiness_score, update_user_career_goal,
    get_db_connection, get_user_by_firebase_uid, link_firebase_uid_to_existing_user,
    get_dashboard_summary, ensure_user_exists
)
from core.firebase_client import verify_firebase_token
from core.response import BaseResponse
from core.exceptions import AppException

router = APIRouter()

# -------------------------------------------------------------
# AUTHENTICATION DEPENDENCY
# -------------------------------------------------------------

def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Dependency that extracts the Firebase JWT from the Authorization header,
    verifies it, and guarantees the user exists in the database before returning
    the full public profile. Uses the centralized ensure_user_exists() which is
    atomic and handles all edge cases (new user, legacy email account, missing
    firebase_uid link).
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header.")

    token = authorization.split(" ")[1]
    payload = verify_firebase_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Session expired or invalid token.")

    db_uuid      = payload["sub"]
    firebase_uid = payload["firebase_uid"]
    email        = payload["email"]
    name         = payload["name"]
    picture      = payload["picture"]

    # Single atomic call — creates user if missing, links UID if needed,
    # updates last_login, and returns the resolved UUID.
    resolved_id = ensure_user_exists(firebase_uid, email, name, picture, db_uuid)

    # Fetch the full profile row for downstream endpoints
    user = get_user_by_id(resolved_id)
    if not user:
        raise HTTPException(status_code=500, detail="User record could not be resolved after initialization.")

    return user

# -------------------------------------------------------------
# SCHEMA DEFINITIONS
# -------------------------------------------------------------

class TaskUpdateRequest(BaseModel):
    task_id: str = Field(..., description="ID of the roadmap task")
    status: str = Field(..., description="New status: Not Started, In Progress, Completed, Skipped")

# -------------------------------------------------------------
# ENDPOINTS
# -------------------------------------------------------------

@router.post("/initialize", response_model=BaseResponse[Dict[str, Any]])
async def initialize_user(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Explicitly initializes (or verifies) the current Firebase user's database
    record. Called by the frontend immediately after login to guarantee the user
    row exists before any dashboard or upload requests are made.
    Returns the full user profile.
    """
    return BaseResponse(
        success=True,
        data=current_user,
        message="User initialized successfully."
    )


@router.get("/profile", response_model=BaseResponse[Dict[str, Any]])
async def get_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Returns the profile information of the current authenticated user.
    """
    return BaseResponse(
        success=True,
        data=current_user,
        message="User profile retrieved successfully."
    )

@router.get("/history", response_model=BaseResponse[List[Dict[str, Any]]])
async def get_history(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Returns the resume upload history and associated ATS scores for the user.
    """
    history = get_user_resume_history(current_user["id"])
    return BaseResponse(
        success=True,
        data=history,
        message="Resume upload history retrieved successfully."
    )

@router.get("/history/{resume_id}", response_model=BaseResponse[Dict[str, Any]])
async def get_history_details(resume_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Retrieves the complete parsed details, ATS score feedback, and recommendations for a previous resume upload.
    """
    details = get_resume_analysis_details(current_user["id"], resume_id)
    if not details:
        raise AppException(message="Resume analysis record not found or access denied.", status_code=404)
    return BaseResponse(
        success=True,
        data=details,
        message="Resume analysis details retrieved successfully."
    )

@router.get("/roadmap/active", response_model=BaseResponse[Dict[str, Any]])
async def get_active_roadmap(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Fetches the active learning roadmap, milestones, and tasks along with task progress states.
    """
    roadmap = get_active_roadmap_for_user(current_user["id"])
    if not roadmap:
        return BaseResponse(
            success=True,
            data={},
            message="No active roadmap found for this user."
        )
        
    roadmap_id = roadmap["id"]
    milestones = get_roadmap_milestones(roadmap_id)
    tasks = get_roadmap_tasks(roadmap_id)
    
    # Fetch progress
    progress = get_user_progress(current_user["id"], roadmap_id)
    analytics = get_analytics(roadmap_id)
    
    return BaseResponse(
        success=True,
        data={
            "roadmap": roadmap,
            "milestones": milestones,
            "tasks": tasks,
            "progress": progress,
            "analytics": analytics
        },
        message="Active roadmap and progress states retrieved."
    )

@router.post("/roadmap/task/update", response_model=BaseResponse[Dict[str, Any]])
async def update_task_status(payload: TaskUpdateRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Updates a task's status and recalculates milestones completion, readiness scores, badges, and analytics.
    """
    user_id = current_user["id"]
    roadmap = get_active_roadmap_for_user(user_id)
    if not roadmap:
        raise AppException(message="No active learning roadmap found for task update.", status_code=400)
        
    roadmap_id = roadmap["id"]
    
    # 1. Update task in database (using new task progress table)
    # Note: we pass None for milestone_id as it's optional
    upsert_task_progress(user_id, roadmap_id, None, payload.task_id, payload.status)
    
    # 2. Retrieve all tasks to compute progress
    tasks = get_roadmap_tasks(roadmap_id)
    total_tasks = len(tasks)
    completed_tasks = [t for t in tasks if t["status"] == "Completed"]
    completed_task_ids = [t["task_id"] for t in completed_tasks]
    
    completion_pct = round((len(completed_tasks) / total_tasks) * 100, 2) if total_tasks > 0 else 0.0
    
    # 3. Recalculate milestones based on completed tasks
    milestones = get_roadmap_milestones(roadmap_id)
    completed_milestones = []
    
    # We complete a milestone if all tasks for that week/month are done, or based on skills.
    # To keep it robust, let's complete a milestone if all tasks associated with its skills are completed, 
    # or if it's the capstone and the capstone tasks are completed.
    for m in milestones:
        # Check tasks for this milestone index (e.g. mapping week numbers)
        # Usually week_number maps to milestone_index + 1 or similar.
        # Let's say milestone_index = X corresponds to some weeks. Let's find tasks matching milestone skills.
        milestone_skills = [s.lower().strip() for s in m.get("skills", [])]
        
        # Find tasks in this roadmap that match these skills in their title/description
        matched_tasks = []
        for t in tasks:
            title_lower = t["title"].lower()
            desc_lower = (t["description"] or "").lower()
            if any(skill in title_lower or skill in desc_lower for skill in milestone_skills):
                matched_tasks.append(t)
                
        # If no tasks matched by skills, match by week sequence:
        # E.g. Milestone 0 -> Week 1-2, Milestone 1 -> Week 3-4, etc.
        if not matched_tasks:
            # Fallback mapping: milestones map to specific weeks
            # E.g., total_weeks / total_milestones weeks per milestone
            weeks_per_milestone = max(1, roadmap["total_weeks"] // max(1, len(milestones)))
            start_week = m["milestone_index"] * weeks_per_milestone + 1
            end_week = (m["milestone_index"] + 1) * weeks_per_milestone
            matched_tasks = [t for t in tasks if start_week <= t["week_number"] <= end_week]
            
        # Check if all matched tasks are completed
        is_complete = len(matched_tasks) > 0 and all(t["status"] == "Completed" for t in matched_tasks)
        
        if is_complete:
            completed_milestones.append(m["milestone_index"])
            update_milestone_completion_db(roadmap_id, m["milestone_index"], True)
        else:
            update_milestone_completion_db(roadmap_id, m["milestone_index"], False)
            
    # 4. Calculate Career Readiness Score
    # Formula: current_readiness = base_readiness + (completion_pct / 100) * (expected_readiness - base_readiness)
    # Let's fetch base career_readiness score from the latest skill gap report or default to 50
    base_readiness = 50
    # Search for base readiness score
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT readiness_score FROM public.skill_gap_reports 
                WHERE user_id = %s AND career_goal = %s 
                ORDER BY created_at DESC LIMIT 1;
            """, (user_id, roadmap["career"]))
            row = cur.fetchone()
            if row:
                base_readiness = row[0]
                
    expected_readiness = roadmap["expected_readiness"]
    current_readiness = int(base_readiness + (completion_pct / 100.0) * (expected_readiness - base_readiness))
    current_readiness = min(expected_readiness, max(base_readiness, current_readiness))
    
    # Update profile readiness
    update_user_readiness_score(user_id, current_readiness)
    
    # 5. Check and unlock badges
    unlocked_badge_ids = []
    # Badge rules:
    badge_catalog = [
        {"id": "foundations",  "name": "Foundations Master",        "emoji": "🏗️", "color": "#60a5fa", "desc": "Completed the foundational milestone", "keywords": ["foundation", "python", "sql", "programming", "web foundation"], "milestone_idx": 0},
        {"id": "ml_explorer",  "name": "Machine Learning Explorer", "emoji": "🤖", "color": "#a78bfa", "desc": "Mastered core Machine Learning concepts", "keywords": ["machine learning", "ml core", "scikit"], "milestone_idx": 1},
        {"id": "dl_specialist", "name": "Deep Learning Specialist",  "emoji": "🧠", "color": "#f472b6", "desc": "Conquered Deep Learning and neural networks", "keywords": ["deep learning", "pytorch", "tensorflow", "framework"], "milestone_idx": 2},
        {"id": "nlp_expert",   "name": "NLP Practitioner",          "emoji": "📝", "color": "#34d399", "desc": "Achieved NLP and language model proficiency", "keywords": ["nlp", "natural language", "bert", "transformers"], "milestone_idx": 3},
        {"id": "llm_builder",  "name": "LLM Builder",               "emoji": "💡", "color": "#fbbf24", "desc": "Built production-ready LLM applications", "keywords": ["llm", "large language", "gpt", "generative"], "milestone_idx": 4},
        {"id": "cloud_guru",   "name": "Cloud Practitioner",        "emoji": "☁️", "color": "#38bdf8", "desc": "Deployed and managed cloud infrastructure", "keywords": ["cloud", "aws", "azure", "gcp", "devops", "deployment"], "milestone_idx": 5},
        {"id": "security_ace", "name": "Security Specialist",       "emoji": "🔐", "color": "#ef4444", "desc": "Mastered cybersecurity and ethical hacking", "keywords": ["security", "penetration", "owasp", "siem", "cryptography"], "milestone_idx": 6},
        {"id": "career_ready", "name": "Career Ready",              "emoji": "🚀", "color": "#10b981", "desc": "Completed the full career roadmap!", "keywords": [], "milestone_idx": -1}
    ]
    
    for badge in badge_catalog:
        should_unlock = False
        progress_str = "0/1"
        
        if badge["id"] == "career_ready":
            should_unlock = completion_pct >= 100.0
            progress_str = f"{int(completion_pct)}%"
        else:
            # Unlock if milestone index is completed
            milestone_idx = badge["milestone_idx"]
            if milestone_idx < len(milestones):
                should_unlock = milestone_idx in completed_milestones
                progress_str = "1/1" if should_unlock else "0/1"
                
        if should_unlock:
            unlocked_badge_ids.append(badge["id"])
            add_or_update_badge(
                user_id=user_id,
                badge_id=badge["id"],
                name=badge["name"],
                emoji=badge["emoji"],
                color=badge["color"],
                description=badge["desc"],
                unlock_condition=f"Complete milestone {badge['name']}",
                unlocked_date=datetime.utcnow().isoformat(),
                progress=progress_str
            )
            # Add an achievement record
            add_achievement(user_id, f"unlock_{badge['id']}", f"Unlocked {badge['name']} Badge!")
        else:
            # Reset/save progress for locked badge
            add_or_update_badge(
                user_id=user_id,
                badge_id=badge["id"],
                name=badge["name"],
                emoji=badge["emoji"],
                color=badge["color"],
                description=badge["desc"],
                unlock_condition=f"Complete milestone {badge['name']}",
                unlocked_date=None,
                progress=progress_str
            )
            
    # 6. Recalculate completed weeks/months/projects
    completed_weeks = []
    completed_months = []
    
    # Calculate week completion
    weeks = sorted(list(set(t["week_number"] for t in tasks)))
    for w in weeks:
        week_tasks = [t for t in tasks if t["week_number"] == w]
        if len(week_tasks) > 0 and all(t["status"] == "Completed" for t in week_tasks):
            completed_weeks.append(w)
            
    # Calculate month completion
    months = sorted(list(set(t["month_number"] for t in tasks)))
    for m in months:
        month_tasks = [t for t in tasks if t["month_number"] == m]
        if len(month_tasks) > 0 and all(t["status"] == "Completed" for t in month_tasks):
            completed_months.append(m)
            
    # Skills Acquired list
    skills_acquired = []
    for m_idx in completed_milestones:
        m = next((mil for mil in milestones if mil["milestone_index"] == m_idx), None)
        if m:
            skills_acquired.extend(m.get("skills", []))
    skills_acquired.extend(roadmap.get("matched_skills", []))
    skills_acquired = list(set(skills_acquired))
    
    # 7. Update User Progress in DB
    create_or_update_user_progress(
        user_id=user_id,
        roadmap_id=roadmap_id,
        completed_skills=skills_acquired,
        completed_tasks=completed_task_ids,
        completed_weeks=completed_weeks,
        completed_months=completed_months,
        completed_milestones=completed_milestones,
        completed_projects=[], # Optional
        current_readiness=current_readiness,
        current_roadmap_completion=completion_pct
    )
    
    # 8. Save updated Analytics
    # Success Probability calculation
    success_prob = min(98, current_readiness + 10) # Simple trend contribution
    career_growth = [
        {"month": "Base", "readiness": base_readiness},
        {"month": "Current", "readiness": current_readiness},
        {"month": "Target", "readiness": expected_readiness}
    ]
    
    save_analytics(
        roadmap_id=roadmap_id,
        current_readiness=current_readiness,
        projected_readiness=expected_readiness,
        roadmap_completion=completion_pct,
        success_probability=success_prob,
        skills_acquired=skills_acquired,
        career_growth=career_growth
    )
    
    # Retrieve updated progress
    updated_progress = get_user_progress(user_id, roadmap_id)
    updated_analytics = get_analytics(roadmap_id)
    
    return BaseResponse(
        success=True,
        data={
            "progress": updated_progress,
            "analytics": updated_analytics,
            "milestones": get_roadmap_milestones(roadmap_id),
            "tasks": get_roadmap_tasks(roadmap_id)
        },
        message="Task status updated and progress recalculated."
    )

@router.get("/dashboard", response_model=BaseResponse[Dict[str, Any]])
async def get_dashboard(
    response: Response,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Aggregates statistics for the user dashboard.
    Data is safe to cache privately for 30 s; stale-while-revalidate allows
    background refresh for up to 60 s after expiry.
    """
    # Override the global no-store default set by the security-headers middleware
    response.headers["Cache-Control"] = "private, max-age=30, stale-while-revalidate=60"
    user_id = current_user["id"]
    roadmap = get_active_roadmap_for_user(user_id)
    badges = get_user_badges(user_id)
    if not badges:
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
            add_or_update_badge(
                user_id=user_id,
                badge_id=b["id"],
                name=b["name"],
                emoji=b["emoji"],
                color=b["color"],
                description=b["desc"],
                unlock_condition=b["condition"],
                unlocked_date=None,
                progress="0/1"
            )
        badges = get_user_badges(user_id)
    achievements = get_user_achievements(user_id)
    history = get_user_resume_history(user_id)
    
    if not roadmap:
        return BaseResponse(
            success=True,
            data={
                "has_active_roadmap": False,
                "current_readiness": current_user["current_readiness_score"] or 0,
                "projected_readiness": 0,
                "roadmap_progress": 0,
                "completed_tasks": 0,
                "remaining_tasks": 0,
                "completed_skills": [],
                "remaining_skills": [],
                "achievements": achievements,
                "badges": badges,
                "estimated_job_ready_date": "N/A",
                "recent_activity": []
            },
            message="No active roadmap found for dashboard."
        )
        
    roadmap_id = roadmap["id"]
    progress = get_user_progress(user_id, roadmap_id)
    analytics = get_analytics(roadmap_id)
    tasks = get_roadmap_tasks(roadmap_id)
    
    # Tasks metrics
    total_tasks = len(tasks)
    completed_tasks = [t for t in tasks if t["status"] == "Completed"]
    remaining_tasks = [t for t in tasks if t["status"] not in ["Completed", "Skipped"]]
    
    # Skills metrics
    all_skills = set(roadmap.get("matched_skills", []) + roadmap.get("missing_skills", []))
    completed_skills_list = progress.get("completed_skills", []) if progress else []
    completed_skills_list = list(set(completed_skills_list + roadmap.get("matched_skills", [])))
    remaining_skills_list = list(all_skills - set(completed_skills_list))
    
    # Estimated ready date
    weeks_left = max(0, roadmap["total_weeks"] - len(progress.get("completed_weeks", []) if progress else []))
    ready_date = (datetime.utcnow() + timedelta(weeks=weeks_left)).strftime("%b %d, %Y")
    
    # Recent activity
    recent_activity = []
    # Join achievements/badges as activity list
    for b in badges:
        if b.get("unlocked_date"):
            recent_activity.append({
                "type": "badge",
                "title": f"Unlocked badge: {b['name']}",
                "timestamp": b["unlocked_date"],
                "emoji": b["emoji"]
            })
            
    for ach in achievements:
        recent_activity.append({
            "type": "achievement",
            "title": ach["name"],
            "timestamp": ach["unlocked_date"],
            "emoji": "🏆"
        })
        
    # Sort activity by timestamp
    recent_activity = sorted(recent_activity, key=lambda x: x["timestamp"], reverse=True)[:5]
    
    return BaseResponse(
        success=True,
        data={
            "has_active_roadmap": True,
            "roadmap_id": roadmap_id,
            "career_goal": roadmap["career"],
            "current_readiness": progress.get("current_readiness", 50) if progress else 50,
            "projected_readiness": roadmap["expected_readiness"],
            "roadmap_progress": progress.get("current_roadmap_completion", 0.0) if progress else 0.0,
            "completed_tasks": len(completed_tasks),
            "remaining_tasks": len(remaining_tasks),
            "completed_skills": completed_skills_list,
            "remaining_skills": remaining_skills_list,
            "achievements": achievements,
            "badges": badges,
            "estimated_job_ready_date": ready_date,
            "recent_activity": recent_activity,
            "success_probability": analytics.get("success_probability", 60) if analytics else 60
        },
        message="User dashboard statistics aggregated."
    )

@router.get("/dashboard/summary", response_model=BaseResponse[Dict[str, Any]])
async def get_dashboard_summary_endpoint(
    response: Response,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Aggregates all user, profile, active roadmap, progress, analytics, badges,
    achievements, and resume history details in a single, high-performance request.
    Data is safe to cache privately for 30 s; stale-while-revalidate allows
    background refresh for up to 60 s after expiry.
    """
    # Override the global no-store default set by the security-headers middleware
    response.headers["Cache-Control"] = "private, max-age=30, stale-while-revalidate=60"
    try:
        user_id = current_user["id"]
        summary = get_dashboard_summary(user_id)
        
        profile = summary.get("profile") or {}
        roadmap = summary.get("roadmap")
        progress = summary.get("progress")
        analytics = summary.get("analytics")
        badges = summary.get("badges") or []
        achievements = summary.get("achievements") or []
        history = summary.get("history") or []
        milestones = summary.get("milestones") or []
        tasks = summary.get("tasks") or []

        has_active_roadmap = roadmap is not None
        
        completed_tasks_count = 0
        remaining_tasks_count = 0
        if tasks:
            completed_tasks_count = len([t for t in tasks if t.get("status") == "Completed"])
            remaining_tasks_count = len([t for t in tasks if t.get("status") not in ["Completed", "Skipped"]])

        completed_skills = []
        remaining_skills = []
        if roadmap:
            all_skills = set(roadmap.get("matched_skills", []) + roadmap.get("missing_skills", []))
            completed_skills = progress.get("completed_skills", []) if progress else []
            completed_skills = list(set(completed_skills + roadmap.get("matched_skills", [])))
            remaining_skills = list(all_skills - set(completed_skills))

        from datetime import datetime, timedelta
        if roadmap and progress:
            weeks_left = max(0, roadmap.get("total_weeks", 4) - len(progress.get("completed_weeks", []) or []))
            ready_date = (datetime.utcnow() + timedelta(weeks=weeks_left)).strftime("%b %d, %Y")
        else:
            ready_date = "N/A"

        # Calculate recent activity
        recent_activity = []
        for b in badges:
            if b.get("unlocked_date"):
                ts = b["unlocked_date"]
                recent_activity.append({
                    "type": "badge",
                    "title": f"Unlocked badge: {b['name']}",
                    "timestamp": ts.isoformat() if hasattr(ts, "isoformat") else str(ts),
                    "emoji": b["emoji"]
                })
        for ach in achievements:
            ts = ach.get("unlocked_date")
            recent_activity.append({
                "type": "achievement",
                "title": ach.get("name"),
                "timestamp": ts.isoformat() if hasattr(ts, "isoformat") else str(ts),
                "emoji": "🏆"
            })
        recent_activity = sorted(recent_activity, key=lambda x: x["timestamp"], reverse=True)[:5]

        # Format timestamps safely for JSON serialization
        for item in history:
            if "created_at" in item and hasattr(item["created_at"], "isoformat"):
                item["created_at"] = item["created_at"].isoformat()

        response_data = {
            "has_active_roadmap": has_active_roadmap,
            "profile": {
                "id": profile.get("id"),
                "email": profile.get("email"),
                "name": profile.get("name"),
                "picture": profile.get("picture"),
                "joined_date": profile.get("joined_date").isoformat() if hasattr(profile.get("joined_date"), "isoformat") else str(profile.get("joined_date")),
                "current_career_goal": profile.get("current_career_goal")
            },
            "readiness": {
                "current_readiness": progress.get("current_readiness", 50) if progress else (profile.get("current_readiness_score") or 50),
                "projected_readiness": roadmap.get("expected_readiness", 90) if roadmap else 0,
                "success_probability": analytics.get("success_probability", 60) if analytics else 60,
                "estimated_job_ready_date": ready_date
            },
            "progress": {
                "roadmap_progress": progress.get("current_roadmap_completion", 0.0) if progress else 0.0,
                "completed_tasks": completed_tasks_count,
                "remaining_tasks": remaining_tasks_count,
                "completed_skills": completed_skills,
                "remaining_skills": remaining_skills
            },
            "roadmap": roadmap,
            "milestones": milestones,
            "tasks": tasks,
            "analytics": analytics,
            "badges": badges,
            "achievements": achievements,
            "history": history,
            "recent_activity": recent_activity
        }
        
        return BaseResponse(
            success=True,
            data=response_data,
            message="Dashboard summary aggregated successfully."
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise AppException(message=f"Failed to load dashboard summary: {str(e)}", status_code=500)
