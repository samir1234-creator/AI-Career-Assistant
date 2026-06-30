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

def run_migration():
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable is not set in backend/.env")
        print("Please configure DATABASE_URL in backend/.env first.")
        print("Example: DATABASE_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres")
        sys.exit(1)
        
    migration_sql_path = BACKEND_DIR / "scripts" / "migration.sql"
    if not migration_sql_path.exists():
        print(f"ERROR: Migration SQL file not found at {migration_sql_path}")
        sys.exit(1)
        
    print(f"Reading migration SQL from {migration_sql_path}...")
    with open(migration_sql_path, "r", encoding="utf-8") as f:
        sql = f.read()
        
    print("Connecting to Supabase PostgreSQL database...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        with conn.cursor() as cur:
            print("Executing migration SQL...")
            cur.execute(sql)
            print("Migration SQL executed successfully!")
        conn.close()
        print("Database migrated successfully!")
    except Exception as e:
        print(f"Migration failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
