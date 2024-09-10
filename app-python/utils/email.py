
from email.message import EmailMessage
from smtplib import SMTP_PORT
import aiosmtplib
from utils.config import FROM_EMAIL, SMTP_HOST, SMTP_PASSWORD, SMTP_USER

async def send_email(to_email: str, subject: str, body: str):
    # Crear el mensaje de correo
    message = EmailMessage()
    message["From"] = FROM_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    # Enviar el correo usando el cliente SMTP asíncrono
    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
        )
        print(f"Correo enviado a {to_email}")
    except Exception as e:
        print(f"Error al enviar correo: {e}")