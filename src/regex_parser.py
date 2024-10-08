import pyparsing as pp


reg_exp = pp.Forward()


paranthese_depth = 0


def increment_paranthese_depth():
  global paranthese_depth
  paranthese_depth = paranthese_depth + 1
  return paranthese_depth

def decrement_paranthese_depth():
  global paranthese_depth
  return_val = paranthese_depth
  paranthese_depth = paranthese_depth - 1
  return return_val

def also_return_a_floating_value():
  return 1.2

character_exp = pp.Word(pp.alphanums, exact=1)

open_paranthese = pp.Literal("(")

close_paranthese = pp.Literal(")")

paranthese_exp = open_paranthese + reg_exp + close_paranthese

# these two creates infinity recursion
# union_exp = reg_exp + "|" + reg_exp
# concat_exp = reg_exp + ";" + reg_exp

union_exp = pp.infix_notation()

# zero_or_more_exp = reg_exp + "*"
# one_or_more_exp = reg_exp + "+"
# zero_or_one_exp = reg_exp + "?"
reg_exp <<= paranthese_exp | character_exp

# reg_exp <<= (character_exp | union_exp | paranthese_exp | concat_exp
#  | zero_or_one_exp | one_or_more_exp | zero_or_one_exp)


test_cases = [
    "a",
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
