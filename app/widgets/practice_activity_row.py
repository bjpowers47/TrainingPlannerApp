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
        drag_start_callback: Callable | None = None,
        drag_motion_callback: Callable | None = None,
        drop_callback: Callable | None = None,
    ):

        super().__init__(parent)

        self.activity = activity
        self.move_up_callback = move_up_callback
        self.move_down_callback = move_down_callback
        self.remove_callback = remove_callback
        self.activity_changed_callback = activity_changed_callback
        self.drag_start_callback = drag_start_callback
        self.drag_motion_callback = drag_motion_callback
        self.drop_callback = drop_callback
        duration_text = self._format_duration(activity.duration_seconds())
        self.duration_var = self._make_value_var(duration_text)
        self.sets_var = self._make_value_var(activity.sets)
        self.coach_notes_var = self._make_value_var(activity.coach_notes)
        self.work_minutes_var, self.work_seconds_var = self._duration_vars(
            activity.work_seconds
        )
        self.rest_minutes_var, self.rest_seconds_var = self._duration_vars(
            activity.rest_seconds
        )
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
        header_frame.grid_columnconfigure(1, weight=1)

        drag_handle = ctk.CTkLabel(
            header_frame,
            text="|||",
            width=30,
            cursor="fleur",
            text_color=("gray40", "gray70"),
        )
        drag_handle.grid(row=0, column=0, padx=(0, 8))
        if self.drag_start_callback is not None:
            drag_handle.bind("<ButtonPress-1>", self.drag_start_callback)
            drag_handle.bind("<B1-Motion>", self.drag_motion_callback)
            drag_handle.bind("<ButtonRelease-1>", self.drop_callback)

        name_label = ctk.CTkLabel(
            header_frame,
            text=f"• {self.activity.name}",
            font=("Segoe UI", 15, "bold"),
            anchor="w",
        )
        name_label.grid(
            row=0,
            column=1,
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
            column=4,
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
            column=3,
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
            column=2,
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
            suffix="min:sec",
            width=66,
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
        self._build_duration_field(
            execution_frame,
            column=3,
            label="Work",
            minutes_variable=self.work_minutes_var,
            seconds_variable=self.work_seconds_var,
        )
        self._build_duration_field(
            execution_frame,
            column=4,
            label="Rest",
            minutes_variable=self.rest_minutes_var,
            seconds_variable=self.rest_seconds_var,
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

    def _build_duration_field(
        self,
        parent,
        column: int,
        label: str,
        minutes_variable: ctk.StringVar,
        seconds_variable: ctk.StringVar,
    ) -> None:
        """Build separate minute and second entries for a duration."""

        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.grid(row=0, column=column, sticky="w", padx=(0, 14))

        ctk.CTkLabel(
            field_frame, text=label, font=("Segoe UI", 13)
        ).pack(side="left", padx=(0, 5))

        for variable, suffix, width in (
            (minutes_variable, "min", 54),
            (seconds_variable, "sec", 42),
        ):
            ctk.CTkEntry(
                field_frame,
                width=width,
                textvariable=variable,
                justify="center",
            ).pack(side="left")
            ctk.CTkLabel(
                field_frame, text=suffix, font=("Segoe UI", 12)
            ).pack(side="left", padx=(4, 7))

    # ==========================================================
    # Business Logic
    # ==========================================================

    def bind_value_changes(self) -> None:
        """Update the PracticeActivity when an editable entry changes."""

        bindings = (
            (self.sets_var, "sets"),
            (self.coach_notes_var, "coach_notes"),
        )

        for variable, attribute_name in bindings:
            variable.trace_add(
                "write",
                lambda *_args, var=variable, attr=attribute_name: (
                    self.save_value(var, attr)
                ),
            )

        for variable, minutes_var, seconds_var, attribute_name in (
            (
                self.work_minutes_var,
                self.work_minutes_var,
                self.work_seconds_var,
                "work_seconds",
            ),
            (
                self.work_seconds_var,
                self.work_minutes_var,
                self.work_seconds_var,
                "work_seconds",
            ),
            (
                self.rest_minutes_var,
                self.rest_minutes_var,
                self.rest_seconds_var,
                "rest_seconds",
            ),
            (
                self.rest_seconds_var,
                self.rest_minutes_var,
                self.rest_seconds_var,
                "rest_seconds",
            ),
        ):
            variable.trace_add(
                "write",
                lambda *_args, mins=minutes_var, secs=seconds_var, attr=attribute_name: (
                    self.save_duration(mins, secs, attr)
                ),
            )

    def save_duration(
        self,
        minutes_variable: ctk.StringVar,
        seconds_variable: ctk.StringVar,
        attribute_name: str,
    ) -> None:
        """Save valid minute/second components as total seconds."""

        minutes_text = minutes_variable.get().strip()
        seconds_text = seconds_variable.get().strip()
        if not minutes_text and not seconds_text:
            value = None
        else:
            try:
                minutes = int(minutes_text or 0)
                seconds = int(seconds_text or 0)
            except ValueError:
                return
            if minutes < 0 or seconds < 0 or seconds > 59:
                return
            value = minutes * 60 + seconds

        setattr(self.activity, attribute_name, value)
        self.refresh_duration()
        if self.activity_changed_callback is not None:
            self.activity_changed_callback()
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

        setattr(
            self.activity,
            attribute_name,
            value,
        )

        if attribute_name in (
            "sets",
        ):
            self.refresh_duration()

        if self.activity_changed_callback is not None:
            self.activity_changed_callback()
    def refresh_duration(self) -> None:
        """Recalculate and display the activity duration."""

        self.duration_var.set(
            self._format_duration(self.activity.duration_seconds())
        )

    @staticmethod
    def _make_value_var(value: int | None) -> ctk.StringVar:
        """Create a StringVar that displays None as a blank entry."""

        display_value = "" if value is None else str(value)
        return ctk.StringVar(value=display_value)

    @staticmethod
    def _duration_vars(total_seconds: float | None) -> tuple[ctk.StringVar, ctk.StringVar]:
        """Create minute and second variables from a stored duration."""

        if total_seconds is None:
            return ctk.StringVar(value="0"), ctk.StringVar(value="0")
        minutes, seconds = divmod(int(total_seconds), 60)
        return ctk.StringVar(value=str(minutes)), ctk.StringVar(value=str(seconds))

    @staticmethod
    def _format_duration(total_seconds: float) -> str:
        """Format an exact duration for the read-only Time field."""
        minutes, seconds = divmod(int(total_seconds), 60)
        return f"{minutes}:{seconds:02d}"
