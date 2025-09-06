# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, field_validator
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
    
    # WhatsApp notification safety features
    whatsapp_notifications_enabled: bool = Field(default=False, alias="WHATSAPP_NOTIFICATIONS_ENABLED")
    whatsapp_rate_limit_per_minute: int = Field(default=10, alias="WHATSAPP_RATE_LIMIT_PER_MINUTE")
    whatsapp_rate_limit_per_hour: int = Field(default=100, alias="WHATSAPP_RATE_LIMIT_PER_HOUR")
    
    # CORS configuration - accepts comma-separated string or list
    cors_origins: str = Field(default="http://localhost:3000,http://localhost:8080", alias="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, alias="CORS_ALLOW_CREDENTIALS")

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string"""
        if isinstance(self.cors_origins, str):
            # Split by comma and strip whitespace
            return [origin.strip() for origin in self.cors_origins.split(',') if origin.strip()]
        return self.cors_origins

    # Settings behavior
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,   # EMAIL_HOST or email_host both work (if you add those later)
        extra="ignore",         # ✨ prevents “Extra inputs are not permitted … value='XYZ'” logs
    )

settings = Settings()
