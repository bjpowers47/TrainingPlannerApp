import customtkinter as ctk
from tkinter import filedialog

from .config import ConfigManager
from .workbook import WorkbookManager
from app.widgets.session_table import SessionTable
from app.repositories.repository_manager import RepositoryManager
from app.services.sample_development_library import load_sample_drills
from app.services.development_library_service import DevelopmentLibraryService
from app.pages.development_library_page import DevelopmentLibraryPage
from app.pages.practice_builder_page import PracticeBuilderPage
from app.models.practice import Practice
from app.constants.player_development import get_phase_by_name

class SoccerTrainingManager(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.config_manager = ConfigManager()
        self.workbook = WorkbookManager()
        self.repositories = RepositoryManager()
        load_sample_drills(self.repositories)
        self.development_library_service = DevelopmentLibraryService(
            self.repositories.drills
        )

        self.current_practice = Practice()
        self.title("Soccer Training Manager")
        self.geometry("1400x900")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        title = ctk.CTkLabel(
            self.sidebar,
            text="⚽ Soccer Training Manager",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(pady=20)

        ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            command=self.show_dashboard
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Training",
            command=self.show_training
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="Open Workbook",
            command=self.load_workbook
        ).pack(side="bottom", fill="x", padx=10, pady=20)

        self.status = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status.grid(row=1, column=0, columnspan=2, sticky="ew")

        ctk.CTkButton(
            self.sidebar,
            text="Development Library",
            command=self.show_development_library
       ).pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            self.sidebar,
            text="Practice Builder",
            command=self.show_practice_builder
        ).pack(fill="x", padx=10, pady=5)
          
        self.show_dashboard()
        ctk.CTkButton(
            self.sidebar,
            text="Open Practice",
            command=self.open_practice,
        ).pack(
            fill="x",
            padx=15,
            pady=5,
        )
        ctk.CTkButton(
            self.sidebar,
            text="New Practice",
            command=self.new_practice,
        ).pack(
            fill="x",
            padx=15,
            pady=5,
        ) 
        ctk.CTkButton(
            self.sidebar,
            text="Save Practice",
            command=self.save_practice,
        ).pack(
            fill="x",
            padx=15,
            pady=5,
        )       

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=20)

        self.info = ctk.CTkTextbox(self.content, width=900, height=600)
        self.info.pack(padx=20, pady=20, fill="both", expand=True)

        self.info.insert(
            "end",
            "Welcome to Soccer Training Manager\n\n"
            "Version 0.2.1\n\n"
            "Load an Excel workbook to begin."
        )

    def show_training(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content,
            text="Training Sessions",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=15)

        table = SessionTable(self.content)
        table.pack(fill="both", expand=True, padx=20, pady=20)

        if self.workbook.worksheet is None:
            self.status.configure(text="No workbook loaded")
            return

        headers = self.workbook.get_headers()
        sessions = self.workbook.get_sessions()

        table.load_data(headers, sessions)

        self.status.configure(
            text=f"{len(sessions)} training sessions loaded"
        )

    def load_workbook(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Excel Workbook", "*.xlsx")]
        )

        if not filename:
            return

        self.workbook.open(filename)

        self.status.configure(text=f"Loaded: {filename}")

        self.show_training()
    def show_development_library(self):
        self.clear_content()

        page = DevelopmentLibraryPage(
            self.content,
            self.development_library_service
        )

        page.pack(fill="both", expand=True)

    def show_practice_builder(self):
        self.clear_content()

        page = PracticeBuilderPage(
            self.content,
            self.current_practice,
            self.show_development_library_for_phase,
        )
        page.pack(fill="both", expand=True)
        page.lift()
        page.focus_set()

    def show_development_library_for_phase(self, phase):
        """Open the library for a selected development phase."""

        selected_development_phase = get_phase_by_name(phase)
        block_id = selected_development_phase.id

        self.clear_content()

        page = DevelopmentLibraryPage(
            self.content,
            self.development_library_service,
            selected_phase=phase,
            add_to_practice_callback=self.add_drills_to_practice,
        )

        page.pack(fill="both", expand=True)
        block_id = selected_development_phase.id
        
        if block_id is not None:
            page.show_drills(block_id)
    
    def add_drills_to_practice(self, phase, drills):
        """Add selected drills and return to the Practice Builder."""

        for drill in drills:
            self.current_practice.add_activity(
                phase,
                drill,
            )

        self.show_practice_builder()
    def open_practice(self):
        """Open a previously saved practice."""

        filename = filedialog.askopenfilename(
            title="Open Practice",
            filetypes=[
                ("JSON Files", "*.json"),
                ("All Files", "*.*"),
            ],
        )

        if not filename:
            return

        self.current_practice = Practice.load_from_json(
            filename
        )

        self.show_practice_builder()
    def new_practice(self):
        """Start a brand-new practice."""

        self.current_practice = Practice()

        self.show_practice_builder()
    def save_practice(self):
        """Save the current practice."""

        filename = filedialog.asksaveasfilename(
            title="Save Practice",
            defaultextension=".json",
            filetypes=[
                ("JSON Files", "*.json"),
                ("All Files", "*.*"),
            ],
        )

        if not filename:
            return

        self.current_practice.save_to_json(filename)
       