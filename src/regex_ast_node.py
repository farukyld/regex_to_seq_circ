from enum import Enum, auto

# I had help from chatGPT to improve this code:
# https://chatgpt.com/share/6706e5f1-5f24-800f-9901-058cce09d736


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
  """
  exception raised when an instance of RegexASTNode
  is tried to be initialized with wrong set of arguments
  """
  pass


class RegexASTNode:

  _literals_created = 0

  @classmethod
  def from_literal(cls, char: str):
    cls._literals_created = cls._literals_created + 1
    return cls(operation=OperationType.LITERAL, char=char, position=cls._literals_created)

  @classmethod
  def from_binary(cls, left: 'RegexASTNode', right: 'RegexASTNode', op: str):
    operations = {
        '|': OperationType.UNION,
        ';': OperationType.CONCAT
    }
    return cls(operation=operations[op], left=left, right=right)

  @classmethod
  def from_repetition(cls, left: 'RegexASTNode', op: str):
    operations = {
        '*': OperationType.ZER_MOR,
        '+': OperationType.ONE_MOR,
        '?': OperationType.ZER_ONE
    }
    return cls(operation=operations[op], left=left)

  @classmethod
  def reset_class_variables(cls):
    cls._literals_created = 0

  @staticmethod
  def calculate_skip(node: 'RegexASTNode') -> bool:
    if node.operation == OperationType.LITERAL:
      return False
    elif node.operation == OperationType.UNION:
      return node.left.skip or node.right.skip
    elif node.operation == OperationType.CONCAT:
      return node.left.skip and node.right.skip
    elif node.operation == OperationType.ZER_MOR or node.operation == OperationType.ZER_ONE:
      return True
    elif node.operation == OperationType.ONE_MOR:
      return node.left.skip

  @staticmethod
  def calculate_out(node: 'RegexASTNode') -> frozenset[int]:
    if node.operation == OperationType.LITERAL:
      return frozenset({node.position})
    elif node.operation == OperationType.UNION:
      return node.left.out.union(node.right.out)
    elif node.operation == OperationType.CONCAT:
      # TODO check if this needs to be copy
      return node.left.out.union(
          node.right.out) if node.right.skip else node.right.out.copy()
    elif node.operation == OperationType.ZER_MOR or node.operation == OperationType.ZER_ONE or node.operation == OperationType.ONE_MOR:
      # TODO check if this needs to be copy
      return node.left.out.copy()

  # TODO check if h needs to be set to {0} as default
  @staticmethod
  def calculate_trig(node: 'RegexASTNode', h: frozenset[int] = frozenset({0})) -> set[tuple[int, str, frozenset[int]]]:
    if not isinstance(h, frozenset):
      raise TypeError("h must be type of frozenset")

    if node.operation == OperationType.LITERAL:
      return {(node.position, node.char, h)}
    elif node.operation == OperationType.UNION:
      return RegexASTNode.calculate_trig(node.left, h).union(
          RegexASTNode.calculate_trig(node.right, h))
    elif node.operation == OperationType.CONCAT:
      # TODO check if this needs to be copy
      right_trig_h = node.left.out.union(
          h) if node.left.skip else node.left.out
      return RegexASTNode.calculate_trig(node.left, h).union(
          RegexASTNode.calculate_trig(node.right, right_trig_h))
    elif node.operation == OperationType.ZER_MOR or node.operation == OperationType.ONE_MOR:
      # TODO check if this needs to be copy
      return RegexASTNode.calculate_trig(node.left, node.left.out.union(h))
    elif node.operation == OperationType.ZER_ONE:
      return RegexASTNode.calculate_trig(node.left, h)

  def __init__(self, operation, left: 'RegexASTNode' = None,
               right: 'RegexASTNode' = None, char: str = None, position: int = None):
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
      if len(char) != 1:
        raise IncorrectInitialization("char literal should be lenth of zero")
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
    # TODO hic bir zaman python oop'yi anlayamayacagim.
    # see: https://chatgpt.com/share/6707ab2d-4f50-800f-bd11-1e8b20f91742
    # can we pass incompletely initalized object self to a method?
    # yes. see: https://chatgpt.com/share/6707b078-3528-800f-b912-b78adfa310fc
    self.skip: bool = RegexASTNode.calculate_skip(self)
    self.out: frozenset[int] = RegexASTNode.calculate_out(self)
    self.trig: set[tuple[int, str, frozenset[int]]
                   ] = RegexASTNode.calculate_trig(self)


# for debugging
if __name__ == "__main__":
  literal1 = RegexASTNode.from_literal('a')
  literal2 = RegexASTNode.from_literal('b')
  literal3 = RegexASTNode.from_literal('b')
  literal4 = RegexASTNode.from_literal('b')
  literal5 = RegexASTNode.from_literal('a')
  concat1 = RegexASTNode.from_binary(literal1, literal2, ';')
  union1 = RegexASTNode.from_binary(concat1, literal3, '|')
  zero_or_more1 = RegexASTNode.from_repetition(union1, '*')
  concat2 = RegexASTNode.from_binary(zero_or_more1, literal4, ';')
  concat3 = RegexASTNode.from_binary(concat2, literal5, ';')
  print("done")