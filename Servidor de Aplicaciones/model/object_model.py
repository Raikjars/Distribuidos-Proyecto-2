from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ObjectBase(BaseModel):
    Name: Optional[str]

# usado para entregar un objeto
class ObjectInJson(ObjectBase):
    id: int
    Name: str
    Action: str
    CreationDate: datetime

    class Config:
        orm_mode = True