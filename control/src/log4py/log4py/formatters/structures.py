from dataclasses import dataclass

from ..extra_templates import TemplateTypes


@dataclass(slots=True)
class LogContext:
    path: str
    line: int


@dataclass(slots=True)
class Log:
    date: str
    context: LogContext
    level: str
    message: str
    request_id: str
    traceback: str
    extra: TemplateTypes
