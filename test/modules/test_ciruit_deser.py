
import json
from backend.circuit_deser import CircuitDeser
from util.path_shortcuts import get_random_output_dir_json_path
from util.color_print import introduce, print_red


if __name__ == "__main__":
  introduce(__file__)
  _, json_path = get_random_output_dir_json_path()
  if not json_path:
    print_red("test_circuit_deser will work only with an existing json file")
    exit(1)
  with open(json_path, "r") as file:
    circuit_info = json.load(file)
    circuit_obj = CircuitDeser.from_dict(circuit_info)
