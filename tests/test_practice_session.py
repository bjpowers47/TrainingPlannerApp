from datetime import date

from app.models.drill import Drill
from app.models.practice_drill import PracticeDrill
from app.models.practice_session import PracticeSession


def test_add_and_remove_practice_drill():

    drill = Drill(
        id=1,
        name="Gates Dribbling",
        development_block_id=1,
        technical_focus_id=None,
        purpose="Improve ball control.",
        duration_minutes=10,
        recommended_players="8",
        equipment=[],
        coaching_points=[],
        progressions=[],
        variations=[],
        notes="",
    )

    practice_drill = PracticeDrill(
        drill=drill,
        order=1,
    )

    session = PracticeSession(
        id=1,
        title="Monday Training",
        session_date=date.today(),
    )

    session.add_drill(practice_drill)

    assert len(session.drills) == 1
    assert session.drills[0] is practice_drill

    session.remove_drill(practice_drill)

    assert len(session.drills) == 0


if __name__ == "__main__":
    test_add_and_remove_practice_drill()
    print("PracticeSession test passed.")

def test_move_practice_drills():

    drill1 = Drill(
        id=1,
        name="Drill 1",
        development_block_id=1,
        technical_focus_id=None,
        purpose="",
        duration_minutes=10,
        recommended_players="8",
        equipment=[],
        coaching_points=[],
        progressions=[],
        variations=[],
        notes="",
    )

    drill2 = Drill(
        id=2,
        name="Drill 2",
        development_block_id=1,
        technical_focus_id=None,
        purpose="",
        duration_minutes=10,
        recommended_players="8",
        equipment=[],
        coaching_points=[],
        progressions=[],
        variations=[],
        notes="",
    )

    session = PracticeSession(
        id=1,
        title="Training",
        session_date=date.today(),
    )

    session.add_drill(
        PracticeDrill(drill=drill1, order=1)
    )

    session.add_drill(
        PracticeDrill(drill=drill2, order=2)
    )

    session.move_drill_down(0)

    assert session.drills[0].drill.name == "Drill 2"
    assert session.drills[1].drill.name == "Drill 1"

    session.move_drill_up(1)

    assert session.drills[0].drill.name == "Drill 1"
    assert session.drills[1].drill.name == "Drill 2"
