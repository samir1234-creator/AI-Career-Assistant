import requests

url = "http://localhost:8000/api/v1/roadmap/generate"
payload = {
    "career": "AI Engineer",
    "matched_skills": ["Python", "Machine Learning", "FastAPI", "Git"],
    "missing_skills": ["Deep Learning", "PyTorch", "TensorFlow", "NLP", "LLMs", "Generative AI", "LangChain", "LlamaIndex"],
    "career_readiness": 72
}

try:
    print("Sending request to:", url)
    response = requests.post(url, json=payload, timeout=5)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Request failed:", e)
