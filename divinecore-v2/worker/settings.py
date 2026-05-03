from pydantic_settings import BaseSettings, SettingsConfigDict


class WorkerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    REDIS_URL: str = "redis://localhost:6379/0"

    AIRTABLE_API_KEY: str = ""
    AIRTABLE_BASE_ID: str = ""
    AIRTABLE_MEETINGS_TABLE: str = "Meetings"
    AIRTABLE_TASKS_TABLE: str = "Task"

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    CATEGORIZER_MODEL: str = "openai/gpt-4o-mini"

    FATHOM_API_KEY: str = ""
    FATHOM_API_BASE_URL: str = "https://api.fathom.ai/external/v1"
    FATHOM_POLL_LOOKBACK_HOURS: int = 24


settings = WorkerSettings()
