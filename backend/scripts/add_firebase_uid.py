import os
import sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

# Load env variables from backend/.env
BACKEND_DIR = Path(__file__).resolve().parent.parent
env_path = BACKEND_DIR / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

def apply_change():
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable is not set in backend/.env")
        sys.exit(1)
        
    print("Connecting to Supabase PostgreSQL database to add firebase_uid column...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        with conn.cursor() as cur:
            # Check if column exists, if not, add it
            cur.execute("""
                ALTER TABLE public.users ADD COLUMN IF NOT EXISTS firebase_uid TEXT;
            """)
            print("Successfully checked/added 'firebase_uid' column to public.users table.")
        conn.close()
    except Exception as e:
        print(f"Database migration failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    apply_change()
