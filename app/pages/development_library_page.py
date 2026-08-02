"""
Coach's Training Manager
------------------------

Module:
    development_library_page.py

Purpose:
    Displays the Development Library for browsing and selecting drills.
"""

import customtkinter as ctk
from app.models.player_development import DEVELOPMENT_BLOCKS

class DevelopmentLibraryPage(ctk.CTkFrame):
    """Development Library page."""

    def __init__(
        self,
        parent,
        development_library_service,
        selected_block=None,
        add_to_practice_callback=None,
        cancel_callback=None,
    ):
        super().__init__(parent)

        self.service = development_library_service
        self.selected_block = selected_block
        self.add_to_practice_callback = add_to_practice_callback
        self.cancel_callback = cancel_callback

        self.selected_block_id = None
        self.selected_drill_ids = set()
        self.current_drill = None
        self.practice_builder_mode = (
            selected_block is not None
            and add_to_practice_callback is not None
        )

        self.build_ui()
        self.load_blocks()
        self.configure_page_mode()


    def build_ui(self):
        """Create the Development Library interface."""

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self.build_titles()
        self.build_frames()
        self.build_drill_list()
        
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
    def build_drill_list(self):
        """Build the drill browsing controls."""

        ctk.CTkLabel(
            self.blocks_frame,
            text="Practice Blocks",
            font=("Segoe UI", 18, "bold"),
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 15),
        )

        self.drills_title = ctk.CTkLabel(
            self.drills_container,
            text="Drills",
            font=("Segoe UI", 18, "bold"),
        )
        self.drills_title.grid(
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
        self.cancel_button = ctk.CTkButton(
            self,
            text="Cancel",
            command=self.cancel_selection,
            fg_color="gray",
        )

        self.cancel_button.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 10),
        )
    def build_frames(self):
        """Build the main page containers."""

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
    def build_titles(self):
        
        """Build the page titles."""

        self.page_title = ctk.CTkLabel(
            self,
            text="Development Library",
            font=("Segoe UI", 28, "bold"),
        )

        self.page_title.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=10,
            pady=(10, 5),
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
    def configure_page_mode(self):
        """Configure the page for browsing or selecting practice drills."""

        if self.practice_builder_mode:
            self.configure_practice_builder_mode()
        else:
            self.configure_browse_mode()    
    def show_welcome_message(self):
        """Display the opening message."""

        self.details_box.delete("1.0", "end")

        if self.selected_block:
            self.details_box.insert(
                "end",
                f"{self.selected_block} Drills\n\n"
                "Select one or more drills.",
            )
        else:
            self.details_box.insert(
                "end",
                "Development Library\n\n"
                "Select a Practice Block.",
            )
    def load_blocks(self):
        """Create the Development Block buttons."""

        for block in DEVELOPMENT_BLOCKS:
            button = ctk.CTkButton(
                self.blocks_frame,
                text=block.name,
                command=lambda selected_block=block: self.show_drills(selected_block),
            )
            button.pack(fill="x", padx=5, pady=5)
    def show_drills(self, block):
        """Display drills for the selected Practice Block."""

        if self.selected_block_id != block.id:
            self.selected_drill_ids.clear()

        self.selected_block = block.name
        self.selected_block_id = block.id

        self.drills_title.configure(
            text=f"{block.name} Drills",
        )

        if self.practice_builder_mode:
            self.page_title.configure(
                text=f"Select {block.name} Drills",
            )

            self.submit_button.configure(
                text=f"Add Selected {block.name} Drills to Practice",
            )

        for widget in self.drills_frame.winfo_children():
            widget.destroy()

        drills = self.service.get_drills_for_block(block.id)

        if not drills:
            label = ctk.CTkLabel(
                self.drills_frame,
                text="No drills found for this Practice Block.",
            )
            label.pack(
                anchor="w",
                padx=10,
                pady=10,
            )
            return

        for drill in drills:
            self.build_drill_row(drill)
    def build_drill_row(self, drill):
        """Build one drill row in the drill list."""

        row = ctk.CTkFrame(self.drills_frame)
        row.pack(
            fill="x",
            padx=10,
            pady=4,
        )

        if self.practice_builder_mode:
            checkbox = ctk.CTkCheckBox(
                row,
                text="",
                width=30,
                command=lambda selected_drill=drill: (
                    self.toggle_drill_selection(selected_drill)
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
    def toggle_drill_selection(self, drill):
        """Toggle a drill and display its details in the shared sidebar."""

        if drill.id in self.selected_drill_ids:
            self.selected_drill_ids.remove(drill.id)
        else:
            self.selected_drill_ids.add(drill.id)

        self.show_drill_details(drill)
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
            self.selected_block,
            selected_drills,
        )
    def configure_browse_mode(self):
        """Configure the page for normal Development Library browsing."""

        self.page_title.configure(
            text="Development Library",
        )

        self.drills_title.configure(
            text="Drills",
        )

        # The sidebar library is for browsing, not adding drills.
        self.submit_button.grid_remove()
        self.cancel_button.grid_remove()
        self.show_welcome_message()

    def configure_practice_builder_mode(self):
        """Configure the page as a focused drill picker."""

        block = self.get_selected_block_object()

        if block is None:
            self.show_welcome_message()
            return

        self.page_title.configure(
            text=f"Select {block.name} Drills",
        )

        self.drills_title.configure(
            text=f"{block.name} Drills",
        )

        self.submit_button.configure(
            text=f"Add Selected {block.name} Drills to Practice",
        )

        # Hide the Practice Block buttons.
        self.blocks_frame.grid_remove()

        # Expand the drill list into the space previously used by block buttons.
        self.drills_container.grid_configure(
            column=0,
            columnspan=2,
        )

        self.submit_button.grid_configure(
            column=0,
            columnspan=2,
        )

        self.show_drills(block)

    def cancel_selection(self) -> None:
        """Return to the Practice Builder without adding drills."""

        if self.cancel_callback is not None:
            self.cancel_callback()  

    def get_selected_block_object(self):
        """Return the Development Block matching the selected block name."""

        for block in DEVELOPMENT_BLOCKS:
            if block.name == self.selected_block:
                return block

        return None
