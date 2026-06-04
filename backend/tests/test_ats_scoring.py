from services.ats_scoring_service import ATSScoringService
from domain.schemas.ats import ATSScoringRequest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_empty_resume_scoring():
    service = ATSScoringService()
    payload = ATSScoringRequest()
    result = service.calculate_score(payload)
    
    assert result.ats_score == 0
    assert result.score_breakdown.skills == 0
    assert result.score_breakdown.projects == 0
    assert result.score_breakdown.education == 0
    assert result.score_breakdown.certifications == 0
    assert result.score_breakdown.achievements == 0
    assert result.score_breakdown.contact == 0
    assert "No skills detected in resume" in result.weaknesses
    assert "No projects or work history listed on resume" in result.weaknesses

def test_skills_scoring_levels():
    service = ATSScoringService()
    
    # 1. Low skills boundary
    payload_low = ATSScoringRequest(skills=["Python"])
    result_low = service.calculate_score(payload_low)
    assert result_low.score_breakdown.skills == 10
    
    # 2. Medium skills boundary
    payload_med = ATSScoringRequest(skills=["Python", "FastAPI", "React", "Docker"])
    result_med = service.calculate_score(payload_med)
    assert result_med.score_breakdown.skills == 20
    
    # 3. High skills boundary
    payload_high = ATSScoringRequest(skills=["Python", "FastAPI", "React", "Docker", "AWS", "Git", "MySQL", "K8s"])
    result_high = service.calculate_score(payload_high)
    assert result_high.score_breakdown.skills == 30

def test_projects_scoring_metrics():
    service = ATSScoringService()
    
    # 1. Multiple projects without metrics/intern/professional keywords
    payload_basic = ATSScoringRequest(projects=["Built a resume parser web app", "Created a chat client"])
    result_basic = service.calculate_score(payload_basic)
    assert result_basic.score_breakdown.projects == 10 # Quantity = 10, Quality = 0
    assert "Quantified achievements missing" in result_basic.weaknesses
    assert "Internship experience missing" in result_basic.weaknesses
    
    # 2. Multiple projects with work experience keyword (developed/developer)
    payload_work = ATSScoringRequest(projects=["Worked as developer on resume parser web app", "Created a chat client"])
    result_work = service.calculate_score(payload_work)
    assert result_work.score_breakdown.projects == 15 # Quantity = 10, Work = 5, Intern = 0, Metrics = 0
    assert "Quantified achievements missing" in result_work.weaknesses
    
    # 3. Multiple projects with work, intern, and metrics
    payload_full = ATSScoringRequest(projects=[
        "Interned as a software developer, built a parsing microservice improving search speed by 40%",
        "Worked as full-time Engineer, deployed 2+ features"
    ])
    result_full = service.calculate_score(payload_full)
    assert result_full.score_breakdown.projects == 25 # Quantity = 10, Work = 5, Intern = 5, Metrics = 5

def test_contact_scoring_github():
    service = ATSScoringService()
    
    # 1. Partial contact, no GitHub, no portfolio
    payload_partial = ATSScoringRequest(name="Rahul Sharma", email="rahul@example.com")
    result_partial = service.calculate_score(payload_partial)
    assert result_partial.score_breakdown.contact == 3 # 1.5 * 2
    assert "GitHub link missing" in result_partial.weaknesses
    assert "Portfolio website missing" in result_partial.weaknesses
    
    # 2. Complete contact + GitHub, but no portfolio
    payload_github = ATSScoringRequest(
        name="Rahul Sharma",
        email="rahul@example.com",
        phone="1234567890",
        linkedin="github.com/rahulsharma"
    )
    result_github = service.calculate_score(payload_github)
    assert result_github.score_breakdown.contact == 8 # 6 + 2 github
    assert "GitHub profile link included" in result_github.strengths
    assert "Portfolio website missing" in result_github.weaknesses
    
    # 3. Complete contact + GitHub + Portfolio
    payload_all = ATSScoringRequest(
        name="Rahul Sharma",
        email="rahul@example.com",
        phone="1234567890",
        linkedin="github.com/rahulsharma portfolio.github.io"
    )
    result_all = service.calculate_score(payload_all)
    assert result_all.score_breakdown.contact == 10 # 6 + 2 github + 2 portfolio

def test_api_ats_score_endpoint():
    payload = {
        "name": "Rahul Sharma",
        "email": "rahul@example.com",
        "phone": "9876543210",
        "linkedin": "linkedin.com/in/rahul github.com/rahul portfolio.github.io",
        "skills": ["Python", "FastAPI", "React", "Docker", "AWS", "Git", "MySQL", "K8s"],
        "projects": [
            "Interned as a software developer, built a parsing microservice improving speed by 35%",
            "Worked as Engineer on 2+ production apps"
        ],
        "education": ["Bachelor of Science in Computer Science"],
        "certifications": ["AWS Certified Solutions Architect"],
        "achievements": ["First Place in National Hackathon"]
    }
    
    response = client.post("/api/v1/ats/score", json=payload)
    assert response.status_code == 200
    
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["message"] == "ATS score calculated successfully."
    
    data = json_data["data"]
    assert data["ats_score"] == 100 # Hits all conditions!
    assert data["score_breakdown"]["skills"] == 30
    assert data["score_breakdown"]["projects"] == 25
    assert data["score_breakdown"]["education"] == 15
    assert data["score_breakdown"]["certifications"] == 10
    assert data["score_breakdown"]["achievements"] == 10
    assert data["score_breakdown"]["contact"] == 10
    assert "GitHub profile link included" in data["strengths"]
    assert "Portfolio website link included" in data["strengths"]
