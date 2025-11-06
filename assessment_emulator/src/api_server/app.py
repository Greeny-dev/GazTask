from fastapi import FastAPI

from log4py.rest_logs import DisableLoggingConfig, RequestLoggingMiddleware, RequestIDMiddleware
from log4py import logger
import uvicorn
from .route import router


def start_api_server(application: FastAPI, host: str, port: int) -> None:
    api_config = DisableLoggingConfig(application, host=host, port=int(port))
    api_server = uvicorn.Server(api_config)

    msg_info = (
        "WEB Server is configured. "
        f"Serve on http://{api_config.host}:{api_config.port}."
    )
    logger.info(msg_info)

    api_server.run()


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(router)

    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    return app