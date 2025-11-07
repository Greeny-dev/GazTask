from http import HTTPMethod, HTTPStatus

import httpx
from httpx import AsyncClient
from infrastructure.interfaces import (AssessmentInteractorInterface,
                                       Measurement)
from log4py import logger

from . import errors


class AssessmentInteractor(AssessmentInteractorInterface):
    def __init__(self, url: str, timeout: int = 60 * 20):
        self._url = url
        self._timeout = timeout

    @errors.catch_errors
    async def get_greenhouse_state(self, measurements: list[Measurement]):
        request = httpx.Request(
            url=f"{self._url}/greenhouse_state",
            method=HTTPMethod.POST,
            json={
                "measurements": [measurement.to_dict() for measurement in measurements]
            },
        )

        logger.debug("Started getting greenhouse state info.")
        response = await self._send_request(request)

        try:
            data = response.json()
        except Exception as exc:
            raise errors.ParsingResponseError(message=str(exc))

        return data

    async def _send_request(self, request: httpx.Request) -> httpx.Response:
        async with AsyncClient(timeout=self._timeout) as client:
            response = await client.send(request)
            await self._check_response(response)

            return response

    @staticmethod
    async def _check_response(response: httpx.Response) -> None:
        if response.status_code != HTTPStatus.OK:
            raise errors.RequestInternalError(
                status_code=response.status_code, error_message=response.text
            )
