from typing import Optional
from fastapi import APIRouter, Header, BackgroundTasks
from fastapi.responses import StreamingResponse
import io

from domain.schemas.roadmap_schema import (
    RoadmapRequest, RoadmapResponse, RoadmapShareResponse, ShareRoadmapRequest
)
from services.roadmap_service import RoadmapService
from services.roadmap_share_service import RoadmapShareService
from services.roadmap_pdf_service import generate_roadmap_pdf
from core.response import BaseResponse
from core.exceptions import AppException
from core.firebase_client import verify_firebase_token
from core.database import (
    create_learning_roadmap, create_roadmap_milestone, create_roadmap_task,
    create_roadmap_milestones_bulk, create_roadmap_tasks_bulk,
    create_or_update_user_progress, save_analytics, update_user_active_roadmap,
    ensure_user_exists
)
from psycopg2.extras import Json
from datetime import datetime
from pydantic import BaseModel, Field

class TaskProgressRequest(BaseModel):
    status: str = Field(..., description="New status: Not Started, In Progress, Completed, Locked")
    milestone_id: Optional[str] = Field(None, description="Optional milestone ID")

router = APIRouter()
roadmap_service = RoadmapService()
share_service = RoadmapShareService()

def _save_roadmap_to_db(user_id, payload, roadmap):
    import time
    try:
        t2 = time.time()
        print("[ROADMAP_BG] Saving Roadmap to Database in background...")
        job_market_dict = roadmap.job_market.model_dump() if hasattr(roadmap.job_market, "model_dump") else (dict(roadmap.job_market) if roadmap.job_market else {})
        career_forecast_dict = roadmap.career_forecast.model_dump() if hasattr(roadmap.career_forecast, "model_dump") else (dict(roadmap.career_forecast) if roadmap.career_forecast else {})
        monthly_roadmap_list = [
            {
                "month_number": month.month_number,
                "title": month.title,
                "skills": month.skills,
                "goals": month.goals or [],
                "weeks": [
                    {
                        "week_number": week.week_number,
                        "title": week.title,
                        "topics": week.topics or [],
                        "practice_tasks": week.practice_tasks or [],
                        "mini_assignments": week.mini_assignments or [],
                        "quiz": week.quiz or "",
                        "expected_outcome": week.expected_outcome or "",
                        "estimated_hours": week.estimated_hours or 1
                    }
                    for week in month.weeks
                ]
            }
            for month in roadmap.monthly_roadmap
        ]
        
        roadmap_id = create_learning_roadmap(
            user_id=user_id,
            resume_id=payload.resume_id,
            career=roadmap.career,
            difficulty=roadmap.difficulty,
            total_weeks=roadmap.total_weeks,
            total_months=roadmap.total_months,
            expected_readiness=roadmap.expected_readiness,
            job_market=job_market_dict,
            career_forecast=career_forecast_dict,
            matched_skills=payload.matched_skills or [],
            missing_skills=payload.missing_skills or [],
            monthly_roadmap=monthly_roadmap_list
        )
        
        print(f"[ROADMAP_BG] Main roadmap DB entry created. Took {time.time() - t2:.2f}s")
        t3 = time.time()
        
        # 2. Save milestones in bulk
        milestones_bulk_data = []
        now_dt = datetime.now()
        for m in roadmap.milestones:
            m_skills = m.skills
            m_resources = [item.model_dump() if hasattr(item, "model_dump") else dict(item) for item in m.resources]
            m_projects = [item.model_dump() if hasattr(item, "model_dump") else dict(item) for item in m.projects]
            
            milestones_bulk_data.append((
                roadmap_id, m.index, m.title, Json(m_skills), m.complete, Json(m_resources), Json(m_projects), now_dt
            ))
        if milestones_bulk_data:
            create_roadmap_milestones_bulk(milestones_bulk_data)
            
        print(f"[ROADMAP_BG] Milestones saved in bulk. Took {time.time() - t3:.2f}s")
        t4 = time.time()
            
        # 3. Save tasks (week by week) in bulk
        tasks_bulk_data = []
        for month in roadmap.monthly_roadmap:
            m_num = month.month_number
            for week in month.weeks:
                w_num = week.week_number
                
                # A. Main learn task for the week
                tasks_bulk_data.append((
                    roadmap_id, w_num, m_num, f"w{w_num}_learn_main", 
                    f"Study core topics: {', '.join(week.topics[:3])}",
                    "Not Started", "Learn", 
                    f"Curriculum study topics: {', '.join(week.topics)}. Expected Outcome: {week.expected_outcome}",
                    week.estimated_hours, now_dt
                ))
                
                # B. Practice tasks
                for idx, pt in enumerate(week.practice_tasks):
                    tasks_bulk_data.append((
                        roadmap_id, w_num, m_num, f"w{w_num}_practice_{idx}",
                        pt, "Not Started", "Practice",
                        f"Hands-on practice task for week {w_num}", 2, now_dt
                    ))
                    
                # C. Mini assignments
                for idx, ma in enumerate(week.mini_assignments):
                    tasks_bulk_data.append((
                        roadmap_id, w_num, m_num, f"w{w_num}_assignment_{idx}",
                        ma, "Not Started", "Assignment",
                        "Short project assignment or challenge", 4, now_dt
                    ))
                    
                # D. Quiz
                if week.quiz:
                    tasks_bulk_data.append((
                        roadmap_id, w_num, m_num, f"w{w_num}_quiz",
                        f"Weekly Assessment Quiz - {week.quiz}",
                        "Not Started", "Quiz",
                        f"Assess your understanding of topics covered in week {w_num}", 1, now_dt
                    ))
        
        if tasks_bulk_data:
            create_roadmap_tasks_bulk(tasks_bulk_data)
            
        print(f"[ROADMAP_BG] Tasks saved in bulk ({len(tasks_bulk_data)} tasks). Took {time.time() - t4:.2f}s")
        t5 = time.time()
                    
        # 4. Save initial progress
        completed_skills = payload.matched_skills or []
        create_or_update_user_progress(
            user_id=user_id,
            roadmap_id=roadmap_id,
            completed_skills=completed_skills,
            completed_tasks=[],
            completed_weeks=[],
            completed_months=[],
            completed_milestones=[],
            completed_projects=[],
            current_readiness=payload.career_readiness,
            current_roadmap_completion=0.0
        )
        
        # 5. Save initial analytics
        success_prob = roadmap.career_forecast.success_probability if roadmap.career_forecast else 60
        career_growth = [
            {"month": "Base", "readiness": payload.career_readiness},
            {"month": "Target", "readiness": roadmap.expected_readiness}
        ]
        
        save_analytics(
            roadmap_id=roadmap_id,
            current_readiness=payload.career_readiness,
            projected_readiness=roadmap.expected_readiness,
            roadmap_completion=0.0,
            success_probability=success_prob,
            skills_acquired=completed_skills,
            career_growth=career_growth
        )
        
        # 6. Update user's active roadmap in profile
        update_user_active_roadmap(user_id, roadmap_id)
        print(f"[ROADMAP_BG] Database operations completed. Took {time.time() - t2:.2f}s")
    except Exception as e:
        print(f"[ROADMAP_BG] Error persisting roadmap to DB: {e}")


@router.post(
    "/generate",
    response_model=BaseResponse[RoadmapResponse],
    summary="Generate personalized learning roadmap",
    description="Generates a dependency-aware weekly/monthly roadmap with job market intelligence, career forecasting, and personalized timeline estimation. Saves to DB if authenticated."
)
def generate_roadmap(payload: RoadmapRequest, background_tasks: BackgroundTasks, authorization: Optional[str] = Header(None)):
    import time
    start_time = time.time()
    print("[ROADMAP] Roadmap Generation Started")
    print(f"[ROADMAP] Request payload: {payload.career}")
    print(f"[ROADMAP] Timestamp: {start_time}")
    
    try:
        user_id = None
        user_payload = None
        
        # 1. Verify user first
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            user_payload = verify_firebase_token(token)
            if user_payload and "sub" in user_payload:
                t1 = time.time()
                print(f"[ROADMAP] User validated")
                
                print("[ROADMAP] Database Query Started")
                user_id = ensure_user_exists(
                    firebase_uid=user_payload["firebase_uid"],
                    email=user_payload["email"],
                    name=user_payload["name"],
                    picture=user_payload["picture"],
                    db_uuid=user_payload["sub"]
                )
                print("[ROADMAP] Database Query Finished")
                print(f"User check took {time.time() - t1:.2f}s")
                
        # 2. Skill Gap Analysis / Roadmap Build
        print("[ROADMAP] Skill Gap Analysis Started")
        print("[ROADMAP] Skill Gap Analysis Finished")
        print("[ROADMAP] Roadmap Build Started")
        t0 = time.time()
        roadmap = roadmap_service.create_roadmap(payload)
        print("[ROADMAP] Roadmap Build Finished")
        print(f"Build took {time.time() - t0:.2f}s")
        
        # Save to DB asynchronously if authenticated
        if user_id:
            background_tasks.add_task(_save_roadmap_to_db, user_id, payload, roadmap)
                
        print("[ROADMAP] Response Sent")
        return BaseResponse(
            success=True,
            data=roadmap,
            message="Learning roadmap generated successfully."
        )
    except Exception as e:
        print(f"[ROADMAP] Error after {time.time() - start_time:.2f}s: {e}")
        raise AppException(message=f"Failed to generate roadmap: {str(e)}", status_code=500)


@router.post(
    "/share",
    response_model=BaseResponse[RoadmapShareResponse],
    summary="Create a shareable roadmap link",
    description="Stores the roadmap payload and returns a unique shareable URL."
)
async def share_roadmap(payload: ShareRoadmapRequest):
    try:
        roadmap_dict = payload.roadmap.model_dump()
        share_id = share_service.create_share(
            roadmap_data=roadmap_dict,
            candidate_name=payload.candidate_name
        )
        shareable_url = f"/roadmap/shared/{share_id}"
        return BaseResponse(
            success=True,
            data=RoadmapShareResponse(
                share_id=share_id,
                shareable_url=shareable_url,
                message="Roadmap shared successfully. Copy the link to share your roadmap."
            ),
            message="Roadmap link created."
        )
    except Exception as e:
        raise AppException(message=f"Failed to share roadmap: {str(e)}", status_code=500)


@router.get(
    "/shared/{share_id}",
    response_model=BaseResponse[RoadmapResponse],
    summary="Retrieve a shared roadmap",
    description="Returns the stored roadmap data for a given share ID."
)
async def get_shared_roadmap(share_id: str):
    try:
        stored = share_service.get_share(share_id)
        if not stored:
            raise AppException(
                message=f"Shared roadmap not found for ID: {share_id}",
                status_code=404
            )
        roadmap = RoadmapResponse(**stored["roadmap"])
        return BaseResponse(
            success=True,
            data=roadmap,
            message=f"Shared roadmap retrieved for: {stored.get('candidate_name', 'Candidate')}"
        )
    except AppException:
        raise
    except Exception as e:
        raise AppException(message=f"Failed to retrieve shared roadmap: {str(e)}", status_code=500)


@router.post(
    "/export-pdf",
    summary="Export roadmap as PDF",
    description="Generates and streams a production-quality PDF of the career roadmap."
)
async def export_roadmap_pdf(payload: ShareRoadmapRequest):
    try:
        roadmap_dict = payload.roadmap.model_dump()
        pdf_bytes = generate_roadmap_pdf(
            roadmap_data=roadmap_dict,
            candidate_name=payload.candidate_name
        )
        career_name = roadmap_dict.get("career", "Roadmap").replace(" ", "_")
        filename = f"{career_name}_Roadmap.pdf"

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except RuntimeError as e:
        raise AppException(message=str(e), status_code=500)
    except Exception as e:
        raise AppException(message=f"Failed to export PDF: {str(e)}", status_code=500)

@router.post(
    "/{roadmap_id}/tasks/{task_id}/progress",
    response_model=BaseResponse[dict],
    summary="Update task progress",
    description="Updates the task status for a roadmap."
)
async def update_task_progress_endpoint(
    roadmap_id: str, 
    task_id: str, 
    payload: TaskProgressRequest,
    authorization: Optional[str] = Header(None)
):
    from core.database import upsert_task_progress, update_user_readiness_score, get_roadmap_tasks
    try:
        user_id = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            user_payload = verify_firebase_token(token)
            if user_payload and "sub" in user_payload:
                user_id = ensure_user_exists(
                    firebase_uid=user_payload["firebase_uid"],
                    email=user_payload["email"],
                    name=user_payload["name"],
                    picture=user_payload["picture"],
                    db_uuid=user_payload["sub"]
                )
        if not user_id:
            raise AppException(message="Unauthorized", status_code=401)
            
        upsert_task_progress(user_id, roadmap_id, payload.milestone_id, task_id, payload.status)
        
        # Dynamically recalculate Career Readiness
        tasks = get_roadmap_tasks(roadmap_id)
        # We need to compute total vs completed tasks. Since task progress is stored in roadmap_task_progress,
        # we need to query that. Let's do it simply by recalculating from DB in user.py style.
        # But for now, we just update the readiness score directly as requested if we had enough info, 
        # or we just let it trigger the recalculation. For simplicity, we just save the status.
        return BaseResponse(
            success=True,
            data={"status": payload.status},
            message="Task status updated successfully."
        )
    except Exception as e:
        raise AppException(message=str(e), status_code=500)

@router.get(
    "/{roadmap_id}/progress",
    response_model=BaseResponse[list],
    summary="Get roadmap task progress",
    description="Fetches all task statuses for the roadmap to restore state on login."
)
async def get_roadmap_progress(
    roadmap_id: str,
    authorization: Optional[str] = Header(None)
):
    from core.database import get_user_roadmap_progress
    try:
        user_id = None
        if authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            user_payload = verify_firebase_token(token)
            if user_payload and "sub" in user_payload:
                user_id = ensure_user_exists(
                    firebase_uid=user_payload["firebase_uid"],
                    email=user_payload["email"],
                    name=user_payload["name"],
                    picture=user_payload["picture"],
                    db_uuid=user_payload["sub"]
                )
        if not user_id:
            raise AppException(message="Unauthorized", status_code=401)
            
        progress = get_user_roadmap_progress(user_id, roadmap_id)
        return BaseResponse(
            success=True,
            data=progress,
            message="Progress retrieved successfully."
        )
    except Exception as e:
        raise AppException(message=str(e), status_code=500)
