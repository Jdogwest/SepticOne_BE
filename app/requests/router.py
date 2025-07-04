from datetime import date
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


@router.get('/{id:int}/', summary="Получить заявку по id")
async def get_request_by_id(id: int, user_data: User = Depends(get_current_manager_user)):
    return await RequestDAO.find_request_by_id(id)


@router.get('/busy_dates/', summary="Получить список занятых дат")
async def get_busy_dates():
    return await RequestDAO.find_busy_dates()


@router.put("/edit/{id}/", summary="Редактировать заявку")
async def edit_request(id: int, data: SRequestEdit, user_data: User = Depends(get_current_manager_user)):
    return await RequestDAO.edit_request(id, data)


@router.get('/brigades_on_date/{date}', summary="Получить бригады на определенную дату")
async def get_brigades_on_date(date: date, user_data: User = Depends(get_current_manager_user)):
    return await RequestDAO.find_brigades_on_date(date)