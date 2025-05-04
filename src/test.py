# contrast to my convention of importing the objects,
# I impot only modules and access objects via module.object
# to show what comes from where in this file.

import json

import pycde

from backend import builder
from backend import circuit_deser
from frontend import ast_to_formal_circuit
from frontend import regex_parser
from frontend import generate_grep_style
from frontend import regex_normalizer
import color_print
import simple_test_cases
import clean
import path_shortcuts

color_print.introduce(__file__)
color_print.print_cyan("removing all content of build")
clean.remove_output_directories()
color_print.print_green("removed")


patterns = simple_test_cases.regexes_with_semicolon
patterns += [regex_normalizer.insert_semicolon_as_concat(
    generate_grep_style.generate_expr(max_depth=6)) for _ in range(3)]

for pattern in patterns:
  color_print.print_cyan(f"parsing regex: {pattern}")
  ast_root = regex_parser.regex_pattern_to_ast(pattern)
  color_print.print_green("parsed")

  color_print.print_cyan(
      "creating the formal definition of sequential circuit and serializing")
  circt_dict = ast_to_formal_circuit.circuit_dict(ast_root, False, pattern)
  color_print.print_green("created, serialized")

  output_dir,json_path = path_shortcuts.get_next_output_dir_and_json()
  color_print.print_cyan(
      f"dumping formal definition into {json_path}")
  with open(json_path, "w") as f:
    f.write(json.dumps(circt_dict, indent=2))
  color_print.print_green("dumped")

  color_print.print_cyan("deserializing json string representing formal definition")
  deserialized = circuit_deser.CircuitDeser.from_dict(circt_dict)
  color_print.print_green("deserialized")

  color_print.print_cyan(
      f"building system verilog output under {output_dir}")
  system = pycde.System([builder.seq_circt_builder(deserialized)], name="seq_circuit",
                        output_directory=output_dir)
  system.compile()
  color_print.print_green("built")
  color_print.print_green("----\n"
              "done")
