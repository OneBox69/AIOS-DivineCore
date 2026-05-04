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

    # Upwork integration
    GOOGLE_OAUTH_CLIENT_ID: str = ""
    GOOGLE_OAUTH_CLIENT_SECRET: str = ""
    GOOGLE_OAUTH_REFRESH_TOKEN: str = ""
    UPWORK_PROPOSAL_TEMPLATE_ID: str = "1BnxRE-zYcri2VuUD5g8M9dzs0sRfNgP2JGU3ek6ztlY"
    UPWORK_SCRIPT_TEMPLATE_ID: str = "1pHZWkjufcmc5JWYS-ide3xxuRsC6UFp5jnKtuJ2khgI"
    UPWORK_TRACKING_SHEET_ID: str = "1yW6xojrzpgj9fBVz3BD_d6PScVqp5XjlbxrD38iZtxU"
    UPWORK_PROPOSAL_FIELDS_MODEL: str = "openai/gpt-4o-mini"
    UPWORK_MERMAID_MODEL: str = "openai/gpt-4o-mini"
    UPWORK_APPLICATION_MODEL: str = "openai/gpt-5.1"


settings = WorkerSettings()
