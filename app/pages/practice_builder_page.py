"""
Wildcat Training Planner
------------------------

Module:
    practice_builder_page.py

Purpose:
    Displays the Practice Builder workspace.
"""

import customtkinter as ctk
from tkinter import messagebox
from app.models.duration import format_duration, format_signed_duration
from app.models.player_development import (
    get_display_name
)
from app.widgets.practice_activity_row import PracticeActivityRow

class PracticeBuilderPage(ctk.CTkFrame):
    """Build and manage a training practice."""

    # ==========================================================
    # Initialization
    # ==========================================================

    def __init__(
        self,
        parent,
        practice,
        open_library_callback,
        export_pdf_callback=None,
        print_callback=None,
        save_practice_callback=None,
        load_unsaved_callback=None,
        has_unsaved_practice=False,
        coaches=None,
    ):
        super().__init__(parent)

        self.practice = practice

        self.open_library_callback = open_library_callback
        self.export_pdf_callback = export_pdf_callback
        self.print_callback = print_callback
        self.save_practice_callback = save_practice_callback
        self.load_unsaved_callback = load_unsaved_callback
        self.has_unsaved_practice = has_unsaved_practice
        self.coaches = coaches or []
        self._drag_source = None
        self._drag_target_row = None

        self.build_ui()
        self.refresh_summary()

    # ==========================================================
    # UI Construction
    # ==========================================================
    
    def build_ui(self):

        """Create the Practice Builder interface."""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.build_title()
        self.build_practice_information()
        self.build_summary()
        self.build_block_sections()

        self.refresh_summary()
        
    def build_title(self):
        """Build the Practice Builder title."""

        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(0, weight=1)
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="Practice Builder",
            font=("Segoe UI", 28, "bold"),
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        self.load_unsaved_button = ctk.CTkButton(
            title_frame,
            text="Load Unsaved Practice",
            command=self.load_unsaved_callback,
            fg_color="#9a6700",
            hover_color="#7a5200",
        )
        self.load_unsaved_button.grid(row=0, column=1, sticky="e", padx=(0, 10))
        if not self.has_unsaved_practice:
            self.load_unsaved_button.grid_remove()
        ctk.CTkButton(
            title_frame,
            text="Save Practice",
            command=self.save_practice_callback,
        ).grid(row=0, column=2, sticky="e", padx=(0, 10))
        ctk.CTkButton(
            title_frame,
            text="Export PDF",
            command=self.export_pdf,
        ).grid(row=0, column=3, sticky="e", padx=(0, 10))
        ctk.CTkButton(
            title_frame,
            text="Print",
            command=self.print_practice,
        ).grid(row=0, column=4, sticky="e")

    def show_load_unsaved_button(self):
        """Offer recovery after an autosave becomes available."""
        self.has_unsaved_practice = True
        self.load_unsaved_button.grid()

    def hide_load_unsaved_button(self):
        """Hide recovery when no separate autosave needs loading."""
        self.has_unsaved_practice = False
        self.load_unsaved_button.grid_remove()

    def export_pdf(self):
        """Capture current values and open the PDF save dialog."""
        self.update_practice_information()
        if self.export_pdf_callback is not None:
            self.export_pdf_callback(self.practice)

    def print_practice(self):
        """Capture current values and open the system print dialog."""
        self.update_practice_information()
        if self.print_callback is not None:
            self.print_callback(self.practice)
    def build_block_sections(self):
        self.block_frame = ctk.CTkScrollableFrame(self)
        self.block_frame.grid(
            row=4,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10,
        )

        self.block_sections = {}

        for block in self.practice.get_block_names():
            self._build_block_section(block)

    def _build_block_section(self, block, before=None):
            """Build one activity block so it can be refreshed independently."""
            section = ctk.CTkFrame(self.block_frame)
            pack_options = {"fill": "x", "padx": 10, "pady": 8}
            if before is not None:
                pack_options["before"] = before
            section.pack(**pack_options)
            self.block_sections[block] = section

            label = ctk.CTkLabel(
                section,
                text=get_display_name(block),
                font=("Segoe UI", 22, "bold"),
                text_color="yellow",
            )
            label.pack(
                anchor="w",
                padx=15,
                pady=(12, 4),
            )
            coach_frame = ctk.CTkFrame(section, fg_color="transparent")
            coach_frame.pack(anchor="w", padx=25, pady=4)
            ctk.CTkLabel(coach_frame, text="Coaches:").pack(side="left", padx=(0, 8))
            for coach in self.coaches:
                var = ctk.BooleanVar(value=coach in self.practice.block_coaches.get(block, []))
                ctk.CTkCheckBox(coach_frame, text=coach, variable=var,
                    command=lambda b=block, c=coach, v=var: self._assign_coach(b, c, v.get())).pack(side="left", padx=4)

            separator = ctk.CTkFrame(
                section,
                height=2,
            )
            separator.pack(
                fill="x",
                padx=15,
                pady=(0, 10),
            )

            activities = self.practice.get_activities(block)

            if activities:
                for activity in activities:
                    activity_row = PracticeActivityRow(
                        section,
                        activity=activity,
                        move_up_callback=lambda selected_block=block, selected_activity=activity: (
                            self.move_activity_up(
                                selected_block,
                                selected_activity,
                            )
                        ),
                        move_down_callback=lambda selected_block=block, selected_activity=activity: (
                            self.move_activity_down(
                                selected_block,
                                selected_activity,
                            )
                        ),
                        remove_callback=lambda selected_block=block, selected_activity=activity: (
                            self.remove_activity(
                                selected_block,
                                selected_activity,
                            )
                        ),
                        activity_changed_callback=self.refresh_summary,
                        drag_start_callback=lambda event, selected_block=block, selected_activity=activity: (
                            self._start_activity_drag(event, selected_block, selected_activity)
                        ),
                        drag_motion_callback=self._drag_activity,
                        drop_callback=self._drop_activity,
                    )

                    activity_row._practice_block = block
                    activity_row._practice_activity = activity

                    activity_row.pack(
                        fill="x",
                        padx=25,
                        pady=4,
                    )
            else:
                placeholder = ctk.CTkLabel(
                    section,
                    text="No activities selected yet.",
                    font=("Segoe UI", 14),
                    text_color="red",
                )
                placeholder.pack(
                    anchor="w",
                    padx=25,
                    pady=(0, 6),
                )

            browse_button = ctk.CTkButton(
                section,
                text=f"Browse {block} Drills",
                command=lambda selected_block=block: (
                    self.browse_library(selected_block)
                ),
            )
            browse_button.pack(
                anchor="w",
                padx=25,
                pady=(8, 12),
            )

    def refresh_block(self, block):
        """Rebuild only the changed block and retain the rest of the page."""
        section = self.block_sections.get(block)
        if section is None:
            return
        block_names = self.practice.get_block_names()
        block_index = block_names.index(block)
        next_section = next(
            (
                self.block_sections[name]
                for name in block_names[block_index + 1:]
                if name in self.block_sections
            ),
            None,
        )
        section.destroy()
        self._build_block_section(block, before=next_section)
        self.refresh_summary()

    def build_summary(self):
        """Build the complete Practice Summary section."""

        self.build_summary_frame()
        self.build_summary_header()
        self.build_summary_details()
        self.build_summary_progress()
    def build_summary_frame(self):
        """Create the frame that contains the Practice Summary."""

        self.summary_frame = ctk.CTkFrame(self)
        self.summary_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15),
        )
        
        self.summary_frame.grid_columnconfigure(0, weight=1) 
    def build_summary_header(self):
        """Build the Practice Summary heading."""

        self.summary_label = ctk.CTkLabel(
            self.summary_frame,
            text="Practice Summary",
            font=("Segoe UI", 18, "bold"),
        )
        self.summary_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 5),
        )

    def build_summary_details(self):
        """Build the coach summary table and column headings."""

        self.summary_table = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
        self.summary_table.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 6),
        )
        column_widths = (150, 80, 90, 100, 220)
        headings = ("Coach", "Activities", "Planned", "Remaining", "Progress")
        for column, (heading, width) in enumerate(zip(headings, column_widths)):
            self.summary_table.grid_columnconfigure(column, weight=1 if column == 4 else 0)
            ctk.CTkLabel(
                self.summary_table,
                text=heading,
                width=width,
                anchor="w" if column in (0, 4) else "center",
                font=ctk.CTkFont(size=13, weight="bold"),
            ).grid(row=0, column=column, sticky="ew", padx=4, pady=(0, 4))

    def build_summary_progress(self):
        """Build one aligned summary row for each coach."""

        self.coach_progress = {}
        self.coach_summary_values = {}
        for row, coach in enumerate([*self.coaches, "Unassigned"], start=1):
            values = {}
            for column, (key, width) in enumerate((
                ("coach", 150),
                ("activities", 80),
                ("planned", 90),
                ("remaining", 100),
            )):
                label = ctk.CTkLabel(
                    self.summary_table,
                    text=coach if key == "coach" else "",
                    width=width,
                    anchor="w" if key == "coach" else "center",
                )
                label.grid(row=row, column=column, sticky="ew", padx=4, pady=3)
                values[key] = label

            progress_cell = ctk.CTkFrame(self.summary_table, fg_color="transparent")
            progress_cell.grid(row=row, column=4, sticky="ew", padx=4, pady=3)
            progress_cell.grid_columnconfigure(0, weight=1)
            bar = ctk.CTkProgressBar(progress_cell)
            bar.grid(row=0, column=0, sticky="ew", padx=(0, 8))
            bar.set(0)
            progress_label = ctk.CTkLabel(progress_cell, text="0%", width=45, anchor="e")
            progress_label.grid(row=0, column=1)
            values["progress"] = progress_label
            self.coach_summary_values[coach] = values
            self.coach_progress[coach] = bar

    def build_practice_information(self):
        """Build the editable Practice Information controls."""

        info_frame = ctk.CTkFrame(self)
        info_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 10),
        )

        info_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            info_frame,
            text="Practice Name:",
        ).grid(
            row=0,
            column=0,
            sticky="e",
            padx=10,
            pady=8,
        )

        self.name_entry = ctk.CTkEntry(info_frame)
        self.name_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=10,
        )
        self.name_entry.insert(0, self.practice.name)

        ctk.CTkLabel(
            info_frame,
            text="Practice Length:",
        ).grid(
            row=1,
            column=0,
            sticky="e",
            padx=10,
            pady=8,
        )

        self.practice_duration_var = ctk.StringVar(value=f"{self.practice.target_minutes:g}")

        duration_frame = ctk.CTkFrame(
            info_frame,
            fg_color="transparent",
        )
        duration_frame.grid(
            row=1,
            column=1,
            sticky="w",
            padx=10,
            pady=8,
        )

        self.practice_duration_entry = ctk.CTkEntry(
            duration_frame,
            width=60,
            textvariable=self.practice_duration_var,
        )
        self.practice_duration_entry.pack(side="left")

        self.practice_duration_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_summary(),
        )

        ctk.CTkLabel(
            duration_frame,
            text="min",
        ).pack(
            side="left",
            padx=(6, 0),
        )
        self.practice_duration_error = ctk.CTkLabel(
            duration_frame, text="", text_color="#ff8a80"
        )
        self.practice_duration_error.pack(side="left", padx=(10, 0))

        ctk.CTkLabel(
            info_frame,
            text="Objective:",
        ).grid(
            row=2,
            column=0,
            sticky="ne",
            padx=10,
            pady=8,
        )

        self.objective_text = ctk.CTkTextbox(
            info_frame,
            height=90,
        )
        self.objective_text.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=8,
        )
        self.objective_text.insert(
            "1.0",
            self.practice.objective,
        )   

    # ==========================================================
    # Navigation
    # ==========================================================
    
    def browse_library(self, block):
            
        """Open the Development Library for the selected block."""

        self.update_practice_information()

        self.open_library_callback(block)
    # ==========================================================
    # Practice Information
    # ==========================================================
    
    def update_practice_information(self) -> None:
        """Copy the Practice Information controls into the Practice model."""

        practice_name = self.name_entry.get().strip()
        self.practice.name = practice_name

        self.practice.objective = (
            self.objective_text.get(
                "1.0",
                "end",
            ).strip()
        )
        try:
            duration = float(self.practice_duration_var.get())
            if duration > 0:
                self.practice.target_minutes = duration
        except ValueError:
            pass

    def validate_practice_name(self) -> bool:
        """Require a name before a practice can be saved."""

        if self.practice.name:
            return True

        messagebox.showwarning(
            "Practice Name Required",
            "Enter a practice name before saving this practice.",
        )
        self.name_entry.focus_set()
        return False

    # ==========================================================
    # Practice Summary
    # ==========================================================
    
    def refresh_summary(self):
        """Update the Practice Summary."""

        try:
            target_minutes = float(self.practice_duration_var.get())
        except ValueError:
            target_minutes = 0
        error = "" if target_minutes > 0 else "Enter a duration greater than zero"
        if hasattr(self, "practice_duration_error"):
            self.practice_duration_error.configure(text=error)

        for coach in [*self.coaches, "Unassigned"]:
            assigned = (
                self.practice.unassigned_blocks()
                if coach == "Unassigned"
                else [b for b, names in self.practice.block_coaches.items() if coach in names]
            )
            count = sum(len(self.practice.activities.get(b, [])) for b in assigned)
            planned_seconds = sum(
                round(a.duration_minutes() * 60)
                for b in assigned
                for a in self.practice.activities.get(b, [])
            )
            target_seconds = round(target_minutes * 60)
            remaining_seconds = target_seconds - planned_seconds
            raw_percent = (
                planned_seconds / target_seconds * 100
                if target_seconds
                else 0
            )
            self.coach_progress[coach].set(min(100, raw_percent) / 100)
            values = self.coach_summary_values[coach]
            values["activities"].configure(text=str(count))
            values["planned"].configure(text=format_duration(planned_seconds))
            values["remaining"].configure(
                text=format_signed_duration(remaining_seconds),
                text_color="#ff8a80" if remaining_seconds < 0 else ("gray10", "gray90"),
            )
            values["progress"].configure(
                text=f"{raw_percent:.0f}%" + (" over" if raw_percent > 100 else ""),
                text_color="#ff8a80" if raw_percent > 100 else ("gray10", "gray90"),
            )

    def _assign_coach(self, block, coach, selected):
        names = self.practice.block_coaches.setdefault(block, [])
        if selected and coach not in names:
            names.append(coach)
        elif not selected and coach in names:
            names.remove(coach)
        if block not in self.practice.selected_blocks:
            self.practice.selected_blocks.append(block)
        self.refresh_summary()

    # ==========================================================
    # Activity Management
    # ==========================================================
    
    def remove_activity(self, block, activity):
        """Remove an activity and refresh the Practice Builder."""

        if not messagebox.askyesno(
            "Remove Activity",
            f'Remove "{activity.name}" from this practice?\n\nThe drill will remain in the Development Library.',
        ):
            return

        self.practice.remove_activity(
            block,
            activity,
        )
        

        self.refresh_block(block)

    def move_activity_up(self, block, activity):
        """Move an activity one position earlier within its block."""

        activities = self.practice.activities.get(block, [])

        try:
            current_index = activities.index(activity)
        except ValueError:
            return

        if current_index == 0:
            return

        activities[current_index - 1], activities[current_index] = (
            activities[current_index],
            activities[current_index - 1],
        )

        self.refresh_block(block)

    def move_activity_down(self, block, activity):
        """Move an activity one position later within its block."""

        activities = self.practice.activities.get(block, [])

        try:
            current_index = activities.index(activity)
        except ValueError:
            return

        if current_index >= len(activities) - 1:
            return

        activities[current_index + 1], activities[current_index] = (
            activities[current_index],
            activities[current_index + 1],
        )

        self.refresh_block(block)

    def _start_activity_drag(self, _event, block, activity):
        """Remember the selected activity when its drag handle is pressed."""
        self._drag_source = (block, activity)

    def _activity_row_at_pointer(self, event):
        """Return the activity row currently beneath the pointer."""
        widget = self.winfo_containing(event.x_root, event.y_root)
        while widget is not None and widget != self.block_frame:
            if hasattr(widget, "_practice_activity"):
                return widget
            widget = getattr(widget, "master", None)
        return None

    def _drag_activity(self, event):
        """Highlight a valid destination row during an activity drag."""
        target = self._activity_row_at_pointer(event)
        source_block = self._drag_source[0] if self._drag_source else None
        if target is not None and target._practice_block != source_block:
            target = None
        if target is self._drag_target_row:
            return
        if self._drag_target_row is not None:
            self._drag_target_row.configure(fg_color=("gray86", "gray17"))
        self._drag_target_row = target
        if target is not None:
            target.configure(fg_color=("gray75", "gray30"))

    def _drop_activity(self, event):
        """Move the dragged activity to the row where it was released."""
        target = self._activity_row_at_pointer(event)
        source = self._drag_source
        self._drag_source = None
        if self._drag_target_row is not None:
            self._drag_target_row.configure(fg_color=("gray86", "gray17"))
        self._drag_target_row = None
        if source is None or target is None:
            return
        block, activity = source
        if target._practice_block != block:
            return
        if self.practice.reorder_activity(block, activity, target._practice_activity):
            self.refresh_block(block)

    # ==========================================================
    # Page Refresh
    # ==========================================================
    
    def refresh_page(self):
        """Rebuild the page from the current Practice model."""

        self.update_practice_information()

        for widget in self.winfo_children():
            widget.destroy()

        self.build_ui()
        self.refresh_summary()
    
