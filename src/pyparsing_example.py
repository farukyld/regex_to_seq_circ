# code generated as an example
# with the help of ChatGPT.
# I am not able to share the conversation link
# because I uploaded a picture in the conversation
# and chatGPT frontend doesn't support
# sharing conversations with image upload currently

import pyparsing as pp
import math
from enum import Enum, auto


# Define an enum for operation types
class OperationType(Enum):
    ADDITION = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    NEGATION = auto()
    SQRT = auto()
    LITERAL = auto()


# Define a class for AST nodes
class ASTNode:
    def __init__(self, operation:OperationType=None, value=None, left=None, right=None):
        self.operation = operation
        self.value = value
        self.left = left  # For binary operators
        self.right = right  # For binary operators

    def __str__(self):
        if self.operation:
            if self.right is not None:
                return f"({self.left.__str__()} {self.operation.name} {self.right.__str__()})"
            elif self.left is not None:
                print(type(self.left))
                return f"({self.operation.name} {self.left.__str__()})"
            else:
                return f"({self.value.__str__()})"
        return str(self.value)


# Define parser
def create_parser():
    integer = pp.Word(pp.nums).setParseAction(lambda t: ASTNode(operation=OperationType.LITERAL, value=int(t[0])))

    # Forward declaration for expressions (since expressions can be nested)
    expr = pp.Forward()

    # Unary operations: sqrt and negation (-)
    # Updated sqrt_expr to return a complete ASTNode
    sqrt_expr = pp.Literal('sqrt').suppress() + expr.setParseAction(lambda t: ASTNode(operation=OperationType.SQRT, left=t[0]))
    unary_expr = pp.Literal('-').setParseAction(lambda: OperationType.NEGATION) + pp.Group(expr)

    # Binary operations: +, -, *, /
    add_op = pp.oneOf('+ -').setParseAction(lambda t: OperationType.ADDITION if t[0] == '+' else OperationType.SUBTRACTION)
    mul_op = pp.oneOf('* /').setParseAction(lambda t: OperationType.MULTIPLICATION if t[0] == '*' else OperationType.DIVISION)

    # Define how to parse binary operations
    term = pp.Group(integer | sqrt_expr | unary_expr)
    factor = pp.infixNotation(term, [
    (mul_op, 2, pp.opAssoc.LEFT, lambda t: ASTNode(operation=t[0][1], left=t[0][0], right=t[0][2])),
    (add_op, 2, pp.opAssoc.LEFT, lambda t: ASTNode(operation=t[0][1], left=t[0][0], right=t[0][2]))
    ])


    # Handling unary sqrt and negation
    expr <<= (unary_expr | sqrt_expr | factor)
    
    return expr


# Function to evaluate AST
def eval_ast(node):
    if node.operation == OperationType.ADDITION:
        return eval_ast(node.left) + eval_ast(node.right)
    elif node.operation == OperationType.SUBTRACTION:
        if node.right:
            return eval_ast(node.left) - eval_ast(node.right)
        else:  # Unary negation
            return -eval_ast(node.left)
    elif node.operation == OperationType.MULTIPLICATION:
        return eval_ast(node.left) * eval_ast(node.right)
    elif node.operation == OperationType.DIVISION:
        return eval_ast(node.left) / eval_ast(node.right)
    elif node.operation == OperationType.SQRT:
        return math.sqrt(eval_ast(node.left))
    elif node.operation == OperationType.NEGATION:
        return -eval_ast(node.left)
    else:
        return node.value


# Test parsing and AST generation
if __name__ == "__main__":
    parser = create_parser()

    test_exprs = [
        "13",
        "sqrt 16",
        "-5 + 3 * 2",
        "sqrt 9 + 4 * 5",
        "10 - sqrt 4"
    ]

    for expr in test_exprs:
        parsed = parser.parseString(expr, parseAll=True)[0]
        print(f"Expression: {expr}")
        print(f"AST: {parsed}")
        print(f"Evaluated Result: {eval_ast(parsed)}\n")
