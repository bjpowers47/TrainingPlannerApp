import customtkinter as ctk
from app.models.player_development import get_phase_by_id
from app.models.player_development import DEVELOPMENT_PHASES

class DrillManagerPage(ctk.CTkFrame):

    def __init__(
        self,
        master,
        drill_service,
        on_new_drill=None,
    ):
        super().__init__(master)

        self.drill_service = drill_service
        self.on_new_drill = on_new_drill

        self.build_ui()
    def _handle_new_drill(self):

        if self.on_new_drill:
            self.on_new_drill()
        else:
            print("No New Drill callback was provided")
    def populate(self):
        """Load drills from the service and display them."""

        grouped = self.drill_service.get_drills_by_phase()

        for phase in DEVELOPMENT_PHASES:

            drills = grouped.get(phase.id, [])

            phase_label = ctk.CTkLabel(
                self.list_frame,
                text=f"{phase.icon} {phase.name} ({len(drills)})",
                anchor="w",
                font=("Segoe UI", 16, "bold"),
            )
            phase_label.pack(
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
                )
                button.pack(
                    fill="x",
                    padx=30,
                    pady=2,
                )


    def build_ui(self):

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