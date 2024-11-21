from functools import lru_cache

from src.app_settings import AppSettings
from src.clients.openai_client import OpenAIStreamingClient
from src.services.client_manager import WebSocketConnectionManager
from src.services.intent_classifier import IntentClassifierService
from src.utils.openai_query_build import OpenAIQueryBuild
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


def get_openai_client():
    openai_settings = get_app_settings().openai_client
    return OpenAIStreamingClient(openai_settings)


def get_connection_manager():
    return WebSocketConnectionManager()


def get_openai_query_builder():
    return OpenAIQueryBuild()


@lru_cache
def get_intent_classifier():
    intent_settings = get_app_settings().intent_classifier
    return IntentClassifierService(settings=intent_settings)
