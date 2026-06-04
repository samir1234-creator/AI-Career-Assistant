from services.career_recommendation_service import CareerRecommendationService
from domain.schemas.career import CareerRecommendationRequest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_resume_a_ai_ml_science():
    """
    Resume A: Python, Machine Learning, FastAPI
    Expected top rankings:
      1. AI Engineer
      2. Machine Learning Engineer
      3. Data Scientist
    """
    service = CareerRecommendationService()
    payload = CareerRecommendationRequest(
        skills=["Python", "Machine Learning", "FastAPI"],
        projects=["Worked on an AI model and built a model training pipeline in Python"],
        education=["Bachelor of Science in Computer Science"],
        certifications=["Coursera Machine Learning Certificate"],
        ats_score=85
    )
    
    results = service.calculate_recommendations(payload)
    roles = [r.role for r in results]
    
    # Assert top careers are present in the top 3 and in the correct order
    assert roles[0] == "AI Engineer"
    assert roles[1] == "Machine Learning Engineer"
    assert roles[2] == "Data Scientist"
    
    # Assert reasons include specific details
    ai_reasons = results[0].reason
    assert any("Python detected" in r or "Python" in r for r in ai_reasons)
    assert any("Machine Learning" in r for r in ai_reasons)

def test_resume_b_fullstack_backend_software():
    """
    Resume B: React, Node.js, MongoDB
    Expected top rankings:
      1. Full Stack Developer
      2. Backend Developer
      3. Software Engineer
    """
    service = CareerRecommendationService()
    payload = CareerRecommendationRequest(
        skills=["React", "Node.js", "MongoDB"],
        projects=["Built a MERN stack web app", "Developed backend services using Express"],
        education=["Bachelor of IT"],
        certifications=["AWS Cloud Developer Cert"],
        ats_score=80
    )
    
    results = service.calculate_recommendations(payload)
    roles = [r.role for r in results]
    
    assert roles[0] == "Full Stack Developer"
    assert roles[1] == "Backend Developer"
    assert roles[2] == "Software Engineer"
    
    fs_reasons = results[0].reason
    assert any("React" in r for r in fs_reasons)
    assert any("Node.js" in r or "NodeJS" in r for r in fs_reasons)

def test_recommendation_endpoint():
    payload = {
        "skills": ["React", "Node.js", "MongoDB"],
        "projects": ["MERN stack app"],
        "education": ["BS in Computer Science"],
        "certifications": [],
        "ats_score": 75
    }
    
    response = client.post("/api/v1/career/recommend", json=payload)
    assert response.status_code == 200
    
    json_data = response.json()
    assert json_data["success"] is True
    
    careers = json_data["data"]["recommended_careers"]
    assert len(careers) == 5
    assert careers[0]["role"] == "Full Stack Developer"
    assert careers[0]["match_score"] > 50
    assert len(careers[0]["reason"]) > 0
