from fastapi import APIRouter
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

router = APIRouter()
roadmap_service = RoadmapService()
share_service = RoadmapShareService()


@router.post(
    "/generate",
    response_model=BaseResponse[RoadmapResponse],
    summary="Generate personalized learning roadmap",
    description="Generates a dependency-aware weekly/monthly roadmap with job market intelligence, career forecasting, and personalized timeline estimation."
)
async def generate_roadmap(payload: RoadmapRequest):
    try:
        roadmap = roadmap_service.create_roadmap(payload)
        return BaseResponse(
            success=True,
            data=roadmap,
            message="Learning roadmap generated successfully."
        )
    except Exception as e:
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
