from fastapi import APIRouter, Depends
from app.requests.dao import RequestDAO
from app.requests.schemas import SRequestCreate, SRequestEdit, SRequestFull
from app.users.dependencies import get_current_manager_user, get_current_user
from app.users.models import User


router = APIRouter(prefix='/requests', tags=['Работа с запросами'])


@router.post("/add/", summary="создать запрос")
async def add_request(request_data: SRequestCreate, user: User = Depends(get_current_user)):
    return await RequestDAO.add_request(request_data, user.id)



@router.get("/all/", summary="Получить все запросы", response_model=list[SRequestFull])
async def get_all_requests(request_status: str | None = None, user_data: User = Depends(get_current_manager_user)):
    return await RequestDAO.find_all_requests(request_status)


@router.get('/my_requests/', summary='Получить мои запросы', response_model=list[SRequestFull])
async def get_my_requests(user_data: User = Depends(get_current_user)):
    return await RequestDAO.find_my_requests(user_data.id)


@router.get('/{id}', summary="Получить заявку по id", response_model = SRequestFull | None)
async def get_request_by_id(id: int, user_data: User = Depends(get_current_manager_user)):
    return await RequestDAO.find_request_by_id(id)


@router.post("/edit/{id}", summary="Редактировать заявку")
async def edit_request(id: int, data: SRequestEdit, user_data: User = Depends(get_current_manager_user)):
    return await RequestDAO.edit_request(id, data)