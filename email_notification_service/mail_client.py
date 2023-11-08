import os
import ssl
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from email_notification_service.config import Config
from email_notification_service.gsuite import GSuiteAPI
from email_notification_service.templates import spending
from email_notification_service.templates.base import BASE_EMAIL


class MailClient:
    def __init__(self) -> None:
        self._context = ssl.create_default_context()
        self._conf = Config()
        self._gs = GSuiteAPI()

    def _send_email(self, subject: str, body: str):
        with SMTP_SSL(
            host=self._conf.MAIL_HOST, port=self._conf.MAIL_PORT, context=self._context
        ) as server:
            server.login(self._conf.MAIL_USER, self._conf.MAIL_PASSWORD)

            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self._conf.MAIL_USER
            message["To"] = self._conf.MAIL_USER

            f = open(f"{os.getcwd()}/email_notification_service/styles/modest.css")
            styles = f.read()

            message.attach(
                MIMEText(BASE_EMAIL.format(styles=styles, body=body), "html")
            )

            server.sendmail(
                self._conf.MAIL_USER, self._conf.MAIL_USER, message.as_string()
            )

    def send_bank_report(self, data: str, transaction_mode=False):
        today = date.today()
        format = "%a %b %d %Y"

        body = (
            spending.WEEKLY_EMAIL.format(
                dateRange=f"{(today - timedelta(7)).strftime(format)} through {today.strftime(format)}",
                data=spending.TRANSACTION_TABLE.format(data=data),
            )
            if transaction_mode
            else spending.DAILY_EMAIL.format(
                date=today.strftime(format),
                data=data,
            )
        )

        self._send_email(
            f"{'Weekly' if transaction_mode else 'Daily'} Finance Report", body
        )

    def send_climbing_routine(self, data: str):
        self._send_email("Today's Workout", data)
