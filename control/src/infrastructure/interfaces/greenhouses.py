from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class MeteringRequest:
    greenhouses: list[int]
    dt_from: datetime | None = None
    dt_to: datetime | None = None

    def to_dict(self) -> dict:
        data = asdict(self)

        if self.dt_from:
            data["dt_from"] = self.dt_from.isoformat()
        if self.dt_to:
            data["dt_to"] = self.dt_to.isoformat()

        return data


class GreenhousesInteractorInterface(ABC):
    @abstractmethod
    async def get_greenhouse_info(self, greenhouse_id: int):
        pass

    @abstractmethod
    async def get_temperature_metering(self, request: MeteringRequest):
        pass

    @abstractmethod
    async def get_humidity_metering(self, request: MeteringRequest):
        pass

    @abstractmethod
    async def get_ph_metering(self, request: MeteringRequest):
        pass
