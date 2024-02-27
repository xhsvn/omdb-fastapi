from fastapi import FastAPI

from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check

from src.base_app import create_app
from src.api.app.routes import router


def create_application() -> FastAPI:
    disable_installed_extensions_check()
    base_app = create_app()
    base_app.include_router(router, prefix="/api")
    add_pagination(base_app)


    return base_app