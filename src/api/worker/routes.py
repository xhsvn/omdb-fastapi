from fastapi import APIRouter

from src.api.worker.endpoints import movies_fetch

router = APIRouter()
routers_list = [movies_fetch.router]

for r in routers_list:
    router.include_router(r)
