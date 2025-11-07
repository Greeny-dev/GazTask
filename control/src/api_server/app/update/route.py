from fastapi import APIRouter, Depends, status
from managers.interfaces import UpdaterInterface

from . import dependency, schema

router = APIRouter(prefix="/update", tags=[""])


@router.post("/metering", status_code=status.HTTP_200_OK, responses={})
async def update_meterings(
    manager: UpdaterInterface = Depends(dependency.dm.get_update_manager),
):
    return await manager.poll_meterings_once()


@router.post("/state", status_code=status.HTTP_200_OK, responses={})
async def update_states(
    manager: UpdaterInterface = Depends(dependency.dm.get_update_manager),
):
    return await manager.poll_statuses_once()
