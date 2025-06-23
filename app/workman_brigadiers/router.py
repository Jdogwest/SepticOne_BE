from fastapi import APIRouter, Depends
from app.workman_brigadiers.dao import WorkmanBrigadierDAO
from app.workman_brigadiers.schemas import SWorkmanBrigadier, SWorkmanBrigadierEdit
from app.workman_brigadiers.rb import RBWorkmanBrigadier
from app.users.dependencies import get_current_manager_user


router = APIRouter(prefix='/workman_brigadiers', tags=['Работа с бригадами'])


@router.get("/", summary="Получить всех рабочих и их бригадиров")
async def get_all_brigades():
    return await WorkmanBrigadierDAO.find_brigades()


@router.put("/edit/", summary="Редактировать связь бригадиров с рабочими")
async def edit_brigadiers_workmans(request_body: SWorkmanBrigadierEdit, manager = Depends(get_current_manager_user)):
    return await WorkmanBrigadierDAO.edit_links(request_body)


@router.get("/free_workers/", summary="Получить всех свободных рабочих")
async def get_free_workers():
    return await WorkmanBrigadierDAO.get_all_free_workers()
