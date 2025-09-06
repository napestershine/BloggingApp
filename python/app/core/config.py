# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from typing import Optional

class Settings(BaseSettings):
    # Core
    database_url: SecretStr = Field(..., alias="DATABASE_URL")  # SecretStr masks value in repr/logs
    secret_key: SecretStr = Field("your-secret-key-here", alias="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Twilio WhatsApp (masked)
    twilio_account_sid: Optional[SecretStr] = Field(default=None, alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[SecretStr]  = Field(default=None, alias="TWILIO_AUTH_TOKEN")
    twilio_whatsapp_number: Optional[str]   = Field(default=None, alias="TWILIO_WHATSAPP_NUMBER")

    # Settings behavior
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,   # EMAIL_HOST or email_host both work (if you add those later)
        extra="ignore",         # ✨ prevents “Extra inputs are not permitted … value='XYZ'” logs
    )

settings = Settings()
