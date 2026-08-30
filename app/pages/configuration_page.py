"""Application and coaching configuration page."""

import customtkinter as ctk
from tkinter import messagebox


class ConfigurationPage(ctk.CTkFrame):
    def __init__(self, master, config_manager, block_repository, on_saved=None):
        super().__init__(master)
        self.config_manager = config_manager
        self.blocks = block_repository
        self.on_saved = on_saved
        self.grid_columnconfigure(0, weight=1)
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Configuration", font=("Segoe UI", 28, "bold")).grid(
            row=0, column=0, sticky="w", padx=30, pady=(25, 12))
        form = ctk.CTkScrollableFrame(self)
        form.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 25))
        self.grid_rowconfigure(1, weight=1)
        form.grid_columnconfigure(1, weight=1)

        self.sport_entry = self._entry(form, 0, "Sport (15 characters)", self.config_manager.data.get("sport", ""))
        self.head_entry = self._entry(form, 1, "Head Coach (25 characters)", self.config_manager.data.get("head_coach", ""))
        ctk.CTkLabel(form, text="Assistant Coach List (one per line, 25 characters each)").grid(
            row=2, column=0, sticky="nw", padx=10, pady=8)
        self.assistants = ctk.CTkTextbox(form, height=110)
        self.assistants.grid(row=2, column=1, sticky="ew", padx=10, pady=8)
        self.assistants.insert("1.0", "\n".join(self.config_manager.data.get("assistant_coaches", [])))

        ctk.CTkLabel(form, text="Block List", font=("Segoe UI", 18, "bold")).grid(
            row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 8))
        self.block_frame = ctk.CTkFrame(form)
        self.block_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=10)
        self._refresh_blocks()
        ctk.CTkButton(form, text="+ Create Block", command=self._create_block).grid(
            row=5, column=0, sticky="w", padx=10, pady=12)
        ctk.CTkButton(form, text="Save Configuration", command=self._save).grid(
            row=6, column=1, sticky="e", padx=10, pady=20)

    def _entry(self, parent, row, label, value):
        ctk.CTkLabel(parent, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=8)
        entry = ctk.CTkEntry(parent)
        entry.grid(row=row, column=1, sticky="ew", padx=10, pady=8)
        entry.insert(0, value)
        return entry

    def _refresh_blocks(self):
        for widget in self.block_frame.winfo_children(): widget.destroy()
        self._drag_source_id = None
        self._drag_target_row = None
        blocks = self.blocks.list_all()
        for row, block in enumerate(blocks):
            row_frame = ctk.CTkFrame(self.block_frame, fg_color="transparent")
            row_frame.grid(row=row, column=0, sticky="ew", padx=4, pady=2)
            row_frame.grid_columnconfigure(1, weight=1)
            row_frame._block_id = block.id
            grip = ctk.CTkLabel(
                row_frame, text="•••", width=32, cursor="fleur",
                text_color=("gray40", "gray70"),
            )
            grip.grid(row=0, column=0, padx=(4, 2))
            grip.bind("<ButtonPress-1>", lambda event, b=block: self._start_block_drag(event, b.id))
            grip.bind("<B1-Motion>", self._drag_block)
            grip.bind("<ButtonRelease-1>", self._drop_block)
            entry = ctk.CTkEntry(row_frame)
            entry.grid(row=0, column=1, sticky="ew", padx=4, pady=3)
            entry.insert(0, block.name)
            ctk.CTkButton(
                row_frame, text="Up", width=48,
                state="disabled" if row == 0 else "normal",
                command=lambda b=block: self._move_block(b.id, -1),
            ).grid(row=0, column=2, padx=2)
            ctk.CTkButton(
                row_frame, text="Down", width=58,
                state="disabled" if row == len(blocks) - 1 else "normal",
                command=lambda b=block: self._move_block(b.id, 1),
            ).grid(row=0, column=3, padx=2)
            ctk.CTkButton(row_frame, text="Update", width=70,
                command=lambda b=block, e=entry: self._update_block(b.id, e.get())).grid(row=0, column=4, padx=4)
            ctk.CTkButton(row_frame, text="Delete", width=70, fg_color="#9b2c2c",
                command=lambda b=block: self._delete_block(b.id)).grid(row=0, column=5, padx=4)
        self.block_frame.grid_columnconfigure(0, weight=1)

    def _start_block_drag(self, _event, block_id):
        self._drag_source_id = block_id

    def _row_at_pointer(self, event):
        widget = self.winfo_containing(event.x_root, event.y_root)
        while widget is not None and widget != self.block_frame:
            if hasattr(widget, "_block_id"):
                return widget
            widget = getattr(widget, "master", None)
        return None

    def _drag_block(self, event):
        target = self._row_at_pointer(event)
        if target is self._drag_target_row:
            return
        if self._drag_target_row is not None:
            self._drag_target_row.configure(fg_color="transparent")
        self._drag_target_row = target
        if target is not None:
            target.configure(fg_color=("gray80", "gray25"))

    def _drop_block(self, event):
        target = self._row_at_pointer(event)
        source_id = self._drag_source_id
        target_id = getattr(target, "_block_id", None)
        self._drag_source_id = None
        if self._drag_target_row is not None:
            self._drag_target_row.configure(fg_color="transparent")
        self._drag_target_row = None
        if source_id is not None and target_id is not None and self.blocks.reorder(source_id, target_id):
            self._refresh_blocks()

    def _create_block(self):
        self.blocks.create("New Block")
        self._refresh_blocks()

    def _move_block(self, block_id, direction):
        if self.blocks.move(block_id, direction):
            self._refresh_blocks()

    def _update_block(self, block_id, name):
        if not name.strip(): return
        try:
            self.blocks.rename(block_id, name)
        except ValueError as error:
            messagebox.showwarning("Invalid Block Name", str(error))
            return
        self._refresh_blocks()

    def _delete_block(self, block_id):
        try:
            self.blocks.delete(block_id)
        except ValueError as error:
            messagebox.showwarning("Block In Use", str(error)); return
        self._refresh_blocks()

    def _save(self):
        assistants = [line.strip()[:25] for line in self.assistants.get("1.0", "end").splitlines() if line.strip()]
        self.config_manager.data.update(sport=self.sport_entry.get().strip()[:15],
            head_coach=self.head_entry.get().strip()[:25], assistant_coaches=assistants)
        self.config_manager.save()
        if self.on_saved: self.on_saved()
        messagebox.showinfo("Configuration", "Configuration saved.")
