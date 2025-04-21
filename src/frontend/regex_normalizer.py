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



def main():
  from frontend.simple_test_cases import regexes_with_semicolon
  # see: https://www.geeksforgeeks.org/python-deleting-all-occurrences-of-character/
  tests = [regex.replace(';', '') for regex in regexes_with_semicolon]
  for test in tests:
    print(f"grep style: {test}, semicolon "
          f"inserted: {insert_semicolon_as_concat(test)}")

if __name__ == "__main__":
  main()