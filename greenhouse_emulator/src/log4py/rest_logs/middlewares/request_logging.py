import json

from log4py import extra_templates, logger
from starlette.datastructures import Headers
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from .. import environment as env
from .. import specs
from .common import unattached_send


class RequestLoggingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        match scope.get(specs.TYPE_KEY):
            case specs.ConnectionScope.HTTP:
                responder: ASGIApp = RequestLoggingResponder(self._app)
            case specs.ConnectionScope.WEBSOCKET:
                responder: ASGIApp = RequestLoggingWebSocketResponder(self._app)
            case _:
                responder = self._app

        await responder(scope, receive, send)


class RequestLoggingResponder:
    _NON_UNICODE_BODY = "<NON_UNICODE_BODY>"

    def __init__(self, app: ASGIApp) -> None:
        self._app = app
        self._response_code: int | None = None
        self._response_headers: str | None = None
        self._response_body: str | None = None
        self._preserved_send: Send = unattached_send

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        cached_body_receive = await self._create_cached_body_receive(scope, receive)
        self._preserved_send = send
        await self._app(scope, cached_body_receive, self._intercept_response_send)

        msg_dbg = "Request is processed."
        logger.debug(
            msg_dbg,
            extra=extra_templates.http.server.ResponseToClient(
                status=self._response_code if self._response_code is not None else -1,
                headers=(
                    self._response_headers if self._response_headers is not None else ""
                ),
                body=self._response_body if self._response_body is not None else "",
            ),
        )

        self._preserved_send = unattached_send
        self._response_code = None
        self._response_headers = None
        self._response_body = None

    async def _create_cached_body_receive(
        self, scope: Scope, receive: Receive
    ) -> Receive:
        request = Request(scope, receive)
        body_chunks: list[bytes] = []
        async for chunk in request.stream():
            body_chunks.append(chunk)
        cached_body = b"".join(body_chunks)

        msg_dbg = "Request is received."
        logger.debug(
            msg_dbg,
            extra=extra_templates.http.server.RequestFromClient(
                method=str(request.method),
                endpoint=str(request.url),
                headers=self._get_request_headers(request),
                body=self._decode_and_truncate_body(cached_body),
                client_ip=request.client.host if request.client is not None else "",
            ),
        )

        is_cache_used = False

        async def _receive() -> Message:
            nonlocal is_cache_used
            if not is_cache_used:
                is_cache_used = True
                cached_message = {
                    specs.TYPE_KEY: specs.ReceiveEvent.REQUEST,
                    specs.BODY_KEY: cached_body,
                    specs.MORE_BODY_KEY: False,
                }
                return cached_message
            return await receive()

        return _receive

    async def _intercept_response_send(self, message: Message) -> None:
        match message.get(specs.TYPE_KEY):
            case specs.SendEvent.RESPONSE_START:
                self._response_code = int(message[specs.STATUS_KEY])
                self._response_headers = self._format_response_headers(
                    message[specs.HEADERS_KEY]
                )
            case specs.SendEvent.RESPONSE_BODY:
                self._response_body = self._decode_and_truncate_body(
                    message[specs.BODY_KEY]
                )
            case _:
                pass

        await self._preserved_send(message)

    def _get_request_headers(self, request: Request) -> str:
        return self._format_headers(request.headers)

    def _format_response_headers(
        self, raw_response_headers: list[tuple[bytes, bytes]]
    ) -> str:
        headers = Headers(raw=raw_response_headers)
        return self._format_headers(headers)

    def _format_headers(self, raw_headers: Headers) -> str:
        headers = dict(raw_headers.items())
        return json.dumps(headers)

    def _decode_and_truncate_body(self, encoded_body: bytes) -> str:
        try:
            body = encoded_body.decode()
        except UnicodeDecodeError:
            return self._NON_UNICODE_BODY

        if len(body) > env.REST4PY_MAXIMUM_BODY_LOG_SIZE:
            body = body[: env.REST4PY_MAXIMUM_BODY_LOG_SIZE] + "..."
        return body


class RequestLoggingWebSocketResponder:
    _NON_UNICODE_BODY = "<NON_UNICODE_BODY>"

    def __init__(self, app: ASGIApp) -> None:
        self._app = app
        self._response_code: int | None = None
        self._response_headers: str | None = None
        self._response_body: str | None = None
        self._preserved_send: Send = unattached_send

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self._preserved_send = send
        await self._app(scope, receive, self._intercept_response_send)

        self._preserved_send = unattached_send
        self._response_code = None
        self._response_headers = None
        self._response_body = None

    async def _intercept_response_send(self, message: Message) -> None:
        match message.get(specs.TYPE_KEY):
            case specs.SendEvent.RESPONSE_START:
                self._response_code = int(message[specs.STATUS_KEY])
                self._response_headers = self._format_response_headers(
                    message[specs.HEADERS_KEY]
                )
            case specs.SendEvent.RESPONSE_BODY:
                self._response_body = self._decode_and_truncate_body(
                    message[specs.BODY_KEY]
                )
            case _:
                pass

        await self._preserved_send(message)

    def _decode_and_truncate_body(self, encoded_body: bytes) -> str:
        try:
            body = encoded_body.decode()
        except UnicodeDecodeError:
            return self._NON_UNICODE_BODY

        if len(body) > env.REST4PY_MAXIMUM_BODY_LOG_SIZE:
            body = body[: env.REST4PY_MAXIMUM_BODY_LOG_SIZE] + "..."
        return body
