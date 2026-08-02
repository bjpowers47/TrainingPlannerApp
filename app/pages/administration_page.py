import customtkinter as ctk


class AdministrationPage(ctk.CTkFrame):
    """Administration dashboard for managing application data."""

    def __init__(
        self,
        master,
        open_drill_manager_callback=None,
        create_template_callback=None,
        import_spreadsheet_callback=None,
        export_spreadsheet_callback=None,
        database_maintenance_callback=None,
        restore_database_callback=None,
    ):
        super().__init__(master)

        self.open_drill_manager_callback = open_drill_manager_callback
        self.create_template_callback = create_template_callback
        self.import_spreadsheet_callback = import_spreadsheet_callback
        self.export_spreadsheet_callback = export_spreadsheet_callback
        self.database_maintenance_callback = database_maintenance_callback
        self.restore_database_callback = restore_database_callback

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

        database_button = ctk.CTkButton(
            tools_frame,
            text="💾 Database Maintenance",
            height=70,
            font=("Segoe UI", 17, "bold"),
            command=self.open_database_maintenance,
        )
        database_button.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=15,
        )

        ctk.CTkButton(
            tools_frame,
            text="Create Drill Template",
            height=48,
            command=self.create_template,
        ).grid(row=2, column=0, sticky="ew", padx=15, pady=15)

        ctk.CTkButton(
            tools_frame,
            text="Import Drill Spreadsheet",
            height=48,
            command=self.import_spreadsheet,
        ).grid(row=2, column=1, sticky="ew", padx=15, pady=15)

        ctk.CTkButton(
            tools_frame,
            text="Restore Database Backup",
            height=48,
            command=self.restore_database,
        ).grid(row=3, column=1, sticky="ew", padx=15, pady=15)

        ctk.CTkButton(
            tools_frame,
            text="Export Drill Spreadsheet",
            height=48,
            command=self.export_spreadsheet,
        ).grid(row=3, column=0, sticky="ew", padx=15, pady=15)

    def open_drill_manager(self):
        """Open the Drill Manager when its callback is available."""

        if self.open_drill_manager_callback is not None:
            self.open_drill_manager_callback()

    def create_template(self):
        if self.create_template_callback is not None:
            self.create_template_callback()

    def import_spreadsheet(self):
        if self.import_spreadsheet_callback is not None:
            self.import_spreadsheet_callback()

    def export_spreadsheet(self):
        if self.export_spreadsheet_callback is not None:
            self.export_spreadsheet_callback()

    def open_database_maintenance(self):
        if self.database_maintenance_callback is not None:
            self.database_maintenance_callback()

    def restore_database(self):
        if self.restore_database_callback is not None:
            self.restore_database_callback()
