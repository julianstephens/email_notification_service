from datetime import date, timedelta

from lunchable import LunchMoney

from email_notification_service.utils.config import Config

from .template_manager import TemplateManager


class LunchMoneyAPI:
    def __init__(self) -> None:
        self._conf = Config()
        self._lunchable = LunchMoney(access_token=self._conf.LM_ACCESS_TOKEN)
        self._manager = TemplateManager()

    def get_accounts(self) -> str:
        """Retrieves balance information for all Plaid accounts"""
        accounts = self._lunchable.get_plaid_accounts()

        res = ""
        for a in accounts:
            acct = a.dict()
            res += self._manager.render_template(
                "account.html",
                name=acct["name"],
                balance=acct["balance"],
                updated=acct["balance_last_update"].strftime("%c"),
            )

        return res

    def get_transactions(self, period: int = 7) -> str:
        """Retrieves all transactions over from today - {period} through today

        Args:
            period (int): date range to filter over
        """
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
