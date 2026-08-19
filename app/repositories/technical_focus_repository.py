"""
Wildcat Training Planner
------------------------

Module:
    technical_focus_repository.py

Purpose:
    Stores and retrieves TechnicalFocus objects.
"""

from app.models.technical_focus import TechnicalFocus


class TechnicalFocusRepository:
    """In-memory repository for technical focuses."""

    def __init__(self) -> None:
        self._technical_focuses: list[TechnicalFocus] = []

    def save(self, technical_focus: TechnicalFocus) -> None:
        """Add or replace a technical focus."""

        for index, existing_focus in enumerate(self._technical_focuses):
            if existing_focus.id == technical_focus.id:
                self._technical_focuses[index] = technical_focus
                return

        self._technical_focuses.append(technical_focus)

    def get_all(self, include_archived: bool = False) -> list[TechnicalFocus]:
        """Return all technical focuses."""

        if include_archived:
            return list(self._technical_focuses)

        return [
            focus
            for focus in self._technical_focuses
            if focus.active
        ]

    def get_by_id(self, technical_focus_id: int) -> TechnicalFocus | None:
        """Find a technical focus by ID."""

        for focus in self._technical_focuses:
            if focus.id == technical_focus_id:
                return focus

        return None

    def get_by_development_block(
        self,
        development_block_id: int,
    ) -> list[TechnicalFocus]:
        """Return active focuses belonging to one development block."""

        return [
            focus
            for focus in self._technical_focuses
            if focus.development_block_id == development_block_id
            and focus.active
        ]

    def get_by_name(
        self,
        name: str,
        development_block_id: int | None = None,
    ) -> TechnicalFocus | None:
        """
        Find an active technical focus by name.

        The optional development_block_id prevents duplicate focus names
        in different development blocks from being confused.
        """

        cleaned_name = name.strip().casefold()

        for focus in self._technical_focuses:
            if not focus.active:
                continue

            if development_block_id is not None:
                if focus.development_block_id != development_block_id:
                    continue

            if focus.name.strip().casefold() == cleaned_name:
                return focus

        return None

    def archive(self, technical_focus_id: int) -> bool:
        """Archive a technical focus."""

        focus = self.get_by_id(technical_focus_id)

        if focus is None:
            return False

        focus.archive()
        return True
