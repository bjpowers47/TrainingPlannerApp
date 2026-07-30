import customtkinter as ctk

from app.models.player_development import DEVELOPMENT_PHASES
from app.services.coaching_library import (
    get_coaching_focus_by_id,
    get_coaching_focus_id_by_name,
    get_coaching_focus_names_by_phase,
)


class DrillEditorPage(ctk.CTkFrame):
    """Page used to create or edit a drill."""

    def __init__(
        self,
        master,
        drill=None,
        on_save=None,
        on_cancel=None,
    ):
        super().__init__(master)
        self.drill = drill
        self.on_save = on_save
        self.on_cancel = on_cancel

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_form()
        self._build_buttons()

        if self.drill is not None:
            self._load_drill()

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

        title_text = "Edit Drill" if self.drill else "New Drill"

        title = ctk.CTkLabel(
            header,
            text=title_text,
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

        self.phase_prompt = "Select Development Phase"

        self.phase_lookup = {
            f"{phase.icon} {phase.name}": phase
            for phase in DEVELOPMENT_PHASES
        }

        phase_names = list(self.phase_lookup.keys())

        self.phase_menu = ctk.CTkOptionMenu(
            self.form,
            values=phase_names,
            height=38,
            command=self._phase_changed,
        )
        self.phase_menu.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )

        # Display the prompt without making it a selectable menu item.
        self.phase_menu.set(self.phase_prompt)

        self._add_label(
            "Coaching Focus",
            row=2,
            column=1,
        )

        self.focus_prompt = "Select Development Phase First"

        self.focus_menu = ctk.CTkOptionMenu(
            self.form,
            values=[self.focus_prompt],
            height=38,
        )
        self.focus_menu.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )
        self.focus_menu.set(self.focus_prompt)

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

        self._add_label("Time (min)", row=7, column=0)

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

        self._add_label("Players", row=7, column=1)

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

        self._build_execution_details()

    def _build_execution_details(self):
        """Build the optional execution detail fields."""

        self._add_label(
            "Execution Details",
            row=9,
            column=0,
        )

        self.execution_frame = ctk.CTkFrame(
            self.form,
            fg_color="transparent",
        )
        self.execution_frame.grid(
            row=10,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )

        for column in range(4):
            self.execution_frame.grid_columnconfigure(column, weight=1)

        self.sets_entry = self._add_execution_field(
            label="Sets",
            placeholder="3",
            column=0,
        )
        self.reps_entry = self._add_execution_field(
            label="Reps",
            placeholder="10",
            column=1,
        )
        self.work_entry = self._add_execution_field(
            label="Work (sec)",
            placeholder="45",
            column=2,
        )
        self.rest_entry = self._add_execution_field(
            label="Rest (sec)",
            placeholder="30",
            column=3,
        )

    def _add_execution_field(self, label, placeholder, column):
        field_frame = ctk.CTkFrame(
            self.execution_frame,
            fg_color="transparent",
        )
        field_frame.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=8,
            pady=10,
        )

        field_frame.grid_columnconfigure(0, weight=1)

        field_label = ctk.CTkLabel(
            field_frame,
            text=label,
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        )
        field_label.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 6),
        )

        entry = ctk.CTkEntry(
            field_frame,
            placeholder_text=placeholder,
            height=36,
        )
        entry.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        return entry

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

    def _phase_changed(self, selected_phase_name):
        """Load the Coaching Focuses for the selected Development Phase."""

        selected_phase = self.phase_lookup.get(selected_phase_name)

        if selected_phase is None:
            self.focus_menu.configure(
                values=[self.focus_prompt]
            )
            self.focus_menu.set(self.focus_prompt)
            return

        focus_names = get_coaching_focus_names_by_phase(
            selected_phase.id
        )

        menu_values = [
            "Not selected",
            *focus_names,
        ]

        self.focus_menu.configure(values=menu_values)
        self.focus_menu.set("Not selected")

    def _load_drill(self):
        """Populate the editor from an existing drill."""

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, self.drill.name)

        selected_phase_name = None

        for menu_name, phase in self.phase_lookup.items():
            if phase.id == self.drill.development_block_id:
                selected_phase_name = menu_name
                break

        if selected_phase_name is not None:
            self.phase_menu.set(selected_phase_name)
            self._phase_changed(selected_phase_name)

        if self.drill.technical_focus_id:
            focus = get_coaching_focus_by_id(
                self.drill.technical_focus_id
            )

            if focus:
                self.focus_menu.set(focus.name)

        self.purpose_textbox.delete("1.0", "end")
        self.purpose_textbox.insert(
            "1.0",
            self.drill.purpose,
        )

        self._set_entry(
            self.duration_entry,
            self.drill.duration_minutes,
        )
        self._set_entry(
            self.players_entry,
            self.drill.recommended_players,
        )

        # getattr keeps older Drill objects compatible until the model is updated.
        sets = getattr(self.drill, "sets", None)
        reps = getattr(self.drill, "reps", None)
        work_seconds = getattr(self.drill, "work_seconds", None)
        rest_seconds = getattr(self.drill, "rest_seconds", None)

        self._set_entry(self.sets_entry, sets)
        self._set_entry(self.reps_entry, reps)
        self._set_entry(self.work_entry, work_seconds)
        self._set_entry(self.rest_entry, rest_seconds)

    @staticmethod
    def _set_entry(entry, value):
        entry.delete(0, "end")

        if value not in (None, ""):
            entry.insert(0, str(value))

    def _save(self):
        """Collect the drill values and send them to the save callback."""

        selected_phase_name = self.phase_menu.get()
        selected_phase = self.phase_lookup.get(selected_phase_name)

        selected_focus_name = self.focus_menu.get()

        development_block_id = None
        technical_focus_id = None

        if selected_phase is not None:
            development_block_id = selected_phase.id

            if selected_focus_name != "Not selected":
                technical_focus_id = get_coaching_focus_id_by_name(
                    name=selected_focus_name,
                    development_phase_id=development_block_id,
                )

        sets = self.sets_entry.get().strip()
        reps = self.reps_entry.get().strip()
        work_seconds = self.work_entry.get().strip()
        rest_seconds = self.rest_entry.get().strip()

        use_execution_details = any(
            (
                sets,
                reps,
                work_seconds,
                rest_seconds,
            )
        )

        drill_data = {
            "name": self.name_entry.get().strip(),
            "development_block_id": development_block_id,
            "technical_focus_id": technical_focus_id,
            "development_phase": (
                selected_phase.name
                if selected_phase is not None
                else ""
            ),
            "technical_focus": (
                selected_focus_name
                if selected_focus_name != "Not selected"
                else ""
            ),
            "purpose": self.purpose_textbox.get(
                "1.0",
                "end",
            ).strip(),
            "duration_minutes": self.duration_entry.get().strip(),
            "recommended_players": self.players_entry.get().strip(),
            "use_execution_details": use_execution_details,
            "sets": sets,
            "reps": reps,
            "work_seconds": work_seconds,
            "rest_seconds": rest_seconds,
        }

        if self.drill is not None:
            drill_data["id"] = self.drill.id

        if self.on_save:
            self.on_save(drill_data)

    def _cancel(self):
        if self.on_cancel:
            self.on_cancel()
