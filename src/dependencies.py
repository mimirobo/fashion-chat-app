from functools import lru_cache

from src.app_settings import AppSettings
from src.utils.validators.stream_validators import StreamValidatorBuilder


@lru_cache
def get_app_settings():
    return AppSettings(_env_file=".env")


def get_stream_validator():
    validation_settings = get_app_settings().stream_validation
    return (
        StreamValidatorBuilder()
        .add_length_validator(validation_settings.max_length)
        .add_regex_validator(validation_settings.regex_pattern)
        .add_html_escape_validator()
        .build()
    )
