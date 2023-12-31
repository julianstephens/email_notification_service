import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    LM_ACCESS_TOKEN: str = os.environ.get("LM_ACCESS_TOKEN") or ""

    MAIL_USER: str = os.environ.get("MAIL_USER") or ""

    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD") or ""

    MAIL_HOST: str = os.environ.get("MAIL_HOST") or ""

    MAIL_PORT: int = int(os.environ.get("MAIL_PORT") or "-1")

    GSUITE_SCOPES: list[str] = [os.environ.get("GSUITE_SCOPE") or ""]

    CLIMBING_SHEET_ID: str = os.environ.get("CLIMBING_SHEET_ID") or ""

    TEMPLATE_DIR: str = os.path.join(
        os.getcwd(), f"{__name__.split('.')[0]}/templates/"
    )

    def __init__(self):
        var_arr = vars(self.__class__)
        members = [
            attr
            for attr in var_arr
            if not callable(getattr(self.__class__, attr)) and not attr.startswith("__")
        ]

        for m in members:
            if not var_arr[m] or var_arr[m] == -1:
                if m != "QUIET_MODE":
                    raise AttributeError(f"Env var '{m}' is not set")

    def get_env(self, key: str):
        os.environ.get(key)

    def set_env(self, key: str, value: str):
        os.environ.setdefault(key, value)

    @staticmethod
    def toggle_quiet_mode():
        os.environ.setdefault("QUIET_MODE", "True")
