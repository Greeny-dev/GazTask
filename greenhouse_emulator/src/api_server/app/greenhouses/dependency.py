from managers.interfaces import GreenhousesManagerInterface


class DependencyManager:
    def __init__(self):
        self._greenhouse_manager: GreenhousesManagerInterface | None = None

    def set_greenhouse_manager(self, manager: GreenhousesManagerInterface):
        self._greenhouse_manager = manager

    async def get_greenhouse_manager(self) -> GreenhousesManagerInterface:
        return self._greenhouse_manager


dm = DependencyManager()
