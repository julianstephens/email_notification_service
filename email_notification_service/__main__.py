import sys

from email_notification_service.lm_api import LunchMoneyAPI
from email_notification_service.mail_client import MailClient

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    transaction_mode = True if arg == "-t" else False
    lm_api = LunchMoneyAPI()
    mc = MailClient()
    mc.send_mail(
        lm_api.get_transactions() if transaction_mode else lm_api.get_accounts(),
        transaction_mode=transaction_mode,
    )
