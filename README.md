# Training Planner Ap

Training Planner Ap helps coaches build purposeful practices, maintain a drill
library, assign coaches, and print complete practice plans.

## Run from source

1. Create and activate a Python virtual environment.
2. Install `requirements.txt`.
3. Run `python main.py`.

For testing and packaging tools, install `requirements-dev.txt` instead.

Practice plans are stored as portable JSON files. The application also keeps a
local recovery draft every 15 seconds while a practice is being edited.

## Test

Run `python -m unittest discover -s tests -p "test_*.py" -v`.

The preferred complete check is `python -m pytest -q`.

## Keyboard shortcuts

- Ctrl+N — new practice
- Ctrl+O — open practice
- Ctrl+S — save practice
- Ctrl+P — print practice
