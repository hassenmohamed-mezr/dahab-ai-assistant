from config import settings


def test_settings_defaults():
    assert settings.APP_NAME == "Dahab AI Assistant"
    assert settings.MODEL_NAME == "gpt-5.5"
    assert settings.DATABASE_URL.startswith("sqlite:///")
    assert settings.DEBUG is False
