import customtkinter as ctk


class DashboardPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(pady=20)

        self.info = ctk.CTkTextbox(
            self,
            width=900,
            height=600
        )

        self.info.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        self.info.insert(
            "end",
            "Welcome to Training Manager\n\n"
            "Version 0.2\n\n"
            "Load an Excel workbook to begin."
        )

    def set_text(self, text):
        self.info.delete("1.0", "end")
        self.info.insert("end", text)
