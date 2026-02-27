from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.view import (AppointmentAdmin, 
                            DoctorAdmin, 
                            ServiceAdmin,
                            UserAdmin)
from app.admin_func.router import router_admin
from app.appointments.models import Appointment
from app.appointments.router import router_appointment
from app.config import settings
from app.database import engine
from app.dentistry.models import Dentistry
from app.doctors.models import Doctor
from app.doctors.router import router_doctor
from app.pages.router import router_main
from app.services.models import Service
from app.specializations.models import Specialization
from app.users.auth import AddUserToContextMiddleware
from app.users.models import User
from app.users.router import router_auth


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


