from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

from app.users.auth import admin_required
from app.users.models import User

templates = Jinja2Templates(directory="app/templates")

from starlette.status import HTTP_303_SEE_OTHER

from app.doctors.dao import DoctorDAO
from app.doctors.schemas import DoctorForm

router_admin = APIRouter(
    prefix="/admin",
    tags=["admin_func"],
)

@router_admin.post("/add_doctor")
async def add_doctor(doctor_data: DoctorForm = Depends(DoctorForm.as_form), admin: User = Depends(admin_required),):
    upload_dir = Path("app") / "static" / "doc_photo"
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = doctor_data.photo.filename
    file_path = upload_dir / filename

    content = await doctor_data.photo.read()
    file_path.write_bytes(content)
    web_path = f"/static/doc_photo/{filename}"

    await DoctorDAO.doctor_add({
            "name": doctor_data.name,
            "lastname": doctor_data.lastname,
            "experience": doctor_data.experience,
            "specialization_id": doctor_data.specialization_id,
            "education": doctor_data.education,
            "photo": web_path,
            "dentistry_id": doctor_data.dentistry_id
        })

    return RedirectResponse(url="/admin", status_code=303)

@router_admin.get("/form_doctor", response_class=HTMLResponse)
async def show_add_doctor_form(request: Request, admin: User = Depends(admin_required)):
    return templates.TemplateResponse("upload_doctor.html", {"request": request})