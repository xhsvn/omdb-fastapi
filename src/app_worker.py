from fastapi import FastAPI

from src.api.worker.routes import router
from src.base_app import create_app


def create_application() -> FastAPI:
    base_app = create_app()
    base_app.include_router(router, prefix="")

    return base_app
