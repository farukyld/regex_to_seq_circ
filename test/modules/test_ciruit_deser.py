
import json
from backend.circuit_deser import CircuitDeser
from util.path_shortcuts import get_any_output_dir_and_json
from util.color_print import introduce


if __name__ == "__main__":
  introduce(__file__)
  _, json_path = get_any_output_dir_and_json()
  with open(json_path, "r") as file:
    circuit_info = json.load(file)
    circuit_obj = CircuitDeser.from_dict(circuit_info)
