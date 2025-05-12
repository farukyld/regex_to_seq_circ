from frontend.regex_normalizer import insert_semicolon_as_concat
from frontend.regex_parser import regex_pattern_to_ast
from util.simple_test_cases import regexes_with_semicolon
from util.generate_grep_style import generate_expr
from util.color_print import CYN, DEF, GRN, introduce


if __name__ == "__main__":
  # see: https://www.geeksforgeeks.org/python-deleting-all-occurrences-of-character/
  introduce(__file__)
  tests = [regex.replace(';', '') for regex in regexes_with_semicolon]
  tests += [generate_expr(max_depth=6) for _ in range(10)]
  for test in tests:
    semicolon_inserted = insert_semicolon_as_concat(test)
    print(f"grep style: {GRN}{test}{DEF}, semicolon "
          f"inserted: {CYN}{semicolon_inserted}{DEF}")
    regex_pattern_to_ast(semicolon_inserted)
