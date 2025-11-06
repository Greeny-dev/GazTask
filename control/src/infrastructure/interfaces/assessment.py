from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Measurement:
    timestamp: datetime
    temperature: float
    humidity: float
    ph: float

    def to_dict(self) -> dict:
        data = asdict(self)

        if self.timestamp:
            data["timestamp"] = self.timestamp.isoformat()

        return data

class AssessmentInteractorInterface(ABC):
    @abstractmethod
    async def get_greenhouse_state(self, metering_info: list[Measurement]):
        pass