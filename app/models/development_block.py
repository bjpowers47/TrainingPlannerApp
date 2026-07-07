"""Development Block domain model."""

from dataclasses import dataclass


@dataclass
class DevelopmentBlock:
    id: int
    name: str
    description: str
    display_order: int
    is_active: bool = True
