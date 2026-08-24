import os

from django.conf import settings


class WalletStorage:
    """Handles reading and writing the two wallet balances to a local file."""

    FILE_NAME = "total_money.txt"

    def __init__(self):
        self.file_path = os.path.join(settings.DATA_DIR, self.FILE_NAME)

    def read_balances(self):
        """Returns (online_balance, offline_balance). Creates the folder and
        file with zero balances on first run if they don't exist yet."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            self._write_raw(0.0, 0.0)

        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        online = float(lines[0]) if len(lines) > 0 else 0.0
        offline = float(lines[1]) if len(lines) > 1 else 0.0
        return online, offline

    def write_balances(self, online, offline):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self._write_raw(online, offline)

    def _write_raw(self, online, offline):
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(f"{online}\n{offline}\n")