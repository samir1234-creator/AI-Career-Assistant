from fastapi import APIRouter
from domain.schemas.skills import SkillClassificationRequest, SkillClassificationResponse, EnrichedSkill
from services.skill_intelligence_service import SkillIntelligenceService
from core.response import BaseResponse
from core.exceptions import AppException

router = APIRouter()
skills_service = SkillIntelligenceService()

@router.post(
    "/classify",
    response_model=BaseResponse[SkillClassificationResponse],
    summary="Classify and enrich skills list",
    description="Accepts a list of raw skill strings, normalizes their spacing and casing, matches them against a taxonomy of 10 technology categories, deduplicates them, and returns the categorized and canonicalized list."
)
async def classify_skills(payload: SkillClassificationRequest):
    try:
        enriched = skills_service.classify_skills(payload.skills)
        enriched_skills_models = [EnrichedSkill(**item) for item in enriched]
        
        return BaseResponse(
            success=True,
            data=SkillClassificationResponse(skills=enriched_skills_models),
            message="Skills classified and enriched successfully."
        )
    except Exception as e:
        raise AppException(message=f"Failed to classify skills: {str(e)}", status_code=500)
