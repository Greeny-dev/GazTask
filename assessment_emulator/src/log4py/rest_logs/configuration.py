import asyncio
import logging
import os
import ssl
from typing import Any, Awaitable, Callable, Type

from uvicorn import Config
from uvicorn.config import (
    HTTPProtocolType,
    InterfaceType,
    LifespanType,
    WSProtocolType,
)


class DefaultConfig(Config):
    pass


# Disable all logs from uvicorn
class DisableLoggingConfig(DefaultConfig):
    def __init__(
        self,
        app: Any | Callable[..., Any] | str,  # noqa: ANN401
        host: str,
        port: int,
        uds: str | None = None,
        fd: int | None = None,
        loop = "auto",
        http: HTTPProtocolType | Type[asyncio.Protocol] = "auto",
        ws: WSProtocolType | Type[asyncio.Protocol] = "auto",
        ws_max_size: int = 16 * 1024 * 1024,
        ws_ping_interval: float | None = 20,
        ws_ping_timeout: float | None = 20,
        ws_per_message_deflate: bool = True,
        lifespan: LifespanType = "auto",
        env_file: str | os.PathLike | None = None,
        interface: InterfaceType = "auto",
        reload: bool = False,
        reload_dirs: list[str] | str | None = None,
        reload_delay: float = 0.25,
        reload_includes: list[str] | str | None = None,
        reload_excludes: list[str] | str | None = None,
        workers: int | None = None,
        proxy_headers: bool = True,
        server_header: bool = True,
        date_header: bool = True,
        forwarded_allow_ips: list[str] | str | None = None,
        root_path: str = "",
        limit_concurrency: int | None = None,
        limit_max_requests: int | None = None,
        backlog: int = 2048,
        timeout_keep_alive: int = 5,
        timeout_notify: int = 30,
        timeout_graceful_shutdown: int | None = None,
        callback_notify: Callable[..., Awaitable[None]] | None = None,
        ssl_keyfile: str | None = None,
        ssl_certfile: str | os.PathLike | None = None,
        ssl_keyfile_password: str | None = None,
        ssl_version: int = ssl.PROTOCOL_TLS_SERVER,
        ssl_cert_reqs: int = ssl.CERT_NONE,
        ssl_ca_certs: str | None = None,
        ssl_ciphers: str = "TLSv1",
        headers: list[tuple[str, str]] | None = None,
        factory: bool = False,
        h11_max_incomplete_event_size: int | None = None,
    ) -> None:
        self.__disable_logging()

        super().__init__(
            app,
            host,
            port,
            uds,
            fd,
            loop,
            http,
            ws,
            ws_max_size,
            ws_ping_interval,
            ws_ping_timeout,
            ws_per_message_deflate,
            lifespan,
            env_file,
            None,
            None,
            False,
            False,
            interface,
            reload,
            reload_dirs,
            reload_delay,
            reload_includes,
            reload_excludes,
            workers,
            proxy_headers,
            server_header,
            date_header,
            forwarded_allow_ips,
            root_path,
            limit_concurrency,
            limit_max_requests,
            backlog,
            timeout_keep_alive,
            timeout_notify,
            timeout_graceful_shutdown,
            callback_notify,
            ssl_keyfile,
            ssl_certfile,
            ssl_keyfile_password,
            ssl_version,
            ssl_cert_reqs,
            ssl_ca_certs,
            ssl_ciphers,
            headers,
            factory,
            h11_max_incomplete_event_size,
        )

    def __disable_logging(self) -> None:
        loggers_names = ["uvicorn.access", "uvicorn.error", "uvicorn.asgi"]

        for logger_name in loggers_names:
            logging.getLogger(logger_name).disabled = True
