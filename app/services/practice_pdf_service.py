"""Create a printable, coach-friendly PDF practice plan."""

from __future__ import annotations

import textwrap
import ctypes
import re
from ctypes import wintypes
from pathlib import Path

from app.config import training_manager_name
from app.models.duration import format_duration
from app.services.coaching_library import get_coaching_focus_by_id


def _clean(value: object) -> str:
    return str(value or "").replace("\r", " ").replace("\n", " ").strip()


def _clean_multiline(value: object) -> str:
    """Normalize user-entered line endings without discarding line breaks."""
    return str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def _join(values: list[str]) -> str:
    return ", ".join(_clean(value) for value in values if _clean(value))


def _join_multiline(values: list[str]) -> str:
    return "\n".join(_clean_multiline(value) for value in values if _clean_multiline(value))


def _duration_text(minutes: float) -> str:
    return format_duration(round(minutes * 60))


_URL_PATTERN = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)


def _contains_url(value: str) -> bool:
    return _URL_PATTERN.search(value) is not None


def build_practice_pdf_lines(practice, coach: str | None = None) -> list[tuple[str, str]]:
    """Build styled logical lines, kept separate for focused validation."""
    lines: list[tuple[str, str]] = []
    lines.append(("title", _clean(practice.name) or f"{training_manager_name(getattr(practice, 'sport', ''))} Practice Plan"))
    if coach:
        lines.append(("normal", f"Coach: {_clean(coach)}"))
    elif _clean(getattr(practice, "head_coach", "")):
        lines.append(("normal", f"Master Plan — Head Coach: {_clean(practice.head_coach)}"))
    details = []
    if _clean(practice.practice_date):
        details.append(f"Date: {_clean(practice.practice_date)}")
    if _clean(practice.team_name):
        details.append(f"Team: {_clean(practice.team_name)}")
    if details:
        lines.append(("normal", " | ".join(details)))
    if _clean_multiline(practice.objective):
        lines.append(("normal", f"Objective: {_clean_multiline(practice.objective)}"))
    lines.append(("spacer", ""))

    for block in practice.get_block_names():
        if coach and coach not in practice.block_coaches.get(block, []):
            continue
        lines.append(("spacer", ""))
        assigned_coaches = practice.block_coaches.get(block, [])
        coach_label = ", ".join(_clean(name) for name in assigned_coaches if _clean(name))
        if coach_label:
            heading = f"{block} — Coach{'es' if len(assigned_coaches) != 1 else ''}: {coach_label}"
        else:
            heading = f"{block} — Coach: Unassigned"
        lines.append(("heading", heading))
        activities = practice.get_activities(block)
        if not activities:
            lines.append(("muted", "No activities planned."))
            continue

        for activity in activities:
            activity_heading = _clean(activity.name)
            practice_note = _clean(activity.coach_notes)
            if practice_note:
                activity_heading = f"{activity_heading} — {practice_note}"
            lines.append(("subheading", activity_heading))
            drill = activity.drill
            facts = [f"Time: {_duration_text(activity.duration_minutes())}"]
            if activity.sets is not None:
                facts.append(f"Sets: {activity.sets}")
            if activity.work_seconds:
                facts.append(f"Work: {_duration_text(activity.work_minutes)}")
            if activity.rest_seconds:
                facts.append(f"Rest: {_duration_text(activity.rest_minutes)}")
            lines.append(("normal", " | ".join(facts)))
            coaching_focus = _clean(getattr(drill, "coaching_focus", ""))
            if not coaching_focus and getattr(drill, "technical_focus_id", None):
                legacy_focus = get_coaching_focus_by_id(drill.technical_focus_id)
                coaching_focus = _clean(legacy_focus.name) if legacy_focus else ""
            detail_values = (
                ("Coaching Focus", coaching_focus),
                ("Directions", _clean_multiline(drill.purpose)),
                ("Recommended Duration", _duration_text(float(drill.duration_minutes))),
                ("Players", drill.recommended_players),
                ("Equipment", _join(drill.equipment)),
                ("Coaching Points", _join_multiline(drill.coaching_points)),
                ("Progressions", _join_multiline(drill.progressions)),
                ("Variations", _join_multiline(drill.variations)),
                ("Drill Notes", _clean_multiline(drill.notes)),
                ("Practice Notes", _clean_multiline(activity.coach_notes)),
            )
            if activity.print_details:
                for label, value in detail_values:
                    lines.append(("detail", f"{label}: {value or 'Not specified'}"))

    lines.append(("spacer", ""))
    lines.append(("total", f"Total Planned Time: {format_duration(practice.total_duration_seconds())}"))
    return lines


def print_practice(practice, coach: str | None = None) -> bool:
    """Show the Windows Print dialog and render directly to its selected printer."""
    class PRINTDLGW(ctypes.Structure):
        # commdlg.h uses two-byte packing for the legacy 32-bit PRINTDLG
        # structure. Without it ctypes produces 68 bytes instead of the 66
        # bytes expected by Windows, causing CDERR_STRUCTSIZE (error 1).
        if ctypes.sizeof(ctypes.c_void_p) == 4:
            _pack_ = 2
        _fields_ = [
            ("lStructSize", wintypes.DWORD), ("hwndOwner", wintypes.HWND),
            ("hDevMode", wintypes.HANDLE), ("hDevNames", wintypes.HANDLE),
            ("hDC", wintypes.HDC), ("Flags", wintypes.DWORD),
            ("nFromPage", wintypes.WORD), ("nToPage", wintypes.WORD),
            ("nMinPage", wintypes.WORD), ("nMaxPage", wintypes.WORD),
            ("nCopies", wintypes.WORD), ("hInstance", wintypes.HINSTANCE),
            ("lCustData", wintypes.LPARAM), ("lpfnPrintHook", ctypes.c_void_p),
            ("lpfnSetupHook", ctypes.c_void_p), ("lpPrintTemplateName", wintypes.LPCWSTR),
            ("lpSetupTemplateName", wintypes.LPCWSTR), ("hPrintTemplate", wintypes.HANDLE),
            ("hSetupTemplate", wintypes.HANDLE),
        ]

    class DOCINFOW(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_int), ("lpszDocName", wintypes.LPCWSTR),
            ("lpszOutput", wintypes.LPCWSTR), ("lpszDatatype", wintypes.LPCWSTR),
            ("fwType", wintypes.DWORD),
        ]

    comdlg32 = ctypes.WinDLL("comdlg32", use_last_error=True)
    gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    comdlg32.PrintDlgW.argtypes = [ctypes.POINTER(PRINTDLGW)]
    comdlg32.PrintDlgW.restype = wintypes.BOOL
    gdi32.CreateFontW.restype = ctypes.c_void_p
    gdi32.SelectObject.argtypes = [wintypes.HDC, ctypes.c_void_p]
    gdi32.SelectObject.restype = ctypes.c_void_p
    gdi32.DeleteObject.argtypes = [ctypes.c_void_p]
    gdi32.DeleteDC.argtypes = [wintypes.HDC]
    gdi32.GetDeviceCaps.argtypes = [wintypes.HDC, ctypes.c_int]
    gdi32.SetBkMode.argtypes = [wintypes.HDC, ctypes.c_int]
    gdi32.SetBkColor.argtypes = [wintypes.HDC, wintypes.DWORD]
    gdi32.StartDocW.argtypes = [wintypes.HDC, ctypes.POINTER(DOCINFOW)]
    gdi32.StartPage.argtypes = [wintypes.HDC]
    gdi32.EndPage.argtypes = [wintypes.HDC]
    gdi32.EndDoc.argtypes = [wintypes.HDC]
    gdi32.AbortDoc.argtypes = [wintypes.HDC]
    user32.DrawTextW.argtypes = [wintypes.HDC, wintypes.LPCWSTR, ctypes.c_int, ctypes.POINTER(wintypes.RECT), wintypes.UINT]
    kernel32.GlobalFree.argtypes = [ctypes.c_void_p]
    kernel32.GlobalFree.restype = ctypes.c_void_p
    pd = PRINTDLGW()
    pd.lStructSize = ctypes.sizeof(PRINTDLGW)
    # Display the normal Windows printer-selection dialog. The coach can pick
    # any installed physical printer or a virtual printer such as Microsoft
    # Print to PDF. Page-range and selection controls do not apply here.
    PD_RETURNDC = 0x00000100
    PD_NOSELECTION = 0x00000004
    PD_NOPAGENUMS = 0x00000008
    PD_USEDEVMODECOPIESANDCOLLATE = 0x00040000
    pd.Flags = (
        PD_RETURNDC
        | PD_NOSELECTION
        | PD_NOPAGENUMS
        | PD_USEDEVMODECOPIESANDCOLLATE
    )
    pd.nFromPage = pd.nToPage = pd.nMinPage = pd.nMaxPage = 1
    pd.nCopies = 1
    if not comdlg32.PrintDlgW(ctypes.byref(pd)):
        error = comdlg32.CommDlgExtendedError()
        if error:
            raise OSError(f"Windows Print dialog failed (error {error}).")
        return False

    hdc = pd.hDC
    LOGPIXELSX, LOGPIXELSY, HORZRES, VERTRES = 88, 90, 8, 10
    dpi_x = gdi32.GetDeviceCaps(hdc, LOGPIXELSX)
    dpi_y = gdi32.GetDeviceCaps(hdc, LOGPIXELSY)
    page_width = gdi32.GetDeviceCaps(hdc, HORZRES)
    page_height = gdi32.GetDeviceCaps(hdc, VERTRES)
    left = right = max(1, int(dpi_x * 0.55))
    top = bottom = max(1, int(dpi_y * 0.55))
    content_right = page_width - right
    content_bottom = page_height - bottom
    DT_WORDBREAK, DT_CALCRECT, DT_NOPREFIX = 0x10, 0x400, 0x800
    TRANSPARENT, OPAQUE = 1, 2
    URL_HIGHLIGHT_COLOR = 0x0073EDFF  # RGB(255, 237, 115) as COLORREF
    styles = {
        "title": (20, 700, 12, 0), "heading": (15, 700, 8, 0),
        "subheading": (11, 700, 4, 0), "total": (12, 700, 8, 0),
        "normal": (10, 400, 4, 0), "detail": (9, 400, 3, 14),
        "muted": (9, 400, 4, 0), "spacer": (7, 400, 7, 0),
    }
    fonts = {}
    old_font = None
    document_started = False
    try:
        for style, (points, weight, _gap, _indent) in styles.items():
            height = -round(points * dpi_y / 72)
            fonts[style] = gdi32.CreateFontW(
                height, 0, 0, 0, weight, 0, 0, 0, 1, 0, 0, 0, 0, "Arial"
            )
        doc = DOCINFOW(ctypes.sizeof(DOCINFOW), _clean(practice.name) or f"{training_manager_name(getattr(practice, 'sport', ''))} Practice Plan", None, None, 0)
        if gdi32.StartDocW(hdc, ctypes.byref(doc)) <= 0:
            raise OSError("Windows could not start the print job.")
        document_started = True
        if gdi32.StartPage(hdc) <= 0:
            raise OSError("Windows could not start the printed page.")
        y = top
        for style, value in build_practice_pdf_lines(practice, coach):
            points, _weight, gap, indent_points = styles[style]
            font = fonts[style]
            previous = gdi32.SelectObject(hdc, font)
            if old_font is None:
                old_font = previous
            indent = round(indent_points * dpi_x / 72)
            if style == "spacer":
                height = round(points * dpi_y / 72)
            else:
                measure = wintypes.RECT(left + indent, y, content_right, content_bottom)
                height = user32.DrawTextW(hdc, value, -1, ctypes.byref(measure), DT_WORDBREAK | DT_CALCRECT | DT_NOPREFIX)
            gap_pixels = round(gap * dpi_y / 72)
            if y + height + gap_pixels > content_bottom:
                gdi32.EndPage(hdc)
                if gdi32.StartPage(hdc) <= 0:
                    raise OSError("Windows could not start the next printed page.")
                y = top
            if style != "spacer":
                target = wintypes.RECT(left + indent, y, content_right, y + height + 2)
                if _contains_url(value):
                    gdi32.SetBkColor(hdc, URL_HIGHLIGHT_COLOR)
                    gdi32.SetBkMode(hdc, OPAQUE)
                else:
                    gdi32.SetBkMode(hdc, TRANSPARENT)
                user32.DrawTextW(hdc, value, -1, ctypes.byref(target), DT_WORDBREAK | DT_NOPREFIX)
                gdi32.SetBkMode(hdc, TRANSPARENT)
            y += height + gap_pixels
        gdi32.EndPage(hdc)
        if gdi32.EndDoc(hdc) <= 0:
            raise OSError("Windows could not complete the print job.")
        document_started = False
        return True
    except Exception:
        if document_started:
            gdi32.AbortDoc(hdc)
        raise
    finally:
        if old_font:
            gdi32.SelectObject(hdc, old_font)
        for font in fonts.values():
            if font:
                gdi32.DeleteObject(font)
        if hdc:
            gdi32.DeleteDC(hdc)
        if pd.hDevMode:
            kernel32.GlobalFree(pd.hDevMode)
        if pd.hDevNames:
            kernel32.GlobalFree(pd.hDevNames)


def export_practice_pdf(filename: str | Path, practice, coach: str | None = None) -> None:
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

    for style, text in build_practice_pdf_lines(practice, coach):
        font, size, leading = styles[style]
        width = 72 if style in {"detail", "muted"} else 82
        wrapped = [
            wrapped_line
            for entered_line in text.split("\n")
            for wrapped_line in (
                textwrap.wrap(entered_line, width=width, break_long_words=False)
                or [""]
            )
        ]
        for line in wrapped:
            if y - leading < bottom:
                pages.append([])
                y = top
            indent = 14 if style == "detail" else 0
            if _contains_url(line):
                highlight_width = min(
                    page_width - left - indent - 54,
                    max(24, round(len(line) * size * 0.52) + 4),
                )
                pages[-1].append(
                    f"% URL highlight\nq 1 0.93 0.45 rg "
                    f"{left + indent - 2} {y - 3} {highlight_width} {leading} re f Q"
                )
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
