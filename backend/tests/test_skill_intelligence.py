from services.skill_intelligence_service import SkillIntelligenceService
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_service_normalization():
    service = SkillIntelligenceService()
    # Test normalization of casing and spaces
    assert service._normalize_name("  Python   ") == "python"
    assert service._normalize_name("React.js") == "react.js"
    assert service._normalize_name("Machine    Learning") == "machine learning"

def test_service_lookup_known():
    service = SkillIntelligenceService()
    # Known skills from skills_database.json
    category1, canonical1 = service.lookup_skill("python")
    assert category1 == "Programming Languages"
    assert canonical1 == "Python"
    
    category2, canonical2 = service.lookup_skill("  React.js  ")
    assert category2 == "Frontend Frameworks"
    assert canonical2 == "React.js"

    category3, canonical3 = service.lookup_skill("Machine Learning")
    assert category3 == "Artificial Intelligence"
    assert canonical3 == "Machine Learning"

    category4, canonical4 = service.lookup_skill("Node.js")
    assert category4 == "Backend Frameworks"
    assert canonical4 == "Node.js"

def test_service_lookup_unknown():
    service = SkillIntelligenceService()
    # Unknown skill should map to Other with same name
    category, canonical = service.lookup_skill("Quantum Computing Framework")
    assert category == "Other"
    assert canonical == "Quantum Computing Framework"

def test_service_classify_skills():
    service = SkillIntelligenceService()
    raw_skills = [
        "python",
        "React",
        "PYTHON", # Duplicate case-insensitive
        "React.js", # Same canonical/lookup name (maps to React.js under Frontend Frameworks, but wait: is React.js different than React? Let's check.)
        "AWS",
        "Docker",
        "UnknownSkill123"
    ]
    
    enriched = service.classify_skills(raw_skills)
    
    # Python and PYTHON are duplicate.
    # React and React.js are distinct normalized strings, so they are kept.
    # React -> Frontend Frameworks -> Frontend Framework
    # React.js -> Frontend Frameworks -> Frontend Framework
    # AWS -> Cloud Computing
    # Docker -> DevOps
    # UnknownSkill123 -> Other
    
    names = [s["name"] for s in enriched]
    assert "Python" in names
    assert "React" in names
    assert "React.js" in names
    assert "AWS" in names
    assert "Docker" in names
    assert "UnknownSkill123" in names
    
    # Deduplication check: Python should only appear once
    assert names.count("Python") == 1

def test_api_classify_endpoint():
    payload = {
        "skills": [
            "Python",
            "React",
            "MongoDB",
            "AWS",
            "Docker",
            "SuperNaturalAI"
        ]
    }
    
    response = client.post("/api/v1/skills/classify", json=payload)
    assert response.status_code == 200
    
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["message"] == "Skills classified and enriched successfully."
    
    skills = json_data["data"]["skills"]
    assert len(skills) == 6
    
    # Verify categories
    expected_mappings = {
        "Python": "Programming Language",
        "React": "Frontend Framework",
        "MongoDB": "Database",
        "AWS": "Cloud Computing",
        "Docker": "DevOps",
        "SuperNaturalAI": "Other"
    }
    
    for item in skills:
        name = item["name"]
        category = item["category"]
        if name in expected_mappings:
            assert category == expected_mappings[name]
