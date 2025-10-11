import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os

FROM_EMAIL = os.getenv("FROM_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(subject, body, to_email):
    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(FROM_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            logging.info(f"Email sent to {to_email}")
    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication failed — check Gmail App Password")
    except smtplib.SMTPRecipientsRefused:
        logging.error("Recipient address was rejected by Gmail")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
