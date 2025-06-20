from app.dao.base import BaseDAO
from app.septics.models import Septic
from app.database import async_session_maker
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


class SepticDAO(BaseDAO):
    model = Septic

    @classmethod
    async def find_full_data(cls):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.owner))
            result = await session.execute(query)

            if not result:
                return None
            
            return result.scalars().all()
            

    @classmethod
    async def edit_septic(cls, user_id: int, data: dict):
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.owner_id == user_id))
            septic = result.scalar_one_or_none()
            if (not septic):
                await SepticDAO.add(owner_id=user_id, **data)

                await session.commit()

                result = await session.execute(select(cls.model).where(cls.model.owner_id == user_id))
                septic = result.scalar_one_or_none()
                return septic

            for key, value in data.items():
                setattr(septic, key, value)

            await session.commit()
            await session.refresh(septic)

            return septic