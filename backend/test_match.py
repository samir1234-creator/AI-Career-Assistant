import time
from services.career_scoring_engine import CareerScoringEngine

t0 = time.time()
print("Testing _is_match with empty string...")
res = CareerScoringEngine._is_match("", "Test Project")
print("Result:", res, "Time:", time.time() - t0)

print("Testing calculate_scores...")
CareerScoringEngine.calculate_scores(
    career_name="Software Engineer",
    matched_skills=[],
    missing_skills=[],
    projects=["Built a cool app", "Another project"],
    certifications=["AWS"],
    education=["BSc CS"],
    ats_score=80
)
print("calculate_scores finished.")
