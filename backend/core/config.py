from dotenv import load_dotenv
load_dotenv()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ilmora"
    API_V1_STR: str = "/api/v1"
    
    # CORS Origins
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # File Upload Limits
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024 # 5 MB

    # Supabase Settings
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_JWT_SECRET: str
    DATABASE_URL: str

    # Firebase Settings
    FIREBASE_PROJECT_ID: str

    class Config:
        case_sensitive = True

settings = Settings()
