from typing import Optional
from domain.schemas.roadmap_schema import RoadmapRequest, RoadmapResponse
from services.roadmap_generator import RoadmapGenerator

class RoadmapService:
    def __init__(self, core_dir: Optional[str] = None):
        """
        Initializes the Roadmap Service and hooks up the Roadmap Generator.
        """
        self.generator = RoadmapGenerator(core_dir=core_dir)

    def create_roadmap(self, payload: RoadmapRequest) -> RoadmapResponse:
        """
        Processes a learning roadmap request and triggers dynamic timeline scheduling.
        """
        return self.generator.generate(
            career=payload.career,
            matched_skills=payload.matched_skills,
            missing_skills=payload.missing_skills,
            career_readiness=payload.career_readiness,
            projects=payload.projects,
            certifications=payload.certifications,
            education=payload.education,
            ats_score=payload.ats_score
        )
