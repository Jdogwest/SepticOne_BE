from fastapi import APIRouter, Depends
from app.request_services.dao import RequestServiceDAO
from app.request_services.schemas import SRequestService
from app.request_services.rb import RBRequestService


router = APIRouter(prefix='/request_services', tags=['Работа с септиками'])


@router.get("/", summary="Получить все запрошенные услуги", response_model=list[SRequestService])
async def get_all_request_services(request_body: RBRequestService = Depends()) -> list[SRequestService]:
    return await RequestServiceDAO.find_all(**request_body.to_dict())
