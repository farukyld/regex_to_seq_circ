# example from
# see: https://github.com/llvm/circt/blob/main/docs/PyCDE/_index.md
from pycde import Input, Output, Module, System
from pycde import generator
from pycde.types import Bits

from path_shortcuts import generate_output_dir_name

class OrInts(Module):
  a = Input(Bits(32))
  b = Input(Bits(32))
  c = Output(Bits(32))

  @generator
  def construct(self):
    self.c = self.a | self.b


ex_dir = generate_output_dir_name(__file__)

system = System([OrInts], name="ExampleSystem", output_directory=ex_dir,)

if __name__ == "__main__":
  print(system.body)
  system.compile()
  pass
