import urllib.request
import json

base_url = "http://localhost:8000"

def run_test_endpoint(path, headers=None, method="GET", data=None):
    url = f"{base_url}{path}"
    req = urllib.request.Request(url, method=method, headers=headers or {})
    if data:
        req.data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
    
    print(f"\n--- Testing {method} {path} ---")
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            print(f"Status: {resp.status}")
            parsed = json.loads(body)
            print("Response:", json.dumps(parsed, indent=2)[:800] + "...")
            return parsed
    except Exception as e:
        print(f"FAILED: {e}")
        if hasattr(e, "read"):
            print("Error body:", e.read().decode('utf-8'))
        return None

# 1. Health check
run_test_endpoint("/health")

# 2. Simulated Developer Auth Headers
headers = {
    "Authorization": "Bearer sim_token_e2e_test_user@career-assistant.ai"
}

# 3. Fetch user profile (Triggers auto-create profile in Supabase DB)
profile = run_test_endpoint("/api/v1/user/profile", headers=headers)
if profile and profile.get("success"):
    print("\nSUCCESS: Profile created/fetched successfully in Supabase PostgreSQL!")

# 4. Fetch dashboard summary stats
summary = run_test_endpoint("/api/v1/user/dashboard/summary", headers=headers)
if summary and summary.get("success"):
    print("\nSUCCESS: Unified Dashboard Summary retrieved successfully!")
    data = summary.get("data", {})
    print(f"Has active roadmap: {data.get('has_active_roadmap')}")
    print(f"Profile keys: {list(data.get('profile', {}).keys())}")
    print(f"Readiness keys: {list(data.get('readiness', {}).keys())}")
    print(f"Progress keys: {list(data.get('progress', {}).keys())}")
    print(f"Badges count: {len(data.get('badges', []))}")
    print(f"History count: {len(data.get('history', []))}")
else:
    print("\nFAILED to get summary.")
