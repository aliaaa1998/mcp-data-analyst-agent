from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "mcp-data-analyst-agent"
    environment: str = Field(default="dev")
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    database_url: str = "postgresql+psycopg://postgres:postgres@postgres:5432/analytics"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    openai_timeout_seconds: int = 45

    artifacts_dir: str = "artifacts"
    charts_dir: str = "artifacts/charts"
    reports_dir: str = "artifacts/reports"

    mcp_sql_server_url: str = "http://mcp_sql:8101"
    mcp_analytics_server_url: str = "http://mcp_analytics:8102"
    mcp_chart_server_url: str = "http://mcp_charts:8103"


@lru_cache
def get_settings() -> Settings:
    return Settings()
