import pyparsing as pp


def repetition_action(tokens_or_ast_node):
  pass


def concatenation_action(tokens_or_ast_node):
  pass


def union_action(tokens_or_ast_node):
  pass


character_exp = pp.Word(pp.alphanums, exact=1)

union = "|"
concatenation = ";"
repetition = pp.one_of("* + ?")

reg_exp = pp.infix_notation(
    character_exp,
    [
        (repetition, 1, pp.opAssoc.LEFT, repetition_action),
        (concatenation, 2, pp.opAssoc.LEFT, concatenation_action),
        (None, 2, pp.opAssoc.LEFT, concatenation_action),
        (union, 2, pp.opAssoc.LEFT, union_action)
    ]
)


test_cases = [
    "a",
    "aa",
    "(a)",
    "a|b",
    "a;b",
    "a;(a|b)*",
    "(a;b|b)*;b+;a?",
]
for test_case in test_cases:
  print("test case: ", test_case)
  parse_result = reg_exp.parse_string(test_case)
  print(parse_result)
