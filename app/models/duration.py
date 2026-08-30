"""Shared duration parsing, formatting, and calculation rules."""

MAX_TOTAL_SECONDS = 240 * 60


def parse_duration_seconds(minutes_value, seconds_value, label="Duration") -> int:
    """Return total seconds from non-negative whole-number components."""
    minutes_text = str(minutes_value or "").strip()
    seconds_text = str(seconds_value or "").strip()
    try:
        minutes = int(minutes_text or 0)
        seconds = int(seconds_text or 0)
    except ValueError as error:
        raise ValueError(
            f"{label} minutes and seconds must be whole numbers."
        ) from error
    if minutes < 0:
        raise ValueError(f"{label} minutes must be zero or greater.")
    if seconds < 0 or seconds > 59:
        raise ValueError(f"{label} seconds must be between 0 and 59.")
    return minutes * 60 + seconds


def format_duration(total_seconds: float | int) -> str:
    """Format a non-negative duration as minutes:seconds."""
    minutes, seconds = divmod(max(0, int(total_seconds)), 60)
    return f"{minutes}:{seconds:02d}"


def format_signed_duration(total_seconds: float | int) -> str:
    """Format a duration as minutes:seconds while preserving a negative sign."""
    rounded_seconds = round(total_seconds)
    sign = "-" if rounded_seconds < 0 else ""
    return f"{sign}{format_duration(abs(rounded_seconds))}"


def execution_total_seconds(sets, work_seconds, rest_seconds) -> int:
    """Calculate Sets × (Work + Rest) with natural empty defaults."""
    set_count = int(sets or 1)
    if set_count < 0:
        raise ValueError("Sets must be zero or greater.")
    return set_count * (int(work_seconds or 0) + int(rest_seconds or 0))


def validate_total_seconds(total_seconds: int) -> int:
    """Enforce the application's maximum execution duration."""
    if total_seconds > MAX_TOTAL_SECONDS:
        raise ValueError("Total Time cannot exceed 240:00.")
    return total_seconds
