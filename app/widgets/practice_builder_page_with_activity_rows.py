"""
Coach's Training Manager
------------------------

Module:
    practice_builder_page.py

Purpose:
    Displays the Practice Builder workspace.
"""

import customtkinter as ctk
from app.models.player_development import (
    DEVELOPMENT_BLOCKS,
    get_display_name,
)
from app.widgets.practice_activity_row import PracticeActivityRow

class PracticeBuilderPage(ctk.CTkFrame):
    """Build and manage a soccer practice."""

    # ==========================================================
    # Initialization
    # ==========================================================

    def __init__(self, parent, practice, open_library_callback):
        super().__init__(parent)

        self.practice = practice

        self.open_library_callback = open_library_callback

        self.blocks = [
            f"{block.icon} {block.name}"
            for block in DEVELOPMENT_BLOCKS
        ]

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

        self.title_label = ctk.CTkLabel(
            self,
            text="Practice Builder",
            font=("Segoe UI", 28, "bold"),
        )
        self.title_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 10),
        )
    def build_block_sections(self):
        self.block_frame = ctk.CTkScrollableFrame(self)
        self.block_frame.grid(
            row=4,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10,
        )

        for block in self.practice.get_blockPracticeBuilderPagePracticeBuilderPage_names():
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
                        parent=section,
                        activity=activity,
                        move_up_callback=(
                            lambda selected_block=block,
                            selected_activity=activity: self.move_activity_up(
                                selected_block,
                                selected_activity,
                            )
                        ),
                        move_down_callback=(
                            lambda selected_block=block,
                            selected_activity=activity: self.move_activity_down(
                                selected_block,
                                selected_activity,
                            )
                        ),
                        remove_callback=(
                            lambda selected_block=block,
                            selected_activity=activity: self.remove_activity(
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
        """Build the one-line practice summary."""

        self.summary_text = ctk.CTkLabel(
            self.summary_frame,
            text="",
            justify="left",
            anchor="w",
            font=("Segoe UI", 14),
            text_color="pink",
        )
        self.summary_text.grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=(0, 6),
        )
    def build_summary_progress(self):
        """Build the practice-time progress display."""

        ctk.CTkLabel(
            self.summary_frame,
            text="Progress",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=(5, 4),
        )

        self.practice_time_progress = ctk.CTkProgressBar(
            self.summary_frame,
        )
        self.practice_time_progress.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 6),
        )
        self.practice_time_progress.set(0)

        self.practice_time_label = ctk.CTkLabel(
            self.summary_frame,
            text="0 / 90 min planned",
        )
        self.practice_time_label.grid(
            row=4,
            column=0,
            sticky="w",
            padx=10,
            pady=(0, 10),
        )
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
            text="Practice Date:",
        ).grid(
            row=1,
            column=0,
            sticky="e",
            padx=10,
            pady=8,
        )

        self.date_entry = ctk.CTkEntry(
            info_frame,
            width=150,
        )
        self.date_entry.grid(
            row=1,
            column=1,
            sticky="w",
            padx=10,
        )
        self.date_entry.insert(0, self.practice.practice_date)

        ctk.CTkLabel(
            info_frame,
            text="Practice Length:",
        ).grid(
            row=2,
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
            row=2,
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
            text="Team:",
        ).grid(
            row=3,
            column=0,
            sticky="e",
            padx=10,
            pady=8,
        )

        self.team_entry = ctk.CTkEntry(
            info_frame,
            width=150,
        )
        self.team_entry.grid(
            row=3,
            column=1,
            sticky="w",
            padx=10,
        )
        self.team_entry.insert(0, self.practice.team_name)

        ctk.CTkLabel(
            info_frame,
            text="Objective:",
        ).grid(
            row=4,
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
            row=4,
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
    
    def update_practice_information(self):
        """Copy the Practice Information controls into the Practice model."""

        self.practice.name = self.name_entry.get().strip()

        self.practice.practice_date = (
            self.date_entry.get().strip()
        )

        self.practice.team_name = (
            self.team_entry.get().strip()
        )

        self.practice.objective = (
            self.objective_text.get(
                "1.0",
                "end",
            ).strip()
        )

    # ==========================================================
    # Practice Summary
    # ==========================================================
    
    def refresh_summary(self):
        """Update the Practice Summary."""

        activity_count = self.practice.activity_count()
        planned_minutes = self.practice.total_duration()

        try:
            target_minutes = int(self.practice_duration_var.get())
        except ValueError:
            target_minutes = 0

        remaining_minutes = target_minutes - planned_minutes

        summary_text = (
            f"Activities: {activity_count}   |  "
            f"Planned: {planned_minutes} min   |   "
            f"Target: {target_minutes} min   |   "
            f"Remaining: {remaining_minutes} min"
        )

        self.summary_text.configure(
            text=summary_text,
        )

        if target_minutes > 0:
            progress = planned_minutes / target_minutes
        else:
            progress = 0

        display_progress = min(max(progress, 0), 1)

        self.practice_time_progress.set(display_progress)

        self.practice_time_label.configure(
            text=f"{planned_minutes} / {target_minutes} min"
        )          
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
    