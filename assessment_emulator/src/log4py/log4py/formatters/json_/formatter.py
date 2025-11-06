import logging

from ... import context
from .. import date
from .. import structures as base_struct
from ..formatter import Formatter as BaseFormatter
from .structures import LogJSON


class Formatter(BaseFormatter):
    """JSON Formatter."""

    def format(self, record: logging.LogRecord) -> str:
        log = LogJSON(
            date=self.formatTime(record, datefmt=date.FORMAT),
            context=base_struct.LogContext(
                path=record.pathname,
                line=record.lineno,
            ),
            level=record.levelname,
            message=record.getMessage(),
            request_id=getattr(record, context.ctx_request_id.name, None),
            traceback=self._get_trace(record),
            extra=getattr(record, "extra", None),
        )

        return str(log)
