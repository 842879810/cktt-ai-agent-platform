"""Configuration schema."""

from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    """Database configuration."""

    host: str = "localhost"
    port: int = 5432
    name: str = "agent_platform"
    user: str = "postgres"
    password: str = ""


class RedisConfig(BaseModel):
    """Redis configuration."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str | None = None


class LLMConfig(BaseModel):
    """LLM provider configuration."""

    provider: str = "openai"
    api_key: str = ""
    model: str = "gpt-4"
    base_url: str | None = None


class AppConfig(BaseModel):
    """Application configuration."""

    debug: bool = False
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
