from enum import Enum, auto


class OperationType(Enum):
  # a
  LITERAL = auto()

  # |
  UNION = auto()

  # ; as in a;b or None as in ab
  CONCAT = auto()

  # *
  ZER_MOR = auto()

  # +
  ONE_MOR = auto()

  # ?
  ZER_ONE = auto()
