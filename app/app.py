import customtkinter as ctk
from tkinter import filedialog

from .config import ConfigManager
from .workbook import WorkbookManager
from app.pages.dashboard_page import DashboardPage
from app.pages.training_page import TrainingPage


class SoccerTrainingManager(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.config_manager = ConfigManager()

        self.workbook = WorkbookManager()

        self.title("Soccer Training Manager")

        self.geometry("1400x900")

        ctk.set_appearance_mode("dark")

        ctk.set_default_color_theme("blue")

        self.build_ui()

    def build_ui(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220)

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.content = ctk.CTkFrame(self)

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        title = ctk.CTkLabel(
            self.sidebar,
            text="⚽ Soccer Training Manager",
            font=("Segoe UI", 22, "bold")
        )

        title.pack(pady=20)

        buttons = [
            "Dashboard",
            "Training",
            "Players",
            "Attendance",
            "Reports",
            "Settings"
        ]

        for text in buttons:

            btn = ctk.CTkButton(
                self.sidebar,
                text=text
            )

            btn.pack(fill="x", padx=10, pady=5)

        load = ctk.CTkButton(
            self.sidebar,
            text="Open Workbook",
            command=self.load_workbook
        )

        load.pack(
            side="bottom",
            fill="x",
            padx=10,
            pady=20
        )

        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w"
        )

        self.status.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew"
        )

        self.dashboard()

    def dashboard(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=20)

        self.info = ctk.CTkTextbox(
            self.content,
            width=900,
            height=600
        )

        self.info.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        self.info.insert(
            "end",
            "Welcome to Soccer Training Manager\n\n"
            "Version 0.1\n\n"
            "Load an Excel workbook to begin."
        )

    def load_workbook(self):

        filename = filedialog.askopenfilename(
            filetypes=[
                ("Excel Workbook", "*.xlsx")
            ]
        )

        if not filename:
            return

        sheets = self.workbook.open(filename)

        self.status.configure(
            text=f"Loaded: {filename}"
        )

        self.info.delete("1.0", "end")

        self.info.insert(
            "end",
            "Workbook Loaded Successfully\n\n"
        )

        self.info.insert(
            "end",
            "Worksheets\n\n"
        )

        for sheet in sheets:

            self.info.insert(
                "end",
                f"• {sheet}\n"
            )