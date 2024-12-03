from pathlib import Path

OUTPUTS_PARENT = Path(__file__).parent
OUTPUT_DIR_SUFFIX = "_output"


def extract_file_name(full_file_path: str) -> str:
  return Path(full_file_path).name.replace('.', '_')


def generate_output_dir_name(full_file_path: str) -> str:
  return OUTPUTS_PARENT / (extract_file_name(full_file_path) + OUTPUT_DIR_SUFFIX)
