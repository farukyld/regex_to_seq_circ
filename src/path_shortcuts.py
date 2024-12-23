from pathlib import Path

OUTPUTS_PARENT = Path(__file__).parent.parent / "build"
INTER_OUTPUTS = OUTPUTS_PARENT / "inter"
FINAL_OUTPUTS = OUTPUTS_PARENT / "final"

TEST_0_JSON_PATH = INTER_OUTPUTS / "circuit_json.json"
OUTPUT_DIR_SUFFIX = "_output"


def extract_file_name(full_file_path: str) -> str:
  return Path(full_file_path).name.replace('.', '_')


def generate_sv_output_dir_name(full_file_path: str) -> str:
  return FINAL_OUTPUTS / (extract_file_name(full_file_path) + OUTPUT_DIR_SUFFIX)

INTER_OUTPUTS.mkdir(parents=True, exist_ok=True)
FINAL_OUTPUTS.mkdir(parents=True, exist_ok=True)



if __name__ =="__main__":
  print(OUTPUTS_PARENT, INTER_OUTPUTS, FINAL_OUTPUTS)
