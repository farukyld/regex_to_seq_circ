# see the  discussion:
# see: https://chatgpt.com/share/68202888-90b4-800f-b425-7b2a4e335eee
import re2


def has_partial_match_ending_at_index(string: str, pattern: str) -> list[bool]:
  mathing_end_indices = [False] * len(string)
  for end in range(1, len(string) + 1):
    for start in range(end):
      match_result = re2.fullmatch(pattern, string[start:end])
      if match_result and match_result.end()-match_result.start() > 0:
        mathing_end_indices[end-1] = True
        break
  return mathing_end_indices


def has_full_match_ending_at_index(string: str, pattern: str) -> list[bool]:
  mathing_end_indices = [False] * len(string)
  for end in range(1, len(string) + 1):
    match_result = re2.fullmatch(pattern, string[:end])
    if match_result and match_result.end()-match_result.start() > 0:
      mathing_end_indices[end-1] = True
  return mathing_end_indices


if __name__ == "__main__":
  print('has_partial_match_ending_at_index(string="abacabacabaa", pattern="abacaba+")\n',
        has_partial_match_ending_at_index(string="abacabacabaa", pattern="abacaba+"))
  print('has_full_match_ending_at_index(string="abacabacabaa", pattern="abacaba+")\n',
        has_full_match_ending_at_index(string="abacabacabaa", pattern="abacaba+"))
  print('has_partial_match_ending_at_index(string="aaabaaa", pattern="a+")\n',
        has_partial_match_ending_at_index(string="aaabaaa", pattern="a+"))
