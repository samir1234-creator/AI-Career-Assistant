import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Load env variables
BACKEND_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BACKEND_DIR / ".env")

# The password is: DN3rPZ2YUq+YiR&
password = "DN3rPZ2YUq+YiR&"
project_ref = "eznsvreplkrydhmerrzi"

regions = [
    'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
    'ap-south-1', 'ap-southeast-1', 'ap-southeast-2',
    'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-3',
    'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-central-1', 'eu-north-1',
    'ca-central-1', 'sa-east-1', 'me-central-1', 'af-south-1'
]

print("Scanning regions to find the active pooler region...")
for region in regions:
    host = f"aws-0-{region}.pooler.supabase.com"
    # Port 5432 is Session mode pooler in Supabase
    conn_str = f"postgresql://postgres.{project_ref}:{password}@{host}:5432/postgres"
    print(f"Trying region {region} ({host})...")
    try:
        conn = psycopg2.connect(conn_str, connect_timeout=3)
        print(f"\nSUCCESS! Found region: {region}")
        print(f"Connection String: {conn_str}")
        conn.close()
        break
    except Exception as e:
        # If the password is correct but the region is wrong, we might get an error about database not existing
        # or we might get a connection timeout. Let's print the error message briefly.
        err_msg = str(e).strip()
        print(f"Failed for {region}: {err_msg}")
