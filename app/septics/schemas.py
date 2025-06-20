from pydantic import BaseModel, Field, ConfigDict


class SSeptic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    city: str = Field(..., min_length=1, max_length=50, description="Город, от 1 до 50 символов")
    street: str = Field(..., min_length=1, max_length=50, description="Улица, от 1 до 50 символов")
    house: str = Field(..., min_length=1, max_length=50, description="Дом, от 1 до 50 символов")
    volume: int = Field(..., description="Объем септика в м3")
    model: str = Field(..., min_length=1, max_length=50, description="Модель септика, от 1 до 50 символов")
    owner_id: int = Field(..., description="ID клиента собственника септика")


class SSepticEdit(BaseModel):
    city: str = Field(..., min_length=1, max_length=50, description="Город, от 1 до 50 символов")
    street: str = Field(..., min_length=1, max_length=50, description="Улица, от 1 до 50 символов")
    house: str = Field(..., min_length=1, max_length=50, description="Дом, от 1 до 50 символов")
    volume: int = Field(..., description="Объем септика в м3")
    model: str = Field(..., min_length=1, max_length=50, description="Модель септика, от 1 до 50 символов")