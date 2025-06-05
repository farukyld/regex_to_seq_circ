# ask chatGPT to fix the docstring:
# see: https://chatgpt.com/share/6709469b-8990-800f-b1c4-9d9d900b7468
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
    if calculate_skip(node.right):
      return calculate_out(node.left).union(calculate_out(node.right))
    else:
      return calculate_out(node.right)
  elif node.operation == OperationType.ZER_MOR or node.operation == OperationType.ZER_ONE or node.operation == OperationType.ONE_MOR:
    return calculate_out(node.left)


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
    if calculate_skip(node.left):
      right_trig_h = calculate_out(node.left).union(h)
    else:
      right_trig_h = calculate_out(node.left)
    return calculate_trig(node.left, h).union(
        calculate_trig(node.right, right_trig_h))
  elif node.operation == OperationType.ZER_MOR or node.operation == OperationType.ONE_MOR:
    return calculate_trig(node.left, calculate_out(node.left).union(h))
  elif node.operation == OperationType.ZER_ONE:
    return calculate_trig(node.left, h)


def generate_regex_from_ast(node: RegexASTNode) -> str:
  if not isinstance(node,RegexASTNode):
    raise TypeError("node must be type of RegexASTNode")

  if node.operation == OperationType.LITERAL:
    return node.char
  elif node.operation == OperationType.UNION:
    left_pattern = generate_regex_from_ast(node.left)
    right_pattern = generate_regex_from_ast(node.right)
    return "(" + left_pattern + "|" + right_pattern + ")"
  elif node.operation == OperationType.CONCAT:
    left_pattern = generate_regex_from_ast(node.left)
    right_pattern = generate_regex_from_ast(node.right)
    return left_pattern + ";" + right_pattern
  elif node.operation == OperationType.ZER_MOR:
    left_pattern = generate_regex_from_ast(node.left)
    return "(" + left_pattern + ")*"
  elif node.operation == OperationType.ONE_MOR:
    left_pattern = generate_regex_from_ast(node.left)
    return "(" + left_pattern + ")+"
  elif node.operation == OperationType.ZER_ONE:
    left_pattern = generate_regex_from_ast(node.left)
    return "(" + left_pattern + ")?"


def circuit_dict(node: RegexASTNode, full_match=True) -> str:
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

  regex = generate_regex_from_ast(node)
  circuit_dict = {
      "regex_canonical": regex,
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

  return circuit_dict
