"""Entry point for ."""


from dotenv import load_dotenv

from mobile_banking_notifications.lm_api import LunchMoneyAPI

load_dotenv(dotenv_path="./.env.local")

if __name__ == "__main__":
    lm_api = LunchMoneyAPI()
    print(lm_api.get_accounts())
