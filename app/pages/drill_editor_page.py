print("Loaded drill_editor_page.py")
import customtkinter as ctk

from app.constants.player_development import DEVELOPMENT_PHASES


class DrillEditorPage(ctk.CTkFrame):
    """Page used to create or edit a drill."""

    def __init__(
        self,
        master,
        on_save=None,
        on_cancel=None,
    ):
        super().__init__(master)

        self.on_save = on_save
        self.on_cancel = on_cancel

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_form()
        self._build_buttons()
    def _build_header(self):
        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(25, 10),
        )

        title = ctk.CTkLabel(
            header,
            text="New Drill",
            font=("Segoe UI", 28, "bold"),
            anchor="w",
        )
        title.pack(fill="x")

        subtitle = ctk.CTkLabel(
            header,
            text="Create a drill for your development library.",
            font=("Segoe UI", 14),
            text_color="gray",
            anchor="w",
        )
        subtitle.pack(
            fill="x",
            pady=(4, 0),
        )

    def _build_form(self):
        self.form = ctk.CTkScrollableFrame(self)
        self.form.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=10,
        )

        self.form.grid_columnconfigure(0, weight=1)
        self.form.grid_columnconfigure(1, weight=1)

        self._add_label("Drill Name", row=0, column=0)

        self.name_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="Example: Gates Dribbling",
            height=38,
        )
        self.name_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )

        self._add_label("Development Phase", row=2, column=0)

        phase_names = [
            f"{phase.icon} {phase.name}"
            for phase in DEVELOPMENT_PHASES
        ]

        self.phase_menu = ctk.CTkOptionMenu(
            self.form,
            values=phase_names,
            height=38,
        )
        self.phase_menu.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )

        self._add_label("Technical Focus", row=2, column=1)

        self.focus_menu = ctk.CTkOptionMenu(
            self.form,
            values=["Not selected"],
            height=38,
        )
        self.focus_menu.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )

        self._add_label("Purpose", row=4, column=0)

        purpose_help = ctk.CTkLabel(
            self.form,
            text="Describe what this drill is trying to teach.",
            font=("Segoe UI", 12),
            text_color="gray",
            anchor="w",
        )
        purpose_help.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 6),
        )

        self.purpose_textbox = ctk.CTkTextbox(
            self.form,
            height=120,
        )
        self.purpose_textbox.grid(
            row=6,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )

        self._add_label("Duration (minutes)", row=7, column=0)

        self.duration_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="10",
            height=38,
        )
        self.duration_entry.grid(
            row=8,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )

        self._add_label("Recommended Players", row=7, column=1)

        self.players_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="8",
            height=38,
        )
        self.players_entry.grid(
            row=8,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )

    def _build_buttons(self):
        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        button_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=30,
            pady=(10, 25),
        )

        button_frame.grid_columnconfigure(0, weight=1)

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=110,
            fg_color="gray",
            command=self._cancel,
        )
        cancel_button.pack(side="right", padx=(10, 0))

        save_button = ctk.CTkButton(
            button_frame,
            text="Save Drill",
            width=130,
            command=self._save,
        )
        save_button.pack(side="right")

    def _add_label(self, text, row, column):
        label = ctk.CTkLabel(
            self.form,
            text=text,
            font=("Segoe UI", 14, "bold"),
            anchor="w",
        )
        label.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=15,
            pady=(8, 6),
        )

    def _save(self):
        """Temporarily display the entered values in the console."""

        drill_data = {
            "name": self.name_entry.get().strip(),
            "development_phase": self.phase_menu.get(),
            "technical_focus": self.focus_menu.get(),
            "purpose": self.purpose_textbox.get(
                "1.0",
                "end",
            ).strip(),
            "duration_minutes": self.duration_entry.get().strip(),
            "recommended_players": self.players_entry.get().strip(),
        }

        print("Drill editor values:")
        print(drill_data)

        if self.on_save:
            self.on_save(drill_data)

    def _cancel(self):
        if self.on_cancel:
            self.on_cancel()