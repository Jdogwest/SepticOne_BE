from sqlalchemy import select
from app.dao.base import BaseDAO
from app.call_requests.models import CallRequest
from app.database import async_session_maker


class CallRequestDAO(BaseDAO):
    model = CallRequest


    @classmethod
    async def add_call_request(cls, request_data: dict):
        async with async_session_maker() as session:
            await CallRequestDAO.add(**request_data)
            return {'message': 'Заявка добавлена!'}
        

    @classmethod
    async def edit_call_request(cls, request_id: int, request_data: dict):
        async with async_session_maker() as session:
            result = await session.execute(select(CallRequest).where(CallRequest.id == request_id))
            request = result.scalar_one()

            for key, value in request_data.items():
                setattr(request, key, value)

            await session.commit()
            await session.refresh(request)

            return request