from datetime import datetime

from email_notification_service.gsuite import GSuiteAPI
from email_notification_service.lm_api import LunchMoneyAPI
from email_notification_service.mail_client import MailClient
from email_notification_service.templates.climbing import CLIMBING_EMAIL


class Handlers:
    def __init__(self):
        self._lm_api = LunchMoneyAPI()
        self._gs_api = GSuiteAPI()
        self._mc = MailClient()

    def spending_daily(self):
        self._mc.send_bank_report(self._lm_api.get_accounts())

    def spending_weekly(self):
        self._mc.send_bank_report(self._lm_api.get_transactions(), True)

    def climbing(self):
        lines = self._gs_api.read_cell(7, datetime.now().weekday()).split("\n")
        split = [line.split("(") for line in lines]
        data = [
            "<tr><td>{activity}</td><td>{time}</td></tr>\n".format(
                activity=s[0].strip(), time=s[1][:-1]
            )
            for s in split
        ]
        self._mc.send_climbing_routine(CLIMBING_EMAIL.format(data="".join(data)))
