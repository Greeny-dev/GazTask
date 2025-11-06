from managers.interfaces import StatisticManagerInterface


class DependencyManager:
    def __init__(self):
        self._statistic_manager: StatisticManagerInterface | None = None

    def set_statistic_manager(self, manager: StatisticManagerInterface):
        self._statistic_manager = manager

    async def get_statistic_manager(self) -> StatisticManagerInterface:
        return self._statistic_manager


dm = DependencyManager()
