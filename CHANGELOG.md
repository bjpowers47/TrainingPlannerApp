# Changelog

## 0.3.0

- Renamed the product to Training Planner Ap.
- Added practice autosave, recovery, recent practices, and safer file opening.
- Replaced the redundant startup recovery popup with a clear Continue Unsaved Practice dashboard action.
- Added recent-practice list management and accurate saved-versus-unsaved draft detection.
- Removed the former Soccer wording from user-visible messages and generated practice plans.
- Added a configurable 15-character Sport field used before Training Manager in user-facing text.
- Shortened the left sidebar heading to Training Planner.
- Prevented removed or renamed coaches from appearing in practice printouts.
- Made database restore replace drills and blocks exactly and refresh the app immediately.
- Removed the unused pandas dependency so 32-bit Windows packaging can install cleanly.
- Corrected Windows print-dialog structure packing in the 32-bit executable.
- Changed coach-facing work and rest durations from seconds to minutes while retaining legacy import support.
- Added row-level error details to the drill import report.
- Added complete text reports beside spreadsheets with import errors or duplicates.
- Made drill imports reactivate or create spreadsheet Development Blocks and preserve unmatched Coaching Focus text.
- Added Up and Down controls for reordering Development Blocks in Configuration.
- Added drag-and-drop Development Block reordering in Administration Configuration.
- Replaced the Drag label with a three-dot handle and documented block reordering in the user manual.
- Added Unassigned block tracking to the Practice Summary and printed practice plans.
- Added keyboard shortcuts and persistent window sizing.
- Added working drill search, block filtering, and undoable drill removal.
- Added visible duration validation and practice-overrun feedback.
- Improved spreadsheet-import boundaries and automated-test reliability.
