import uvicorn
from fastapi import FastAPI

from log4py import logger
from log4py.rest_logs import DisableLoggingConfig


def start_api_server(application: FastAPI, host: str, port: int) -> None:
    api_config = DisableLoggingConfig(application, host=host, port=int(port))
    api_server = uvicorn.Server(api_config)

    msg_info = (
        "WEB Server is configured. "
        f"Serve on http://{api_config.host}:{api_config.port}."
    )
    logger.info(msg_info)

    api_server.run()
