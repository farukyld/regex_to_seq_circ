import pyparsing as pp
from frontend.regex_ast_node import RegexASTNode
from frontend.ast_to_formal_circuit import calculate_trig

# see: https://github.com/pyparsing/pyparsing/blob/master/examples/simpleArith.py


def repetition_action(tokens_or_ast_nodes):
  ast_node = tokens_or_ast_nodes[0][0]
  operator = tokens_or_ast_nodes[0][1]
  return RegexASTNode.from_repetition(ast_node, operator)


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

  def fold(nodes: list[RegexASTNode]):
    return [RegexASTNode.from_binary(l, r, op)
            for l, r in zip(nodes[::2], nodes[1::2])]

  while len(nodes) >= 2:
    if len(nodes) % 2 == 0:
      nodes = fold(nodes)
    else:
      excess = nodes.pop()
      nodes = fold(nodes)
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

# for debugging
if __name__ == "__main__":
  test_cases = [
      "a?",
      "(a;b|b)*;b;a",
      "a|a|a|a|a",
      "a",
      "(a)",
      "a*",
      "a+",
      "a?",
      "a|b;c",
      "a|b|c",
      "a;b|c",
      "a+;b+",
      "a+;b*",
      "a+;b?",
      "a*;b*",
      "a*;b+",
      "a*;b?",
      "a?;b?",
      "a?;b+",
      "a?;b*",
      "a|b",
      "a;b",
      "a;(a|b)*",
      "(a;b|b)*;b+;a?",
  ]

  test_results = {}
  for test_case in test_cases:
    print("test case: ", test_case)
    parse_result = reg_exp.parse_string(test_case)
    test_results[test_case] = parse_result[0]

  trig_E_1 = calculate_trig(
      test_results["(a;b|b)*;b;a"], frozenset({1}))
  trig_E_0 = calculate_trig(
      test_results["(a;b|b)*;b;a"], frozenset({0}))

  print("done")
