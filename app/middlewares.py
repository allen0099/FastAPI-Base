import logging
import time

from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from uvicorn.protocols.utils import get_client_addr, get_path_with_query_string


class LogRequestMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # process the request and get the response
        start_time: float = time.time()
        response: Response = await call_next(request)
        process_time: float = time.time() - start_time

        response.headers["X-Process-Time"] = str(process_time)
        response.background = BackgroundTask(
            self.logging_time,
            request,
            response,
            process_time,
        )

        return response

    @staticmethod
    def logging_time(request: Request, response: Response, _time: float):
        access_log: logging.Logger = logging.getLogger("uvicorn.time")

        access_log.info(
            '%s - "%s %s HTTP/%s" %d %f, response bytes: %s',
            get_client_addr(request.scope),  # type: ignore
            request.scope["method"],
            get_path_with_query_string(request.scope),  # type: ignore
            request.scope["http_version"],
            response.status_code,
            _time,
            response.headers.get("Content-Length", 0),
        )
