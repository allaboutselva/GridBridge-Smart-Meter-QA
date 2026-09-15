import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    api_base_url: str = os.getenv("API_BASE_URL", "http://127.0.0.1:8001")
    api_username: str = os.getenv("API_USERNAME", "qa_user")
    api_password: str = os.getenv("API_PASSWORD", "change-me")
    jwt_secret: str = os.getenv("JWT_SECRET", "development-only-change-me")
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = int(os.getenv("JWT_EXPIRY_MINUTES", "30"))
    request_timeout: float = float(os.getenv("REQUEST_TIMEOUT", "10"))
    db_host: str = os.getenv("DB_HOST", "127.0.0.1")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "smart_meter_qa")

settings = Settings()
