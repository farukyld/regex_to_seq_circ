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
import clean
import path_shortcuts


BLK = "\033[30m"
RED = "\033[31m"
GRN = "\033[32m"
YLW = "\033[33m"
BLU = "\033[34m"
MGT = "\033[35m"
CYN = "\033[36m"
WTE = "\033[37m"
DEF = "\033[0m"


def print_green(*args):
  print(GRN, end="")
  print(*args)
  print(DEF, end="")


def print_cyan(*args):
  print(CYN, end="")
  print(*args)
  print(DEF, end="")


print_cyan("removing all content of build")
clean.remove_all_build_content()
print_green("removed")


patterns = ["(a;b|b)*;b;a"]
patterns += [regex_normalizer.insert_semicolon_as_concat(
    generate_grep_style.generate_expr(max_depth=6)) for _ in range(3)]

for pattern in patterns:
  print_cyan(f"parsing regex: {pattern}")
  ast_root = regex_parser.regex_pattern_to_ast(pattern)
  print_green("parsed")

  print_cyan(
      "creating the formal definition of sequential circuit and serializing")
  circt_dict = ast_to_formal_circuit.circuit_dict(ast_root, False, pattern)
  print_green("created, serialized")

  print_cyan(
      f"dumping formal definition into {path_shortcuts.TEST_0_JSON_PATH}")
  with open(path_shortcuts.TEST_0_JSON_PATH, "w") as f:
    f.write(json.dumps(circt_dict, indent=2))
  print_green("dumped")

  print_cyan("deserializing json string representing formal definition")
  deserialized = circuit_deser.CircuitDeser.from_dict(circt_dict)
  print_green("deserialized")

  output_dir = path_shortcuts.generate_sv_output_dir_name(__file__)
  print_cyan(
      f"building system verilog output under {output_dir}")
  system = pycde.System([builder.seq_circt_builder(deserialized)], name="seq_circuit",
                        output_directory=output_dir)
  system.compile()
  print_green("built")
  print_green("----\n"
              "done")
