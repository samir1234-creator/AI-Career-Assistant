from services.extraction_service import ExtractionService

def test_extract_information_complete():
    resume_text = """
    John Doe
    Email: john.doe@example.com
    Phone: (555) 555-5555
    LinkedIn: linkedin.com/in/johndoe
    
    Technical Skills:
    Python, FastAPI, React, JavaScript, SQL
    
    Education:
    Bachelor of Science in Computer Science, ABC University, 2020 - 2024
    
    Projects:
    - AI Career Assistant: Built a resume parsing app using FastAPI and React
    - Portfolio Website: Personal portfolio showing projects
    
    Certifications:
    AWS Certified Cloud Practitioner, 2023
    """
    
    data = ExtractionService.extract_information(resume_text)
    
    assert data.name == "John Doe"
    assert data.email == "john.doe@example.com"
    assert data.phone == "(555) 555-5555"
    assert "linkedin.com/in/johndoe" in data.linkedin
    assert "Python" in data.skills
    assert "FastAPI" in data.skills
    assert any("Bachelor of Science in Computer Science" in item for item in data.education)
    assert any("AI Career Assistant" in item for item in data.projects)
    assert any("AWS Certified Cloud Practitioner" in item for item in data.certifications)

def test_extract_information_empty():
    data = ExtractionService.extract_information("")
    assert data.name is None
    assert data.email is None
    assert data.phone is None
    assert data.linkedin is None
    assert len(data.skills) == 0
    assert len(data.education) == 0
    assert len(data.projects) == 0
    assert len(data.certifications) == 0

def test_extract_multi_word_skills():
    # Test case 1: standard multi-word skills
    text1 = """
    Technical Skills:
    Spring Boot, Machine Learning, Deep Learning, Computer Vision, Natural Language Processing, Data Structures and Algorithms, REST APIs
    """
    data1 = ExtractionService.extract_information(text1)
    expected_skills = [
        "Spring Boot", "Machine Learning", "Deep Learning", 
        "Computer Vision", "Natural Language Processing", 
        "Data Structures and Algorithms", "REST APIs"
    ]
    for skill in expected_skills:
        assert skill in data1.skills

    # Test case 2: multi-word skills split across multiple lines and containing repeated keywords (like Learning)
    text2 = """
    Technical Skills:
    Spring
    Boot
    Machine
    Learning
    Deep
    Learning
    Computer
    Vision
    Natural
    Language
    Processing
    Data
    Structures
    and
    Algorithms
    REST
    APIs
    """
    data2 = ExtractionService.extract_information(text2)
    for skill in expected_skills:
        assert skill in data2.skills

    # Test case 3: repeated word boundaries and deduplication checks
    text3 = """
    Technical Skills:
    Spring Cloud, Spring Boot, REST API, REST APIs
    """
    data3 = ExtractionService.extract_information(text3)
    assert "Spring Cloud" in data3.skills
    assert "Spring Boot" in data3.skills
    assert "REST API" in data3.skills
    assert "REST APIs" in data3.skills
