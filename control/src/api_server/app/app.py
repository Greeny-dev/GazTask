from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.interfaces import AuthServiceInterface
from log4py.rest_logs import RequestIDMiddleware, RequestLoggingMiddleware
from managers.interfaces import StatisticManagerInterface, UpdaterInterface

from .statistic import statistic_dependency, statistic_router
from .update import update_dependency, update_router
from .middlewares import AuthMiddleware
from . import dependency


def create_app(
        statistic_manager: StatisticManagerInterface,
        updater_manager: UpdaterInterface,
        auth_service: AuthServiceInterface
) -> FastAPI:
    app = FastAPI()

    statistic_dependency.dm.set_statistic_manager(statistic_manager)
    app.include_router(statistic_router)

    update_dependency.dm.set_update_manager(updater_manager)
    app.include_router(update_router)

    dependency.auth_service = auth_service

    app.add_middleware(AuthMiddleware)
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
