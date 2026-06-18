import os
import smtplib
from email.message import EmailMessage


def enviar_email_alerta(asunto, mensaje, destinatarios=None):
    remitente = os.getenv("EMAIL_REMITENTE")
    password = os.getenv("EMAIL_PASSWORD")

    if destinatarios is None:
        destino = os.getenv("EMAIL_DESTINO")
        destinatarios = [correo.strip() for correo in destino.split(",")] if destino else []

    if not remitente or not password or not destinatarios:
        print("No se enviará email: faltan datos de configuración.")
        return False

    email = EmailMessage()
    email["From"] = remitente
    email["To"] = ", ".join(destinatarios)
    email["Subject"] = asunto
    email.set_content(mensaje)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, password)
            smtp.send_message(email, to_addrs=destinatarios)

        print("Email enviado correctamente.")
        return True

    except Exception as e:
        print(f"No se pudo enviar el email: {e}")
        return False