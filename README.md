# Wildcat Training Planner

Wildcat Training Planner helps coaches build purposeful practices, maintain a drill
library, assign coaches, and print complete practice plans.

## Features

Maintain a reusable development drill library
Organize drills into configurable development blocks
Build practices and assign blocks to coaches
Calculate activity and practice times in minutes and seconds
Save and reopen practice plans
Print practices or export them as PDF files
Highlight web addresses included in printed and exported drill information
Import and export drills using spreadsheets
Automatically recover unsaved practice work
Back up and restore application data

## Requirements

Windows 10 or Windows 11
Python 3.12 or later when running from source
The packaged Windows executable does not require a separate Python installation.

## Run from source

Create and activate a Python virtual environment, then install the project dependencies:

1. python -m venv venv
2. .\venv\Scripts\Activate.ps1
3. python -m pip install -r requirements-dev.txt
4. python main.py

For testing and packaging tools, install `requirements-dev.txt` instead.

Practice plans are stored as portable JSON files. The application also keeps a
local recovery draft every 15 seconds while a practice is being edited.

## Run the Packaged Application

Open:
Training Planner.exe

Application data is stored separately from the executable, so replacing the executable does not remove the drill library, settings, or saved practices.

## Application Data

The packaged application stores its working data under:

%LOCALAPPDATA%\TrainingPlannerAp

## Test

Run `python -m unittest discover -s tests -p "test_*.py" -v`.

The preferred complete check is `python -m pytest -q`.

Run `python -m ruff check app tests main.py` for static quality checks. Before
packaging a release, complete `docs/RELEASE_CHECKLIST.md`.

## Keyboard shortcuts

- Ctrl+N — new practice
- Ctrl+O — open practice
- Ctrl+S — save practice
- Ctrl+P — print practice

See `docs/User_Manual.md` for instructions on configuring and using the application.
