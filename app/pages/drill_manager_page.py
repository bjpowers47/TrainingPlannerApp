import customtkinter as ctk
from tkinter import messagebox

from app.models.player_development import DEVELOPMENT_BLOCKS


class DrillManagerPage(ctk.CTkFrame):

    def __init__(
        self,
        master,
        drill_service,
        on_new_drill=None,
        on_edit_drill=None,
        blocks=None,
    ):
        super().__init__(master)

        self.drill_service = drill_service
        self.on_new_drill = on_new_drill
        self.on_edit_drill = on_edit_drill
        # ``None`` means no block configuration was supplied. An empty list is
        # valid live configuration and must not restore hard-coded blocks.
        self.available_blocks = DEVELOPMENT_BLOCKS if blocks is None else blocks
        self.search_var = ctk.StringVar()
        self.block_filter_var = ctk.StringVar(value="All Blocks")
        self.last_archived = None

        self.build_ui()

    def _handle_new_drill(self):
        """Open the editor for a new drill."""

        if self.on_new_drill:
            self.on_new_drill()
        else:
            print("No New Drill callback was provided")

    def _handle_edit_drill(self, drill):
        """Open the requested drill in the editor."""
        if self.on_edit_drill:
            self.on_edit_drill(drill)
        else:
            print("No Edit Drill callback was provided")

    def _handle_delete_drill(self, drill):
        """Confirm and archive the requested drill."""
        confirmed = messagebox.askyesno(
            "Delete Drill",
            f'Remove "{drill.name}" from the active drill library?\n\n'
            "You can undo this action immediately afterward.",
        )
        if not confirmed:
            return

        if not self.drill_service.delete_drill(drill.id):
            messagebox.showwarning(
                "Drill Not Found",
                "This drill could not be found. The list will be refreshed.",
            )

        self.last_archived = drill
        self.undo_button.pack(side="right", padx=(0, 8))
        self._refresh_list()

    def _undo_archive(self):
        if self.last_archived and self.drill_service.restore_drill(self.last_archived.id):
            self.last_archived = None
            self.undo_button.pack_forget()
            self._refresh_list()

    def _refresh_list(self):
        """Reload the drill list after a change."""

        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.populate()

    def populate(self):
        """Load drills from the service and display them."""

        grouped = self.drill_service.get_drills_by_block()
        query = self.search_var.get().strip().casefold()
        selected_block = self.block_filter_var.get()

        # Use the same live database blocks as the editor. Configuration can
        # delete and recreate a block with a new ID, so the legacy constants
        # can no longer reliably group newly saved drills.
        for block in self.available_blocks:
            drills = grouped.get(block.id, [])
            if selected_block != "All Blocks" and block.name != selected_block:
                continue
            if query:
                drills = [drill for drill in drills if query in " ".join((
                    drill.name or "", drill.purpose or "", drill.coaching_focus or "",
                    " ".join(drill.equipment), " ".join(drill.coaching_points),
                )).casefold()]
            icon = getattr(block, "icon", None)
            icon_prefix = f"{icon} " if icon else ""

            block_label = ctk.CTkLabel(
                self.list_frame,
                text=f"{icon_prefix}{block.name} ({len(drills)})",
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
                drill_item = ctk.CTkFrame(
                    self.list_frame,
                    fg_color="transparent",
                )
                drill_item.pack(
                    fill="x",
                    padx=30,
                    pady=(2, 0),
                )

                drill_row = ctk.CTkFrame(
                    drill_item,
                    fg_color="transparent",
                )
                drill_row.pack(
                    fill="x",
                    pady=(0, 3),
                )

                name_label = ctk.CTkLabel(
                    drill_row,
                    text=drill.name,
                    anchor="w",
                )
                name_label.pack(
                    side="left",
                    fill="x",
                    expand=True,
                    padx=(12, 10),
                )

                delete_button = ctk.CTkButton(
                    drill_row,
                    text="Delete",
                    width=80,
                    fg_color="#9b2c2c",
                    hover_color="#7f1d1d",
                    command=lambda selected_drill=drill: (
                        self._handle_delete_drill(selected_drill)
                    ),
                )
                delete_button.pack(side="right", padx=(6, 0))

                edit_button = ctk.CTkButton(
                    drill_row,
                    text="Edit",
                    width=80,
                    command=lambda selected_drill=drill: (
                        self._handle_edit_drill(selected_drill)
                    ),
                )
                edit_button.pack(side="right")

                divider = ctk.CTkFrame(
                    drill_item,
                    height=1,
                    fg_color=("gray75", "gray30"),
                )
                divider.pack(fill="x")

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
        self.undo_button = ctk.CTkButton(
            header, text="Undo Remove", width=105, command=self._undo_archive
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

        filters = ctk.CTkFrame(self, fg_color="transparent")
        filters.pack(fill="x", padx=30, pady=(10, 10))
        search = ctk.CTkEntry(
            filters,
            placeholder_text="Search drills...",
            textvariable=self.search_var,
        )
        search.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkOptionMenu(
            filters,
            variable=self.block_filter_var,
            values=["All Blocks", *[block.name for block in self.available_blocks]],
            command=lambda _value: self._refresh_list(),
            width=190,
        ).pack(side="right")
        self.search_var.trace_add("write", lambda *_args: self._refresh_list())

        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(10, 20),
        )

        self.populate()
