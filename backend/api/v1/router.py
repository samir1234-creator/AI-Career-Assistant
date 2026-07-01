from fastapi import APIRouter
from api.v1.endpoints import resume, skills, ats, career, skill_gap_endpoint, roadmap_endpoint, user, interview, feedback

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(skills.router, prefix="/skills", tags=["skills"])
api_router.include_router(ats.router, prefix="/ats", tags=["ats"])
api_router.include_router(career.router, prefix="/career", tags=["career"])
api_router.include_router(skill_gap_endpoint.router, prefix="/skill-gap", tags=["skill-gap"])
api_router.include_router(roadmap_endpoint.router, prefix="/roadmap", tags=["roadmap"])
api_router.include_router(interview.router, prefix="/interview", tags=["interview"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])




