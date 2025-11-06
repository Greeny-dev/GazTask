import uvicorn
from fastapi import FastAPI

from log4py import logger
from log4py.rest_logs import DisableLoggingConfig



async def start_api_server(application: FastAPI, host: str, port: int) -> None:
    api_config = DisableLoggingConfig(application, host=host, port=int(port))
    api_server = uvicorn.Server(api_config)

    logger.info(f"WEB Server is configured. Serve on http://{api_config.host}:{api_config.port}")

    await api_server.serve()
