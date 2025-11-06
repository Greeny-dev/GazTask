import os
import asyncio

from api_server import create_app, start_api_server
from log4py import logger
from managers import StatisticsManager
from managers.updater import Updater
from infrastructure.assessment_service import AssessmentInteractor
from infrastructure.greenhouses_service import GreenhouseInteractor
from infrastructure.auth_service import AuthService

async def main() -> int:
    greenhouse_interactor_url = os.getenv("GREENHOUSE_SERVICE")
    assessment_interactor_url = os.getenv("ASSESSMENT_SERVICE")

    try:
        gi = GreenhouseInteractor(greenhouse_interactor_url)
        ai = AssessmentInteractor(assessment_interactor_url)
        auth_service = AuthService()
    except Exception:
        msg_crit = "Error during infrastructure init. Check Configs"
        logger.critical(msg_crit)
        return 1

    try:
        statistic_manager = StatisticsManager()
        updater_manager = Updater(gi, ai)
    except Exception:
        msg_crit = "Error during managers init. Check Configs"
        logger.critical(msg_crit)
        return 1

    try:
        app = create_app(
            statistic_manager,
            updater_manager,
            auth_service
        )
    except Exception:
        msg_crit = "Error during service's initialization. Check configs."
        logger.critical(msg_crit)
        return 1

    host = os.getenv("API_SERVER_HOST")
    port = int(os.getenv("API_SERVER_PORT"))

    upd_task = asyncio.create_task(updater_manager.start())

    api_task = start_api_server(
        app,
        host=host,
        port=port,
    )

    await asyncio.gather(upd_task, api_task)

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())

    os._exit(exit_code)
