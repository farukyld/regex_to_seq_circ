import json
from frontend.ast_to_formal_circuit import circuit_dict
from frontend.regex_ast_node import RegexASTNode
from util.path_shortcuts import get_next_unused_output_dir_and_json, get_first_existing_output_dir_json_path
from util.color_print import introduce

# for debugging
if __name__ == "__main__":
  introduce(__file__)
  literal1 = RegexASTNode.from_literal('a')
  literal2 = RegexASTNode.from_literal('b')
  literal3 = RegexASTNode.from_literal('b')
  literal4 = RegexASTNode.from_literal('b')
  literal5 = RegexASTNode.from_literal('a')
  concat1 = RegexASTNode.from_binary(literal1, literal2, ';')
  union1 = RegexASTNode.from_binary(concat1, literal3, '|')
  zero_or_more1 = RegexASTNode.from_repetition(union1, '*')
  concat2 = RegexASTNode.from_binary(zero_or_more1, literal4, ';')
  concat3 = RegexASTNode.from_binary(concat2, literal5, ';')

  _, json_path = get_first_existing_output_dir_json_path()
  if not json_path:
    odir, json_path = get_next_unused_output_dir_and_json()
    odir.mkdir()

  with open(json_path, "w") as file:
    file.write(json.dumps(circuit_dict(concat3), indent=2))

  print("done")
