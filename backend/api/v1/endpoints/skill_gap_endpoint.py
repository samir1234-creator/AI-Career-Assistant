from fastapi import APIRouter
from domain.schemas.skill_gap_schema import SkillGapRequest, SkillGapResponse
from services.skill_gap_analysis_service import SkillGapAnalysisService
from core.response import BaseResponse
from core.exceptions import AppException

router = APIRouter()
skill_gap_service = SkillGapAnalysisService()

@router.post(
    "/analyze",
    response_model=BaseResponse[SkillGapResponse],
    summary="Analyze skill gap for a target career path",
    description="Accepts target career name along with candidate matched and missing skills, and computes detailed skill gap metrics including readiness score, priorities, impact scores, learning times, gap severity, and key insights."
)
async def analyze_skill_gap(payload: SkillGapRequest):
    try:
        analysis = skill_gap_service.analyze_gap(payload)
        return BaseResponse(
            success=True,
            data=analysis,
            message="Skill gap analysis completed successfully."
        )
    except Exception as e:
        raise AppException(message=f"Failed to analyze skill gap: {str(e)}", status_code=500)
