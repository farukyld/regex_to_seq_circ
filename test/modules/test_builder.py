import json

from pycde import System

from backend.builder import seq_circt_builder
from backend.circuit_deser import CircuitDeser
from util.move_build_params_to_hw import move_build_params_from_json_to_sv_in_output_directory
from util.path_shortcuts import get_random_output_dir_json_path
from util.color_print import introduce, print_red


if __name__ == "__main__":
  introduce(__file__)
  output_dir, json_path = get_random_output_dir_json_path()
  if not json_path:
    print_red("test_builder will work only with an existing json file")
    exit(1)

  with open(json_path, "r") as f:
    json_obj = json.load(f)
  formal_circuit = CircuitDeser.from_dict(json_obj)

  top_module = seq_circt_builder(formal_circuit)

  system = System([top_module], name="seq_circuit",
                  output_directory=output_dir)

  system.compile()
  move_build_params_from_json_to_sv_in_output_directory(output_dir)