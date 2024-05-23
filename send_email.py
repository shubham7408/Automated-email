import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv

PORT = 587
EMAIL_SERVER = "smtp.gmail.com"

current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

sender_email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def send_email(subject, receiver_email, name, due_date, invoice_no, amount):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Coding is Fun Testing", sender_email))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        <html>
        <body>
        <h1>Invoice {invoice_no}</h1>
        <p>Dear {name},</p>
        <p>I hope you are well.</p>
        <p>This is a reminder that your invoice <strong>{invoice_no}</strong> is due on {due_date}.</p>
        <p>The amount due is <strong>${amount}</strong>.</p>
        <p>Thank you for your prompt payment.</p>
        </body>
        </html>
        """,
        subtype="html",
    )
    
    try:
        with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to authenticate with the SMTP server: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    
if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        name="Aditya Pawar",
        receiver_email="adityapawar9767@gmail.com",
        due_date="2024-05-24",
        invoice_no="002",
        amount="1000"
    )
