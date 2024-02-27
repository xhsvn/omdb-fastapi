from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI



from src.core.database import setup_db


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:

    # Startup
    engine, session_factory = setup_db()
    _application.state.db_engine = engine
    _application.state.session_factory = session_factory

    yield
    
    # Shutdown
    await engine.dispose()




def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app
