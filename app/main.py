from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware


from app.config import settings
from app.users.router import router as router_users
from app.users.router_auth import router as router_auth
from app.septics.router import router as router_septics
from app.services.router import router as router_services
from app.requests.router import router as router_requests
from app.workman_brigadiers.router import router as router_workman_brigadiers
from app.request_services.router import router as router_request_services
from app.call_requests.router import router as router_call_requests
import logging
from dotenv import load_dotenv



load_dotenv()
logging.basicConfig(level=logging.INFO)
print(">>> FastAPI App is loading <<<")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

app.include_router(router_users)
app.include_router(router_auth)
app.include_router(router_septics)
app.include_router(router_services)
app.include_router(router_requests)
app.include_router(router_workman_brigadiers)
app.include_router(router_request_services)
app.include_router(router_call_requests)



