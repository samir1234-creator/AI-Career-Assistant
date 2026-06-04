from pydantic import BaseModel, Field
from typing import List, Optional

class ATSScoringRequest(BaseModel):
    name: Optional[str] = Field(None, description="Candidate name")
    email: Optional[str] = Field(None, description="Candidate email address")
    phone: Optional[str] = Field(None, description="Candidate phone number")
    linkedin: Optional[str] = Field(None, description="Candidate LinkedIn profile URL")
    skills: List[str] = Field(default_factory=list, description="List of technical skills")
    projects: List[str] = Field(default_factory=list, description="List of project entries/descriptions")
    education: List[str] = Field(default_factory=list, description="List of education records")
    certifications: List[str] = Field(default_factory=list, description="List of certifications")
    achievements: List[str] = Field(default_factory=list, description="List of achievements")

class ScoreBreakdown(BaseModel):
    skills: int = Field(..., description="Technical skills section score (out of 30)")
    projects: int = Field(..., description="Projects & experience section score (out of 25)")
    education: int = Field(..., description="Education section score (out of 15)")
    certifications: int = Field(..., description="Certifications section score (out of 10)")
    achievements: int = Field(..., description="Achievements section score (out of 10)")
    contact: int = Field(..., description="Contact information section score (out of 10)")

class ATSScoringResponse(BaseModel):
    ats_score: int = Field(..., description="Overall ATS compatibility score (out of 100)")
    score_breakdown: ScoreBreakdown = Field(..., description="Score breakdown across categories")
    strengths: List[str] = Field(default_factory=list, description="Actionable strengths found in the resume")
    weaknesses: List[str] = Field(default_factory=list, description="Weaknesses or areas of concern detected")
    recommendations: List[str] = Field(default_factory=list, description="Concrete improvement tips")
