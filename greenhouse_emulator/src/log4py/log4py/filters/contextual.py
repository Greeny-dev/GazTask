import logging

from .. import context


class Filter(logging.Filter):
    """
    Filter responsible for adding contextual information.

    It is better to have filter for such purpose instead of handler or formatter
    because filter applied before logger forwards log record to handlers.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        ctx_vars = [context.ctx_request_id]

        for ctx_var in ctx_vars:
            try:
                setattr(record, ctx_var.name, ctx_var.get())
            except LookupError:
                pass

        return True
