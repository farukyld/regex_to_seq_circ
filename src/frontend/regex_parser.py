import pyparsing as pp
from frontend.regex_ast_node import RegexASTNode
from frontend.ast_to_formal_circuit import calculate_trig

# see: https://github.com/pyparsing/pyparsing/blob/master/examples/simpleArith.py


def repetition_action(tokens_or_ast_nodes):
  ast_node = tokens_or_ast_nodes[0][0]
  operator_queue:list[RegexASTNode] = tokens_or_ast_nodes[0][1:]
  operator_queue.reverse()
  while len(operator_queue) >= 1:
    ast_node = RegexASTNode.from_repetition(ast_node, operator_queue.pop())
  return ast_node


def binary_op_action(tokens_or_ast_nodes):
  # unfortunately, pyparsing doesn't create
  # a left associative decomposition of a;b;c
  # instead, it generates a shallow decomposition:
  #    ;
  #  / | \
  # a  b  c
  # I convert this into a tree that each
  # node has at most 2 children

  # skip every other element, even indexes are nodes, odd indexes are operators
  nodes = tokens_or_ast_nodes[0][::2]
  op = tokens_or_ast_nodes[0][1]

  def fold_binary(nodes: list[RegexASTNode]):
    return [RegexASTNode.from_binary(l, r, op)
            for l, r in zip(nodes[::2], nodes[1::2])]

  while len(nodes) >= 2:
    if len(nodes) % 2 == 0:
      nodes = fold_binary(nodes)
    else:
      excess = nodes.pop()
      nodes = fold_binary(nodes)
      nodes.append(excess)

  return nodes[0]


def character_action(tokens_or_ast_nodes):
  return RegexASTNode.from_literal(tokens_or_ast_nodes[0])


character_exp = pp.Word(pp.alphanums, exact=1)
character_exp.add_parse_action(character_action)

union = "|"
concatenation = ";"
repetition = pp.one_of("* + ?")

reg_exp = pp.infix_notation(
    character_exp,
    [
        (repetition, 1, pp.opAssoc.LEFT, repetition_action),
        (concatenation, 2, pp.opAssoc.LEFT, binary_op_action),
        (union, 2, pp.opAssoc.LEFT, binary_op_action),
    ]
)


# see: https://chatgpt.com/share/6707a7b0-3b8c-800f-9754-eb98f105c56f
line_start = pp.LineStart()
line_start.add_parse_action(RegexASTNode.reset_class_variables)
reg_exp = line_start + reg_exp

def regex_pattern_to_ast(pattern: str) -> RegexASTNode:
  return reg_exp.parse_string(pattern,parse_all=True)[0]

# for debugging
if __name__ == "__main__":
  from src.simple_test_cases import regexes_with_semicolon
  test_results = {}
  for test_case in regexes_with_semicolon:
    print("test case: ", test_case)
    # see: https://chatgpt.com/share/6805cea4-1810-800f-bc56-f79c9aca6dd5
    parse_result = reg_exp.parse_string(test_case,parse_all=True)
    test_results[test_case] = parse_result[0]

  trig_E_1 = calculate_trig(
      test_results["(a;b|b)*;b;a"], frozenset({1}))
  trig_E_0 = calculate_trig(
      test_results["(a;b|b)*;b;a"], frozenset({0}))

  print("done")
