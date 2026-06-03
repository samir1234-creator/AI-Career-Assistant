from pydantic import BaseModel

class ResumeParseData(BaseModel):
    filename: str
    file_size_bytes: int
    page_count: int
    text_content: str
