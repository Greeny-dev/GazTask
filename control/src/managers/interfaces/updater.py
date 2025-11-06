from abc import ABC, abstractmethod


class UpdaterInterface(ABC):
    @abstractmethod
    async def poll_meterings_once(self):
        pass

    @abstractmethod
    async def poll_statuses_once(self):
        pass