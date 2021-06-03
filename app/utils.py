from datetime import datetime
from pathlib import Path
from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr

from app.core.config import settings


async def send_email(subject: str, email_to: List[EmailStr], email_template: str):
    try:
        assert settings.EMAILS_ENABLED, "No provided configuration for email variables"
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_FROM_NAME=settings.EMAILS_FROM_NAME,
            MAIL_TLS=settings.MAIL_TLS,
            MAIL_SSL=settings.MAIL_SSL,
            USE_CREDENTIALS=True,
        )

        message = MessageSchema(
            subject=subject, recipients=email_to, body=email_template, subtype="html"
        )
        fm = FastMail(conf)
        return await fm.send_message(message)
    except Exception as e:
        raise e


async def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    email_template = template_str.format(
        project_name=settings.PROJECT_NAME,
        username=email,
        email=email_to,
        valid_hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
        link=link,
    )
    await send_email(
        subject=subject, email_to=[email_to], email_template=email_template
    )


def convert_datetime_to_realworld(dt: datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )
