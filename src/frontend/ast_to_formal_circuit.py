
# ask chatGPT to fix the docstring:
# see: https://chatgpt.com/share/6709469b-8990-800f-b1c4-9d9d900b7468
import json

from path_shortcuts import TEST_0_JSON_PATH
from frontend.regex_ast_node import OperationType, RegexASTNode


class NotSupportedConversion(Exception):
  """
  Exception raised when attempting to convert a
  node to a circuit JSON, where none of the node's
  children is in the first position of the regular
  expression having been parsed. <\p>
  or user may have forgotten to RegexASTNode.reset_class_variables before starting to parse a new regex. 
  """
  pass


def calculate_skip(node: RegexASTNode) -> bool:
  if not isinstance(node, RegexASTNode):
    print(type(node))
    print(RegexASTNode)
    raise TypeError("node must be type of RegexASTNode")

  if node.operation == OperationType.LITERAL:
    return False
  elif node.operation == OperationType.UNION:
    return calculate_skip(node.left) or calculate_skip(node.right)
  elif node.operation == OperationType.CONCAT:
    return calculate_skip(node.left) and calculate_skip(node.right)
  elif node.operation == OperationType.ZER_MOR or node.operation == OperationType.ZER_ONE:
    return True
  elif node.operation == OperationType.ONE_MOR:
    return calculate_skip(node.left)


def calculate_out(node: RegexASTNode) -> frozenset[int]:
  if not isinstance(node, RegexASTNode):
    raise TypeError("node must be type of RegexASTNode")
  if node.operation == OperationType.LITERAL:
    return frozenset({node.position})
  elif node.operation == OperationType.UNION:
    return calculate_out(node.left).union(calculate_out(node.right))
  elif node.operation == OperationType.CONCAT:
    # TODO check if this needs to be copy
    return calculate_out(node.left).union(
        calculate_out(node.right)) if calculate_skip(node.right) else calculate_out(node.right).copy()
  elif node.operation == OperationType.ZER_MOR or node.operation == OperationType.ZER_ONE or node.operation == OperationType.ONE_MOR:
    # TODO check if this needs to be copy
    return calculate_out(node.left).copy()

# TODO check if h needs to be set to {0} as default
def calculate_trig(node: RegexASTNode, h: frozenset[int] = frozenset({0})) -> set[tuple[int, str, frozenset[int]]]:
  if not isinstance(node, RegexASTNode):
    print(type(node))
    print(RegexASTNode)
    raise TypeError("node must be type of RegexASTNode")
  if not isinstance(h, frozenset):
    raise TypeError("h must be type of frozenset")

  if node.operation == OperationType.LITERAL:
    return {(node.position, node.char, h)}
  elif node.operation == OperationType.UNION:
    return calculate_trig(node.left, h).union(
        calculate_trig(node.right, h))
  elif node.operation == OperationType.CONCAT:
    # TODO check if this needs to be copy
    right_trig_h = calculate_out(node.left).union(
        h) if calculate_skip(node.left) else calculate_out(node.left)
    return calculate_trig(node.left, h).union(
        calculate_trig(node.right, right_trig_h))
  elif node.operation == OperationType.ZER_MOR or node.operation == OperationType.ONE_MOR:
    # TODO check if this needs to be copy
    return calculate_trig(node.left, calculate_out(node.left).union(h))
  elif node.operation == OperationType.ZER_ONE:
    return calculate_trig(node.left, h)


def circuit_json(node: RegexASTNode, full_match=True, regex="") -> str:
  if not isinstance(node, RegexASTNode):
    raise TypeError("node must be type of RegexASTNode")
  left_most_leaf = node
  while left_most_leaf.left:
    left_most_leaf = left_most_leaf.left
  # since we use left child for unary operations,
  # left-most child of a node must be a LITERAL (char)
  # and has a globally determined position attached to it
  # i.e. position is not relative to any of parent nodes,
  # it is relative to the entire reg_exp having been parsed
  if left_most_leaf.position != 1:
    raise NotSupportedConversion(
        "not should contain the LITERAL at the first position as its left-most children")

  circuit_dict = {
      "regex": regex,
      "n_states": RegexASTNode._literals_created + 1,
      "full_match": full_match,
      "accept_states": list(calculate_out(node)),
      "transitions": [
          {
              "to_state": i,
              "must_read": a,
              "from_states": list(h),
          } for i, a, h in calculate_trig(node)
      ]
  }

  json_str = json.dumps(circuit_dict, indent=2)
  return json_str



# for debugging
if __name__ == "__main__":
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
  with open(TEST_0_JSON_PATH, "w") as file:
    file.write(circuit_json(concat3))

  print("done")
