from pathlib import Path
import random

from util.color_print import print_red

# see: https://chatgpt.com/share/68243ba9-8c88-800f-9761-c0f4175e5125
MAX_OUTPUTS = 100
OUTPUTS_PARENT = Path(__file__).parent.parent.parent / "build"
OUTPUTS_PARENT.mkdir(exist_ok=True, parents=True)
_JSON_FILE_NAME = "formal.json"
_HW_DIR_NAME = "hw"
_LAST_INDEX_FILE = OUTPUTS_PARENT / ".last_index_used.txt"


def get_next_unused_output_dir_and_json() -> tuple[Path, Path] | tuple[None, None]:
  """
  Return the next unused output directory and its json path, creating it is left to caller.
  If all allowed output names (output_xxx) are used, return None,None.
  """
  for i in range(1, MAX_OUTPUTS + 1):
    name = f"output_{i:03d}"
    path = OUTPUTS_PARENT / name
    if not path.exists():
      path.mkdir()
      return path, path / _JSON_FILE_NAME  # available slot
  return None, None


def get_first_existing_output_dir_json_path() -> tuple[Path, Path] | tuple[None, None]:
  """
  returns output directory and its json path with the smallest timestamp.
  if no output directory, return None,None.
  """
  candidates: list[tuple[float, Path]] = []
  for i in range(1, MAX_OUTPUTS + 1):
    name = f"output_{i:03d}"
    path = OUTPUTS_PARENT / name
    if path.exists():
      stat = path.stat()
      candidates.append((stat.st_mtime, path))

  # all existing canditates are appended
  candidates.sort()
  dir_path = candidates[0][1]
  return dir_path, dir_path / _JSON_FILE_NAME


def get_next_existing_output_dir_json_path() -> tuple[Path, Path]:
  """
  return the directory and its json path whose name comes after saved name. 
  if there is no such ones, return the ones with the smallest timestamp.
  """
  try:
    last_index = int(_LAST_INDEX_FILE.read_text().strip())
  except Exception:
    last_index = 0

  for i in range(last_index + 1, MAX_OUTPUTS):
    path = OUTPUTS_PARENT / f"output_{i:03d}"
    if path.exists():
      _LAST_INDEX_FILE.write_text(str(i))
      return path, path / _JSON_FILE_NAME

  path, json = get_first_existing_output_dir_json_path()
  last_index = int(path.name[-3:])
  _LAST_INDEX_FILE.write_text(str(last_index))

  return path, json


def get_random_output_dir_json_path() -> tuple[Path, Path] | tuple[None, None]:
  """
  Returns a random existing output directory and its json path.
  """
  existing_paths = [
      OUTPUTS_PARENT / f"output_{i:03d}"
      for i in range(1, MAX_OUTPUTS + 1)
      if (OUTPUTS_PARENT / f"output_{i:03d}").exists()
  ]

  if not existing_paths:
    return None, None

  choice = random.choice(existing_paths)
  return choice, choice / _JSON_FILE_NAME
