from http import HTTPMethod, HTTPStatus

import httpx
from httpx import AsyncClient

from log4py import logger

from . import errors
from infrastructure.interfaces import GreenhousesInteractorInterface, MeteringRequest


class GreenhouseInteractor(GreenhousesInteractorInterface):
    def __init__(self, url: str):
        self._url = url

    @errors.catch_errors
    async def get_greenhouse_info(self, greenhouse_id: int):
        request = httpx.Request(
            url=f"{self._url}/greenhouses_info/{greenhouse_id}",
            method=HTTPMethod.GET,
        )

        logger.debug("Started getting greenhouse info.")
        response = await self._send_request(request)

        try:
            data = response.json()
        except Exception as exc:
            raise errors.ParsingResponseError(message=str(exc))

        return data

    @errors.catch_errors
    async def get_temperature_metering(self, metering_request: MeteringRequest):
        request = httpx.Request(
            url=f"{self._url}/temperature",
            method="POST",
            json=metering_request.to_dict()
        )

        logger.debug("Getting temperature metering.")
        response = await self._send_request(request)

        try:
            data = response.json()
        except Exception as exc:
            raise errors.ParsingResponseError(message=str(exc))

        return data

    @errors.catch_errors
    async def get_humidity_metering(self, metering_request: MeteringRequest):
        request = httpx.Request(
            url=f"{self._url}/humidity",
            method="POST",
            json=metering_request.to_dict()
        )

        logger.debug("Getting humidity metering.")
        response = await self._send_request(request)

        try:
            data = response.json()
        except Exception as exc:
            raise errors.ParsingResponseError(message=str(exc))

        return data

    @errors.catch_errors
    async def get_ph_metering(self, metering_request: MeteringRequest):
        request = httpx.Request(
            url=f"{self._url}/ph",
            method="POST",
            json=metering_request.to_dict()
        )

        logger.debug("Getting PH metering.")
        response = await self._send_request(request)

        try:
            data = response.json()
        except Exception as exc:
            raise errors.ParsingResponseError(message=str(exc))

        return data


    async def _send_request(self, request: httpx.Request) -> httpx.Response:
        async with AsyncClient() as client:
            response = await client.send(request)
            await self._check_response(response)

            return response

    @staticmethod
    async def _check_response(response: httpx.Response) -> None:
        if response.status_code != HTTPStatus.OK:
            raise errors.RequestInternalError(
                status_code=response.status_code, error_message=response.text
            )
