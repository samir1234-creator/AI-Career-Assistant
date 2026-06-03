class AppException(Exception):
    """Base application exception."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class FileValidationException(AppException):
    """Exception raised for file validation errors."""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=400)

class PDFParsingException(AppException):
    """Exception raised for errors during PDF parsing."""
    def __init__(self, message: str):
        super().__init__(message=message, status_code=422)
