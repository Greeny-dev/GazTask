import functools

from httpx import HTTPError


class GreenhouseInteractorBaseError(Exception):
    """Base exception for app level errors"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class RequestExternalError(GreenhouseInteractorBaseError):
    """An exception for external errors"""

    pass


class RequestInternalError(GreenhouseInteractorBaseError):
    """An exception for internal backend errors"""

    def __init__(self, status_code: int, error_message: str):
        self.message = f"""Internal error was received:
            Status code: {status_code}
            Error message: {error_message}
        """


class ParsingResponseError(GreenhouseInteractorBaseError):
    """An exception for parsing response errors"""


class UnexpectedGreenhouseInteractorError(GreenhouseInteractorBaseError):
    """An exception for unexpected errors"""

    pass


def catch_errors(func):
    @functools.wraps(func)
    async def function_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPError as exc:
            raise RequestExternalError(message=str(exc))
        except (RequestInternalError, ParsingResponseError) as exc:
            raise exc
        except Exception as exc:
            raise UnexpectedGreenhouseInteractorError(message=str(exc))

    return function_wrapper
