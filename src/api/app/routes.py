from fastapi import APIRouter

from src.api.app.endpoints import auth, users, movies, movie_import

router = APIRouter()
routers_list = [auth.router, users.router, movies.router, movie_import.router]

for r in routers_list:
    router.include_router(r)
