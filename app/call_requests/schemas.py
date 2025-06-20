from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SCallRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    fio: str
    phone_number: str
    comment: str
    status: str

class SCallRequestCreate(BaseModel):
    fio: str
    phone_number: str
    comment: str


class SCallRequestUpdate(BaseModel):
    comment: str
    status: str