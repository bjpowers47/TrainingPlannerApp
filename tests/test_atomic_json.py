import json

from app.services.atomic_json import write_json_atomic


def test_atomic_json_replaces_existing_file(tmp_path):
    destination = tmp_path / "settings.json"
    destination.write_text('{"old": true}', encoding="utf-8")

    write_json_atomic(destination, {"new": True})

    assert json.loads(destination.read_text(encoding="utf-8")) == {"new": True}
    assert list(tmp_path.iterdir()) == [destination]
