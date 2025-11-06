from managers.interfaces import UpdaterInterface


class DependencyManager:
    def __init__(self):
        self._update_manager: UpdaterInterface | None = None

    def set_update_manager(self, manager: UpdaterInterface):
        self._update_manager = manager

    async def get_update_manager(self) -> UpdaterInterface:
        return self._update_manager


dm = DependencyManager()
