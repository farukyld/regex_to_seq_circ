from pathlib import Path

MAX_OUTPUTS = 100
OUTPUTS_PARENT = Path(__file__).parent.parent / "build"
INTER_OUTPUTS = OUTPUTS_PARENT / "inter"
FINAL_OUTPUTS = OUTPUTS_PARENT / "final"

TEST_0_JSON_PATH = INTER_OUTPUTS / "circuit_json.json"

INTER_OUTPUTS.mkdir(parents=True, exist_ok=True)
FINAL_OUTPUTS.mkdir(parents=True, exist_ok=True)


def _get_oldest_or_next_output(base_dir: Path, suffix: str = "") -> Path:
  """
  Get the next available or oldest reusable output path.
  """
  candidates = []
  for i in range(1, MAX_OUTPUTS + 1):
    name = f"output_{i:03d}{suffix}"
    path = base_dir / name
    if not path.exists():
      return path  # available slot
    stat = path.stat()
    candidates.append((stat.st_mtime, path))

  # All slots taken — return the oldest one
  candidates.sort()
  return candidates[0][1]


def generate_sv_output_dir_name() -> Path:
  """
  Generate or reuse an output directory under FINAL_OUTPUTS.
  """
  path = _get_oldest_or_next_output(FINAL_OUTPUTS)
  return path


def generate_json_output_path() -> Path:
  """
  Generate or reuse a JSON file path under INTER_OUTPUTS.
  """
  path = _get_oldest_or_next_output(INTER_OUTPUTS, suffix=".json")
  return path


# For testing
if __name__ == "__main__":
  generate_sv_output_dir_name().mkdir(exist_ok=True,parents=True)
  print("SV output dir:", generate_sv_output_dir_name())
  print("JSON output path:", generate_json_output_path())
