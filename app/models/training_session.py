from dataclasses import dataclass


@dataclass
class TrainingSession:
    row_number: int

    values: list

    def get(self, column):
        if column < len(self.values):
            return self.values[column]
        return ""

    def set(self, column, value):
        while len(self.values) <= column:
            self.values.append("")
        self.values[column] = value