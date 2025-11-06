from dataclasses import dataclass


@dataclass(slots=True)
class RequestFromClient:
    method: str
    endpoint: str
    headers: str
    body: str
    client_ip: str


@dataclass(slots=True)
class ResponseToClient:
    status: int
    headers: str
    body: str
