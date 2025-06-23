from datetime import date
from fastapi import HTTPException
from sqlalchemy import delete, func, insert, select
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.requests.models import Request
from app.requests.schemas import SRequestCreate, SRequestEdit
from app.database import async_session_maker
from app.septics.models import Septic
from app.services.models import Service
from app.request_services.models import RequestService
from app.users.models import User
from app.workman_brigadiers.models import WorkmanBrigadier


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
            if request is None:
                return None

            brigadier = await session.execute(
                select(User).where(User.id == request.brigadier_id)
            )
            brigadier = brigadier.scalar_one_or_none()

            workmans = await session.execute(
                select(WorkmanBrigadier).where(WorkmanBrigadier.brigadier_id == request.brigadier_id)
            )
            workmans = [wb for wb in workmans]
            workmans_count = len(workmans)

            if brigadier is None:
                return None

            brigadier_dict = {
                "id": brigadier.id,
                "name": brigadier.name,
                "surname": brigadier.surname,
                "patronymic": brigadier.patronymic,
                "phone_number": brigadier.phone_number,
                "email": brigadier.email,
                "role": brigadier.role,
                "workmans_count": workmans_count,
            }

            response = {
                "id": request.id,
                "created_at": request.created_at,
                "client_id": request.client_id,
                "contract_number": request.contract_number,
                "status": request.status,
                "summary": request.summary,
                "septic_id": request.septic_id,
                "planed_start_date": request.planed_start_date,
                "planed_start_time": request.planed_start_time,
                "comment": request.comment,
                "work_comment": request.work_comment,
                "brigadier": brigadier_dict,
                "client": request.client,  # Assuming client is a related model
                "septic": request.septic,  # Assuming septic is a related model
                "services": [service.service for service in request.services]  # Assuming services is a relationship
            }
            return response if response else None

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
                if key == "services":
                    continue
                setattr(request, key, value)

            for service in data.services:
                await session.execute(
                    delete(RequestService).where(
                        RequestService.request_id == id and
                        RequestService.service_id == service.service_id
                    )
                )

            for service in data.services:
                await session.execute(
                    insert(RequestService).values(
                        request_id=id,
                        service_id=service.service_id,
                        amount=service.amount
                    )
                )

            await session.commit()
            return {"message": "Заявка успешно обновлена"}
        

    @classmethod
    async def find_busy_dates(cls):
        async with async_session_maker() as session:
            query = select(Request).where((Request.status == 'in_progress') | (Request.status == 'new'))
            requests = await session.execute(query)
            requests = requests.scalars().all()

            busy_dates = set()
            for request in requests:
                busy_dates.add((request.planed_start_date, request.brigadier_id))

            query = select(User).where(User.role == "brigadier")
            brigadiers = await session.execute(query)
            brigadiers = brigadiers.scalars().all()
            busy_dates_copy = busy_dates.copy()
            for busy_date in busy_dates_copy:
                available_brigadiers = [brigadier.id for brigadier in brigadiers if brigadier.id != busy_date[1]]
                if available_brigadiers:
                    busy_dates.remove(busy_date)

            result = [date[0] for date in busy_dates]
            return list(result)


    @classmethod
    async def find_brigades_on_date(cls, date: date):
        async with async_session_maker() as session:
            query = select(Request).where((Request.status == 'in_progress') | (Request.status == 'new'))
            requests = await session.execute(query)
            requests = requests.scalars().all()
            
            busy_brigadiers = set()
            for request in requests:
                if request.planed_start_date == date and request.brigadier_id is not None:
                    busy_brigadiers.add(request.brigadier_id)
            
            query = select(User).where((User.role == "brigadier") & (User.id.notin_(busy_brigadiers)))
            available_brigadiers = await session.execute(query)
            available_brigadiers = available_brigadiers.scalars().all()

            available_brigadiers = [brigadier for brigadier in available_brigadiers]

            for brigadier in available_brigadiers:
                query = select(func.count("*")).select_from(WorkmanBrigadier).where(WorkmanBrigadier.brigadier_id == brigadier.id)
                workmans_amount = await session.execute(query)

                setattr(brigadier, 'workmans_count', workmans_amount.scalar_one_or_none())
         
            available_brigadiers = [{
                "id": brigadier.id,
                "name": brigadier.name,
                "surname": brigadier.surname,
                "patronymic": brigadier.patronymic,
                "phone_number": brigadier.phone_number,
                "email": brigadier.email,
                "role": brigadier.role,
                "workmans_count": brigadier.workmans_count,
            } for brigadier in available_brigadiers]

                
            return available_brigadiers
