from fastapi import APIRouter
from domain.schemas.career import CareerRecommendationRequest, CareerRecommendationResponse
from services.career_recommendation_service import CareerRecommendationService
from core.response import BaseResponse
from core.exceptions import AppException

router = APIRouter()
career_service = CareerRecommendationService()

@router.post(
    "/recommend",
    response_model=BaseResponse[CareerRecommendationResponse],
    summary="Recommend top 5 career paths",
    description="Accepts candidate skills, projects, education, certifications, and ATS score, calculates match ratings locally, and returns the top 5 sorted career recommendations with reasoning."
)
async def recommend_careers(payload: CareerRecommendationRequest):
    try:
        recommendations = career_service.calculate_recommendations(payload)
        return BaseResponse(
            success=True,
            data=CareerRecommendationResponse(recommended_careers=recommendations),
            message="Career recommendations generated successfully."
        )
    except Exception as e:
        raise AppException(message=f"Failed to generate career recommendations: {str(e)}", status_code=500)
