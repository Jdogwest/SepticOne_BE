import decimal
import re
from pydantic import BaseModel, Field, field_validator, ConfigDict



class SService(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=1, max_length=50, description="Название услуги, от 1 до 50 символов")
    price: decimal.Decimal = Field(..., description="Цена услуги")
    description: str = Field(..., min_length=1, max_length=100, description="Описание услуги, от 1 до 100 символов")
    time_to_complete: float = Field(..., description="Время выполнения услуги в часах")