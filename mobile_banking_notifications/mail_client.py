import datetime
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from mobile_banking_notifications.config import Config


class MailClient:
    def __init__(self) -> None:
        self._context = ssl.create_default_context()
        self._conf = Config()

    def send_mail(self, data: str):
        with SMTP_SSL(
            host=self._conf.MAIL_HOST, port=self._conf.MAIL_PORT, context=self._context
        ) as server:
            server.login(self._conf.MAIL_USER, self._conf.MAIL_PASSWORD)

            message = MIMEMultipart("alternative")
            message["Subject"] = "Daily Finance Report"
            message["From"] = self._conf.MAIL_USER
            message["To"] = self._conf.MAIL_USER

            body = f"""
            <html>
                <body>
                    <h1>Daily Finance Report: {datetime.datetime.now().strftime("%a %b %d %Y")}</h1>

                    <hr />

                    {data}
                </body>
            </html>
            """

            message.attach(MIMEText(body, "html"))

            server.sendmail(
                self._conf.MAIL_USER, self._conf.MAIL_USER, message.as_string()
            )
