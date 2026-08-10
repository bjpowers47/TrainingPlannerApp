"""
Training Planner Ap
------------------------

Module:
    practice_activity_row.py

Purpose:
    Displays and edits one activity within a specific practice.
"""

from collections.abc import Callable

import customtkinter as ctk

from app.models.practice_activity import PracticeActivity


class PracticeActivityRow(ctk.CTkFrame):
    """Display and edit one practice-specific activity."""

    # ==========================================================
    # Initialization
    # ==========================================================

    def __init__(
        self,
        parent,
        activity: PracticeActivity,
        move_up_callback: Callable[[], None],
        move_down_callback: Callable[[], None],
        remove_callback: Callable[[], None],
        activity_changed_callback: Callable[[], None] | None = None,
    ):

        super().__init__(parent)

        self.activity = activity
        self.move_up_callback = move_up_callback
        self.move_down_callback = move_down_callback
        self.remove_callback = remove_callback
        self.activity_changed_callback = activity_changed_callback
        duration = activity.duration_minutes()
        duration_text = (
            str(int(duration))
            if duration.is_integer()
            else f"{duration:.1f}"
        )
        self.duration_var = self._make_value_var(duration_text)
        self.sets_var = self._make_value_var(activity.sets)
        self.coach_notes_var = self._make_value_var(activity.coach_notes)
        self.work_var = self._make_value_var(activity.work_minutes)
        self.rest_var = self._make_value_var(activity.rest_minutes)
        self.print_details_var = ctk.BooleanVar(value=activity.print_details)
        
        self.build_ui()
        self.bind_value_changes()

    # ==========================================================
    # UI Construction
    # ==========================================================

    def build_ui(self) -> None:
        """Create the activity row interface."""

        self.grid_columnconfigure(0, weight=1)

        self.build_header()
        self.build_execution_fields()

    def build_header(self) -> None:
        """Build the activity name and management buttons."""

        header_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(8, 4),
        )
        header_frame.grid_columnconfigure(0, weight=1)

        name_label = ctk.CTkLabel(
            header_frame,
            text=f"• {self.activity.name}",
            font=("Segoe UI", 15, "bold"),
            anchor="w",
        )
        name_label.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        remove_button = ctk.CTkButton(
            header_frame,
            text="✕",
            width=32,
            command=self.remove_callback,
        )
        remove_button.grid(
            row=0,
            column=3,
            padx=(8, 0),
        )

        move_down_button = ctk.CTkButton(
            header_frame,
            text="▼",
            width=32,
            command=self.move_down_callback,
        )
        move_down_button.grid(
            row=0,
            column=2,
            padx=(5, 0),
        )

        move_up_button = ctk.CTkButton(
            header_frame,
            text="▲",
            width=32,
            command=self.move_up_callback,
        )
        move_up_button.grid(
            row=0,
            column=1,
            padx=(5, 0),
        )

    def build_execution_fields(self) -> None:
        """Build the always-visible execution controls."""

        execution_frame = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        execution_frame.grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=(2, 10),
        )

        self._build_value_field(
            execution_frame,
            column=0,
            label="Time",
            variable=self.duration_var,
            suffix="min",
        )
        self._build_value_field(
            execution_frame,
            column=1,
            label="Sets",
            variable=self.sets_var,
        )
        self._build_value_field(
            execution_frame,
            column=2,
            label="Note",
            variable=self.coach_notes_var,
            width=180,
        )
        self._build_value_field(
            execution_frame,
            column=3,
            label="Work",
            variable=self.work_var,
            suffix="min",
        )
        self._build_value_field(
            execution_frame,
            column=4,
            label="Rest",
            variable=self.rest_var,
            suffix="min",
        )
        ctk.CTkCheckBox(
            execution_frame,
            text="Print Details",
            variable=self.print_details_var,
            command=self.save_print_details,
        ).grid(row=0, column=5, sticky="w", padx=(8, 0))

    def save_print_details(self) -> None:
        """Store whether this drill's descriptive details should be printed."""
        self.activity.print_details = self.print_details_var.get()
        if self.activity_changed_callback is not None:
            self.activity_changed_callback()

    def _build_value_field(
        self,
        parent,
        column: int,
        label: str,
        variable: ctk.StringVar,
        suffix: str = "",
        width: int = 54,
    ) -> None:
        """Build one labeled execution entry."""

        field_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )
        field_frame.grid(
            row=0,
            column=column,
            sticky="w",
            padx=(0, 14),
        )

        ctk.CTkLabel(
            field_frame,
            text=label,
            font=("Segoe UI", 13),
        ).pack(
            side="left",
            padx=(0, 5),
        )

        entry = ctk.CTkEntry(
            field_frame,
            width=width,
            textvariable=variable,
            justify="center",
        )
        if label == "Time":
            entry.configure(state="readonly")

        entry.pack(side="left")

        if suffix:
            ctk.CTkLabel(
                field_frame,
                text=suffix,
                font=("Segoe UI", 12),
            ).pack(
                side="left",
                padx=(4, 0),
            )

    # ==========================================================
    # Business Logic
    # ==========================================================

    def bind_value_changes(self) -> None:
        """Update the PracticeActivity when an editable entry changes."""

        bindings = (
            (self.sets_var, "sets"),
            (self.coach_notes_var, "coach_notes"),
            (self.work_var, "work_minutes"),
            (self.rest_var, "rest_minutes"),
        )

        for variable, attribute_name in bindings:
            variable.trace_add(
                "write",
                lambda *_args, var=variable, attr=attribute_name: (
                    self.save_value(var, attr)
                ),
            )
    def save_value(
        self,
        variable: ctk.StringVar,
        attribute_name: str,
    ) -> None:
        """Save an edited execution value to the activity."""

        text = variable.get().strip()

        if attribute_name == "coach_notes":
            value = text[:200]

        else:
            if text == "":
                value = None
            else:
                try:
                    value = float(text)
                except ValueError:
                    return

                if value < 0:
                    return
                if attribute_name in ("work_minutes", "rest_minutes") and value * 2 != int(value * 2):
                    return

        setattr(
            self.activity,
            attribute_name,
            value,
        )

        if attribute_name in (
            "sets",
            "work_minutes",
            "rest_minutes",
        ):
            self.refresh_duration()

        if self.activity_changed_callback is not None:
            self.activity_changed_callback()
    def refresh_duration(self) -> None:
        """Recalculate and display the activity duration."""

        duration = self.activity.duration_minutes()

        duration_text = (
            str(int(duration))
            if duration.is_integer()
            else f"{duration:.1f}"
        )

        self.duration_var.set(duration_text)

    @staticmethod
    def _make_value_var(value: int | None) -> ctk.StringVar:
        """Create a StringVar that displays None as a blank entry."""

        display_value = "" if value is None else str(value)
        return ctk.StringVar(value=display_value)
