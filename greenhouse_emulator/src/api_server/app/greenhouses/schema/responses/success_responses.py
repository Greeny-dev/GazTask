from datetime import datetime
from typing import List, Optional, Tuple

from pydantic import BaseModel, RootModel


class MeteringPoint(RootModel[List[Tuple[datetime, Optional[float]]]]):
    pass


class GreenhouseMeterings(BaseModel):
    id: int
    data: MeteringPoint


GreenhousesMeteringsResponse = list[GreenhouseMeterings]
