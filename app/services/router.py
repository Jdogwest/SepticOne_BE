from fastapi import APIRouter, Depends
from app.services.dao import ServiceDAO
from app.services.schemas import SService
from app.services.rb import RBService


router = APIRouter(prefix='/services', tags=['Работа с услугами'])


@router.get("/", summary="Получить все услуги", response_model=list[SService])
async def get_all_services(request_body: RBService = Depends()) -> list[SService]:
    return await ServiceDAO.find_all(**request_body.to_dict())

@router.get("/{id}/", summary="Получить одну услугу по id")
async def get_service_by_id(service_id: int) -> SService | None:
    rez = await ServiceDAO.find_one_or_none_by_id(service_id)
    if rez is None:
        return {'message': f'Услуга с id {service_id} не найдена!'}
    return rez