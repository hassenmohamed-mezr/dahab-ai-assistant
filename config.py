from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from the .env file.
    """

    # ==========================
    # Application
    # ==========================

    APP_NAME: str = "Dahab AI Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # ==========================
    # AI
    # ==========================

    OPENAI_API_KEY: str = ""
    MODEL_NAME: str = "gpt-5.5"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000

    # ==========================
    # WhatsApp
    # ==========================

    WHATSAPP_TOKEN: str = ""
    VERIFY_TOKEN: str = ""
    PHONE_NUMBER_ID: str = ""

    # ==========================
    # Database
    # ==========================

    DATABASE_URL: str = "sqlite:///./dahab.db"

    # ==========================
    # Scheduler
    # ==========================

    TIMEZONE: str = "Africa/Cairo"

    # ==========================
    # Pydantic Settings
    # ==========================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()