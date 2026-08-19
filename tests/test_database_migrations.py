from app.database import CURRENT_SCHEMA_VERSION, Database


def test_database_records_current_schema_version(tmp_path):
    database = Database(tmp_path / "training.db")
    database.initialize()

    with database.connect() as connection:
        version = connection.execute(
            "SELECT MAX(version) FROM schema_migrations"
        ).fetchone()[0]

    assert version == CURRENT_SCHEMA_VERSION
