import typer

from email_notification_service.handlers import Handlers

app = typer.Typer()
spending_app = typer.Typer()
app.add_typer(spending_app, name="spending", help="Finance reports")

handlers = Handlers()


@spending_app.command("daily", help="Generate a report of today's balances")
def spending_daily():
    handlers.spending_daily()


@spending_app.command("weekly", help="Generate a report of the week's expenses")
def spending_weekly():
    handlers.spending_weekly()


@app.command("climbing", help="Get today's climbing workout")
def climbing():
    handlers.climbing()
