from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# path env
env_path = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str
    # подключение к БД на синхронном движке и создание сессии для синхронных подключений
    database_url: str = "postgresql://todo_user:todo_pass@localhost:5432/todo_db"
    database_user: str
    database_pass: str
    # если не указано, то берется из env для settings приложения
    model_config = SettingsConfigDict(
        env_file=env_path / ".env",
        env_file_encoding="utf-8",
    )

    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
