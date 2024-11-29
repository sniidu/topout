from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class Problem(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int
    gymid: int
    gradeid: int
    added: datetime
    deactivated: Optional[datetime]
