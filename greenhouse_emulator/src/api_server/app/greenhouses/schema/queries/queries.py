import datetime
from typing import List, Optional

from pydantic import BaseModel


class MeteringsRequest(BaseModel):
    greenhouses: List[int]
    dt_from: Optional[datetime.datetime] = None
    dt_to: Optional[datetime.datetime] = None
