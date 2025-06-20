import logging
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.requests.models import Request
from app.requests.schemas import SRequestCreate, SRequestEdit
from app.database import async_session_maker
from app.septics.models import Septic
from app.services.models import Service
from app.request_services.models import RequestService
from app.requests.rb import RBRequest
from app.users.models import User


class RequestDAO(BaseDAO):
    model = Request

    @classmethod
    async def add_request(cls, data: SRequestCreate, user_id: int):
        async with async_session_maker() as session:
            result_septic = await session.execute(
                select(Septic).where(Septic.owner_id == user_id)
            )
            septic = result_septic.scalars().first()
            if not septic:
                raise ValueError("У пользователя нет привязанного септика")

            result_services = await session.execute(
                select(Service)
            )
            services = result_services.scalars().all()

            service_map = {s.id: s.price for s in services}

            total_summary = 0
            for item in data.services:
                service_id = item.service_id
                amount = item.amount
                if service_id in service_map:
                    total_summary += service_map[service_id] * amount
                else:
                    raise ValueError(f"Услуга с ID {service_id} не найдена в базе")

            
            new_request = cls.model(
                client_id = user_id,
                septic_id = septic.id,
                status = 'new',
                planed_start_time = data.planed_start_time,
                planed_start_date = data.planed_start_date,
                comment = data.comment,
                summary = total_summary)
            
            session.add(new_request)

            await session.commit()
            await session.refresh(new_request)

            for serv in data.services:
                new_service_request_item = RequestService(
                    request_id = new_request.id,
                    amount = serv.amount,
                    service_id = serv.service_id
                )
                session.add(new_service_request_item)

            await session.commit()

            created_request = await session.execute(
                select(Request).where(Request.id == new_request.id)
                .options(
                    selectinload(Request.client),
                    selectinload(Request.septic),
                    selectinload(Request.services).selectinload(RequestService.service)
                )
            )
            created_request = created_request.scalar_one()


            return created_request.to_dict()
        

    @classmethod
    async def find_all_requests(cls, request_status: str = None):
        async with async_session_maker() as session:
            if request_status:
                result = await session.execute(
                select(cls.model).where(Request.status == request_status)
                .options(
                    selectinload(cls.model.client),
                    selectinload(cls.model.septic),
                    selectinload(cls.model.services).selectinload(RequestService.service)
                )
            ) 
            else:
                result = await session.execute(
                    select(cls.model)
                    .options(
                        selectinload(cls.model.client),
                        selectinload(cls.model.septic),
                        selectinload(cls.model.services).selectinload(RequestService.service)
                    )
                )
            requests = result.scalars().all()

            return [req.to_dict() for req in requests]
        

    @classmethod
    async def find_my_requests(cls, user_id: int):
       async with async_session_maker() as session:
           result = await session.execute(
                select(cls.model)
                .where(cls.model.client_id == user_id)
                .options(
                    selectinload(cls.model.client),
                    selectinload(cls.model.septic),
                    selectinload(cls.model.services).selectinload(RequestService.service)
                )
            )
           requests = result.scalars().all()
           return [req.to_dict() for req in requests]


    @classmethod
    async def find_request_by_id(cls, id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(cls.model).where(Request.id == id)
                .options(
                    selectinload(cls.model.client),
                    selectinload(cls.model.septic),
                    selectinload(cls.model.services).selectinload(RequestService.service)
                )
            )
            request = result.scalar_one_or_none()

            return request.to_dict() if request else None
        

    @classmethod
    async def edit_request(cls, id: int, data: SRequestEdit):
        async with async_session_maker() as session:
            request = await session.execute(
                select(Request).where(Request.id == id)
            )
            request = request.scalar_one_or_none()
            
            if not request:
                raise HTTPException(status_code=404, detail="Заявка не найдена")

            for key, value in data:
                setattr(request, key, value)

            await session.commit()
            return {"message": "Заявка успешно обновлена"}