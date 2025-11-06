from abc import ABC, abstractmethod


class StatisticManagerInterface(ABC):
    @abstractmethod
    async def get_available_filters(self):
        pass

    @abstractmethod
    async def get_greenhouses_statistics(self, region_id: int | None, state: int | None):
        pass

    @abstractmethod
    async def get_greenhouse_status_history(self, greenhouse_id: int):
        pass

    @abstractmethod
    async def get_meterings(self, page_number: int):
        pass

    @abstractmethod
    async def update_metering_value(self, metering_id: int, new_value: float):
        pass