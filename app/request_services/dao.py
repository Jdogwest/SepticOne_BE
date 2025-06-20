from app.dao.base import BaseDAO
from app.request_services.models import RequestService
from app.database import async_session_maker
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


class RequestServiceDAO(BaseDAO):
    model = RequestService