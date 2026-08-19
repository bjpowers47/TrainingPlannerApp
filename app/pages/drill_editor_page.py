import customtkinter as ctk

from app.models.player_development import DEVELOPMENT_BLOCKS
from app.services.coaching_library import (
    get_coaching_focus_by_id,
)
from tkinter import messagebox
from app.models.drill_form_data import DrillFormData
from app.models.duration import (
    execution_total_seconds,
    format_duration,
    parse_duration_seconds,
    validate_total_seconds,
)

class DrillEditorPage(ctk.CTkFrame):
    """Page used to create or edit a drill."""

    def __init__(
        self,
        master,
        drill=None,
        on_save=None,
        on_cancel=None,
        blocks=None,
    ):
        super().__init__(master)
        self.drill = drill
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.available_blocks = DEVELOPMENT_BLOCKS if blocks is None else blocks

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_form()
        self._build_buttons()

        if self.drill is not None:
            self._load_drill()
        self.after_idle(self._remember_initial_state)

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

        self._add_label("Development Block", row=2, column=0)

        self.block_prompt = "Select Development Block"

        self.block_lookup = {
            f"{getattr(block, 'icon', '•')} {block.name}": block
            for block in self.available_blocks
        }

        block_names = list(self.block_lookup.keys())

        self.block_menu = ctk.CTkOptionMenu(
            self.form,
            values=block_names,
            height=38,
            command=self._block_changed,
        )
        self.block_menu.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )

        # Display the prompt without making it a selectable menu item.
        self.block_menu.set(self.block_prompt)

        self._add_label(
            "Coaching Focus",
            row=2,
            column=1,
        )

        self.focus_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="Freeform coaching focus (50 characters max)",
            height=38,
        )
        self.focus_entry.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )

        self._add_label("Directions", row=4, column=0)

        purpose_help = ctk.CTkLabel(
            self.form,
            text="Describe how to run the drill.",
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

        self._add_label("Time (min:sec)", row=7, column=0)

        self.duration_entry = ctk.CTkEntry(
            self.form,
            height=38,
            width=84,
            justify="center",
            state="readonly",
        )
        self.duration_entry.grid(
            row=8,
            column=0,
            sticky="w",
            padx=15,
            pady=(0, 18),
        )

        self._add_label("Players", row=7, column=1)

        self.players_var = ctk.StringVar()
        self.players_var.trace_add("write", self._limit_players_text)
        self.players_entry = ctk.CTkEntry(
            self.form,
            placeholder_text="8",
            height=38,
            width=260,
            textvariable=self.players_var,
        )
        self.players_entry.grid(
            row=8,
            column=1,
            sticky="w",
            padx=15,
            pady=(0, 18),
        )

        self._build_execution_details()
        self._build_library_details()

    def _limit_players_text(self, *_args):
        """Keep the Players field within its 30-character limit."""
        value = self.players_var.get()
        if len(value) > 30:
            self.players_var.set(value[:30])

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

        for column in range(3):
            self.execution_frame.grid_columnconfigure(column, weight=1)

        self.sets_entry = self._add_execution_field(
            label="Sets",
            placeholder="3",
            column=0,
            entry_width=64,
        )
        self._set_entry(self.sets_entry, 1)
        (
            self.work_minutes_entry,
            self.work_seconds_entry,
        ) = self._add_duration_fields(
            label="Work",
            column=1,
        )
        (
            self.rest_minutes_entry,
            self.rest_seconds_entry,
        ) = self._add_duration_fields(
            label="Rest",
            column=2,
            left_padding=24,
        )

        self._set_duration_entries(
            self.work_minutes_entry, self.work_seconds_entry, 0
        )
        self._set_duration_entries(
            self.rest_minutes_entry, self.rest_seconds_entry, 0
        )

        digits_3 = (self.register(self._valid_digits), "%P", "3", "")
        seconds_2 = (self.register(self._valid_digits), "%P", "2", "59")
        self.sets_entry.configure(validate="key", validatecommand=digits_3)
        for entry in (self.work_minutes_entry, self.rest_minutes_entry):
            entry.configure(validate="key", validatecommand=digits_3)
        for entry in (self.work_seconds_entry, self.rest_seconds_entry):
            entry.configure(validate="key", validatecommand=seconds_2)

        for entry in (
            self.sets_entry,
            self.work_minutes_entry,
            self.work_seconds_entry,
            self.rest_minutes_entry,
            self.rest_seconds_entry,
        ):
            entry.bind("<KeyRelease>", self._refresh_duration)
            entry.bind("<FocusIn>", self._select_entry_text)
            entry.bind("<Return>", lambda _event: self._save())
            entry.bind("<Escape>", lambda _event: self._cancel())
        self.work_minutes_entry.bind(
            "<KeyRelease>",
            lambda event: self._minutes_key_released(
                event, self.work_seconds_entry
            ),
        )
        self.rest_minutes_entry.bind(
            "<KeyRelease>",
            lambda event: self._minutes_key_released(
                event, self.rest_seconds_entry
            ),
        )
        for entry in (self.work_seconds_entry, self.rest_seconds_entry):
            entry.bind("<FocusOut>", self._normalize_seconds)

        self.execution_error = ctk.CTkLabel(
            self.execution_frame,
            text="",
            text_color=("#b42318", "#ff8a80"),
            anchor="w",
        )
        self.execution_error.grid(
            row=1, column=0, columnspan=3, sticky="ew", padx=8
        )
        ctk.CTkLabel(
            self.execution_frame,
            text="Total Time = Sets × (Work + Rest). Maximum total: 240:00.",
            text_color="gray",
            anchor="w",
        ).grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=(2, 0))
        self._refresh_duration()

    @staticmethod
    def _valid_digits(proposed, max_digits, max_value):
        """Allow a blank value or a bounded whole number while typing."""
        if proposed == "":
            return True
        if not proposed.isdigit() or len(proposed) > int(max_digits):
            return False
        return not max_value or int(proposed) <= int(max_value)

    @staticmethod
    def _select_entry_text(event):
        event.widget.after_idle(lambda: event.widget.select_range(0, "end"))

    def _minutes_key_released(self, event, seconds_entry):
        self._refresh_duration(event)
        if len(event.widget.get()) == 3 and event.keysym.isdigit():
            seconds_entry.focus_set()

    def _normalize_seconds(self, event):
        text = event.widget.get().strip()
        if text:
            self._set_entry(event.widget, f"{int(text):02d}")
        else:
            self._set_entry(event.widget, "00")
        self._refresh_duration()

    def _add_execution_field(
        self, label, placeholder, column, entry_width=None
    ):
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
            width=entry_width or 120,
            justify="center",
        )
        entry.grid(
            row=1,
            column=0,
            sticky="w" if entry_width else "ew",
        )

        return entry

    def _add_duration_fields(
        self, label, column, left_padding=8
    ):
        """Build a labeled pair of minute and second inputs."""
        field_frame = ctk.CTkFrame(
            self.execution_frame,
            fg_color="transparent",
        )
        field_frame.grid(
            row=0,
            column=column,
            sticky="w",
            padx=(left_padding, 8),
            pady=10,
        )

        ctk.CTkLabel(
            field_frame,
            text=label,
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 6))

        minutes_entry = ctk.CTkEntry(
            field_frame,
            placeholder_text="0",
            height=36,
            width=64,
            justify="center",
        )
        minutes_entry.grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(field_frame, text="min").grid(
            row=1, column=1, padx=(5, 12)
        )

        seconds_entry = ctk.CTkEntry(
            field_frame,
            placeholder_text="00",
            height=36,
            width=50,
            justify="center",
        )
        seconds_entry.grid(row=1, column=2, sticky="w")
        ctk.CTkLabel(field_frame, text="sec").grid(
            row=1, column=3, padx=(5, 0)
        )

        return minutes_entry, seconds_entry

    def _build_library_details(self):
        """Build the descriptive fields stored with library drills."""

        self.equipment_textbox = self._add_multiline_field(
            "Equipment (one item per line)", 11, 90
        )
        self.coaching_points_textbox = self._add_multiline_field(
            "Coaching Points (one point per line)", 13, 120
        )
        self.progressions_textbox = self._add_multiline_field(
            "Progressions (one progression per line)", 15, 120
        )
        self.variations_textbox = self._add_multiline_field(
            "Variations (one variation per line)", 17, 120
        )
        self.notes_textbox = self._add_multiline_field("Notes", 19, 120)

    def _add_multiline_field(self, label, row, height):
        self._add_label(label, row=row, column=0)
        textbox = ctk.CTkTextbox(self.form, height=height)
        textbox.grid(
            row=row + 1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=(0, 18),
        )
        return textbox

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

        self.save_button = ctk.CTkButton(
            button_frame,
            text="Save Drill",
            width=130,
            command=self._save,
        )
        self.save_button.pack(side="right")

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

    def _block_changed(self, selected_block_name):
        """Load the Coaching Focuses for the selected Development Block."""

        return

    def _load_drill(self):
        """Populate the editor from an existing drill."""

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, self.drill.name)

        selected_block_name = None

        for menu_name, block in self.block_lookup.items():
            if block.id == self.drill.development_block_id:
                selected_block_name = menu_name
                break

        if selected_block_name is not None:
            self.block_menu.set(selected_block_name)
            self._block_changed(selected_block_name)

        focus_name = getattr(self.drill, "coaching_focus", "")
        if not focus_name and self.drill.technical_focus_id:
            focus = get_coaching_focus_by_id(self.drill.technical_focus_id)
            focus_name = focus.name if focus else ""
        self.focus_entry.insert(0, focus_name)

        self.purpose_textbox.delete("1.0", "end")
        self.purpose_textbox.insert(
            "1.0",
            self.drill.purpose,
        )

        self._set_entry(
            self.players_entry,
            self.drill.recommended_players,
        )

        # getattr keeps older Drill objects compatible until the model is updated.
        sets = getattr(self.drill, "sets", None)
        work_seconds = getattr(self.drill, "work_seconds", None)
        rest_seconds = getattr(self.drill, "rest_seconds", None)

        self._set_entry(self.sets_entry, sets)
        self._set_duration_entries(
            self.work_minutes_entry, self.work_seconds_entry, work_seconds
        )
        self._set_duration_entries(
            self.rest_minutes_entry, self.rest_seconds_entry, rest_seconds
        )
        self._refresh_duration()

        self._set_textbox(
            self.equipment_textbox,
            "\n".join(getattr(self.drill, "equipment", [])),
        )
        self._set_textbox(
            self.coaching_points_textbox,
            "\n".join(getattr(self.drill, "coaching_points", [])),
        )
        self._set_textbox(
            self.progressions_textbox,
            "\n".join(getattr(self.drill, "progressions", [])),
        )
        self._set_textbox(
            self.variations_textbox,
            "\n".join(getattr(self.drill, "variations", [])),
        )
        self._set_textbox(
            self.notes_textbox,
            getattr(self.drill, "notes", ""),
        )

    @staticmethod
    def _set_entry(entry, value):
        entry.delete(0, "end")

        if value not in (None, ""):
            entry.insert(0, str(value))

    @classmethod
    def _set_duration_entries(cls, minutes_entry, seconds_entry, total_seconds):
        """Populate duration component entries from stored seconds."""
        if total_seconds is None:
            cls._set_entry(minutes_entry, 0)
            cls._set_entry(seconds_entry, 0)
            return
        minutes, seconds = divmod(int(total_seconds), 60)
        cls._set_entry(minutes_entry, minutes)
        cls._set_entry(seconds_entry, seconds)

    def _refresh_duration(self, _event=None):
        """Update the read-only Time field from the execution values."""
        try:
            sets = int(self.sets_entry.get().strip() or 1)
            work_seconds = int(self._duration_seconds(
                self.work_minutes_entry.get(),
                self.work_seconds_entry.get(),
                "Work",
            ) or 0)
            rest_seconds = int(self._duration_seconds(
                self.rest_minutes_entry.get(),
                self.rest_seconds_entry.get(),
                "Rest",
            ) or 0)
        except ValueError as error:
            if hasattr(self, "execution_error"):
                self.execution_error.configure(text=str(error))
            return
        if sets < 0:
            return

        total_seconds = execution_total_seconds(
            sets, work_seconds, rest_seconds
        )
        over_limit = total_seconds > 240 * 60
        if hasattr(self, "execution_error"):
            self.execution_error.configure(
                text="Total Time cannot exceed 240:00." if over_limit else ""
            )
        if hasattr(self, "save_button"):
            self.save_button.configure(state="disabled" if over_limit else "normal")
        self.duration_entry.configure(state="normal")
        self._set_entry(
            self.duration_entry,
            format_duration(total_seconds),
        )
        self.duration_entry.configure(state="readonly")

    @staticmethod
    def _duration_seconds(minutes_value, seconds_value, label):
        """Validate duration components and return total seconds or blank."""
        minutes_text = str(minutes_value or "").strip()
        seconds_text = str(seconds_value or "").strip()
        if not minutes_text and not seconds_text:
            return ""
        return str(parse_duration_seconds(minutes_text, seconds_text, label))

    @staticmethod
    def _set_textbox(textbox, value):
        textbox.delete("1.0", "end")
        if value:
            textbox.insert("1.0", value)

    @staticmethod
    def _textbox_lines(textbox):
        return [
            line.strip()
            for line in textbox.get("1.0", "end").splitlines()
            if line.strip()
        ]

    @staticmethod
    def _optional_number_for_save(value):
        """Return an empty form value for a missing optional number."""
        if value is None:
            return ""
        if isinstance(value, str) and value.strip().casefold() in {"", "none", "null"}:
            return ""
        return value

    @staticmethod
    def _whole_number(value, label, *, required=False):
        """Validate a non-negative whole-number form field."""
        value = str(value).strip()
        if not value:
            if required:
                raise ValueError(f"{label} is required.")
            return ""
        try:
            number = float(value)
        except ValueError as error:
            raise ValueError(f"{label} must be a whole number.") from error
        if number < 0 or not number.is_integer():
            raise ValueError(f"{label} must be a non-negative whole number.")
        return str(int(number))

    def _save(self):
        """Collect the drill values and send them to the save callback."""

        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Drill Name Required", "Please enter a Drill Name.")
            return

        selected_block_name = self.block_menu.get()
        selected_block = self.block_lookup.get(selected_block_name)

        selected_focus_name = self.focus_entry.get().strip()[:50]

        development_block_id = None
        technical_focus_id = None

        if selected_block is not None:
            development_block_id = selected_block.id

        if development_block_id is None:
            messagebox.showwarning(
                "Development Block Required",
                "Please select a Development Block.",
            )
            return

        try:
            sets = self._whole_number(self.sets_entry.get(), "Sets")
        except ValueError as error:
            messagebox.showwarning("Invalid Drill Details", str(error))
            return
        try:
            work_seconds = self._duration_seconds(
                self.work_minutes_entry.get(),
                self.work_seconds_entry.get(),
                "Work",
            )
            rest_seconds = self._duration_seconds(
                self.rest_minutes_entry.get(),
                self.rest_seconds_entry.get(),
                "Rest",
            )
        except ValueError as error:
            messagebox.showwarning("Invalid Time", str(error))
            return

        total_seconds = execution_total_seconds(sets, work_seconds, rest_seconds)
        try:
            validate_total_seconds(total_seconds)
        except ValueError as error:
            messagebox.showwarning(
                "Invalid Time",
                f"{error} Reduce Sets, Work, or Rest.",
            )
            self.sets_entry.focus_set()
            return
        duration_minutes = str(total_seconds // 60)

        use_execution_details = any(
            (
                sets,
                work_seconds,
                rest_seconds,
            )
        )
        
        drill_data = DrillFormData(
            name=name,
            development_block_id=development_block_id,
            technical_focus_id=technical_focus_id,
            technical_focus=selected_focus_name,
            purpose=self.purpose_textbox.get(
                "1.0",
                "end",
            ).strip(),
            duration_minutes=duration_minutes,
            recommended_players=self.players_entry.get().strip()[:30],
            use_execution_details=use_execution_details,
            sets=sets,
            # Reps is retained for older drills even though the current form uses
            # sets and timed work/rest controls.
            reps=self._optional_number_for_save(
                getattr(self.drill, "reps", "") if self.drill else ""
            ),
            work_seconds=work_seconds,
            rest_seconds=rest_seconds,
            equipment=self._textbox_lines(self.equipment_textbox),
            coaching_points=self._textbox_lines(self.coaching_points_textbox),
            progressions=self._textbox_lines(self.progressions_textbox),
            variations=self._textbox_lines(self.variations_textbox),
            notes=self.notes_textbox.get("1.0", "end").strip(),
            id=self.drill.id if self.drill is not None else None,
        )

        if not self.on_save:
            messagebox.showerror(
                "Drill Not Saved",
                "The drill editor is not connected to storage. Please return to the library and try again.",
            )
            return

        try:
            self.on_save(drill_data)
        except Exception as error:
            # Tkinter callback exceptions are otherwise only written to a console,
            # which packaged desktop builds do not display.
            messagebox.showerror(
                "Drill Not Saved",
                f"The drill could not be saved. Your entries are still on this page.\n\n{error}",
            )

    def _cancel(self):
        if self._form_changed() and not messagebox.askyesno(
            "Discard Changes",
            "Discard the changes made to this drill?",
        ):
            return
        if self.on_cancel:
            self.on_cancel()

    def _remember_initial_state(self):
        self._initial_form_state = self._form_state()

    def _form_changed(self):
        return getattr(self, "_initial_form_state", self._form_state()) != self._form_state()

    def _form_state(self):
        """Return the editable form content for change detection."""
        return (
            self.name_entry.get(),
            self.block_menu.get(),
            self.focus_entry.get(),
            self.purpose_textbox.get("1.0", "end").strip(),
            self.players_entry.get(),
            self.sets_entry.get(),
            self.work_minutes_entry.get(),
            self.work_seconds_entry.get(),
            self.rest_minutes_entry.get(),
            self.rest_seconds_entry.get(),
            self.equipment_textbox.get("1.0", "end").strip(),
            self.coaching_points_textbox.get("1.0", "end").strip(),
            self.progressions_textbox.get("1.0", "end").strip(),
            self.variations_textbox.get("1.0", "end").strip(),
            self.notes_textbox.get("1.0", "end").strip(),
        )
