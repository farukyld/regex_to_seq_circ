# see: https://chatgpt.com/share/68055bdd-9638-800f-b288-24e7c614deb0


def insert_semicolon_as_concat(s):
  # Insert ; between atoms/groups where concatenation is implied
  output = ""
  prev = ""
  for c in s:
    if prev:
      if (
          (prev.isalnum() or prev in ')*+?') and
          (c.isalnum() or c == '(')
      ):
        output += ';'
    output += c
    prev = c
  return output


GRN = "\033[32m"
CYN = "\033[36m"
DEF = "\033[0m"


def main():
  from simple_test_cases import regexes_with_semicolon
  from frontend.generate_grep_style import generate_expr
  from frontend.regex_parser import regex_pattern_to_ast
  # see: https://www.geeksforgeeks.org/python-deleting-all-occurrences-of-character/
  tests = [regex.replace(';', '') for regex in regexes_with_semicolon]
  tests += [generate_expr(max_depth=6) for _ in range(10)]
  for test in tests:
    semicolon_inserted = insert_semicolon_as_concat(test)
    print(f"grep style: {GRN}{test}{DEF}, semicolon "
          f"inserted: {CYN}{semicolon_inserted}{DEF}")
    regex_pattern_to_ast(semicolon_inserted)


if __name__ == "__main__":
  main()
