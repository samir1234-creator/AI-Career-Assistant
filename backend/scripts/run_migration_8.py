import os
import sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
env_path = BACKEND_DIR / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

def run_migration():
    migration_sql_path = BACKEND_DIR / "scripts" / "migration_phase_8.sql"
    with open(migration_sql_path, "r", encoding="utf-8") as f:
        sql = f.read()
        
    print("Connecting to Supabase PostgreSQL database for Phase 8...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(sql)
            print("Migration SQL executed successfully for Phase 8!")
        conn.close()
    except Exception as e:
        print(f"Migration failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
