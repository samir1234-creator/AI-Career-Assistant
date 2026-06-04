from fastapi import APIRouter
from api.v1.endpoints import resume, skills, ats, career

api_router = APIRouter()
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(skills.router, prefix="/skills", tags=["skills"])
api_router.include_router(ats.router, prefix="/ats", tags=["ats"])
api_router.include_router(career.router, prefix="/career", tags=["career"])

