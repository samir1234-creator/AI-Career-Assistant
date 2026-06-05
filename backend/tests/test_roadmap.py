from services.roadmap_service import RoadmapService
from domain.schemas.roadmap_schema import RoadmapRequest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_roadmap_generator_service_ai_engineer():
    """
    Test Case: AI Engineer Roadmap Generation
    Matched Skills: Python, Machine Learning, FastAPI, Git
    Missing Skills: Deep Learning, PyTorch, TensorFlow, NLP, LLMs, Generative AI, LangChain, LlamaIndex
    Expected: Dynamic monthly/weekly allocation, resources, milestones, project recommendations
    """
    service = RoadmapService()
    payload = RoadmapRequest(
        career="AI Engineer",
        matched_skills=["Python", "Machine Learning", "FastAPI", "Git"],
        missing_skills=["Deep Learning", "PyTorch", "TensorFlow", "NLP", "LLMs", "Generative AI", "LangChain", "LlamaIndex"],
        career_readiness=72
    )
    
    response = service.create_roadmap(payload)
    
    # Assert metadata
    assert response.career == "AI Engineer"
    assert response.expected_readiness >= 92
    assert response.difficulty == "Advanced"
    
    # Timeline should have 7 skills scheduled:
    # Due to personalized timeline estimation, missing skills have their durations reduced by 30% because Python/Machine Learning are in matched_skills.
    # Total weeks: 22 weeks learning + 4 weeks Capstone Portfolio = 26 weeks
    assert response.total_weeks == 26
    assert response.total_months == 7 # 22 weeks partitioned to 6 months + 1 portfolio month = 7 months total
    
    # Assert Monthly schedule details
    assert len(response.monthly_roadmap) == 7
    
    # Month 1
    m1 = response.monthly_roadmap[0]
    assert m1.month_number == 1
    assert "Deep Learning" in m1.skills
    assert len(m1.weeks) == 4
    assert m1.weeks[0].week_number == 1
    assert m1.weeks[0].title == "Neural Networks Foundations"
    assert "Perceptrons" in m1.weeks[0].topics
    
    # Month 1 Projects
    assert len(m1.projects) > 0
    assert m1.projects[0].title == "Neural Network from Scratch"
    
    # Milestone progress tracking
    # Python, ML are matched, so Milestone 1 should be complete.
    # Deep Learning is missing, so Milestone 2 should be incomplete.
    assert len(response.milestones) > 0
    m1_tracker = next(m for m in response.milestones if "Foundations" in m.title)
    assert m1_tracker.complete is True
    
    m2_tracker = next(m for m in response.milestones if "Core Deep Learning" in m.title)
    assert m2_tracker.complete is False
    
    # Progress metrics
    assert response.progress.completion_percentage == 72
    assert response.progress.current_month == 1
    assert "Foundations" in "".join(response.progress.completed_milestones)

def test_roadmap_endpoint():
    """
    Test API endpoint /api/v1/roadmap/generate
    """
    payload = {
        "career": "AI Engineer",
        "matched_skills": ["Python", "Machine Learning", "FastAPI", "Git"],
        "missing_skills": ["Deep Learning", "PyTorch", "TensorFlow", "NLP", "LLMs", "Generative AI", "LangChain", "LlamaIndex"],
        "career_readiness": 72
    }
    
    response = client.post("/api/v1/roadmap/generate", json=payload)
    assert response.status_code == 200
    
    json_data = response.json()
    assert json_data["success"] is True
    
    data = json_data["data"]
    assert data["career"] == "AI Engineer"
    assert data["expected_readiness"] >= 92
    assert data["difficulty"] == "Advanced"
    assert data["total_months"] == 7
    assert len(data["monthly_roadmap"]) == 7
    assert len(data["milestones"]) > 0
