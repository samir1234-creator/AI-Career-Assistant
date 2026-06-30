import re

file_path = "frontend/src/pages/RoadmapDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Make accesses safe
content = content.replace("liveRoadmap.career", "liveRoadmap?.career")
content = content.replace("liveRoadmap.job_market", "liveRoadmap?.job_market")
content = content.replace("liveRoadmap.career_forecast", "liveRoadmap?.career_forecast")
content = content.replace("liveRoadmap.matched_skills", "(liveRoadmap?.matched_skills || [])")
content = content.replace("liveRoadmap.missing_skills", "(liveRoadmap?.missing_skills || [])")
content = content.replace("liveRoadmap.milestones", "(liveRoadmap?.milestones || [])")
content = content.replace("liveRoadmap.progress?.completion_percentage", "(liveRoadmap?.progress?.completion_percentage || 0)")
content = content.replace("liveRoadmap.expected_readiness", "(liveRoadmap?.expected_readiness || 0)")
content = content.replace("liveRoadmap.projects", "(liveRoadmap?.projects || [])")
content = content.replace("liveRoadmap.monthly_roadmap", "(liveRoadmap?.monthly_roadmap || [])")
content = content.replace("liveRoadmap.total_weeks", "(liveRoadmap?.total_weeks || 0)")
content = content.replace("liveRoadmap.total_months", "(liveRoadmap?.total_months || 0)")
content = content.replace("liveRoadmap.difficulty", "(liveRoadmap?.difficulty || 'Beginner')")


# Find the early returns block
early_returns = """  // If liveRoadmap is not loaded yet
  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '6rem 2rem' }}>
        <div className="spinner"></div>
        <p style={{ color: 'var(--text-muted)', fontWeight: '500' }}>Loading live study progress...</p>
      </div>
    );
  }

  if (!liveRoadmap) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-muted)' }}>
        No active career roadmap found.
      </div>
    );
  }"""

# Remove the early returns from their original place
content = content.replace(early_returns, "")

# Insert the early returns just before the final return
final_return_pos = content.find("  return (\n    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', animation: 'fadeIn 0.3s ease' }}>")

content = content[:final_return_pos] + early_returns + "\n\n" + content[final_return_pos:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Dashboard fixed.")
