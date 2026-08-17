"""Coordinate practice PDF export and Windows printing for the desktop UI."""

from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox
from typing import Callable

from app.services.practice_pdf_service import export_practice_pdf, print_practice


class PracticeOutputController:
    """Keep output dialogs and error handling out of the main application."""

    def __init__(
        self,
        config_data: Callable[[], dict],
        configured_coaches: Callable[[], list[str]],
        set_status: Callable[[str], None],
    ) -> None:
        self._config_data = config_data
        self._configured_coaches = configured_coaches
        self._set_status = set_status

    def _prepare(self, practice) -> None:
        config = self._config_data()
        practice.head_coach = config.get("head_coach", "")
        practice.sport = config.get("sport", "")[:15]
        practice.retain_configured_coaches(self._configured_coaches())

    @staticmethod
    def safe_filename(name: str) -> str:
        cleaned = "".join(
            character if character.isalnum() or character in " -_" else "_"
            for character in (name or "practice_plan")
        ).strip()
        return cleaned or "practice_plan"

    def export_pdf(self, practice) -> None:
        filename = filedialog.asksaveasfilename(
            title="Export Practice PDF",
            initialfile=f"{self.safe_filename(practice.name)}.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
        )
        if not filename:
            self._set_status("PDF export canceled")
            return
        try:
            self._prepare(practice)
            export_practice_pdf(filename, practice)
        except Exception as error:
            self._set_status("PDF export failed")
            messagebox.showerror(
                "PDF Export Failed",
                f"The practice plan could not be exported.\n\n{error}",
            )
            return
        self._set_status(f"PDF exported: {Path(filename).name}")

    def print(self, practice) -> None:
        try:
            self._prepare(practice)
            printed = print_practice(practice)
        except Exception as error:
            self._set_status("Print failed")
            messagebox.showerror(
                "Print Failed",
                f"The practice plan could not be opened for printing.\n\n{error}",
            )
            return
        self._set_status("Practice sent to printer" if printed else "Print canceled")
