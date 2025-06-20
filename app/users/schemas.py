import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional

from app.septics.schemas import SSepticEdit

class SUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str = Field(..., min_length=3, max_length=50, description="Имя клиента, от 3 до 50 символов")
    surname: str = Field(..., min_length=3, max_length=50, description="Фамилия клиента, от 3 до 50 символов")
    patronymic: Optional[str] = Field(default=None, min_length=3, max_length=50, description="Отчество клиента, от 3 до 50 символов")
    phone_number: Optional[str] = Field(default=None, description="Номер телефона в международном формате, начинающийся с '+'")
    email: str = Field(..., description="Электронная почта клиента")
    role: str = Field(..., min_length=1, max_length=50, description="роль, от 1 до 50 символов")


    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if value is None:
            return value 
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return value
    
    @field_validator("email")
    def validate_email(cls, value):
        if not re.match(r'^\S+@\S+\.\S+$', value):
            raise ValueError('Некорректная электронная почта')
        return value
    

class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    name: str = Field(..., min_length=3, max_length=50, description="Имя клиента, от 3 до 50 символов")
    surname: str = Field(..., min_length=3, max_length=50, description="Фамилия клиента, от 3 до 50 символов")
    patronymic: str = Field(default=None, description="Отчество клиента, от 3 до 50 символов")
    
    @field_validator("email")
    def validate_email(cls, value):
        if not re.match(r'^\S+@\S+\.\S+$', value):
            raise ValueError('Некорректная электронная почта')
        return value
    

class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


class SUserEdit(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Имя клиента, от 3 до 50 символов")
    surname: str = Field(..., min_length=3, max_length=50, description="Фамилия клиента, от 3 до 50 символов")
    patronymic: str = Field(default=None, description="Отчество клиента, от 3 до 50 символов")
    email: str = Field(..., description="Электронная почта клиента")
    phone_number: Optional[str] = Field(None, description="Номер телефона в международном формате, начинающийся с '+'")

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        if value is None:
            return value
        if not re.match(r'^\+\d{1,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return value
    
class SUserEditFull(BaseModel):
    client: SUserEdit
    septic: SSepticEdit

class SUserEditFullAndRole(BaseModel):
    client: SUserEdit
    septic: SSepticEdit
    new_role: str