from fastapi import APIRouter, Depends, status
from managers.interfaces import StatisticManagerInterface

from . import dependency, schema

router = APIRouter(prefix="/statistic", tags=[""])


@router.get("/filters", status_code=status.HTTP_200_OK, responses={})
async def get_available_filters(
    manager: StatisticManagerInterface = Depends(dependency.dm.get_statistic_manager),
):
    return await manager.get_available_filters()


@router.get("", status_code=status.HTTP_200_OK, responses={})
async def get_info(
    region_id: int | None = None,
    state: int | None = None,
    manager: StatisticManagerInterface = Depends(dependency.dm.get_statistic_manager),
):
    return await manager.get_greenhouses_statistics(region_id, state)


@router.get(
    "/greenhouse/history/{_id}",
    status_code=status.HTTP_200_OK,
    responses={},
)
async def get_change_history(
    _id: int,
    manager: StatisticManagerInterface = Depends(dependency.dm.get_statistic_manager),
):
    return await manager.get_greenhouse_status_history(_id)


@router.get(
    "/meterings",
    status_code=200,
    responses={},
)
async def get_meterings(
    page: int = 1,
    manager: StatisticManagerInterface = Depends(dependency.dm.get_statistic_manager),
):
    return await manager.get_meterings(page_number=page)


@router.put(
    "/meterings/{metering_id}",
    status_code=200,
    responses={},
)
async def update_metering(
    metering_id: int,
    new_value: float,
    manager: StatisticManagerInterface = Depends(dependency.dm.get_statistic_manager),
):
    return await manager.update_metering_value(metering_id, new_value)
