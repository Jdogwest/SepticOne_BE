from app.dao.base import BaseDAO
from app.services.models import Service


class ServiceDAO(BaseDAO):
    model = Service