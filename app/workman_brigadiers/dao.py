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
                all_workman_ids = [worker_id for b in brigades.brigads for worker_id in b.workman_ids]

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

            return await WorkmanBrigadierDAO.find_brigades()




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
            workmans_resualt = await session.execute(select(User).where(User.role == "workman"))
            workamans = workmans_resualt.scalars().all()
            
            workmans_in_brigades = await session.execute(select(WorkmanBrigadier.workman_id))

            free_workmans = [worker for worker in workamans if worker.id not in workmans_in_brigades.scalars().all()]
            for worker in free_workmans:
                worker.__dict__.pop("password", None)
            return free_workmans

