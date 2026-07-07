import customtkinter as ctk
from tkinter import ttk


class SessionTable(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.tree = ttk.Treeview(self, show="headings")

        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

    def load_data(self, headers, sessions):

        self.tree.delete(*self.tree.get_children())

        self.tree["columns"] = headers

        for header in headers:
            self.tree.heading(header, text=str(header))
            self.tree.column(header, width=120, anchor="center")

        for session in sessions:
            self.tree.insert(
                "",
                "end",
                values=session.values
            )