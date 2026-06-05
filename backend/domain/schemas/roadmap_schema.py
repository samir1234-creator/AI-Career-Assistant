from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RoadmapResourceItem(BaseModel):
    name: str = Field(..., description="Curated resource name")
    url: str = Field(..., description="Resource link URL")
    type: str = Field(..., description="Resource type: Course, Book, Documentation, Video, Practice")

class RoadmapProjectItem(BaseModel):
    title: str = Field(..., description="Project title name")
    description: str = Field(..., description="Detailed description of project scope")
    difficulty: str = Field(..., description="Project difficulty level: Beginner, Intermediate, Advanced")
    tech: List[str] = Field(default_factory=list, description="Technologies used in the project")
    estimated_hours: Optional[int] = Field(None, description="Estimated hours to complete the project")

class RoadmapWeeklyPlan(BaseModel):
    week_number: int = Field(..., description="Absolute sequence week number")
    title: str = Field(..., description="Description title for the week")
    description: str = Field("", description="Detailed summary of the week's goals")
    topics: List[str] = Field(default_factory=list, description="Curriculum topics for study")
    resources: List[RoadmapResourceItem] = Field(default_factory=list, description="Curated resource links")
    practice_tasks: List[str] = Field(default_factory=list, description="Hands-on practice exercises")
    mini_assignments: List[str] = Field(default_factory=list, description="Short project assignments or tasks")
    quiz: str = Field("", description="Description of the quiz for the week (e.g. 10 Questions)")
    expected_outcome: str = Field("", description="Target learning outcome of the week")
    estimated_hours: int = Field(8, description="Estimated study hours required")

class RoadmapMonthlyPlan(BaseModel):
    month_number: int = Field(..., description="Chronological sequence month number")
    title: str = Field(..., description="Descriptive title of the monthly subject theme")
    skills: List[str] = Field(default_factory=list, description="Skills focused on during this month")
    goals: List[str] = Field(default_factory=list, description="Milestone learning goals")
    weeks: List[RoadmapWeeklyPlan] = Field(default_factory=list, description="Detailed week-by-week layout")
    projects: List[RoadmapProjectItem] = Field(default_factory=list, description="Recommended portfolio projects")

class RoadmapRequest(BaseModel):
    career: str = Field(..., description="Target career role name")
    matched_skills: List[str] = Field(default_factory=list, description="List of currently possessed skills")
    missing_skills: List[str] = Field(default_factory=list, description="List of missing skills to acquire")
    career_readiness: int = Field(50, description="Base career readiness percentage score")
    projects: List[str] = Field(default_factory=list, description="List of projects")
    certifications: List[str] = Field(default_factory=list, description="List of certifications")
    education: List[str] = Field(default_factory=list, description="List of education")
    ats_score: int = Field(70, description="ATS score")

class MilestoneProgressTracker(BaseModel):
    index: int = Field(..., description="Sequence milestone index")
    title: str = Field(..., description="Title of the milestone step")
    skills: List[str] = Field(default_factory=list, description="Skills associated with this milestone")
    complete: bool = Field(False, description="Whether this milestone is completed")
    resources: List[RoadmapResourceItem] = Field(default_factory=list, description="Resources for this milestone")
    projects: List[RoadmapProjectItem] = Field(default_factory=list, description="Portfolio projects for this milestone")

class RoadmapProgressInfo(BaseModel):
    completion_percentage: int = Field(..., description="Roadmap Completion percentage")
    current_month: int = Field(1, description="Current active month of study")
    completed_milestones: List[str] = Field(default_factory=list, description="List of completed milestone titles")
    remaining_milestones: List[str] = Field(default_factory=list, description="List of remaining milestone titles")

class JobMarketIntelligence(BaseModel):
    india_salary: Dict[str, Any] = Field(default_factory=dict, description="India salary range data")
    global_salary: Dict[str, Any] = Field(default_factory=dict, description="Global salary range data")
    demand_level: str = Field("High", description="Current market demand level")
    hiring_trend: str = Field("Steady", description="Hiring trend description")
    trend_direction: str = Field("stable", description="up/down/stable")
    estimated_job_openings: int = Field(0, description="Estimated annual job openings")
    yoy_growth: str = Field("+0%", description="Year-over-year growth rate")
    top_employers: List[str] = Field(default_factory=list, description="Top hiring companies")
    remote_friendly: bool = Field(True, description="Whether role is remote-friendly")
    certification_boost: List[str] = Field(default_factory=list, description="Certifications that boost hirability")

class CareerOutcomeForecast(BaseModel):
    current_readiness: int = Field(..., description="Current career readiness percentage")
    projected_readiness: int = Field(..., description="Projected readiness after roadmap completion")
    success_probability: int = Field(..., description="Estimated job-landing success probability")
    eligible_roles: List[str] = Field(default_factory=list, description="Roles user will be eligible for after completion")
    time_to_job_ready: str = Field("", description="Human-readable time estimate to job readiness")
    skills_mastered: int = Field(0, description="Number of skills already mastered")
    skills_remaining: int = Field(0, description="Number of skills still to learn")
    total_study_hours: int = Field(0, description="Total learning hours estimate")
    weekly_workload: str = Field("", description="Weekly study workload hours")
    monthly_workload: str = Field("", description="Monthly study workload hours")
    estimated_completion_date: str = Field("", description="Target date for job readiness")

class RoadmapShareResponse(BaseModel):
    share_id: str = Field(..., description="Unique ID for sharing the roadmap")
    shareable_url: str = Field(..., description="Full shareable URL")
    message: str = Field("Roadmap shared successfully.", description="Confirmation message")

class RoadmapResponse(BaseModel):
    career: str = Field(..., description="Target expected career role")
    expected_readiness: int = Field(..., description="Expected career readiness score after completing roadmap")
    difficulty: str = Field(..., description="Roadmap difficulty classification: Beginner, Intermediate, Advanced")
    total_weeks: int = Field(..., description="Total weeks of required learning")
    total_months: int = Field(..., description="Total months of required learning")
    monthly_roadmap: List[RoadmapMonthlyPlan] = Field(default_factory=list, description="List of monthly schedules")
    milestones: List[MilestoneProgressTracker] = Field(default_factory=list, description="Topological milestones roadmap")
    progress: RoadmapProgressInfo = Field(..., description="Aggregated learning progress metrics")
    job_market: Optional[JobMarketIntelligence] = Field(None, description="Job market intelligence for this career")
    career_forecast: Optional[CareerOutcomeForecast] = Field(None, description="Career outcome forecast metrics")


class ShareRoadmapRequest(BaseModel):
    roadmap: RoadmapResponse = Field(..., description="Full roadmap data to share or export")
    candidate_name: Optional[str] = Field(None, description="Optional candidate name for the PDF/share header")
