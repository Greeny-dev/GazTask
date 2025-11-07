import asyncio
import random
from datetime import datetime
from typing import List

from fastapi import APIRouter, status
from pydantic import BaseModel, conint

router = APIRouter(prefix="", tags=["states"])


class Measurement(BaseModel):
    timestamp: datetime
    temperature: float
    humidity: float
    ph: float


class MeasurementsInput(BaseModel):
    measurements: List[Measurement]


class StateResponse(BaseModel):
    state: conint(ge=0, le=2)


@router.post(
    "/greenhouse_state",
    response_model=StateResponse,
    status_code=status.HTTP_200_OK,
)
async def get_state(data: MeasurementsInput):
    await asyncio.sleep(60 * 10)

    state = random.choices(population=[0, 1, 2], weights=[0.6, 0.3, 0.1], k=1)[0]

    return {"state": state}
