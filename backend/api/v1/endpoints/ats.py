from typing import Optional
from fastapi import APIRouter, Header
from domain.schemas.ats import ATSScoringRequest, ATSScoringResponse
from services.ats_scoring_service import ATSScoringService
from core.response import BaseResponse
from core.exceptions import AppException
from core.firebase_client import verify_firebase_token
from core.database import create_ats_report, ensure_user_exists

router = APIRouter()
ats_service = ATSScoringService()

@router.post(
    "/score",
    response_model=BaseResponse[ATSScoringResponse],
    summary="Calculate ATS compatibility score",
    description="Accepts structured resume data and returns an ATS compatibility score, detailed breakdown, strengths, weaknesses, and recommendations. Also saves the report if authenticated."
)
async def calculate_ats_score(payload: ATSScoringRequest, authorization: Optional[str] = Header(None)):
    try:
        score_data = ats_service.calculate_score(payload)
        
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
                # Convert pydantic response model to dict
                score_dict = score_data.model_dump() if hasattr(score_data, "model_dump") else dict(score_data)
                create_ats_report(
                    user_id=resolved_user_id,
                    resume_id=payload.resume_id,
                    ats_score=score_data.ats_score,
                    report_data=score_dict
                )
                
        return BaseResponse(
            success=True,
            data=score_data,
            message="ATS score calculated successfully."
        )
    except Exception as e:
        raise AppException(message=f"Failed to calculate ATS score: {str(e)}", status_code=500)

