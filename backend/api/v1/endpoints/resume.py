import os
import tempfile
from fastapi import APIRouter, UploadFile, File, Request
from domain.schemas.resume import ResumeParseData
from services.resume_service import ResumeService
from core.response import BaseResponse
from core.exceptions import FileValidationException
from utils.file_validators import validate_pdf_magic_bytes, validate_file_size
from core.config import settings

router = APIRouter()

@router.post("/upload", response_model=BaseResponse[ResumeParseData])
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
