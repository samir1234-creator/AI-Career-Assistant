from fastapi import APIRouter
from domain.schemas.ats import ATSScoringRequest, ATSScoringResponse
from services.ats_scoring_service import ATSScoringService
from core.response import BaseResponse
from core.exceptions import AppException

router = APIRouter()
ats_service = ATSScoringService()

@router.post(
    "/score",
    response_model=BaseResponse[ATSScoringResponse],
    summary="Calculate ATS compatibility score",
    description="Accepts structured resume data and returns an ATS compatibility score, detailed breakdown, strengths, weaknesses, and recommendations."
)
async def calculate_ats_score(payload: ATSScoringRequest):
    try:
        score_data = ats_service.calculate_score(payload)
        return BaseResponse(
            success=True,
            data=score_data,
            message="ATS score calculated successfully."
        )
    except Exception as e:
        raise AppException(message=f"Failed to calculate ATS score: {str(e)}", status_code=500)
