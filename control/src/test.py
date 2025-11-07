import asyncio

from infrastructure.assessment_service import AssessmentInteractor
from infrastructure.greenhouses_service import GreenhouseInteractor
from managers.updater import Updater

gi = GreenhouseInteractor("http://localhost:30103")
ai = AssessmentInteractor("http://localhost:30203")
gpd = Updater(gi, ai, metering_interval=1500, status_interval=900)

asyncio.run(gpd.start())
