# see: https://chatgpt.com/share/68055bdd-9638-800f-b288-24e7c614deb0


import random
from frontend.operation_types import OperationType
import string


def weighted_choice(choices):
  """choices: list of (item, weight) tuples"""
  total = sum(weight for _, weight in choices)
  r = random.uniform(0, total)
  upto = 0
  for item, weight in choices:
    if upto + weight >= r:
      return item
    upto += weight


def generate_expr(max_depth=3):
  if max_depth == 0:
    return random.choice(string.ascii_letters + string.digits)

  productions = [
      (OperationType.LITERAL, 20),      # More likely to stop
      (OperationType.CONCAT, 8),
      (OperationType.UNION, 8),
      (OperationType.ZER_MOR, 2),
      (OperationType.ONE_MOR, 2),
      (OperationType.ZER_ONE, 1),
  ]

  choice = weighted_choice(productions)

  if choice == OperationType.LITERAL:
    return generate_expr(max_depth-1)
  elif choice == OperationType.UNION:
    return f"({generate_expr(max_depth-1)}|{generate_expr(max_depth-1)})"
  elif choice == OperationType.CONCAT:
    return f"{generate_expr(max_depth-1)}{generate_expr(max_depth-1)}"
  elif choice == OperationType.ZER_MOR:
    return f"{generate_expr(max_depth-1)}*"
  elif choice == OperationType.ONE_MOR:
    return f"{generate_expr(max_depth-1)}+"
  elif choice == OperationType.ZER_ONE:
    return f"{generate_expr(max_depth-1)}?"


def main():
  for _ in range(10):
    print(generate_expr())


if __name__ == "__main__":
  main()
