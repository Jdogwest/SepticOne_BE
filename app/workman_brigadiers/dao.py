from datetime import date
from app.requests.models import Request
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.workman_brigadiers.models import WorkmanBrigadier
from app.workman_brigadiers.schemas import SWorkmanBrigadierEdit
from app.users.models import User
from collections import defaultdict


class WorkmanBrigadierDAO(BaseDAO):
    model = WorkmanBrigadier

    @classmethod
    async def edit_links(cls, brigades: SWorkmanBrigadierEdit):
        async with async_session_maker() as session:
            for brigad in brigades.brigads:
                all_workman_ids = brigad.workman_ids

                await session.execute(
                    delete(WorkmanBrigadier).where(
                        WorkmanBrigadier.workman_id.in_(all_workman_ids)
                    )
                )

                await session.execute(
                    delete(WorkmanBrigadier).where(WorkmanBrigadier.brigadier_id == brigad.brigadier_id)
                )
                
                # Добавляем новые связи для бригадира и его рабочих
                for workman_id in brigad.workman_ids:
                    new_link = WorkmanBrigadier(brigadier_id=brigad.brigadier_id, workman_id=workman_id)
                    session.add(new_link)

            await session.commit()

            response = await WorkmanBrigadierDAO.find_brigades()
            

            return response




    @classmethod
    async def find_brigades(cls):
        async with async_session_maker() as session:
            result = await session.execute(
                select(WorkmanBrigadier).options(
                    selectinload(WorkmanBrigadier.brigadier),
                    selectinload(WorkmanBrigadier.workman)
                )
            )

            brigades = result.scalars().all()
           

            brigade_map = defaultdict(list)

            result_brigadiers = await session.execute(
                select(User).where(User.role == 'brigadier')
            )


            for wb in brigades:
                brigade_data = {
                    "brigadier_id": wb.brigadier.id,
                    "brigadier_name": wb.brigadier.name,
                    "brigadier_surname": wb.brigadier.surname,
                    "brigadier_patronymic": wb.brigadier.patronymic,
                    "workers": []
                }

                worker_data = {
                    "workman_id": wb.workman.id,
                    "workman_name": wb.workman.name,
                    "workman_surname": wb.workman.surname,
                    "workman_patronymic": wb.workman.patronymic
                }

                brigade_data["workers"].append(worker_data)
                brigade_map[wb.brigadier.id].append(brigade_data)

            
            final_result = []

            for brigadier_id, workers_list in brigade_map.items():
                merged = workers_list[0]
                all_workers = [w["workers"][0] for w in workers_list]
                merged["workers"] = all_workers
                final_result.append(merged)

            # Добавляем бригадиров без рабочих
            for brigadier in result_brigadiers.scalars():
                if brigadier.id not in brigade_map:
                    final_result.append({
                        "brigadier_id": brigadier.id,
                        "brigadier_name": brigadier.name,
                        "brigadier_surname": brigadier.surname,
                        "brigadier_patronymic": brigadier.patronymic,
                        "workers": []
                    })

            return final_result
        
    @classmethod
    async def get_all_free_workers(cls):
        async with async_session_maker() as session:
            result_all = await session.execute(select(User).where(User.role == "workman"))
            all_workmen = result_all.scalars().all()

            result_busy = await session.execute(select(WorkmanBrigadier.workman_id))
            busy_ids = set(result_busy.scalars().all())

            free_workmen = [w for w in all_workmen if w.id not in busy_ids]

            for w in free_workmen:
                w.__dict__.pop("password", None)

            return free_workmen

        
        
    @classmethod
    async def find_busy_brigades_by_dates(cls):
        async with async_session_maker() as session:
            query = select(Request).where(Request.status.in_(['new', 'in_progress']))
            requests_result = await session.execute(query)
            requests = requests_result.scalars().all()

            busy_by_date: dict[date, list[dict]] = {}

            for req in requests:
                if req.brigadier_id:
                    user_query = select(User).where(User.id == req.brigadier_id)
                    brigadier_result = await session.execute(user_query)
                    brigadier = brigadier_result.scalar_one_or_none()
                    if brigadier:
                        busy_by_date.setdefault(req.planed_start_date, []).append({
                            "request_id": req.id, 
                            "id": brigadier.id,
                            "name": brigadier.name,
                            "surname": brigadier.surname,
                            "patronymic": brigadier.patronymic,
                            "email": brigadier.email,
                            "phone_number": brigadier.phone_number,
                        })

            result = [
                {
                    "date": day.isoformat(),
                    "busy_brigadiers": brigadiers
                }
                for day, brigadiers in sorted(busy_by_date.items())
            ]

            return result