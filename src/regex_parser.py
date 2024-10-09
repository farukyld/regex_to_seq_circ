import pyparsing as pp
from regex_ast_node import RegexASTNode


no_action = 1


def repetition_action(tokens_or_ast_nodes):
  if isinstance(tokens_or_ast_nodes[0],RegexASTNode):
    ast_node = tokens_or_ast_nodes[0]
    operator = tokens_or_ast_nodes[1]
    print("repetition, tokens[0] is instance Node")
  else:
    ast_node = tokens_or_ast_nodes[0][0]
    operator = tokens_or_ast_nodes[0][1]
    print("repetition, tokens[0] is NOT instance Node")
  return RegexASTNode.from_repetition(ast_node, operator)


def binary_op_action(tokens_or_ast_nodes):
  left = tokens_or_ast_nodes[0][0]
  op = tokens_or_ast_nodes[0][1]
  right = tokens_or_ast_nodes[0][2]
  return RegexASTNode.from_binary(left, right, op)


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
    "a",
    "(a)",
    "a*",
    "a+",
    "a?",
    "a|b;c",
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

for test_case in test_cases:
  print("test case: ", test_case)
  parse_result = reg_exp.parse_string(test_case)
  print(parse_result)
