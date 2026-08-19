# Wildcat Training Planner Release Checklist

## Code and data

- Update `APP_VERSION` and `CHANGELOG.md`.
- Confirm no personal databases, configuration, practices, backups, or logs are staged.
- Run `python -m compileall -q app`.
- Run `python -m ruff check app tests main.py`.
- Run `python -m pytest -q`.

## Upgrade and workflow checks

- Open an existing database and practice created by the previous release.
- Create, edit, save, reopen, and remove a drill.
- Build a practice with timed sets and confirm the calculated total.
- Save, reopen, print, and recover an unsaved practice.
- Export and import the drill spreadsheet.
- Create and restore a database backup.

## Packaging

- Build `WildcatTrainingPlanner.exe` from a clean environment.
- Confirm the executable name, icon, window title, version, and documentation.
- Test on a Windows account that has no existing application data.
- Confirm user data is written outside the installed executable.
- Archive the tested build and tag the matching source revision.
