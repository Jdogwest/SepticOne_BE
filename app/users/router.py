from fastapi import APIRouter, Depends
from app.users.dao import UserDAO
from app.users.schemas import SUser, SUserEdit, SUserEditFull, SUserEditFullAndRole
from app.users.rb import RBUser
from app.users.models import User
from app.users.dependencies import get_current_admin_user, get_current_manager_user, get_current_user


router = APIRouter(prefix='/users', tags=['Работа с пользователями'])


@router.get("/", summary="Получить всех пользователей", response_model=list[SUser])
async def get_all_users(request_body: RBUser = Depends()) -> list[SUser]:
    return await UserDAO.find_all(**request_body.to_dict())


@router.get("/{id}", summary="Получить одного пользователя по id")
async def get_user_by_id(id: int, admin: User = Depends(get_current_manager_user)):
    rez = await UserDAO.getClient(id)
    if rez is None:
        return {'message': f'Пользователь с id {id} не найден!'}
    
    return rez


@router.get("/me/", summary="Получить текущего пользователя")
async def get_me(user_data: User = Depends(get_current_user)):
    return await UserDAO.getClient(user_data.id)


@router.get("/all_users/", summary="Получить всех пользователей. Только для администратора")
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UserDAO.find_all()

@router.get("/all_clients/", summary="Получить всех клиентов. Лдя менеджера и админа")
async def get_all_clients(user_data: User = Depends(get_current_manager_user)):
    return await UserDAO.find_all(role="client")


@router.post("/edit-user/", summary="Редактировать пользователя. Для клиента")
async def edit_user(user_data: SUserEdit, user: User = Depends(get_current_user)):
    return await UserDAO.edit_client(user.id, user_data.model_dump())

@router.post("/edit-user-full/{user_id}", summary="Редактировать пользователя. Для менеджера и админа")
async def edit_user(user_id: int, user_data: SUserEditFull, user: User = Depends(get_current_manager_user)):
    return await UserDAO.edit_user_full(user_id, user_data.model_dump())

@router.post("/edit-user-and-role/{user_id}", summary="Редактировать пользователя и роль. Только для админа")
async def edit_user_and_roll(user_id: int, user_data: SUserEditFullAndRole, user: User = Depends(get_current_admin_user)):
    return await UserDAO.edit_user_full_and_role(user_id, user_data.model_dump())
