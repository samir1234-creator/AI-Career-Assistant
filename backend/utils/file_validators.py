from core.exceptions import FileValidationException

def validate_pdf_magic_bytes(file_content: bytes):
    """
    Validates if the file content starts with the PDF magic bytes (%PDF-).
    """
    if not file_content.startswith(b"%PDF-"):
        raise FileValidationException("Invalid file format. File does not appear to be a valid PDF.")

def validate_file_size(file_size: int, max_size: int):
    """
    Validates that the file size does not exceed the maximum allowed size.
    """
    if file_size > max_size:
        raise FileValidationException(f"File too large. Max size is {max_size / (1024 * 1024)}MB.")
