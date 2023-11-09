import os
import ssl
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from email_notification_service import utils
from email_notification_service.services.gsuite import GSuiteAPI
from email_notification_service.services.template_manager import TemplateManager
from email_notification_service.utils.config import Config


class MailClient:
    def __init__(self) -> None:
        self._context = ssl.create_default_context()
        self._conf = Config()
        self._gs = GSuiteAPI()
        self._manager = TemplateManager()

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

            html = self._manager.render_template("base.html", styles=styles, body=body)

            message.attach(MIMEText(html, "html"))

            utils.logger.info("Email sent. Complete!")
            server.sendmail(
                self._conf.MAIL_USER, self._conf.MAIL_USER, message.as_string()
            )

    def send_bank_report(self, data: str, transaction_mode=False):
        today = date.today()
        format = "%a %b %d %Y"

        body = (
            self._manager.render_template(
                "weekly_spending.html",
                dateRange=f"{(today - timedelta(7)).strftime(format)} through {today.strftime(format)}",
                data=self._manager.render_template("transaction_table.html", data=data),
            )
            if transaction_mode
            else self._manager.render_template(
                "daily_spending.html",
                date=today.strftime(format),
                data=data,
            )
        )

        self._send_email(
            f"{'Weekly' if transaction_mode else 'Daily'} Finance Report", body
        )

    def send_climbing_routine(self, data: str):
        print("email", data)
        self._send_email("Today's Workout", data)
