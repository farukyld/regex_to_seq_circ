BLK = "\033[30m"
RED = "\033[31m"
GRN = "\033[32m"
YLW = "\033[33m"
BLU = "\033[34m"
MGT = "\033[35m"
CYN = "\033[36m"
WTE = "\033[37m"
DEF = "\033[0m"


def print_green(*args):
  print(GRN, end="")
  print(*args)
  print(DEF, end="")


def print_cyan(*args):
  print(CYN, end="")
  print(*args)
  print(DEF, end="")


def print_yellow(*args):
  print(YLW, end="")
  print(*args)
  print(DEF, end="")
