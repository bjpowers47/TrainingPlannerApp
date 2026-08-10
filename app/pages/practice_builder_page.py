"""
Coach's Training Manager
------------------------

Module:
    practice_builder_page.py

Purpose:
    Displays the Practice Builder workspace.
"""

import customtkinter as ctk
from tkinter import messagebox
from app.models.player_development import (
    DEVELOPMENT_BLOCKS,
    get_display_name
)
from app.widgets.practice_activity_row import PracticeActivityRow

class PracticeBuilderPage(ctk.CTkFrame):
    """Build and manage a soccer practice."""

    # ==========================================================
    # Initialization
    # ==========================================================

    def __init__(
        self,
        parent,
        practice,
        open_library_callback,
        export_pdf_callback=None,
        save_practice_callback=None,
        coaches=None,
    ):
        super().__init__(parent)

        self.practice = practice

        self.open_library_callback = open_library_callback
        self.export_pdf_callback = export_pdf_callback
        self.save_practice_callback = save_practice_callback
        self.coaches = coaches or []

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
        ctk.CTkButton(
            title_frame,
            text="Save Practice",
            command=self.save_practice_callback,
        ).grid(row=0, column=1, sticky="e", padx=(0, 10))
        ctk.CTkButton(
            title_frame,
            text="Print",
            command=self.save_as_pdf,
        ).grid(row=0, column=2, sticky="e")

    def save_as_pdf(self):
        """Capture current values and open the print dialog."""
        self.update_practice_information()
        if self.export_pdf_callback is not None:
            self.export_pdf_callback(self.practice)
    def build_block_sections(self):
        self.block_frame = ctk.CTkScrollableFrame(self)
        self.block_frame.grid(
            row=4,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10,
        )

        self.build_warm_up_section()

        for block in self.practice.get_block_names():
            section = ctk.CTkFrame(self.block_frame)
            section.pack(
                fill="x",
                padx=10,
                pady=8,
            )

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
                    )

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

    def build_warm_up_section(self):
        """Build the fixed warm-up section shown before development blocks."""
        section = ctk.CTkFrame(self.block_frame)
        section.pack(fill="x", padx=10, pady=8)

        ctk.CTkLabel(
            section,
            text="Warm Up",
            font=("Segoe UI", 22, "bold"),
            text_color="yellow",
        ).pack(anchor="w", padx=15, pady=(12, 4))

        separator = ctk.CTkFrame(section, height=2)
        separator.pack(fill="x", padx=15, pady=(0, 10))

        duration_frame = ctk.CTkFrame(section, fg_color="transparent")
        duration_frame.pack(anchor="w", padx=25, pady=(0, 12))
        ctk.CTkLabel(duration_frame, text="Warm-up duration:").pack(side="left")

        self.warm_up_duration_var = ctk.StringVar(
            value=str(self.practice.warm_up_minutes)
        )
        self.warm_up_duration_entry = ctk.CTkEntry(
            duration_frame,
            width=60,
            textvariable=self.warm_up_duration_var,
            justify="center",
        )
        self.warm_up_duration_entry.pack(side="left", padx=(8, 6))
        self.warm_up_duration_entry.bind(
            "<KeyRelease>", lambda _event: self.save_warm_up_duration()
        )
        ctk.CTkLabel(duration_frame, text="min").pack(side="left")

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
        column_widths = (150, 80, 100, 90, 100, 220)
        headings = ("Coach", "Activities", "Warm-up", "Planned", "Remaining", "Progress")
        for column, (heading, width) in enumerate(zip(headings, column_widths)):
            self.summary_table.grid_columnconfigure(column, weight=1 if column == 5 else 0)
            ctk.CTkLabel(
                self.summary_table,
                text=heading,
                width=width,
                anchor="w" if column in (0, 5) else "center",
                font=ctk.CTkFont(size=13, weight="bold"),
            ).grid(row=0, column=column, sticky="ew", padx=4, pady=(0, 4))

    def build_summary_progress(self):
        """Build one aligned summary row for each coach."""

        self.coach_progress = {}
        self.coach_summary_values = {}
        for row, coach in enumerate(self.coaches, start=1):
            values = {}
            for column, (key, width) in enumerate((
                ("coach", 150),
                ("activities", 80),
                ("warm_up", 100),
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
            progress_cell.grid(row=row, column=5, sticky="ew", padx=4, pady=3)
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

        self.practice_duration_var = ctk.StringVar(value="90")

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
        self.save_warm_up_duration()

    def save_warm_up_duration(self) -> None:
        """Copy a valid non-negative warm-up duration into the practice."""
        text = self.warm_up_duration_var.get().strip()
        if text == "":
            self.practice.warm_up_minutes = 0
        else:
            try:
                minutes = float(text)
            except ValueError:
                return
            if minutes < 0:
                return
            if minutes * 2 != int(minutes * 2):
                return
            self.practice.warm_up_minutes = minutes
        self.refresh_summary()

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

        for coach in self.coaches:
            assigned = [b for b, names in self.practice.block_coaches.items() if coach in names]
            count = sum(len(self.practice.activities.get(b, [])) for b in assigned)
            minutes = sum(a.duration_minutes() for b in assigned for a in self.practice.activities.get(b, []))
            remaining = target_minutes - self.practice.warm_up_minutes - minutes
            percent = min(100, (minutes + self.practice.warm_up_minutes) / target_minutes * 100) if target_minutes else 0
            self.coach_progress[coach].set(percent / 100)
            values = self.coach_summary_values[coach]
            values["activities"].configure(text=str(count))
            values["warm_up"].configure(text=f"{self.practice.warm_up_minutes:g} min")
            values["planned"].configure(text=f"{minutes:g} min")
            values["remaining"].configure(text=f"{remaining:g} min")
            values["progress"].configure(text=f"{percent:.0f}%")

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

        self.practice.remove_activity(
            block,
            activity,
        )
        

        self.refresh_page()

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

        self.refresh_page()
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

        self.refresh_page()

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
    
