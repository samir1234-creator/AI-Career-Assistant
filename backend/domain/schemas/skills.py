from pydantic import BaseModel, Field
from typing import List

class SkillClassificationRequest(BaseModel):
    skills: List[str] = Field(..., description="List of raw skill strings to enrich and categorize")

class EnrichedSkill(BaseModel):
    name: str = Field(..., description="The canonical name of the skill")
    category: str = Field(..., description="The singular category name of the skill")

class SkillClassificationResponse(BaseModel):
    skills: List[EnrichedSkill] = Field(default_factory=list, description="List of categorized and enriched skills")
