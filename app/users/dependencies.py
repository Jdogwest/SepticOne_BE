

from datetime import datetime, timezone
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from app.config import get_auth_data
from app.users.dao import UserDAO
from app.users.models import User


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


def decode_token(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')


def check_token(payload = Depends(decode_token)):
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    return payload


async def get_current_user(payload = Depends(check_token)):
    user_id = payload.get('sub')
    
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    user = await UserDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    
    user.__dict__.pop("password", None)
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role == "admin":
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')

async def get_current_manager_user(current_user: User = Depends(get_current_user)):
    if current_user.role == "manager" or current_user.role == "admin":
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')