# see: https://chatgpt.com/share/683d395d-4424-800f-b95c-c6fc9f59acbf
import json
from pathlib import Path
from util.simple_test_cases import (
    benchmarking_caconical_forms, benchmarking_compact_forms)


def move_build_params_from_json_to_sv_in_output_directory(output_dir: Path):
  sv_file = list((output_dir / "hw").glob("*.sv"))[0]
  json_file = list((output_dir).glob("*.json"))[0]
  with open(json_file, "r") as f:
    json_obj = json.load(f)

  regex_canonical = json_obj["regex_canonical"]
  regex = benchmarking_caconical_forms.get(regex_canonical, "<unknown>")
  regex_compact = benchmarking_compact_forms.get(regex, "<unknown>")
  full_match = json_obj["full_match"]
  header = f"""// regex_canonical: {regex_canonical}
// regex: {regex}
// regex_compact: {regex_compact}
// full_match: {full_match}
  """
  sv_file.write_text(header + sv_file.read_text())