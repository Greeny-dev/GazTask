from fastapi import APIRouter, Depends, status
from managers.interfaces import GreenhousesManagerInterface

from . import dependency, schema

router = APIRouter(prefix="", tags=["greenhouses, meterings"])


@router.get(
    "/greenhouses_info/{greenhouse_id}", status_code=status.HTTP_200_OK, responses={}
)
async def get_greenhouse(
    greenhouse_id: int,
    manager: GreenhousesManagerInterface = Depends(
        dependency.dm.get_greenhouse_manager
    ),
):
    info = await manager.get_greenhouse_info(greenhouse_id)
    return info


async def _get_meterings(
    manager: GreenhousesManagerInterface,
    request: schema.queries.MeteringsRequest,
    metering_type_name: str,
):
    return await manager.get_meterings(
        greenhouse_ids=request.greenhouses,
        metering_type_name=metering_type_name,
        dt_from=request.dt_from,
        dt_to=request.dt_to,
    )


@router.post(
    "/temperature",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.responses.success_responses.GreenhousesMeteringsResponse
        }
    },
)
async def get_temperature(
    request: schema.queries.MeteringsRequest,
    manager: GreenhousesManagerInterface = Depends(
        dependency.dm.get_greenhouse_manager
    ),
) -> schema.responses.success_responses.GreenhousesMeteringsResponse:

    return await _get_meterings(manager, request, "temperature")


@router.post(
    "/humidity",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.responses.success_responses.GreenhousesMeteringsResponse
        }
    },
)
async def get_humidity(
    request: schema.queries.MeteringsRequest,
    manager: GreenhousesManagerInterface = Depends(
        dependency.dm.get_greenhouse_manager
    ),
) -> schema.responses.success_responses.GreenhousesMeteringsResponse:

    return await _get_meterings(manager, request, "humidity")


@router.post(
    "/ph",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.responses.success_responses.GreenhousesMeteringsResponse
        }
    },
)
async def get_ph(
    request: schema.queries.MeteringsRequest,
    manager: GreenhousesManagerInterface = Depends(
        dependency.dm.get_greenhouse_manager
    ),
) -> schema.responses.success_responses.GreenhousesMeteringsResponse:

    return await _get_meterings(manager, request, "ph")
