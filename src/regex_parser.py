import pyparsing as pp
from regex_ast_node import RegexASTNode


no_action = 0


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
if not no_action:
  character_exp.add_parse_action(character_action)

union = "|"
concatenation = ";"
repetition = pp.one_of("* + ?")

if no_action:
  reg_exp = pp.infix_notation(
      character_exp,
      [
          (repetition, 1, pp.opAssoc.LEFT),
          (concatenation, 2, pp.opAssoc.LEFT),
          (union, 2, pp.opAssoc.LEFT),
      ]
  )
else:
  reg_exp = pp.infix_notation(
      character_exp,
      [
          (repetition, 1, pp.opAssoc.LEFT, repetition_action),
          (concatenation, 2, pp.opAssoc.LEFT, binary_op_action),
          (union, 2, pp.opAssoc.LEFT, binary_op_action),
      ]
  )


test_cases = [
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


if not no_action:
  test_results = {}
for test_case in test_cases:
  print("test case: ", test_case)
  parse_result = reg_exp.parse_string(test_case)
  if no_action:
    print(parse_result[0])
  else:
    test_results[test_case] = parse_result[0]

if not no_action:
  print("done")
