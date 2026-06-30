import os
import tempfile
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Request, Header
from domain.schemas.resume import ResumeParseData
from domain.schemas.extraction import ExtractionRequest, ResumeExtractionData
from services.resume_service import ResumeService
from services.extraction_service import ExtractionService
from core.response import BaseResponse
from core.exceptions import FileValidationException, AppException
from utils.file_validators import validate_pdf_magic_bytes, validate_file_size
from core.config import settings
from core.firebase_client import verify_firebase_token
from core.database import save_current_resume, ensure_user_exists

router = APIRouter()

@router.post(
    "/upload", 
    response_model=BaseResponse[ResumeParseData],
    summary="Upload and parse a PDF resume",
    description="Accepts a PDF file, validates its format (magic bytes) and size, extracts its text using pdfplumber, and returns structured metadata including filename, size, page count, and the extracted text content. The uploaded file is temporarily stored and immediately deleted after processing."
)
async def upload_resume(request: Request, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise FileValidationException("Only PDF files are supported.")
        
    file_content = await file.read()
    file_size = len(file_content)
    
    validate_file_size(file_size, settings.MAX_UPLOAD_SIZE)
    validate_pdf_magic_bytes(file_content)
    
    # User Requirement: Save uploaded PDF to a temporary file, process, and delete.
    temp_file_path = None
    try:
        # Create a named temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
            
        # Parse text from the temporary file
        result = ResumeService.extract_text_from_pdf(temp_file_path, file.filename, file_size)
        
        return BaseResponse(
            success=True,
            data=ResumeParseData(**result),
            message="Resume parsed successfully."
        )
    finally:
        # Ensure cleanup even if an exception occurs
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@router.post(
    "/extract",
    response_model=BaseResponse[ResumeExtractionData],
    summary="Extract structured information from resume text",
    description="Accepts raw resume text, parses sections and fields (name, email, phone, linkedin, skills, education, projects, certifications), and returns structured JSON details. Also saves it to resume history if user is authenticated."
)
async def extract_resume_info(payload: ExtractionRequest, authorization: Optional[str] = Header(None)):
    try:
        extracted_data = ExtractionService.extract_information(payload.text_content)
        
        # If user is authenticated, save the resume history
        if authorization and authorization.startswith("Bearer "):
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

                # Save to DB
                data_dict = extracted_data.model_dump() if hasattr(extracted_data, "model_dump") else dict(extracted_data)
                resume_id = save_current_resume(
                    user_id=resolved_user_id,
                    resume_file_url="local_text_only",
                    resume_text=payload.text_content,
                    parsed_data=data_dict
                )
                # Set resume_id in output schema
                extracted_data.resume_id = resume_id

        return BaseResponse(
            success=True,
            data=extracted_data,
            message="Resume information extracted successfully."
        )
    except Exception as e:
        raise AppException(message=f"Failed to extract information: {str(e)}", status_code=500)

