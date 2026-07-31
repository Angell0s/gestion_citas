# backend\app\core\config.py
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent
ENV_FILE = ROOT_DIR / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE, override=False)

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 5432))

    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in environment variables")
    
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))

    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    PROJECT_NAME = os.getenv("PROJECT_NAME", "Sistema de Citas")
    PROJECT_VERSION = os.getenv("PROJECT_VERSION", "0.1.0")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    ACCESS_TOKEN_EXPIRE_MINUTES_REMEMBER = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES_REMEMBER", 60 * 24 * 7))  # 7 días
    ACCESS_TOKEN_EXPIRE_MINUTES_DEFAULT = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES_DEFAULT", 60))  # 1 hora

    FIRST_SUPERUSER_USERNAME = os.getenv("FIRST_SUPERUSER_USERNAME", "admin")
    FIRST_SUPERUSER_EMAIL = os.getenv("FIRST_SUPERUSER_EMAIL", "admin@example.com")
    FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD", "AdminPasswordSecreta123!")

settings = Settings()