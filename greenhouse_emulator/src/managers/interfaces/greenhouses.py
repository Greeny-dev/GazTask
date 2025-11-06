from abc import ABC, abstractmethod


class GreenhousesManagerInterface(ABC):
    @staticmethod
    @abstractmethod
    async def get_greenhouse_info(greenhouse_id: int):
        pass

    @staticmethod
    @abstractmethod
    async def get_meterings(
        greenhouse_ids: list[int],
        metering_type_name: str,
        dt_from: str | None = None,
        dt_to: str | None = None,
    ):
        pass
