import sqlite3
from datetime import date

import customtkinter as ctk
from PIL import Image
from tkinter import PhotoImage, TclError, filedialog, messagebox

from .config import ConfigManager
from .workbook import WorkbookManager
from app.widgets.session_table import SessionTable
from app.repositories.repository_manager import RepositoryManager
from app.services.development_library_service import DevelopmentLibraryService
from app.pages.development_library_page import DevelopmentLibraryPage
from app.pages.practice_builder_page import PracticeBuilderPage
from app.pages.administration_page import AdministrationPage
from app.pages.drill_manager_page import DrillManagerPage
from app.models.practice import Practice
from app.models.player_development import (
    get_block_by_id,
    get_block_by_name,
)
from app.pages.drill_editor_page import DrillEditorPage
from app.models.drill import Drill
from app.services.drill_spreadsheet_service import (
    create_template,
    export_spreadsheet,
    import_spreadsheet,
)
from app.config import BACKUP_DIR, RESOURCE_ROOT, ROOT
from app.services.database_maintenance_service import DatabaseMaintenanceService
from app.services.practice_pdf_service import export_practice_pdf

class SoccerTrainingManager(ctk.CTk):
# ==========================================================
# Initialization
# ==========================================================

    def __init__(self):
        super().__init__()

        self.config_manager = ConfigManager()
        self.workbook = WorkbookManager()
        self.repositories = RepositoryManager()
        self.development_library_service = DevelopmentLibraryService(
            self.repositories.drills
        )
        self.database_maintenance = DatabaseMaintenanceService(
            ROOT / "data" / "coach_training.db",
            BACKUP_DIR,
        )

        self.current_practice = Practice()
        self.title("Training Manager")
        self.geometry("1400x900")
        self.logo_path = (
            RESOURCE_ROOT / "assets" / "images" / "training_manager_logo.png"
        )
        self._set_window_icon()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.build_ui()

    def _set_window_icon(self):
        """Use the Training Manager logo as the native window icon."""
        try:
            self.window_icon = PhotoImage(file=str(self.logo_path))
            self.iconphoto(True, self.window_icon)
        except (OSError, TclError):
            self.window_icon = None

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.sidebar_logo = ctk.CTkImage(
            light_image=Image.open(self.logo_path),
            dark_image=Image.open(self.logo_path),
            size=(52, 52),
        )
        title = ctk.CTkLabel(
            self.sidebar,
            text="Training Manager",
            image=self.sidebar_logo,
            compound="left",
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(pady=20)

        ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            command=self.show_dashboard
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
            "Welcome to Training Manager\n\n"
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
            self.show_development_library_for_block,
            self.save_practice_pdf,
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

    def show_development_library_for_block(self, block):
        """Open the library for a selected development block."""

        selected_development_block = get_block_by_name(block)

        if selected_development_block is None:
            print(f"Unknown development block: {block}")
            return

        self.clear_content()

        page = DevelopmentLibraryPage(
            self.content,
            self.development_library_service,
            selected_block=block,
            add_to_practice_callback=self.add_drills_to_practice,
            cancel_callback=self.show_practice_builder,
        )

        page.pack(fill="both", expand=True)

        page.show_drills(selected_development_block)
    def add_drills_to_practice(self, block, drills):
        """Add selected drills and return to the Practice Builder."""

        for drill in drills:
            self.current_practice.add_activity(
                block,
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
        if not self.practice_builder_page.validate_practice_name():
            return

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

    def save_practice_pdf(self, practice):
        """Ask for a PDF destination and export the current practice plan."""
        safe_name = "".join(
            character if character.isalnum() or character in ("-", "_") else "_"
            for character in (practice.name.strip() or "practice_plan")
        ).strip("_") or "practice_plan"
        filename = filedialog.asksaveasfilename(
            title="Save Practice Plan as PDF",
            initialfile=f"{safe_name}_{date.today().isoformat()}.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF Document", "*.pdf")],
        )
        if not filename:
            self.status.configure(text="PDF export canceled")
            return
        try:
            export_practice_pdf(filename, practice)
        except Exception as error:
            self.status.configure(text="PDF export failed")
            messagebox.showerror(
                "PDF Export Failed",
                f"The practice PDF could not be created.\n\n{error}",
            )
            return
        self.status.configure(text=f"PDF saved: {filename}")
        messagebox.showinfo(
            "Practice PDF Saved",
            f"The practice plan was saved successfully.\n\n{filename}",
        )

# ==========================================================
# Administration
# ==========================================================

    def show_administration(self):
        """Display the Administration dashboard."""

        self.clear_content()

        page = AdministrationPage(
            self.content,
            open_drill_manager_callback=self.show_drill_manager,
            create_template_callback=self.create_drill_template,
            import_spreadsheet_callback=self.import_drill_spreadsheet,
            export_spreadsheet_callback=self.export_drill_spreadsheet,
            database_maintenance_callback=self.run_database_maintenance,
            restore_database_callback=self.restore_database_backup,
        )
        page.pack(
            fill="both",
            expand=True,
        )

    def run_database_maintenance(self):
        """Check database health, then offer backup and optimization."""
        try:
            status = self.database_maintenance.check_health()
        except (OSError, sqlite3.DatabaseError) as error:
            messagebox.showerror("Database Maintenance", str(error))
            return

        if not status.is_healthy:
            messagebox.showerror(
                "Database Maintenance",
                f"The integrity check reported: {status.integrity}\n\n"
                "Optimization was not run.",
            )
            return

        proceed = messagebox.askyesno(
            "Database Maintenance",
            "Database health: Good\n"
            f"Tables: {status.table_count}\n"
            f"Size: {status.size_bytes / (1024 * 1024):.2f} MB\n\n"
            "Create a backup and optimize the database now?",
        )
        if not proceed:
            return

        try:
            backup_path = self.database_maintenance.create_backup()
            bytes_saved = self.database_maintenance.optimize()
        except (OSError, sqlite3.DatabaseError) as error:
            messagebox.showerror("Database Maintenance", str(error))
            return

        messagebox.showinfo(
            "Database Maintenance",
            "Maintenance completed successfully.\n\n"
            f"Backup: {backup_path.name}\n"
            f"Space recovered: {bytes_saved / 1024:.1f} KB",
        )

    def restore_database_backup(self):
        """Select, validate, and restore a database backup."""
        filename = filedialog.askopenfilename(
            title="Restore Database Backup",
            initialdir=BACKUP_DIR,
            filetypes=[("SQLite Database Backup", "*.db"), ("All Files", "*.*")],
        )
        if not filename:
            return

        try:
            status = self.database_maintenance.validate_backup(filename)
        except (OSError, sqlite3.DatabaseError) as error:
            messagebox.showerror("Restore Database", str(error))
            return

        confirmed = messagebox.askyesno(
            "Restore Database",
            "The selected backup is healthy.\n"
            f"Tables: {status.table_count}\n"
            f"Size: {status.size_bytes / (1024 * 1024):.2f} MB\n\n"
            "Restore it now? The current database will be backed up first.",
        )
        if not confirmed:
            return

        try:
            safety_backup = self.database_maintenance.restore_backup(filename)
        except (OSError, sqlite3.DatabaseError) as error:
            messagebox.showerror("Restore Database", str(error))
            return

        messagebox.showinfo(
            "Restore Database",
            "The database was restored successfully.\n\n"
            f"Previous database backup: {safety_backup.name}\n\n"
            "Please restart the application before continuing.",
        )

    def create_drill_template(self):
        filename = filedialog.asksaveasfilename(
            title="Create Drill Import Template",
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx")],
        )
        if filename:
            create_template(filename)
            messagebox.showinfo("Template Created", "The drill import template is ready.")

    def import_drill_spreadsheet(self):
        filename = filedialog.askopenfilename(
            title="Import Drill Spreadsheet",
            filetypes=[("Excel Workbook", "*.xlsx")],
        )
        if not filename:
            return
        report = import_spreadsheet(filename, self.repositories.drills)
        lines = [f"Imported: {report.imported}"]
        if report.duplicates:
            lines.append(f"Duplicates skipped: {len(report.duplicates)}")
        if report.errors:
            lines.append(f"Errors: {len(report.errors)}")
        messagebox.showinfo("Drill Import Report", "\n".join(lines))

    def export_drill_spreadsheet(self):
        filename = filedialog.asksaveasfilename(
            title="Export Active Drills",
            initialfile=f"soccer_drills_{date.today().isoformat()}.xlsx",
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx")],
        )
        if not filename:
            return
        try:
            exported = export_spreadsheet(filename, self.repositories.drills)
        except Exception as error:
            messagebox.showerror(
                "Drill Export Failed",
                f"The spreadsheet could not be created.\n\n{error}",
            )
            return
        messagebox.showinfo(
            "Drill Export Complete",
            f"Exported {exported} active drill(s).\n\n{filename}",
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

        block = get_block_by_id(
            data["development_block_id"]
        )

        if block is None:
            raise ValueError(
                "Unknown development block ID: "
                f"{data['development_block_id']}"
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
            drill.development_block_id = block.id
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
                development_block_id=block.id,
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
            f"block ID {drill.development_block_id})"
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
    def cancel_selection(self) -> None:
        """Return to the Practice Builder without adding drills."""

        if self.cancel_callback is not None:
            self.cancel_callback()  

