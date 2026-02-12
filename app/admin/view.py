from sqladmin import ModelView
from app.appointments.models import Appointment
from app.doctors.models import Doctor
from app.services.models import Service
from app.users.models import User
from markupsafe import Markup
from fastapi import Request


class UserAdmin(ModelView, model=User):
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True

    column_details_exclude_list = [User.password_hash]
    form_excluded_columns = [User.password_hash]

    name = "Пользователи"
    name_plural = "Пользователи"

    column_list = [
        User.id,
        User.name,
        User.lastname,
        User.age,
        User.email,
    ]


class AppointmentAdmin(ModelView, model=Appointment):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    name = "Записи"
    name_plural = "Записи"

    column_list = (
        [c for c in Appointment.__table__.c]
        + [Appointment.user, Appointment.doctor, Appointment.service]
    )


class DoctorAdmin(ModelView, model=Doctor):
    details_template = "custom_details.html"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    column_list = (
        [c for c in Doctor.__table__.c]
        + [Doctor.dentistry, Doctor.specialization]
    )

    column_details_exclude_list = [Doctor.photo]

    name = "Врачи"
    name_plural = "Врачи"

class ServiceAdmin(ModelView, model=Service):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    name = "Услуги"
    name_plural = "Услуги"

    column_list = (
        [c for c in Service.__table__.c]
        + [Service.specialization]
    )
