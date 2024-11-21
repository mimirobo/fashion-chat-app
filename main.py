import sys
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.api import health, ws_api, intent_api
from src.api.tags_metadata import tags_metadata
from src.dependencies import get_app_settings
from src.logger import logger

try:
    app_settings = get_app_settings()
except Exception as e:
    logger.critical("Error in App Settings: %s", e)
    sys.exit(-1)


def add_api_routers(fa_app: FastAPI):
    fa_app.include_router(health.router, prefix="/health")
    fa_app.include_router(ws_api.router, prefix="/ws")
    fa_app.include_router(intent_api.router, prefix="/intent")


@asynccontextmanager
async def api_lifespan(fa_app: FastAPI):
    # App Startup
    load_dotenv()
    logger.info("Starting fashion chat service...")
    add_api_routers(fa_app)
    yield
    # App Cleanup
    logger.info("Shutting down fashion chat service")


def create_app() -> FastAPI:
    return FastAPI(
        lifespan=api_lifespan,
        root_path=app_settings.api_path_prefix,
        root_path_in_servers=False,
        openapi_tags=tags_metadata,
    )


if __name__ == "__main__":
    app = create_app()

    @app.get("/", include_in_schema=False)
    async def index():
        return RedirectResponse(url="/docs")

    uvicorn.run(app, host="0.0.0.0", port=8080)
