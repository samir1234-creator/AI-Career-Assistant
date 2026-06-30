import sys
import time

def test_roadmap():
    from services.roadmap_generator import RoadmapGenerator
    print("Initializing generator...")
    t0 = time.time()
    gen = RoadmapGenerator()
    print(f"Initialized in {time.time()-t0:.2f}s")
    
    print("Generating roadmap...")
    t1 = time.time()
    try:
        res = gen.generate(
            career="Data Scientist",
            matched_skills=["Python", "SQL"],
            missing_skills=["Machine Learning", "Deep Learning", "NLP"],
            career_readiness=50,
            projects=[],
            certifications=[],
            education=[],
            ats_score=70
        )
        print(f"Generated successfully in {time.time()-t1:.2f}s")
    except Exception as e:
        print(f"Error during generation: {e}")

if __name__ == "__main__":
    test_roadmap()
