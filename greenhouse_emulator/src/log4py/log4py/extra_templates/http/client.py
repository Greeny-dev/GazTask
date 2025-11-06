from dataclasses import dataclass


@dataclass(slots=True)
class RequestToServer:
    method: str
    endpoint: str
    headers: str
    body: str
    server_ip: str
    proxy: str


@dataclass(slots=True)
class ResponseFromServer:
    status: int
    headers: str
    body: str
