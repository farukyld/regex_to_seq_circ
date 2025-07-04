# contrast to my convention of importing the objects,
# I impot only modules and access objects via module.object
# to show what comes from where in this file.

import json
import random

import pycde

from backend import builder
from backend import circuit_deser
from frontend import ast_to_formal_circuit
from frontend import regex_parser
from util import generate_grep_style, color_print, clean, path_shortcuts, simple_test_cases, move_build_params_to_hw
from frontend import regex_normalizer

color_print.introduce(__file__)
color_print.print_cyan("removing all content of build")
clean.remove_output_directories()
color_print.print_green("removed")


# patterns = simple_test_cases.health_check
patterns = simple_test_cases.benchmarking
# patterns += [regex_normalizer.insert_semicolon_as_concat(
#     generate_grep_style.generate_expr(max_depth=6)) for _ in range(3)]

for pattern in patterns:
  color_print.print_cyan(f"parsing regex: {pattern}")
  ast_root = regex_parser.regex_pattern_to_ast(pattern)
  color_print.print_green("parsed")

  for partial_match in [True,False]:
    color_print.print_cyan(
        f"creating the formal definition of sequential circuit with partial match: {partial_match} and serializing")
    circt_dict = ast_to_formal_circuit.circuit_dict(ast_root, partial_match)
    color_print.print_green("created, serialized")

    output_dir, json_path = path_shortcuts.get_next_unused_output_dir_and_json()
    output_dir.mkdir()
    color_print.print_cyan(
        f"dumping formal definition into {json_path}")
    with open(json_path, "w") as f:
        f.write(json.dumps(circt_dict, indent=2))
    color_print.print_green("dumped")

    color_print.print_cyan(
        "deserializing json string representing formal definition")
    deserialized = circuit_deser.CircuitDeser.from_dict(circt_dict)
    color_print.print_green("deserialized")

    color_print.print_cyan(
        f"building system verilog output under {output_dir}")
    system = pycde.System([builder.seq_circt_builder(deserialized)], name="seq_circuit",
                            output_directory=output_dir)
    system.compile()
    move_build_params_to_hw.move_build_params_from_json_to_sv_in_output_directory(output_dir)
    color_print.print_green("built")
    color_print.print_green("----\n"
                            "done")
