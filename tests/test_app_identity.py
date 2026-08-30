from app.config import WINDOW_TITLE


def test_executable_window_title_is_training_planner():
    assert WINDOW_TITLE == "Training Planner"


def test_banner_title_is_not_user_configurable():
    from app.config import DEFAULT_CONFIG

    assert "title" not in DEFAULT_CONFIG
