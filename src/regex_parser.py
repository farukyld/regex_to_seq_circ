import pyparsing as pp


reg_exp = pp.Forward()

character_exp = pp.Word(pp.alphanums, exact=1)
character_exp.add_parse_action(lambda: print("parsing a character_exp"))

paranthese_exp = pp.Literal("(") + reg_exp + ")"
paranthese_exp.add_parse_action(lambda : print("parsing a paranthese_exp"))

# union_exp = reg_exp + "|" + reg_exp
# concat_exp = reg_exp + ";" + reg_exp
# zero_or_more_exp = reg_exp + "*"
# one_or_more_exp = reg_exp + "+"
# zero_or_one_exp = reg_exp + "?"
reg_exp <<= paranthese_exp |character_exp

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
  print("test case: ",test_case)
  parse_result = reg_exp.parse_string(test_case)
  print(parse_result)
