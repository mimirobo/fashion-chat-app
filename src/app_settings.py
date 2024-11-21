import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAISettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    api_key: str


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        _env_file=".env", extra="ignore", validate_default=False
    )
    api_path_prefix: Optional[str] = "/"
    commit_sha: Optional[str] = os.getenv("COMMIT_SHA", "")
    environment: Optional[str] = os.getenv("ENVIRONMENT", "")
    openai: OpenAISettings

    def __init__(self, *args, **kwargs):
        kwargs["openai"] = OpenAISettings(
            _env_file=kwargs["_env_file"], _env_prefix="OPENAI_"
        )
        super().__init__(*args, **kwargs)
