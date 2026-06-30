from typing import Optional
from fastapi import APIRouter, Header
from domain.schemas.skill_gap_schema import SkillGapRequest, SkillGapResponse
from services.skill_gap_analysis_service import SkillGapAnalysisService
from core.response import BaseResponse
from core.exceptions import AppException
from core.firebase_client import verify_firebase_token
from core.database import create_skill_gap_report, update_user_career_goal, ensure_user_exists

router = APIRouter()
skill_gap_service = SkillGapAnalysisService()

@router.post(
    "/analyze",
    response_model=BaseResponse[SkillGapResponse],
    summary="Analyze skill gap for a target career path",
    description="Accepts target career name along with candidate matched and missing skills, and computes detailed skill gap metrics including readiness score, priorities, impact scores, learning times, gap severity, and key insights. Also saves report and goal if authenticated."
)
async def analyze_skill_gap(payload: SkillGapRequest, authorization: Optional[str] = Header(None)):
    try:
        analysis = skill_gap_service.analyze_gap(payload)
        
        # Save to DB if authenticated and resume_id is present
        if authorization and authorization.startswith("Bearer ") and payload.resume_id:
            token = authorization.split(" ")[1]
            user_payload = verify_firebase_token(token)
            if user_payload and "sub" in user_payload:
                # CRITICAL FIX: Guarantee user exists before FK-referencing INSERTs.
                resolved_user_id = ensure_user_exists(
                    firebase_uid=user_payload["firebase_uid"],
                    email=user_payload["email"],
                    name=user_payload["name"],
                    picture=user_payload["picture"],
                    db_uuid=user_payload["sub"]
                )

                # 1. Update target career goal in profile
                update_user_career_goal(resolved_user_id, payload.career)

                # 2. Save skill gap report details
                priority_ranking = [item.model_dump() if hasattr(item, "model_dump") else dict(item) for item in analysis.roadmap_compatibility]
                create_skill_gap_report(
                    user_id=resolved_user_id,
                    resume_id=payload.resume_id,
                    career_goal=payload.career,
                    matched_skills=payload.matched_skills,
                    missing_skills=payload.missing_skills,
                    priority_ranking=priority_ranking,
                    readiness_score=analysis.career_readiness
                )
                
        return BaseResponse(
            success=True,
            data=analysis,
            message="Skill gap analysis completed successfully."
        )
    except Exception as e:
        raise AppException(message=f"Failed to analyze skill gap: {str(e)}", status_code=500)
