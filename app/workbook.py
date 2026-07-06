from pathlib import Path
from datetime import datetime
import shutil

from openpyxl import load_workbook

from app.models.training_session import TrainingSession


class WorkbookManager:

    def __init__(self):

        self.workbook = None
        self.worksheet = None
        self.filename = None

    def open(self, filename):

        self.filename = filename

        self.workbook = load_workbook(filename)

        self.worksheet = self.workbook.active

    def get_headers(self):

        headers = []

        for cell in self.worksheet[1]:
            headers.append(cell.value)

        return headers

    def get_sessions(self):

        sessions = []

        for row in self.worksheet.iter_rows(min_row=2):

            values = []

            for cell in row:
                values.append(cell.value)

            sessions.append(
                TrainingSession(
                    row_number=row[0].row,
                    values=values
                )
            )

        return sessions

    def save(self):

        self.backup()

        self.workbook.save(self.filename)

    def backup(self):

        backup = Path("backups")

        backup.mkdir(exist_ok=True)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        shutil.copy(
            self.filename,
            backup / f"{stamp}_{Path(self.filename).name}"
        )