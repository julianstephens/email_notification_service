"""LunchMoney Handlers"""
import os

from lunchable import LunchMoney

token = os.environ.get("LM_ACCESS_TOKEN")
if not token:
    raise ValueError("Env var 'LM_ACCESS_TOKEN' not set")

lunch = LunchMoney(access_token=token)


def getAccounts():  # pragma: no cover
    accounts = lunch.get_plaid_accounts()

    for a in accounts:
        print(a)
