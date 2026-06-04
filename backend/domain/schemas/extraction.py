from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractionRequest(BaseModel):
    text_content: str

class ResumeExtractionData(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
