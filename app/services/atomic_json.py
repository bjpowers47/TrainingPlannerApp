"""Crash-resistant JSON file writing."""

import json
import os
import tempfile
from pathlib import Path


def write_json_atomic(file_path: Path | str, data, *, indent=4) -> None:
    """Write JSON completely before replacing an existing destination."""
    destination = Path(file_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=destination.parent, delete=False
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(data, temporary_file, indent=indent)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        temporary_path.replace(destination)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()
