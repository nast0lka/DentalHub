from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.appointments.router import get_user_appointments
from app.dentistry.router import get_dentistry
from app.doctors.router import get_doctors
from app.services.router import get_services
from app.specializations.router import get_specializations
from app.users.auth import get_current_user

templates = Jinja2Templates(directory="app/templates")

router_main = APIRouter(
    prefix="",
    tags=["pages"],
)

@router_main.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        }
    )

@router_main.get("/doctors")
async def doctors(request: Request, doctors=Depends(get_doctors), specializations=Depends(get_specializations)):
    return templates.TemplateResponse(
        "doctors.html",
        {
            "request": request,
            "doctors": doctors,
            "specializations": specializations
        }
    )

@router_main.get("/about")
async def about(request: Request, clinics=Depends(get_dentistry)):
    return templates.TemplateResponse(
        "about.html",
        {
            "request": request,
            "clinics": clinics
        }
    )

@router_main.get("/services")
async def services(request: Request, services=Depends(get_services)):
    return templates.TemplateResponse(
        "services.html",
        {
            "request": request,
            "services": services
        }
    )

@router_main.get("/price")
async def price(request: Request, services=Depends(get_services)):
    return templates.TemplateResponse(
        "price.html",
        {
            "request": request,
            "services": services
        }
    )

@router_main.get("/register")
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router_main.get("/login")
async def get_login_page(request: Request):
    registration_sent = request.cookies.get("registration_sent")
    resp = templates.TemplateResponse("auth/login.html", {"request": request, "registration_sent": registration_sent})
    if registration_sent:
        resp.delete_cookie("registration_sent")
    return resp

@router_main.get("/profile")
async def get_profile_page(
    request: Request,
    user=Depends(get_current_user),
    appointments=Depends(get_user_appointments),
):
    return templates.TemplateResponse(
        "me.html",
        {
            "request": request,
            "user": user,
            "appointments": appointments,
        },
    )

@router_main.get("/appointment")
async def get_appointment_page(request: Request, services=Depends(get_services), doctors=Depends(get_doctors)):
    user = await get_current_user(request)
    if not user:
        return templates.TemplateResponse("auth/login.html", {"request": request})
    return templates.TemplateResponse("appointment.html", {"request": request, "user": user, "doctors": doctors, "services": services})


