from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    REDIS_URL: str = "redis://localhost:6379/0"

    # Supabase — required by the /outreach dashboard views in
    # sales_os/web/instantly_routes.py to read from the outreach_* tables.
    SUPABASE_URL: str = ""
    SUPABASE_SECRET_KEY: str = ""

    # Instantly webhook ingress — shared secret Instantly sends in X-Webhook-Secret.
    INSTANTLY_WEBHOOK_SECRET: str = ""


settings = ApiSettings()
