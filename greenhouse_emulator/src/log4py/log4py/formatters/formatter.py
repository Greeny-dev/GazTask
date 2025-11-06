import abc
import logging
import time

from . import date


class Formatter(logging.Formatter, abc.ABC):
    """Base Formatter."""

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def format(self, record: logging.LogRecord) -> str:
        return super().format(record)

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = ...) -> str:
        ct = self.converter(record.created)
        if datefmt:
            if date.MILLISECONDS_DIRECTIVE in datefmt:
                msecs = "%03d" % record.msecs
                datefmt = datefmt.replace(date.MILLISECONDS_DIRECTIVE, msecs)
            return time.strftime(datefmt, ct)

        s = time.strftime(self.default_time_format, ct)
        if self.default_msec_format:
            s = self.default_msec_format % (s, record.msecs)
        return s

    def _get_trace(self, record: logging.LogRecord) -> str | None:
        if record.exc_text is not None:
            return record.exc_text
        if record.exc_info:
            return self.formatException(record.exc_info)
        return None
