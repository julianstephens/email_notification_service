from mobile_banking_notifications.lm_api import LunchMoneyAPI
from mobile_banking_notifications.mail_client import MailClient

if __name__ == "__main__":
    lm_api = LunchMoneyAPI()
    mc = MailClient()
    mc.send_mail(lm_api.get_accounts())
