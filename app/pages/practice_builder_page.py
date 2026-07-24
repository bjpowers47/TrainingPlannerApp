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
    DEVELOPMENT_PHASES,
    get_display_name,
)
from app.models.player_development import get_display_name

class PracticeBuilderPage(ctk.CTkFrame):
    """Early Practice Builder page."""

    def __init__(self, parent, practice, open_library_callback):
        super().__init__(parent)

        self.practice = practice

        self.open_library_callback = open_library_callback

        self.phases = [
            f"{phase.icon} {phase.name}"
            for phase in DEVELOPMENT_PHASES
        ]

        self.build_ui()
        self.refresh_summary()

    def build_ui(self):
        """Create the Practice Builder interface."""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Practice Builder",
            font=("Segoe UI", 28, "bold"),
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=15,
        )
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
            sticky="w",
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

        self.name_entry.insert(
            0,
            self.practice.name,
        )
        ctk.CTkLabel(
            info_frame,
            text="Practice Date:",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=8,
        )

        self.date_entry = ctk.CTkEntry(info_frame)

        self.date_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=10,
        )

        self.date_entry.insert(
            0,
            self.practice.practice_date,
        )
        ctk.CTkLabel(
            info_frame,
            text="Team:",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=10,
            pady=8,
        )

        self.team_entry = ctk.CTkEntry(info_frame)

        self.team_entry.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
        )

        self.team_entry.insert(
            0,
            self.practice.team_name,
        )
        ctk.CTkLabel(
            info_frame,
            text="Objective:",
        ).grid(
            row=3,
            column=0,
            sticky="nw",
            padx=10,
            pady=8,
        )

        self.objective_text = ctk.CTkTextbox(
            info_frame,
            height=90,
        )

        self.objective_text.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=10,
            pady=8,
        )

        self.objective_text.insert(
            "1.0",
            self.practice.objective,
        )

        self.summary_label = ctk.CTkLabel(
            self,
            text="Practice Summary",
            font=("Segoe UI", 18, "bold"),
        )
        self.summary_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
        )

        self.summary_text = ctk.CTkLabel(
            self,
            text="",
            justify="left",
            font=("Segoe UI", 14),
        )
        self.summary_text.grid(
            row=3,
            column=0,
            sticky="w",
            padx=30,
            pady=(0, 15),
        )

        self.phase_frame = ctk.CTkScrollableFrame(self)
        self.phase_frame.grid(
            row=4,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10,
        )


        for phase in self.practice.get_phase_names():
            section = ctk.CTkFrame(self.phase_frame)
            section.pack(
                fill="x",
                padx=10,
                pady=8,
            )

            label = ctk.CTkLabel(
                section,
                text=get_display_name(phase),
                font=("Segoe UI", 22, "bold"),
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

            activities = self.practice.get_activities(phase)

            if activities:
                for activity in activities:
                    activity_row = ctk.CTkFrame(
                        section,
                        fg_color="transparent",
                    )
                    activity_row.pack(
                        fill="x",
                        padx=25,
                        pady=2,
                    )

                    activity_label = ctk.CTkLabel(
                        activity_row,
                        text=f"• {activity.name}",
                        font=("Segoe UI", 14),
                    )
                    activity_label.pack(
                        side="left",
                        anchor="w",
                    )
                    move_up_button = ctk.CTkButton(
                        activity_row,
                        text="▲",
                        width=32,
                        command=lambda selected_phase=phase, selected_activity=activity: (
                            self.move_activity_up(
                                selected_phase,
                                selected_activity,
                            )
                        ),
                    )
                    move_up_button.pack(
                        side="right",
                        padx=(5, 0),
                    )

                    move_down_button = ctk.CTkButton(
                        activity_row,
                        text="▼",
                        width=32,
                        command=lambda selected_phase=phase, selected_activity=activity: (
                            self.move_activity_down(
                                selected_phase,
                                selected_activity,
                            )
                        ),
                    )
                    move_down_button.pack(
                        side="right",
                        padx=(5, 0),
                    )

                    remove_button = ctk.CTkButton(
                        activity_row,
                        text="✕",
                        width=32,
                        command=lambda selected_phase=phase, selected_activity=activity: (
                            self.remove_activity(
                                selected_phase,
                                selected_activity,
                            )
                        ),
                    )
                    remove_button.pack(
                        side="right",
                        padx=(10, 0),
                    )
            else:
                placeholder = ctk.CTkLabel(
                    section,
                    text="No activities selected yet.",
                    font=("Segoe UI", 14),
                )
                placeholder.pack(
                    anchor="w",
                    padx=25,
                    pady=(0, 6),
                )

            browse_button = ctk.CTkButton(
                section,
                text=f"Browse {phase} Drills",
                command=lambda selected_phase=phase: (
                    self.browse_library(selected_phase)
                ),
            )
            browse_button.pack(
                anchor="w",
                padx=25,
                pady=(8, 12),
            )
            
    def refresh_summary(self):
        """Update the Practice Summary."""

        activity_count = self.practice.activity_count()
        total_minutes = self.practice.total_duration()

        self.summary_text.configure(
            text=(
                f"Activities: {activity_count}\n"
                f"Estimated Time: {total_minutes} minutes"
            )
        )
    def browse_library(self, phase):
        """Open the Development Library for the selected phase."""

        self.update_practice_information()

        self.open_library_callback(phase)
    def remove_activity(self, phase, activity):
        """Remove an activity and refresh the Practice Builder."""

        self.practice.remove_activity(
            phase,
            activity,
        )
        

        self.refresh_page()
    def refresh_page(self):
        """Rebuild the page from the current Practice model."""

        self.update_practice_information()

        for widget in self.winfo_children():
            widget.destroy()

        self.build_ui()
        self.refresh_summary()
    def move_activity_up(self, phase, activity):
        """Move an activity one position earlier within its phase."""

        activities = self.practice.activities.get(phase, [])

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


    def move_activity_down(self, phase, activity):
        """Move an activity one position later within its phase."""

        activities = self.practice.activities.get(phase, [])

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