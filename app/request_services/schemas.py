from pydantic import BaseModel, Field, ConfigDict


class SRequestService(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    service_id: int = Field(..., description="ID услуги")
    amount: int = Field(..., description="Количество услуг")