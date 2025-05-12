# see: https://chatgpt.com/share/68055bdd-9638-800f-b288-24e7c614deb0
from frontend.regex_parser import regex_pattern_to_ast


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
