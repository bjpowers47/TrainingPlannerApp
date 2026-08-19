"""Typed data transferred from the Drill Editor to application services."""

from dataclasses import asdict, dataclass, field


@dataclass
class DrillFormData:
    name: str
    development_block_id: int
    technical_focus_id: int | None
    technical_focus: str
    purpose: str
    duration_minutes: str
    recommended_players: str
    use_execution_details: bool
    sets: str
    reps: object
    work_seconds: str
    rest_seconds: str
    equipment: list[str] = field(default_factory=list)
    coaching_points: list[str] = field(default_factory=list)
    progressions: list[str] = field(default_factory=list)
    variations: list[str] = field(default_factory=list)
    notes: str = ""
    id: int | None = None

    def to_dict(self) -> dict:
        """Provide a compatibility mapping for the existing save service."""
        values = asdict(self)
        if self.id is None:
            values.pop("id")
        return values
