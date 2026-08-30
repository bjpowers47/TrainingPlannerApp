import pytest

from app.models.duration import (
    MAX_TOTAL_SECONDS,
    execution_total_seconds,
    format_duration,
    format_signed_duration,
    parse_duration_seconds,
    validate_total_seconds,
)


def test_duration_round_trip():
    seconds = parse_duration_seconds("123", "05", "Work")
    assert seconds == 7385
    assert format_duration(seconds) == "123:05"


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [(155, "2:35"), (0, "0:00"), (-20, "-0:20"), (-155, "-2:35")],
)
def test_signed_duration_format(seconds, expected):
    assert format_signed_duration(seconds) == expected


@pytest.mark.parametrize("seconds", ["60", "99", "-1"])
def test_seconds_must_be_between_zero_and_fifty_nine(seconds):
    with pytest.raises(ValueError, match="between 0 and 59"):
        parse_duration_seconds("0", seconds, "Rest")


def test_execution_total_uses_one_set_when_blank():
    assert execution_total_seconds("", 75, 15) == 90


def test_maximum_total_boundary():
    assert validate_total_seconds(MAX_TOTAL_SECONDS) == MAX_TOTAL_SECONDS
    with pytest.raises(ValueError, match="240:00"):
        validate_total_seconds(MAX_TOTAL_SECONDS + 1)
