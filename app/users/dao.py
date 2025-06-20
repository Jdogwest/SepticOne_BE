from sqlalchemy.future import select
from app.dao.base import BaseDAO
from app.users.models import User
from app.database import async_session_maker
from app.septics.models import Septic
from app.septics.dao import SepticDAO


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        user = await super().find_one_or_none(**filter_by)
        if user:
            user.__dict__.pop("password", None)
        return user
    
    @classmethod
    async def find_one_or_none_with_pass(cls, **filter_by):
        user = await super().find_one_or_none(**filter_by)
        return user

    @classmethod
    async def find_all(cls, **filter_by):
        users = await super().find_all(**filter_by)
        for user in users:
            user.__dict__.pop("password", None)
        return users
    

    @classmethod
    async def edit_client(cls, user_id: int, data: dict):
        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one()

            for key, value in data.items():
                setattr(user, key, value)

            await session.commit()
            await session.refresh(user)

            return user
        

    @classmethod
    async def edit_user_full(cls, user_id: int, data: dict):
        async with async_session_maker() as session:
            print(data)
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one()

            for key, value in data['client'].items():
                setattr(user, key, value)

            SepticDAO.edit_septic(user_id, data['septic'])

            await session.commit()
            await session.refresh(user)

            return user
        

    @classmethod
    async def edit_user_full_and_role(cls, user_id: int, data: dict):
        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one()

            for key, value in data['client'].items():
                setattr(user, key, value)

            setattr(user, 'role', data['new_role'])

            SepticDAO.edit_septic(user_id, data['septic'])

            await session.commit()
            await session.refresh(user)

            return user
        

    @classmethod
    async def getClient(cls, user_id: int):
        async with async_session_maker() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one()
            user.__dict__.pop("password", None)

            result = await session.execute(select(Septic).where(Septic.owner_id == user_id))
            septic = result.scalar_one_or_none()

            return {
                "user": user,
                "septic": septic
            }