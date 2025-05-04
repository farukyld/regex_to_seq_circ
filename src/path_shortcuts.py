from pathlib import Path
from typing import Union

MAX_OUTPUTS = 100
OUTPUTS_PARENT = Path(__file__).parent.parent / "build"
OUTPUTS_PARENT.mkdir(exist_ok=True, parents=True)
_JSON_FILE_NAME = "formal.json"


def get_next_output_dir_and_json() -> tuple[Path, Path]:
  """
  Get the next available or oldest reusable output path.
  """
  candidates: list[tuple[float, Path]] = []
  for i in range(1, MAX_OUTPUTS + 1):
    name = f"output_{i:03d}"
    path = OUTPUTS_PARENT / name
    if not path.exists():
      path.mkdir()
      return path, path / _JSON_FILE_NAME  # available slot
    stat = path.stat()
    candidates.append((stat.st_mtime, path))

  # All slots taken — return the oldest one
  candidates.sort()
  dir_name = candidates[0][1]
  return dir_name, dir_name / _JSON_FILE_NAME


def get_any_output_dir_and_json() -> tuple[Path, Path]:
  """
  Return the first existing output directory and its JSON file.
  """
  for i in range(1, MAX_OUTPUTS + 1):
    name = f"output_{i:03d}"
    path = OUTPUTS_PARENT / name
    if path.exists():
      return path, path / _JSON_FILE_NAME
