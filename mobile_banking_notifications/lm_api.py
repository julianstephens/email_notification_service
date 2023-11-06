import os

from lunchable import LunchMoney


class LunchMoneyAPI:
    def __init__(self) -> None:
        self._token = os.environ.get("LM_ACCESS_TOKEN")
        if not self._token:
            raise ValueError("Env var 'LM_ACCESS_TOKEN' not set")
        self._lunchable = LunchMoney(access_token=self._token)

    def get_accounts(self):
        return self._lunchable.get_plaid_accounts()
