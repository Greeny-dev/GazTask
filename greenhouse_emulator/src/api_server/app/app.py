from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from log4py.rest_logs import RequestIDMiddleware, RequestLoggingMiddleware
from managers.interfaces import GreenhousesManagerInterface

from .greenhouses import greenhouses_dependency, greenhouses_router


def create_app(greenhouses_manager: GreenhousesManagerInterface) -> FastAPI:
    app = FastAPI()

    greenhouses_dependency.dm.set_greenhouse_manager(greenhouses_manager)
    app.include_router(greenhouses_router)

    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
