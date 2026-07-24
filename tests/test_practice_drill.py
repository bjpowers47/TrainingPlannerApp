from app.models.drill import Drill
from app.models.practice_drill import PracticeDrill


def test_practice_drill_stores_session_settings():
    drill = Drill(
        id=1,
        name="Gates Dribbling",
        development_block_id=1,
        technical_focus_id=None,
        purpose="Improve close control and awareness.",
        duration_minutes=10,
        recommended_players="8",
        equipment=["Cones", "Soccer balls"],
        coaching_points=[],
        progressions=[],
        variations=[],
        notes="",
    )

    practice_drill = PracticeDrill(
        drill=drill,
        order=2,
        repetitions=3,
        work_seconds=90,
        rest_seconds=20,
        coach_notes="Use the weaker foot.",
    )

    assert practice_drill.drill is drill
    assert practice_drill.order == 2
    assert practice_drill.repetitions == 3
    assert practice_drill.work_seconds == 90
    assert practice_drill.rest_seconds == 20
    assert practice_drill.coach_notes == "Use the weaker foot."


if __name__ == "__main__":
    test_practice_drill_stores_session_settings()
    print("PracticeDrill test passed.")