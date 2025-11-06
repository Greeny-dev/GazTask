from typing import NoReturn

from starlette.types import Message


async def unattached_send(_: Message) -> NoReturn:
    msg_exc = "`send` awaitable is not set."
    raise RuntimeError(msg_exc)
