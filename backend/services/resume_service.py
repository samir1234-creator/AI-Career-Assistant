import os
import tempfile
import pdfplumber
from core.exceptions import PDFParsingException

class ResumeService:
    @staticmethod
    def extract_text_from_pdf(file_path: str, filename: str, file_size: int) -> dict:
        """
        Extracts text from a validated PDF file located at file_path.
        Handles corruption and empty PDFs.
        """
        extracted_text = ""
        page_count = 0
        
        try:
            with pdfplumber.open(file_path) as pdf:
                page_count = len(pdf.pages)
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        extracted_text += text + "\n"
        except Exception as e:
            raise PDFParsingException(f"Failed to read PDF file. It might be corrupted. Details: {str(e)}")
            
        cleaned_text = extracted_text.strip()
        
        if not cleaned_text:
            raise PDFParsingException("The uploaded PDF appears to be empty or contains no extractable text (e.g., it is an image-based PDF without OCR).")
            
        return {
            "filename": filename,
            "file_size_bytes": file_size,
            "page_count": page_count,
            "text_content": cleaned_text
        }
