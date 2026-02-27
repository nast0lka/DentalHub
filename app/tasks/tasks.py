import asyncio

from app.tasks.celery import celery
from app.tasks.email_templates import send_email
from app.users.token import create_access_token
from app.users.dao import UserDAO


@celery.task
async def send_confirmation_email(user_id: int):
    user = await UserDAO.find_one_or_none(id=user_id)
    token = create_access_token({"sub": str(user.id)})
    confirmation_url = f"http://localhost:8000/auth/confirm?token={token}"
    plain_text = "Спасибо за регистрацию!"
    html_content = f"""
    <p>Перейдите по ссылке для завершения регистрации: <a href="{confirmation_url}">Подтвердить регистрацию</a></p>
    """
    asyncio.run(
        send_email(
            to_email=user.email,
            subject="Подтверждение регистрации",
            html_content=html_content,
            plain_text=plain_text
        )
    )