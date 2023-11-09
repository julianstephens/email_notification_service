import os
from datetime import datetime

import email_notification_service.services as services
from email_notification_service import utils


class Handlers:
    def __init__(self):
        self._lm_api = services.LunchMoneyAPI()
        self._gs_api = services.GSuiteAPI()
        self._mc = services.MailClient()
        self._manager = services.TemplateManager()
        self._conf = utils.Config()
        self._conf.set_env("QUIET_MODE", os.environ.get("QUIET_MODE") or "False")
        self.quiet_mode = bool(self._conf.get_env("QUIET_MODE"))

    def spending_daily(self):
        self._mc.send_bank_report(self._lm_api.get_accounts())

    def spending_weekly(self):
        self._mc.send_bank_report(self._lm_api.get_transactions(), True)

    def climbing(self):
        utils.logger.info("Reading data from Sheets...")
        utils.logger.info(f"day: {datetime.now().isoweekday()}")
        data = self._gs_api.read_cell(7, datetime.now().isoweekday())
        if not data:
            utils.logger.info("No data or rest day. Complete.")
            return

        utils.logger.info("Building table for email...")
        split = [line.split("(") for line in data.split("\n")]
        data = [
            "<tr><td>{activity}</td><td>{time}</td></tr>\n".format(
                activity=s[0].strip(), time=s[1][:-1]
            )
            for s in split
        ]
        utils.logger.info("Parsing html...")
        print("not in quiet mode", self.quiet_mode)
        html = self._manager.render_template("climbing.html", data="".join(data))
        if not self.quiet_mode:
            self._mc.send_climbing_routine(html)
