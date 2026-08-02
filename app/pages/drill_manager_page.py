import customtkinter as ctk

from app.models.player_development import DEVELOPMENT_BLOCKS


class DrillManagerPage(ctk.CTkFrame):

    def __init__(
        self,
        master,
        drill_service,
        on_new_drill=None,
        on_edit_drill=None,
    ):
        super().__init__(master)

        self.drill_service = drill_service
        self.on_new_drill = on_new_drill
        self.on_edit_drill = on_edit_drill

        self.selected_drill = None

        self.build_ui()

    def _handle_new_drill(self):
        """Open the editor for a new drill."""

        if self.on_new_drill:
            self.on_new_drill()
        else:
            print("No New Drill callback was provided")

    def _select_drill(self, drill):
        """Select a drill in the manager."""

        self.selected_drill = drill
        self.edit_button.configure(state="normal")

    def _handle_edit_drill(self):
        """Open the selected drill in the editor."""

        if self.selected_drill is None:
            return

        if self.on_edit_drill:
            self.on_edit_drill(self.selected_drill)
        else:
            print("No Edit Drill callback was provided")

    def populate(self):
        """Load drills from the service and display them."""

        grouped = self.drill_service.get_drills_by_block()

        for block in DEVELOPMENT_BLOCKS:
            drills = grouped.get(block.id, [])

            block_label = ctk.CTkLabel(
                self.list_frame,
                text=f"{block.icon} {block.name} ({len(drills)})",
                anchor="w",
                font=("Segoe UI", 16, "bold"),
            )
            block_label.pack(
                fill="x",
                padx=10,
                pady=(15, 5),
            )

            if not drills:
                empty = ctk.CTkLabel(
                    self.list_frame,
                    text="No drills yet.",
                    anchor="w",
                    text_color="gray",
                )
                empty.pack(
                    fill="x",
                    padx=30,
                    pady=(0, 8),
                )
                continue

            for drill in drills:
                button = ctk.CTkButton(
                    self.list_frame,
                    text=drill.name,
                    anchor="w",
                    command=lambda selected_drill=drill: (
                        self._select_drill(selected_drill)
                    ),
                )
                button.pack(
                    fill="x",
                    padx=30,
                    pady=2,
                )

    def build_ui(self):
        """Create the Drill Manager interface."""

        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        header.pack(
            fill="x",
            padx=30,
            pady=(25, 5),
        )

        title = ctk.CTkLabel(
            header,
            text="Drill Manager",
            font=("Segoe UI", 28, "bold"),
        )
        title.pack(side="left")

        new_button = ctk.CTkButton(
            header,
            text="+ New Drill",
            command=self._handle_new_drill,
        )
        new_button.pack(side="right")

        self.edit_button = ctk.CTkButton(
            header,
            text="Edit Drill",
            command=self._handle_edit_drill,
            state="disabled",
        )
        self.edit_button.pack(
            side="right",
            padx=(0, 10),
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Manage your coaching drills.",
            font=("Segoe UI", 14),
        )
        subtitle.pack(
            anchor="w",
            padx=30,
            pady=(0, 10),
        )

        search = ctk.CTkEntry(
            self,
            placeholder_text="Search drills...",
        )
        search.pack(
            fill="x",
            padx=30,
            pady=(10, 10),
        )

        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 20),
        )

        self.populate()