import re

file_path = "frontend/src/pages/RoadmapDashboard.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix getSharedRoadmap
content = content.replace("exportRoadmapPDF, getSharedRoadmap", "exportRoadmapPDF")
content = content.replace("exportRoadmapPDF,  ", "exportRoadmapPDF")

# Fix STORAGE_KEY
content = re.sub(r'const STORAGE_KEY = .*?\n', '', content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Final ESLint fixes applied.")
