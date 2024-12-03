# see: https://github.com/llvm/circt/blob/main/docs/PyCDE/examples/structs.py
from pycde import Input, Output, generator, System, Module
from pycde.types import Bits
from pycde.signals import Struct, BitsSignal

from regex_to_seq_circ.src.backend.examples.pycde_examples.path_shortcuts import generate_output_dir_name


class ExStruct(Struct):
  a: Bits(4)  # vscode python extension warns but pycde package handles it
  # correctly
  b: Bits(32)

  def get_b_xor(self, x: int) -> BitsSignal:
    return self.b ^ Bits(32)(x)


class StructExample(Module):
  inp1 = Input(ExStruct)
  out1 = Output(Bits(32))
  out2 = Output(Bits(4))
  out3 = Output(ExStruct)

  @generator
  def build(self):
    self.out1 = self.inp1.get_b_xor(5432)
    self.out2 = self.inp1.a
    self.out3 = ExStruct(a=self.inp1.a, b=42)


ex_dir = generate_output_dir_name(__file__)


if __name__ == "__main__":
  system = System(StructExample, output_directory=ex_dir)
  system.compile()
