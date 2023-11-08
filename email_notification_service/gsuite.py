import os

import gspread
from gspread.auth import Path

from email_notification_service.config import Config


class GSuiteAPI:
    def __init__(self) -> None:
        self._cred_file_path = f"{os.getcwd()}/gsuite_creds.json"
        self._conf = Config()
        self.gc = gspread.service_account(
            filename=Path(self._cred_file_path), scopes=self._conf.GSUITE_SCOPES
        )

    def get_worksheet(self, worksheet: int):
        sh = self.gc.open_by_key(self._conf.CLIMBING_SHEET_ID)
        return sh.get_worksheet(worksheet)

    def read_row(self, row: int, worksheet: int = 0):
        ws = self.get_worksheet(worksheet)
        return ws.row_values(row)

    def read_cell(self, row: int, col: int, worksheet: int = 0):
        ws = self.get_worksheet(worksheet)
        return ws.cell(row, col).value
