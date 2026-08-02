"""Create and import the collaborative Development Library spreadsheet."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from app.models.drill import Drill
from app.models.player_development import (
    DEVELOPMENT_BLOCKS,
    get_block_by_id,
    get_block_by_name,
)
from app.services.coaching_library import get_coaching_focus_by_id


HEADERS = (
    "Development Block", "Drill Name", "Purpose", "Duration Minutes",
    "Recommended Players", "Equipment", "Coaching Points", "Progressions",
    "Variations", "Notes",
)

EXPORT_HEADERS = (
    "Drill ID", "Development Block", "Coaching Focus", "Drill Name",
    "Purpose", "Duration Minutes", "Recommended Players",
    "Use Execution Details", "Sets", "Reps", "Work Seconds", "Rest Seconds",
    "Equipment", "Coaching Points", "Progressions", "Variations", "Notes",
)


def _safe_spreadsheet_text(value: object) -> object:
    """Prevent exported text from being interpreted as an Excel formula."""
    if not isinstance(value, str):
        return value
    if value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def _pipe_join(values: list[str]) -> str:
    return " | ".join(str(value).strip() for value in values if str(value).strip())


def export_spreadsheet(filename: str | Path, repository) -> int:
    """Export active drills to a formatted, coach-readable Excel workbook."""
    drills = [drill for drill in repository.get_all() if drill.active]
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Active Drills"
    worksheet.append(EXPORT_HEADERS)

    for drill in drills:
        block = get_block_by_id(drill.development_block_id)
        focus = (
            get_coaching_focus_by_id(drill.technical_focus_id)
            if drill.technical_focus_id is not None
            else None
        )
        values = (
            drill.id,
            block.name if block else f"Unknown block ({drill.development_block_id})",
            focus.name if focus else "",
            drill.name,
            drill.purpose,
            drill.duration_minutes,
            drill.recommended_players,
            "Yes" if drill.use_execution_details else "No",
            drill.sets,
            drill.reps,
            drill.work_seconds,
            drill.rest_seconds,
            _pipe_join(drill.equipment),
            _pipe_join(drill.coaching_points),
            _pipe_join(drill.progressions),
            _pipe_join(drill.variations),
            drill.notes,
        )
        worksheet.append([_safe_spreadsheet_text(value) for value in values])

    header_fill = PatternFill("solid", fgColor="1F4E78")
    for cell in worksheet[1]:
        cell.font = Font(color="FFFFFF", bold=True)
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions
    worksheet.row_dimensions[1].height = 24
    for row in worksheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    for index, column in enumerate(worksheet.columns, start=1):
        longest = max(len(str(cell.value or "")) for cell in column)
        worksheet.column_dimensions[get_column_letter(index)].width = min(
            max(longest + 2, 12), 42
        )

    workbook.save(filename)
    return len(drills)


@dataclass
class ImportReport:
    imported: int = 0
    duplicates: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def create_template(filename: str | Path) -> None:
    """Create an Excel template that coaches can complete without the app."""
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Drills"
    worksheet.append(HEADERS)
    worksheet.append([
        "Ball Mastery", "Example: Toe Taps", "Build comfort on the ball.",
        10, "Any", "Ball; cones", "Head up; light touches", "Add movement",
        "Use weaker foot", "Delete this example before importing.",
    ])
    instructions = workbook.create_sheet("Instructions")
    instructions.append(["How to use this template"])
    instructions.append(["Add one drill per row on the Drills sheet."])
    instructions.append(["Use one of these Development Blocks:"])
    for block in DEVELOPMENT_BLOCKS:
        instructions.append([block.name])
    instructions.append(["Separate list items with semicolons."])
    workbook.save(filename)


def import_spreadsheet(filename: str | Path, repository) -> ImportReport:
    """Validate a drill spreadsheet and add valid, non-duplicate drills."""
    report = ImportReport()
    worksheet = load_workbook(filename, data_only=True)["Drills"]
    headers = [cell.value for cell in next(worksheet.iter_rows(min_row=1, max_row=1))]
    if tuple(headers) != HEADERS:
        report.errors.append("The spreadsheet does not use the Drill Import Template.")
        return report

    existing = repository.get_all()
    known = {(drill.development_block_id, drill.name.casefold()) for drill in existing}
    next_id = max((drill.id for drill in existing), default=0) + 1

    for row_number, values in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
        if not any(value not in (None, "") for value in values):
            continue
        block_name, name, purpose, duration, players, equipment, points, progressions, variations, notes = values
        block = get_block_by_name(str(block_name).strip()) if block_name else None
        clean_name = str(name).strip() if name else ""
        if not block or not clean_name:
            report.errors.append(f"Row {row_number}: Development Block and Drill Name are required.")
            continue
        key = (block.id, clean_name.casefold())
        if key in known:
            report.duplicates.append(f"Row {row_number}: {clean_name}")
            continue
        try:
            duration_minutes = int(duration or 0)
        except (TypeError, ValueError):
            report.errors.append(f"Row {row_number}: Duration Minutes must be a whole number.")
            continue
        split = lambda value: [item.strip() for item in str(value or "").split(";") if item.strip()]
        repository.save(Drill(
            id=next_id, name=clean_name, development_block_id=block.id,
            purpose=str(purpose or "").strip(), duration_minutes=duration_minutes,
            recommended_players=str(players or "").strip(), equipment=split(equipment),
            coaching_points=split(points), progressions=split(progressions),
            variations=split(variations), notes=str(notes or "").strip(),
        ))
        known.add(key)
        next_id += 1
        report.imported += 1
    return report
