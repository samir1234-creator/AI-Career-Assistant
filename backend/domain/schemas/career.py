from pydantic import BaseModel, Field
from typing import List, Optional

class CareerRecommendationRequest(BaseModel):
    skills: List[str] = Field(default_factory=list, description="List of technical skills")
    projects: List[str] = Field(default_factory=list, description="List of project/work entries")
    education: List[str] = Field(default_factory=list, description="List of education records")
    certifications: List[str] = Field(default_factory=list, description="List of certifications")
    ats_score: int = Field(0, description="Overall ATS compatibility score (out of 100)")
    resume_id: Optional[str] = Field(None, description="Optional associated resume UUID")

class CareerRecommendation(BaseModel):
    role: str = Field(..., description="The recommended career role title")
    category: str = Field(..., description="The category of the career")
    description: str = Field(..., description="A brief description of the role")
    match_score: int = Field(..., description="The matching percentage score (0-100)")
    reason: List[str] = Field(default_factory=list, description="Actionable lists of reasons explaining the match")
    difficulty_level: str = Field(..., description="The difficulty level of the career path")
    growth_level: str = Field(..., description="The career growth level")
    future_demand: str = Field(..., description="The future demand level")
    related_careers: List[str] = Field(default_factory=list, description="List of related careers")
    required_skills: List[str] = Field(default_factory=list, description="List of required skills for the career")
    preferred_skills: List[str] = Field(default_factory=list, description="List of preferred skills for the career")


class CareerRecommendationResponse(BaseModel):
    recommended_careers: List[CareerRecommendation] = Field(default_factory=list, description="Sorted list of recommended careers")
