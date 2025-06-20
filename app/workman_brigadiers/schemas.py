import re
from pydantic import BaseModel, Field, field_validator, ConfigDict



class SWorkmanBrigadier(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    workman_id: int = Field(..., description="ID рабочего")
    brigadier_id: int = Field(..., description="ID бригадира")


class SBrigads(BaseModel):
    brigadier_id: int
    workman_ids: list[int]


class SWorkmanBrigadierEdit(BaseModel):
    brigads: list[SBrigads]