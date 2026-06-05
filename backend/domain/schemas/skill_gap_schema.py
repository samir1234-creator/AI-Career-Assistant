from pydantic import BaseModel, Field
from typing import List, Dict

class RoadmapSkillItem(BaseModel):
    skill: str = Field(..., description="The name of the skill")
    priority: str = Field(..., description="Skill priority level (lowercase): critical, important, optional")
    impact_score: int = Field(..., description="Impact score (0-100)")
    learning_time_weeks: int = Field(..., description="Learning time in weeks (integer)")
    dependencies: List[str] = Field(default_factory=list, description="Direct prerequisite skills")

class SkillGapItem(BaseModel):
    skill: str = Field(..., description="The name of the missing skill")
    priority: str = Field(..., description="Skill priority classification: Critical, Important, Optional")
    impact_score: int = Field(..., description="Impact of missing skill on career readiness (0-100)")
    estimated_learning_time: str = Field(..., description="Estimated time required to learn this skill")
    effort_score: str = Field(..., description="Effort required: Low, Medium, High, Very High")

class SkillGapInsights(BaseModel):
    strong_areas: List[str] = Field(default_factory=list, description="Areas where the candidate is strong")
    weak_areas: List[str] = Field(default_factory=list, description="Areas where the candidate needs improvement")
    summary_text: str = Field(..., description="Bulleted summary of candidate foundations and prioritized skills")

class SkillGapRequest(BaseModel):
    career: str = Field(..., description="The target career role title")
    matched_skills: List[str] = Field(default_factory=list, description="List of matched skills")
    missing_skills: List[str] = Field(default_factory=list, description="List of missing skills")
    projects: List[str] = Field(default_factory=list, description="List of projects")
    certifications: List[str] = Field(default_factory=list, description="List of certifications")
    education: List[str] = Field(default_factory=list, description="List of education")
    ats_score: int = Field(70, description="ATS score")

class MilestoneItem(BaseModel):
    index: int = Field(..., description="The sequence index of the milestone")
    title: str = Field(..., description="The title descriptive of the milestone step")
    skills: List[str] = Field(default_factory=list, description="Skills to acquire in this milestone")

class SkillGapResponse(BaseModel):
    career: str = Field(..., description="The target career role title")
    career_readiness: int = Field(..., description="Calculated career readiness percentage (0-100)")
    gap_severity: str = Field(..., description="Gap severity level: Low Gap, Medium Gap, High Gap")
    critical_skills: List[SkillGapItem] = Field(default_factory=list, description="List of missing skills with Critical priority")
    important_skills: List[SkillGapItem] = Field(default_factory=list, description="List of missing skills with Important priority")
    optional_skills: List[SkillGapItem] = Field(default_factory=list, description="List of missing skills with Optional priority")
    insights: SkillGapInsights = Field(..., description="Key insights on strengths and weaknesses")
    career_readiness_level: str = Field(..., description="Career readiness level: Beginner, Early Stage, Developing, Nearly Job Ready, Job Ready")
    
    job_ready_time_weeks: str = Field(..., description="Estimated time to become job ready in weeks range")
    job_ready_time_months: str = Field(..., description="Estimated time to become job ready in months range")
    priority_ranking: List[str] = Field(default_factory=list, description="Exact learning priority ranking order")
    missing_categories: Dict[str, List[str]] = Field(default_factory=dict, description="Missing skills grouped by category")
    roadmap_compatibility: List[RoadmapSkillItem] = Field(default_factory=list, description="Compatibility layer details for Phase 7 roadmap consumption")
    milestones: List[MilestoneItem] = Field(default_factory=list, description="Milestone-based career progression path")

