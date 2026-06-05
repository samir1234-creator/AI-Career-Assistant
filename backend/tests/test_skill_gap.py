from services.skill_gap_analysis_service import SkillGapAnalysisService
from domain.schemas.skill_gap_schema import SkillGapRequest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_skill_gap_analysis_service_ai_engineer():
    """
    Test Case: AI Engineer
    Matched Skills: Python, Machine Learning, FastAPI, Git
    Missing Skills: Deep Learning, LLMs, NLP, Generative AI, LangChain
    Expected readiness: 72%
    Expected severity: Medium Gap
    """
    service = SkillGapAnalysisService()
    payload = SkillGapRequest(
        career="AI Engineer",
        matched_skills=["Python", "Machine Learning", "FastAPI", "Git"],
        missing_skills=["Deep Learning", "LLMs", "NLP", "Generative AI", "LangChain"]
    )
    
    response = service.analyze_gap(payload)
    
    # Assert readiness score, level, and gap severity
    assert response.career_readiness == 72
    assert response.gap_severity == "Medium Gap"
    assert response.career_readiness_level == "Developing"
    
    # Assert job readiness timeline
    assert response.job_ready_time_weeks == "20 Weeks"
    assert response.job_ready_time_months == "5 Months"
    
    # Assert priority ranking
    assert response.priority_ranking == ["Deep Learning", "NLP", "LLMs", "Generative AI", "LangChain"]
    
    # Assert missing categories grouping
    assert response.missing_categories == {"AI Skills": ["Deep Learning", "LLMs", "NLP", "Generative AI", "LangChain"]}
    
    # Assert critical skills
    critical_names = [item.skill for item in response.critical_skills]
    assert "Deep Learning" in critical_names
    assert "LLMs" in critical_names
    for item in response.critical_skills:
        if item.skill == "Deep Learning":
            assert item.impact_score == 95
            assert item.estimated_learning_time == "4 weeks"
            assert item.priority == "Critical"
            
    # Assert important skills
    important_names = [item.skill for item in response.important_skills]
    assert "NLP" in important_names
    assert "Generative AI" in important_names
    for item in response.important_skills:
        if item.skill == "NLP":
            assert item.impact_score == 75
            assert item.estimated_learning_time == "2 weeks"
            assert item.priority == "Important"

    # Assert optional skills
    optional_names = [item.skill for item in response.optional_skills]
    assert "LangChain" in optional_names
    for item in response.optional_skills:
        if item.skill == "LangChain":
            assert item.impact_score == 40
            assert item.estimated_learning_time == "1 week"
            assert item.priority == "Optional"

    # Assert insights
    assert "Python" in response.insights.strong_areas
    assert "Machine Learning" in response.insights.strong_areas
    assert "FastAPI" in response.insights.strong_areas
    assert "Git" in response.insights.strong_areas
    
    assert "Deep Learning" in response.insights.weak_areas
    assert "LLMs" in response.insights.weak_areas
    assert "NLP" in response.insights.weak_areas
    assert "Generative AI" in response.insights.weak_areas
    assert "LangChain" not in response.insights.weak_areas # LangChain is optional

    # Assert roadmap compatibility layer
    assert len(response.roadmap_compatibility) == 5
    dl_item = next(item for item in response.roadmap_compatibility if item.skill == "Deep Learning")
    assert dl_item.priority == "critical"
    assert dl_item.impact_score == 95
    assert dl_item.learning_time_weeks == 4
    assert "Python" in dl_item.dependencies
    assert "Machine Learning" in dl_item.dependencies

    # Assert milestones
    assert len(response.milestones) == 6
    assert response.milestones[0].index == 1
    assert response.milestones[0].title == "Milestone 1: Core Deep Learning"
    assert response.milestones[0].skills == ["Deep Learning"]
    assert response.milestones[5].index == 6
    assert response.milestones[5].title == "Milestone 6: AI Engineer Ready"
    assert response.milestones[5].skills == ["Ready to apply for AI Engineer roles!"]

def test_skill_gap_analysis_endpoint():
    """
    Test API endpoint /api/v1/skill-gap/analyze
    """
    payload = {
        "career": "AI Engineer",
        "matched_skills": ["Python", "Machine Learning", "FastAPI", "Git"],
        "missing_skills": ["Deep Learning", "LLMs", "NLP", "Generative AI", "LangChain"]
    }
    
    response = client.post("/api/v1/skill-gap/analyze", json=payload)
    assert response.status_code == 200
    
    json_data = response.json()
    assert json_data["success"] is True
    
    data = json_data["data"]
    assert data["career"] == "AI Engineer"
    assert data["career_readiness"] == 72
    assert data["gap_severity"] == "Medium Gap"
    assert data["career_readiness_level"] == "Developing"
    assert data["job_ready_time_weeks"] == "20 Weeks"
    assert data["job_ready_time_months"] == "5 Months"
    assert data["priority_ranking"] == ["Deep Learning", "NLP", "LLMs", "Generative AI", "LangChain"]
    assert len(data["critical_skills"]) == 2
    assert len(data["important_skills"]) == 2
    assert len(data["optional_skills"]) == 1
    
    # Assert endpoint milestone details
    assert len(data["milestones"]) == 6
    assert data["milestones"][0]["index"] == 1
    assert data["milestones"][0]["title"] == "Milestone 1: Core Deep Learning"
    assert data["milestones"][5]["title"] == "Milestone 6: AI Engineer Ready"
