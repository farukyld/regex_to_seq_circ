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


class IncorrectInitialization(Exception):
  pass


class RegexASTNode:
  pass


class RegexASTNode:
  def __init__(self, operation, left: RegexASTNode = None,
               right: RegexASTNode = None, char: str = None, position: int = None):
    """_summary_

    Args:
        left (_type_): left operand (for concatenation and union)
        right (_type_): right operand (for concatenation and union)
        char (_type_): literal value (for regex alphabet characters)
        position (_type_): position in the regex of a char literal used in the algorithm
        operation (_type_): operation type.
          LITERAL for E := a <p>
          UNION   for E := E_1 | E_2 <p>
          CONCAT  for E := E_1 ; E_2 or E := E_1E_2 <p>
          ZER_MOR     E := E_1* <p>
          ONE_MOR     E := E_1+ <p>
          ZER_ONE     E := E_1?
    """
    if operation == OperationType.LITERAL:
      if left != None or right != None:
        raise IncorrectInitialization(
            "literal must not have left or right operands")
      if char == None or position == None:
        raise IncorrectInitialization("literal must have char and position")

    if operation == OperationType.CONCAT or operation == OperationType.UNION:
      if left == None or right == None:
        raise IncorrectInitialization(
            "binary operations must have left and right operands")
      if char != None or position != None:
        raise IncorrectInitialization(
            "binary operations must not have char or position field to be initialized")

    if operation == OperationType.ZER_MOR or operation == OperationType.ONE_MOR or operation == OperationType.ZER_ONE:
      if left == None:
        raise IncorrectInitialization(
            "unary operations must have left operand")
      if right != None or char != None or position != None:
        raise IncorrectInitialization(
            "unary operations must not have right operand or char or position field to be initialized.")
    
    self.operation = operation
    self.char = char
    self.position = position
    self.left = left
    self.right = right
