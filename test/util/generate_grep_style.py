# see: https://chatgpt.com/share/68055bdd-9638-800f-b288-24e7c614deb0


import random
import re
from frontend.operation_types import OperationType
import string

from util.color_print import introduce


def maybe_wrap(expr, op_type):
  PAREN_PROBABILITIES = {
      OperationType.UNION: 0.9,
      OperationType.CONCAT: 0.3,
      OperationType.ZER_MOR: 0.2,
      OperationType.ONE_MOR: 0.2,
      OperationType.ZER_ONE: 0.2,
      OperationType.LITERAL: 0.1,
  }
  prob = PAREN_PROBABILITIES.get(op_type, 0)
  if random.random() < prob:
    return f"({expr})"
  return expr


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

  PRODUCTION_WEIGHTS = [
      (OperationType.LITERAL, 20),      # More likely to stop
      (OperationType.CONCAT, 8),
      (OperationType.UNION, 8),
      (OperationType.ZER_MOR, 2),
      (OperationType.ONE_MOR, 2),
      (OperationType.ZER_ONE, 1),
  ]

  choice = weighted_choice(PRODUCTION_WEIGHTS)

  if choice == OperationType.LITERAL:
    return maybe_wrap(generate_expr(max_depth - 1),choice)
  elif choice == OperationType.UNION:
    left = generate_expr(max_depth - 1)
    right = generate_expr(max_depth - 1)
    return maybe_wrap(f"{left}|{right}", choice)
  elif choice == OperationType.CONCAT:
    left = generate_expr(max_depth - 1)
    right = generate_expr(max_depth - 1)
    return maybe_wrap(f"{left}{right}", choice)
  elif choice == OperationType.ZER_MOR:
    inner = generate_expr(max_depth - 1) + "*"
    return maybe_wrap(inner, choice)
  elif choice == OperationType.ONE_MOR:
    inner = generate_expr(max_depth - 1)  + "+"
    return maybe_wrap(inner, choice)
  elif choice == OperationType.ZER_ONE:
    inner = generate_expr(max_depth - 1)  + "?"
    return maybe_wrap(inner, choice)


if __name__ == "__main__":
  introduce(__file__)
  for _ in range(10):
    expr = generate_expr()
    print(expr)
    re.compile(expr)
