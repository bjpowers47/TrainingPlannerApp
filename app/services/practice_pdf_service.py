"""Create a printable, coach-friendly PDF practice plan."""

from __future__ import annotations

import textwrap
from pathlib import Path


def _clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def _join(values: list[str]) -> str:
    return ", ".join(_clean(value) for value in values if _clean(value))


def _duration_text(minutes: float) -> str:
    return f"{int(minutes)} min" if minutes.is_integer() else f"{minutes:.1f} min"


def build_practice_pdf_lines(practice) -> list[tuple[str, str]]:
    """Build styled logical lines, kept separate for focused validation."""
    lines: list[tuple[str, str]] = []
    lines.append(("title", _clean(practice.name) or "Soccer Practice Plan"))
    details = []
    if _clean(practice.practice_date):
        details.append(f"Date: {_clean(practice.practice_date)}")
    if _clean(practice.team_name):
        details.append(f"Team: {_clean(practice.team_name)}")
    if details:
        lines.append(("normal", " | ".join(details)))
    if _clean(practice.objective):
        lines.append(("normal", f"Objective: {_clean(practice.objective)}"))
    lines.append(("spacer", ""))

    lines.append(("heading", "Warm Up"))
    lines.append(("normal", f"Duration: {practice.warm_up_minutes} min"))

    for block in practice.get_block_names():
        lines.append(("spacer", ""))
        lines.append(("heading", block))
        activities = practice.get_activities(block)
        if not activities:
            lines.append(("muted", "No activities planned."))
            continue

        for activity in activities:
            lines.append(("subheading", activity.name))
            drill = activity.drill
            facts = [f"Time: {_duration_text(activity.duration_minutes())}"]
            if activity.sets is not None:
                facts.append(f"Sets: {activity.sets}")
            if _clean(activity.reps):
                facts.append(f"Reps: {_clean(activity.reps)}")
            if activity.work_seconds:
                facts.append(f"Work: {activity.work_seconds} sec")
            if activity.rest_seconds:
                facts.append(f"Rest: {activity.rest_seconds} sec")
            lines.append(("normal", " | ".join(facts)))
            for label, value in (
                ("Purpose", drill.purpose),
                ("Players", drill.recommended_players),
                ("Equipment", _join(drill.equipment)),
                ("Coaching Points", _join(drill.coaching_points)),
                ("Progressions", _join(drill.progressions)),
                ("Variations", _join(drill.variations)),
                ("Drill Notes", drill.notes),
                ("Practice Notes", activity.coach_notes),
            ):
                if _clean(value):
                    lines.append(("detail", f"{label}: {_clean(value)}"))

    lines.append(("spacer", ""))
    lines.append(("total", f"Total Planned Time: {practice.total_duration()} min"))
    return lines


def export_practice_pdf(filename: str | Path, practice) -> None:
    """Write the practice as a valid multi-page PDF using built-in fonts."""
    page_width, page_height = 612, 792
    left, top, bottom = 54, 738, 54
    pages: list[list[str]] = [[]]
    y = top

    styles = {
        "title": ("F2", 20, 27),
        "heading": ("F2", 15, 22),
        "subheading": ("F2", 11, 17),
        "total": ("F2", 12, 19),
        "normal": ("F1", 10, 15),
        "detail": ("F1", 9, 13),
        "muted": ("F1", 9, 14),
        "spacer": ("F1", 7, 9),
    }

    def pdf_text(text: str) -> str:
        encoded = text.encode("cp1252", errors="replace").decode("cp1252")
        return encoded.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    for style, text in build_practice_pdf_lines(practice):
        font, size, leading = styles[style]
        width = 72 if style in {"detail", "muted"} else 82
        wrapped = textwrap.wrap(text, width=width, break_long_words=False) or [""]
        for line in wrapped:
            if y - leading < bottom:
                pages.append([])
                y = top
            indent = 14 if style == "detail" else 0
            pages[-1].append(
                f"BT /{font} {size} Tf 1 0 0 1 {left + indent} {y} Tm ({pdf_text(line)}) Tj ET"
            )
            y -= leading

    objects: list[bytes] = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    page_ids = [5 + index * 2 for index in range(len(pages))]
    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    for index, commands in enumerate(pages):
        page_id = page_ids[index]
        content_id = page_id + 1
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_width} {page_height}] "
                f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
                f"/Contents {content_id} 0 R >>"
            ).encode()
        )
        stream = "\n".join(commands).encode("cp1252", errors="replace")
        objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    )
    Path(filename).write_bytes(output)
