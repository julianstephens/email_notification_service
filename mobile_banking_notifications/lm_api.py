from datetime import date, timedelta

from lunchable import LunchMoney

from mobile_banking_notifications.config import Config
from mobile_banking_notifications.templates import ACCOUNT_TEMPLATE


class LunchMoneyAPI:
    def __init__(self) -> None:
        self._conf = Config()
        self._lunchable = LunchMoney(access_token=self._conf.LM_ACCESS_TOKEN)

    def get_accounts(self) -> str:
        accounts = self._lunchable.get_plaid_accounts()

        res = ""
        for a in accounts:
            acct = a.dict()
            res += ACCOUNT_TEMPLATE.format(
                name=acct["name"],
                balance=acct["balance"],
                updated=acct["balance_last_update"].strftime("%c"),
            )

        return res

    def get_transactions(self, period=7) -> str:
        transactions = self._lunchable.get_transactions(
            start_date=date.today() - timedelta(period),
            end_date=date.today(),
        )

        res = ""
        total = 0
        for t in transactions:
            cat = None
            if t.category_id:
                cat = self._lunchable.get_category(t.category_id)

            if t.amount > 0:
                total += t.amount
                res += f"""
                    <tr>
                        <td {"style='background-color:#e58ba6;'" if cat and cat.name == "Food and drink" else None}>{t.payee}</td>
                            <td style="text-align: right;">${'{:.2f}'.format(t.amount)}</td>
                    </tr>
                """

        if total > 0:
            res += f"""
                <tr style="font-weight: bold;">
                    <td>Total Spent</td>
                    <td>${'{:.2f}'.format(total)}</td>
                </tr>
            """

        return res
