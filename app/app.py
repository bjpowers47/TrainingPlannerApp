import sqlite3
from copy import deepcopy
from dataclasses import asdict
import json
from datetime import date, datetime
from pathlib import Path

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
from app.pages.configuration_page import ConfigurationPage
from app.models.practice import Practice
from app.models.player_development import (
    get_block_by_id,
    get_block_by_name,
)


def _to_int_or_none(value):
    """Parse an optional numeric form value without accepting invalid input."""
    if value is None:
        return None

    value = str(value).strip()
    if value.casefold() in {"", "none", "null"}:
        return None

    return int(float(value))
from app.pages.drill_editor_page import DrillEditorPage
from app.models.drill import Drill
from app.services.drill_spreadsheet_service import (
    create_template,
    export_spreadsheet,
    import_spreadsheet,
)
from app.config import (
    APP_NAME, APP_VERSION, AUTOSAVE_FILE, BACKUP_DIR, PRACTICES_DIR,
    RESOURCE_ROOT, ROOT, training_manager_name,
)
from app.services.database_maintenance_service import DatabaseMaintenanceService
from app.services.practice_pdf_service import print_practice

class TrainingPlannerApp(ctk.CTk):
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
            training_manager_name(self.config_manager.data.get("sport", "")),
        )

        self.current_practice = Practice()
        self.current_practice_path = None
        self._saved_practice_signature = self._practice_signature(self.current_practice)
        self.title(APP_NAME)
        self.geometry(
            f"{self.config_manager.data.get('window_width', 1400)}x"
            f"{self.config_manager.data.get('window_height', 900)}"
        )
        self.logo_path = (
            RESOURCE_ROOT / "assets" / "images" / "training_manager_logo.png"
        )
        self._set_window_icon()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.build_ui()
        self.bind_all("<Control-s>", lambda _event: self.save_practice())
        self.bind_all("<Control-o>", lambda _event: self.open_practice())
        self.bind_all("<Control-n>", lambda _event: self.new_practice())
        self.bind_all("<Control-p>", lambda _event: self.save_practice_pdf(self.current_practice))
        self.protocol("WM_DELETE_WINDOW", self._close_application)
        self.after(15000, self._autosave_draft)

    def _set_window_icon(self):
        """Use the application logo as the native window icon."""
        try:
            self.window_icon = PhotoImage(file=str(self.logo_path))
            self.iconphoto(True, self.window_icon)
        except (OSError, TclError):
            self.window_icon = None

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.banner = ctk.CTkLabel(self, text=self.config_manager.data.get("title", APP_NAME)[:40], font=("Segoe UI", 22, "bold"), height=42)
        self.banner.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.grid(row=1, column=0, sticky="ns")

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.sidebar_logo = ctk.CTkImage(
            light_image=Image.open(self.logo_path),
            dark_image=Image.open(self.logo_path),
            size=(52, 52),
        )
        title = ctk.CTkLabel(
            self.sidebar,
            text=APP_NAME,
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

        self.status = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status.grid(row=2, column=0, columnspan=2, sticky="ew")

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
            text="Duplicate Practice",
            command=self.duplicate_practice,
        ).pack(fill="x", padx=15, pady=5)
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

        actions = ctk.CTkFrame(self.content, fg_color="transparent")
        actions.pack(fill="x", padx=30, pady=(5, 15))
        ctk.CTkButton(actions, text="New Practice", command=self.new_practice).pack(side="left", padx=(0, 8))
        ctk.CTkButton(actions, text="Open Practice", command=self.open_practice).pack(side="left", padx=8)
        if self._has_unsaved_draft():
            ctk.CTkButton(
                actions,
                text="Continue Unsaved Practice",
                command=self.restore_autosave,
            ).pack(side="left", padx=8)

        ctk.CTkLabel(
            self.content,
            text=f"Welcome to {APP_NAME}  •  Version {APP_VERSION}\n"
                 f"Head Coach: {self.config_manager.data.get('head_coach', '') or 'Not configured'}",
            justify="left",
        ).pack(anchor="w", padx=30, pady=(0, 18))

        ctk.CTkLabel(self.content, text="Recent Practices", font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=30)
        recent = [Path(item) for item in self.config_manager.data.get("recent_practices", [])]
        recent = [path for path in recent if path.is_file()]
        if not recent:
            ctk.CTkLabel(self.content, text="No saved practices yet.", text_color="gray").pack(anchor="w", padx=30, pady=10)
        for path in recent[:8]:
            row = ctk.CTkFrame(self.content, fg_color="transparent")
            row.pack(fill="x", padx=30, pady=4)
            ctk.CTkButton(
                row, text=path.stem, anchor="w",
                command=lambda selected=path: self._open_practice_path(selected),
            ).pack(side="left", fill="x", expand=True, padx=(0, 8))
            ctk.CTkButton(
                row,
                text="Delete",
                width=80,
                fg_color="#9b2c2c",
                hover_color="#7f1d1d",
                command=lambda selected=path: self._delete_recent_practice(selected),
            ).pack(side="right")
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
            self.development_library_service,
            blocks=self.repositories.development_blocks.list_all(),
        )

        page.pack(fill="both", expand=True)
    def show_practice_builder(self):
        self.clear_content()
        self.current_practice.configured_blocks = [block.name for block in self.repositories.development_blocks.list_all()]
        self.practice_builder_page = PracticeBuilderPage(
            self.content,
            self.current_practice,
            self.show_development_library_for_block,
            export_pdf_callback=self.save_practice_pdf,
            save_practice_callback=self.save_practice,
            coaches=self._configured_coaches(),
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

        selected_development_block = self.repositories.development_blocks.get_by_name(block)

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
            blocks=self.repositories.development_blocks.list_all(),
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
        self._autosave_draft(schedule_next=False)
        self.current_practice = Practice()
        self.current_practice_path = None
        self._saved_practice_signature = self._practice_signature(self.current_practice)
        self.show_practice_builder()

    def duplicate_practice(self):
        """Create an editable copy without changing the original file."""
        page = getattr(self, "practice_builder_page", None)
        if page is not None and page.winfo_exists():
            page.update_practice_information()
        duplicate = deepcopy(self.current_practice)
        duplicate.name = f"{duplicate.name} Copy".strip()
        self.current_practice = duplicate
        self.current_practice_path = None
        self._saved_practice_signature = None
        self.show_practice_builder()
        self.status.configure(text="Practice duplicated; save it with a new name")
    def open_practice(self):
        """Open a previously saved practice."""
        filename = filedialog.askopenfilename(
            title="Open Practice",
            initialdir=self.config_manager.data.get("last_practice_folder", str(PRACTICES_DIR)),
            filetypes=[
                ("JSON Files", "*.json"),
                ("All Files", "*.*"),
            ],
        )

        if not filename:
            return

        self._open_practice_path(filename)

    def _open_practice_path(self, filename):
        """Open a saved practice with a coach-friendly error if it is damaged."""
        try:
            practice = Practice.load_from_json(filename)
        except (OSError, ValueError, TypeError) as error:
            messagebox.showerror(
                "Open Practice",
                f"This practice could not be opened. It may be damaged or incompatible.\n\n{error}",
            )
            return
        self.current_practice = practice
        self.current_practice_path = Path(filename)
        self._saved_practice_signature = self._practice_signature(practice)
        self.config_manager.remember_practice(filename)
        self.show_practice_builder()
    def save_practice(self):
        """Save the current practice to a JSON file."""

        if not hasattr(self, "practice_builder_page"):
            return

        self.practice_builder_page.update_practice_information()
        if not self.practice_builder_page.validate_practice_name():
            return

        invalid_characters = '<>:"/\\|?*'
        safe_name = "".join(
            "_" if character in invalid_characters or ord(character) < 32 else character
            for character in self.current_practice.name.strip()
        ).rstrip(". ")[:100].rstrip(". ")
        reserved_names = {"CON", "PRN", "AUX", "NUL"} | {
            f"{prefix}{number}"
            for prefix in ("COM", "LPT")
            for number in range(1, 10)
        }
        if safe_name.upper() in reserved_names:
            safe_name = f"_{safe_name}"
        safe_name = safe_name or "practice"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = self.current_practice_path
        if filename is None:
            filename = filedialog.asksaveasfilename(
                title="Save Practice",
                initialdir=self.config_manager.data.get("last_practice_folder", str(PRACTICES_DIR)),
                initialfile=f"{safe_name}_{timestamp}.json",
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            )

        if not filename:
            return

        self.current_practice.save_to_json(filename)
        self.current_practice_path = Path(filename)
        self._saved_practice_signature = self._practice_signature(self.current_practice)
        self.config_manager.remember_practice(filename)
        AUTOSAVE_FILE.unlink(missing_ok=True)
        self.status.configure(text=f"Saved: {Path(filename).name}")

    def save_practice_pdf(self, practice):
        """Open the print dialog for the current practice plan."""
        try:
            head_coach = self.config_manager.data.get("head_coach", "")
            practice.head_coach = head_coach
            practice.sport = self.config_manager.data.get("sport", "")[:15]
            printed = print_practice(practice)
        except Exception as error:
            self.status.configure(text="Print failed")
            messagebox.showerror(
                "Print Failed",
                f"The practice plan could not be opened for printing.\n\n{error}",
            )
            return
        self.status.configure(text="Practice sent to printer" if printed else "Print canceled")

    def _autosave_draft(self, schedule_next=True):
        """Persist an unobtrusive recovery copy of the practice in progress."""
        try:
            page = getattr(self, "practice_builder_page", None)
            if page is not None and page.winfo_exists():
                page.update_practice_information()
            signature = self._practice_signature(self.current_practice)
            if (
                signature != self._saved_practice_signature
                and (self.current_practice.name or self.current_practice.activity_count())
            ):
                self.current_practice.save_to_json(AUTOSAVE_FILE)
                self.status.configure(text="Draft autosaved")
        except (OSError, ValueError, TclError):
            # Autosave must never interrupt planning; explicit save still reports errors.
            pass
        finally:
            if schedule_next:
                self.after(15000, self._autosave_draft)

    def restore_autosave(self):
        try:
            self.current_practice = Practice.load_from_json(AUTOSAVE_FILE)
        except (OSError, ValueError, TypeError) as error:
            messagebox.showerror("Recover Draft", f"The draft could not be recovered.\n\n{error}")
            return
        self.current_practice_path = None
        self._saved_practice_signature = None
        self.show_practice_builder()
        self.status.configure(text="Recovered autosaved draft")

    @staticmethod
    def _practice_signature(practice):
        """Return a stable representation used to distinguish saved and unsaved work."""
        data = asdict(practice)
        data.pop("configured_blocks", None)
        return json.dumps(data, sort_keys=True, ensure_ascii=False)

    def _has_unsaved_draft(self):
        """Return True only when autosave contains work not already saved."""
        if not AUTOSAVE_FILE.is_file():
            return False
        try:
            draft = Practice.load_from_json(AUTOSAVE_FILE)
            draft_signature = self._practice_signature(draft)
            for filename in self.config_manager.data.get("recent_practices", []):
                path = Path(filename)
                if path.is_file() and self._practice_signature(Practice.load_from_json(path)) == draft_signature:
                    AUTOSAVE_FILE.unlink(missing_ok=True)
                    return False
            return bool(draft.name or draft.activity_count())
        except (OSError, ValueError, TypeError):
            return False

    def _delete_recent_practice(self, path):
        """Remove an item from dashboard history while preserving its file."""
        if not messagebox.askyesno(
            "Delete Recent Practice",
            f'Remove "{path.stem}" from Recent Practices?\n\nThe saved practice file will not be deleted.',
        ):
            return
        self.config_manager.forget_practice(path)
        self.show_dashboard()

    def _close_application(self):
        self._autosave_draft(schedule_next=False)
        self.config_manager.data["window_width"] = self.winfo_width()
        self.config_manager.data["window_height"] = self.winfo_height()
        self.config_manager.save()
        self.destroy()

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
            configuration_callback=self.show_configuration,
        )
        page.pack(
            fill="both",
            expand=True,
        )

    def _configured_coaches(self):
        values = [self.config_manager.data.get("head_coach", ""), *self.config_manager.data.get("assistant_coaches", [])]
        return [value for value in values if value]

    def show_configuration(self):
        self.clear_content()
        ConfigurationPage(self.content, self.config_manager, self.repositories.development_blocks, self._configuration_saved).pack(fill="both", expand=True)

    def _configuration_saved(self):
        self.banner.configure(text=self.config_manager.data.get("title", APP_NAME)[:40])
        self.database_maintenance.manager_name = training_manager_name(
            self.config_manager.data.get("sport", "")
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
            initialfile=f"training_planner_drills_{date.today().isoformat()}.xlsx",
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx")],
        )
        if not filename:
            return
        try:
            exported = export_spreadsheet(
                filename,
                self.repositories.drills,
                self.repositories.development_blocks,
            )
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
            blocks=self.repositories.development_blocks.list_all(),
        )

        page.pack(fill="both", expand=True)
    def show_drill_editor(self, drill=None):
        self.clear_content()

        page = DrillEditorPage(
            self.content,
            drill=drill,
            on_save=self.handle_drill_editor_save,
            on_cancel=self.show_drill_manager,
            blocks=self.repositories.development_blocks.list_all(),
        )

        page.pack(fill="both", expand=True)
    def handle_drill_editor_save(self, data):
        """Create a new drill or update an existing drill."""
        existing_drills = self.repositories.drills.get_all()

        block = self.repositories.development_blocks.get_by_id(
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
            drill.coaching_focus = data.get("technical_focus", "")[:50]
            drill.purpose = data["purpose"].strip()
            drill.duration_minutes = int(
                data["duration_minutes"] or 0
            )
            drill.use_execution_details = data.get(
                "use_execution_details",
                False,
            )

            drill.sets = _to_int_or_none(data.get("sets", ""))
            drill.reps = _to_int_or_none(data.get("reps", ""))
            drill.work_seconds = _to_int_or_none(
                data.get("work_seconds", "")
            )
            drill.rest_seconds = _to_int_or_none(
                data.get("rest_seconds", "")
            )
            drill.recommended_players = data[
                "recommended_players"
            ].strip()
            drill.equipment = list(data.get("equipment", []))
            drill.coaching_points = list(data.get("coaching_points", []))
            drill.progressions = list(data.get("progressions", []))
            drill.variations = list(data.get("variations", []))
            drill.notes = data.get("notes", "").strip()

            action = "Updated"

        else:
            #
            # Create a new drill
            #
            # Archived drills are intentionally omitted by get_all().  Let the
            # repository allocate against every stored row so a new drill can
            # never overwrite an archived ID and remain hidden.
            next_id = self.repositories.drills.get_next_id()

            drill = Drill(
                id=next_id,
                name=data["name"].strip(),
                development_block_id=block.id,
                technical_focus_id=data.get(
                    "technical_focus_id"
                ),
                coaching_focus=data.get("technical_focus", "")[:50],
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
                sets=_to_int_or_none(data.get("sets", "")),
                reps=_to_int_or_none(data.get("reps", "")),
                work_seconds=_to_int_or_none(
                    data.get("work_seconds", "")
                ),
                rest_seconds=_to_int_or_none(
                    data.get("rest_seconds", "")
                ),
                equipment=list(data.get("equipment", [])),
                coaching_points=list(data.get("coaching_points", [])),
                progressions=list(data.get("progressions", [])),
                variations=list(data.get("variations", [])),
                notes=data.get("notes", "").strip(),
            )

            action = "Created"

        self.repositories.drills.save(drill)

        saved_drill = self.repositories.drills.get_by_id(drill.id)
        if saved_drill is None or not saved_drill.active:
            raise RuntimeError(
                "The database did not return the saved drill. No changes were made to the screen."
            )

        self.status.configure(text=f'{action} drill: {saved_drill.name}')

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
