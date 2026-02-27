from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.config import settings


async def send_email(to_email: str, subject: str, html_content: str, plain_text: str):
    message = MIMEMultipart("alternative")
    message["From"] = settings.SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject

    plain_text_message = MIMEText(plain_text, "plain", "utf-8")
    html_message = MIMEText(
        html_content,
        "html",
        "utf-8"
    )
    message.attach(plain_text_message)
    message.attach(html_message)

    await aiosmtplib.send(message, hostname=settings.SMTP_HOST, port=settings.SMTP_PORT, password=settings.SMTP_PASS, username=settings.SMTP_USER,  start_tls=True)