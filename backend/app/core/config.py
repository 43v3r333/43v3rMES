from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    PROJECT_NAME: str = "AI MES Platform"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "test-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/mes_db"
    class Config:
        env_file = ".env"
        case_sensitive = True
settings = Settings()
