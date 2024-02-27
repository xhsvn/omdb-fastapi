from fastapi import FastAPI


from src.base_app import create_app
from src.api.worker.routes import router


def create_application() -> FastAPI:
    base_app = create_app()
    base_app.include_router(router, prefix="")

    return base_app