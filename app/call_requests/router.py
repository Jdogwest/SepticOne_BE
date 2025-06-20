from fastapi import APIRouter, Depends
from app.call_requests.dao import CallRequestDAO
from app.call_requests.schemas import SCallRequest
from app.call_requests.rb import RBCallRequest
from app.users.dependencies import get_current_manager_user
from app.users.models import User
from app.call_requests.schemas import SCallRequestCreate, SCallRequestUpdate


router = APIRouter(prefix='/call-requests', tags=['Работа с запросами на звонок'])


@router.get("/", summary="Получить все запросы", response_model=list[SCallRequest])
async def get_all_requests(request_body: RBCallRequest = Depends()) -> list[SCallRequest]:
    return await CallRequestDAO.find_all(**request_body.to_dict())


@router.post("/add-call-request/")
async def add_call_request(request_data: SCallRequestCreate):
    return await CallRequestDAO.add_call_request(request_data.model_dump())


@router.post("/edit-call-request/{request_id}")
async def edit_call_request(request_id: int, request_data: SCallRequestUpdate, manager: User = Depends(get_current_manager_user)):
    return await CallRequestDAO.edit_call_request(request_id, request_data.model_dump())