"""Settings management."""


from pydantic_settings import BaseSettings

from .schema import AppConfig


class Settings(BaseSettings):
    """Application settings."""

    # App settings
    debug: bool = False
    environment: str = "development"

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Database settings
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "agent_platform"
    database_user: str = "postgres"
    database_password: str = ""

    # Redis settings
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # LLM settings
    llm_provider: str = "openai"
    llm_api_key: str = ""
    llm_model: str = "gpt-4"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def to_app_config(self) -> AppConfig:
        """Convert to AppConfig."""
        return AppConfig(
            debug=self.debug,
            environment=self.environment,
            host=self.api_host,
            port=self.api_port,
        )


# Global settings instance
settings = Settings()
