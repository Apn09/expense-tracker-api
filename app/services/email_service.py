import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_password_reset_email(email: str, reset_link: str):
    message = EmailMessage()

    message["Subject"] = "Reset your password"
    message["From"] = settings.SMTP_FROM
    message["To"] = email

    email_body = f"""
Hello,

We received a request to reset your password.

Please click the link below to reset your password:

{reset_link}

This link will expire in
{settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES} minutes.

If you did not request this password reset,
you can ignore this email.

Thanks,
Expense Tracker Team
"""

    message.set_content(email_body)

    with smtplib.SMTP(
        settings.SMTP_HOST,
        settings.SMTP_PORT
    ) as server:

        server.starttls()

        server.login(
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD
        )

        server.send_message(message)
