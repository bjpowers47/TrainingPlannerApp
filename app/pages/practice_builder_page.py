"""
Coach's Training Manager
------------------------

Module:
    practice_builder_page.py

Purpose:
    Displays the Practice Builder workspace.
"""

import customtkinter as ctk


class PracticeBuilderPage(ctk.CTkFrame):
    """Early Practice Builder page."""

    def __init__(self, parent, practice, open_library_callback):
        super().__init__(parent)

        self.practice = practice

        self.open_library_callback = open_library_callback

        self.phases = [
            "⚽ Ball Mastery",
            "🎯 Movement",
            "🥇 1v1",
            "👥 Small Group",
            "🥅 Match Application",
            "📝 Review",
        ]

        self.build_ui()
        self.refresh_summary()

    def build_ui(self):
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

        for phase in self.phases:
            section = ctk.CTkFrame(self.phase_frame)
            section.pack(
                fill="x",
                padx=10,
                pady=8,
            )

            label = ctk.CTkLabel(
                section,
                text=phase,
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

            placeholder = ctk.CTkLabel(
                section,
                text="No activities selected yet.",
                font=("Segoe UI", 14),
            )
            placeholder.pack(anchor="w", padx=25, pady=(0, 6))

            browse_button = ctk.CTkButton(
                section,
                text=f"Browse {phase}",
                command=lambda selected_phase=phase: self.browse_library(selected_phase),
            )

            browse_button.pack(anchor="w", padx=25, pady=(0, 12))

    def refresh_summary(self):
        """Update the displayed Practice Summary."""

        activity_count = self.practice.activity_count()

        self.summary_text.configure(
            text=(
                f"Activities: {activity_count}\n"
                "Estimated Time: Coming Soon"
            )
        )

    def browse_library(self, phase):
        """Open the Development Library for the selected phase."""

        self.open_library_callback(phase)