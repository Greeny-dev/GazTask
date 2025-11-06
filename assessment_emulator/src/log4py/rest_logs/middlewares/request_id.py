import uuid

from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from log4py import logger

from .. import specs
from .common import unattached_send


class RequestIDMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        match scope.get(specs.TYPE_KEY):
            case specs.ConnectionScope.HTTP:
                responder: ASGIApp = RequestIDResponder(self._app)
            case specs.ConnectionScope.WEBSOCKET:
                responder: ASGIApp = RequestIDWebSocketResponder(self._app)
            case _:
                responder = self._app

        await responder(scope, receive, send)


class RequestIDResponder:
    _REQUEST_ID_HEADER_KEY = "X-Request-ID"

    def __init__(self, app: ASGIApp) -> None:
        self._app = app
        self._preserved_send: Send = unattached_send

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        headers = MutableHeaders(scope=scope)

        if (request_id := headers.get(self._REQUEST_ID_HEADER_KEY)) is not None:
            logger.set_request_id(request_id)
        else:
            logger.set_request_id(str(uuid.uuid4()))

        self._preserved_send = send
        await self._app(scope, receive, self._respond_with_request_id)

        self._preserved_send = unattached_send

    async def _respond_with_request_id(self, message: Message) -> None:
        match message.get(specs.TYPE_KEY):
            case specs.SendEvent.RESPONSE_START:
                if (request_id := logger.get_request_id()) is not None:
                    headers = MutableHeaders(scope=message)
                    headers.append(self._REQUEST_ID_HEADER_KEY, request_id)
            case _:
                pass

        await self._preserved_send(message)


class RequestIDWebSocketResponder:
    _REQUEST_ID_HEADER_KEY = "X-Request-ID"

    def __init__(self, app: ASGIApp) -> None:
        self._app = app
        self._preserved_send: Send = unattached_send

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        headers = MutableHeaders(scope=scope)

        if (request_id := headers.get(self._REQUEST_ID_HEADER_KEY)) is not None:
            logger.set_request_id(request_id)
        else:
            logger.set_request_id(str(uuid.uuid4()))

        self._preserved_send = send
        await self._app(scope, receive, self._respond_with_request_id)

        self._preserved_send = unattached_send

    async def _respond_with_request_id(self, message: Message) -> None:
        match message.get(specs.TYPE_KEY):
            case specs.SendEvent.RESPONSE_START:
                if (request_id := logger.get_request_id()) is not None:
                    headers = MutableHeaders(scope=message)
                    headers.append(self._REQUEST_ID_HEADER_KEY, request_id)
            case _:
                pass

        await self._preserved_send(message)
