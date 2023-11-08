import typer

from email_notification_service.lm_api import LunchMoneyAPI
from email_notification_service.mail_client import MailClient

app = typer.Typer()
spending_app = typer.Typer()
app.add_typer(spending_app, name="spending", help="Finance reports")

lm_api = LunchMoneyAPI()
mc = MailClient()


@spending_app.command("daily", help="Generate a report of today's balances")
def spending_daily():
    mc.send_bank_report(lm_api.get_accounts())


@spending_app.command("weekly", help="Generate a report of the week's expenses")
def spending_weekly():
    mc.send_bank_report(lm_api.get_transactions(), True)


@app.command("climbing", help="Get today's climbing workout")
def climbing():
    pass
