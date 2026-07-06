import customtkinter as ctk

from app.widgets.session_table import SessionTable


class TrainingPage(ctk.CTkFrame):

    def __init__(self, master, workbook_manager):
        super().__init__(master)

        self.workbook = workbook_manager

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Training Schedule",
            font=("Segoe UI", 24, "bold")
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 10)
        )

        self.search = ctk.CTkEntry(
            self,
            placeholder_text="Search..."
        )

        self.search.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 10)
        )

        self.table = SessionTable(self)

        self.table.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 20)
        )

    def refresh(self):

        if self.workbook.worksheet is None:
            return

        sessions = self.workbook.get_sessions()

        self.table.load_sessions(sessions)