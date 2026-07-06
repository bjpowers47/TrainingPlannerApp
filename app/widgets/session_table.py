from tkinter import ttk


class SessionTable(ttk.Treeview):

    COLUMNS = (
        "Date",
        "Start",
        "End",
        "Age Group",
        "Topic",
        "Location",
        "Coach"
    )

    def __init__(self, master):

        super().__init__(
            master,
            columns=self.COLUMNS,
            show="headings",
            selectmode="browse"
        )

        for column in self.COLUMNS:
            self.heading(column, text=column)
            self.column(
                column,
                width=120,
                anchor="center",
                stretch=True
            )

    def clear(self):
        """Remove all rows."""
        for item in self.get_children():
            self.delete(item)

    def load_sessions(self, sessions):
        """Load TrainingSession objects into the table."""

        self.clear()

        for session in sessions:

            values = session.values[:7]

            while len(values) < 7:
                values.append("")

            self.insert("", "end", values=values)

    def selected(self):
        """Return the selected row id."""

        selection = self.selection()

        if not selection:
            return None

        return selection[0]