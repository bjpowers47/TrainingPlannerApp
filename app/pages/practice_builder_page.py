"""
Coach's Training Manager
------------------------

Module:
    practice_builder_page.py

Purpose:
    Displays the Practice Builder workspace.
"""

import customtkinter as ctk
from app.constants.development_phases import DEVELOPMENT_PHASES
from app.constants.player_development import DEVELOPMENT_PHASES
from app.constants.player_development import get_display_name

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
        self.grid_rowconfigure(3, weight=1)

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

        self.summary_label = ctk.CTkLabel(
            self,
            text="Practice Summary",
            font=("Segoe UI", 18, "bold"),
        )
        self.summary_label.grid(
            row=1,
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
            row=2,
            column=0,
            sticky="w",
            padx=30,
            pady=(0, 15),
        )

        self.phase_frame = ctk.CTkScrollableFrame(self)
        self.phase_frame.grid(
            row=3,
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

        for widget in self.winfo_children():
            widget.destroy()

        self.build_ui()
        self.refresh_summary() 