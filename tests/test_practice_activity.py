from app.models.drill import Drill
from app.models.practice_activity import PracticeActivity
from app.models.practice import Practice


def test_default_duration():
    """Uses the drill duration when no override exists."""

    drill = Drill(
        id=1,
        name="Ball Taps",
        development_block_id=1,
        technical_focus_id=None,
        purpose="Control",
        duration_minutes=10,
        recommended_players="1+",
    )

    activity = PracticeActivity(drill)

    assert activity.duration_minutes() == 10


def test_override_duration():
    """Uses the override duration when provided."""

    drill = Drill(
        id=1,
        name="Ball Taps",
        development_block_id=1,
        technical_focus_id=None,
        purpose="Control",
        duration_minutes=10,
        recommended_players="1+",
    )

    activity = PracticeActivity(
        drill,
        duration_override=6,
    )

    assert activity.duration_minutes() == 6


def test_name_property():
    """Returns the drill name."""

    drill = Drill(
        id=1,
        name="Ball Taps",
        development_block_id=1,
        technical_focus_id=None,
        purpose="Control",
        duration_minutes=10,
        recommended_players="1+",
    )

    activity = PracticeActivity(drill)

    assert activity.name == "Ball Taps"


def test_duration_uses_exact_work_and_rest_seconds():
    drill = Drill(
        id=1,
        name="Intervals",
        development_block_id=1,
        technical_focus_id=None,
        purpose="Fitness",
        duration_minutes=10,
        recommended_players="1+",
    )
    activity = PracticeActivity(
        drill,
        sets=3,
        work_seconds=75,
        rest_seconds=20,
    )

    assert activity.duration_seconds() == 285
    assert activity.duration_minutes() == 4.75


if __name__ == "__main__":
    test_default_duration()
    test_override_duration()
    test_name_property()

    print("PracticeActivity tests passed.")

def test_practice_activity_is_saved_and_loaded(tmp_path):
    drill = Drill(
        id=1,
        name="Ball Taps",
        development_block_id=1,
        technical_focus_id=None,
        purpose="Control",
        duration_minutes=10,
        recommended_players="1+",
    )

    practice = Practice()
    phase = practice.get_block_names()[0]

    practice.add_activity(phase, drill)

    filename = tmp_path / "practice.json"
    practice.save_to_json(filename)

    loaded_practice = Practice.load_from_json(filename)
    loaded_activity = loaded_practice.get_activities(phase)[0]

    assert loaded_activity.name == "Ball Taps"
    assert loaded_activity.duration_minutes() == 10
