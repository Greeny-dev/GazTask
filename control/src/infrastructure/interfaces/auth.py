from abc import ABC, abstractmethod


class AuthServiceInterface(ABC):
    @staticmethod
    @abstractmethod
    async def check(auth_header: str) -> bool:
        pass
