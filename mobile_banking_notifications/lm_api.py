from lunchable import LunchMoney

from mobile_banking_notifications.config import Config


class LunchMoneyAPI:
    def __init__(self) -> None:
        self._conf = Config()
        self._lunchable = LunchMoney(access_token=self._conf.LM_ACCESS_TOKEN)

    def get_accounts(self) -> str:
        accounts = self._lunchable.get_plaid_accounts()

        res = ""
        for a in accounts:
            acct = a.dict()
            res += (
                "<h2><b>{name}:</b> {balance} <em>({updated})</em></h2><br />".format(
                    name=acct["name"],
                    balance=acct["balance"],
                    updated=acct["balance_last_update"].strftime("%c"),
                )
            )

        return res
