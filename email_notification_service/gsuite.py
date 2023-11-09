import os

from gspread.auth import READONLY_SCOPES, Path, service_account

from email_notification_service.config import Config


class GSuiteAPI:
    def __init__(self) -> None:
        self._conf = Config()
        self._path = os.path.join(os.getcwd(), "creds.json")

        if not os.path.isfile(self._path):
            raise AttributeError("Error: gsuite credentials file does not exist")

        self._gc = service_account(
            filename=Path(self._path),
            scopes=READONLY_SCOPES,
        )

    def get_worksheet(self, worksheet: int):
        sh = self._gc.open_by_key(self._conf.CLIMBING_SHEET_ID)
        return sh.get_worksheet(worksheet)

    def read_row(self, row: int, worksheet: int = 0):
        ws = self.get_worksheet(worksheet)
        return ws.row_values(row)

    def read_cell(self, row: int, col: int, worksheet: int = 0):
        ws = self.get_worksheet(worksheet)
        return ws.cell(row, col).value
