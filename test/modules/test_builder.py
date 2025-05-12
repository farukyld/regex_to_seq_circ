import json

from pycde import System

from backend.builder import seq_circt_builder
from backend.circuit_deser import CircuitDeser
from util.path_shortcuts import get_any_output_dir_and_json
from util.color_print import introduce


if __name__ == "__main__":
  introduce(__file__)
  output_dir, json_path = get_any_output_dir_and_json()
  with open(json_path, "r") as f:
    json_obj = json.load(f)
  formal_circuit = CircuitDeser.from_dict(json_obj)

  top_module = seq_circt_builder(formal_circuit)

  system = System([top_module], name="seq_circuit",
                  output_directory=output_dir)

  system.compile()
