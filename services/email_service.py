import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

def send_contract_email(to_email, subject, body, pdf_path):
    email_login = os.getenv("SOFT_TRAVELS_EMAIL")
    email_password = os.getenv("SOFT_TRAVELS_EMAIL_PASSWORD")

    if not email_login or not email_password:
        raise Exception("Не задані SOFT_TRAVELS_EMAIL або SOFT_TRAVELS_EMAIL_PASSWORD")

    message = EmailMessage()
    message["From"] = email_login
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    with open(pdf_path, "rb") as file:
        message.add_attachment(
            file.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(pdf_path)
        )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(email_login, email_password)
        smtp.send_message(message)
