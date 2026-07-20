import customtkinter as ctk


class AdministrationPage(ctk.CTkFrame):
    """Administration dashboard for managing application data."""

    def __init__(
        self,
        master,
        open_drill_manager_callback=None,
    ):
        super().__init__(master)

        self.open_drill_manager_callback = open_drill_manager_callback

        self.grid_columnconfigure(0, weight=1)

        self.build_ui()

    def build_ui(self):
        """Build the Administration dashboard."""

        title = ctk.CTkLabel(
            self,
            text="Administration",
            font=("Segoe UI", 28, "bold"),
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=30,
            pady=(30, 8),
        )

        subtitle = ctk.CTkLabel(
            self,
            text=(
                "Manage drills, coaching content, imports, exports, "
                "and application data."
            ),
            font=("Segoe UI", 14),
        )
        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            padx=30,
            pady=(0, 20),
        )

        tools_frame = ctk.CTkFrame(self)
        tools_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 30),
        )

        tools_frame.grid_columnconfigure(0, weight=1)
        tools_frame.grid_columnconfigure(1, weight=1)

        drill_button = ctk.CTkButton(
            tools_frame,
            text="📚 Drill Manager",
            height=70,
            font=("Segoe UI", 17, "bold"),
            command=self.open_drill_manager,
        )
        drill_button.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=15,
        )

        technical_focus_button = ctk.CTkButton(
            tools_frame,
            text="🎯 Technical Focus Manager",
            height=70,
            font=("Segoe UI", 17, "bold"),
            state="disabled",
        )
        technical_focus_button.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=15,
            pady=15,
        )

        import_export_button = ctk.CTkButton(
            tools_frame,
            text="📥 Import / Export",
            height=70,
            font=("Segoe UI", 17, "bold"),
            state="disabled",
        )
        import_export_button.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=15,
        )

        database_button = ctk.CTkButton(
            tools_frame,
            text="💾 Database Maintenance",
            height=70,
            font=("Segoe UI", 17, "bold"),
            state="disabled",
        )
        database_button.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=15,
            pady=15,
        )

    def open_drill_manager(self):
        """Open the Drill Manager when its callback is available."""

        if self.open_drill_manager_callback is not None:
            self.open_drill_manager_callback()