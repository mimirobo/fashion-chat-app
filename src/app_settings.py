import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    api_key: str
    model: str = "gpt-4"


class StreamValidationSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    max_length: Optional[int] = 500
    regex_pattern: Optional[str] = r"^[a-zA-Z0-9 .,!?-]+$"


class IntentClassificationSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    candidate_labels: Optional[dict] = {
        "fashion": 1.0,
        "clothing": 1.0,
        "t-shirt": 1.0,
        "red": 0.3,
    }  # samples
    threshold: Optional[float] = 0.55


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        _env_file=".env", extra="ignore", validate_default=False
    )
    api_path_prefix: Optional[str] = "/"
    commit_sha: Optional[str] = os.getenv("COMMIT_SHA", "")
    environment: Optional[str] = os.getenv("ENVIRONMENT", "")
    openai_client: OpenAISettings
    stream_validation: StreamValidationSettings
    intent_classifier: IntentClassificationSettings

    def __init__(self, *args, **kwargs):
        kwargs["openai_client"] = OpenAISettings(
            _env_file=kwargs["_env_file"], _env_prefix="OPENAI_"
        )
        kwargs["stream_validation"] = StreamValidationSettings(
            _env_file=kwargs["_env_file"], _env_prefix="STREAM_VALIDATION_"
        )
        kwargs["intent_classifier"] = IntentClassificationSettings(
            _env_file=kwargs["_env_file"], _env_prefix="INTENT_CLASSIFICATION_"
        )
        super().__init__(*args, **kwargs)
