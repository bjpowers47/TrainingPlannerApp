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
from app.pages.administration_page import AdministrationPage
from app.pages.drill_manager_page import DrillManagerPage
from app.models.practice import Practice
from app.models.player_development import get_phase_by_name
from app.pages.drill_editor_page import DrillEditorPage
from app.models.drill import Drill

class SoccerTrainingManager(ctk.CTk):
# ==========================================================
# Initialization
# ==========================================================

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
            font=("Segoe UI", 18, "bold")
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
        administration_button = ctk.CTkButton(
            self.sidebar,
            text="Administration",
            command=self.show_administration,
        )
        administration_button.pack(
            fill="x",
            padx=15,
            pady=6,
        )   
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

# ==========================================================
# Navigation
# ==========================================================

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
    def show_development_library(self):
        self.clear_content()

        page = DevelopmentLibraryPage(
            self.content,
            self.development_library_service
        )

        page.pack(fill="both", expand=True)
    def show_practice_builder(self):
        self.clear_content()
        self.practice_builder_page = PracticeBuilderPage(
            self.content,
            self.current_practice,
            self.show_development_library_for_phase,
        )
        self.practice_builder_page.pack(
            fill="both",
            expand=True,
        )

        self.practice_builder_page.pack( 
            fill="both", 
            expand=True, 
        )

        self.practice_builder_page.lift()
        self.practice_builder_page.focus_set()

# ==========================================================
# Practice Management
# ==========================================================

    def show_development_library_for_phase(self, phase):
        """Open the library for a selected development phase."""

        selected_development_phase = get_phase_by_name(phase)

        if selected_development_phase is None:
            print(f"Unknown development phase: {phase}")
            return

        self.clear_content()

        page = DevelopmentLibraryPage(
            self.content,
            self.development_library_service,
            selected_phase=phase,
            add_to_practice_callback=self.add_drills_to_practice,
        )

        page.pack(fill="both", expand=True)

        page.show_drills(selected_development_phase)
    def add_drills_to_practice(self, phase, drills):
        """Add selected drills and return to the Practice Builder."""

        for drill in drills:
            self.current_practice.add_activity(
                phase,
                drill,
            )

        self.show_practice_builder()
    def new_practice(self):
        """Start a brand-new practice."""
        self.current_practice = Practice()
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
    def save_practice(self):
        """Save the current practice to a JSON file."""

        if not hasattr(self, "practice_builder_page"):
            return

        self.practice_builder_page.update_practice_information()

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

# ==========================================================
# Administration
# ==========================================================

    def show_administration(self):
        """Display the Administration dashboard."""

        self.clear_content()

        page = AdministrationPage(
            self.content,
            open_drill_manager_callback=self.show_drill_manager,
        )
        page.pack(
            fill="both",
            expand=True,
        )
    def show_drill_manager(self):

        self.clear_content()

        page = DrillManagerPage(
            self.content,
            self.development_library_service,
            on_new_drill=self.show_drill_editor,
            on_edit_drill=self.show_drill_editor,
        )

        page.pack(fill="both", expand=True)
    def show_drill_editor(self, drill=None):
        self.clear_content()

        page = DrillEditorPage(
            self.content,
            drill=drill,
            on_save=self.handle_drill_editor_save,
            on_cancel=self.show_drill_manager,
        )

        page.pack(fill="both", expand=True)
    def handle_drill_editor_save(self, data):
        """Create a new drill or update an existing drill."""

        def to_int_or_none(value):
            value = str(value).strip()

            if value == "":
                return None

            return int(value)
        existing_drills = self.repositories.drills.get_all()

        phase = get_phase_by_name(data["development_phase"])

        if phase is None:
            raise ValueError(
                f"Unknown development phase: {data['development_phase']}"
            )

        drill_id = data.get("id")

        if drill_id is not None:
            #
            # Edit an existing drill
            #
            drill = next(
                (
                    existing_drill
                    for existing_drill in existing_drills
                    if existing_drill.id == drill_id
                ),
                None,
            )

            if drill is None:
                raise ValueError(
                    f"Unable to find drill with ID {drill_id}."
                )

            drill.name = data["name"].strip()
            drill.development_block_id = phase.id
            drill.technical_focus_id = data.get(
                "technical_focus_id"
            )
            drill.purpose = data["purpose"].strip()
            drill.duration_minutes = int(
                data["duration_minutes"] or 0
            )
            drill.use_execution_details = data.get(
                "use_execution_details",
                False,
            )

            drill.sets = to_int_or_none(data.get("sets", ""))
            drill.reps = to_int_or_none(data.get("reps", ""))
            drill.work_seconds = to_int_or_none(
                data.get("work_seconds", "")
            )
            drill.rest_seconds = to_int_or_none(
                data.get("rest_seconds", "")
            )
            drill.recommended_players = data[
                "recommended_players"
            ].strip()

            action = "Updated"

        else:
            #
            # Create a new drill
            #
            next_id = max(
                (drill.id for drill in existing_drills),
                default=0,
            ) + 1

            drill = Drill(
                id=next_id,
                name=data["name"].strip(),
                development_block_id=phase.id,
                technical_focus_id=data.get(
                    "technical_focus_id"
                ),
                purpose=data["purpose"].strip(),
                duration_minutes=int(
                    data["duration_minutes"] or 0
                ),
                recommended_players=data[
                    "recommended_players"
                ].strip(),

                use_execution_details=data.get(
                    "use_execution_details",
                    False,
                ),
                sets=to_int_or_none(data.get("sets", "")),
                reps=to_int_or_none(data.get("reps", "")),
                work_seconds=to_int_or_none(
                    data.get("work_seconds", "")
                ),
                rest_seconds=to_int_or_none(
                    data.get("rest_seconds", "")
                ),
            )

            action = "Created"

        self.repositories.drills.save(drill)

        print(
            f"{action} drill: {drill.name} "
            f"(ID {drill.id}, "
            f"phase ID {drill.development_block_id})"
        )

        self.show_drill_manager()

# ==========================================================
# Workbook
# ==========================================================

    def load_workbook(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Excel Workbook", "*.xlsx")]
        )

        if not filename:
            return

        self.workbook.open(filename)

        self.status.configure(text=f"Loaded: {filename}")

        self.show_training()
