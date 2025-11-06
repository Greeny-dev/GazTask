import base64
import hashlib
from sqlalchemy import select
from infrastructure.database import async_session_maker
from infrastructure.interfaces import AuthServiceInterface
from .models import Users


class AuthService(AuthServiceInterface):
    @staticmethod
    async def check(authorization_header: str | None = None) -> bool:
        if not authorization_header or not authorization_header.startswith("Basic "):
            return False

        try:
            encoded = authorization_header.split(" ")[1]
            decoded = base64.b64decode(encoded).decode("utf-8")
            username, password = decoded.split(":", 1)
        except Exception:
            return False

        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

        async with async_session_maker() as session:
            query = select(Users).where(Users.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

        if not user:
            return False

        return user.password_hash == password_hash
