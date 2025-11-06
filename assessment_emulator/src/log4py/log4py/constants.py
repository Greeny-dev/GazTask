import logging
from enum import StrEnum


class LogLevel(StrEnum):
    CRITICAL = logging.getLevelName(logging.CRITICAL)
    ERROR = logging.getLevelName(logging.ERROR)
    WARNING = logging.getLevelName(logging.WARNING)
    INFO = logging.getLevelName(logging.INFO)
    DEBUG = logging.getLevelName(logging.DEBUG)


class LogFormat(StrEnum):
    JSON = "JSON"
    PLAIN = "PLAIN"


class LogVerbosity(StrEnum):
    LOW = "LOW"
    HIGH = "HIGH"
