from typing import Optional
from fastapi import APIRouter, Header
from domain.schemas.career import CareerRecommendationRequest, CareerRecommendationResponse
from services.career_recommendation_service import CareerRecommendationService
from core.response import BaseResponse
from core.exceptions import AppException
from core.firebase_client import verify_firebase_token
from core.database import create_career_recommendations, ensure_user_exists

router = APIRouter()
career_service = CareerRecommendationService()

@router.post(
    "/recommend",
    response_model=BaseResponse[CareerRecommendationResponse],
    summary="Recommend top 5 career paths",
    description="Accepts candidate skills, projects, education, certifications, and ATS score, calculates match ratings locally, and returns the top 5 sorted career recommendations with reasoning. Also saves to DB if authenticated."
)
async def recommend_careers(payload: CareerRecommendationRequest, authorization: Optional[str] = Header(None)):
    try:
        recommendations = career_service.calculate_recommendations(payload)

        # Save to DB if authenticated and resume_id is present
        if authorization and authorization.startswith("Bearer ") and payload.resume_id:
            token = authorization.split(" ")[1]
            user_payload = verify_firebase_token(token)
            if user_payload and "sub" in user_payload:
                # ── CRITICAL FIX: guarantee user row exists before FK INSERT ──
                resolved_user_id = ensure_user_exists(
                    firebase_uid=user_payload["firebase_uid"],
                    email=user_payload["email"],
                    name=user_payload["name"],
                    picture=user_payload["picture"],
                    db_uuid=user_payload["sub"]
                )
                # Convert list of pydantic models to dict list
                recs_dict_list = [r.model_dump() if hasattr(r, "model_dump") else dict(r) for r in recommendations]
                create_career_recommendations(
                    user_id=resolved_user_id,
                    resume_id=payload.resume_id,
                    recommendations=recs_dict_list
                )

        return BaseResponse(
            success=True,
            data=CareerRecommendationResponse(recommended_careers=recommendations),
            message="Career recommendations generated successfully."
        )
    except Exception as e:
        raise AppException(message=f"Failed to generate career recommendations: {str(e)}", status_code=500)
