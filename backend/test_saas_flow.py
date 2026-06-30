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
            print("Response:", json.dumps(parsed, indent=2)[:500] + "...")
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

# 4. Fetch dashboard stats
run_test_endpoint("/api/v1/user/dashboard", headers=headers)

# 5. Fetch resume history
run_test_endpoint("/api/v1/user/history", headers=headers)
