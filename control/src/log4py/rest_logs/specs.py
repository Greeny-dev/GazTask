from enum import StrEnum

TYPE_KEY = "type"
BODY_KEY = "body"
MORE_BODY_KEY = "more_body"
HEADERS_KEY = "headers"
STATUS_KEY = "status"


class ConnectionScope(StrEnum):
    HTTP = "http"
    WEBSOCKET = "websocket"


class HTTPEvent(StrEnum):
    def __get__(self, _instance, _owner) -> str:  # noqa
        return f"http.{self}"


class WebSocketEvent(StrEnum):
    def __get__(self, _instance, _owner) -> str:  # noqa
        return f"websocket.{self}"


class ReceiveEvent(HTTPEvent, WebSocketEvent):
    REQUEST = "request"
    DISCONNECT = "disconnect"
    WEBSOCKET_CONNECT = "websocket.connect"
    WEBSOCKET_DISCONNECT = "websocket.disconnect"


class SendEvent(HTTPEvent, WebSocketEvent):
    RESPONSE_START = "response.start"
    RESPONSE_BODY = "response.body"
    WEBSOCKET_MESSAGE = "websocket.message"
