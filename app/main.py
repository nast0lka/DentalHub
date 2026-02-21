from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from app.users.auth import get_current_user
from app.users.auth import AddUserToContextMiddleware
from fastapi.responses import HTMLResponse
from app.database import engine
from app.config import settings

from app.admin.auth import authentication_backend
from app.admin.view import AppointmentAdmin, DoctorAdmin, ServiceAdmin, UserAdmin

from app.doctors.models import Doctor
from app.appointments.models import Appointment
from app.users.models import User
from app.services.models import Service
from app.dentistry.models import Dentistry
from app.specializations.models import Specialization

from app.pages.router import router_main
from app.users.router import router_auth
from app.doctors.router import router_doctor
from app.appointments.router import router_appointment
from app.admin_func.router import router_admin

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from redis.asyncio import Redis

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(
    title="Стоматология", version="1.0.0", lifespan=lifespan
)

app.include_router(router_main)
app.include_router(router_auth)
app.include_router(router_doctor)
app.include_router(router_appointment)
app.include_router(router_admin)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)

app.add_middleware(AddUserToContextMiddleware)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
)

admin.add_view(UserAdmin)
admin.add_view(AppointmentAdmin)
admin.add_view(DoctorAdmin)
admin.add_view(ServiceAdmin)