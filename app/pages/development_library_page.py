"""
Coach's Training Manager
------------------------

Module:
    development_library_page.py

Purpose:
    Displays the Development Library for browsing and selecting drills.
"""

import customtkinter as ctk
from app.constants.player_development import DEVELOPMENT_PHASES


class DevelopmentLibraryPage(ctk.CTkFrame):
    """Development Library page."""

    def __init__(
        self,
        parent,
        development_library_service,
        selected_phase=None,
        add_to_practice_callback=None,
    ):
        super().__init__(parent)

        self.service = development_library_service
        self.selected_phase = selected_phase
        self.add_to_practice_callback = add_to_practice_callback

        self.selected_block_id = None
        self.selected_drill_ids = set()

        self.build_ui()
        self.load_blocks()
        self.show_welcome_message()

    def build_ui(self):
        """Create the Development Library interface."""

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Development Library",
            font=("Segoe UI", 28, "bold"),
        )
        title.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=20,
            pady=15,
        )

        details_title = ctk.CTkLabel(
            self,
            text="Drill Details",
            font=("Segoe UI", 18, "bold"),
        )
        details_title.grid(
            row=0,
            column=2,
            sticky="w",
            padx=20,
        )

        self.blocks_frame = ctk.CTkFrame(
            self,
            width=220,
        )
        self.blocks_frame.grid(
            row=1,
            column=0,
            sticky="nsw",
            padx=10,
            pady=10,
        )

        self.drills_container = ctk.CTkFrame(self)
        self.drills_container.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10,
        )
        self.drills_container.grid_columnconfigure(0, weight=1)
        self.drills_container.grid_rowconfigure(1, weight=1)

        self.details_box = ctk.CTkTextbox(
            self,
            wrap="word",
        )
        self.details_box.grid(
            row=1,
            column=2,
            rowspan=2,
            sticky="nsew",
            padx=10,
            pady=10,
        )

        ctk.CTkLabel(
            self.blocks_frame,
            text="Practice Phases",
            font=("Segoe UI", 18, "bold"),
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 15),
        )

        ctk.CTkLabel(
            self.drills_container,
            text="Drills",
            font=("Segoe UI", 18, "bold"),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=(10, 15),
        )

        self.drills_frame = ctk.CTkScrollableFrame(
            self.drills_container,
            width=320,
        )
        self.drills_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10),
        )

        self.submit_button = ctk.CTkButton(
            self,
            text="Add Selected Drills to Practice",
            command=self.submit_selected_drills,
        )
        self.submit_button.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=10,
            pady=(0, 10),
        )

    def show_welcome_message(self):
        """Display the opening message."""

        self.details_box.delete("1.0", "end")

        if self.selected_phase:
            self.details_box.insert(
                "end",
                f"{self.selected_phase} Drills\n\n"
                "Select one or more drills.",
            )
        else:
            self.details_box.insert(
                "end",
                "Development Library\n\n"
                "Select a Practice Phase.",
            )

    def load_blocks(self):
        """Create the Development Phase buttons."""

        for phase in DEVELOPMENT_PHASES:
            button = ctk.CTkButton(
                self.blocks_frame,
                text=f"{phase.icon} {phase.name}",
                command=lambda selected_id=phase.id: self.show_drills(
                    selected_id
                ),
            )
            button.pack(
                fill="x",
                padx=10,
                pady=6,
            )
    def show_drills(self, block_id):
        """Display drills for the selected Practice Phase."""

        self.selected_block_id = block_id

        for widget in self.drills_frame.winfo_children():
            widget.destroy()

        drills = self.service.get_drills_for_block(block_id)

        if not drills:
            label = ctk.CTkLabel(
                self.drills_frame,
                text="No drills found for this Practice Phase.",
            )
            label.pack(
                anchor="w",
                padx=10,
                pady=10,
            )
            return

        for drill in drills:
            row = ctk.CTkFrame(self.drills_frame)
            row.pack(
                fill="x",
                padx=10,
                pady=4,
            )

            checkbox = ctk.CTkCheckBox(
                row,
                text="",
                width=30,
                command=lambda drill_id=drill.id: (
                    self.toggle_drill_selection(drill_id)
                ),
            )
            checkbox.pack(
                side="left",
                padx=5,
            )

            button = ctk.CTkButton(
                row,
                text=drill.name,
                command=lambda selected_drill=drill: (
                    self.show_drill_details(selected_drill)
                ),
            )
            button.pack(
                side="left",
                fill="x",
                expand=True,
                padx=5,
            )

    def toggle_drill_selection(self, drill_id):
        """Add or remove a drill from the current selection."""

        if drill_id in self.selected_drill_ids:
            self.selected_drill_ids.remove(drill_id)
        else:
            self.selected_drill_ids.add(drill_id)

    def show_drill_details(self, drill):
        """Display the selected drill's information."""

        self.details_box.delete("1.0", "end")

        self.details_box.insert("end", f"{drill.name}\n")
        self.details_box.insert(
            "end",
            "\n────────────────────────────\n\n",
        )

        self.details_box.insert("end", "Purpose\n")
        self.details_box.insert(
            "end",
            f"{drill.purpose}\n\n",
        )

        self.details_box.insert("end", "Recommended Structure\n")
        self.details_box.insert(
            "end",
            f"Duration: {drill.duration_minutes} minutes\n",
        )
        self.details_box.insert(
            "end",
            f"Players: {drill.recommended_players}\n\n",
        )

        self.details_box.insert("end", "Equipment\n")
        for item in drill.equipment:
            self.details_box.insert(
                "end",
                f"• {item}\n",
            )

        self.details_box.insert("end", "\nCoaching Points\n")
        for point in drill.coaching_points:
            self.details_box.insert(
                "end",
                f"• {point}\n",
            )

        self.details_box.insert("end", "\nProgressions\n")
        for progression in drill.progressions:
            self.details_box.insert(
                "end",
                f"• {progression}\n",
            )

        self.details_box.insert("end", "\nVariations\n")
        for variation in drill.variations:
            self.details_box.insert(
                "end",
                f"• {variation}\n",
            )

        if drill.notes:
            self.details_box.insert("end", "\nNotes\n")
            self.details_box.insert(
                "end",
                drill.notes,
            )

    def submit_selected_drills(self):
        """Add selected drills to the current practice."""

        selected_drills = []

        for drill_id in self.selected_drill_ids:
            drill = self.service.get_drill(drill_id)

            if drill is not None:
                selected_drills.append(drill)

        if not selected_drills:
            self.details_box.delete("1.0", "end")
            self.details_box.insert(
                "end",
                "Select at least one drill before continuing.",
            )
            return

        if self.add_to_practice_callback is None:
            self.details_box.delete("1.0", "end")
            self.details_box.insert(
                "end",
                f"{len(selected_drills)} drill(s) selected.\n\n"
                "Open the library from the Practice Builder "
                "to add them to a practice.",
            )
            return

        self.add_to_practice_callback(
            self.selected_phase,
            selected_drills,
        )