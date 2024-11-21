from functools import lru_cache

from src.app_settings import AppSettings

@lru_cache
def get_app_settings():
    return AppSettings(_env_file=".env")
