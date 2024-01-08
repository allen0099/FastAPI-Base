from fastapi import APIRouter

from . import root

routes: APIRouter = APIRouter()


for route in [
    root,
]:
    if hasattr(route, "router"):
        routes.include_router(route.router)
