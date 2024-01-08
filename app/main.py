import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

import config
import routers
from middlewares import LogRequestMiddleware


def create_app() -> FastAPI:
    middleware: list[Middleware] = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
            allow_credentials=True,
        ),
        Middleware(LogRequestMiddleware),
    ]

    if config.DEBUG:
        app: FastAPI = FastAPI(
            debug=True,
            title="Backend API",
            middleware=middleware,
        )

    else:
        app: FastAPI = FastAPI(
            title="Backend API",
            middleware=middleware,
            openapi_url="",
            docs_url="",
            redoc_url="",
        )

    app.include_router(routers.routes)

    return app


if __name__ == "__main__":
    uvicorn.run(
        "main:create_app",
        host=config.get("HOST"),
        port=int(config.get("PORT")),
        reload=config.RELOAD,
        factory=True,
        log_config=config.LOG_CONFIG,
    )
