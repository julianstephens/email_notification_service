import os
import ssl
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from mobile_banking_notifications.config import Config
from mobile_banking_notifications.templates import (
    DAILY_EMAIL_TEMPLATE,
    TRANSACTION_TABLE_TEMPLATE,
    WEEKLY_EMAIL_TEMPLATE,
)


class MailClient:
    def __init__(self) -> None:
        self._context = ssl.create_default_context()
        self._conf = Config()

    def send_mail(self, data: str, transaction_mode=False):
        with SMTP_SSL(
            host=self._conf.MAIL_HOST, port=self._conf.MAIL_PORT, context=self._context
        ) as server:
            server.login(self._conf.MAIL_USER, self._conf.MAIL_PASSWORD)

            message = MIMEMultipart("alternative")
            message[
                "Subject"
            ] = f"{'Weekly' if transaction_mode else 'Daily'} Finance Report"
            message["From"] = self._conf.MAIL_USER
            message["To"] = self._conf.MAIL_USER

            f = open(f"{os.getcwd()}/mobile_banking_notifications/styles/modest.css")
            styles = f.read()

            today = date.today()
            format = "%a %b %d %Y"

            body = (
                WEEKLY_EMAIL_TEMPLATE.format(
                    styles=styles,
                    dateRange=f"{(today - timedelta(7)).strftime(format)} through {(today + timedelta(7)).strftime(format)}",
                    data=TRANSACTION_TABLE_TEMPLATE.format(data=data),
                )
                if transaction_mode
                else DAILY_EMAIL_TEMPLATE.format(
                    styles=styles,
                    date=today.strftime(format),
                    data=data,
                )
            )
            message.attach(MIMEText(body, "html"))

            server.sendmail(
                self._conf.MAIL_USER, self._conf.MAIL_USER, message.as_string()
            )
