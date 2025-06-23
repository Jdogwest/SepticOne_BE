from datetime import date, datetime, time
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class SRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    client_id: int
    contract_number: str | None
    status: str
    summary: int
    septic_id: int
    planed_start_time: time
    planed_start_date: date
    comment: str
    work_comment: str



class ServiceItem(BaseModel):
    service_id: int
    amount: int


class SRequestCreate(BaseModel):
    planed_start_date: date
    planed_start_time: time
    comment: Optional[str] = None
    services: List[ServiceItem]



class SUserShort(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: Optional[str] = None
    phone_number: Optional[str] = None

class SSepticShort(BaseModel):
    id: int
    model: str
    volume: int
    city: str
    street: str
    house: str


class SRequestServiceShort(BaseModel):
    service_id: int
    amount: int
    name: str

class SRequestFull(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    client_id: int
    contract_number: Optional[str]
    status: str
    summary: int
    septic_id: int
    planed_start_time: time
    planed_start_date: date
    comment: Optional[str]
    work_comment: Optional[str]
    brigadier_id: Optional[int] = None 

    client: SUserShort
    septic: SSepticShort
    services: List[SRequestServiceShort]


class SRequestServiceShortEdit(BaseModel):
    service_id: int
    amount: int


class SRequestEdit(BaseModel):
    status: Optional[str] = None
    planed_start_time: Optional[time] = None
    planed_start_date: Optional[date] = None
    brigadier_id: Optional[int] = None
    contract_number: Optional[str] = None
    comment: Optional[str] = None
    work_comment: Optional[str] = None
    services: List[SRequestServiceShortEdit] = []
    



